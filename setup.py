#!/usr/bin/env python3

from setuptools import setup, find_packages

NAME = 'hamdb'
VERSION = '0.0.8'
DESCRIPTION = 'Ham Database CLI and API'
LONG_DESCRIPTION = 'Database of Amateur Radio Licensee Information'
AUTHOR = 'Ryan Petris'
AUTHOR_EMAIL = 'ryan@petris.net'
LICENSE = 'AGPL3'
PLATFORMS = 'Any'
URL = 'https://github.com/ryanpetris/ham-db'
DOWNLOAD_URL = 'https://github.com/ryanpetris/ham-db'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License version 3 (AGPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
]
PROJECT_URLS = {
   'Bug Tracker': 'https://github.com/ryanpetris/ham-db/issues',
   'Source Code': 'https://github.com/ryanpetris/ham-db',
}
COMMANDS = [
    'import',
    'query',
    'sync',
    'web'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    platforms=PLATFORMS,
    url=URL,
    download_url=DOWNLOAD_URL,
    classifiers=CLASSIFIERS,
    project_urls=PROJECT_URLS,
    python_requires='>=3.11',
    install_requires=[
        'dict2xml',
        'Flask',
        'psycopg',
        'psycopg[binary,pool]',
        'PyYAML'
    ],
    package_dir={
        '': 'src'
    },
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [f'hamdb-{c} = hamdb.cli.{c}_cmd:{c}_main' for c in COMMANDS]
    }
)
