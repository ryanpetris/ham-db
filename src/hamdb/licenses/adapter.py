#!/usr/bin/env python3

from .sql_queries import cmd_init, cmd_license_query
from ..common import get_known_authority_codes, get_authority
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

    def query_callsign(self, *args: str, **kwargs: any) -> Optional[list[dict[str, any]]]:
        if not args:
            return None

        items = list(self._conn.fetch(cmd_license_query, callsigns=list(args)))
        licenses = [i.get('data') for i in items if i.get('type') == 'L']
        all_admin_callsigns = set(i.get('data').get('admin_callsign') for i in items if i.get('type') == 'A')
        administrators = None

        if all_admin_callsigns and not kwargs.get('for_admins', None):
            administrators = self.query_callsign(*all_admin_callsigns, for_admins=True)

        for data in licenses:
            data['qualifications'] = [i.get('data').get('qualification') for i in items if i.get('callsign') == data.get('callsign') and i.get('type') == 'Q']

            if administrators:
                admin_callsigns = [i.get('data').get('admin_callsign') for i in items if i.get('callsign') == data.get('callsign') and i.get('type') == 'A']
                data['administrators'] = [i for i in administrators if i.get('callsign') in admin_callsigns]

        return licenses

    def query_callsign_one(self, callsign: str) -> Optional[dict[str, any]]:
        result = self.query_callsign(callsign)

        if not result:
            return None

        return next(iter(result), None)

    def repopulate(self):
        self._conn.execute(cmd_init)

        for code in get_known_authority_codes():
            authority = get_authority(code)

            if authority.sync_sql_command:
                self._conn.execute(authority.sync_sql_command)
