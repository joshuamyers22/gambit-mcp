# syntax=docker/dockerfile:1.7
FROM python:3.12.14-slim-bookworm@sha256:782412e85d0f0984994c290652577d4018aff08145c85b262bb63dc0c7522254 AS builder
ENV UV_NO_CACHE=1 UV_LINK_MODE=copy
WORKDIR /app
RUN python -m pip install --no-cache-dir uv==0.12.5
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --no-editable

FROM python:3.12.14-slim-bookworm@sha256:782412e85d0f0984994c290652577d4018aff08145c85b262bb63dc0c7522254 AS runtime
ARG APP_RELEASE=0.1.0
ARG APP_REVISION=local
LABEL org.opencontainers.image.version="${APP_RELEASE}" \
  org.opencontainers.image.revision="${APP_REVISION}"
ENV PATH=/app/.venv/bin:$PATH \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  APP_TRANSPORT=streamable-http \
  APP_HOST=0.0.0.0 \
  APP_RELEASE="${APP_RELEASE}" \
  APP_REVISION="${APP_REVISION}"
RUN groupadd --system --gid 10001 app && useradd --system --uid 10001 --gid app app
WORKDIR /app
COPY --from=builder --chown=10001:10001 /app/.venv /app/.venv
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2)"]
ENTRYPOINT ["gambit-mcp"]
