FROM python:3.8-slim-buster

ENV LANG C.UTF-8
ENV TZ UTC
ENV PYTHONUNBUFFERED 1
#ENV PYTHONPATH /backend
EXPOSE 80

RUN apt-get update && apt-get install -y git gcc libmariadb-dev curl

#RUN bash -c "if [ $EVN == 'production' ]; then copy . ./backend; fi"
COPY . ./backend
WORKDIR /backend
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN poetry install --no-root

# 環境毎の差異に対応するため、uvicornの起動は、docker-composeやtask-definitionで行う
#ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--log-config", "logger_config.yaml"]
