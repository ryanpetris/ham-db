#!/usr/bin/env python3

import json
import re
import yaml

from .exceptions import WebException
from ..common import clean_null_fields
from dict2xml import Converter as XmlConverter
from flask import Flask, request, Response
from typing import Callable, Optional, Pattern


ACCEPT_HEADER_REGEX: Pattern = re.compile('(?P<type>[a-z/+]+)(;q=(?P<weight>[0-9.]+))?', re.RegexFlag.IGNORECASE)

CONTENT_TYPE_JSON: str = 'application/json'
CONTENT_TYPE_YAML: str = 'application/yaml'
CONTENT_TYPE_XML: str = 'application/xml'
CONTENT_TYPE_HTML: str = 'text/html'

SUPPORTED_CONTENT_TYPES = [
    CONTENT_TYPE_JSON,
    CONTENT_TYPE_YAML,
    CONTENT_TYPE_XML,
    CONTENT_TYPE_HTML
]


def dynamic_response(app: Flask):
    func: Optional[Callable] = None

    def wrapper(f):
        nonlocal func
        func = f

        return process

    def process(*args):
        response = Response()
        data = None

        try:
            data = func(*args)
        except WebException as ex:
            response.status = ex.status_code
            data = {
                'error': ex.message or 'error'
            }

        content_type = _get_accept_preference()

        if content_type == CONTENT_TYPE_JSON:
            return _respond_json(response, data)
        elif content_type == CONTENT_TYPE_YAML:
            return _respond_yaml(response, data)
        elif content_type == CONTENT_TYPE_XML:
            return _respond_xml(response, data)
        elif content_type == CONTENT_TYPE_HTML:
            return _respond_html(response, data)

    return wrapper


def _get_accept_preference():
    found_content_type = None
    found_content_type_weight = 0

    for header in request.headers.get('accept', '').split(','):
        header = header.strip().lower()
        match = ACCEPT_HEADER_REGEX.fullmatch(header.strip())

        if not match:
            continue

        content_type = match.group('type')

        if content_type not in SUPPORTED_CONTENT_TYPES:
            continue

        weight = 1

        try:
            str_weight = match.group('weight')

            if str_weight:
                weight = float(str_weight)
        except ValueError:
            continue

        if weight > found_content_type_weight:
            found_content_type = content_type
            found_content_type_weight = weight

    return found_content_type or SUPPORTED_CONTENT_TYPES[0]


def _respond_json(response: Response, data: dict[str, any]):
    response.data = json.dumps(clean_null_fields(data), sort_keys=True)
    response.content_type = f'{CONTENT_TYPE_JSON}; charset=utf-8'
    return response


def _respond_yaml(response: Response, data: dict[str, any]):
    response.data = yaml.safe_dump(clean_null_fields(data), sort_keys=True)
    response.content_type = f'{CONTENT_TYPE_YAML}; charset=utf-8'
    return response


def _respond_xml(response: Response, data: dict[str, any]):
    converter = XmlConverter(indent=None, newlines=None)
    response.data = converter.build(clean_null_fields(data))
    response.content_type = f'{CONTENT_TYPE_XML}; charset=utf-8'
    return response


def _respond_html(response: Response, data: dict[str, any]):
    return _respond_json(response, data)
