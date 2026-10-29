# EkNothi web chat + WhatsApp webhook.
# Chromium is installed for the case file PDF (Bangla shaping needs a real browser engine).
# bookworm: Playwright 1.49's --with-deps package list doesn't match Debian 13 (trixie).
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    EKNOTHI_VAR_DIR=/data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && python -m playwright install --with-deps --only-shell chromium \
 && rm -rf /var/lib/apt/lists/*

COPY app ./app
COPY data ./data
COPY web ./web

# Mount a persistent volume at /data: conversations (SQLite) and case files live there.
RUN mkdir -p /data
EXPOSE 8000

# Hosts like Railway and Render set $PORT.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --proxy-headers --forwarded-allow-ips='*'"]
