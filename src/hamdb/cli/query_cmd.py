#!/usr/bin/env python3

import sys

from ..common import die, dump_json
from ..db import SqlConnection
from ..fcc import FccAdapter


def query_main():
    if len(sys.argv) < 2:
        die("Please specify callsign to query.")

    with FccAdapter(SqlConnection()) as fcc:
        data = fcc.get_callsign_data(sys.argv[1])

        print(dump_json(data))


if __name__ == "__main__":
    query_main()
