# -*- coding: utf-8 -*-
"""
PostgreSQL store for pulsar apps.

Example:

    impoer asyncio
    from pulsar.apps.data import create_store

    loop = asyncio.get_event_loop()
    pg_store = create_store(
        postgresql://scailer:passwd@localhost:5432/dbname,
        loop=loop, pool_size=3, timeout=60.0)

    await pg_store.safe_execute(SQL, *params)
    list = await pg_store.safe_fetch_list(SQL, *params)

"""

import aiopg
import logging
import psycopg2

from functools import wraps
from pulsar.apps.data import RemoteStore
from concurrent.futures import TimeoutError

logger = logging.getLogger('pgstore')


async def safe(operation, *args, **options):
    try:
        return await operation(*args, **options)
    except (psycopg2.Warning, psycopg2.Error) as error:
        logger.error(str(error))
        return None


def error_handler(func):
    @wraps(func)
    async def wrapper(self, *args, **kw):
        try:
            return await func(self, *args, **kw)
        except (TimeoutError, psycopg2.OperationalError) as exc:
            logger.error('PG ERROR: \n{}\n{}\n{}'.format(args[0], args[1:], kw))
            raise
    return wrapper


class PGStore(RemoteStore):
    def _init(self, **kwargs):
        self.pool_size = kwargs.get('pool_size', 10)
        self.timeout = kwargs.get('timeout', 60.0)
        self._pool = aiopg.pool.Pool(
            self.buildurl(), minsize=self.pool_size, maxsize=self.pool_size,
            loop=self._loop, timeout=self.timeout, enable_json=True,
            enable_hstore=True, enable_uuid=True, echo=False, on_connect=None)

    @property
    def pool(self):
        return self._pool

    def connect(self, protocol_factory=None):
        return self.pool.acquire()

    @error_handler
    async def execute(self, *args, **options):
        with await self.pool.cursor() as cur:
            await cur.execute(*args, **options)

    @error_handler
    async def fetchone(self, *args, **options):
        row = None

        with await self.pool.cursor() as cur:
            await cur.execute(*args, **options)
            row = await cur.fetchone()

        return row

    @error_handler
    async def fetchall(self, *args, **options):
        rows = None

        with await self.pool.cursor() as cur:
            await cur.execute(*args, **options)
            rows = await cur.fetchall()

        return rows

    @error_handler
    async def fetch_scalar(self, *args, **options):
        row = await self.fetchone(*args, **options)
        return row[0]

    @error_handler
    async def fetch_exist(self, *args, **options):
        row = await self.fetchone(*args, **options)
        return bool(row)

    @error_handler
    async def fetch_flat(self, *args, **options):
        rows = await self.fetchall(*args, **options)
        return [row[0] for row in rows]

    @error_handler
    async def fetch_object(self, *args, **options):
        """
            Return dict with column name as keys and data as values

            > q = await DB.fetch_object('SELECT * FROM users WHERE id=11')
            < {}

            > q = await DB.fetch_object('SELECT id, name FROM users')
            < {'id': 2L, 'name': 'username'}

            > q = await DB.fetch_object('SELECT 1')
            < {'?column?': 1}
        """

        row = None

        with await self.pool.cursor() as cur:
            await cur.execute(*args, **options)
            row, desc = await cur.fetchone(), cur.description

        if not row:
            return {}

        return {col.name: val for col, val in zip(desc, row)}

    @error_handler
    async def fetch_list(self, *args, **options):
        rows = None

        with await self.pool.cursor() as cur:
            await cur.execute(*args, **options)
            rows, desc = await cur.fetchall(), cur.description

        if not rows:
            return []

        return [{col.name: val for col, val in zip(desc, row)} for row in rows]

    def safe_fetch_list(self, *args, **options):
        return safe(self.fetch_list, *args, **options)

    def safe_fetch_object(self, *args, **options):
        return safe(self.fetch_object, *args, **options)

    def safe_fetch_flat(self, *args, **options):
        return safe(self.fetch_flat, *args, **options)

    def safe_execute(self, *args, **options):
        return safe(self.execute, *args, **options)
