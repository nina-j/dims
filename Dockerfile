FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION="1.1.13" \
    POETRY_VIRTUALENVS_CREATE=false


RUN pip3 install poetry==${POETRY_VERSION} --quiet --no-cache-dir
WORKDIR /code
RUN mkdir data
COPY . .
RUN poetry install --no-interaction
