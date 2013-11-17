from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class AddForm(Form):
    author = TextField('Author', validators=[DataRequired()])
    title = TextField('Title', validators=[DataRequired()])


class SearchForm(Form):
    search = TextField('Search', validators=[DataRequired()])
