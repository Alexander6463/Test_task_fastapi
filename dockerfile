from python:3.8.10 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install pipenv

COPY .env alembic.ini main.py Pipfile Pipfile.lock ./

RUN pipenv install --system

COPY alembic alembic
COPY db db
COPY src src

FROM base as build
CMD alembic upgrade head && python3 main.py

FROM base as test
COPY tests tests
RUN pipenv install --system --dev
CMD pytest -vv --cov .

