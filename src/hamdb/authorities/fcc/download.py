#!/usr/bin/env python3

import http.client
import shutil
import tempfile
import urllib.request

from ...common import datetime_to_iso_datetime, iso_datetime_to_datetime, last_modified_date_to_datetime
from datetime import datetime
from typing import IO, Iterable, Optional


AM_LICENSE_FULL_URL: str = 'https://data.fcc.gov/download/pub/uls/complete/l_amat.zip'

AM_LICENSE_DAILY_URLS: list[str] = [
    'https://data.fcc.gov/download/pub/uls/daily/l_am_sun.zip',
    'https://data.fcc.gov/download/pub/uls/daily/l_am_mon.zip',
    'https://data.fcc.gov/download/pub/uls/daily/l_am_tue.zip',
    'https://data.fcc.gov/download/pub/uls/daily/l_am_wed.zip',
    'https://data.fcc.gov/download/pub/uls/daily/l_am_thu.zip',
    'https://data.fcc.gov/download/pub/uls/daily/l_am_fri.zip',
    'https://data.fcc.gov/download/pub/uls/daily/l_am_sat.zip'
]


class FccLicenseFile:
    @property
    def last_modified(self):
        return self._last_modified

    @property
    def file(self):
        return self._file

    def __init__(self, last_modified: str, file: IO[bytes]):
        self._last_modified: str = last_modified
        self._file: IO[bytes] = file


def get_daily_files(find_after: str) -> Iterable[FccLicenseFile]:
    files: list[FccLicenseFile] = []
    find_after_date = iso_datetime_to_datetime(find_after)

    for url in AM_LICENSE_DAILY_URLS:
        file = _get_auto_cleanup_file(url, find_after_date)

        if not file:
            continue

        files.append(file)

    for file in sorted(files, key=lambda i: i.last_modified):
        yield file


def get_full_file() -> FccLicenseFile:
    return _get_auto_cleanup_file(AM_LICENSE_FULL_URL)


def _get_auto_cleanup_file(url: str, only_after: datetime = None) -> Optional[FccLicenseFile]:
    request = urllib.request.Request(url)

    with urllib.request.urlopen(request) as response:
        response: http.client.HTTPResponse

        last_modified = last_modified_date_to_datetime(response.headers.get('last-modified', None))

        if not last_modified:
            return None

        if only_after and last_modified <= only_after:
            return None

        file = tempfile.NamedTemporaryFile()

        # noinspection PyTypeChecker
        shutil.copyfileobj(response, file)
        file.flush()

        return FccLicenseFile(datetime_to_iso_datetime(last_modified), file)
