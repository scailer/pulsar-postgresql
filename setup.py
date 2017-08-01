# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='pulsar-postgresql',
    version='0.1.2',
    author='Dmitriy Vlasov',
    author_email='scailer@yandex.ru',

    packages=['pg_store'],
    include_package_data=True,
    install_requires=['aiopg==0.13.0'],
    requires=['aiopg', 'pulsar (>= 1.5.4)'],

    url='https://github.com/scailer/pulsar-postgresql',
    license='MIT license',
    description='Pulsar store for postgresql database based on aiopg',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
