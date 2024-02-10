#!/usr/bin/env python3

import re

from typing import Optional, Pattern


ACCEPT_HEADER_REGEX: Pattern = re.compile('(?P<type>[a-z/+]+)(;q=(?P<weight>[0-9.]+))?', re.RegexFlag.IGNORECASE)


def get_accept_header_values(accept_header: str) -> Optional[list[str]]:
    if accept_header is None:
        return None

    items: list[dict[str, str]] = []

    for header in accept_header.split(','):
        header = header.strip().lower()
        match = ACCEPT_HEADER_REGEX.fullmatch(header.strip())

        if not match:
            continue

        content_type = match.group('type')
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
