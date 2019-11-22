from . import *
from sqlalchemy import func
@lab_manage.route('/check_labs',methods=['GET','POST'])
@login_required
def check_labs():

    limit=int(request.args['limit'])
    page=int(request.args['page'])
    sId = request.args.get('sId')
    info_search = request.args.get('info_search')
    main_search = request.args.get('main_search')
    if sId is  None  and main_search is None and info_search is None:
        labs=db.session.query(Laboratory).order_by('id').limit(limit).offset((page-1)*limit).all()
        # labs_len=labs.count()
    elif info_search is not None:
        info_search = '%'.join(list(info_search))
        if len(info_search)>0:
            info_search = '%'+info_search+'%' 
        cIds = db.session.query(InstallList.cId).filter(InstallList.sId==sId)
        lIds = db.session.query(Computer.lId).filter(Computer.id.in_(cIds))
        labs = db.session.query(Laboratory)\
                           .filter(and_(Laboratory.lName.like(info_search),Laboratory.id.in_(lIds))).all()

                   
    elif sId is not None:
        cIds = db.session.query(InstallList.cId).filter(InstallList.sId==sId)
        lIds = db.session.query(Computer.lId).filter(Computer.id.in_(cIds))
        labs = db.session.query(Laboratory)\
                           .filter(Laboratory.id.in_(lIds)).all()
    
    elif main_search is not None:
        main_search = '%'.join(list(main_search))
        if len(main_search)>0:
            main_search = '%'+main_search+'%'
        labs=db.session.query(Laboratory).filter(Laboratory.lName.like(main_search)).order_by('id').limit(limit).offset((page-1)*limit).all()
 

    labs_len=len(labs)
    data=[]
    for lab in labs:
        item={'id':lab.id,
                    'lName':lab.lName,
                    'aId':lab.aId,
                    'count':lab.cCount}
        data.append(item)
    table_result = {"code": 0, "msg": None, "count": labs_len, "data": data}
    return jsonify(table_result)    
    

@lab_manage.route('/delete_labs',methods=['POST'])
@login_required
@admin_required
def delete_check_labs():
    del_ids = json.loads(request.form.get('ids'))

    try:
        for id in del_ids:
            db.session.execute(delete_lab(repr(id)))
        db.session.commit()
        return 'success',200
    except:
        db.session.rollback()
        return 'fail',404
