# Splitwise MCP Service

This repository contains a **Model Context Protocol (MCP)** server for the
Splitwise API.  The goal of this project is to expose all Splitwise
API methods through both an official MCP server (for AI agents) and REST API 
while persisting the received data into a MongoDB database, logging every 
request/response, and offering REST endpoints to retrieve the cached data.  
Additionally we provide a set of higher‑level helper endpoints to handle common
scenarios such as adding expenses evenly or generating monthly reports.

## Features

* ✅ **Official MCP Server** – implements the Model Context Protocol using
  the [official Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk).
  Provides 10+ MCP tools (`get_current_user`, `list_groups`, `get_group`, 
  `list_expenses`, etc.) and 2 MCP resources (`splitwise://group/{name}`, 
  `splitwise://balance`) for AI agents to interact with Splitwise data.

* ✅ **Splitwise API Integration** – each MCP tool calls the underlying
  Splitwise API via the [`splitwise` Python client](https://github.com/namaggarwal/splitwise),
  stores the returned data in the database, logs the call, and
  responds with a normalised JSON representation of the result.

* ✅ **Database persistence** – results are persisted in MongoDB
  collections named after the API method (e.g. `groups`, `expenses`) along
  with a timestamp.  A separate `logs` collection captures
  metadata about each request/response pair for auditing.

* ✅ **REST endpoints** – in addition to the MCP server, the
  application provides GET endpoints such as `/groups`, `/expenses`,
  etc. which read from MongoDB and return cached data.  These
  endpoints closely mirror Splitwise's own HTTP API but without
  triggering calls to Splitwise – useful for quick lookups or
  offline access.

* ✅ **Custom helper methods** – the server implements richer workflows 
  such as evenly splitting an expense with a specific user, generating 
  category reports for a month, modifying groups or expenses and 
  optimising debt distribution.

* ✅ **Dockerised** – the repository includes a `Dockerfile` and
  `docker-compose.yml` to simplify deployment.  The recommended
  hosting target for production is [Hetzner](https://www.hetzner.com/) or any other
  platform capable of running Docker containers.  See
  **Deployment** below for details.

* ✅ **Comprehensive Testing** – includes 76 unit tests with mocks
  plus integration tests that validate end-to-end functionality against
  the live Splitwise API. Integration tests create temporary test groups
  and clean up automatically.

* ✅ **Modern Development Workflow** – uses Ruff for linting and formatting
  (replacing Black, isort, flake8), comprehensive Makefile for all operations,
  GitHub Actions CI/CD, and proper virtual environment management.

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

# Start development server
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

# Start server
uvicorn app.main:app --reload
```

### Option 3: Docker Development

```bash
# Start full stack with MongoDB
make docker-dev

# Or manually with docker-compose
docker-compose up --build
```

**Access the API**: Open [`http://localhost:8000/docs`](http://localhost:8000/docs) for interactive API documentation.

## Using the MCP Server

The service provides both an MCP server for AI agents and REST endpoints for traditional HTTP clients:

### MCP Protocol Access

The MCP server is available at `http://localhost:8000/mcp` and implements the official Model Context Protocol. AI agents and MCP clients can connect to:

```
http://localhost:8000/mcp
```

**Available MCP Tools:**
- `get_current_user` - Get authenticated user information
- `list_groups` - List all groups for the user
- `get_group` - Get specific group by ID
- `list_expenses` - List expenses (with optional filters)
- `get_expense` - Get specific expense by ID
- `list_friends` - List all friends
- `get_friend` - Get specific friend by ID
- `list_categories` - List expense categories
- `list_currencies` - List supported currencies
- `get_exchange_rates` - Get current exchange rates
- `list_notifications` - List notifications

**Available MCP Resources:**
- `splitwise://group/{name}` - Access group information by name
- `splitwise://balance` - Access current user balance information

**MCP Client Integration:**
AI agents can connect using any MCP-compatible client. The server handles authentication, data persistence, and audit logging automatically. All MCP tool calls maintain the same database persistence and logging as the original HTTP endpoints.

### REST API Access

Traditional HTTP endpoints remain available for direct integration:

- `GET /groups` - Cached groups data
- `GET /expenses` - Cached expenses data  
- `GET /friends` - Cached friends data
- `GET /logs` - Operation audit logs
- `GET /custom/*` - Helper endpoints (see Custom Usage Examples below)

## Deployment

The project is designed for containerised deployment.  An example
`docker-compose.yml` is provided to spin up the FastAPI service
alongside a MongoDB instance.  On Hetzner you can either run this
compose file directly on a cloud server or build/push the Docker
image to your registry and use a managed environment such as
EasyPanel.

**Basic flow for deployment:**

1. Build and push your image:

   ```bash
   docker build -t your-dockerhub-user/splitwise-mcp:latest .
   docker push your-dockerhub-user/splitwise-mcp:latest
   ```

2. Configure your Hetzner/EasyPanel service:

   * Set the container image to `your-dockerhub-user/splitwise-mcp:latest`.
   * Add environment variables:
     - `SPLITWISE_API_KEY` (required) - Your Splitwise API key
     - `MONGO_URI` (optional) - MongoDB connection string (defaults to `mongodb://localhost:27017`)
     - `DB_NAME` (optional) - Database name (defaults to `splitwise`)
   * Expose port **8000** (serves both REST API and MCP server).
   * Optionally run the provided `docker-compose.yml` if you need
     MongoDB on the same host.

3. Point your domain (`https://sw-mcp.paulakimenko.xyz`) to the
   deployed service.  Ensure HTTPS termination is handled by your
   provider or reverse proxy.

## Architecture

The service follows a three-layer architecture:

```
┌─────────────────────────────────────────────┐
│                FastAPI App                  │
├─────────────────────────────────────────────┤
│ MCP Server        │ REST Cache    │ Custom  │
│ (Official SDK)    │ Endpoints     │ Helpers │
│                   │               │         │
│ • Tools (10+)     │ • /groups     │ • /custom/* │
│ • Resources (2)   │ • /expenses   │         │
│ • /mcp            │ • /friends    │         │
├─────────────────────────────────────────────┤
│            Splitwise SDK Client             │
├─────────────────────────────────────────────┤
│     MongoDB Persistence & Audit Logging    │
└─────────────────────────────────────────────┘
```

**Key Components:**
- **MCP Server**: Official MCP SDK implementation for AI agent integration
- **REST Cache Layer**: Read-only endpoints serving cached MongoDB data  
- **Custom Helpers**: Business logic for common expense scenarios
- **Database Persistence**: All MCP operations automatically cached with timestamps
- **Audit Logging**: Complete operation history for debugging and compliance

## Custom Usage Examples

The following examples demonstrate how the MCP server can fulfil
common Splitwise scenarios. Replace `GROUP_NAME`, `USER_NAME`, 
etc. with real values:

| Task | Example Call |
|------|-------------|
| Add expense `AMOUNT CURRENCY` to group `GROUP_NAME` split equally with `USER_NAME` with comment `COMMENT` | `POST /custom/add_expense_equal_split` with body `{ "group_name": "Trip", "amount": 100, "currency_code": "UAH", "participant_name": "John", "description": "Dinner" }` |
| Show expenses in group for a month | `GET /custom/expenses_by_month?group_name=Trip&month=2025-10` |
| Create group and add user | `POST /custom/create_group` with body `{ "name": "Apartment", "user_email": "example@example.com" }` |
| List active groups | `GET /groups` |
| Modify group (simplify_by_default) | `PATCH /custom/update_group` with body `{ "group_id": 12345, "simplify_by_default": true }` |
| Change housing expense amount for a month | `POST /custom/update_expense_amount_by_category` with body `{ "group_name": "Apartment", "month": "2025-10", "category": "rent", "new_amount": 3000 }` |
| Split expense with custom ratios | `POST /custom/split_expense_custom` with body `{ "group_name": "Apartment", "expense_name": "Utilities", "participant_name": "John", "ratio": 3 }` |
| Category report for previous month | `GET /custom/monthly_report?group_name=Apartment&month=2025-09` |

## Development & Testing

### Available Make Commands

```bash
# Development
make setup                    # Full development setup
make dev                     # Start development server
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
make docker-compose-up     # Start services
make docker-compose-down   # Stop services
make docker-dev           # Start dev environment

# CI/CD
make ci                   # Full CI pipeline (unit tests)
make ci-full             # Full CI + integration tests
```

### Testing Strategy

The project includes comprehensive testing:

- **Unit Tests** (76 tests): Fast, mock-based tests covering all modules including MCP server
- **Integration Tests**: End-to-end tests against live Splitwise API and MCP server integration
- **Test Coverage**: Detailed coverage reporting with pytest-cov

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

**Adding MCP Tools:**
1. Add your tool function to `app/mcp_server.py` with `@mcp.tool()` decorator
2. Use `await _call_splitwise_method(ctx, "method_name", **args)` for Splitwise API calls
3. Add corresponding tests to `tests/test_mcp_server.py`
4. Update this README with the new tool in the MCP Tools list
