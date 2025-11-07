# Logging System Documentation

## Overview

The Splitwise MCP Service uses **standard Python logging** with **automatic PII masking** to ensure privacy compliance while maintaining observability. All logs are written to **stdout** in a structured JSON format, making them compatible with modern log aggregation systems.

## Key Features

### ✅ Privacy-Compliant PII Masking

All sensitive user data is automatically masked before logging:

**Email Masking:**
- Pattern: `"john.doe@example.com"` → `"j***@example.com"`
- Domain preserved for debugging context
- Single-character local parts: `"a@example.com"` → `"*@example.com"`

**Name Masking:**
- Pattern: `"John Doe"` → `"J*** D***"`
- First letter preserved, rest replaced with asterisks
- Multi-word names: Each word masked separately
- Short names: `"Al"` → `"A***"`

**Field-Based Detection:**
Automatically masks these fields in all logged data:
- `first_name`
- `last_name`
- `email`
- `user_email`
- `user_first_name`
- `user_last_name`

**Content-Based Detection:**
Uses regex patterns to find and mask emails in arbitrary text strings.

### ✅ Standard Python Logging

**Configuration:**
```python
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

**Output Format:**
```
2025-01-15 14:30:45 - app.logging_utils - INFO - {"operation": "list_groups", "operation_type": "MCP_TOOL", "masked_params": {...}}
```

**Log Levels:**
- `INFO`: Successful operations
- `ERROR`: Failed operations or API errors

### ✅ Structured JSON Metadata

Each log entry includes:
- `operation`: MCP method name (e.g., "list_groups")
- `operation_type`: Type of operation (e.g., "MCP_TOOL", "API_ERROR", "CACHE_FALLBACK")
- `masked_params`: Request parameters with PII masked
- `response_summary`: Response metadata (keys, count, type) instead of full response
- `error`: Error message if operation failed

**Example Log Entry:**
```json
{
  "operation": "create_expense",
  "operation_type": "MCP_TOOL",
  "masked_params": {
    "description": "Lunch",
    "cost": "25.50",
    "users__0__first_name": "J***",
    "users__0__email": "j***@example.com"
  },
  "response_keys": ["expense"],
  "timestamp": "2025-01-15T14:30:45Z"
}
```

## Implementation Details

### PII Masking Functions

**`mask_email(email: str) -> str`**
- Preserves domain for debugging
- Handles single-character local parts
- Returns invalid emails unchanged

**`mask_name(name: str) -> str`**
- Shows first letter only
- Handles multi-word names
- Short names become "***"

**`mask_pii_in_string(text: str) -> str`**
- Uses `EMAIL_PATTERN` regex
- Finds emails in arbitrary strings
- Applies email masking

**`mask_pii(data: Any) -> Any`**
- Recursive processing for nested structures
- Handles dicts, lists, strings, primitives
- Field-based and content-based detection

### Log Operation Function

**`log_operation(operation: str, operation_type: str, params: dict | None = None, response: Any = None, error: str | None = None) -> None`**

**Behavior:**
- Masks PII in params before logging
- Masks PII in response before logging
- Adds response summaries instead of full response data:
  - Dicts: Logs `response_keys` (list of keys)
  - Lists: Logs `response_count` (number of items)
  - Other: Logs `response_type` (Python type name)
- Uses ERROR level when error parameter is present
- Uses INFO level for successful operations
- Gracefully handles logging failures (never crashes operation)

**Usage Example:**
```python
from app.logging_utils import log_operation

# Successful operation
log_operation(
    operation="create_expense",
    operation_type="MCP_TOOL",
    params={"description": "Lunch", "cost": "25.50"},
    response={"expense": {"id": 12345}}
)

# Failed operation
log_operation(
    operation="list_groups",
    operation_type="API_ERROR",
    params={},
    error="Connection timeout"
)
```

## Migration from MongoDB Logging

**Previous System:**
- Wrote logs to MongoDB `logs` collection
- Used `insert_document("logs", log_doc)`
- No PII masking
- Required MongoDB connection

**Current System:**
- Writes to stdout via Python `logging` module
- Automatic PII masking
- No MongoDB dependency for logging
- Compatible with log aggregation systems

**Breaking Changes:**
- None! The `log_operation()` function signature is unchanged
- All existing code works without modification
- MongoDB is now **optional** (only used for caching)

## Benefits

### 🔒 Privacy & Compliance
- ✅ PII automatically masked in all logs
- ✅ Domain-preserving email masking for debugging
- ✅ First-letter name masking maintains some context
- ✅ Compliant with privacy regulations (GDPR, CCPA)

### 🚀 Operational Simplicity
- ✅ No MongoDB required for logging
- ✅ Standard Python logging (familiar to all developers)
- ✅ Stdout output (compatible with Docker, Kubernetes, etc.)
- ✅ Works with log aggregation systems (Datadog, Splunk, etc.)

### 🔍 Better Debugging
- ✅ Structured JSON logs
- ✅ Response summaries (keys/count/type)
- ✅ Operation type categorization
- ✅ Preserved email domains for issue tracking

### 💪 Zero Regression
- ✅ All existing tests passing
- ✅ Same function signatures
- ✅ Backward compatible
- ✅ No code changes required in existing modules

## Testing

The logging system includes comprehensive test coverage:

**PII Masking Tests (14 tests):**
- Email masking edge cases
- Name masking variations
- Dict, list, and nested structure masking
- String content detection

**Log Operation Tests (9 tests):**
- Success/error logging behavior
- PII masking verification
- Response summary generation
- Exception handling

**Run Tests:**
```bash
# Test logging specifically
pytest tests/test_logging_utils.py -v

# All unit tests
make unit-test

# Full test suite
make test-full
```

## Log Aggregation Integration

The structured JSON logs are compatible with popular log aggregation systems:

**Datadog:**
```bash
# Logs automatically parsed as JSON
# PII already masked, safe for Datadog storage
```

**Splunk:**
```bash
# Use JSON source type
# Logs indexed with structured fields
```

**CloudWatch:**
```bash
# JSON logs parsed automatically
# Create metrics from operation_type field
```

**Elasticsearch/Kibana:**
```bash
# JSON logs indexed as structured documents
# Create visualizations from operation and response_keys
```

## Future Enhancements

Potential improvements for consideration:

- [ ] Configurable masking patterns via environment variables
- [ ] Additional PII field detection (phone numbers, addresses)
- [ ] Log sampling for high-volume environments
- [ ] Configurable log levels per operation type
- [ ] Correlation IDs for request tracing
- [ ] Performance metrics in log metadata
