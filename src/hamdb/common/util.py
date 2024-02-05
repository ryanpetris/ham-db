#!/usr/bin/env python3

import json
import sys


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
