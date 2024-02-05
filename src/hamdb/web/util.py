#!/usr/bin/env python3

from ..db import SqlReader
from datetime import datetime
from typing import Optional


def query_license(callsign: str = None, frn: str = None, identifier: int = None):
    with SqlReader() as sql:
        if callsign:
            return sql.get_callsign_data(callsign)
        elif frn:
            return sql.get_callsign_data(frn)
        elif identifier:
            return sql.get_unique_identifier_data(identifier)

    return None


def get_basic_data(record):
    return {
        'callsign': record['en']['callsign'],
        'frn': record['en']['frn'],
        'operator_class': record['am']['operator_class'],
        'grant_date': _convert_date(record['hd']['grant_date']),
        'expire_date': _convert_date(record['hd']['expired_date']),
        'convicted_felon': _convert_yes_no(record['hd']['convicted']),
        'name': {
            'full': record['en']['entity_name'],
            'first': record['en']['first_name'],
            'middle': record['en']['mi'],
            'last': record['en']['last_name']
        },
        'address': {
            'line1': record['en']['street_address'],
            'city': record['en']['city'],
            'state': record['en']['state'],
            'zip': record['en']['zip_code'],
        }
    }


def _convert_date(value: Optional[str]) -> Optional[str]:
    return datetime.strptime(value, '%m/%d/%Y').strftime('%Y-%m-%d')


def _convert_yes_no(value: Optional[str]) -> Optional[bool]:
    if not value:
        return None

    value = value.upper()

    if value == 'Y':
        return True
    elif value == 'N':
        return False

    return None
