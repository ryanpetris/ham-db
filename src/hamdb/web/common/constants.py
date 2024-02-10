#!/usr/bin/env python3

CONTENT_TYPE_JSON: str = 'application/json'
CONTENT_TYPE_YAML: str = 'application/yaml'
CONTENT_TYPE_XML: str = 'application/xml'

DEFAULT_CHARSET: str = 'utf-8'

ALL_HTTP_METHODS: set[str] = {
    'GET',
    'POST',
    'HEAD',
    'PUT',
    'PATCH',
    'DELETE'
}