#!/usr/bin/env python3

from .response import dynamic_response
from .util import query_license, get_basic_data
from flask import Flask, request


app = Flask(__name__)


@app.route('/query')
@dynamic_response(app)
def query():
    params = {
        'callsign': request.args.get('callsign', None),
        'frn': request.args.get('frn', None)
    }

    if 'identifier' in request.args:
        try:
            params['identifier'] = int(request.args['identifier'])
        except ValueError:
            pass

    data = query_license(**params)

    if not data:
        app.response_class(status=404)

    return get_basic_data(data)
