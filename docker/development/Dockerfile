FROM python:3.9.1-alpine

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code
WORKDIR /code

ADD . /code/

RUN ls /code/

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates \
    gcc \
    postgresql-dev \
    linux-headers \
    musl-dev \
    libffi-dev \
    jpeg-dev \
    zlib-dev \
    postgresql-client \
    && pip install -r /code/requirements/development.txt \
    && find /usr/local \
    \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' + \
    && runDeps="$( \
    scanelf --needed --nobanner --recursive /usr/local \
    | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
    | sort -u \
    | xargs -r apk info --installed \
    | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

EXPOSE 8000
CMD ["uvicorn", "--host", "0.0.0.0", "hermes.app:app"]