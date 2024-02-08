#!/usr/bin/env python3

from ..licenses import LicensesAdapter
from ..db import SqlConnection


def sync_main():
    with LicensesAdapter(SqlConnection(readonly=False)) as licenses:
        licenses.repopulate()


if __name__ == "__main__":
    sync_main()
