from . import *
@user_manage.route('/manage_user',methods=['GET','POST'])
@login_required
@admin_required
def manage_user():
    # TODO 用户管理界面操作
    form=NewUserForm()
    
    if form.validate_on_submit():
        # 插入用户数据
        account=form.account.data
        if(form.choise.data=='del'):
            db.session.execute(delete_user(account))
            try:
                db.session.commit()
                flash('删除成功')
            except:
                db.session.rollback()
                flash('删除失败:(,没有这个用户或者其它错误')
        elif form.choise.data=='reset':
            db.session.execute(reset_user_pwd(account))
            try:
                db.session.commit()
                flash('重置成功')
            except:
                db.session.rollback()
                flash('重置失败:(,没有这个用户或者其它错误')            
            
            
        elif(form.choise.data=='insert'):
            tName=form.tName.data
            password=form.password.data
            Dept=form.Dept.data
            Position=form.Position.data
            if tName=='' or password=='' or Dept=='' or Position=='':
                flash("用户数据不能为空")
                redirect(url_for("user_manage.manage_user"))
            else:
                teacher=Teacher(account,generate_password_hash(password),tName,Dept,Position)
                db.session.add(teacher)
                try:
                    db.session.commit()
                    flash('登记成功')
                except:
                    db.session.rollback()
                    flash('登记失败')
                redirect(url_for('user_manage.manage_user'))
    return render_template("manage-user.html",form=form,name=session.get('name'),role=session['role'])

@user_manage.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.password2.data != form.password.data:
        flash(u'两次密码不一致！')
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            password = generate_password_hash(form.password2.data)
            if session['role']=='admin':
                db.session.execute(set_admin_passwd(current_user.id,password))
            elif session['role']=='teacher':
                db.session.execute(set_teacher_passwd(current_user.id,password))
            try:
                db.session.commit()
                flash(u'已成功修改密码！')
                if(session['role'] == 'admin'):    
                    return redirect(url_for('main.logout'))
                if(session['role'] == 'teacher'):    
                    return redirect(url_for('main.logout'))
            except:
                db.session.rollback()
                flash(u'修改失败')
                

        else:
            flash(u'原密码输入错误，修改失败！')
    return render_template("change-password.html", form=form,name=session.get('name'),role=session['role'])
