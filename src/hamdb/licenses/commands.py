#!/usr/bin/env python3

from .adapter import LicensesAdapter
from ..common import eprint
from ..db import SqlConnection


def repopulate_licenses():
    eprint('Repopulating license database...')

    with LicensesAdapter(SqlConnection(readonly=False)) as licenses:
        licenses.repopulate()
