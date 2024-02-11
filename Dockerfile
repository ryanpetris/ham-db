FROM alpine:edge AS base

RUN apk update && apk add py3-pip


FROM base AS build

COPY src /app/src/
COPY MANIFEST.in /app/
COPY setup.py /app/
COPY requirements_build.txt /app/

RUN pip install --break-system-packages build installer setuptools wheel
RUN cd /app && python -m build --wheel --no-isolation


FROM base

COPY --from=build /app/dist/hamdb-*.whl /

RUN pip install --break-system-packages gunicorn /hamdb-*.whl
