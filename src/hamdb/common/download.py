#!/usr/bin/env python3

import http.client
import shutil
import tempfile
import urllib.request

from .util import datetime_to_iso_datetime, iso_datetime_to_datetime, last_modified_date_to_datetime
from datetime import datetime
from typing import IO, Optional, Union


class DownloadFile:
    @property
    def last_modified(self) -> str:
        return self._last_modified

    @property
    def file(self) -> IO[bytes]:
        return self._file

    def __init__(self, last_modified: str, file: IO[bytes]):
        self._last_modified: str = last_modified
        self._file: IO[bytes] = file


def download_file(url: str, only_after: Union[datetime, str, None] = None) -> Optional[DownloadFile]:
    if only_after and isinstance(only_after, str):
        only_after = iso_datetime_to_datetime(only_after)

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
        file.seek(0)

        return DownloadFile(datetime_to_iso_datetime(last_modified), file)
