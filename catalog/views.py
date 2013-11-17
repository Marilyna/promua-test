from flask import render_template, redirect, request, url_for, flash

from catalog import app, db, forms, bcrypt
from catalog.models import Author, Book, User
from flask.ext.login import login_user


@app.route('/')
def search():
    form = forms.SearchForm()
    all_books = Book.query.all()
    return render_template('search.html', form=form, books=all_books)


@app.route('/edit/', methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        # TODO edit book
        return 'edit OK!!!'
    form = forms.AddForm()
    all_books = Book.query.all()
    return render_template('edit.html', form=form, books=all_books)


@app.route('/add/', methods=['POST'])
def add():
    book = Book(title=request.form['title'])
    author = Author.query.filter_by(name=request.form['author']).one()
    if not author:
        author = Author(name=request.form['author'])
    author.books.append(book)
    db.session.add(book)
    db.session.add(author)
    db.session.commit()
    return redirect(url_for('edit'))


@app.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    form = forms.LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).one()
        # check password and log in
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, force=True)
            flash("Logged in successfully.")
            return redirect(request.args.get('next') or url_for('search'))
        error = 'Invalid email or password'
    return render_template('login.html', form=form, error=error)


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