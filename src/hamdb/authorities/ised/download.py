#!/usr/bin/env python3

import http.client
import shutil
import tempfile
import urllib.request

from ...common import datetime_to_iso_datetime, iso_datetime_to_datetime, last_modified_date_to_datetime
from datetime import datetime
from typing import IO, Optional


LICENSE_FULL_URL: str = 'https://apc-cap.ic.gc.ca/datafiles/amateur_delim.zip'


class IsedLicenseFile:
    @property
    def last_modified(self):
        return self._last_modified

    @property
    def file(self):
        return self._file

    def __init__(self, last_modified: str, file: IO[bytes]):
        self._last_modified: str = last_modified
        self._file: IO[bytes] = file


def get_full_file(find_after: str) -> IsedLicenseFile:
    find_after_date = iso_datetime_to_datetime(find_after)
    return _get_auto_cleanup_file(LICENSE_FULL_URL, only_after=find_after_date)


def _get_auto_cleanup_file(url: str, only_after: datetime = None) -> Optional[IsedLicenseFile]:
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

        return IsedLicenseFile(datetime_to_iso_datetime(last_modified), file)

