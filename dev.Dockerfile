FROM python:3.12-slim-bookworm

# hadolint ignore=DL3008,DL3009
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

COPY pyproject.toml uv.lock /

RUN uv sync --frozen
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app

ENV PYTHONPATH=/

COPY ./app /app

ENTRYPOINT ["/app/entrypoint.sh"]
