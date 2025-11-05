# Splitwise MCP Service - Developer Instructions

## Architecture Overview

This is a **FastAPI-based MCP (Magic Control Panel) proxy service** that wraps the Splitwise API with caching, logging, and Ukrainian-localized helper endpoints. The service follows a three-layer architecture:

1. **MCP Layer** (`/mcp/{method_name}`) - Generic proxy routes that map snake_case names to Splitwise SDK camelCase methods
2. **REST Cache Layer** (`/groups`, `/expenses`, etc.) - Read-only endpoints serving cached MongoDB data
3. **Custom Helpers** (`/custom/*`) - Ukrainian-localized business logic for common expense scenarios

### Key Components

- **`app/main.py`** - FastAPI app with route definitions and dependency injection
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

### Data Persistence Pattern
Every successful MCP call automatically persists results with timestamps:
```python
response_data = client.convert(result)  # Convert SDK objects to dicts
insert_document(method_name, {"response": response_data})  # Store in MongoDB
log_operation(endpoint, method, params, response_data)  # Audit logging
```

### Ukrainian Localization
Custom endpoints serve Ukrainian business scenarios with Ukrainian field descriptions in Pydantic models:
```python
group_name: str = Field(..., description="Назва групи")
amount: float = Field(..., description="Сума витрати")
```

## Development Workflows

### Environment Setup
Required environment variables:
- `SPLITWISE_API_KEY` - Personal API token from Splitwise
- `MONGO_URI` - MongoDB connection (defaults to `mongodb://localhost:27017`)
- `DB_NAME` - Database name (defaults to `splitwise`)

### Local Development
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker Development
Use `docker-compose.yml` for full stack with MongoDB:
```bash
docker-compose up --build
```

### Adding New MCP Methods
1. Add mapping to `SplitwiseClient.METHOD_MAP`
2. Test via `/mcp/{method_name}` endpoint - no code changes needed
3. Add REST endpoint in `main.py` if cached access is desired

### Adding Custom Helpers
1. Implement async function in `custom_methods.py` taking `SplitwiseClient` parameter  
2. Add route in `main.py` under `/custom/*` path
3. Create Pydantic model in `models.py` if complex request body needed

## Data Flow Patterns

### Read Operations
1. Client calls `/groups` → `find_latest("list_groups")` → returns cached MongoDB data
2. No Splitwise API calls for GET endpoints (pure cache reads)

### Write Operations  
1. Client calls `/mcp/create_expense` → `SplitwiseClient.call_mapped_method()` → Splitwise API
2. Response auto-persisted to MongoDB with timestamp
3. Operation logged to `logs` collection

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

### Docker Deployment
- Multi-stage build with system dependencies for `pymongo` compilation
- Service discovery via container names (`mongo:27017`)
- Volume mount for development (`./:/app:ro`)

## Testing & Debugging

- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Logs Endpoint**: `GET /logs` returns recent operation audit trail
- **Health Check**: Any REST endpoint will verify MongoDB connectivity
- **Error Patterns**: 404 for unmapped methods, 400 for SDK errors, 500 for internal errors