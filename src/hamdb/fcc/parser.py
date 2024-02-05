#!/usr/bin/env python3

import csv
import io

from ..common import eprint
from typing import Iterable
from zipfile import ZipFile


def parse_fcc_zip(zip_path: str):
    with ZipFile(zip_path, 'r') as zf:
        for file in zf.filelist:
            if not file.filename.endswith(".dat"):
                continue

            eprint(f"Processing file {file.filename}...")
            processed = 0

            with zf.open(file, 'r') as f:
                with io.TextIOWrapper(f, newline="\r\n") as w:
                    for row in parse_fcc_csv(w):
                        yield row

                        processed += 1

                        if processed % 100000 == 0:
                            eprint(f"Processed {processed} records")

            eprint(f"Completed file {file.filename} with {processed} records")


def parse_fcc_csv(data: Iterable[str]):
    reader = csv.reader(_fcc_csv_fixer(data), dialect='unix', delimiter="|", quoting=csv.QUOTE_NONE, strict=False)

    for row in reader:
        yield list(_fcc_result_fixer(row))


def _fcc_csv_fixer(data: Iterable[str]) -> Iterable[str]:
    partial_line = ""

    for line in data:
        if line.endswith("\r\r\n"):
            partial_line += line
            continue

        result = partial_line.replace("\n", "\\n") + line
        partial_line = ""

        yield result.replace("\r", "").replace("\n", "")


def _fcc_result_fixer(data: Iterable[str]) -> Iterable[str]:
    for item in data:
        yield item.replace("\\n", "\n").strip()
