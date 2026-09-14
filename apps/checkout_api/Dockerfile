FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1
# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Omit development dependencies
ENV UV_NO_DEV=1

USER root

RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*
RUN groupadd -g 1000 fastapigroup 
RUN useradd -m -u 1000 -g fastapigroup fastapiuser

# Install application
WORKDIR /app
RUN chown -R fastapiuser:fastapigroup /app
COPY --chown=fastapiuser:fastapigroup . /app
COPY --chown=fastapiuser:fastapigroup pyproject.toml /app

USER fastapiuser
# Install dependencies
RUN uv sync --locked
# Run the application using uvicorn
CMD ["uv", "run", "uvicorn", "apps.checkout_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
