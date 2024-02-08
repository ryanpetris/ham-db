#!/usr/bin/env python3

from .commands import ised_import
from .converter import IsedDataConverter
from .sql_queries import cmd_license_insert
from ...common import Authority as BaseAuthority, DataConverter


class Authority(BaseAuthority):
    @property
    def name(self) -> str:
        return 'Innovation Science and Economic Development Canada'

    @property
    def code(self) -> str:
        return 'ISED'

    @property
    def data_converter(self) -> type[DataConverter]:
        return IsedDataConverter

    @property
    def sync_sql_command(self) -> str:
        return cmd_license_insert

    def run_import(self, args: list[str]):
        return ised_import(args)
