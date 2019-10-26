from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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
from sqlalchemy import CheckConstraint,ForeignKey
import os
# import pandas as pd
from form import *
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

class Adminitrator(db.Model,UserMixin): 
    __tablename__='Adminitrator'
# 简单起见 管理员都是全权限
    id = db.Column(CHAR(16), primary_key=True)
    pwd = db.Column(CHAR(128),nullable=False)
    aName = db.Column(NVARCHAR(32),nullable=False)


    def __init__(self, id, pwd, aName):
        self.id = id
        self.aName = aName
        self.pwd = pwd
        # self.right = right

    def get_id(self):
        return self.id

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

    def __init__(self, id,pwd,tName,dept,position):
        self.id = id
        self.tName = tName
        self.pwd = pwd
        self.dept = dept
        self.position = position
        # self.right = right

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
    id = db.Column(CHAR(16),primary_key=True)
    sName = db.Column(NVARCHAR(None),nullable=False)
    version = db.Column(NVARCHAR(8),nullable=True)
    sysType = db.Column(CHAR(16), CheckConstraint("sysType='win7' or sysType='ubuntu16.04' or sysType = 'centos7'"),nullable=False,default='win7') # win7 ubuntu16.04 centos 7

    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)

    def __repr__(self):
        return '<Software %r>' % self.sName

class Laboratory(db.Model):
    __tablename__='Laboratory'
    id = db.Column(CHAR(16),primary_key=True)
    lName = db.Column(NVARCHAR(32),nullable=False)
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)

    def __repr__(self):
        return '<Laboratory %r>'%self.lName

class Computer(db.Model):
    __tablename__='Computer'
    id = db.Column(CHAR(16),primary_key=True)
    cName = db.Column(CHAR(16),nullable=False)
    producer = db.Column(VARCHAR(16),nullable=False)
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

# web
@login_manager.user_loader
def load_admin(admin_id):
    return Adminitrator.query.get(int(admin_id))

@login_manager.user_loader
def load_teacher(teacher_id):
    return Teacher.query.get(int(teacher_id))

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
                return redirect(url_for('admin_view'))


        elif form.role.data == 'teacher':
            user = Teacher.query.filter_by(id=form.account.data).first()
            # TODO 教师界面跳转
            if user is None or not user.verify_password(form.password):
                flash('账号或密码错误！')
                return redirect(url_for('login'))
            else:
                login_user(user)
                session['id'] = user.id
                session['name'] = user.tName
                session['role'] = 'teacher'
                return redirect(url_for('teacher_view'))
            pass
    return render_template('login.html', form=form)

# 本系统没有注册系统，但是有增加教师用户的功能



# def importComputerFromCSV(csv_pth,aId):
#     df = pd.read_csv(csv_pth)
#     # err = open('importComputerErr.csv','w')
#     err_df = pd.DataFrame(columns=df.columns)
#     for i,row in df.iterrows():
#         try:
#             item=Computer()
#             item.id = row['id']
#             item.cName = row['cName']
#             item.producer = row['producer']
#             item.lId = row['lId']
#             item.normal = row['normal']
#             item.aId = aId
#             db.session.add(item)
#             db.session.commit()
            
#         except:
#             err_df.loc[len(err_df)]=dict(row)
#     if(len(err_df)>0):
#         err_df.to_csv('importComputerErr.csv')
#     return len(df)-len(err_df),len(err_df) # 成功数，失败数
# # TODO 计算机录入界面设计


# TODO 实验室增加
@app.route('/new_lab', methods=['GET', 'POST'])
@login_required
def newLab():
    form = newLabForm()
    if form.validate_on_submit():
        exist = Laboratory.query.filter_by(id=request.form.get('labId')).first()
        if exist is not None:
            flash(u'该实验室已经存在,请重新填写')
        else:
            try:
                lab = Laboratory()
                lab.id = request.form.get('labId')
                book.book_name = request.form.get('lName')
                db.session.add(lab)
                db.session.commit()
                flash(u'实验室信息添加成功！')
            except:
                flash(u'实验室信息添加失败:(')
            finally:
                return redirect(url_for('newLab'))
    return render_template('new-lab.html', name=session.get('name'), form=form)    
# TODO 软件录入
# TODO 软件安装
# TODO 需求解决
# TODO 计算机资源查找
# TODO 计算机资源统计


