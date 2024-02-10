#!/usr/bin/env python3

from ...common import DownloadFile, download_file

LICENSE_FULL_URL: str = 'https://apc-cap.ic.gc.ca/datafiles/amateur_delim.zip'


def get_full_file(find_after: str) -> DownloadFile:
    return download_file(LICENSE_FULL_URL, only_after=find_after)
