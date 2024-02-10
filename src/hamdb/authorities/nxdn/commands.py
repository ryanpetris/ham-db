#!/usr/bin/env python3

import csv
import io
from typing import Iterable

from .sql_queries import cmd_full_init
from ...common import download_file
from ...common.settings import DB_SCHEMA_NXDN
from ...db import SqlConnection

LICENSE_FULL_URL: str = 'https://radioid.net/static/nxdn.csv'
LAST_DATE_SETTING: str = 'nxdn_id_file_last_date'


def run_import(args: list[str]) -> bool:
    force_download = len(args) >= 1 and args[0] == 'full'
    sql = SqlConnection(readonly=False)
    last_modified = None

    sql.init()

    if not force_download:
        last_modified = sql.get_setting(LAST_DATE_SETTING)

    file = download_file(LICENSE_FULL_URL, only_after=last_modified)

    if not file:
        return False

    rows = []
    first_row = True

    with io.TextIOWrapper(file.file) as w:
        for row in _parse_csv(w):
            if first_row:
                first_row = False
                continue

            rows.append({
                'callsign': row[1],
                'nxdnid': int(row[0]),
                'first_name': row[2],
                'last_name': row[3],
                'city': row[4],
                'state': row[5],
                'country': row[6]
            })

    sql.execute(cmd_full_init)
    sql.execute_many(
        f'INSERT INTO {DB_SCHEMA_NXDN}.nxdnids (callsign, nxdnid, first_name, last_name, city, state, country) VALUES (%(callsign)s, %(nxdnid)s, %(first_name)s, %(last_name)s, %(city)s, %(state)s, %(country)s);',
        rows)
    sql.set_setting(LAST_DATE_SETTING, file.last_modified)
    sql.commit()

    return True


def _parse_csv(data: Iterable[str]) -> Iterable[list[str]]:
    reader = csv.reader(data, dialect='unix', delimiter=",", quoting=csv.QUOTE_NONE)

    for row in reader:
        yield row
