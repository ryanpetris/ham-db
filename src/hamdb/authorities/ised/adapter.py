#!/usr/bin/env python3

from typing import Optional

from .sql_queries import cmd_full_init
from ...common.settings import DB_SCHEMA_ISED
from ...db import SqlConnection


class IsedAdapter:
    def __init__(self, conn: SqlConnection):
        self._conn = conn
        self._insert_cache = {}

    def _get_insert_cmd(self, table: str, data: dict[str, str]):
        command = self._insert_cache.get(table, None)

        if command is None:
            command = "INSERT INTO "
            command += DB_SCHEMA_ISED
            command += "."
            command += table
            command += " ("
            command += str.join(", ", data.keys())
            command += ") VALUES ("
            command += str.join(", ", (f"%({f})s" for f in data.keys()))
            command += ");"

            self._insert_cache[table] = command

        return command

    def clear_schema(self):
        self._conn.execute(cmd_full_init)

    def find_individual(self, first_name: str, last_name: str, postal_code: str) -> Optional[dict[str, any]]:
        return self._conn.fetch_one(
            f'SELECT * FROM {DB_SCHEMA_ISED}.licenses WHERE club_name IS NULL AND first_name = %(first_name)s AND surname = %(last_name)s AND postal_code = %(postal_code)s',
            first_name=first_name,
            last_name=last_name,
            postal_code=postal_code
        )

    def get_callsign_data(self, callsign: str) -> Optional[dict[str, any]]:
        return self._conn.fetch_one(f'SELECT * FROM {DB_SCHEMA_ISED}.licenses WHERE callsign = %(callsign)s',
                                    callsign=callsign)

    def insert(self, table: str, data: dict[str, str]):
        command = self._get_insert_cmd(table, data)
        self._conn.execute(command, **data)

    def insert_many(self, table, data: list[dict[str, str]]):
        command = self._get_insert_cmd(table, data[0])
        self._conn.execute_many(command, data)
