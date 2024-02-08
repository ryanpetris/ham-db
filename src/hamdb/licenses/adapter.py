#!/usr/bin/env python3

from .sql_queries import cmd_init
from ..authorities.fcc.sql_queries import cmd_license_insert as cmd_fcc_license_insert
from ..authorities.ised.sql_queries import cmd_license_insert as cmd_ised_license_insert
from ..common.settings import DB_SCHEMA_LICENSES
from ..db import SqlConnection
from typing import Optional


class LicensesAdapter:
    def __init__(self, conn: SqlConnection):
        self._conn = conn
        self._insert_cache = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._conn.readonly:
            self._conn.commit()

    def query_callsign(self, callsign: str) -> Optional[dict[str, any]]:
        result = self._conn.fetch_kw(f'SELECT * FROM {DB_SCHEMA_LICENSES}.licenses WHERE callsign = %(callsign)s', callsign=callsign)
        data = next(iter(result), None)

        if not data:
            return None

        if data['entity_type'] != 'I':
            data['administrators'] = []
            administrators = self._conn.fetch_kw(f'SELECT admin_callsign FROM {DB_SCHEMA_LICENSES}.administrators WHERE callsign = %(callsign)s', callsign=callsign)

            for item in administrators:
                data['administrators'].append(self.query_callsign(item['admin_callsign']))
        else:
            qualifications = self._conn.fetch_kw(f'SELECT qualification FROM {DB_SCHEMA_LICENSES}.qualifications WHERE callsign = %(callsign)s', callsign=callsign)
            data['qualifications'] = [i['qualification'] for i in qualifications]

        return data

    def repopulate(self):
        self._conn.execute(cmd_init)
        self._conn.execute(cmd_fcc_license_insert)
        self._conn.execute(cmd_ised_license_insert)
