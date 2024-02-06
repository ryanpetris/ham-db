#!/usr/bin/env python3

import sys

from ..authorities.fcc import fcc_import
from ..authorities.ised import ised_import
from ..common import die


def import_main():
    if len(sys.argv) < 2:
        die('Please specify authority')

    authority = sys.argv[1]
    args = sys.argv[2:]

    if authority.lower() == 'fcc':
        fcc_import(args)
    elif authority.lower() == 'ised':
        ised_import(args)
    else:
        die(f'Invalid authority: {authority}')


if __name__ == "__main__":
    import_main()
