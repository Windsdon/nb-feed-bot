FROM python:3.10-alpine

RUN addgroup -S app && adduser -S app -G app

ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.4.2

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code

RUN chown app:app .

COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Creating folders, and files for a project:
COPY . /code

USER app

CMD ["celery", "-A", "bot.tasks", "worker", "--loglevel=INFO", "-E", "-B", "--pool", "threads"]
