FROM python:3.8-alpine

WORKDIR /var

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/var

RUN apk update && apk add gcc musl-dev libffi-dev openssl-dev python3-dev

ADD requirements.txt .
RUN pip3 install --upgrade setuptools pip cffi
RUN pip3 install -r requirements.txt

COPY . /var