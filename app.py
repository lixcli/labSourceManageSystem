from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify,abort
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import sqlalchemy as sa
from flask_script import Manager, Shell
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mssql import  \
    BIGINT, BINARY, BIT, CHAR, DATE, DATETIME, DATETIME2, \
    DATETIMEOFFSET, DECIMAL, FLOAT, IMAGE, INTEGER, MONEY, \
    NCHAR, NTEXT, NUMERIC, NVARCHAR, REAL, SMALLDATETIME, \
    SMALLINT, SMALLMONEY, SQL_VARIANT, TEXT, TIME, \
    TIMESTAMP, TINYINT, UNIQUEIDENTIFIER, VARBINARY, VARCHAR
from sqlalchemy import CheckConstraint,ForeignKey,PrimaryKeyConstraint
import os
from sql_for_lab import *
# import pandas as pd
from form import *
import time
import json
import zlib
app = Flask(__name__)

# app.run(debug=True)
manager = Manager(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
user = 'sa'
pwd = 'admin'
server = 'localhost'
dbname = 'DB_laboratory'
driver = "ODBC Driver 17 for SQL Server"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{user}:{pwd}@{server}/{dbname}?driver={driver}"
basedir = os.path.abspath(os.path.dirname(__file__))
# db_engine, tables = get_database()
db = SQLAlchemy(app)

def make_shell_context():
    return dict(app=app, db=db, Adminitrator=Adminitrator, Teacher=Teacher)
    # pass

manager.add_command("shell", Shell(make_context=make_shell_context))

# stop visitor
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.login_message = u"请先登录。"

class FullError(Exception):
    pass

# 定义用户权限
class Permission:
    ADMIN = 0x01
    USER = 0x02

def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            # 判断用户是否具有某特定权限，如果没有则抛出403错误
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(func):
    # 相当于调用decorator(func)
    return permission_required(Permission.ADMIN)(func)

def user_required(func):
    return permission_required(Permission.USER)(func)

class Adminitrator(db.Model,UserMixin): 
    __tablename__='Adminitrator'
# 简单起见 管理员都是全权限
    id = db.Column(CHAR(16), primary_key=True)
    pwd = db.Column(CHAR(128),nullable=False)
    aName = db.Column(NVARCHAR(32),nullable=False)
    permission=Permission.ADMIN

    def __init__(self, id, pwd, aName):
        self.id = id
        self.aName = aName
        self.pwd = pwd
        
        # self.right = right

    def get_id(self):
        return self.id
    def can(self,permission):
        return (self.permission& permission)==permission
    def verify_password(self, pwd):
        # pwd_hash=generate_password_hash(pwd)
        if check_password_hash(self.pwd.strip(),pwd.strip()):
            return True
        else:
            return False

    def __repr__(self):
        return '<Adminitrator %r>' % self.aName

class Teacher(db.Model,UserMixin):
    __tablename__='Teacher'
    id = db.Column(CHAR(16), primary_key=True)
    pwd = db.Column(CHAR(128),nullable=False)
    tName = db.Column(NVARCHAR(32),nullable=False) 
    Dept = db.Column(NVARCHAR(64),nullable=False) # 系别
    Position = db.Column(NVARCHAR(8),nullable=False) # 职位: 教授 副教授 助理教授 讲师 辅导员
    permission=Permission.USER
    def __init__(self, id,pwd,tName,dept,position):
        self.id = id
        self.tName = tName
        self.pwd = pwd
        self.dept = dept
        self.position = position
        
        # self.right = right

    def can(self,permission):
        return (self.permission&permission) == permission

    def get_id(self):
        return self.id

    def verify_password(self, pwd):
        # pwd_hash=generate_password_hash(pwd)
        if check_password_hash(self.pwd.strip(),pwd.strip()):
            return True
        else:
            return False

    def __repr__(self):
        return '<Teacher %r>' % self.tName

class Software(db.Model):
    __tablename__='Software'
    id = db.Column(CHAR(32),primary_key=True)
    sName = db.Column(NVARCHAR(None),nullable=False)
    version = db.Column(NVARCHAR(8),nullable=True)
    sysType = db.Column(CHAR(16),nullable=False) # win7 ubuntu16.04 centos 7
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)

    def __repr__(self):
        return '<Software %r>' % self.sName

