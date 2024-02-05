#!/usr/bin/env python3

import sys

from ..common import die, eprint
from ..fcc import parse_fcc_zip, Record
from ..db import SqlWriter


def import_main():
    if len(sys.argv) < 2:
        die("Please specify zip file to import.")

    with SqlWriter(fresh=True) as sw:
        batch = []
        batch_count = 0

        record_type = None
        record_count = 0

        def process_batch():
            nonlocal batch, batch_count

            if batch_count == 0:
                return

            sw.insert_many(batch)

            batch = []
            batch_count = 0

        def finish_record_type():
            nonlocal record_type, record_count

            eprint(f"Completed record type {record_type} with {record_count} records")

            record_type = None
            record_count = 0

        for row in parse_fcc_zip(sys.argv[1]):
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


if __name__ == "__main__":
    import_main()
