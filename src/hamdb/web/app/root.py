#!/usr/bin/env python3

from flask import Blueprint

from ..common import BadRequestException, NotFoundException, BaseView, register_route
from ...common import safe_get
from ...db import query_statistics_latest
from ...licenses import query_basic_data

bp = Blueprint('root', __name__, template_folder='./template')


@register_route(bp, '/')
class RootView(BaseView):
    def get(self):
        if self.is_html_requested:
            return self.render_template('root.html')

        raise NotFoundException()


@register_route(bp, '/query')
class RootQueryView(BaseView):
    def get(self, callsign: str):
        if not callsign:
            raise BadRequestException('Callsign not specified')

        callsign = callsign.upper()
        data = query_basic_data(callsign)

        if not data:
            raise NotFoundException(f'Callsign {callsign!r} not found.')

        if self.is_html_requested:
            return self.render_template('query.html', license=self._convert_for_html(data))

        return data

    def _convert_for_html(self, data: dict[str, any]) -> dict[str, any]:
        result = {
            'callsign': safe_get(data, 'callsign'),
            'status': safe_get(data, 'status'),
            'license': safe_get(data, 'license', default={}),
            'name': self._get_name(data),
            'address': safe_get(data, 'address', default={}),
            'extra_data': safe_get(data, 'extra_data', default={}),
            'administrators': [self._convert_for_html(a) for a in safe_get(data, 'administrators', default=[])]
        }

        return result

    def _get_name(self, data: dict[str, any]) -> str:
        name = ('%s %s %s' % (
            safe_get(data, 'name', 'first', default=''),
            safe_get(data, 'name', 'middle', default=''),
            safe_get(data, 'name', 'last', default='')
        )).strip()

        if not name:
            name = safe_get(data, 'name', 'full', default='').strip()

        return name


@register_route(bp, '/statistics')
class RootStatisticsView(BaseView):
    def get(self):
        data = query_statistics_latest()

        if not data:
            raise NotFoundException()

        statistics = [data]

        if self.is_html_requested:
            for stat in statistics:
                for item in stat['data']:
                    if item['type'] == 'active_licenses_by_state' and item['state'] is None:
                        item['state'] = ''

            return self.render_template('statistics.html', statistics=statistics)

        return data
