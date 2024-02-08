#!/usr/bin/env python3

from .adapter import IsedAdapter
from .download import get_full_file
from .parser import parse_ised_zip
from ...common import eprint
from ...db import SqlConnection
from typing import Iterable


ISED_LICENSE_FILE_LAST_DATE_SETTING: str = 'ised_license_file_last_date'


def run_import(args: list[str]):
    force_download = len(args) >= 1 and args[0] == 'full'
    sql = SqlConnection(readonly=False)
    sql.init()

    return _process_full_file(sql, force_download=force_download)


def _insert_rows(ised: IsedAdapter, rows: Iterable[dict[str, str]]):
    batch = []
    batch_count = 0
    record_count = 0

    def process_batch():
        nonlocal batch, batch_count

        if batch_count == 0:
            return

        ised.insert_many('licenses', batch)

        batch = []
        batch_count = 0

    for row in rows:
        batch.append(row)
        batch_count += 1
        record_count += 1

        if batch_count % 10000 == 0:
            process_batch()

        if record_count % 100000 == 0:
            eprint(f"Processed {record_count} records")

    process_batch()
    eprint(f"Completed license import with {record_count} records")


def _process_full_file(sql: SqlConnection, force_download: bool = False):
    ised = IsedAdapter(sql)
    last_modified = None

    if not force_download:
        last_modified = sql.get_setting(ISED_LICENSE_FILE_LAST_DATE_SETTING)

    file = get_full_file(last_modified)

    if not file:
        return False

    eprint(f"Processing full file with date {file.last_modified}...")

    ised.clear_schema()
    _insert_rows(ised, parse_ised_zip(file.file))
    sql.set_setting(ISED_LICENSE_FILE_LAST_DATE_SETTING, file.last_modified)
    sql.commit()

    return True
