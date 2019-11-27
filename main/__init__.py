
from ..model import *
from ..form import *
from ..sql_for_lab import *
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from .. import login_manager
from flask import Blueprint
main = Blueprint('main',__name__,
static_folder='../static/',
template_folder='../templates',
)
from . import admin_main,login_logout,user_main


