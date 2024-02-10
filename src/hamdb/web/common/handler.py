#!/usr/bin/env python3

import inspect

from .constants import CONTENT_TYPE_JSON, CONTENT_TYPE_YAML, CONTENT_TYPE_XML, ALL_HTTP_METHODS
from .exceptions import BadRequestException, NotFoundException, WebException
from .header import get_accept_header_values
from .serializer import serialize_json, serialize_yaml, serialize_xml
from ...common import clean_null_fields
from enum import Enum
from flask import request
from flask.sansio.scaffold import Scaffold
from flask.wrappers import Response
from typing import Callable, Iterable, Optional, Tuple, Union

DEFAULT_CONTENT_TYPE = '_default'

RESPONSE_TYPE_MAP: dict[str, Callable[[Union[dict[any, any], list[any], any]], Tuple[str, str]]] = {
    CONTENT_TYPE_JSON: serialize_json,
    CONTENT_TYPE_YAML: serialize_yaml,
    CONTENT_TYPE_XML: serialize_xml,
    DEFAULT_CONTENT_TYPE: serialize_json
}


class HandlerArgumentSource(Enum):
    REQUEST = 1
    DIRECT = 2


class Handler:
    request_func_prefix = 'do_'
    any_method_func = f'{request_func_prefix}any'

    def __init__(self, arg_source: HandlerArgumentSource = None):
        self._arg_source: HandlerArgumentSource = arg_source or HandlerArgumentSource.REQUEST

    def __call__(self, *args, **kwargs):
        status_code = 200

        try:
            result = self.execute(*args, **kwargs)
        except WebException as ex:
            result = {
                'error': {
                    'code': ex.status_code,
                    'message': ex.message
                }
            }

        if result is None or isinstance(result, (str, bytes, Response)):
            return result

        result, content_type = self._serialize_data(result)

        return Response(response=result, content_type=content_type, status=status_code)

    def execute(self, *args, **kwargs):
        method_func = self._get_func_for_method(request.method)

        if method_func is None:
            raise NotFoundException()

        if self._arg_source == HandlerArgumentSource.REQUEST:
            method_args, missing = self._extract_arguments_for_method(method_func)

            if missing:
                raise BadRequestException(f'Missing required arguments: {", ".join(missing)}')

            return method_func(**method_args)
        elif self._arg_source == HandlerArgumentSource.DIRECT:
            return method_func(*args, **kwargs)
        else:
            raise Exception(f'Invalid arg_source value: {self._arg_source}')

    @classmethod
    def register(cls, func: callable, *args, **kwargs):
        func(*args, **kwargs)(cls().__call__)

    @classmethod
    def register_route(cls, app: Scaffold, *args, **kwargs):
        if 'methods' not in kwargs:
            do_methods = [k for k, v in inspect.getmembers(cls) if k.startswith(cls.request_func_prefix) and isinstance(v, Callable)]

            if cls.any_method_func in do_methods:
                methods = list(ALL_HTTP_METHODS)
            else:
                temp_methods = [m.removeprefix(cls.request_func_prefix).upper() for m in do_methods]
                methods = [m for m in temp_methods if m in ALL_HTTP_METHODS]

            kwargs['methods'] = methods

        cls.register(app.route, *args, **kwargs)

    # noinspection PyMethodMayBeStatic
    def _extract_arguments_for_method(self, func: callable) -> Tuple[dict[str, str], list[str]]:
        signature: inspect.Signature = inspect.signature(func)
        param_lower_map = {p.lower(): p for p in signature.parameters.keys()}
        filtered_args = {param_lower_map.get(k.lower()): v for k, v in request.args.items() if k.lower() in param_lower_map.keys()}
        missing_params = [k.lower() for k, v in signature.parameters.items() if k not in filtered_args and not v.default != inspect.Parameter.empty]

        return filtered_args, missing_params

    def _gen_func_names_for_method(self, method: str) -> Iterable[str]:
        yield '%s%s' % (self.request_func_prefix, method.lower())
        yield self.any_method_func

    def _get_func_for_method(self, method: str) -> Optional[callable]:
        for func_name in self._gen_func_names_for_method(method):
            if not hasattr(self, func_name):
                continue

            func = getattr(self, func_name)

            if not isinstance(func, Callable):
                continue

            return func

        return None

    # noinspection PyMethodMayBeStatic
    def _serialize_data(self, data: Union[dict[any, any], list[any], any]) -> Tuple[str, str]:
        result = clean_null_fields(data)
        accept_items = get_accept_header_values(request.headers.get('accept', None)) or []
        serialize_func = next((RESPONSE_TYPE_MAP[i] for i in accept_items if i in RESPONSE_TYPE_MAP), None) or RESPONSE_TYPE_MAP[DEFAULT_CONTENT_TYPE]

        return serialize_func(result)
