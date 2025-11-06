# Scripts Directory

This directory contains utility scripts for testing and managing the Splitwise MCP service.

## Available Scripts

### `test_docker_mcp.sh`
**Purpose**: Automated Docker testing workflow
- Starts Docker Compose services (MongoDB + MCP Server)
- Waits for services to be ready
- Runs comprehensive functionality tests
- Provides access URLs and next steps

**Usage**:
```bash
# From project root
./scripts/test_docker_mcp.sh
```

**Requirements**: Docker Desktop running, docker-compose available

### `test_mcp_docker.py`
**Purpose**: Comprehensive MCP server functionality testing
- Tests health endpoint
- Validates API documentation availability
- Checks MCP endpoint responses
- Lists available MCP tools
- Tests custom endpoints

**Usage**:
```bash
# From project root
python scripts/test_mcp_docker.py
```

**Requirements**: Python with requests library, MCP server running on localhost:8000

### `test_mcp_manual.py`
**Purpose**: Manual testing utilities for MCP server functionality
- Interactive testing of MCP server components
- Debugging and development utilities

**Usage**:
```bash
# From project root
python scripts/test_mcp_manual.py
```

## Testing Workflow

1. **Start Docker Services**: `./scripts/test_docker_mcp.sh`
2. **Manual Testing**: `python scripts/test_mcp_docker.py`
3. **Stop Services**: `docker-compose down`

## Access Points

When services are running:
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MCP Tools**: http://localhost:8000/mcp-test/list-tools
- **Health Check**: http://localhost:8000/health
- **MongoDB**: mongodb://localhost:27017