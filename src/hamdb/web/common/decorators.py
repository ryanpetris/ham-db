#!/usr/bin/env python3

from flask.sansio.scaffold import Scaffold

from .view import BaseView


def register_route(app: Scaffold, *args, **kwargs):
    def wrapper(func):
        if issubclass(func, BaseView):
            app.add_url_rule(*args, **kwargs, view_func=func.as_view(func.__name__))
            return func

        return app.route(*args, **kwargs)(func)

    return wrapper
