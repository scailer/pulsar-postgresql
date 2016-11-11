# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='pulsar-postgresql',
    version='0.1.0',
    author='Dmitriy Vlasov',
    author_email='scailer@yandex.ru',

    packages=['pg_store'],
    include_package_data=True,
    install_requires=['aiopg==0.9.2'],
    requires=['aiopg', 'pulsar (>= 1.4.0)'],

    url='https://github.com/scailer/pulsar-postgresql',
    license='MIT license',
    description='Pulsar store for postgresql database based on aiopg',

    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Pulsar',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
    ),
)
