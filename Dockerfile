# syntax=docker/dockerfile:1

# ============================================================
# Stage 1: Builder
# Installs build dependencies and prepares an isolated venv.
# ============================================================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /build

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv "$VIRTUAL_ENV"

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install -r requirements.txt


# ============================================================
# Stage 2: Final Runtime
# Lightweight image with no compiler/build tools.
# ============================================================
FROM python:3.11-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    WEB_CONCURRENCY=1

WORKDIR /app

# Runtime libraries only.
# libmariadb3 is needed if requirements uses mysqlclient.
# It is harmless for PyMySQL-based projects and keeps MySQL compatibility safe.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libmariadb3 \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system appgroup \
    && adduser --system --ingroup appgroup --home /app appuser

COPY --from=builder /opt/venv /opt/venv
COPY app ./app

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers ${WEB_CONCURRENCY}"]