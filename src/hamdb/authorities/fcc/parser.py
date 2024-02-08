#!/usr/bin/env python3

import csv
import io

from typing import IO, Iterable
from zipfile import ZipFile


def parse_fcc_zip(zip_data: IO[bytes]) -> Iterable[list[str]]:
    with ZipFile(zip_data, 'r') as zf:
        for file in zf.filelist:
            if not file.filename.endswith(".dat"):
                continue

            with zf.open(file, 'r') as f:
                with io.TextIOWrapper(f, newline="\r\n") as w:
                    for row in parse_fcc_csv(w):
                        yield row


def parse_fcc_csv(data: Iterable[str]) -> Iterable[list[str]]:
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
