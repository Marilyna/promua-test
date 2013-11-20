import json
from flask_wtf import Form

from wtforms import TextField, PasswordField, IntegerField, FieldList
from wtforms.validators import DataRequired, Email, EqualTo

from catalog import db, bcrypt
from catalog.validators import EmailUnique
from catalog.models import Book, Author, User


class AddForm(Form):
    book_id = IntegerField()
    authors = FieldList(TextField('Author', validators=[DataRequired()]), min_entries=1)
    title = TextField('Title', validators=[DataRequired()])

    def save(self):
        book = Book(title=self.title.data)
        authors = []
        for name in self.authors.data:
            authors.append(Author.query.filter_by(name=name).first() or Author(name=name))

        for author in authors:
            author.books.append(book)
            db.session.add(author)
        db.session.add(book)
        db.session.commit()
        return book

    def edit(self):
        book = Book.query.get(self.book_id.data)
        if not book:
            return json.dumps({'error': 'No book found!'})
        book.title = self.title.data

        old_authors = book.authors
        new_authors = []
        for name in self.authors.data:
            new_authors.append(Author.query.filter_by(name=name).first() or Author(name=name))

        # TODO fix this ugly!
        for old_author in old_authors:
            if old_author not in new_authors:
                old_author.books.remove(book)
                db.session.add(old_author)
        for new_author in new_authors:
            if new_author not in old_authors:
                new_author.books.append(book)
                db.session.add(new_author)
        db.session.commit()
        return json.dumps({'authors': ', '.join([author.name for author in new_authors]), 'title': book.title})


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