class Laboratory(db.Model):
    __tablename__='Laboratory'
    id = db.Column(CHAR(16),primary_key=True)
    lName = db.Column(NVARCHAR(32),nullable=False)
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)
    cCount = db.Column(INTEGER,nullable=False)

    def __repr__(self):
        return '<Laboratory %r>'%self.lName

class Computer(db.Model):
    __tablename__='Computer'
    id = db.Column(CHAR(32),primary_key=True)
    cName = db.Column(NVARCHAR(16),nullable=False)
    producer = db.Column(NVARCHAR(16),nullable=False)
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False) # 入库管理员
    lId = db.Column(CHAR(16),ForeignKey('Laboratory.id')) # 所在lab编号
    normal = db.Column(BIT,nullable=False,default=1) # 正常与否

    def __repr__(self):
        return '<Computer %r>'%self.cName
    
class InstallList(db.Model): 
    __tablename__='InstallList'
    id = db.Column(CHAR(32),primary_key=True) # 格式:in<date>/<nums>：in20170901/1
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)
    cId = db.Column(CHAR(16),ForeignKey('Computer.id'),nullable=False)
    sId = db.Column(CHAR(16),ForeignKey('Software.id'),nullable=False)

    def __repr__(self):
        return '<InstallList %r>' % self.id

class LabManage(db.Model):
    __tablename__='LabManage'
    id = db.Column(INTEGER,autoincrement=True,primary_key=True)
    lId = db.Column(CHAR(16),ForeignKey('Laboratory.id'),nullable=False)
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)

    def __repr__(self):
        return '<LabManage %r>' % self.id

class Demand(db.Model):
    __tablename__='Demand'
    id = db.Column(CHAR(32),primary_key=True) # 格式:de<date>/<nums>
    tId = db.Column(CHAR(16),ForeignKey('Teacher.id'),nullable=False)
    lId = db.Column(CHAR(16),ForeignKey('Laboratory.id'),nullable=False) # 目标实验室号
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'))
    content = db.Column(NVARCHAR(None)) # 
    response = db.Column(NVARCHAR(None)) # 回复可选
    inDate = db.Column(DATE,server_default='GETDATE()')
    closeDate = db.Column(DATE) #null:待处理 not null:已经解决
    
    def __repr__(self):
        return '<Demand %r>' %self.id

class ComputerSys(db.Model):
    __tablename__='ComputerSys'
    __table_args__ = (
        PrimaryKeyConstraint('cId', 'sys'),
    )
    cId = db.Column(CHAR(16),ForeignKey('Computer.id'),nullable=False)
    sys = db.Column(CHAR(16),nullable=False)
    def __repr__(self):
        return '<ComputerSys computer_%r,system_%r>' %(self.cId,self.sys)
# web
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
                status = login_user(user)
                session['id'] = user.id
                session['name'] = user.aName
                session['role'] = 'admin'
                return redirect(url_for('admin_view'))


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
                return redirect(url_for('teacher_view'))
            
    return render_template('login.html', form=form)

@app.route('/admin')
@login_required
@admin_required
def admin_view():
    # TODO 管理员视图
    return render_template('admin-index.html',name=session.get('name'),role=session['role'])
    

@app.route('/teacher')
@user_required
@login_required
def teacher_view():

    return render_template('teacher-index.html',name=session.get('name'),role=session['role'])


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经登出！')
    return redirect(url_for('login'))

@app.route('/new_lab', methods=['GET', 'POST'])
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
                return redirect(url_for('newLab'))
    return render_template('new-lab.html', name=session.get('name'),role=session['role'], form=form)    

@app.route('/delete_lab', methods=['GET', 'POST'])
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
                return redirect(url_for('deleteLab'))
    return render_template('delete-lab.html', name=session.get('name'),role=session['role'], form=form)    



@app.route('/new_software',methods = ['GET','POST'])
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
                return redirect(url_for('newSoftware'))
    return render_template('new-software.html', name=session.get('name'),role=session['role'], form=form)    

