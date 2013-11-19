import json

from flask import render_template, redirect, request, url_for
from flask.ext.login import login_user, login_required, logout_user, current_user

from catalog import app, db, forms, bcrypt
from catalog.models import Author, Book, User


@app.route('/')
def search():
    form = forms.SearchForm()
    all_books = Book.query.all()
    return render_template('search.html', form=form, books=all_books,
                           user=current_user if current_user.is_authenticated() else None)


@app.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        book = Book.query.get(request.form.get('book_id'))
        book.title = request.form.get('new_title')
        old_author = book.authors[0]
        new_author = Author.query.filter_by(name=request.form.get('new_author')).first()
        if not new_author:
            new_author = Author(name=request.form['new_author'])
        # replace old authorship with new one
        new_author.books.append(book)
        old_author.books.remove(book)
        db.session.add(book)
        db.session.add(new_author)
        db.session.add(old_author)
        db.session.commit()
        return json.dumps({'author': new_author.name, 'title': book.title})
        #FIXME now need to reload page to view refreshed list

    form = forms.AddForm()
    all_books = Book.query.all()
    return render_template('edit-books.html', form=form, books=all_books,
                           user=current_user if current_user.is_authenticated() else None)


@app.route('/add/', methods=['POST'])
@login_required
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


@app.route('/delete/', methods=['POST'])
@login_required
def delete():
    ids_to_delete = request.form.getlist('selected_books')
    for id in ids_to_delete:
        book = Book.query.get(id)
        db.session.delete(book)
    db.session.commit()

    return redirect(url_for('edit'))


@app.route('/authors/', methods=['POST', 'GET'])
@login_required
def authors():
    return render_template('edit-authors.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    form = forms.RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        # register new user
        user = User(email=form.email.data, password=bcrypt.generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('search'))
    return render_template('registration.html', form=form)


@app.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    nexturl = request.args.get('next') or request.form.get('next') or url_for('search')
    form = forms.LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        # check password and log in
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(nexturl)
        error = 'Invalid email or password'
    return render_template('login.html', form=form, error=error, next=nexturl)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('search'))
