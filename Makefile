.PHONY: run shell env db

DB=db.sqlite

help:
	@echo "Use \`make <target>\` with one of targets:"
	@echo "  env    setup virtualenv with requirements"
	@echo "  db     initialize db"
	@echo "  run    run development server"
	@echo "  shell  start python shell"

run:
	env/bin/python manage.py runserver

shell:
	env/bin/python manage.py shell

env:
	virtualenv env
	pip install -r requirements.txt

db: create-db populate-db

create-db:
	sqlite3 $(DB) < sql/tables.sql

populate-db:
	sqlite3 $(DB) < sql/data.sql
