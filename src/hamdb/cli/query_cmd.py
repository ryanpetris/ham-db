#!/usr/bin/env python3

import sys

from ..common import die, dump_json
from ..licenses import query_basic_data


def query_main():
    if len(sys.argv) < 2:
        die("Please specify callsign to query.")

    data = query_basic_data(sys.argv[1])

    if data:
        print(dump_json(data))


if __name__ == "__main__":
    query_main()
