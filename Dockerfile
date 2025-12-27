# -------------------------------
# Base image: Python 3.11
# -------------------------------
FROM python:3.11-slim

# -------------------------------
# System dependencies
# -------------------------------
RUN apt-get update && apt-get install -y \
    git \
    ca-certificates \
    curl \
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
# Clone your fork
# -------------------------------
RUN git clone https://github.com/RolandWijnen/tidal-mcp.git .

# -------------------------------
# Install Python dependencies
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
# Default CMD (can be overridden in Docker Compose)
# -------------------------------
CMD ["npx", "-y", "supergateway", "--stdio", "uv run python mcp_server/server.py", "--port", "6015"]
