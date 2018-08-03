FROM python:3.7.0-alpine3.8

MAINTAINER Sami Racho <sami@racho.es>

ENV APPPATH=/healthchecker
RUN mkdir -p ${APPPATH}
COPY src/ ${APPPATH}

RUN pip install -r ${APPPATH}/resources/requirements.txt

ARG HK_NOTIFY_TOKEN
ENV HK_NOTIFY_TOKEN=$HK_NOTIFY_TOKEN

ENTRYPOINT ${APPPATH}/main.py