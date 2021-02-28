FROM python:3.8.8-alpine

USER root

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    openssl-dev make
RUN apk add rust cargo bash

RUN pip install --upgrade pip
RUN pip install poetry

RUN addgroup -g 1000 -S python && adduser -u 1000 -S python -G python
USER python

RUN mkdir home/python/server
WORKDIR home/python/server

ADD pyproject.toml .
RUN poetry install

USER root
RUN apk del --no-cache .build-deps

USER python
COPY --chown=python:python . /home/python/server

EXPOSE 8000
