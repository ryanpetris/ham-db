#!/usr/bin/env python3


from abc import ABC, abstractmethod
from typing import Optional


class WebException(Exception, ABC):
    @property
    @abstractmethod
    def status_code(self) -> int:
        pass

    @property
    def message(self) -> Optional[str]:
        return self._message

    def __init__(self, message: Optional[str] = None):
        super().__init__()
        self._message: Optional[str] = message


class BadRequestException(WebException):
    @property
    def status_code(self) -> int:
        return 400

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Bad Request')


class NotFoundException(WebException):
    @property
    def status_code(self) -> int:
        return 404

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or 'Not Found')
