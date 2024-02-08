#!/usr/bin/env python3

from ...common import DownloadFile, download_file
from typing import Iterable


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


def get_daily_files(find_after: str) -> Iterable[DownloadFile]:
    files: list[DownloadFile] = []

    for url in AM_LICENSE_DAILY_URLS:
        file = download_file(url, find_after)

        if not file:
            continue

        files.append(file)

    for file in sorted(files, key=lambda i: i.last_modified):
        yield file


def get_full_file() -> DownloadFile:
    return download_file(AM_LICENSE_FULL_URL)
