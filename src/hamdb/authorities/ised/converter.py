#!/usr/bin/env python3

from typing import Optional

from ...common import DataConverter


class IsedDataConverter(DataConverter):
    @classmethod
    def convert_qualification(cls, value: Optional[str]) -> Optional[str]:
        if not value:
            return None

        value = value.upper()

        if value == 'A':
            return 'ISED:BASIC'

        if value == 'B':
            return 'ISED:5WPM'

        if value == 'C':
            return 'ISED:12WPM'

        if value == 'D':
            return 'ISED:ADVANCED'

        if value == 'E':
            return 'ISED:BASIC_HONOURS'

        return None
