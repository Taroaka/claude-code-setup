FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# Runtime deps: ffmpeg for video assembly, ca-certificates for HTTPS
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv for dependency management (CPU-only image)
RUN pip install --no-cache-dir uv

COPY requirements.txt /app/requirements.txt
RUN uv pip install --system --requirement /app/requirements.txt

COPY . /app

CMD ["bash"]
