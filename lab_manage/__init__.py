
from ..model import *
from ..form import *
from ..sql_for_lab import *
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from mvc_mode_labSys import *
from flask import Blueprint
lab_manage = Blueprint('lab_manage',__name__,
static_folder='../static',
template_folder='../templates')
from . import views,services
