#!/usr/bin/env python3

from .records import Record
from .sql_queries import cmd_full_init
from ...common.settings import DB_SCHEMA_FCC
from ...db import SqlConnection


class FccAdapter:
    def __init__(self, conn: SqlConnection):
        self._conn = conn
        self._insert_cache = {}

    def _get_insert_cmd(self, record: Record):
        command = self._insert_cache.get(record.record_def.record_type, None)

        if command is None:
            command = "INSERT INTO "
            command += DB_SCHEMA_FCC
            command += "."
            command += record.record_def.record_type.lower()
            command += " ("
            command += str.join(", ", record.record_def.fields)
            command += ") VALUES ("
            command += str.join(", ", (f"%({f})s" for f in record.record_def.fields))
            command += ");"

            self._insert_cache[record.record_def.record_type] = command

        return command

    def clear_schema(self):
        self._conn.execute(cmd_full_init)

    def clear_data_for_identifiers(self, identifiers: list[int]):
        for table in Record.get_types():
            table = table.lower()

            command = f'DELETE FROM {DB_SCHEMA_FCC}.{table} WHERE unique_system_identifier = ANY(%(identifiers)s);'
            self._conn.execute(command, identifiers=identifiers)

    def get_callsign_data(self, callsign: str):
        hd_record = next(iter(sorted(sorted([
            r for r in self._conn.fetch(
                f'SELECT unique_system_identifier, license_status, effective_date FROM {DB_SCHEMA_FCC}.hd WHERE callsign = %(callsign)s',
                callsign=callsign)
        ], key=lambda r: r["effective_date"]), key=lambda r: r["license_status"])), None)

        if not hd_record:
            return None

        return self.get_unique_identifier_data(hd_record["unique_system_identifier"])

    def get_frn_data(self, frn: str):
        en_record = self._conn.fetch_one(f'SELECT unique_system_identifier FROM {DB_SCHEMA_FCC}.en WHERE frn = %(frn)s',
                                         frn=frn)

        if not en_record:
            return None

        return self.get_unique_identifier_data(en_record["unique_system_identifier"])

    def get_unique_identifier_data(self, identifier: int):
        data = {}

        for table in Record.get_types():
            table = table.lower()

            command = f'SELECT * FROM {DB_SCHEMA_FCC}.{table} WHERE unique_system_identifier = %(identifier)s;'
            rows = list(self._conn.fetch(command, identifier=identifier))

            if not rows:
                continue

            if table in ['am', 'en', 'hd', 'sf']:
                data[table] = rows[0]
            else:
                data[table] = rows

        return data

    def insert(self, record: Record):
        command = self._get_insert_cmd(record)
        self._conn.execute(command, **record.__dict__)

    def insert_many(self, record: list[Record]):
        command = self._get_insert_cmd(record[0])
        self._conn.execute_many(command, [r.__dict__ for r in record])
