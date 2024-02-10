#!/usr/bin/env python3

import json
from typing import Callable, Tuple, Union

import yaml
from dict2xml import Converter as XmlConverter
from flask.wrappers import Response

from .constants import CONTENT_TYPE_JSON, CONTENT_TYPE_YAML, CONTENT_TYPE_XML, DEFAULT_CHARSET
from .exceptions import WebException
from .headers import get_header_preference
from ...common import clean_null_fields


class _Serializer:
    @classmethod
    def serialize(cls, data: Union[dict[any, any], list[any], any]) -> Tuple[str, str]:
        serializer = cls._find_serializer()
        result = clean_null_fields(data)

        return serializer(result)

    @classmethod
    def _find_serializer(cls) -> Callable[[Union[dict[any, any], list[any], any]], tuple[str, str]]:
        content_type = get_header_preference(CONTENT_TYPE_JSON, CONTENT_TYPE_YAML, CONTENT_TYPE_XML)

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
