#!/usr/bin/env python3

import sys

from ..common import die
from ..common.settings import DB_NAME
from ..fcc import parse_fcc_zip, Record
from ..db import SqlWriter


def import_main():
    if len(sys.argv) < 2:
        die("Please specify zip file to import.")

    with SqlWriter(fresh=True) as sw:
        batch = []
        batch_count = 0

        def process_batch():
            nonlocal batch, batch_count

            if batch_count == 0:
                return

            sw.insert_many(batch)

            batch = []
            batch_count = 0

        for row in parse_fcc_zip(sys.argv[1]):
            item = Record.init(row[0], row)

            if batch and batch[0].record_type != item.record_type:
                process_batch()

            batch.append(item)
            batch_count += 1

            if batch_count % 10000 == 0:
                process_batch()

        process_batch()


if __name__ == "__main__":
    import_main()
