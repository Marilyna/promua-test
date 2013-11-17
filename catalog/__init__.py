from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
from flask.ext.login import LoginManager


app = Flask('catalog')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()


def create(config):
    app.config.update(config)
    app.secret_key = 'Drugs are bad! okay?'
    login_manager.init_app(app)

    import catalog.views