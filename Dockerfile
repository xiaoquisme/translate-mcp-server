FROM ghcr.io/astral-sh/uv:python3.12-alpine

RUN apk add --no-cache \
    build-base \
    cargo \
    rust

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app \
    RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH

COPY pyproject.toml .
COPY uv.lock .
COPY .python-version .
RUN uv sync

COPY . /app

ENV PORT=8000 \
    HOST=0.0.0.0

EXPOSE 8000

CMD [".venv/bin/python", "main.py"]

