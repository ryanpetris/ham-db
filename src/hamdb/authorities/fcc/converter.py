#!/usr/bin/env python3

from ...common import DataConverter


class FccDataConverter(DataConverter):
    @classmethod
    def convert_qualification(cls, value: str | None) -> str | None:
        if not value:
            return None

        value = value.upper()

        if value == 'E':
            return 'FCC:AMATEUR_EXTRA'

        if value == 'A':
            return 'FCC:ADVANCED'

        if value == 'G':
            return 'FCC:GENERAL'

        if value == 'P':
            return 'FCC:TECHNICIAN_PLUS'

        if value == 'T':
            return 'FCC:TECHNICIAN'

        if value == 'N':
            return 'FCC:NOVICE'

        return None
