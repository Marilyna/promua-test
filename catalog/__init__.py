from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt


app = Flask('catalog')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


def create(config):
    app.config.update(config)
    app.secret_key = 'Drugs are bad! okay?'

    app.static_folder = 'static'  # Enable is back, but the URL rule is
    app.add_url_rule('/static/<path:filename>', endpoint='static', view_func=app.send_static_file)

    from catalog.login import login_manager
    login_manager.init_app(app)

    from flask_wtf.csrf import CsrfProtect
    CsrfProtect(app)

    import catalog.views