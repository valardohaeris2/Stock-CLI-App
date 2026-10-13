# syntax=docker/dockerfile:1

# Base image pinned by digest so builds are reproducible and can't be silently swapped.
# Update with: docker buildx imagetools inspect python:3.13-slim-trixie
ARG PYTHON_IMAGE=python:3.13-slim-trixie@sha256:70729b46c69b4f1e97c4822c1af3df53a1476cf5ddc6c087c0c10bc3a5678c2f

# ---- Build stage: install dependencies into an isolated virtualenv ----
FROM ${PYTHON_IMAGE} AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Hash-locked deps. Regenerate after editing requirements.txt:
#   docker run --rm -v "$PWD":/src -w /src python:3.13-slim-trixie sh -c \
#     'pip install pip-tools && pip-compile --generate-hashes --strip-extras --allow-unsafe -o requirements.lock requirements.txt'
COPY requirements.lock .
RUN pip install --require-hashes --only-binary=:all: -r requirements.lock \
    && pip uninstall -y pip

# ---- Runtime stage: minimal image, no build tooling, non-root ----
FROM ${PYTHON_IMAGE} AS runtime

# Apply OS security patches released since the base image was built, and drop
# pip (not needed at runtime; its vendored libraries carry their own CVEs)
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip uninstall -y --root-user-action=ignore pip \
    && rm -f /usr/local/bin/pip*

# Unprivileged user with a fixed UID (works with runAsNonRoot in Kubernetes)
RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg \
    MPLCONFIGDIR=/tmp/matplotlib \
    XDG_CACHE_HOME=/tmp/cache

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
# Code is owned by root and read-only to the app user
COPY main.py .
COPY stock_analyzer/ stock_analyzer/

# Writable location for --csv / --save-chart output (mount a volume here)
RUN mkdir /output && chown app:app /output

USER app:app

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
