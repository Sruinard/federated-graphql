FROM python:3.9-alpine


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME=/etc/poetry

# Install dev dependencies
RUN apk update \
    && apk add curl postgresql-dev gcc python3-dev musl-dev openssl-dev libffi-dev

RUN pip install -U pip \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 -

ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock /usr/src/app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . .

CMD poetry run task server
