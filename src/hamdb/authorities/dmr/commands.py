#!/usr/bin/env python3

import csv
import io

from .sql_queries import cmd_full_init
from ...common import download_file
from ...common.settings import DB_SCHEMA_DMR
from ...db import SqlConnection
from typing import Iterable

LICENSE_FULL_URL: str = 'https://radioid.net/static/dmrid.dat'
LAST_DATE_SETTING: str = 'dmr_id_file_last_date'


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

    with io.TextIOWrapper(file.file) as w:
        for row in _parse_csv(w):
            rows.append({
                'callsign': row[1],
                'dmrid': int(row[0])
            })

    sql.execute(cmd_full_init)
    sql.execute_many(f'INSERT INTO {DB_SCHEMA_DMR}.dmrids (callsign, dmrid) VALUES (%(callsign)s, %(dmrid)s);', rows)
    sql.set_setting(LAST_DATE_SETTING, file.last_modified)
    sql.commit()

    return True


def _parse_csv(data: Iterable[str]) -> Iterable[list[str]]:
    reader = csv.reader(data, dialect='unix', delimiter=";", quoting=csv.QUOTE_NONE)

    for row in reader:
        yield row
