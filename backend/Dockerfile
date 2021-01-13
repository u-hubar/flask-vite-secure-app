FROM python:3.8-alpine

WORKDIR /var

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/var

ADD requirements.txt .
RUN pip3 install --upgrade setuptools pip
RUN pip3 install -r requirements.txt

COPY . /var