# -*- coding: utf-8 -*-

from pulsar.utils.config import Global, TestOption
from pulsar.apps.data import register_store


class PGServer(Global):
    name = 'pg_server'
    flags = ['--pg-server']
    meta = "CONNECTION_STRING"
    default = 'postgres://postgres:postgres@localhost:5432/database'
    desc = 'Default connection string for the postgresql server'


class TestPGDSN(TestOption):
    name = "test_pg_dsn"
    flags = ['--test-pg-dsn']
    desc = 'Connection string for the postgresql server with test database'


class TestPGDataSQL(TestOption):
    name = "test_pg_data"
    flags = ['--test-pg-data-source']
    desc = "Source files with SQL for init database"


register_store('postgresql', 'pg_store.store.PGStore')
