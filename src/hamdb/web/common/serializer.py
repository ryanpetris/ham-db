#!/usr/bin/env python3

import json
import re
from typing import Callable, Pattern, Tuple, Union

import yaml
from dict2xml import Converter as XmlConverter
from flask import request
from flask.wrappers import Response

from .constants import CONTENT_TYPE_JSON, CONTENT_TYPE_YAML, CONTENT_TYPE_XML, DEFAULT_CHARSET
from .exceptions import WebException
from ...common import clean_null_fields

ACCEPT_HEADER_REGEX: Pattern = re.compile('(?P<type>[a-z/+]+)(;q=(?P<weight>[0-9.]+))?', re.RegexFlag.IGNORECASE)


def _get_accept_header_values() -> list[str]:
    accept_header = request.headers.get('accept', None)

    if accept_header is None:
        return []

    items: list[dict[str, str]] = []

    for header in accept_header.split(','):
        header = header.strip().lower()
        match = ACCEPT_HEADER_REGEX.fullmatch(header.strip())

        if not match:
            continue

        content_type = match.group('type')
        weight = 1

        try:
            str_weight = match.group('weight')

            if str_weight:
                weight = float(str_weight)
        except ValueError:
            continue

        items.append({
            'type': content_type,
            'weight': weight
        })

    items.sort(key=lambda i: (-i['weight'], i['type']))

    return [i['type'] for i in items]


class _Serializer:
    @classmethod
    def serialize(cls, data: Union[dict[any, any], list[any], any]) -> Tuple[str, str]:
        accept_headers = _get_accept_header_values()
        serializer = cls._find_serializer(accept_headers)
        result = clean_null_fields(data)

        return serializer(result)

    @classmethod
    def _find_serializer(cls, content_types: list[str]) -> Callable[[Union[dict[any, any], list[any], any]], tuple[str, str]]:
        for content_type in content_types:
            if content_type == CONTENT_TYPE_JSON:
                return cls._serialize_json

            if content_type == CONTENT_TYPE_YAML:
                return cls._serialize_yaml

            if content_type == CONTENT_TYPE_XML:
                return cls._serialize_xml

        return cls._serialize_json

    @staticmethod
    def _serialize_json(data: Union[dict[any, any], list[any], any]) -> tuple[str, str]:
        return json.dumps(data, sort_keys=True), f'{CONTENT_TYPE_JSON}; charset={DEFAULT_CHARSET}'

    @staticmethod
    def _serialize_yaml(data: Union[dict[any, any], list[any], any]) -> tuple[str, str]:
        return yaml.safe_dump(data, sort_keys=True), f'{CONTENT_TYPE_YAML}; charset={DEFAULT_CHARSET}'

    @staticmethod
    def _serialize_xml(data: Union[dict[any, any], list[any], any]) -> tuple[str, str]:
        converter = XmlConverter(indent=None, newlines=None)
        return converter.build({'result': data}), f'{CONTENT_TYPE_XML}; charset={DEFAULT_CHARSET}'


def serializer_wrapper(func: callable):
    def decorator(*args, **kwargs):
        status_code = 200

        try:
            data = func(*args, **kwargs)
        except WebException as ex:
            status_code = ex.status_code

            data = {
                'error': {
                    'code': ex.status_code,
                    'message': ex.message
                }
            }

        if data is None or isinstance(data, (str, bytes, Response)):
            return data

        result, content_type = _Serializer.serialize(data)

        return Response(response=result, content_type=content_type, status=status_code)

    return decorator
