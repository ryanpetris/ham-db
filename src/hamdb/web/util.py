#!/usr/bin/env python3

from ..db import SqlReader
from datetime import datetime
from typing import List, Optional


def query_license(callsign: str = None, frn: str = None, identifier: int = None):
    with SqlReader() as sql:
        if callsign:
            return sql.get_callsign_data(callsign)
        elif frn:
            return sql.get_callsign_data(frn)
        elif identifier:
            return sql.get_unique_identifier_data(identifier)

    return None


def query_basic_data(callsign: str = None, frn: str = None, identifier: int = None):
    data = query_license(callsign, frn, identifier)

    if not data:
        return None

    response = get_basic_data(data)
    trustee_callsign = data['am'].get('trustee_callsign', None)

    if trustee_callsign:
        trustee_data = query_license(trustee_callsign)

        if trustee_data:
            response["administrators"] = [get_basic_data(trustee_data)]

    return response


def get_basic_data(record):
    return {
        'callsign': record['en']['callsign'],
        'status': _convert_license_status(record['hd']['license_status']),
        'license': {
            'authority': 'FCC',
            'qualifications': _convert_operator_class(record['am']['operator_class']),
            'grant_date': _convert_date(record['hd']['grant_date']),
            'expiration_date': _convert_date(record['hd']['expired_date']),
        },
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
            'zip': record['en']['zip_code']
        },
        'authority_data': {
            'frn': record['en']['frn'],
            'licensee_id': record['en']['licensee_id'],
            'unique_system_identifier': record['en']['unique_system_identifier'],
            'is_convicted_felon': _convert_yes_no(record['hd']['convicted'])
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

    if value == 'N':
        return False

    return None


def _convert_operator_class(value: Optional[str]) -> Optional[List[str]]:
    if not value:
        return None

    value = value.upper()

    if value == 'E':
        return ['FCC:AMATEUR_EXTRA']

    if value == 'A':
        return ['FCC:ADVANCED']

    if value == 'G':
        return ['FCC:GENERAL']

    if value == 'P':
        return ['FCC:TECHNICIAN_PLUS']

    if value == 'T':
        return ['FCC:TECHNICIAN']

    if value == 'N':
        return ['FCC:NOVICE']

    return None


def _convert_license_status(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    value = value.upper()

    if value == 'A':
        return 'ACTIVE'

    if value == 'C':
        return 'NOT_ACTIVE'

    if value == 'E':
        return 'NOT_ACTIVE'

    if value == 'T':
        return 'NOT_ACTIVE'

    if value == 'L':
        return 'ACTION_PENDING'

    if value == 'X':
        return 'ACTION_PENDING'

    if value == 'P':
        return None

    return None
