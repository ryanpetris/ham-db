#!/usr/bin/env python3

import csv
import io

from typing import IO, Iterable
from zipfile import ZipFile


ISED_CSV_HEADERS: list[str] = [
    'callsign',
    'first_name',
    'surname',
    'address_line',
    'city',
    'prov_cd',
    'postal_code',
    'qual_a',
    'qual_b',
    'qual_c',
    'qual_d',
    'qual_e',
    'club_name',
    'club_name_2',
    'club_address',
    'club_city',
    'club_prov_cd',
    'club_postal_code'
]


def parse_ised_zip(zip_data: IO[bytes]) -> Iterable[dict[str, str]]:
    with ZipFile(zip_data, 'r') as zf:
        for file in zf.filelist:
            if not file.filename == 'amateur_delim.txt':
                continue

            with zf.open(file, 'r') as f:
                with io.TextIOWrapper(f, newline="\r\n") as w:
                    for row in parse_ised_csv(w):
                        yield row


def parse_ised_csv(data: Iterable[str]) -> Iterable[dict[str, str]]:
    reader = csv.reader(data, dialect='unix', delimiter=";", quoting=csv.QUOTE_NONE, strict=False)
    expected_length = len(ISED_CSV_HEADERS)
    is_first_line = True

    for row in reader:
        if is_first_line:
            is_first_line = False
            continue

        if len(row) != expected_length:
            raise Exception(f"record length mismatch; expected {expected_length}, received {len(row)}")

        data = {}

        for i in range(0, expected_length):
            value = row[i].strip()

            if not value:
                value = None

            data[ISED_CSV_HEADERS[i]] = value

        yield data
