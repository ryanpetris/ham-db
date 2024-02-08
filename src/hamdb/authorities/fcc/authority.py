#!/usr/bin/env python3

from .commands import fcc_import
from .converter import FccDataConverter
from .sql_queries import cmd_license_insert
from ...common import Authority as BaseAuthority, DataConverter


class Authority(BaseAuthority):
    @property
    def name(self) -> str:
        return 'Federal Communication Commission'

    @property
    def code(self) -> str:
        return 'FCC'

    @property
    def data_converter(self) -> type[DataConverter]:
        return FccDataConverter

    @property
    def sync_sql_command(self) -> str:
        return cmd_license_insert

    def run_import(self, args: list[str]) -> bool:
        return fcc_import(args)
