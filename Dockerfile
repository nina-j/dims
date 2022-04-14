FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION="1.1.13" \
    POETRY_VIRTUALENVS_CREATE=false


RUN pip3 install --no-cache-dir poetry==${POETRY_VERSION}
WORKDIR /code
COPY . .
RUN poetry install --no-interaction
