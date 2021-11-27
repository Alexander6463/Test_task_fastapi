from python:3.8.10 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip install pipenv

COPY . ./

RUN pipenv install --system

CMD alembic upgrade head && python3 main.py

