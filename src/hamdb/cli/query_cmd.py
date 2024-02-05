#!/usr/bin/env python3

import sys

from ..common import die, dump_json
from ..db import SqlReader


def query_main():
    if len(sys.argv) < 2:
        die("Please specify callsign to query.")

    with SqlReader() as sql:
        sql: SqlReader

        data = sql.get_callsign_data(sys.argv[1])

        print(dump_json(data))


if __name__ == "__main__":
    query_main()
