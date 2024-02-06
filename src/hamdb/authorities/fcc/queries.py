#!/usr/bin/env python3

import re

from .adapter import FccAdapter
from ...db import SqlConnection
from datetime import datetime
from typing import Optional, Pattern


FCC_CALLSIGN_REGEX: Pattern[str] = re.compile('^(A[A-L]|K|N|W)', re.RegexFlag.IGNORECASE)


def fcc_query_basic_data(callsign: str = None, frn: str = None, identifier: int = None) -> Optional[dict[str, any]]:
    data = _query_license(callsign, frn, identifier)

    if not data:
        return None

    response = _get_basic_data(data)
    trustee_callsign = data['am'].get('trustee_callsign', None)

    if trustee_callsign:
        trustee_data = _query_license(trustee_callsign)

        if trustee_data:
            response["administrators"] = [_get_basic_data(trustee_data)]

    return response


def _convert_applicant_type_code(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    value = value.upper()

    if value == 'B':
        return 'CLUB'

    if value == 'G':
        return 'GOVERNMENT'

    if value == 'I':
        return 'INDIVIDUAL'

    if value == 'M':
        return 'MILITARY'

    if value == 'R':
        return 'RACES'

    return None


def _convert_date(value: Optional[str]) -> Optional[str]:
    return datetime.strptime(value, '%m/%d/%Y').strftime('%Y-%m-%d')


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


def _convert_operator_class(value: Optional[str]) -> Optional[list[str]]:
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


def _convert_yes_no(value: Optional[str]) -> Optional[bool]:
    if not value:
        return None

    value = value.upper()

    if value == 'Y':
        return True

    if value == 'N':
        return False

    return None


def _get_basic_data(record: dict[str, any]) -> dict[str, any]:
    return {
        'callsign': record['en']['callsign'],
        'status': _convert_license_status(record['hd']['license_status']),
        'license': {
            'authority': 'FCC',
            'qualifications': _convert_operator_class(record['am']['operator_class']),
            'grant_date': _convert_date(record['hd']['grant_date']),
            'expiration_date': _convert_date(record['hd']['expired_date']),
            'entity_type': _convert_applicant_type_code(record['en']['applicant_type_code'])
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


def _query_license(callsign: str = None, frn: str = None, identifier: int = None) -> Optional[dict[str, any]]:
    sql = SqlConnection()

    with FccAdapter(sql) as fcc:
        if callsign:
            return fcc.get_callsign_data(callsign)
        elif frn:
            return fcc.get_callsign_data(frn)
        elif identifier:
            return fcc.get_unique_identifier_data(identifier)

    return None