@app.route('/check_softwares',methods=['GET','POST'])
@login_required

def check_softwares():

    softwares=db.session.execute(exist_software)
    data=[]
    for software in softwares:
        item={'id':software.id,
                    'sName':software.sName,
                    'version':software.version,
                    'sysType':software.sysType,
                    'aId':software.aId}
        data.append(item)
    table_result = {"code": 0, "msg": None, "count": len(data), "data": data}
    return jsonify(table_result)

@app.route('/check_labs',methods=['GET','POST'])
@login_required
def check_labs():

    labs=db.session.execute(exist_lab)
    labs = labs.fetchall()
    data=[]
    for lab in labs:
        item={'id':lab[0],
                    'lName':lab[1],
                    'aId':lab[2],
                    'count':lab[3]}
        data.append(item)
    table_result = {"code": 0, "msg": None, "count": len(data), "data": data}
    return jsonify(table_result)    
    

@app.route('/new_computer',methods = ['GET','POST'])
@login_required
@admin_required
def newComputer():
    form = newComputerForm()
    if form.validate_on_submit():
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
            db.session.add(computer)
            db.session.commit()
            flash(u'新电脑编号:'+cId)
            flash(u'电脑信息添加成功！')
        except:
            db.session.rollback()
            flash(u'电脑信息添加失败:(')
            
        finally:
            return redirect(url_for('newComputer'))
    return render_template('new-computer.html', name=session.get('name'),role=session['role'], form=form)    

@app.route('/delete_labs',methods=['POST'])
@login_required
@admin_required
def delete_check_labs():
    del_ids = json.loads(request.form.get('ids'))

    try:
        for id in del_ids:
            db.session.execute(delete_lab(repr(id)))
        db.session.commit()
        return 'success',200
    except:
        db.session.rollback()
        return 'fail',403

@app.route('/delete_softwares',methods=['POST'])
@login_required
@admin_required
def delete_check_softwares():
    del_ids = json.loads(request.form.get('ids'))

    try:
        for id in del_ids:
            db.session.execute(delete_software(repr(id)))
        db.session.commit()
        return 'success',200
    except:
        db.session.rollback()
        return 'fail',403

@app.route('/lab_Set',methods=['GET','POST'])
@login_required
@admin_required
def labSet():
    form=labSetForm() #虚表单
    return render_template('lab-set.html',name=session.get('name'),role=session['role'],form=form)

@app.route('/check_softwares_by_names',methods=['GET','POST'])
@login_required
def check_softwares_by_names():
    sName = json.loads(request.args.get('names'))
    sName = map(repr,sName)
    softwares = db.session.execute(exist_software_by_name(','.join(sName)))
    data=[]
    for software in softwares:
        item={'id':software.id,
                'sName':software.sName,
                'sysType':software.sysType,
                'version':software.version,
                'aId':software.aId}
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)
    

@app.route('/check_uninstall_by_sId',methods=['GET','POST'])
@login_required
def check_uninstall_by_sId():
    ids = json.loads(request.args.get('ids'))
    ids = map(repr,ids)
    labId = request.args.get('labId')
    data =[]
    computers = db.session.execute(not_have_software_of(','.join(ids),labId))
    for computer in computers:
        item={
            'id':computer.id,
            'cName':computer.cName,
            'producer':computer.producer,
            'aId':computer.aId
        }
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)
    


@app.route('/check_install_by_sId',methods=['GET','POST'])
@login_required
def check_install_by_sId():
    ids = json.loads(request.args.get('ids'))
    ids = map(repr,ids)
    labId = request.args.get('labId')
    data =[]
    computers = db.session.execute(have_software_of(','.join(ids),labId))
    for computer in computers:
        item={
            'id':computer.id,
            'cName':computer.cName,
            'producer':computer.producer,
            'aId':computer.aId
        }
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)
    

