from . import *

@soft_manage.route('/new-software',methods = ['GET','POST'])
@login_required
@admin_required
def newSoftware():
    form = newSoftwareForm()
    if form.validate_on_submit():
        exist = Software.query.filter_by(sName=request.form.get('sName'),version=request.form.get('sVersion')).first() #根据版本和名字确定
        if exist is not None:
            flash(u'该版本软件已经存在,请重新填写')
        else:
            try:
                # 获取id
                result = db.session.execute(max_software).fetchall()
                if(result[0][0] is None):
                    count=0
                else:
                    count = result[0][0]+1
                sId = f's{time.strftime("%Y%m%d",time.localtime())}/{count}'
                software = Software()
                software.id = sId
                software.aId=current_user.id
                software.sysType = request.form.get('sSysType')
                software.sName = request.form.get('sName')
                software.version = request.form.get('sVersion')
                db.session.add(software)
                db.session.commit()
                flash(u'软件信息添加成功！')
            except:
                db.session.rollback()
                flash(u'软件添加失败:(')
                
            finally:
                return redirect(url_for('soft_manage.newSoftware'))
    return render_template('new-software.html', name=session.get('name'),role=session['role'], form=form)    


@soft_manage.route('/soft_info/',methods=['GET','POST'])
@login_required
# @admin_required
def softInfo():
    sId = request.args.get('sId')
    form = newSoftwareForm()
    class tmp:
        pass
    soft = tmp()
    res = db.session.query(Software).filter_by(id=sId).first()
    if res is not None:
        form.sName = soft.sName = res.sName
        form.sysType = soft.sysType = res.sysType
        form.sVersion = soft.version = res.version
    else:
        return 'fail',404


    return render_template('soft-info.html',name=session.get('name'),role=session['role'],sId=sId,soft=soft,form=form)

