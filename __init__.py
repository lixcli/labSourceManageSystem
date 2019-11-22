# -*- coding: utf-8 -*-
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
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint,ForeignKey,PrimaryKeyConstraint,and_
import os
from .sql_for_lab import *
# import pandas as pd
from .form import *
import time
import json
import zlib
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.login_message = u"请先登录。"
app.config.from_object('mvc_mode_labSys.setting')
# app.config.from_envvar('FLASKR_SETTINGS')

basedir = os.path.abspath(os.path.dirname(__file__))
# db_engine, tables = get_database()
db = SQLAlchemy(app)
# def make_shell_context():
#     return dict(app=app, db=db, Adminitrator=Adminitrator, Teacher=Teacher)
#     # pass
# manager = Manager(app)
# manager.add_command("shell", Shell(make_context=make_shell_context))

# stop visitor
from .computer_manage import computer_manage
from .user_manage import user_manage
from .lab_manage import lab_manage
from .demand_manage import demand_manage
from .software_manage import soft_manage
from .main import main
app.register_blueprint(computer_manage)
app.register_blueprint(user_manage)
app.register_blueprint(demand_manage)
app.register_blueprint(lab_manage)
app.register_blueprint(soft_manage)
app.register_blueprint(main)


