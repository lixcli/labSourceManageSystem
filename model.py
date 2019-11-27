from mvc_mode_labSys import db,current_user
from functools import wraps
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from . import *
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.mssql import  \
    BIGINT, BINARY, BIT, CHAR, DATE, DATETIME, DATETIME2, \
    DATETIMEOFFSET, DECIMAL, FLOAT, IMAGE, INTEGER, MONEY, \
    NCHAR, NTEXT, NUMERIC, NVARCHAR, REAL, SMALLDATETIME, \
    SMALLINT, SMALLMONEY, SQL_VARIANT, TEXT, TIME, \
    TIMESTAMP, TINYINT, UNIQUEIDENTIFIER, VARBINARY, VARCHAR
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint,ForeignKey,PrimaryKeyConstraint,and_

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
        self.Dept = dept
        self.Position = position
        
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

    cpu = db.Column(CHAR(3),nullable=False)
    mm = db.Column(TINYINT,nullable=False,default=8)

    def __repr__(self):
        return '<Computer %r>'%self.cName
    
class InstallList(db.Model): 
    __tablename__='InstallList'
    id = db.Column(CHAR(32),primary_key=True) # 格式:in<date>/<nums>：in20170901/1
    aId = db.Column(CHAR(16),ForeignKey('Adminitrator.id'),nullable=False)
    cId = db.Column(CHAR(32),ForeignKey('Computer.id'),nullable=False)
    sId = db.Column(CHAR(32),nullable=False)
    sys = db.Column(CHAR(16),nullable=False)

    def __repr__(self):
        return '<InstallList %r>' % self.id


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
    cId = db.Column(CHAR(32),ForeignKey('Computer.id'))
    sys = db.Column(CHAR(32))
    def __repr__(self):
        return '<ComputerSys computer_%r,system_%r>' %(self.cId,self.sys)
