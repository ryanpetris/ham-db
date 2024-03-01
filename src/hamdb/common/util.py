#!/usr/bin/env python3

import json
import sys
import time

from datetime import datetime, timezone
from typing import Iterable


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def die(*args, **kwargs):
    eprint(*args, **kwargs)
    sys.exit(1)


def clean_null_fields(value):
    if isinstance(value, dict):
        result = {k: clean_null_fields(v) for k, v in value.items() if v is not None}
        result = {k: v for k, v in result.items() if v is not None}

        if len(result) == 0:
            return None

        return result

    elif isinstance(value, list):
        if len(value) == 0:
            return None

        return [clean_null_fields(v) for v in value]

    else:
        return value


def dump_json(data: any):
    return json.dumps(clean_null_fields(data), indent=4, default=str)


def datetime_to_iso_datetime(date: datetime) -> str | None:
    if date is None:
        return None

    return date.isoformat()


def iso_datetime_to_datetime(date: str) -> datetime | None:
    if date is None:
        return None

    return datetime.fromisoformat(date)


def last_modified_date_to_datetime(date: str) -> datetime | None:
    if date is None:
        return None

    # Example Date: 'Sun, 04 Feb 2024 22:18:43 GMT'
    date_parts = time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')[0:6]
    return datetime(*date_parts, tzinfo=timezone.utc)


def map_lower(items: Iterable[str]) -> dict[str, str]:
    return {p.lower(): p for p in items}


def keys_lower(items: dict[str, any]) -> dict[str, any]:
    return {k.lower(): v for k, v in items.items()}


def safe_get(data: dict[str, any], *keys: any, default: any = None) -> any:
    for key in keys:
        if data is None:
            return default

        if not isinstance(data, dict):
            return default

        data = data.get(key, None)

    if data is None:
        return default

    return data
