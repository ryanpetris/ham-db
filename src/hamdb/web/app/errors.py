#!/usr/bin/env python3

from flask import Blueprint
from werkzeug.exceptions import HTTPException as WerkzeugHTTPException

from ..common import WebException, serializer_wrapper

bp = Blueprint('error', __name__)


@bp.app_errorhandler(WerkzeugHTTPException)
@serializer_wrapper
def _werkzeug_exception_handler(ex: WerkzeugHTTPException):
    raise WebException(ex.code, ex.description)


@bp.app_errorhandler(WebException)
@serializer_wrapper
def _web_exception_handler(ex: WebException):
    raise ex
