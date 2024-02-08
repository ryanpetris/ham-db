#!/usr/bin/env python3

from .commands import run_import
from .sql_queries import cmd_license_insert
from ...common import Authority as BaseAuthority, DataConverter
from typing import Optional


class Authority(BaseAuthority):
    @property
    def name(self) -> str:
        return 'Radio ID DMR ID Database'

    @property
    def code(self) -> str:
        return 'DMR'

    @property
    def data_converter(self) -> Optional[type[DataConverter]]:
        return None

    @property
    def sync_priority(self) -> Optional[int]:
        return 10

    @property
    def sync_sql_command(self) -> Optional[str]:
        return cmd_license_insert

    def run_import(self, args: list[str]) -> bool:
        return run_import(args)
