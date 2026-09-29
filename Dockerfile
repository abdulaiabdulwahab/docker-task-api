# =====================================
# STAGE 1 — Builder
# =====================================

FROM python:3.13-slim AS builder

WORKDIR /build


# Copy dependency definition first
COPY requirements.txt .


# Create an isolated Python environment
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install \
       --no-cache-dir \
       -r requirements.txt



# =====================================
# STAGE 2 — Runtime
# =====================================

FROM python:3.13-slim AS runtime


# Use the virtual environment created
# in the builder stage
ENV PATH="/opt/venv/bin:$PATH"


# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1


# Send Python output directly to logs
ENV PYTHONUNBUFFERED=1


# Create non-root application user
RUN useradd \
    --create-home \
    --uid 10001 \
    appuser


WORKDIR /app


# Copy only installed dependencies
# from the build stage
COPY --from=builder /opt/venv /opt/venv


# Copy application source
COPY app.py .


# Run as non-root
USER appuser


EXPOSE 5000


# Docker periodically checks whether
# the application is responding.
HEALTHCHECK \
  --interval=10s \
  --timeout=3s \
  --start-period=10s \
  --retries=3 \
  CMD python -c \
  "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" \
  || exit 1


# Start production web server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]