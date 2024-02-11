#!/usr/bin/env python3

from datetime import date, timedelta

from .sql import SqlConnection
from ..common import get_authority


def query_statistics(start_date: date | str, end_date: date | str):
    sql = SqlConnection()

    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)

    if isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)

    results = list(sql.fetch(
        'SELECT date, data FROM statistics WHERE date >= %(start_date)s AND date < %(end_date)s',
        start_date=start_date,
        end_date=end_date + timedelta(days=1)
    ))

    for result in results:
        _convert_inplace(result['data'])

    return results


def query_statistics_latest():
    sql = SqlConnection()

    result = sql.fetch_one('SELECT date, data FROM statistics WHERE id = (SELECT MAX(i.id) FROM statistics i)')

    _convert_inplace(result['data'])

    return result


def _convert_inplace(data: list[dict[str, any]]):
    for item in data:
        if item['type'] == 'active_licenses_by_qualification':
            item['qualification'] = get_authority(item['authority']).data_converter.convert_qualification(
                item['qualification'])
