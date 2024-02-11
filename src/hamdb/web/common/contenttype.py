#!/usr/bin/env python3

import re
from enum import Enum
from typing import Optional, Pattern

from flask import request

CONTENT_TYPE_JSON: str = 'application/json'
CONTENT_TYPE_YAML: str = 'application/yaml'
CONTENT_TYPE_XML: str = 'application/xml'
CONTENT_TYPE_HTML: str = 'text/html'

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


class ContentType(Enum):
    JSON = 1
    YAML = 2
    XML = 3
    HTML = 4

    def get_type_header(self) -> str:
        if self == ContentType.JSON:
            return CONTENT_TYPE_JSON

        if self == ContentType.YAML:
            return CONTENT_TYPE_YAML

        if self == ContentType.XML:
            return CONTENT_TYPE_XML

        if self == ContentType.HTML:
            return CONTENT_TYPE_HTML

    @classmethod
    def get_by_type_header(cls, content_type: str) -> Optional['ContentType']:
        if not content_type:
            return None

        content_type = content_type.lower()

        if content_type == CONTENT_TYPE_JSON:
            return ContentType.JSON

        if content_type == CONTENT_TYPE_YAML:
            return ContentType.YAML

        if content_type == CONTENT_TYPE_XML:
            return ContentType.XML

        if content_type == CONTENT_TYPE_HTML:
            return ContentType.HTML

    @classmethod
    def get_header_preference(cls) -> Optional['ContentType']:
        available_content_types = {t.get_type_header(): t for t in list(cls)}
        request_content_types = _get_accept_header_values()

        return next((available_content_types.get(t) for t in request_content_types if t in available_content_types),
                    None)
