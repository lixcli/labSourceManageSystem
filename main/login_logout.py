
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from . import *

@login_manager.user_loader
def load_admin(id):
    if session['role']=='admin':
        return Adminitrator.query.get(str(id))
    elif session['role']=='teacher':
        return Teacher.query.get(str(id))


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出！')
    return redirect(url_for('login'))
