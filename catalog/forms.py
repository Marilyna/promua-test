from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired


class LoginForm(Form):
    login = TextField('Login', validators=[DataRequired()])
    password = TextField('Password', validators=[DataRequired()])
