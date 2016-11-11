# pulsar-postgresql
Pulsar store for postgresql database

## Install

Rquires pulsar >= 1.5.4

```
$ pip install pulsar-postgresql
OR
$ pip install git+https://github.com/scailer/pulsar-postgresql
```

## Usage

Basic

```
>>> import asyncio
>>> import pg_store
>>> from pulsar.apps.data import create_store
>>> 
>>> loop = asyncio.get_current_loop()
>>> store = create_store('postgresql://user:pass@localhost:5432/db')
>>> res = loop.run_until_complete(store.fetch_list('SELECT id, title FROM table'))
>>> res
[{'id': 1, 'title': 'a'}, {'id': 2, 'title': 'b'}, {'id': 3, 'title': 'c'}]
```

Pulsar app

```python
class Web(wsgi.LazyWsgi):
    def setup(self, environ):
        cfg = environ['pulsar.cfg']
        loop = environ['pulsar.connection']._loop
        pg_dsn = cfg.settings.get('pg_server').value,
        self.pg_store = create_store(pg_dsn, loop=loop, pool_size=10, timeout=60.0)
        ...
        
    async def page(self, request):
        data = await self.pg_store.fetch_list('SELECT id, title FROM table')
        ...
```

```python
def main():
    Server(pg_server='postgresql://user:pass@localhost:5432/db').start()
```

OR

```
$ python runserver.py --pg-server postgresql://user:pass@localhost:5432/db
```

## Testing

PGPlugin create test database with "test" postfix, optionaly init it from sql file and drop it after tests end.
Insure that all option classes imported before test runner init. 
For safety if db host is not localhost you must confirm actions with database.

--test-pg-dsn - database for access and manage, from it will create test database
--test-pg-data-source - path to file with sql for init test database

```
$ python runtests.py --test-plugins pg_store.tests.PGPlugin \
  --test-pg-dsn postgresql://user:pass@localhost:5432/db \
  --test-pg-data-source tests/pg_schema.sql
```

```python
class MyTest(TestCase):
    @classmethod
    async def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()
        # Plugin add to each testcase PG_DSN attribute
        cls.pg = create_store(cls.PG_DSN, loop=cls.loop)
```
