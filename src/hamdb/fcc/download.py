#!/usr/bin/env python3

import http.client
import shutil
import tempfile
import time
import urllib.request

from datetime import datetime, timezone
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
    find_after_date = _parse_db_time(find_after)

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

        last_modified = _parse_last_modified_date(response.headers.get('last-modified', None))

        if not last_modified:
            return None

        if only_after and last_modified <= only_after:
            return None

        file = tempfile.NamedTemporaryFile()

        # noinspection PyTypeChecker
        shutil.copyfileobj(response, file)
        file.flush()

        return FccLicenseFile(_to_db_time(last_modified), file)


def _get_download_path_for_date(date: datetime):
    result = date.strftime('%Y%m%d%H%M%S')
    return f'{result}.zip'


def _parse_db_time(date: str) -> Optional[datetime]:
    if date is None:
        return None

    return datetime.fromisoformat(date)


def _parse_last_modified_date(date: str) -> Optional[datetime]:
    if date is None:
        return None

    # Example Date: 'Sun, 04 Feb 2024 22:18:43 GMT'
    date_parts = time.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')[0:6]
    return datetime(*date_parts, tzinfo=timezone.utc)


def _to_db_time(date: datetime) -> Optional[str]:
    if date is None:
        return None

    return date.isoformat()
