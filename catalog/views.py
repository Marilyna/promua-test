from flask import render_template, redirect, request, url_for

from catalog import app, db, forms
from catalog.models import Author, Book


@app.route('/')
def search():
    form = forms.SearchForm()
    all_books = Book.query.all()
    return render_template('search.html', form=form, books=all_books)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # if valid_login(request.form['username'],
        #                request.form['password']):
        #     return log_the_user_in(request.form['username'])
        # else:
        #     error = 'Invalid username/password'
        pass
    form = forms.LoginForm()
    return render_template('login.html', form=form, error=error)


@app.route('/edit/', methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        return 'edit OK!!!'
    form = forms.AddForm()
    all_books = Book.query.all()
    return render_template('edit.html', form=form, books=all_books)


@app.route('/add/', methods=['POST'])
def add():
    book = Book(title=request.form['title'])
    author = Author.query.filter_by(name=request.form['author']).first()
    if not author:
        author = Author(name=request.form['author'])
    author.books.append(book)
    db.session.add(book)
    db.session.add(author)
    db.session.commit()
    return redirect(url_for('edit'))
