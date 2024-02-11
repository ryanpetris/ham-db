#!/usr/bin/env python3

import json
from typing import Union

import yaml
from dict2xml import Converter as XmlConverter
from flask.wrappers import Response

from .constants import DEFAULT_CHARSET
from .contenttype import ContentType
from .exceptions import WebException
from .template import render_template
from ...common import clean_null_fields


def _serialize_json(data: Union[dict[any, any], list[any], any]) -> str:
    return json.dumps(data, sort_keys=True, default=str)


def _serialize_yaml(data: Union[dict[any, any], list[any], any]) -> str:
    return yaml.safe_dump(data, sort_keys=True)


def _serialize_xml(data: Union[dict[any, any], list[any], any]) -> str:
    converter = XmlConverter(indent=None, newlines=None)
    return converter.build({'result': data})


def serializer_wrapper(func: callable):
    def decorator(*args, **kwargs):
        status_code = 200
        content_type = ContentType.get_header_preference() or ContentType.JSON

        try:
            response = func(*args, **kwargs)
        except WebException as ex:
            status_code = ex.status_code
            response = {
                'error': {
                    'code': ex.status_code,
                    'message': ex.message
                }
            }

            if content_type == ContentType.HTML:
                response = render_template('error.html', error=response['error'])

        if response is not None and not isinstance(response, (str, bytes, Response)):
            response = clean_null_fields(response)

            if content_type == ContentType.JSON:
                response = _serialize_json(response)
            elif content_type == ContentType.YAML:
                response = _serialize_yaml(response)
            elif content_type == ContentType.XML:
                response = _serialize_xml(response)

        return Response(response=response, content_type=f'{content_type.get_type_header()}; charset={DEFAULT_CHARSET}',
                        status=status_code)

    return decorator
