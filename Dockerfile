FROM python:3.12.1

WORKDIR /ExanteDataBackend

RUN apt-get update
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=~/.local/bin/poetry python3 -

RUN apt-get update && \
    apt-get -y install curl && \
    apt-get -y install nano && \
    apt-get -y install htop

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml /ExanteDataBackend/
RUN ~/.local/bin/poetry/bin/poetry config virtualenvs.create false && \
    ~/.local/bin/poetry/bin/poetry install --no-root --no-interaction && \
    rm -rf /root/.cache/pypoetry

COPY entrypoint.sh entrypoint.sh

COPY . .
EXPOSE 8000
CMD ["bash", "entrypoint.sh"]
