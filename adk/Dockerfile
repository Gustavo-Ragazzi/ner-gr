FROM python:3.13-slim

WORKDIR /app

ENV POETRY_VERSION=1.8.2
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y curl build-essential && \
  curl -sSL https://install.python-poetry.org | python3 - && \
  ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

COPY named_entity_recognition ./named_entity_recognition

CMD ["poetry", "run", "adk", "web", "--host", "0.0.0.0", "--port", "8000"]
