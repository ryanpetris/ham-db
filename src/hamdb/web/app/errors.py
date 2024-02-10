#!/usr/bin/env python3

from ..common import NotFoundException, InternalServerErrorException, Handler
from flask import Blueprint
from werkzeug.exceptions import NotFound as WerkzeugNotFound, InternalServerError as WerkzeugInternalServerError

bp = Blueprint('error', __name__)


@bp.app_errorhandler(WerkzeugNotFound)
class NotFoundErrorHandler(Handler):
    def do_any(self):
        raise NotFoundException


@bp.app_errorhandler(WerkzeugInternalServerError)
class InternalServerErrorHandler(Handler):
    def do_any(self):
        raise InternalServerErrorException
