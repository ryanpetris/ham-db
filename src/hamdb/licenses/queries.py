#!/usr/bin/env python3

import sys

from .adapter import LicensesAdapter
from ..common import DataConverter, clean_null_fields
from ..db import SqlConnection


def query_basic_data(callsign: str = None):
    if not callsign:
        return None

    with LicensesAdapter(SqlConnection()) as licenses:
        data = licenses.query_callsign(callsign)

    return _db_to_basic_data(data)


def _db_to_basic_data(data: dict[str, any]) -> dict[str, any]:
    converter = DataConverter.get_converter_for_authority(data['authority'])

    result = {
        'callsign': data.get('callsign', None),
        'status': converter.convert_status(data.get('status', None)),
        'license': {
            'authority': data.get('authority', None),
            'qualifications': [converter.convert_qualification(q) for q in data.get('qualifications', None) or []],
            'grant_date': converter.convert_date(data.get('grant_date', None)),
            'expiration_date': converter.convert_date(data.get('expiration_date', None)),
            'entity_type': converter.convert_entity_type(data.get('entity_type', None))
        },
        'name': {
            'full': data.get('name_full', None),
            'first': data.get('name_first', None),
            'middle': data.get('name_middle', None),
            'last': data.get('name_last', None)
        },
        'address': {
            'line1': data.get('address_line1', None),
            'line2': data.get('address_line2', None),
            'city': data.get('address_city', None),
            'state': data.get('address_state', None),
            'zip': data.get('address_zip', None)
        },
        'extra_data': {k: v for k, v in (data.get('extra_data', None) or {}).items() if not k.startswith('_')},
        'administrators': [_db_to_basic_data(a) for a in data.get('administrators', None) or []]
    }

    if not result.get('administrators', None) and (data.get('extra_data', None) or {}).get('_administrators'):
        result['administrators'] = [_db_to_basic_data(a) for a in (data.get('extra_data', None) or {}).get('_administrators') or []]

    return result
