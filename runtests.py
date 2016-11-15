# -*- coding: utf-8 -*-

from pulsar.apps.test import TestSuite
from pg_store import PGServer, TestPGDSN, TestPGDataSQL  # noqa


if __name__ == '__main__':
    TestSuite(modules=['tests']).start()
