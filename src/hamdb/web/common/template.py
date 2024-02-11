#!/usr/bin/env python3

from flask import render_template as flask_render_template
from jinja2.environment import Template

from ...common.settings import SITE_NAME


def _get_template_config():
    return {
        'site_name': SITE_NAME
    }


def render_template(template: str | Template | list[str | Template], **context) -> str:
    return flask_render_template(template, config=_get_template_config(), **context)
