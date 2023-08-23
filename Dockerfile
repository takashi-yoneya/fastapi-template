FROM python:3.11-bookworm

ENV LANG C.UTF-8
ENV TZ UTC
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /backend/app:/backend
ENV TERM xterm-256color

RUN apt-get update && apt-get install -y \
    git \
    gcc \
    libmariadb-dev \
    curl

WORKDIR /backend
COPY ./requirements.lock /backend/

# ryeがrequirements.lockを常に最新化していることを前提とした暫定的な対応
RUN sed '/-e/d' requirements.lock > requirements.txt
RUN pip install -r requirements.txt

COPY . /backend/
