# Scripts Directory

This directory contains utility scripts for testing and managing the Splitwise MCP service.

## Available Scripts

### `test_docker_mcp.sh`
**Purpose**: Automated Docker testing workflow
- Starts Docker Compose services (MCP Server)
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

### `test_splitwise_integration.py`
**Purpose**: Comprehensive Splitwise MCP connector integration testing
- Validates remote MCP connector endpoints
- Tests get_current_user, list_groups, list_expenses
- Validates search and fetch tools (required for ChatGPT connectors)
- Provides detailed error diagnostics and troubleshooting guidance

**Usage**:
```bash
# From project root
python scripts/test_splitwise_integration.py

# Or with custom configuration
export SPLITWISE_MCP_URL='https://sw-mcp.paulakimenko.xyz'
python scripts/test_splitwise_integration.py

# Or with uv (recommended)
uv run scripts/test_splitwise_integration.py
```

**Requirements**: Python with httpx and asyncio support, remote MCP server running

**Configuration**:
- `SPLITWISE_MCP_URL`: Base URL of the MCP server (default: https://sw-mcp.paulakimenko.xyz)

**What it tests**:
1. ✅ Basic connectivity and authentication (get_current_user)
2. ✅ Group enumeration (list_groups)
3. ✅ Expense listing with parameters (list_expenses)
4. ✅ Search tool functionality (ChatGPT connector requirement)
5. ✅ Fetch tool functionality (ChatGPT connector requirement)

**Troubleshooting**: The script provides detailed diagnostics when tests fail:
- 400 Bad Request → Check authentication token, base URL, JSON formatting
- Connection errors → Verify server is running and accessible
- Missing endpoints → May need to implement search/fetch tools for ChatGPT

## Testing Workflow

### Local Development Testing
1. **Start Docker Services**: `./scripts/test_docker_mcp.sh`
2. **Manual Testing**: `python scripts/test_mcp_docker.py`
3. **Stop Services**: `docker-compose down`

### Remote MCP Connector Testing
1. **Configure credentials** (if not using defaults):
   ```bash
   export SPLITWISE_MCP_URL='https://your-mcp-server.com'
   ```
2. **Run integration tests**: `python scripts/test_splitwise_integration.py`
3. **Review results**: Check the test summary for any failures
4. **Troubleshoot**: Follow the detailed diagnostics if tests fail

## Access Points

When services are running:
- **API Server**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MCP Tools**: http://localhost:8000/mcp-test/list-tools
- **Health Check**: http://localhost:8000/health