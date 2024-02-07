FROM alpine:edge AS base

RUN apk update && apk add py3-pip


FROM base AS build

COPY src /app/src/
COPY setup.py /app/

RUN pip install --break-system-packages build installer setuptools wheel
RUN cd /app && python -m build --wheel --no-isolation


FROM base

COPY --from=build /app/dist/hamdb-*.whl /

RUN pip install --break-system-packages gunicorn /hamdb-*.whl
