from flask import render_template, redirect, request, url_for
from flask.ext.login import login_user, login_required, logout_user, current_user

from catalog import app, db, forms, bcrypt
from catalog.models import Author, Book, User


@app.route('/')
def search():
    # TODO search function
    form = forms.SearchForm()
    all_books = Book.query.all()
    return render_template('search.html', form=form, books=all_books,
                           user=current_user if current_user.is_authenticated() else None)


@app.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    form = forms.AddForm()
    if request.method == 'POST':
        return form.edit()
    all_books = Book.query.all()
    return render_template('edit-books.html', form=form, books=all_books,
                           user=current_user if current_user.is_authenticated() else None)


@app.route('/add/', methods=['POST'])
@login_required
def add():
    form = forms.AddForm()
    form.save()
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
        form.save()
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
