#!/usr/bin/env python3


from typing import Optional


class WebException(Exception):
    @property
    def status_code(self) -> int:
        return self._code

    @property
    def message(self) -> str:
        return self._message

    def __init__(self, code: int, message: str):
        super().__init__()
        self._code = code
        self._message: str = message


class BadRequestException(WebException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(400, message or 'Bad Request')


class NotFoundException(WebException):
    def __init__(self, message: Optional[str] = None):
        super().__init__(404, message or 'Not Found')
