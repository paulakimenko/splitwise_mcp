# Splitwise MCP Service

This repository contains a **Model Context Protocol (MCP)** server for the
Splitwise API. The goal of this project is to provide a pure MCP SDK implementation
that exposes all Splitwise API methods as MCP tools and resources for AI agents,
while persisting data into a MongoDB database and logging every operation.
Additionally, we provide MCP prompts for higher-level workflows such as expense
management and financial reporting.

## Features

* ✅ **Pure MCP SDK Implementation** – built with the 
  [official Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk) using FastMCP.
  Provides 20+ MCP tools for write operations (`create_expense`, `create_group`, 
  `delete_expense`, etc.), 10+ MCP resources for read operations (`splitwise://current_user`, 
  `splitwise://groups`, `splitwise://expenses/{id}`, etc.), and MCP prompts for complex workflows.

* ✅ **Splitwise API Integration** – comprehensive method mapping covering all Splitwise
  operations via the [`splitwise` Python client](https://github.com/namaggarwal/splitwise).
  Each MCP operation stores data in MongoDB, logs the call, and responds with normalized JSON.

* ✅ **Smart Caching Layer** – intelligent MongoDB-based caching with entity-specific TTLs
  reduces API calls and improves performance. GET operations check cache first (expenses: 5min,
  groups: 60min, categories: 24h), while write operations auto-invalidate affected caches.
  Cache can be disabled via environment variable for testing or real-time requirements.

* ✅ **Database Persistence** – all operations are persisted in MongoDB
  collections named after the API method (e.g. `list_groups`, `create_expense`) with
  timestamps. A separate `logs` collection captures metadata for auditing.

* ✅ **MCP Resources for Read Operations** – GET operations are exposed as MCP resources
  using the `splitwise://` URI scheme. Resources support caching and provide structured
  access to Splitwise data for AI agents.

* ✅ **MCP Tools for Write Operations** – POST/PUT/DELETE operations are exposed as MCP tools
  that modify Splitwise data and update the local cache. Tools include parameter validation
  and error handling.

* ✅ **MCP Prompts for Workflows** – complex multi-step operations like expense reporting,
  debt optimization, and group management are available as MCP prompts that guide AI agents
  through structured workflows.

* ✅ **Dockerized** – single-service Docker container with MongoDB integration.
  Pre-built image available on Docker Hub (`paulakimenko/splitwise-mcp:latest`).
  Includes health checks and graceful database connection handling.

* ✅ **Comprehensive Testing** – 105 unit tests with mocks plus integration tests
  validating MCP server functionality and Splitwise API integration. Tests include
  MCP protocol validation, caching layer verification, and end-to-end workflows.

* ✅ **Modern Development Workflow** – Ruff for linting/formatting, comprehensive
  Makefile for all operations, GitHub Actions CI/CD, and proper MCP SDK patterns.

## Quick Start

### Option 1: Using Makefile (Recommended)

```bash
# Clone the repository
git clone https://your-repo-url.git
cd splitwise_mcp

# Complete setup (creates venv, installs deps, creates .env)
make setup

# Add your Splitwise API key to .env file
# Edit .env and set SPLITWISE_API_KEY=your_actual_key

# Start MCP server
make dev
```

### Option 2: Manual Setup

```bash
# Clone and enter directory
git clone https://your-repo-url.git
cd splitwise_mcp

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Create environment file
cp .env.example .env
# Edit .env and add your SPLITWISE_API_KEY

# Start MCP server
python -m app.main
```

### Option 3: Docker Development

```bash
# Start full stack with MongoDB
make docker-dev

# Or manually with docker-compose
docker-compose up --build
```

**Access the MCP Server**: 
- **Local Development**: The server runs on stdio transport and can be connected to by MCP-compatible clients
- **Docker/Remote**: The server uses Streamable HTTP transport and is accessible at `http://localhost:8000/mcp`
- **Testing**: Use the provided scripts in the `scripts/` directory for both transport modes

### Testing Scripts

The `scripts/` directory contains utility scripts for testing and managing the service:

- **`test_docker_mcp.sh`** - Automated Docker testing workflow that starts services and runs comprehensive tests
- **`test_mcp_docker.py`** - Python script for testing MCP server functionality  
- **`test_mcp_manual.py`** - Manual testing utilities for development

**Quick Test**: `./scripts/test_docker_mcp.sh` (starts Docker services and runs all tests)

See [`scripts/README.md`](scripts/README.md) for detailed documentation.

## Environment Configuration

The service requires minimal environment configuration:

**Required Variables:**
- `SPLITWISE_API_KEY` - Your Splitwise personal API token (get from [splitwise.com](https://secure.splitwise.com/apps))

**Optional Variables:**
- `MONGO_URI` - MongoDB connection string (defaults to `mongodb://localhost:27017`)
- `DB_NAME` - Database name (defaults to `splitwise`)
- `MCP_TRANSPORT` - Transport mode: `stdio` (default) or `streamable-http` for remote operation
- `MCP_HOST` - Host to bind to (defaults to `0.0.0.0` for HTTP transport)
- `MCP_PORT` - Port for HTTP transport (defaults to `8000`)
- `CACHE_ENABLED` - Enable/disable caching layer (defaults to `true`)
- `CACHE_TTL_EXPENSES` - Cache TTL for expenses in minutes (defaults to `5`)
- `CACHE_TTL_FRIENDS` - Cache TTL for friends in minutes (defaults to `5`)
- `CACHE_TTL_USERS` - Cache TTL for users in minutes (defaults to `60`)
- `CACHE_TTL_GROUPS` - Cache TTL for groups in minutes (defaults to `60`)
- `CACHE_TTL_CATEGORIES` - Cache TTL for categories in minutes (defaults to `1440`)
- `CACHE_TTL_CURRENCIES` - Cache TTL for currencies in minutes (defaults to `1440`)
- `CACHE_TTL_NOTIFICATIONS` - Cache TTL for notifications in minutes (defaults to `0` - never cache)

**MCP Endpoint Configuration:**
- **Local Development** (stdio): No configuration needed, server runs on stdio transport
- **Docker/Remote** (HTTP): Server automatically runs on HTTP transport at `/mcp` endpoint
  - Default URL: `http://localhost:8000/mcp`
  - The `/mcp` path is the MCP protocol endpoint, not a separate BASE_URL configuration
  - Client connections go to the full URL including the `/mcp` path

**MCP Protocol Notes:**
- The MCP server requires protocol initialization before accepting other requests
- Initialize with protocol version `2024-11-05` and client capabilities
- See integration tests for initialization examples

**Migration Note:** Previous versions used separate `MCP_BASE_URL` environment variable.  
This has been consolidated into the server's HTTP configuration - clients connect directly  
to `http://host:port/mcp` where the `/mcp` path is the MCP endpoint.

## Using the MCP Server

This is a pure MCP SDK implementation that communicates via stdio with MCP-compatible clients:

### MCP Protocol Access

The MCP server supports both local and remote access modes:

**Local Development (stdio):**
```bash
python -m app.main
```

**Remote Access (Streamable HTTP):**
```bash
# Set environment variables for HTTP transport
export MCP_TRANSPORT=streamable-http
export MCP_HOST=0.0.0.0
export MCP_PORT=8000
python -m app.main

# Or use Docker with pre-configured HTTP transport
docker-compose up --build
# Server accessible at http://localhost:8000/mcp
```

**Available MCP Tools (Write Operations):**
- `create_expense` - Create new expense with custom or equal splits
- `update_expense` - Modify existing expense details  
- `delete_expense` - Delete an expense
- `undelete_expense` - Restore a deleted expense
- `create_group` - Create new group with members
- `delete_group` - Delete a group and all expenses
- `undelete_group` - Restore deleted group
- `add_user_to_group` - Add member to existing group
- `remove_user_from_group` - Remove member from group
- `create_friend` - Add new friend by email
- `create_friends` - Batch add multiple friends
- `delete_friend` - Remove friendship
- `update_user` - Update user profile information
- `create_comment` - Add comment to expense
- `delete_comment` - Delete expense comment

**Available MCP Resources (Read Operations):**
- `splitwise://current_user` - Current authenticated user information
- `splitwise://groups` - List all user's groups
- `splitwise://group/{id}` - Specific group by ID
- `splitwise://expenses` - List user's expenses (with filters)
- `splitwise://expense/{id}` - Specific expense by ID
- `splitwise://friends` - List all friends
- `splitwise://friend/{id}` - Specific friend by ID
- `splitwise://categories` - List expense categories
- `splitwise://currencies` - List supported currencies
- `splitwise://notifications` - List recent notifications
- `splitwise://comments/{expense_id}` - Comments for expense

**Available MCP Prompts (Workflows):**
- `expense_management_workflow` - Guided expense creation and management
- `group_management_workflow` - Complete group setup and member management
- `financial_reporting_workflow` - Generate reports and analyze spending
- `debt_settlement_workflow` - Optimize and settle outstanding balances

**MCP Client Integration:**
AI agents connect via stdio protocol. The server handles Splitwise authentication, MongoDB persistence, and operation logging automatically. All operations maintain audit trails and cache data locally.

### Database Integration

All MCP operations automatically persist data to MongoDB with intelligent caching:

- **Collections**: Named after operations (`list_groups`, `create_expense`, etc.)
- **Timestamps**: All documents include creation timestamps for cache validation
- **Audit Logging**: Separate `logs` collection tracks all operations
- **Smart Caching**: Entity-specific TTLs reduce API calls:
  - Expenses & Friends: 5 minutes (frequently changing data)
  - Users & Groups: 60 minutes (moderately stable data)
  - Categories & Currencies: 24 hours (static data)
  - Notifications: Never cached (always fresh)
- **Cache Invalidation**: Write operations automatically invalidate related caches
  - Creating/updating/deleting expenses invalidates expense cache
  - Group operations invalidate group and member caches
  - Friend operations invalidate friend cache
- **Graceful Degradation**: Server continues operation if database is unavailable
- **Cache Control**: Set `CACHE_ENABLED=false` to disable caching entirely

### Example MCP Interactions

```bash
# Using MCP CLI tools or compatible client
mcp connect stdio python -m app.main

# Resources are accessed via URI scheme
mcp get splitwise://current_user
mcp get splitwise://groups
mcp get splitwise://expenses?group_id=12345

# Tools are called with parameters
mcp call create_expense '{"description": "Lunch", "cost": "25.50", "group_id": 123, "split_equally": true}'
mcp call create_group '{"name": "Trip 2025", "group_type": "trip"}'
```

## Deployment

The project is designed for containerized deployment as a pure MCP server with **Streamable HTTP transport** for remote access. An example `docker-compose.yml` is provided to run the MCP service alongside MongoDB. The server supports both stdio (local) and HTTP (remote) transports, making it suitable for integration with AI agent platforms and MCP-compatible clients from any machine.

### Using Pre-built Docker Image

The service is available as a pre-built Docker image on Docker Hub:

```bash
# Pull and run the latest image with MongoDB
docker-compose up -d

# Or run the MCP server directly
docker run --env-file .env paulakimenko/splitwise-mcp:latest
```

**Available Docker Image:**
- **Registry**: `paulakimenko/splitwise-mcp:latest`
- **Base**: Python 3.11 slim
- **Protocol**: MCP via stdio
- **Database**: MongoDB integration with graceful fallback

### Custom Deployment Workflow

1. **Using Makefile (Recommended):**

   ```bash
   # Configure your Docker registry in .env
   echo "DOCKER_REGISTRY=your_dockerhub_username" >> .env
   echo "DOCKER_IMAGE_NAME=splitwise-mcp" >> .env
   
   # Build and push image
   make docker-build-push
   
   # Or build and push separately
   make docker-build
   make docker-push
   ```

2. **Manual Docker Commands:**

   ```bash
   docker build -t your-dockerhub-user/splitwise-mcp:latest .
   docker push your-dockerhub-user/splitwise-mcp:latest
   ```

3. **Configure your MCP client integration:**

   * Set the container image to `paulakimenko/splitwise-mcp:latest` or your custom image.
   * Add environment variables:
     - `SPLITWISE_API_KEY` (required) - Your Splitwise API key
     - `MONGO_URI` (optional) - MongoDB connection string (defaults to `mongodb://localhost:27017`)
     - `DB_NAME` (optional) - Database name (defaults to `splitwise`)
     - `MCP_TRANSPORT=streamable-http` (for Docker/remote) - Enables HTTP transport
     - `MCP_HOST=0.0.0.0` (for Docker/remote) - Binds to all interfaces
     - `MCP_PORT=8000` (for Docker/remote) - HTTP server port
   * **Local Access**: Configure MCP client to connect via stdio: `python -m app.main`
   * **Remote Access**: Configure MCP client to connect via HTTP: `http://localhost:8000/mcp`
   * Use `docker-compose.yml` for pre-configured remote access with MongoDB.

3. **Integration with AI Platforms:**
   
   The MCP server can be integrated with AI agent platforms that support
   the Model Context Protocol. Configure your AI agent to connect either:
   - **Locally**: via stdio transport for same-machine access
   - **Remotely**: via HTTP transport (`http://host:8000/mcp`) for network access

## Architecture

The service follows a pure MCP SDK architecture:

```
┌─────────────────────────────────────────────┐
│        MCP Server (stdio + HTTP)            │
│           FastMCP + Official SDK            │
│    🔌 Local: stdio | Remote: HTTP:8000     │
├─────────────────────────────────────────────┤
│ Resources (GET)   │ Tools (POST)  │ Prompts │
│                   │               │         │
│ • current_user    │ • create_*    │ • expense_mgmt │
│ • groups         │ • update_*    │ • group_mgmt   │
│ • expenses       │ • delete_*    │ • financial    │
│ • friends        │ • add_user    │ • debt_settle  │
├─────────────────────────────────────────────┤
│       CachedSplitwiseClient (Wrapper)       │
│    • Entity-specific TTL caching            │
│    • Automatic cache invalidation           │
│    • MongoDB-backed persistence             │
├─────────────────────────────────────────────┤
│            Splitwise SDK Client             │
│         (Comprehensive Method Map)          │
├─────────────────────────────────────────────┤
│     MongoDB Persistence & Audit Logging    │
│      (Graceful Degradation if Offline)     │
└─────────────────────────────────────────────┘
```

**Key Components:**
- **MCP Server**: Pure FastMCP implementation with dual transport support (stdio/HTTP)
- **Transport Modes**: stdio for local development, Streamable HTTP for remote access
- **Resources**: GET operations via `splitwise://` URI scheme with caching
- **Tools**: POST/PUT/DELETE operations with parameter validation  
- **Prompts**: Complex workflows guiding AI agents through multi-step operations
- **Caching Layer**: CachedSplitwiseClient wrapper with intelligent TTL management
- **Database Persistence**: Automatic caching with timestamps and audit trails
- **Splitwise Integration**: Complete API coverage with method mapping

## MCP Usage Examples

The following examples demonstrate common Splitwise workflows using MCP tools, resources, and prompts:

### Basic Operations

| Task | MCP Command |
|------|-------------|
| Get current user info | `mcp get splitwise://current_user` |
| List all groups | `mcp get splitwise://groups` |
| Get specific group | `mcp get splitwise://group/12345` |
| List expenses | `mcp get splitwise://expenses` |
| Create equal split expense | `mcp call create_expense '{"description": "Dinner", "cost": "50.00", "group_id": 123, "split_equally": true}'` |
| Create custom split expense | `mcp call create_expense '{"description": "Groceries", "cost": "80.00", "group_id": 123, "users__0__user_id": 456, "users__0__paid_share": "80.00", "users__0__owed_share": "40.00", "users__1__user_id": 789, "users__1__paid_share": "0.00", "users__1__owed_share": "40.00"}'` |
| Create new group | `mcp call create_group '{"name": "Weekend Trip", "group_type": "trip"}'` |
| Add friend | `mcp call create_friend '{"user_email": "friend@example.com", "user_first_name": "Jane", "user_last_name": "Doe"}'` |

### Advanced Workflows

| Task | MCP Prompt |
|------|------------|
| Complete expense management | `mcp prompt expense_management_workflow` |
| Full group setup | `mcp prompt group_management_workflow` |
| Generate financial reports | `mcp prompt financial_reporting_workflow` |
| Optimize debt settlement | `mcp prompt debt_settlement_workflow` |

### Resource Filtering

| Task | MCP Resource URI |
|------|------------------|
| Expenses for specific group | `splitwise://expenses?group_id=12345` |
| Expenses in date range | `splitwise://expenses?dated_after=2025-01-01&dated_before=2025-01-31` |
| Friend details | `splitwise://friend/456` |
| Expense comments | `splitwise://comments/78901` |

## Development & Testing

### Available Make Commands

```bash
# Development
make setup                    # Full development setup
make dev                     # Start MCP server
make venv                    # Create virtual environment

# Testing
make unit-test               # Run unit tests (fast, uses mocks)
make integration-test        # Run integration tests (requires API key)
make test-all               # Run checks + unit tests
make test-full              # Run all tests including integration

# Code Quality
make lint                   # Check code with Ruff
make lint-fix              # Auto-fix style issues
make format                # Format code
make check                 # Run all quality checks

# Docker
make docker-build         # Build Docker image
make docker-push          # Push Docker image to registry
make docker-build-push    # Build and push Docker image
make docker-run           # Run Docker container locally
make docker-compose-up    # Start services
make docker-compose-down  # Stop services
make docker-dev          # Start dev environment

# CI/CD
make ci                   # Full CI pipeline (unit tests)
make ci-full             # Full CI + integration tests
```

### Testing Strategy

The project includes comprehensive testing:

- **Unit Tests** (105 tests): Fast, mock-based tests covering all modules including MCP server and caching layer
- **Integration Tests**: End-to-end tests against live Splitwise API and MCP server integration
- **Test Coverage**: Detailed coverage reporting with pytest-cov

**Test Breakdown:**
- Cached Client: 37 tests (initialization, TTL validation, cache operations, invalidation)
- Custom Methods: 10 tests (expense analysis, reporting workflows)
- Database: 9 tests (MongoDB operations, connection handling)
- MCP Server: 14 tests (pure MCP implementation, ChatGPT connector compatibility)
- Models: 8 tests (Pydantic validation)
- Splitwise Client: 18 tests (SDK wrapper, method mapping)
- Transport: 7 tests (stdio/HTTP transport configuration)
- Integration: 16 tests (live API, MCP protocol compliance)

```bash
# Run unit tests (safe, no API calls)
make unit-test

# Run integration tests (creates/deletes test group)
# Requires SPLITWISE_API_KEY in environment
make integration-test
```

### Code Quality Standards

- **Ruff**: Modern linter and formatter (replaces Black, isort, flake8)  
- **MyPy**: Optional static type checking
- **pytest**: Test framework with asyncio support
- **GitHub Actions**: Automated CI/CD on all pushes and PRs

## Contributing

Pull requests are welcome! If you find a bug or want to add additional MCP tools, helper endpoints, or improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Run `make test-full` to verify everything works
5. Submit a pull request

**Code Standards**: 
- Use `make lint-fix` to auto-format code with Ruff
- Add unit tests for new functionality  
- Add integration tests for API endpoints
- For MCP tools: add tests in `tests/test_mcp_server.py`
- Update documentation as needed
- Follow the existing patterns for async operations and database persistence

**Adding MCP Components:**

**Tools (Write Operations):**
1. Add tool function to `app/mcp_server.py` with `@mcp.tool()` decorator
2. Use `await _call_splitwise_method(ctx, "method_name", **args)` for Splitwise API calls
3. Add method mapping to `SplitwiseClient.METHOD_MAP` if needed
4. Add tests to `tests/test_mcp_server.py`

**Resources (Read Operations):**
1. Add resource function with `@mcp.resource("splitwise://path")` decorator
2. Implement caching logic with MongoDB fallback
3. Add URI pattern to resource documentation
4. Add integration tests for resource access

**Prompts (Workflows):**
1. Add prompt function with `@mcp.prompt()` decorator  
2. Design structured workflow with clear steps
3. Reference existing tools and resources
4. Test complete workflow scenarios
