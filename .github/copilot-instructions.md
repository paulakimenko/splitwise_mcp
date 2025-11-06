# Splitwise MCP Service - Developer Instructions

## Quick Start Essentials

This is a **pure MCP server** (FastMCP) that wraps the Splitwise API for AI agents. The architecture uses **async-over-sync** patterns since the Splitwise SDK is synchronous, and employs **method mapping** to bridge MCP's snake_case conventions with the SDK's camelCase methods.

### Critical Architecture Decisions

**1. ChatGPT Connector Requirements (MANDATORY)**
- **Problem**: ChatGPT connectors REQUIRE exactly two specific tools: `search` and `fetch`
- **Solution**: Added `search` tool (returns list of results with id/title/url) and `fetch` tool (returns full document with id/title/text/url/metadata)
- **Impact**: Without these tools, connector won't appear in ChatGPT despite passing all MCP compliance checks
- **Files**: `app/main.py` (search/fetch implementations), tests in `test_mcp_pure.py`
- **Spec**: [ChatGPT MCP Building Guide](https://platform.openai.com/docs/guides/tools-connectors-mcp)

**2. Nginx Reverse Proxy (Production Deployment)**
- **Problem**: FastMCP returns HTTP 406 for GET requests to `/mcp`, violating MCP spec (expects 405)
- **Solution**: `nginx.conf` intercepts GET requests, returns proper 405 before FastMCP sees them
- **Impact**: Without nginx, ChatGPT and other MCP clients fail during capability negotiation
- **Files**: `docker-compose.yml` (nginx service), `nginx.conf` (405 workaround)

**3. Dual Transport Support**
- **Local Dev**: `stdio` transport (default) - MCP protocol over stdin/stdout
- **Remote/Docker**: `streamable-http` transport - HTTP server on port 8000 at `/mcp` endpoint
- **Switch**: Set `MCP_TRANSPORT=streamable-http` environment variable
- **Why**: stdio for local testing, HTTP for ChatGPT integration and remote clients

**4. MongoDB Graceful Degradation**
- All operations attempt database persistence but **never fail** if MongoDB is unavailable
- Pattern: `try: insert_document(...) except Exception: logging.warning(...)`
- Enables testing without MongoDB while maintaining audit trail in production

**5. Method Mapping Bridge**
```python
# app/splitwise_client.py - Core translation layer
METHOD_MAP = {
    "list_groups": "getGroups",      # MCP snake_case → SDK camelCase
    "create_expense": "createExpense",
    # ... 20+ method mappings
}
```

## Essential References

📋 **[MCP Python SDK Docs](docs-for-copilot/MCP_SDK_README.md)** - FastMCP patterns, context injection, transport options
📋 **[ChatGPT MCP Integration](docs-for-copilot/CHAT_GPT_BUILDING_MCP.md)** - Required `search`/`fetch` tools, testing, security
📋 **[OAuth 2.1 Spec](docs-for-copilot/AUTH_MCP.md)** - Authorization flows, PKCE, dynamic client registration  
📋 **[Splitwise OpenAPI](docs-for-copilot/splitwise-openapi.json)** - Complete API reference, data models, parameters
📋 **[Use Case Examples](docs-for-copilot/use-cases.md)** - 42 real-world expense workflows and patterns

## Key Components & Data Flow

```
MCP Client → [nginx:80] → [FastMCP:8000] → SplitwiseClient → Splitwise API
                ↓              ↓                                      ↓
           405 on GET    Async Wrapper                          SDK (sync)
                          ↓                                          ↓
                    MongoDB (graceful)                      object_to_dict()
```

**`app/main.py`** - Entry point with transport detection, no FastAPI (pure MCP)
**`app/splitwise_client.py`** - METHOD_MAP bridge + SDK wrapper + helper methods (`get_group_by_name`, etc.)
**`app/custom_methods.py`** - Business logic: `expenses_by_month`, `monthly_report` (async, takes SplitwiseClient)
**`app/db.py`** - MongoDB ops with graceful failure: `insert_document`, `find_latest`, `find_all`
**`app/utils.py`** - `object_to_dict()` for SDK→JSON, `month_range()` for date filtering

### MCP Tool/Resource Pattern
```python
# All tools use this helper for consistency
async def _call_splitwise_tool(ctx: Context, method_name: str, **kwargs) -> dict:
    client = ctx.request_context.lifespan_context["client"]  # From lifespan mgmt
    result = await asyncio.to_thread(client.call_mapped_method, method_name, **kwargs)  # Async wrapper
    response_data = client.convert(result)  # SDK objects → dict
    insert_document(method_name, {"response": response_data})  # Persist (graceful)
    log_operation(method_name, "TOOL_CALL", kwargs, response_data)  # Audit trail
    return response_data

# Example tool
@mcp.tool()
async def create_expense(cost: str, description: str, ctx: Context, **kwargs) -> dict:
    return await _call_splitwise_tool(ctx, "create_expense", cost=cost, description=description, **kwargs)
```

## Development Workflows

### Environment Setup
Required environment variables:
- `SPLITWISE_API_KEY` - Personal API token from Splitwise
- `MONGO_URI` - MongoDB connection (defaults to `mongodb://localhost:27017`)
- `DB_NAME` - Database name (defaults to `splitwise`)

**MCP Transport Configuration** (for remote operation):
- `MCP_TRANSPORT` - Transport mode: `stdio` (default) or `streamable-http` for remote access
- `MCP_HOST` - Host to bind to (defaults to `0.0.0.0` for HTTP transport)
- `MCP_PORT` - Port for HTTP transport (defaults to `8000`)

### Quick Start with Makefile
The project includes a comprehensive Makefile for all development operations:

```bash
# Full setup from scratch
make setup                    # Creates venv, installs deps, creates .env

# Development server
make dev                      # Start MCP server with stdio transport

# Testing
make unit-test               # Run unit tests only
make integration-test        # Run integration tests (requires API key)
make test-all               # Run all checks + unit tests
make test-full              # Run all checks + unit + integration tests

# Code quality
make lint                   # Check code with Ruff
make lint-fix              # Auto-fix Ruff issues
make format                # Format code with Ruff
make check                 # Run all quality checks

# Docker operations
make docker-build         # Build Docker image
make docker-push          # Push image to registry
make docker-build-push    # Build and push image
make docker-run           # Run container locally
make docker-compose-up    # Start services
make docker-compose-down  # Stop services
make docker-dev          # Start dev environment

# CI simulation
make ci                   # Full CI pipeline (unit tests)
make ci-full             # Full CI + integration tests
```

### Manual Development Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # or: .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Create environment file
cp .env.example .env
# Edit .env and add your SPLITWISE_API_KEY

# Start development server  
python -m app.main  # Pure MCP server via stdio
```

### Docker Development
Use `docker-compose.yml` for full stack with MongoDB and Streamable HTTP transport:
```bash
docker-compose up --build
```

**Remote Access Configuration:**
- The Docker deployment uses **Streamable HTTP transport** for remote access
- Server runs on port `8000` and is accessible at `http://localhost:8000/mcp`
- MCP clients can connect remotely using the Streamable HTTP transport
- Environment variables `MCP_TRANSPORT=streamable-http`, `MCP_HOST=0.0.0.0`, `MCP_PORT=8000` are pre-configured

### Adding New MCP Tools
1. Add mapping to `SplitwiseClient.METHOD_MAP` if not already present
2. Add tool function in `app/main.py` with `@mcp.tool()` decorator
3. Use `await _call_splitwise_tool(ctx, "method_name", **args)` for Splitwise API calls
4. Add tests to `tests/test_mcp_pure.py`

### Adding Custom Helpers
1. Implement async function in `custom_methods.py` taking `SplitwiseClient` parameter  
2. Add MCP tool in `main.py` that calls the custom method
3. Create Pydantic model in `models.py` if complex parameter validation needed

## Testing & Debugging

### Test Architecture
The project includes comprehensive testing at multiple levels:

- **Unit Tests** (`tests/`) - Mock-based testing of all modules (76 tests)
- **Integration Tests** (`tests/integration/`) - End-to-end tests against live Splitwise API
- **MCP Server Tests** (`tests/test_mcp_pure.py`) - Comprehensive MCP tool and resource testing
- **Test Coverage** - Comprehensive coverage reporting with pytest-cov

### Running Tests
```bash
# Unit tests only (safe, uses mocks)
make unit-test

# Integration tests (requires SPLITWISE_API_KEY, creates/deletes test group)
make integration-test

# All tests with coverage
make unit-test-coverage

# Full test suite
make test-full
```

### Integration Test Behavior
Integration tests create a temporary test group in your Splitwise account:
- Group name: `MCP_Test_Group_{timestamp}`
- Creates real expenses for testing
- Automatically cleans up all created data
- Requires valid `SPLITWISE_API_KEY` in environment

### Code Quality Tools
- **Ruff** - Modern Python linter and formatter (replaces Black, isort, flake8)
- **MyPy** - Static type checking (optional)
- **pytest** - Test framework with asyncio support

### Development Tools
- **MCP Inspector**: `uv run mcp dev app.main` for interactive testing
- **Stdio Communication**: Direct MCP protocol via stdin/stdout
- **Database Logging**: All operations logged to MongoDB with timestamps
- **Error Patterns**: MCP protocol errors, SDK validation errors, Splitwise API errors

### CI/CD Pipeline
- **GitHub Actions** - Automated testing on all pushes and PRs
- **Multi-Python** - Tests against Python 3.11 and 3.12
- **Docker Build** - Validates container builds
- **Integration Tests** - Optional integration testing on main branch (requires secrets)

## Code Style & Standards

### Python Style Guidelines
This project follows strict code style standards enforced by **Ruff** (replacing Black, isort, flake8):

**Key Style Rules:**
- **Line Length**: 88 characters (Black-compatible)
- **Quotes**: Double quotes for strings (`"hello"` not `'hello'`)
- **Indentation**: 4 spaces (no tabs)
- **Import Organization**: Ruff isort with known first-party (`app`) and third-party packages
- **Type Annotations**: Python 3.11+ style with `from __future__ import annotations`
- **Trailing Commas**: Magic trailing commas respected (auto-formatted)

**Specific Patterns Used:**
```python
# Future annotations import (always first in new files)
from __future__ import annotations

# Type hints with Union style (not | syntax for compatibility)
from typing import Any, Dict, List, Optional

# Double quotes consistently
message: str = "This is the project standard"

# Descriptive docstrings with triple double quotes
"""This is a module docstring.

Provides functionality for X, Y, and Z operations.
"""

# Exception handling with specific error types
try:
    result = some_operation()
except ValueError as exc:
    raise HTTPException(status_code=400, detail=str(exc)) from exc
```

### Testing Patterns
**Unit Test Structure:**
```python
class TestClassName:
    """Test class functionality."""
    
    def test_method_name_success(self):
        """Test successful operation."""
        # Arrange, Act, Assert pattern
        
    @pytest.mark.asyncio
    async def test_async_method(self):
        """Test async functionality."""
        
    def test_error_condition(self):
        """Test error handling."""
        with pytest.raises(ValueError, match="specific error message"):
            # Test code
```

**Mock Patterns:**
```python
# Combined context managers with parentheses (not nested with)
with (
    patch("app.main.asyncio.to_thread") as mock_to_thread,
    patch("app.main.insert_document"),
    patch("app.main.log_operation"),
):
    # Test implementation
```

**MCP Testing Patterns:**
```python
@pytest.fixture
def mock_context(mock_splitwise_client):
    """Mock MCP Context object."""
    context = Mock()
    context.request_context.lifespan_context = {"client": mock_splitwise_client}
    return context

@pytest.mark.asyncio
async def test_mcp_tool(mock_context):
    """Test MCP tool functionality."""
    from app.main import my_tool
    
    with (
        patch("app.main.asyncio.to_thread") as mock_to_thread,
        patch("app.main.insert_document"),
        patch("app.main.log_operation"),
    ):
        result = await my_tool("test_param", mock_context)
        assert result == {"converted": "data"}
```

### MCP Development Patterns
**Tool Implementation:**
```python
@mcp.tool()
async def my_tool(param: str, ctx: Context) -> dict[str, Any]:
    """Tool description for AI agents."""
    return await _call_splitwise_method(ctx, "method_name", param=param)
```

**Resource Implementation:**
```python
@mcp.resource("splitwise://resource/{name}")
async def my_resource(name: str, ctx: Context) -> str:
    """Resource description."""
    client = ctx.request_context.lifespan_context["client"]
    result = client.some_method(name)
    return str(client.convert(result))
```

**Lifespan Management:**
```python
@asynccontextmanager
async def mcp_lifespan(server: Server):
    """MCP server lifespan with SplitwiseClient initialization."""
    # Setup code - initialize client
    yield {"client": client}
    # Cleanup code if needed
```

### Database Patterns
**MongoDB Operations:**
```python
# Always add timestamps to documents
document = {**document, "timestamp": datetime.now(UTC)}
result = db[collection].insert_one(document)

# Consistent query patterns
def find_latest(collection: str) -> dict[str, Any] | None:
    """Return most recent document by timestamp."""
    db = get_db()
    return db[collection].find_one(sort=[("timestamp", -1)])
```

### Pydantic Model Patterns
```python
class RequestModel(BaseModel):
    field_name: str = Field(..., description="Clear field description")
    optional_field: str | None = None
    
    @field_validator("field_name")
    @classmethod
    def validate_field(cls, v: str) -> str:
        """Validate and transform field value."""
        return v.upper()  # Example transformation
```

### Async/Threading Patterns
**Splitwise SDK Integration:**
```python
# Always use asyncio.to_thread for synchronous SDK calls
result = await asyncio.to_thread(client.call_mapped_method, method_name, **args)

# Consistent client access pattern
client: SplitwiseClient = request.app.state.client
```

### File Organization Standards
**Module Structure:**
- `app/main.py` - Entry point and MCP server implementation
- `app/models.py` - Pydantic schemas only  
- `app/splitwise_client.py` - SDK wrapper and method mapping
- `app/custom_methods.py` - Business logic functions (async)
- `app/db.py` - Database utilities (sync functions)
- `app/utils.py` - Pure utility functions
- `app/logging_utils.py` - Logging helpers

**Import Organization:**
```python
# Standard library imports
from __future__ import annotations
import asyncio
import os
from typing import Any

# Third-party imports  
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel

# Local imports
from . import custom_methods
from .db import find_latest, insert_document
from .models import RequestModel
```

### Error Handling Philosophy
- **Be Specific**: Use appropriate MCP error types (tool errors, validation errors, resource errors)
- **Preserve Context**: Use `raise ... from exc` to maintain exception chains
- **Log Everything**: All operations logged with context for debugging
- **Fail Fast**: Validate inputs early and return clear error messages

### Documentation Standards
- **Docstrings**: Triple double quotes, clear descriptions
- **Type Hints**: All functions and methods fully typed
- **Comments**: Explain WHY, not WHAT (code should be self-documenting)
- **Examples**: Include usage examples in complex docstrings

### Makefile Usage
Always use Makefile commands for consistency:
- `make dev` - Start development server
- `make test-all` - Run all checks and unit tests
- `make ci-full` - Complete CI pipeline with integration tests
- `make format` - Format code (before committing)
- `make lint-fix` - Fix linting issues automatically