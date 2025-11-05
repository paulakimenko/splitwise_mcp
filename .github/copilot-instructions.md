# Splitwise MCP Service - Developer Instructions

## Architecture Overview

This is a **FastAPI-based Model Context Protocol (MCP) server** that integrates the Splitwise API with the official Python MCP SDK, providing both MCP tools for AI agents and REST endpoints for traditional clients. The service follows a three-layer architecture:

1. **MCP Server Layer** (`/mcp`) - Official MCP SDK server with tools and resources for AI agent integration
2. **REST Cache Layer** (`/groups`, `/expenses`, etc.) - Read-only endpoints serving cached MongoDB data
3. **Custom Helpers** (`/custom/*`) - Localized business logic for common expense scenarios

### Key Components

- **`app/main.py`** - FastAPI app with route definitions, dependency injection, and MCP server mounting
- **`app/mcp_server.py`** - Official MCP server implementation with tools, resources, and lifespan management
- **`app/splitwise_client.py`** - Wrapper around `splitwise` SDK with method mapping and data conversion
- **`app/custom_methods.py`** - Higher-level business logic (expense filtering, reports)
- **`app/db.py`** - MongoDB utilities with timestamp-based document insertion
- **`app/models.py`** - Pydantic request/response schemas

## Critical Patterns

### Method Mapping Pattern
The core MCP functionality uses `SplitwiseClient.METHOD_MAP` to translate external snake_case names to SDK camelCase methods:
```python
METHOD_MAP = {
    "list_groups": "getGroups",
    "get_expense": "getExpense",
    # ... maps external API to internal SDK
}
```

### Async-over-Sync Pattern  
Splitwise SDK is synchronous, so use `asyncio.to_thread()` for all SDK calls:
```python
result = await asyncio.to_thread(client.call_mapped_method, method_name, **args)
```

### MCP Tool Pattern
All MCP tools use the `_call_splitwise_method` helper for consistent async operations and persistence:
```python
@mcp.tool()
async def get_current_user(ctx: Context) -> dict[str, Any]:
    """Get current authenticated user information."""
    return await _call_splitwise_method(ctx, "get_current_user")

async def _call_splitwise_method(ctx: Context, method_name: str, **kwargs) -> dict[str, Any]:
    """Helper function for MCP tools with consistent async handling and persistence."""
    client = ctx.request_context.lifespan_context["client"]
    result = await asyncio.to_thread(client.call_mapped_method, method_name, **kwargs)
    response_data = client.convert(result)
    insert_document(method_name, {"response": response_data})
    log_operation(method_name, "TOOL_CALL", kwargs, response_data)
    return response_data
```

### Localized Business Logic
Custom endpoints serve common business scenarios with descriptive field names in Pydantic models:
```python
group_name: str = Field(..., description="Group name")
amount: float = Field(..., description="Expense amount")
```

## Development Workflows

### Environment Setup
Required environment variables:
- `SPLITWISE_API_KEY` - Personal API token from Splitwise
- `MONGO_URI` - MongoDB connection (defaults to `mongodb://localhost:27017`)
- `DB_NAME` - Database name (defaults to `splitwise`)

### Quick Start with Makefile
The project includes a comprehensive Makefile for all development operations:

```bash
# Full setup from scratch
make setup                    # Creates venv, installs deps, creates .env

# Development server
make dev                      # Start FastAPI server with reload

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
uvicorn app.main:app --reload
```

### Docker Development
Use `docker-compose.yml` for full stack with MongoDB:
```bash
docker-compose up --build
```

### Adding New MCP Tools
1. Add mapping to `SplitwiseClient.METHOD_MAP` if not already present
2. Add tool function in `app/mcp_server.py` with `@mcp.tool()` decorator
3. Use `await _call_splitwise_method(ctx, "method_name", **args)` for Splitwise API calls
4. Add tests to `tests/test_mcp_server.py`
5. Add REST endpoint in `main.py` if cached access is desired

### Adding Custom Helpers
1. Implement async function in `custom_methods.py` taking `SplitwiseClient` parameter  
2. Add route in `main.py` under `/custom/*` path
3. Create Pydantic model in `models.py` if complex request body needed

## Data Flow Patterns

