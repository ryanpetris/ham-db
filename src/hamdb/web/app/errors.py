#!/usr/bin/env python3

from ..common import WebException, Handler, HandlerArgumentSource, register
from flask import Blueprint
from werkzeug.exceptions import HTTPException as WerkzeugHTTPException

bp = Blueprint('error', __name__)


@register(bp.app_errorhandler, WerkzeugHTTPException)
class WerkzeugHTTPExceptionHandler(Handler):
    def __init__(self):
        super().__init__(arg_source=HandlerArgumentSource.DIRECT)

    def do_any(self, ex: WerkzeugHTTPException):
        raise WebException(ex.code, ex.description)
