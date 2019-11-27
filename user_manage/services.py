from . import *
@user_manage.route('/show_user',methods=['GET','POST'])
@login_required
@admin_required
def showUser():
    # TODO 显示用户数据
    users=db.session.query(Teacher).order_by(Teacher.tName).all()
    data=[]
    for user in users:
        item={'id':user.id,
                'Dept':user.Dept,
                'Position':user.Position,
                'tName':user.tName,
                }
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)

@user_manage.route('/del_user',methods=['GET','POST'])
@login_required
@admin_required
def del_user():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            db.session.execute(delete_user(id))
            db.session.commit()
            success+=1
        except:
            db.session.rollback()
    if success > 0:
        return str(success),200
    else:
        return 'fail',404   
        

@user_manage.route('/reset_user',methods=['GET','POST'])
@login_required
@admin_required
def reset_user():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            db.session.execute(reset_user_pwd(id))
            db.session.commit()
            success+=1
        except:
            db.session.rollback()
    if success > 0:
        return str(success),200
    else:
        return 'fail',404   
      