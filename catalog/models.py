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
    name = db.Column(db.Unicode(100))
    books = db.relationship(Book, secondary=authorship, backref=db.backref('authors'))
