#!/usr/bin/env python3

from .commands import run_import
from .converter import IsedDataConverter
from .sql_queries import cmd_license_insert
from ...common import Authority as BaseAuthority, DataConverter
from typing import Optional


class Authority(BaseAuthority):
    @property
    def name(self) -> str:
        return 'Innovation Science and Economic Development Canada'

    @property
    def code(self) -> str:
        return 'ISED'

    @property
    def data_converter(self) -> Optional[type[DataConverter]]:
        return IsedDataConverter

    @property
    def sync_sql_command(self) -> Optional[str]:
        return cmd_license_insert

    def run_import(self, args: list[str]):
        return run_import(args)
