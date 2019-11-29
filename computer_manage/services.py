from .  import *

@computer_manage.route('/check_uninstall_by_sId',methods=['GET','POST'])
@login_required
def check_uninstall_by_sId():
    ids = json.loads(request.args.get('ids'))
    ids = map(repr,ids)
    labId = request.args.get('labId')
    data =[]
    computers = db.session.execute(not_have_software_of(','.join(ids),labId))
    for computer in computers:
        # relate_sys = ";".join(db.session.query(ComputerSys).filter(ComputerSys.cId==computer.id).all())
        item={
            'id':computer.id,
            'cName':computer.cName,
            'producer':computer.producer,
            'aId':computer.aId,
            'cpu':computer.cpu,
            'normal':'正常'if computer.normal==1 else '异常',
            'cMm':computer.mm,
            # 'cSys':relate_sys
        }
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)
    
@computer_manage.route('/check_install_by_sId',methods=['GET','POST'])
@login_required
def check_install_by_sId():
    ids = json.loads(request.args.get('ids'))
    ids = map(repr,ids)
    labId = request.args.get('labId')
    data =[]
    computers = db.session.execute(have_software_of(','.join(ids),labId))
    for computer in computers:
        # relate_sys = ";".join(db.session.query(ComputerSys).filter(ComputerSys.cId==computer.id).all())
        item={
            'id':computer.id,
            'cName':computer.cName,
            'producer':computer.producer,
            'aId':computer.aId,
            'cpu':computer.cpu,
            'normal':'正常'if computer.normal==1 else '异常',
            'cMm':computer.mm,
            # 'cSys':relate_sys
        }
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)
    

@computer_manage.route('/check_avil_computer',methods=['GET','POST'])
@login_required
@admin_required
def check_avil_computer():
    page=int(request.args['page'])
    limit=int(request.args['limit'])
    data =[]
    computer_len = db.session.query(Computer).filter(Computer.lId==None).count()
    # computer_len=db.session.execute(count_avil_computer).fetchall()[0][0]
    computers = db.session.query(Computer).filter(Computer.lId==None).order_by('id').limit(limit).offset((page-1)*limit).all()

    # computers = db.session.execute(avil_computer(page,limit))
    for computer in computers:
        # relate_sys=db.session.query(ComputerSys).filter_by(cId=computer.id).all()
        item={
            'id':computer.id,
            'cName':computer.cName,
            'producer':computer.producer,
            'aId':computer.aId,
            'cpu':computer.cpu,
            'normal':'正常'if computer.normal==1 else '异常',
            'cMm':computer.mm,
            # 'cSys':relate_sys
        }
        data.append(item)
    table_result={"code":0,"msg":None,"count":computer_len,"data":data}
    return jsonify(table_result)

@computer_manage.route('/check_own_computer',methods=['GET','POST'])
@login_required
def check_own_computer():
    labId = request.args.get('labId')
    data =[]
    limit=int(request.args['limit'])
    page=int(request.args['page'])
    main_search = request.args.get('main_search')
    # computers = db.session.execute(lab_computer_of(labId))
    if main_search is None:
        computers = db.session.query(Computer).filter_by(lId=labId).order_by('id').limit(limit).offset((page-1)*limit).all()
        computers_len = db.session.query(Computer).filter_by(lId=labId).count()
    elif main_search is not None:
        main_search = '%'.join(list(main_search))
        if len(main_search)>0:
            main_search = '%'+main_search+'%'
        computers = db.session.query(Computer).filter(and_(Computer.cName.like(main_search),Computer.lId==labId)).order_by('id').limit(limit).offset((page-1)*limit).all()
        computers_len = db.session.query(Computer).filter(and_(Computer.cName.like(main_search),Computer.lId==labId)).count()
        

    for computer in computers:
        item={
            'id':computer.id,
            'cName':computer.cName,
            'producer':computer.producer,
            'aId':computer.aId,
            'cpu':computer.cpu,
            'normal':'正常'if computer.normal==1 else '异常',
            'cMm':computer.mm,
        }
        data.append(item)
    table_result={"code":0,"msg":None,"count":computers_len,"data":data}
    return jsonify(table_result)

@computer_manage.route('/import_computers_for_lab',methods=['GET','POST'])
@login_required
@admin_required
def import_computers_for_lab():
    cIds=json.loads(request.form.get('cIds'))
    labId = request.form.get('labId')
    success=0

    # 先求已有电脑数和最大容纳电脑数
    own_computers_count=Computer.query.filter_by(lId=labId).count()
    max_computer_count=Laboratory.query.filter_by(id=labId).first().cCount
    if(own_computers_count >= max_computer_count):
        return 'full',404
    for cId in cIds:
        try:
            db.session.execute(import_computer(cId,labId))
            own_computers_count+=1
            if(own_computers_count>max_computer_count):
                raise FullError
            db.session.commit()
            success+=1
        except FullError:
            db.session.rollback()
            break

        except:
            db.session.rollback()
    if(success>0):
        return str(success),200
    else:
        return 'fail',404

@computer_manage.route('/export_computers_for_lab',methods=['GET','POST'])
@login_required
@admin_required
def export_computers_for_lab():
    cIds=json.loads(request.form.get('cIds'))
    success=0
    for cId in cIds:
        try:
            db.session.execute(export_computer(cId))
            db.session.commit()
            success+=1
        except:
            db.session.rollback()
    if(success>0):
        return str(success),200
    else:
        return 'fail',404

@computer_manage.route('/del_computer',methods=['GET','POST'])
@login_required
@admin_required
def del_computer():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            db.session.execute(delete_computer(id))
            db.session.commit()
            success+=1
        except:
            db.session.rollback()
    if success > 0:
        return str(success),200
    else:
        return 'fail',404   
            