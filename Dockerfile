
# syntax=docker/dockerfile:1

FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/sentinel

# Create a non-root user
RUN groupadd --system sentinel && \
    useradd --system --gid sentinel \
    --no-create-home sentinel

# Install application dependencies
COPY requirements-prod-pinned.txt ./
RUN python -m pip install --no-cache-dir \
    -r requirements-prod-pinned.txt

# Copy application code
COPY --chown=sentinel:sentinel app/ ./app/

# Run the application as a non-root user
USER sentinel

EXPOSE 8000

# Check application health
HEALTHCHECK --interval=30s --timeout=3s \
    --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).close()"

CMD ["python", "-m", "uvicorn", "app.main:testapp", \
     "--host", "0.0.0.0", "--port", "8000"]
