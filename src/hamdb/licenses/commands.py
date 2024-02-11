#!/usr/bin/env python3

from .adapter import LicensesAdapter
from ..common import eprint
from ..db import SqlConnection


def repopulate_licenses():
    eprint('Repopulating license database...')

    sql = SqlConnection(readonly=False)
    sql.init()

    with LicensesAdapter(sql) as licenses:
        licenses.repopulate()
