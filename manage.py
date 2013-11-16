#!/usr/bin/env python
from opster import command, dispatch


CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///../db.sqlite',
}


@command()
def printdb():
    from catalog import db, models
    def dump(sql, *args, **kwargs):
        print sql.compile(dialect=engine.dialect)
    engine = db.create_engine('sqlite://', strategy='mock', executor=dump)
    db.metadata.create_all(engine)


@command()
def syncdb():
    from catalog import db, models, create
    create(CONFIG)
    db.create_all()


@command()
def shell():
    from catalog import app, create

    create(CONFIG)

    with app.test_request_context('/'):
        app.preprocess_request()

        banner = 'Interactive Shell\n'

        try:
            from IPython import embed
        except ImportError:
            pass
        else:
            try:
                import sys
                if sys.platform == 'win32':
                    import pyreadline
            except ImportError:
                banner = ('There is IPython installed on your system, '
                          'but no pyreadline\n' + banner)
            else:
                embed(banner1=banner)
                return
        from code import interact
        interact(banner)


@command()
def runserver():
    from catalog import app, create
    create(CONFIG)
    app.run(host='0.0.0.0', port=8000)


if __name__ == '__main__':
    dispatch()
