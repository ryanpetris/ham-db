#!/bin/sh

export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)/src:$PYTHONPATH"

exec flask --app 'hamdb.web:create_app()' run
