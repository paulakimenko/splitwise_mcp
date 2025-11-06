# Splitwise MCP Server Usage

This project provides a Model Context Protocol (MCP) server for Splitwise expense management.

## Running the MCP Server

### Method 1: Direct Python Execution
```bash
# Set environment variables
export SPLITWISE_API_KEY="your_api_key_here"
export MONGO_URI="mongodb://localhost:27017"
export DB_NAME="splitwise"

# Run the MCP server
python -m app.mcp_server
```

### Method 2: Using the MCP CLI
```bash
# Install MCP CLI if not already installed
pip install mcp

# Set environment variables in your shell or .env file
export SPLITWISE_API_KEY="your_api_key_here"
export MONGO_URI="mongodb://localhost:27017"  
export DB_NAME="splitwise"

# Run using MCP CLI with the configuration
mcp install ./mcp.json
mcp run splitwise
```

### Method 3: Integration with Claude Desktop or other MCP clients

Add this to your MCP client configuration:

```json
{
  "mcpServers": {
    "splitwise": {
      "command": "python",
      "args": ["-m", "app.mcp_server"],
      "cwd": "/path/to/splitwise_mcp",
      "env": {
        "SPLITWISE_API_KEY": "your_api_key_here",
        "MONGO_URI": "mongodb://localhost:27017",
        "DB_NAME": "splitwise"
      }
    }
  }
}
```

## Available MCP Tools

- `get_current_user`: Get current authenticated user information
- `list_groups`: List all groups for the current user
- `get_group`: Get details of a specific group by ID
- `list_expenses`: List expenses with optional filters
- `get_expense`: Get details of a specific expense by ID
- `list_friends`: List all friends for the current user
- `get_friend`: Get details of a specific friend by ID
- `list_categories`: List all expense categories
- `list_currencies`: List all supported currencies
- `get_exchange_rates`: Get current exchange rates
- `list_notifications`: List notifications with optional limit

## Available MCP Resources

- `splitwise://group/{name}`: Get group information by name

## Testing the MCP Server

```bash
# Test with MCP CLI
echo '{"method": "tools/list"}' | mcp connect ./mcp.json splitwise

# Test a specific tool
echo '{"method": "tools/call", "params": {"name": "list_groups", "arguments": {}}}' | mcp connect ./mcp.json splitwise
```

## FastAPI REST Server

The project also includes a FastAPI REST server for traditional HTTP API access:

```bash
# Run the REST API server
uvicorn app.main:app --reload --port 8000
```

This provides HTTP endpoints at:
- `GET /groups` - List groups (cached)
- `GET /expenses` - List expenses (cached) 
- `GET /friends` - List friends (cached)
- `POST /custom/add_expense_equal_split` - Add expense with equal split
- `GET /health` - Health check
- `GET /logs` - View operation logs

The REST API and MCP server can run simultaneously on different processes.