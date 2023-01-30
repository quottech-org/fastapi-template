ARG PYTHON_VERSION=3.9
FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED 1
ARG PIP_EXTRA_INDEX_URL

RUN mkdir -p /code/
WORKDIR /code/

COPY ub_backend/pyproject.toml /code/
COPY ub_backend/poetry.lock /code/

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi -vvv


CMD gunicorn --reload --bind 0.0.0.0:8000 -w 1 -k uvicorn.workers.UvicornWorker ub_backend.main:app