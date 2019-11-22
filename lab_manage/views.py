from . import *

@lab_manage.route('/new_lab', methods=['GET', 'POST'])
@login_required
@admin_required
def newLab():
    form = newLabForm()
    if form.validate_on_submit():
        exist = Laboratory.query.filter_by(id=request.form.get('labId')).first()
        if exist is not None:
            flash(u'该实验室编号已经存在,请重新填写')
        else:
            try:
                lab = Laboratory()
                lab.id = request.form.get('labId')
                lab.lName = request.form.get('labName')
                lab.aId = current_user.id
                lab.cCount = int(request.form.get('labcCount'))

                db.session.add(lab)
                flash(u'实验室信息添加成功！')
                db.session.commit()
            except :
                db.session.rollback()
                flash(u'实验室信息添加失败:(')
                
            finally:
                return redirect(url_for('lab_manage.newLab'))
    return render_template('new-lab.html', name=session.get('name'),role=session['role'], form=form)    

@lab_manage.route('/delete_lab', methods=['GET', 'POST'])
@login_required
@admin_required
def deleteLab():
    form = deleteLabForm()
    flash(u'注意:该实验室电脑将被设置为闲置')
    if form.validate_on_submit():
        exist = Laboratory.query.filter_by(id=request.form.get('labId')).first()
        if exist is None:
            flash(u'该实验室编号不存在,请重新填写')
        else:
            try:
                # 移除电脑
                db.session.execute(remove_computer_from(exist.id.strip()))
                db.session.commit()
                db.session.delete(exist)
                flash(u'实验室信息删除成功！')
                db.session.commit()
            except :
                db.session.rollback()
                flash(u'实验室信息添加失败:(')
                
            finally:
                return redirect(url_for('lab_manage.deleteLab'))
    return render_template('delete-lab.html', name=session.get('name'),role=session['role'], form=form)    


@lab_manage.route('/lab_Set',methods=['GET','POST'])
@login_required
@admin_required
def labSet():
    form=labSetForm() #虚表单
    return render_template('lab-set.html',name=session.get('name'),role=session['role'],form=form)

@lab_manage.route('/lab_computer',methods=['GET','POST'])
@login_required
@admin_required
def labComputer():
    return render_template('lab-computer.html',name=session.get('name'),role=session['role'])

@lab_manage.route('/lab_info/',methods=['GET','POST'])
@login_required
def labInfo():
    labId = request.args.get('labId')
    class tmp:
        pass
    lab = tmp()
    res = db.session.query(Laboratory).filter_by(id=labId).first()
    if res is not None:
        lab.id = res.id
        lab.name = res.lName
    else:
        return 'fail',404
    return render_template('lab-info.html',name=session.get('name'),role=session['role'],labId=labId,lab=lab)

