#!/usr/bin/env python3

from ...common import map_lower


def get_header_preference(*prefs: str) -> str | None:
    content_types = _get_accept_header_values()
    prefs_lower_map = map_lower(prefs)

    return next((prefs_lower_map.get(t) for t in content_types if t in prefs_lower_map), None)
