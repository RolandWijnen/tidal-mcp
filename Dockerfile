# -------------------------------
# Base image: Python 3.11
# -------------------------------
FROM python:3.11-slim

# -------------------------------
# System dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# Install uv
# -------------------------------
RUN pip install --no-cache-dir uv

# -------------------------------
# App directory
# -------------------------------
WORKDIR /app

# -------------------------------
# Copy local code into container
# -------------------------------
COPY . /app

# -------------------------------
# Install Python dependencies (NO venv)
# -------------------------------
RUN uv pip install --system --editable .

# -------------------------------
# Environment
# -------------------------------
ENV PYTHONUNBUFFERED=1

# -------------------------------
# Expose MCP port
# -------------------------------
EXPOSE 6015

# -------------------------------
# Start MCP via supergateway
# -------------------------------
CMD ["npx", "-y", "supergateway", "--stdio", "uv run python mcp_server/server.py", "--port", "6015"]
