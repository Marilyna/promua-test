from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask('catalog')
db = SQLAlchemy(app)


def create(config):
    app.config.update(config)
    app.secret_key = 'Drugs are bad! okay?'
    import catalog.views