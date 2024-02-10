#!/usr/bin/env python3

import importlib
import os
from abc import ABC, abstractmethod
from typing import Optional

from .converter import DataConverter

authority_cache: dict[str, 'Authority'] = {}


class Authority(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def code(self) -> str:
        pass

    @property
    @abstractmethod
    def data_converter(self) -> Optional[type[DataConverter]]:
        pass

    @property
    def sync_priority(self) -> Optional[int]:
        return 0

    @property
    @abstractmethod
    def sync_sql_command(self) -> Optional[str]:
        pass

    @abstractmethod
    def run_import(self, args: list[str]):
        pass


def _ensure_authority_cache():
    if authority_cache:
        return

    module = importlib.import_module("..authorities", package=__package__)
    module_path = module.__path__[0]

    for module_name in os.listdir(module_path):
        if not os.path.isdir(os.path.join(module_path, module_name)):
            continue

        # noinspection PyBroadException
        try:
            module = importlib.import_module(f"..authorities.{module_name}", package=__package__)
            authority = module.Authority()

            authority_cache[authority.code.upper()] = authority
        except Exception:
            pass


def get_known_authority_codes() -> list[str]:
    _ensure_authority_cache()

    return [*authority_cache.keys()]


def get_authority(code: str) -> 'Authority':
    _ensure_authority_cache()

    code = code.upper()

    if code not in authority_cache:
        raise Exception(f'Invalid authority code: {code!r}')

    return authority_cache[code]
