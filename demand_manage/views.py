from . import *


@demand_manage.route('/post_demand',methods=['GET','POST'])
@login_required
@user_required
def post_demand():
    form=DemandForm()
    if form.validate_on_submit():
        demand=Demand()
        demand.aId=None
        demand.tId=current_user.id
        demand.response=None
        demand.lId=form.labId.data
        demand.inDate=time.strftime("%Y-%m-%d",time.localtime())
        id=db.session.execute(max_today_demand).fetchall()[0][0]
        if(id is None):
            demand.id=f'd{time.strftime("%Y%m%d",time.localtime())}/1'
        else:
            id+=1
            demand.id=f'd{time.strftime("%Y%m%d",time.localtime())}/{id}'
        demand.content=form.demand.data
        try:
            db.session.add(demand)
            db.session.commit()
            flash('提交成功')
        except Exception as e:
            print(repr(e))
            db.session.rollback()
            flash('提交失败:(')
    return render_template('demand-post.html', name=session.get('name'),role=session['role'], form=form) 

@demand_manage.route('/show_tDemand',methods=['GET','POST'])
@login_required
@user_required
def show_tDemand():
    return render_template('demand-show.html', name=session.get('name'),role=session['role'])

@demand_manage.route('/oper_demand',methods=['GET','POST'])
@login_required
@admin_required
def operDemand():
    return render_template('demand-oper.html', name=session.get('name'),role=session['role'])

