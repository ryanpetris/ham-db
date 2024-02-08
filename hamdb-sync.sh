#!/bin/sh

export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)/src:$PYTHONPATH"

exec python3 -u -m hamdb.cli.sync_cmd "$@"
