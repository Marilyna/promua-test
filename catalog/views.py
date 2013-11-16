from flask import render_template, request

from catalog import app, forms, models

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
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

@app.route('/edit')
def edit():
    return render_template('edit.html')
