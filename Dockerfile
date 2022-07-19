FROM python:3.10-slim-buster as base
RUN apt-get update; apt-get install curl -y
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /todo_app
COPY pyproject.toml /todo_app/pyproject.toml
COPY poetry.lock /todo_app/poetry.lock
COPY todo_app ./todo_app

FROM base AS production
RUN poetry config virtualenvs.create false --local && poetry install
ENV PORT=80
CMD poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:$PORT

FROM base AS development
RUN poetry install
EXPOSE 5000
ENTRYPOINT poetry run flask run --host 0.0.0.0

FROM base AS testing
RUN poetry install
RUN apt-get update && apt-get install -y firefox-esr curl
RUN curl -sSLO https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/ \
   && rm geckodriver-*.tar.gz
COPY .env.test /todo_app/.env.test
ENTRYPOINT [ "poetry", "run", "pytest" ]