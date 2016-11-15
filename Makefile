all: clean test

init_db: 
	createdb pg_store

clean:
	rm -rf build && rm -rf htmlcov && rm -rf .coverage && rm -rf .cache && rm -rf dist && rm -rf pulsar_postgresql.egg-info

test: SHELL:=/bin/bash
test: 
	python3 runtests.py --coverage --test-plugins pg_store.tests.PGPlugin --test-pg-dsn postgresql://localhost:5432/pg_store --test-pg-data-source tests/db.sql && coverage html --include='pg_store/*'

pypi:
	python2 setup.py sdist upload
