# ---- Builder Stage ----
FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

COPY . .

# ---- Production Stage ----
FROM python:3.12-slim AS production

RUN groupadd -r appgroup && useradd -r -g appgroup appuser
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/*
RUN find / -perm /6000 -type f -exec chmod a-s {} + || true

WORKDIR /app

COPY --from=builder /install /usr/local
COPY --from=builder --chown=appuser:appgroup /app ./

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER appuser

RUN chmod +x entrypoint.sh

ENTRYPOINT ["dumb-init", "--", "./entrypoint.sh"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

LABEL org.opencontainers.image.source="https://github.com/yourorg/youth"
LABEL org.opencontainers.image.description="Youth Backend API"
