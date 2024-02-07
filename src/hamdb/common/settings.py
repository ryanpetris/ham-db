#!/usr/bin/env python3
import os

DB_HOST: str = os.environ.get('HAMDB_DB_HOST', None)
DB_PORT: str = os.environ.get('HAMDB_DB_PORT', None)
DB_NAME: str = os.environ.get('HAMDB_DB_NAME', 'hamdb')
DB_USERNAME: str = os.environ.get('HAMDB_DB_USERNAME', None)
DB_PASSWORD: str = os.environ.get('HAMDB_DB_PASSWORD', None)
DB_SCHEMA_FCC: str = os.environ.get('HAMDB_DB_SCHEMA_FCC', 'fcc')
DB_SCHEMA_ISED: str = os.environ.get('HAMDB_DB_SCHEMA_ISED', 'ised')
