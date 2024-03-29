#!/usr/bin/env python3

import inspect
from typing import Callable, Optional, Tuple

from flask import request, render_template
from flask.globals import current_app
from flask.views import MethodView, http_method_funcs
from jinja2.environment import Template

from .contenttype import ContentType
from .exceptions import BadRequestException, NotFoundException
from .serializer import serializer_wrapper
from ...common import map_lower, keys_lower
from ...common.settings import SITE_NAME


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


def _get_template_config():
    return {
        'site_name': SITE_NAME
    }


class BaseView(MethodView):
    provide_automatic_options = True

    @property
    def is_html_requested(self) -> bool:
        return ContentType.get_header_preference() == ContentType.HTML

    @serializer_wrapper
    def dispatch_request(self, **kwargs) -> any:
        func = _get_func_for_method(self, request.method)

        if not func and request.method == 'HEAD':
            func = _get_func_for_method(self, 'GET')

        if not func:
            raise NotFoundException(f"Method {request.method!r} not implemented.")

        args, missing = _extract_arguments_for_method(func, kwargs)

        if missing:
            raise BadRequestException(f'Missing required arguments: {", ".join(missing)}')

        return current_app.ensure_sync(func)(**args)

    @staticmethod
    def render_template(template: str | Template | list[str | Template], **context) -> str:
        return render_template(template, config=_get_template_config(), **context)
