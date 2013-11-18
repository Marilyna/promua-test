from catalog import db


authorship = db.Table(
    'authorship', db.Model.metadata,
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(255))


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(100), index=True, unique=True)
    books = db.relationship(Book, secondary=authorship, backref=db.backref('authors'))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode(255), index=True, unique=True)
    password = db.Column(db.String(60))

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

