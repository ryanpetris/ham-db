#!/usr/bin/env python3

from .handler import Handler
from flask.sansio.scaffold import Scaffold


def app_route(app: Scaffold, rule: str, **options: any):
    def wrapper(func):
        if issubclass(func, Handler):
            func.register_route(app, rule, **options)
            return func

        return app.route(rule, **options)(func)

    return wrapper
