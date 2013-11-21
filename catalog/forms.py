from flask_wtf import Form

from wtforms import TextField, PasswordField, FieldList
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from catalog import db, bcrypt
from catalog.validators import EmailUnique
from catalog.models import Book, Author, User


class BookForm(Form):
    authors = FieldList(TextField('Author', validators=[DataRequired()]), min_entries=1)
    title = TextField('Title', validators=[DataRequired()])

    def create(self):
        book = Book(title=self.title.data)
        book.authors = [Author.query.filter_by(name=name).first() or
                        Author(name=name)
                        for name in set(self.authors.data)]

        db.session.add(book)
        db.session.commit()
        return book

    def edit(self, book):
        book.title = self.title.data

        old_authors = {author.name: author for author in book.authors}
        new_authors = [old_authors.get(name) or
                       Author.query.filter_by(name=name).first() or
                       Author(name=name)
                       for name in set(self.authors.data)]

        book.authors = new_authors
        for old_author in set(old_authors.values()) - set(new_authors):
            if not old_author.books:
                db.session.delete(old_author)

        db.session.commit()

    def validate_title(self, field):
        books = Book.query.filter_by(title=field.data).all()
        for book in books:
            authors = [name for name in set(self.authors.data)]
            book_authors = [author.name for author in set(book.authors)]
            if authors == book_authors:
                raise ValidationError('This book already exists')


class AuthorForm(Form):
    name = TextField('Name', validators=[DataRequired()])

    def create(self):
        author = Author.query.filter_by(name=self.name.data).first() or Author(name=self.name.data)
        db.session.add(author)
        db.session.commit()
        return author

    def edit(self, author):
        author.name = self.name.data
        db.session.commit()


class SearchForm(Form):
    search = TextField('Search', validators=[DataRequired()])


class LoginForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    user = None

    def validate_email(self, field):
        self.user = User.query.filter_by(email=field.data).first()
        if not self.user:
            raise ValidationError('No such user')

    def validate_password(self, field):
        if self.user and not bcrypt.check_password_hash(self.user.password, field.data):
            raise ValidationError('Wrong password')


class RegistrationForm(Form):
    email = TextField('Email', validators=[DataRequired(), Email(), EmailUnique()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat password')

    def save(self):
        # register new user
        user = User(email=self.email.data, password=bcrypt.generate_password_hash(self.password.data))
        db.session.add(user)
        db.session.commit()
        return user
