#!/usr/bin/env python3

import sys

from ..common import eprint, get_authority, get_known_authority_codes
from ..licenses import repopulate_licenses


def import_main():
    authority_codes = get_known_authority_codes()
    args = sys.argv[1:]
    did_anything = False

    if args and args[0].upper() in authority_codes:
        authority_codes = [args[0].upper()]
        args = args[1:]

    for authority_code in authority_codes:
        authority = get_authority(authority_code)
        eprint(f'Processing {authority.code} data...')

        did_anything = authority.run_import(args) or did_anything

    if did_anything:
        repopulate_licenses()


if __name__ == "__main__":
    import_main()
