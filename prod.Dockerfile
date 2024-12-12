FROM python:3.12.8-slim-bookworm

# hadolint ignore=DL3008,DL3009
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/0.5.8/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV UV_COMPILE_BYTECODE=1

ENV PATH="/root/.local/bin/:$PATH"

COPY pyproject.toml uv.lock /

RUN uv sync --frozen --no-dev
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app

COPY ./app /app

ENTRYPOINT ["/app/entrypoint.sh"]
