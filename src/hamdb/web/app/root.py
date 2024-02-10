#!/usr/bin/env python3

from flask import Blueprint

from ..common import BadRequestException, NotFoundException, BaseView, register_route
from ...licenses import query_basic_data

bp = Blueprint('root', __name__, template_folder='./template')


@register_route(bp, '/')
class RootView(BaseView):
    def get(self):
        if not self.is_html_requested:
            raise NotFoundException()

        return 'Hello World'


@register_route(bp, '/query')
class QueryView(BaseView):
    def get(self, callsign: str):
        if not callsign:
            raise BadRequestException('Callsign not specified')

        data = query_basic_data(callsign)

        if not data:
            raise NotFoundException(f'Callsign {callsign!r} not found.')

        if self.is_html_requested:
            return self.render_template('callsign_basic_data.html', license=data)

        return data
