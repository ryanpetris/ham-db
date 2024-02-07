#!/bin/bash

set -e
set -o pipefail

REGISTRY="$1"
VERSION="$(python ./setup.py --version)"

if [ -z "$REGISTRY" ]; then
    echo "Please specify registry"
fi

docker image tag "ham-db:${VERSION}" "${REGISTRY}/ham-db:${VERSION}"
docker image tag "ham-db:latest" "${REGISTRY}/ham-db:latest"

docker image push "${REGISTRY}/ham-db:${VERSION}"
docker image push "${REGISTRY}/ham-db:latest"
