#!/usr/bin/env python3

import json
import sys
import time

from datetime import datetime, timezone
from typing import Optional


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def die(*args, **kwargs):
    eprint(*args, **kwargs)
    sys.exit(1)


def clean_null_fields(d):
    if isinstance(d, dict):
        return {k: clean_null_fields(v) for k, v in d.items() if v is not None}
    elif isinstance(d, list):
        return [clean_null_fields(v) for v in d]
    else:
        return d


def dump_json(data: any):
    return json.dumps(clean_null_fields(data), indent=4)


def datetime_to_iso_datetime(date: datetime) -> Optional[str]:
    if date is None:
        return None

    return date.isoformat()


def iso_datetime_to_datetime(date: str) -> Optional[datetime]:
    if date is None:
        return None

    return datetime.fromisoformat(date)


def last_modified_date_to_datetime(date: str) -> Optional[datetime]:
    if date is None:
        return None

    # Example Date: 'Sun, 04 Feb 2024 22:18:43 GMT'
    date_parts = time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')[0:6]
    return datetime(*date_parts, tzinfo=timezone.utc)
