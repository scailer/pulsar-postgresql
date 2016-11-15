# -*- coding: utf-8 -*-

import unittest

from pg_store.store import PGStore  # noqa
from pg_store.tests import PGPlugin  # noqa
from pg_store import TestPGDSN, TestPGDataSQL
from pulsar.apps.data import create_store
import pulsar


class TestPlugin(unittest.TestCase):
    async def test_cfg(self):
        cfg = pulsar.Config()
        pgserver, testdata = TestPGDSN(), TestPGDataSQL()
        pgserver.value = 'postgresql://user:pass@localhost:5432/db'
        testdata.value = 'db.sql'
        cfg.settings['test_pg_dsn'] = pgserver
        cfg.settings['test_pg_data'] = testdata
        PGPlugin().configure(cfg)


class TestStore(unittest.TestCase):
    def setUp(self):
        self.pg = create_store(self.PG_DSN, pool_size=2, timeout=9)

    async def test_list(self):
        ret = await self.pg.safe_fetch_list(
            'SELECT id, title FROM mytable ORDER BY id')
        self.assertEqual(len(ret), 3)
        self.assertEqual(ret[0]['id'], 1)
        self.assertEqual(ret[0]['title'], 'a')

    async def test_object(self):
        ret = await self.pg.safe_fetch_object(
            'SELECT id, title FROM mytable ORDER BY id')
        self.assertEqual(ret['id'], 1)
        self.assertEqual(ret['title'], 'a')

    async def test_flat(self):
        ret = await self.pg.safe_fetch_flat(
            'SELECT title FROM mytable ORDER BY id')
        self.assertEqual(ret[0], 'a')

    async def test_execute(self):
        ret = await self.pg.safe_execute(
            'SELECT id, title FROM mytable ORDER BY id')
        self.assertEqual(ret, None)

    async def test_scalar(self):
        ret = await self.pg.fetch_scalar(
            'SELECT id, title FROM mytable ORDER BY id')
        self.assertEqual(ret, 1)

    async def test_exist(self):
        ret = await self.pg.fetch_exist(
            'SELECT id, title FROM mytable ORDER BY id')
        self.assertEqual(ret, True)

    async def test_empty_list(self):
        ret = await self.pg.safe_fetch_list(
            'SELECT id, title FROM mytable WHERE id > 100')
        self.assertEqual(ret, [])

    async def test_empty_object(self):
        ret = await self.pg.safe_fetch_object(
            'SELECT id, title FROM mytable WHERE id > 100')
        self.assertEqual(ret, {})

    async def test_err(self):
        ret = await self.pg.safe_fetch_list('SELECT id, tit FROM mytable')
        self.assertEqual(ret, None)

    async def test_conn(self):
        ret = self.pg.connect()
        self.assertNotEqual(ret, None)
