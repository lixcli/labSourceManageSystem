from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from . import *
@main.route('/admin')
@login_required
@admin_required
def admin_view():
    return render_template('admin-index.html',name=session.get('name'),role=session['role'])