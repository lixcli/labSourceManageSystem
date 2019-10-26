from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField,RadioField
from wtforms.validators import DataRequired, EqualTo, Length


class Login(FlaskForm):
    account = StringField(u'账号', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    role = RadioField('teacher',choices=[('admin','管理员'),('teacher','教师')])
    submit = SubmitField(u'登录')