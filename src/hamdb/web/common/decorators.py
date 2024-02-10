#!/usr/bin/env python3

from .handler import Handler
from flask.sansio.scaffold import Scaffold


def register(app: callable, *args, **kwargs):
    def wrapper(func):
        if issubclass(func, Handler):
            func.register(app, *args, **kwargs)
            return func

        return app(*args, **kwargs)(func)

    return wrapper


def register_route(app: Scaffold, *args, **kwargs):
    def wrapper(func):
        if issubclass(func, Handler):
            func.register_route(app, *args, **kwargs)
            return func

        return app.route(*args, **kwargs)(func)

    return wrapper
