
from ..model import *
from ..form import *
from ..sql_for_lab import *
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from .. import *

from flask import Blueprint
user_manage = Blueprint('user_manage',__name__,
static_folder='../static',
template_folder='../templates')
from . import views,services
