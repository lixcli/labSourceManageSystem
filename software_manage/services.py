from . import *

@soft_manage.route('/check_softwares',methods=['GET','POST'])
@login_required
def check_softwares():

    limit=int(request.args['limit'])
    page=int(request.args['page'])
    labId = request.args.get('labId')
    main_search = request.args.get('main_search')
    info_search = request.args.get('info_search')
    if labId is None and main_search is None and info_search is None:
        softwares=db.session.query(Software).order_by('id').limit(limit).offset((page-1)*limit).all()
        softwares_len=db.session.query(Software).count()
    elif main_search is not None:
        main_search = '%'.join(list(main_search))
        if len(main_search)>0:
            main_search = '%'+main_search+'%'
        softwares=db.session.query(Software).filter(Software.sName.like(main_search)).order_by('id').limit(limit).offset((page-1)*limit).all()
        softwares_len=db.session.query(Software).filter(Software.sName.like(main_search)).count()
    elif info_search is not None:
        info_search = '%'.join(list(info_search))
        if len(info_search)>0:
            info_search = '%'+info_search+'%'
        cIds = db.session.query(Computer.id).filter_by(lId=labId)
        sIds = db.session.query(InstallList.sId).filter(InstallList.cId.in_(cIds)).distinct()
        softwares = db.session.query(Software).filter(and_(Software.sName.like(info_search),Software.id.in_(sIds))).order_by('id').\
                                    limit(limit).offset((page-1)*(limit)).all()
        softwares_len = sIds.count()
    elif labId is not None:
        cIds = db.session.query(Computer.id).filter_by(lId=labId)
        sIds = db.session.query(InstallList.sId).filter(InstallList.cId.in_(cIds)).distinct()
        
        softwares = db.session.query(Software).filter(Software.id.in_(sIds)).order_by('id').\
                                    limit(limit).offset((page-1)*(limit)).all()
        softwares_len = sIds.count()
    data=[]
    for software in softwares:
        item={'id':software.id,
                    'sName':software.sName,
                    'version':software.version,
                    'sysType':software.sysType,
                    'aId':software.aId}
        data.append(item)
    table_result = {"code": 0, "msg": None, "count": softwares_len, "data": data}
    return jsonify(table_result)

@soft_manage.route('/delete_softwares',methods=['POST'])
@login_required
@admin_required
def delete_check_softwares():
    del_ids = json.loads(request.form.get('ids'))

    try:
        for id in del_ids:
            db.session.execute(delete_software(repr(id)))
        db.session.commit()
        return 'success',200
    except:
        db.session.rollback()
        return 'fail',404

@soft_manage.route('/check_softwares_by_names',methods=['GET','POST'])
@login_required
def check_softwares_by_names():
    sName = json.loads(request.args.get('names'))
    # sName = map(repr,sName)
    softwares = db.session.query(Software).filter(Software.sName.in_(sName)).all()
    # softwares = db.session.execute(exist_software_by_name(','.join(sName)))
    data=[]
    for software in softwares:
        item={'id':software.id,
                'sName':software.sName,
                'sysType':software.sysType,
                'version':software.version,
                'aId':software.aId}
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)
    

@soft_manage.route('/install_softwares_for_lab',methods=['GET','POST'])
@login_required
@admin_required
def install_softwares_for_lab():
    cIds = json.loads(request.form.get('cIds'))
    sIds = json.loads(request.form.get('sIds'))
    success=0
    for sId in sIds:
        for cId in cIds:

            count = db.session.execute(max_today_install).fetchall()
            if(count[0][0] is None):
                count=0
            else:
                count = count[0][0]    
            try:
                sys=db.session.query(Software).filter_by(id=sId).first().sysType
                # db.session.close()
                db.session.execute(install(sId,cId,current_user.id,sys,count+1))
                db.session.commit()
                success+=1
            except:
                db.session.rollback()
    if(success>0):
        return str(success),200
    else:
        return 'fail',404

@soft_manage.route('/uninstall_softwares_for_lab',methods=['GET','POST'])
@login_required
@admin_required
def uninstall_softwares_for_lab():
    cIds = json.loads(request.form.get('cIds'))
    sIds = json.loads(request.form.get('sIds'))
    # labId = request.form.get('labId')
    # fail=[]
    success=0
    for sId in sIds:
        for cId in cIds:
            try:
                # 求id
                db.session.execute(uninstall(sId,cId))
                db.session.commit()
                success+=1
            except:
                db.session.rollback()
    if(success>0):
        return str(success),200
    else:
        return 'fail',404

@soft_manage.route('/soft_set',methods=['POST'])
@login_required
@admin_required
def soft_set():
    sId = request.form.get('sId')
    software = db.session.query(Software).filter_by(id=sId).first()
    software.sysType = request.form.get('sSysType')
    software.sName = request.form.get('sName')
    software.version = request.form.get('sVersion')
    try:

        db.session.commit()
        return "success", 200
    except:
        db.session.rollback()
        return 'fail',404

@soft_manage.route('/lab_softwares/<labId>',methods=['GET','POST'])
@login_required
def get_lab_software(lab_id):
    limit = int(request.args['limit'])
    page = int(request.args['page'])

    cIds = db.session.query(Computer.id).filter_by(id=lab_id)
    sIds = db.session.query(InstallList.sId).filter(InstallList.cId.in_(cIds))
    softwares = db.session.query(Software).filter(Software.id.in_(sIds)).order_by('id').\
                                limit(limit).offset((page-1)*(limit)).all()
    softwares_len = sIds.count()
    data = []
    for software in softwares:
        item={'id':software.id,
                    'sName':software.sName,
                    'version':software.version,
                    'sysType':software.sysType,
                    'aId':software.aId}
        data.append(item)
    table_result = {"code": 0, "msg": None, "count": softwares_len, "data": data}
    return jsonify(table_result)