#!/bin/bash
# Test MCP Server with Docker Compose

set -e

echo "🚀 Starting MCP Server with Docker Compose..."

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

# Start services
echo "📦 Starting MongoDB and MCP Server..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if containers are running
echo "🔍 Checking container status..."
docker-compose ps

# Test the MCP server
echo "🧪 Testing MCP server functionality..."
python3 scripts/test_mcp_docker.py

echo ""
echo "✅ MCP Server is running!"
echo "🌐 Access the API at: http://localhost:8000"
echo "📚 View API docs at: http://localhost:8000/docs"
echo "🔧 MCP tools at: http://localhost:8000/mcp-test/list-tools"
echo ""
echo "To stop the services, run: docker-compose down"