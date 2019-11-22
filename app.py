
from . import *
from .model import Adminitrator,Teacher
@login_manager.user_loader
def load_admin(id):
    if session['role']=='admin':
        return Adminitrator.query.get(str(id))
    elif session['role']=='teacher':
        return Teacher.query.get(str(id))


@app.route('/',methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        if form.role.data == 'admin':
            user = Adminitrator.query.filter_by(id=form.account.data).first()
            if user is None or not user.verify_password(form.password.data):
                flash('账号或密码错误！')
                return redirect(url_for('login'))
            else:
                login_user(user)
                session['id'] = user.id
                session['name'] = user.aName
                session['role'] = 'admin'
                return redirect(url_for('main.admin_view'))


        elif form.role.data == 'teacher':
            user = Teacher.query.filter_by(id=form.account.data).first()

            if user is None or not user.verify_password(form.password.data):
                flash('账号或密码错误！')
                return redirect(url_for('login'))
            else:
                status = login_user(user)
                session['id'] = user.id
                session['name'] = user.tName
                session['role'] = 'teacher'
                return redirect(url_for('main.teacher_view'))
            
    return render_template('login.html', form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
if __name__ == '__main__':
    app.run(debug=True)