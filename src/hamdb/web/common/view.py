#!/usr/bin/env python3

import inspect
from typing import Callable, Optional, Tuple

from flask import request
from flask.globals import current_app
from flask.views import MethodView, http_method_funcs
from flask.wrappers import Response
from werkzeug.exceptions import MethodNotAllowed

from .exceptions import NotFoundException
from .serializer import serializer_wrapper
from ...common import map_lower, keys_lower


def _extract_arguments_for_method(func: callable, kwargs: dict[str, any]) -> Tuple[dict[str, str], list[str]]:
    signature = inspect.signature(func)
    args_lower_map = map_lower(signature.parameters.keys())
    provided_args = keys_lower({**kwargs, **request.args})
    missing = [k.lower() for k, v in signature.parameters.items() if
               k.lower() not in provided_args and not v.default != inspect.Parameter.empty]

    return {args_lower_map.get(k): v for k, v in provided_args.items() if k in args_lower_map}, missing


def _get_func_for_method(view: 'BaseView', method: str) -> Optional[callable]:
    method = method.lower()

    if method not in http_method_funcs:
        return None

    if not hasattr(view, method):
        return None

    func = getattr(view, method)

    if not isinstance(func, Callable):
        return None

    return func


class BaseView(MethodView):
    provide_automatic_options = True

    @serializer_wrapper
    def dispatch_request(self, **kwargs) -> Response:
        func = _get_func_for_method(self, request.method)

        if not func and request.method == 'HEAD':
            func = _get_func_for_method(self, 'HEAD')

        if not func:
            raise NotFoundException(f"Method {request.method!r} not implemented.")

        args, missing = _extract_arguments_for_method(func, kwargs)

        if missing:
            raise MethodNotAllowed()

        return current_app.ensure_sync(func)(**args)
