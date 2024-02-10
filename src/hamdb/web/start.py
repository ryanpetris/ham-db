#!/usr/bin/env python3

from flask import Flask

from .app import error_bp, root_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(error_bp)
    app.register_blueprint(root_bp)

    return app
