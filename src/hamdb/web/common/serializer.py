#!/usr/bin/env python3

import json
import yaml

from .constants import CONTENT_TYPE_JSON, CONTENT_TYPE_YAML, CONTENT_TYPE_XML, DEFAULT_CHARSET
from dict2xml import Converter as XmlConverter


def serialize_json(data: dict[str, any]) -> tuple[str, str]:
    return json.dumps(data, sort_keys=True), f'{CONTENT_TYPE_JSON}; charset={DEFAULT_CHARSET}'


def serialize_yaml(data: dict[str, any]) -> tuple[str, str]:
    return yaml.safe_dump(data, sort_keys=True), f'{CONTENT_TYPE_YAML}; charset={DEFAULT_CHARSET}'


def serialize_xml(data: dict[str, any]) -> tuple[str, str]:
    converter = XmlConverter(indent=None, newlines=None)
    return converter.build(data), f'{CONTENT_TYPE_XML}; charset={DEFAULT_CHARSET}'
