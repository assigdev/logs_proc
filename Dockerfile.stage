FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN \
  apt-get -y update && \
  apt-get install -y gettext && \
  apt-get clean
RUN pip install uwsgi

ADD . /opt/logs_proc
WORKDIR /opt/logs_proc/app

RUN pip install pipenv && \
    pipenv install --system --deploy --three

EXPOSE 8000
ENV PORT 8000
