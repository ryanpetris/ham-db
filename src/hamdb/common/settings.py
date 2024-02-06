#!/usr/bin/env python3
import os

DB_NAME: str = os.environ.get('HAMDB_DB_NAME', 'hamdb')
DB_SCHEMA_FCC: str = os.environ.get('HAMDB_DB_SCHEMA_FCC', 'fcc')
DB_SCHEMA_ISED: str = os.environ.get('HAMDB_DB_SCHEMA_ISED', 'ised')
