from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

from catalog.validators import EmailUnique


class AddForm(Form):
    author = TextField('Author', validators=[DataRequired()])
    title = TextField('Title', validators=[DataRequired()])


class SearchForm(Form):
    search = TextField('Search', validators=[DataRequired()])


class LoginForm(Form):
    email = TextField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(Form):
    email = TextField('Email', validators=[Email(), EmailUnique()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm',
                                                                                 message='Passwords must match')])
    confirm = PasswordField('Repeat password')
