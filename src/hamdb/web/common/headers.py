#!/usr/bin/env python3

import re
from typing import Pattern, Optional

from flask import request

from ...common import map_lower

ACCEPT_HEADER_REGEX: Pattern = re.compile('(?P<type>[a-z/+]+)(;q=(?P<weight>[0-9.]+))?', re.RegexFlag.IGNORECASE)


def _get_accept_header_values() -> list[str]:
    accept_header = request.headers.get('accept', None)

    if accept_header is None:
        return []

    items: list[dict[str, any]] = []

    for header in accept_header.split(','):
        header = header.strip().lower()
        match = ACCEPT_HEADER_REGEX.fullmatch(header.strip())

        if not match:
            continue

        content_type = match.group('type').lower()
        weight = 1

        try:
            str_weight = match.group('weight')

            if str_weight:
                weight = float(str_weight)
        except ValueError:
            continue

        items.append({
            'type': content_type,
            'weight': weight
        })

    items.sort(key=lambda i: (-i['weight'], i['type']))

    return [i['type'] for i in items]


def get_header_preference(*prefs: str) -> Optional[str]:
    content_types = _get_accept_header_values()
    prefs_lower_map = map_lower(prefs)

    return next((prefs_lower_map.get(t) for t in content_types if t in prefs_lower_map), None)
