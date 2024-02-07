#!/usr/bin/env python3

import psycopg
import psycopg.conninfo

from .queries import cmd_init
from ..common.settings import DB_HOST, DB_PORT, DB_NAME, DB_USERNAME, DB_PASSWORD
from decimal import Decimal
from typing import TYPE_CHECKING, Iterable, Optional

if TYPE_CHECKING:
    from _typeshed.dbapi import DBAPIConnection, DBAPICursor


class SqlReadOnlyException(Exception):
    def __init__(self, message=None, *args, **kwargs):
        if not message:
            message = 'Attempted to run write command on read-only connection.'

        # noinspection PyArgumentList
        super().__init__(message, *args, **kwargs)


class SqlConnection:
    @property
    def readonly(self) -> bool:
        return self._readonly

    def __init__(self, dbname: str = None, readonly: bool = True):
        self._readonly: bool = readonly
        self._conn: DBAPIConnection = psycopg.connect(_get_db_conninfo(sslmode='disable'))

        if self._readonly:
            self._conn.read_only = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._readonly:
            self.commit()

    def _throw_if_readonly(self):
        if self._readonly:
            raise SqlReadOnlyException()

    def commit(self):
        self._throw_if_readonly()
        self._conn.commit()

    def execute(self, command: str, params: dict[str, any] = None):
        self._throw_if_readonly()

        with self._conn.cursor() as cursor:
            cursor.execute(command, params)

    def execute_kw(self, command: str, **kwargs):
        return self.execute(command, kwargs)

    def execute_many(self, command: str, params: list[dict[str, any]]):
        self._throw_if_readonly()

        with self._conn.cursor() as cursor:
            cursor: DBAPICursor
            cursor.executemany(command, params)

    def fetch(self, command: str, params: dict[str, any] = None) -> Iterable[dict[str, any]]:
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

    def fetch_kw(self, command: str, **kwargs) -> Iterable[dict[str, any]]:
        return self.fetch(command, kwargs)

    def get_setting(self, name: str) -> Optional[str]:
        result = self.fetch_kw('SELECT value FROM settings WHERE name = %(name)s', name=name)
        item = next(iter(result), None)

        if not item:
            return None

        return item['value']

    def init(self):
        self._throw_if_readonly()
        self.execute(cmd_init)

    def schema_exists(self, schema: str):
        result = self.fetch_kw('SELECT true AS schema_exists FROM information_schema.schemata WHERE schema_name = %(schema)s;', schema=schema)
        item = next(iter(result), None)

        return item and item.get('schema_exists', False)

    def set_setting(self, name: str, value: str):
        self._throw_if_readonly()
        self.execute_kw('INSERT INTO settings (name, value) VALUES (%(name)s, %(value)s) ON CONFLICT (name) DO UPDATE SET value = EXCLUDED.value', name=name, value=value)


def _get_db_conninfo(**kwargs):
    params = {
        'dbname': DB_NAME,
        **kwargs
    }

    if DB_HOST:
        params['host'] = DB_HOST

    if DB_PORT:
        params['port'] = DB_PORT

    if DB_USERNAME:
        params['user'] = DB_USERNAME

    if DB_PASSWORD:
        params['password'] = DB_PASSWORD

    return psycopg.conninfo.make_conninfo(**params)
