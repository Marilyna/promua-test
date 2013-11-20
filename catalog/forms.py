import json
from flask_wtf import Form

from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

from catalog import db, bcrypt
from catalog.validators import EmailUnique
from catalog.models import Book, Author, User


class AddForm(Form):
    book_id = IntegerField()
    author = TextField('Author', validators=[DataRequired()])
    title = TextField('Title', validators=[DataRequired()])

    def save(self):
        book = Book(title=self.title.data)
        author = Author.query.filter_by(name=self.author.data).first() or Author(name=self.author.data)
        author.books.append(book)
        db.session.add(book)
        db.session.add(author)
        db.session.commit()
        return book

    def edit(self):
        book = Book.query.get(self.book_id.data)
        book.title = self.title.data

        old_author = book.authors[0]
        new_author = Author.query.filter_by(name=self.author.data).first() or Author(name=self.author.data)
        new_author.books.append(book)
        old_author.books.remove(book)
        db.session.add(book)
        db.session.add(new_author)
        db.session.add(old_author)
        db.session.commit()
        return json.dumps({'author': new_author.name, 'title': book.title})


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

    def save(self):
        # register new user
        user = User(email=self.email.data, password=bcrypt.generate_password_hash(self.password.data))
        db.session.add(user)
        db.session.commit()
        return user
