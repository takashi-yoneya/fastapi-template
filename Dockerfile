# ベースイメージ
# FROM python:3.8.6-alpine3.12
FROM python:3.8-slim-buster

# 環境変数
ENV LANG C.UTF-8
ENV TZ UTC
ENV PYTHONUNBUFFERED 1
EXPOSE 80

# 各種パッケージのインストール
RUN apt-get update && apt-get install -y git gcc libmariadb-dev curl sudo procps
# RUN apt-get update && apt-get install -y \
#     git \
#     curl \
#     mariadb-connector-c-dev
#RUN apt-get update && git curl build-base mariadb-connector-c-dev
# swig gfortran linux-headers

# Mecab
# RUN cd /tmp \
#     && git clone https://github.com/taku910/mecab.git \
#     && cd mecab/mecab/ \
#     && ./configure --enable-utf8-only --with-charset=utf8 \
#     && make \
#     && make install \
#     && cd ../mecab-ipadic \
#     && ./configure --with-charset=utf8 \
#     && make \
#     && make install

# INSTALL
#COPY requirements.txt /home
#WORKDIR /home

# COPY ./backend ./backend
# COPY ./requirements.txt ./requirements.txt
# COPY .env .env
# COPY ./logger.conf ./logger.conf
# COPY ./logger_config.yaml ./logger_config.yaml
# Install Poetry
COPY . ./backend
WORKDIR /backend
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
# COPY ./pyproject.toml ./poetry.lock* /backend
# COPY ./backend/pyproject.toml /backend/pyproject.toml

RUN poetry install --no-root

#RUN poetry install

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--log-config", "logger_config.yaml"]
# CMD ["uvicorn","main:app","--host","0.0.0.0", "--port", "80", "--reload"]
# CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "manaus.server.main:app", "--bind=0.0.0.0:80"]