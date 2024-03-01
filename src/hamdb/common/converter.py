#!/usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import date


class DataConverter(ABC):
    @classmethod
    def convert_date(cls, value: date | None):
        if not value:
            return None

        if isinstance(value, date):
            return value.strftime('%Y-%m-%d')

        return value

    @classmethod
    def convert_entity_type(cls, value: str | None) -> str | None:
        if not value:
            return None

        value = value.upper()

        if value == 'C':
            return 'CLUB'

        if value == 'G':
            return 'GOVERNMENT'

        if value == 'I':
            return 'INDIVIDUAL'

        if value == 'M':
            return 'MILITARY'

        if value == 'R':
            return 'RACES'

        return None

    @classmethod
    @abstractmethod
    def convert_qualification(cls, value: str | None) -> str | None:
        raise Exception('abstract method')

    @classmethod
    def convert_status(cls, value: str | None) -> str | None:
        if not value:
            return None

        value = value.upper()

        if value == 'A':
            return 'ACTIVE'

        if value == 'N':
            return 'NOT_ACTIVE'

        if value == 'P':
            return 'ACTION_PENDING'

        return None