### Read Operations
1. Client calls `/groups` → `find_latest("list_groups")` → returns cached MongoDB data
2. No Splitwise API calls for GET endpoints (pure cache reads)

### MCP Tool Operations  
1. AI agent calls MCP tool → `_call_splitwise_method()` → `asyncio.to_thread()` → Splitwise API
2. Response auto-persisted to MongoDB with timestamp
3. Operation logged to `logs` collection with "TOOL_CALL" action type

### Custom Workflows
1. Client calls `/custom/add_expense_equal_split` → business logic in `custom_methods.py`
2. Uses `SplitwiseClient` helpers like `get_group_by_name()`, `get_user_from_group()`  
3. Constructs SDK objects (`Expense`, `ExpenseUser`) manually
4. Persists results following standard pattern

## Key Integration Points

### Splitwise SDK Integration
- Uses bearer token authentication (personal API key)
- All complex SDK objects converted via `client.convert()` using `utils.object_to_dict()`
- Group/user lookups use name-based helpers rather than IDs

### MongoDB Integration
- Collections named after MCP method names (`list_groups`, `create_expense`, etc.)
- All documents include `timestamp` field for ordering
- Separate `logs` collection for audit trail

### MCP Server Integration
- Official MCP SDK from modelcontextprotocol/python-sdk
- FastMCP server mounted at `/mcp` path via Starlette mounting
- Context injection provides access to SplitwiseClient via lifespan management
- All MCP operations maintain database persistence and audit logging

### Docker Deployment
- **Pre-built Image**: `paulakimenko/splitwise-mcp:latest` available on Docker Hub
- **Build Process**: Multi-stage build with system dependencies for `pymongo` compilation
- **Registry Configuration**: Set `DOCKER_REGISTRY`, `DOCKER_IMAGE_NAME`, `DOCKER_TAG` in `.env`
- **Service Discovery**: Container names (`mongo:27017`) for docker-compose
- **Development**: Volume mount for development (`./:/app:ro`)
- **Makefile Commands**: `make docker-build`, `make docker-push`, `make docker-build-push`

## Testing & Debugging

### Test Architecture
The project includes comprehensive testing at multiple levels:

- **Unit Tests** (`tests/`) - Mock-based testing of all modules (76 tests)
- **Integration Tests** (`tests/integration/`) - End-to-end tests against live Splitwise API
- **MCP Server Tests** (`tests/test_mcp_server.py`) - Comprehensive MCP tool and resource testing
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
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Logs Endpoint**: `GET /logs` returns recent operation audit trail
- **Health Check**: `GET /health` returns service status with database connectivity details
- **Error Patterns**: 404 for unmapped methods, 400 for SDK errors, 500 for internal errors

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
    from app.mcp_server import my_tool
    
    with (
        patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
        patch("app.mcp_server.insert_document"),
        patch("app.mcp_server.log_operation"),
    ):
        result = await my_tool("test_param", mock_context)
        assert result == {"converted": "data"}
```

### FastAPI Patterns
**Route Definitions:**
```python
@app.post(
    "/endpoint/{param}",
    summary="Clear description",
    responses={
        404: {"description": "Not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal error"},
    },
)
async def endpoint_function(
    request: Request,
    param: str = Path(..., description="Parameter description"),
    body: ModelClass | None = None,
) -> Any:
    """Detailed docstring explaining endpoint functionality."""
```

**Error Handling:**
```python
try:
    result = await asyncio.to_thread(client.method, **args)
except AttributeError as exc:
    log_operation(endpoint, method, params, None, str(exc))
    raise HTTPException(status_code=404, detail=str(exc)) from exc
except Exception as exc:
    log_operation(endpoint, method, params, None, str(exc))
    raise HTTPException(status_code=500, detail=str(exc)) from exc
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

### File Organization Standards
**Module Structure:**
- `app/main.py` - FastAPI app and route definitions only
- `app/mcp_server.py` - MCP server implementation with tools and resources
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
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local imports
from . import custom_methods
from .db import find_latest, insert_document
from .models import RequestModel
```

### Error Handling Philosophy
- **Be Specific**: Use appropriate HTTP status codes (404 for not found, 400 for bad input, 500 for internal errors)
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