@app.route('/install_softwares_for_lab',methods=['GET','POST'])
@login_required
@admin_required
def install_softwares_for_lab():
    cIds = json.loads(request.form.get('cIds'))
    sIds = json.loads(request.form.get('sIds'))
    # labId = request.args.get('labId')
    # fail=[]
    success=0
    for sId in sIds:
        for cId in cIds:

            count = db.session.execute(max_today_install).fetchall()
            if(count[0][0] is None):
                count=0
            else:
                count = count[0][0]    
            try:
                db.session.execute(install(sId,cId,current_user.id,count+1))
                db.session.commit()
                success+=1
            except:
                db.session.rollback()
    if(success>0):
        return str(success),200
    else:
        return 'fail',403

@app.route('/uninstall_softwares_for_lab',methods=['GET','POST'])
@login_required
@admin_required
def uninstall_softwares_for_lab():
    cIds = json.loads(request.form.get('cIds'))
    sIds = json.loads(request.form.get('sIds'))
    # labId = request.form.get('labId')
    # fail=[]
    success=0
    for sId in sIds:
        for cId in cIds:
            try:
                # 求id
                db.session.execute(uninstall(sId,cId))
                db.session.commit()
                success+=1
            except:
                db.session.rollback()
    if(success>0):
        return str(success),200
    else:
        return 'fail',403


@app.route('/lab_computer',methods=['GET','POST'])
@login_required
@admin_required
def labComputer():
    return render_template('lab-computer.html',name=session.get('name'),role=session['role'])

@app.route('/check_avil_computer',methods=['GET','POST'])
@login_required
@admin_required
def check_avil_computer():

    data =[]
    computers = db.session.execute(avil_computer)
    for computer in computers:
        item={
            'id':computer.id,
            'cName':computer.cName,
            'producer':computer.producer,
            'normal':'正常' if computer.normal==1 else '异常',
            'aId':computer.aId
        }
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)

@app.route('/check_own_computer',methods=['GET','POST'])
@login_required
def check_own_computer():
    labId = request.args.get('labId')
    data =[]
    computers = db.session.execute(lab_computer_of(labId))
    for computer in computers:
        item={
            'id':computer.id,
            'cName':computer.cName,
            'producer':computer.producer,
            'normal':'正常' if computer.normal==1 else '异常',
            'aId':computer.aId
        }
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)

@app.route('/import_computers_for_lab',methods=['GET','POST'])
@login_required
@admin_required
def import_computers_for_lab():
    cIds=json.loads(request.form.get('cIds'))
    labId = request.form.get('labId')
    success=0

    # 先求已有电脑数和最大容纳电脑数
    own_computers_count=Computer.query.filter_by(lId=labId).count()
    max_computer_count=Laboratory.query.filter_by(id=labId).first().cCount
    if(own_computers_count >= max_computer_count):
        return 'full',403
    for cId in cIds:
        try:
            db.session.execute(import_computer(cId,labId))
            own_computers_count+=1
            if(own_computers_count>max_computer_count):
                raise FullError
            db.session.commit()
            success+=1
        except FullError:
            db.session.rollback()
            break

        except:
            db.session.rollback()
    if(success>0):
        return str(success),200
    else:
        return 'fail',403

@app.route('/export_computers_for_lab',methods=['GET','POST'])
@login_required
@admin_required
def export_computers_for_lab():
    cIds=json.loads(request.form.get('cIds'))
    success=0
    for cId in cIds:
        try:
            db.session.execute(export_computer(cId))
            db.session.commit()
            success+=1
        except:
            db.session.rollback()
    if(success>0):
        return str(success),200
    else:
        return 'fail',403





@app.route('/post_demand',methods=['GET','POST'])
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
# TODO 需求概览

@app.route('/show_tDemand',methods=['GET','POST'])
@login_required
@user_required
def show_tDemand():
    return render_template('demand-show.html', name=session.get('name'),role=session['role'])

@app.route('/close_tDemand',methods=['GET','POST'])
@login_required
@user_required
def close_tDemand():
    tId=current_user.id
    sql=close_teacher_demand(tId)
    demands=db.session.execute(sql)
    data=[]
    for demand in demands:
        item={'id':demand.id,
                'response':demand.response,
                'closeDate':demand.closeDate,
                'lId':demand.lId,
                'content':demand.content,
                'aId':demand.aId}
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)

