#!/usr/bin/env python3

from .response import dynamic_response
from ..licenses import query_basic_data
from flask import Flask, request


app = Flask(__name__)


@app.route('/query')
@dynamic_response(app)
def query():
    callsign = request.args.get('callsign', None)
    return query_basic_data(callsign)
