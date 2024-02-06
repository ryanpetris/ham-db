#!/usr/bin/env python3

from .adapter import FccAdapter
from .download import get_daily_files, get_full_file
from .parser import parse_fcc_zip
from .records import Record
from ...common import eprint
from ...common.settings import DB_SCHEMA_FCC
from ...db import SqlConnection
from typing import Iterable


FCC_LICENSE_FILE_LAST_DATE_SETTING: str = 'fcc_license_file_last_date'


def fcc_import(args: list[str]):
    full_import = len(args) >= 1 and args[0] == 'full'
    sql = SqlConnection(readonly=False)
    sql.init()

    if full_import or not sql.schema_exists(DB_SCHEMA_FCC):
        _process_full_file(sql)

    _process_daily_file(sql)


def _insert_rows(fcc: FccAdapter, rows: Iterable[list[str]]):
    batch = []
    batch_count = 0

    record_type = None
    record_count = 0

    def process_batch():
        nonlocal batch, batch_count

        if batch_count == 0:
            return

        fcc.insert_many(batch)

        batch = []
        batch_count = 0

    def finish_record_type():
        nonlocal record_type, record_count

        eprint(f"Completed record type {record_type} with {record_count} records")

        record_type = None
        record_count = 0

    for row in rows:
        item = Record.init(row[0], row)

        if record_type and record_type != item.record_type:
            process_batch()
            finish_record_type()

        if not record_type:
            record_type = item.record_type

            eprint(f"Processing record type {record_type}...")

        batch.append(item)
        batch_count += 1
        record_count += 1

        if batch_count % 10000 == 0:
            process_batch()

        if record_count % 100000 == 0:
            eprint(f"Processed {record_count} records")

    process_batch()
    finish_record_type()


def _process_full_file(sql: SqlConnection):
    with FccAdapter(sql) as fcc:
        file = get_full_file()

        fcc.clear_schema()
        _insert_rows(fcc, parse_fcc_zip(file.file.name))
        sql.set_setting(FCC_LICENSE_FILE_LAST_DATE_SETTING, file.last_modified)
        sql.commit()


def _process_daily_file(sql: SqlConnection):
    with FccAdapter(sql) as fcc:
        last_modified = sql.get_setting(FCC_LICENSE_FILE_LAST_DATE_SETTING)

        for file in get_daily_files(last_modified):
            eprint(f"Processing file with date {file.last_modified}...")

            rows = list(parse_fcc_zip(file.file.name))
            unique_ids = set(r[1] for r in rows)

            eprint(f'Processing {len(rows)} records for {len(unique_ids)} distinct licenses...')

            fcc.clear_data_for_identifiers([int(i) for i in unique_ids])
            _insert_rows(fcc, rows)
            sql.set_setting(FCC_LICENSE_FILE_LAST_DATE_SETTING, file.last_modified)
            sql.commit()
