#!/usr/bin/env python3

from .fcc import FCC_CALLSIGN_REGEX, fcc_query_basic_data
from .ised import ISED_CALLSIGN_REGEX, ised_query_basic_data


def query_basic_data(callsign: str = None, frn: str = None, identifier: int = None):
    if callsign:
        if FCC_CALLSIGN_REGEX.match(callsign):
            return fcc_query_basic_data(callsign=callsign)

        if ISED_CALLSIGN_REGEX.match(callsign):
            return ised_query_basic_data(callsign=callsign)

        return None

    return fcc_query_basic_data(frn=frn, identifier=identifier)
