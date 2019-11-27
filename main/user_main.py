from . import *
@main.route('/user')
@user_required
@login_required
def teacher_view():
    return render_template('teacher-index.html',name=session.get('name'),role=session['role'])
