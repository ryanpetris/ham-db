#!/usr/bin/env python3

import re

from .adapter import IsedAdapter
from ...db import SqlConnection
from typing import Optional, Pattern


ISED_CALLSIGN_REGEX: Pattern[str] = re.compile('^(C[F-KY-Z]|V[A-GX-Y]|X[J-O])', re.RegexFlag.IGNORECASE)


def ised_query_basic_data(callsign: str = None) -> Optional[dict[str, any]]:
    data = _query_license(callsign)

    if not data:
        return None

    response = _get_basic_data(data)

    if response['license']['entity_type'] == 'CLUB':
        trustee_data = _query_trustee_license(data)

        if trustee_data:
            response["administrators"] = [_get_basic_data(trustee_data)]
        else:
            response["administrators"] = [_get_basic_trustee_data(data)]

    return response


def _convert_qualifications(data):
    qual_a = (data.get('qual_a', '') or '').upper()
    qual_b = (data.get('qual_b', '') or '').upper()
    qual_c = (data.get('qual_c', '') or '').upper()
    qual_d = (data.get('qual_d', '') or '').upper()
    qual_e = (data.get('qual_e', '') or '').upper()

    result = []

    if qual_a == 'A':
        result.append('ISED:BASIC')

    if qual_b == 'B':
        result.append('ISED:5WPM')

    if qual_c == 'C':
        result.append('ISED:12WPM')

    if qual_d == 'D':
        result.append('ISED:ADVANCED')

    if qual_e == 'E':
        result.append('ISED:BASIC_HONOURS')

    return result


def _convert_entity_type(data):
    if data.get('club_name', None):
        return 'CLUB'

    return 'INDIVIDUAL'


def _get_basic_data(data: dict[str, any]) -> dict[str, any]:
    result: dict[str, any] = {
        'callsign': data['callsign'],
        'status': 'ACTIVE',
        'license': {
            'authority': 'ISED',
            'entity_type': _convert_entity_type(data)
        }
    }

    if result['license']['entity_type'] == 'CLUB':
        result['name'] = {
            'full': data['club_name']
        }

        result['address'] = {
            'line1': data['club_address'],
            'city': data['club_city'],
            'state': data['club_prov_cd'],
            'zip': data['club_postal_code']
        }

        if data['club_name_2']:
            result['authority_data'] = {
                'club_name_2': data['club_name_2']
            }
    else:
        result['license']['qualifications'] = _convert_qualifications(data)

        result['name'] = {
            'full': f'{data["surname"]}, {data["first_name"]}',
            'first': data["first_name"],
            'last': data["surname"]
        }

        result['address'] = {
            'line1': data['address_line'],
            'city': data['city'],
            'state': data['prov_cd'],
            'zip': data['postal_code']
        }

    return result


def _get_basic_trustee_data(data: dict[str, any]) -> dict[str, any]:
    result: dict[str, any] = {
        'license': {
            'authority': 'ISED',
            'qualifications': _convert_qualifications(data),
            'entity_type': 'INDIVIDUAL'
        },
        'name': {
            'full': f'{data["surname"]}, {data["first_name"]}',
            'first': data["first_name"],
            'last': data["surname"]
        },
        'address': {
            'line1': data['address_line'],
            'city': data['city'],
            'state': data['prov_cd'],
            'zip': data['postal_code']
        }
    }

    return result


def _query_license(callsign: str = None) -> Optional[dict[str, any]]:
    sql = SqlConnection()

    with IsedAdapter(sql) as ised:
        if callsign:
            return ised.get_callsign_data(callsign)

    return None


def _query_trustee_license(data: dict[str, any]) -> Optional[dict[str, any]]:
    sql = SqlConnection()

    with IsedAdapter(sql) as ised:
        return ised.find_individual(data['first_name'], data['surname'], data['postal_code'])
