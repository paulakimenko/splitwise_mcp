FROM python:3.11-slim

# Install system dependencies including supervisor for process management
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential supervisor && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create supervisor configuration
COPY <<EOF /etc/supervisor/conf.d/splitwise.conf
[supervisord]
nodaemon=true

[program:fastapi]
command=uvicorn app.main:app --host 0.0.0.0 --port 8000
directory=/app
autostart=true
autorestart=true
stderr_logfile=/var/log/fastapi.err.log
stdout_logfile=/var/log/fastapi.out.log

[program:mcp_server]
command=python -m app.mcp_server
directory=/app
autostart=true
autorestart=true
stderr_logfile=/var/log/mcp_server.err.log
stdout_logfile=/var/log/mcp_server.out.log
EOF

EXPOSE 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]