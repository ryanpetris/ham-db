#!/usr/bin/env python3
import os

DB_NAME: str = os.environ.get('HAMDB_DB_NAME', 'hamdb')
DB_PREFIX: str = os.environ.get('HAMDB_DB_PREFIX', 'fcc_')