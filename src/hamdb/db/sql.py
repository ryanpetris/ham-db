#!/usr/bin/env python3

import psycopg2 as db

from .static_queries import cmd_init, cmd_drop_all
from ..common.settings import DB_NAME, DB_PREFIX
from ..fcc import Record
from decimal import Decimal
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from _typeshed.dbapi import DBAPIConnection, DBAPICursor


class SqlBase:
    def __init__(self, dbname: str = None):
        self._conn: DBAPIConnection = db.connect(database=dbname or DB_NAME, sslmode="disable")


class SqlReader(SqlBase):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def execute(self, command: str, params: Dict[str, any]):
        with self._conn.cursor() as cursor:
            cursor: DBAPICursor
            cursor.execute(command, params)

            for row in cursor.fetchall():
                data = {}

                for i in range(0, len(cursor.description)):
                    row_data = row[i]

                    if isinstance(row_data, Decimal):
                        row_data = int(row_data)

                    data[cursor.description[i][0]] = row_data

                yield data

    def get_callsign_data(self, callsign: str):
        params = {
            'callsign': callsign
        }

        hd_record = next(iter(sorted(sorted([
            r for r in self.execute(f'SELECT unique_system_identifier, license_status, effective_date FROM {DB_PREFIX}hd WHERE callsign = %(callsign)s', params)
        ], key=lambda r: r["effective_date"]), key=lambda r: r["license_status"])), None)

        if not hd_record:
            return None

        return self.get_unique_identifier_data(hd_record["unique_system_identifier"])

    def get_frn_data(self, frn: str):
        params = {
            'frn': frn
        }

        en_record = next(self.execute(f'SELECT unique_system_identifier FROM {DB_PREFIX}en WHERE frn = %(frn)s', params), None)

        if not en_record:
            return None

        return self.get_unique_identifier_data(en_record["unique_system_identifier"])

    def get_unique_identifier_data(self, identifier: int):
        data = {}
        params = {
            'identifier': identifier
        }

        for table in Record.get_types():
            table = table.lower()

            command = f'SELECT * FROM {DB_PREFIX}{table} WHERE unique_system_identifier = %(identifier)s;'
            rows = list(self.execute(command, params))

            if not rows:
                continue

            if table in ['am', 'en', 'hd', 'sf']:
                data[table] = rows[0]
            else:
                data[table] = rows

        return data


class SqlWriter(SqlBase):
    def __init__(self, dbname: str = None, fresh: bool = False):
        super().__init__(dbname)
        self._insert_cache = {}

        if fresh:
            self._drop_all_tables()

        self._init_database()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()

    def commit(self):
        self._conn.commit()

    def insert(self, record: Record):
        command = self.get_insert_cmd(record)

        with self._conn.cursor() as cursor:
            cursor.execute(command, record.__dict__)

    def insert_many(self, record: List[Record]):
        command = self.get_insert_cmd(record[0])

        with self._conn.cursor() as cursor:
            cursor: DBAPICursor
            cursor.executemany(command, [r.__dict__ for r in record])

    def get_insert_cmd(self, record: Record):
        command = self._insert_cache.get(record.record_def.record_type, None)

        if command is None:
            command = "INSERT INTO "
            command += DB_PREFIX
            command += record.record_def.record_type.lower()
            command += " ("
            command += str.join(", ", record.record_def.fields)
            command += ") VALUES ("
            command += str.join(", ", (f"%({f})s" for f in record.record_def.fields))
            command += ");"

            self._insert_cache[record.record_def.record_type] = command

        return command

    def _init_database(self):
        with self._conn.cursor() as cursor:
            cursor.execute(cmd_init)

    def _drop_all_tables(self):
        with self._conn.cursor() as cursor:
            cursor.execute(cmd_drop_all)
