FROM python:3.13.5-slim-bookworm AS base

ARG USER_ID=1000
ARG GROUP_ID=1000
ARG NONROOT_USER=nonroot
ARG UV_PATH=./.local/bin/uv
ARG PYSETUP_PATH=/opt/pysetup

ENV UV_COMPILE_BYTECODE=1
ENV PATH="${PYSETUP_PATH}/.venv/bin:${PATH}"

RUN groupadd --gid ${GROUP_ID} ${NONROOT_USER} && \
    useradd --uid ${USER_ID} --gid ${GROUP_ID} --create-home --home-dir ${PYSETUP_PATH} ${NONROOT_USER} && \
    mkdir -p ${PYSETUP_PATH}/app && \
    chown -R ${NONROOT_USER}:${NONROOT_USER} ${PYSETUP_PATH}

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

USER ${NONROOT_USER}
WORKDIR ${PYSETUP_PATH}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY --chown=${NONROOT_USER}:${NONROOT_USER} pyproject.toml uv.lock ./

RUN ${UV_PATH} venv && \
    ${UV_PATH} sync --frozen

FROM base AS runtime

COPY --from=base ${PYSETUP_PATH}/.venv ${PYSETUP_PATH}/.venv
COPY --chown=${NONROOT_USER}:${NONROOT_USER} ./app ${PYSETUP_PATH}/app

WORKDIR ${PYSETUP_PATH}/app
