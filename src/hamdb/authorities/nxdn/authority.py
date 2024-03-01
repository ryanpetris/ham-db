#!/usr/bin/env python3

from .commands import run_import
from .sql_queries import cmd_license_insert
from ...common import Authority as BaseAuthority, DataConverter


class Authority(BaseAuthority):
    @property
    def name(self) -> str:
        return 'Radio ID NXDN ID Database'

    @property
    def code(self) -> str:
        return 'NXDN'

    @property
    def data_converter(self) -> type[DataConverter] | None:
        return None

    @property
    def sync_priority(self) -> int | None:
        return 10

    @property
    def sync_sql_command(self) -> str | None:
        return cmd_license_insert

    def run_import(self, args: list[str]) -> bool:
        return run_import(args)