@app.route('/open_tDemand',methods=['GET','POST'])
@login_required
@user_required
def open_tDemand():
    tId=current_user.id

    sql=open_teacher_demand(tId)
    demands=db.session.execute(sql)
    data=[]
    for demand in demands:
        item={'id':demand.id,
                'response':demand.response,
                'closeDate':demand.closeDate,
                'lId':demand.lId,
                'status':'受理' if demand.aId is not None else '未受理',
                'content':demand.content}
        data.append(item)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)

@app.route('/del_demand',methods=['GET','POST'])
@login_required
def del_demand():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            Demand.query.filter_by(id=id).delete()
            db.session.commit()
            success+=1
        except:
            db.session.rollback()
    if success>0:
        return str(success),200
    else:
        return 'fail',403

# TODO 需求解决

@app.route('/oper_demand',methods=['GET','POST'])
@login_required
@admin_required
def operDemand():
    return render_template('demand-oper.html', name=session.get('name'),role=session['role'])


def getDemands(sql):
    demands=db.session.execute(sql)
    data=[]
    for demand in demands:
        item={'id':demand.id,
                'response':demand.response,
                'closeDate':demand.closeDate,
                'lId':demand.lId,
                'aId':demand.aId,
                'tId':demand.tId,
                'status':'受理' if demand.aId is not None else '未受理',
                'content':demand.content}
        data.append(item)
    return data

@app.route('/check_open_demand',methods=['GET','POST'])
@login_required
@admin_required
def check_open_Demand():
    data=getDemands(all_open_demand)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)
    
@app.route('/check_accepted_demand',methods=['GET','POST'])
@login_required
@admin_required  
def check_accepted_demand():
    sql=all_m_accepted_demand(current_user.id)
    data=getDemands(sql)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)

@app.route('/check_close_demand',methods=['GET','POST'])
@login_required
@admin_required  
def check_close_aDemand():
    sql=all_m_close_demand(current_user.id)
    data=getDemands(sql)
    table_result={"code":0,"msg":None,"count":len(data),"data":data}
    return jsonify(table_result)


# 需求受理与取消

@app.route('/accept_demand',methods=['GET','POST'])
@login_required
@admin_required
def accept_demand():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            db.session.execute(set_demand_accept(id,current_user.id))
            db.session.commit()
            success+=1
        except:
            db.rollback()
    if success > 0:
        return str(success),200
    else:
        return 'fail',403

@app.route('/cancel_accept_demand',methods=['GET','POST'])
@login_required
@admin_required
def del_acDemand():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            db.session.execute(cancel_demand_accept(id,current_user.id))
            db.session.commit()
            success+=1
        except:
            db.rollback()
    if success > 0:
        return str(success),200
    else:
        return 'fail',403

@app.route('/close_accepted_demand',methods=['GET','POST'])
@login_required
@admin_required
def close_acDemand():
    Ids=json.loads(request.form.get('Ids'))
    success=0
    for id in Ids:
        try:
            db.session.execute(close_accepted_demand(id))
            db.session.commit()
            success+=1
        except:
            db.session.rollback()
    if success > 0:
        return str(success),200
    else:
        return 'fail',403    

@app.route('/set_response',methods=['GET','POST'])
@login_required
@admin_required
def set_response():
    Ids=json.loads(request.form.get('Ids'))[0]
    res=request.form.get('res')
    success=0
    try:
        db.session.execute(set_demand_response(Ids,res))
        db.session.commit()
        success+=1
    except:
        db.session.rollback()
        
    if success > 0:
        return str(success),200
    else:
        return 'fail',403  

# TODO 电脑出库

# TODO 密码修改用户名修改

@app.route('/change_password', methods=['GET', 'POST'])
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
                    return redirect(url_for('logout'))
                if(session['role'] == 'teacher'):    
                    return redirect(url_for('logout'))
            except:
                db.session.rollback()
                flash(u'修改失败')
                

        else:
            flash(u'原密码输入错误，修改失败！')
    return render_template("change-password.html", form=form,name=session.get('name'),role=session['role'])
