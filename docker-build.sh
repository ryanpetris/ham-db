#!/bin/bash

set -e
set -o pipefail

VERSION="$(python ./setup.py --version)"

exec docker buildx build -t "ham-db:${VERSION}" -t "ham-db:latest" .
