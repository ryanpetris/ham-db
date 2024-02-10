#!/usr/bin/env python3

from flask import Blueprint

from ..common import BadRequestException, NotFoundException, BaseView, register_route
from ...licenses import query_basic_data

bp = Blueprint('root', __name__)


@register_route(bp, '/query')
class QueryView(BaseView):
    def get(self, callsign: str):
        if not callsign:
            raise BadRequestException('Callsign not specified')

        data = query_basic_data(callsign)

        if not data:
            raise NotFoundException(f'Callsign {callsign!r} not found.')

        return data
