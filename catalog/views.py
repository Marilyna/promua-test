from operator import or_

from flask import render_template, redirect, request, url_for, jsonify
from flask.ext.login import login_user, login_required, logout_user, current_user

from catalog import app, db, forms
from catalog.models import Author, Book


@app.route('/')
def search():
    form = forms.SearchForm(request.args)
    search_keys = request.args.get('search')
    if not search_keys:
        books = Book.query.all()
    else:
        sqllike = []
        for search_key in search_keys.split(' '):
            like_key = '%' + search_key + '%'
            # case-insensitive like may not work in SQLite with Cyrillic
            sqllike.append(Book.title.ilike(like_key))
            sqllike.append(Author.name.ilike(like_key))
        filter_clause = reduce(or_, sqllike)
        books = Book.query.join(Book.authors).filter(filter_clause)
    return render_template('search.html', form=form, books=books,
                           user=current_user if current_user.is_authenticated() else None)


@app.route('/edit/', methods=['GET'])
@login_required
def edit():
    form = forms.BookForm()
    all_books = Book.query.all()
    return render_template('edit-books.html', form=form, books=all_books,
                           user=current_user if current_user.is_authenticated() else None)


@app.route('/edit/<int:book_id>/', methods=['POST'])
@login_required
def edit_book(book_id):

    book = Book.query.get_or_404(book_id)
    form = forms.BookForm()
    if form.validate():
        form.edit(book)
        return jsonify(title=book.title, authors=', '.join(author.name for author in book.authors))
    return jsonify(**form.errors), 400


@app.route('/add/', methods=['POST'])
@login_required
def add():
    form = forms.BookForm()
    if form.validate():
        form.create()
        return redirect(url_for('edit'))
    return jsonify(**form.errors), 400


@app.route('/delete/', methods=['POST'])
@login_required
def delete():
    ids_to_delete = request.form.getlist('selected_books')
    for id in ids_to_delete:
        book = Book.query.get_or_404(id)
        authors = book.authors
        for author in authors:
            # if this book is the only one, delete author
            if len(author.books) == 1:
                db.session.delete(author)
        db.session.delete(book)
    db.session.commit()
    return redirect(url_for('edit'))


@app.route('/authors/', methods=['GET'])
@login_required
def authors():
    form = forms.AuthorForm()
    all_authors = Author.query.all()
    return render_template('edit-authors.html', form=form, authors=all_authors,
                           user=current_user if current_user.is_authenticated() else None)


@app.route('/authors/<int:author_id>/', methods=['POST'])
@login_required
def edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    form = forms.AuthorForm()
    if form.validate():
        form.edit(author)
        return jsonify(name=author.name)
    return jsonify(**form.errors), 400


@app.route('/add_author/', methods=['POST'])
@login_required
def add_author():
    form = forms.AuthorForm()
    form.create()
    return redirect(url_for('authors'))


@app.route('/delete_author/', methods=['POST'])
@login_required
def delete_author():
    ids_to_delete = request.form.getlist('selected_authors')
    for id in ids_to_delete:
        author = Author.query.get(id)
        books = author.books
        for book in books:
            # if this is the only author, delete the book
            if len(book.authors) == 1:
                db.session.delete(book)
        db.session.delete(author)
    db.session.commit()
    return redirect(url_for('authors'))


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user)
        return redirect(url_for('search'))
    return render_template('registration.html', form=form)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    nexturl = request.values.get('next') or url_for('search')
    form = forms.LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        return redirect(nexturl)
    return render_template('login.html', form=form, next=nexturl)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('search'))
