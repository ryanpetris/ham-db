#!/usr/bin/env python3

from abc import ABC, abstractmethod
from datetime import date
from typing import Optional


class DataConverter(ABC):
    @classmethod
    def convert_date(cls, value: Optional[date]):
        if not value:
            return None

        return value.strftime('%Y-%m-%d')

    @classmethod
    def convert_entity_type(cls, value: Optional[str]) -> Optional[str]:
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
    def convert_qualification(cls, value: Optional[str]) -> Optional[str]:
        raise Exception('abstract method')

    @classmethod
    def convert_status(cls, value: Optional[str]) -> Optional[str]:
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

    @staticmethod
    def get_converter_for_authority(authority: str) -> type['DataConverter']:
        authority = authority.upper()

        if authority == 'FCC':
            from ..authorities.fcc import FccDataConverter

            return FccDataConverter

        if authority == 'ISED':
            from ..authorities.ised import IsedDataConverter

            return IsedDataConverter

        raise Exception(f'Data converter for authority {authority} not found.')
