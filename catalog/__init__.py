from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt


app = Flask('catalog')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


def create(config):
    app.config.update(config)
    app.secret_key = 'Drugs are bad! okay?'
    
    from catalog.login import login_manager
    login_manager.init_app(app)

    import catalog.views