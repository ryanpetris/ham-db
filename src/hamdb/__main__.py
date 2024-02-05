#!/usr/bin/env python3

from .db import SqlWriter
from .fcc import parse_fcc_zip, Record

with SqlWriter() as sw:
    for row in parse_fcc_zip("data/licenses/l_amat.zip"):
        record = Record.init(row[0], row)
        sw.insert(record)
