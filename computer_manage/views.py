from . import *

@computer_manage.route('/new_computer',methods = ['GET','POST'])
@login_required
@admin_required
def newComputer():
    form = newComputerForm()
    success=0
    if form.validate_on_submit():
        count=int(request.form.get('count'))
        for i in range(count):
            try:
                # 获取id
                result = db.session.execute(max_computer).fetchall()
                if(result[0][0] is None):
                    count=1
                else:
                    count = result[0][0]+1
                cId = f'c{time.strftime("%Y%m%d",time.localtime())}/{count}'
                computer = Computer()
                computer.id = cId
                computer.aId=current_user.id
                computer.cName = request.form.get('cName')
                computer.producer = request.form.get('cProducer')
                computer.mm = request.form.get('cMm')
                computer.cpu = request.form.get('cpu')
                db.session.add(computer)
                db.session.commit() 
                # TODO 添加系统信息插入
                computer_sys = ComputerSys()
                computer_sys.cId = cId
                computer_sys.sys = request.form.get('cSys')
                db.session.add(computer_sys)
                db.session.commit()
                success+=1
            except:
                db.session.rollback()
                # flash(u'电脑信息添加失败:(')
        flash("成功登记"+str(success)+"台电脑")

                
    return render_template('new-computer.html', name=session.get('name'),role=session['role'], form=form)    

@computer_manage.route('/lab_computer',methods=['GET','POST'])
@login_required
@admin_required
def labComputer():
    return render_template('lab-computer.html',name=session.get('name'),role=session['role'])

@computer_manage.route('/remove_computer',methods=['GET','POST'])
@login_required
@admin_required
def removeComputer():
    form=newComputerForm()
    id=request.form.get('cId')
    flash("注意:点击提交即删除，没有确认步骤，请确认好再点击提交")
    if form.validate_on_submit():
            db.session.execute(delete_computer(id))
            try:
                db.session.commit()
                flash('删除成功')
            except:
                db.session.rollback()
                flash('删除失败:(,没有这个用户或者其它错误')
    return render_template("remove-computer.html",form=form,name=session.get('name'),role=session['role'])
