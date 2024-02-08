#!/usr/bin/env python3

from .exceptions import BadRequestException, NotFoundException
from .response import dynamic_response
from ..licenses import query_basic_data
from flask import Flask, request


app = Flask(__name__)


@app.route('/query')
@dynamic_response(app)
def query():
    callsign = request.args.get('callsign', None)

    if not callsign:
        raise BadRequestException('Callsign not specified')

    data = query_basic_data(callsign)

    if not data:
        raise NotFoundException(f'Callsign {callsign} not found.')

    return data
