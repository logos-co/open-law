# frontent builder stage ---------------------------------------------
FROM node:20.3-alpine3.18 as frontend_builder

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN yarn
RUN npx update-browserslist-db@latest -y
RUN yarn css
RUN yarn js

# backend builder stage ----------------------------------------------
FROM python:3.11-alpine as backend_builder

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN apk update \
 && apk add --no-cache pkgconfig gcc musl-dev libffi-dev \
 && rm -rf /var/cache/apk/*

RUN python -m venv $VIRTUAL_ENV \
 && pip install poetry

RUN poetry install --only main --no-interaction --no-ansi \
 && poetry add gunicorn

# final image stage --------------------------------------------------
FROM python:3.11-alpine as final

ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir /app
WORKDIR /app

RUN adduser -D app
USER app

RUN pip install poetry

COPY --chown=app:app --from=frontend_builder /app/app/static ./static
COPY --chown=app:app --from=backend_builder  /app ./

ENTRYPOINT ["/bin/sh", "./start_server.sh"]
