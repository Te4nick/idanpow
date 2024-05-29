FROM python:3.12.2-alpine3.19

WORKDIR /app

RUN apk upgrade --no-cache

RUN pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false  \
    && poetry install --no-dev

COPY ./api/ /app/

CMD poetry run gunicorn