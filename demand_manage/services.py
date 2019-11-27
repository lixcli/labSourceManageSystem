from . import *
@demand_manage.route('/close_tDemand',methods=['GET','POST'])
@login_required
@user_required
def close_tDemand():
    limit = int(request.args['limit'])
    page = int(request.args['page'])
    tId=current_user.id
    # sql=close_teacher_demand(tId)
    # demands=db.session.execute(sql)
    demands=db.session.query(Demand).filter(and_(Demand.tId==tId , Demand.closeDate != None)).\
                                    order_by('id').limit(limit).offset((page-1)*limit).all()
    demands_len = db.session.query(Demand).filter(and_(Demand.tId==tId , Demand.closeDate != None)).count()
    data=[]
    for demand in demands:
        item={'id':demand.id,
                'response':demand.response,
                'closeDate':demand.closeDate,
                'lId':demand.lId,
                'content':demand.content,
                'aId':demand.aId}
        data.append(item)
    table_result={"code":0,"msg":None,"count":demands_len,"data":data}
    return jsonify(table_result)

@demand_manage.route('/open_tDemand',methods=['GET','POST'])
@login_required
@user_required
def open_tDemand():
    tId=current_user.id
    limit = int(request.args['limit'])
    page = int(request.args['page'])
    # sql=open_teacher_demand(tId)
    # demands=db.session.execute(sql)
    demands = db.session.query(Demand).filter(and_(Demand.tId == current_user.id, Demand.closeDate == None)).\
                                        order_by('id').limit(limit).offset((page-1)*limit).all()
    demands_len = db.session.query(Demand).filter(and_(Demand.tId == current_user.id , Demand.closeDate == None)).count()
    data=[]
    for demand in demands:
        item={'id':demand.id,
                'response':demand.response,
                'closeDate':demand.closeDate,
                'lId':demand.lId,
                'status':'受理' if demand.aId is not None else '未受理',
                'content':demand.content}
        data.append(item)
    table_result={"code":0,"msg":None,"count":demands_len,"data":data}
    return jsonify(table_result)

@demand_manage.route('/del_demand',methods=['GET','POST'])
@login_required
def del_demand():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            Demand.query.filter_by(id=id).delete()
            db.session.commit()
            success+=1
        except:
            db.session.rollback()
    if success>0:
        return str(success),200
    else:
        return 'fail',404


@demand_manage.route('/check_open_demand',methods=['GET','POST'])
@login_required
@admin_required
def check_open_Demand():
    # data=getDemands(all_open_demand)
    limit = int(request.args['limit'])
    page = int(request.args['page'])
    demands = db.session.query(Demand).filter(Demand.closeDate == None).\
                                        order_by('id').limit(limit).offset((page-1)*limit)
    demands_len = db.session.query(Demand).filter(Demand.closeDate == None).count()
    data=[]
    for demand in demands:
        item={'id':demand.id,
                'response':demand.response,
                'closeDate':demand.closeDate,
                'lId':demand.lId,
                'aId':demand.aId,
                'tId':demand.tId,
                'status':'受理' if demand.aId is not None else '未受理',
                'content':demand.content}
        data.append(item)
    table_result={"code":0,"msg":None,"count":demands_len,"data":data}
    return jsonify(table_result)
  

@demand_manage.route('/check_accepted_demand',methods=['GET','POST'])
@login_required
@admin_required  
def check_accepted_demand():
    # sql=all_m_accepted_demand(current_user.id)
    limit = int(request.args['limit'])
    page = int(request.args['page'])
    demands = db.session.query(Demand).filter(and_(Demand.closeDate == None , Demand.aId==current_user.id)).\
                                        order_by('id').limit(limit).offset((page-1)*limit)
    demands_len = db.session.query(Demand).filter(and_(Demand.closeDate == None , Demand.aId==current_user.id)).count()   
    data=[]
    for demand in demands:
        item={'id':demand.id,
                'response':demand.response,
                'closeDate':demand.closeDate,
                'lId':demand.lId,
                'aId':demand.aId,
                'tId':demand.tId,
                'status':'受理' if demand.aId is not None else '未受理',
                'content':demand.content}
        data.append(item)
    table_result={"code":0,"msg":None,"count":demands_len,"data":data}
    return jsonify(table_result)
@demand_manage.route('/check_close_demand',methods=['GET','POST'])
@login_required
@admin_required  
def check_close_aDemand():
    limit = int(request.args['limit'])
    page = int(request.args['page'])
    demands = db.session.query(Demand).filter(and_(Demand.closeDate != None , Demand.aId==current_user.id)).\
                                        order_by('id').limit(limit).offset((page-1)*limit)
    demands_len = db.session.query(Demand).filter(and_(Demand.closeDate != None , Demand.aId==current_user.id)).count()   
    data=[]
    for demand in demands:
        item={'id':demand.id,
                'response':demand.response,
                'closeDate':demand.closeDate,
                'lId':demand.lId,
                'aId':demand.aId,
                'tId':demand.tId,
                'status':'受理' if demand.aId is not None else '未受理',
                'content':demand.content}
        data.append(item)
    table_result={"code":0,"msg":None,"count":demands_len,"data":data}
    return jsonify(table_result)

@demand_manage.route('/accept_demand',methods=['GET','POST'])
@login_required
@admin_required
def accept_demand():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            db.session.execute(set_demand_accept(id,current_user.id))
            db.session.commit()
            success+=1
        except:
            db.rollback()
    if success > 0:
        return str(success),200
    else:
        return 'fail',404

@demand_manage.route('/cancel_accept_demand',methods=['GET','POST'])
@login_required
@admin_required
def del_acDemand():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            db.session.execute(cancel_demand_accept(id,current_user.id))
            db.session.commit()
            success+=1
        except:
            db.rollback()
    if success > 0:
        return str(success),200
    else:
        return 'fail',404

@demand_manage.route('/close_acDemand',methods=['GET','POST'])
@login_required
@admin_required
def close_acDemand():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            db.session.execute(close_accepted_demand(id))
            db.session.commit()
            success+=1
        except:
            db.session.rollback()
    if success > 0:
        return str(success),200
    else:
        return 'fail',404    

@demand_manage.route('/set_response',methods=['GET','POST'])
@login_required
@admin_required
def set_response():
    Ids=json.loads(request.form.get('Ids'))[0]
    res=request.form.get('res')
    success=0
    try:
        db.session.execute(set_demand_response(Ids,res))
        db.session.commit()
        success+=1
    except:
        db.session.rollback()
        
    if success > 0:
        return str(success),200
    else:
        return 'fail',404  

