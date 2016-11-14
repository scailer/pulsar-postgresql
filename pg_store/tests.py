# -*- coding: utf-8 -*-
"""
Pulsar test plugin for integration with postgresql.
Cteate test database "dbname_test", optionaly init from sql file,
and drop after tests finished.

--test-plugins pg_store.tests.PGPlugin
--test-pg-dsn postgresql://user:pass@localhost:5432/dbname
--test-pg-data-source tests/pg_schema.txt

"""

import re
import psycopg2

from pulsar.apps.test.plugins.base import TestPlugin

regexp_dsn = re.compile(
    r'^(?:(?P<schema>.*?)?://)?(?:(?P<username>.*?)(?::(?P<password>.*))?@)'
    r'?(?:(?P<host>.*?)(?::(?P<port>\d+))?)?\/(?P<database>.*?)'
    r'(?:\?(?P<params>[^\?]*))?$'
)


class PGPlugin(TestPlugin):
    def configure(self, cfg):
        self.config = cfg
        self.pg_dsn_main = cfg.settings.get('test_pg_dsn').value
        self.pg_dsn_test = cfg.settings.get('test_pg_dsn').value + '_test'
        self.pg_data_sql = cfg.settings.get('test_pg_data').value

    def checkdb(self):
        _, _, _, host, _, db, _ = regexp_dsn.match(self.pg_dsn_test).groups()

        if host not in ('localhost', '127.0.0.1'):
            r = input('Do you realy want run tests on {} database? '
                      '[y/N]:'.format(self.pg_dsn_test))

            if r.lower() not in ('y', 'yes'):
                raise

        return db

    def createdb(self):
        print('CREATEDB')
        db_name = self.checkdb()
        conn = psycopg2.connect(self.pg_dsn_main)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        try:
            conn.cursor().execute('CREATE DATABASE {}'.format(db_name))

        except psycopg2.ProgrammingError:
            conn.cursor().execute('DROP DATABASE {}'.format(db_name))
            conn.cursor().execute('CREATE DATABASE {}'.format(db_name))

        conn.close()

    def initdb(self):
        print('INITDB')
        conn = psycopg2.connect(self.pg_dsn_test)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        with open(self.pg_data_sql, 'r') as source:
            conn.cursor().execute(source.read())
        conn.close()

    def dropdb(self):
        print('DROPDB')
        db_name = self.checkdb()
        conn = psycopg2.connect(self.pg_dsn_main)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        conn.cursor().execute('''
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity WHERE datname = '{}'
            AND pid <> pg_backend_pid()
        '''.format(db_name))

        conn.cursor().execute('DROP DATABASE {}'.format(db_name))
        conn.close()

    def on_start(self):
        self.createdb()
        if self.pg_data_sql:
            try:
                self.initdb()
            except Exception as e:
                print('FALED INIT:', e)
                raise

    def on_end(self):
        self.dropdb()

    def startTestClass(self, testcls):
        testcls.PG_DSN = self.pg_dsn_test
