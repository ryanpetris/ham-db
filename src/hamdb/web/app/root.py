#!/usr/bin/env python3

from ..common import BadRequestException, NotFoundException, Handler, app_route
from ...licenses import query_basic_data
from flask import Blueprint

bp = Blueprint('root', __name__)


@app_route(bp, '/query')
class QueryHandler(Handler):
    def do_get(self, callsign: str):
        if not callsign:
            raise BadRequestException('Callsign not specified')

        data = query_basic_data(callsign)

        if not data:
            raise NotFoundException(f'Callsign {callsign} not found.')

        return data
