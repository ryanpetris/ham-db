#!/usr/bin/env python3

import inspect

from .constants import CONTENT_TYPE_JSON, CONTENT_TYPE_YAML, CONTENT_TYPE_XML
from .exceptions import BadRequestException, NotFoundException, WebException
from .header import get_accept_header_values
from .serializer import serialize_json, serialize_yaml, serialize_xml
from ...common import clean_null_fields
from flask import request
from flask.wrappers import Response
from typing import Callable, Iterable, Optional, Tuple

DEFAULT_CONTENT_TYPE = '_default'

RESPONSE_TYPE_MAP: dict[str, Callable[[dict[str, any]], str]] = {
    CONTENT_TYPE_JSON: serialize_json,
    CONTENT_TYPE_YAML: serialize_yaml,
    CONTENT_TYPE_XML: serialize_xml,
    DEFAULT_CONTENT_TYPE: serialize_json
}


class Handler:
    request_func_prefix = 'do_'

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance(*args, **kwargs)

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        status_code = 200

        try:
            result = self.execute()
        except WebException as ex:
            result = {
                'error': {
                    'code': ex.status_code,
                    'message': ex.message
                }
            }

        if result is None or isinstance(result, (str, bytes, Response)):
            return result

        result = clean_null_fields(result)
        accept_items = get_accept_header_values(request.headers.get('accept', None)) or []
        serialize_func = next((RESPONSE_TYPE_MAP[i] for i in accept_items if i in RESPONSE_TYPE_MAP), None) or RESPONSE_TYPE_MAP[DEFAULT_CONTENT_TYPE]

        result, content_type = serialize_func(result)

        return Response(response=result, content_type=content_type, status=status_code)

    def execute(self):
        method_func = self._get_func_for_method(request.method)

        if method_func is None:
            raise NotFoundException()

        args, missing = self._extract_arguments_for_method(method_func)

        if missing:
            raise BadRequestException(f'Missing required arguments: {", ".join(missing)}')

        return method_func(**args)

    def _extract_arguments_for_method(self, func: Callable) -> Tuple[dict[str, str], list[str]]:
        signature: inspect.Signature = inspect.signature(func)
        param_lower_map = {p.lower(): p for p in signature.parameters.keys()}
        filtered_args = {param_lower_map.get(k.lower()): v for k, v in request.args.items() if k.lower() in param_lower_map.keys()}
        missing_params = [k.lower() for k, v in signature.parameters.items() if k not in filtered_args and not v.default != inspect.Parameter.empty]

        return filtered_args, missing_params

    def _gen_func_names_for_method(self, method: str) -> Iterable[str]:
        yield '%s%s' % (self.request_func_prefix, method.lower())
        yield '%s%s' % (self.request_func_prefix, 'any')

    def _get_func_for_method(self, method: str) -> Optional[Callable]:
        for func_name in self._gen_func_names_for_method(method):
            if not hasattr(self, func_name):
                continue

            func = getattr(self, func_name)

            if not isinstance(func, Callable):
                continue

            return func

        return None
