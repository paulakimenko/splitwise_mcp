"""Main FastAPI application for the Splitwise MCP service."""

from __future__ import annotations

import asyncio
import logging
import os
from contextlib import asynccontextmanager, suppress
from typing import Any
from unittest.mock import Mock

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from . import custom_methods, mcp_server
from .db import find_latest, get_db, insert_document
from .logging_utils import log_operation
from .mcp_server import mcp
from .models import (
    AddExpenseEqualSplitRequest,
    GenericResponse,
)
from .splitwise_client import SplitwiseClient

# Import splitwise SDK classes with error handling for optional dependency
try:
    from splitwise.expense import Expense, ExpenseUser  # type: ignore
except ImportError:
    # Handle case where splitwise SDK is not available
    Expense = None  # type: ignore
    ExpenseUser = None  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    api_key = os.environ.get("SPLITWISE_API_KEY")
    consumer_key = os.environ.get("SPLITWISE_CONSUMER_KEY")
    consumer_secret = os.environ.get("SPLITWISE_CONSUMER_SECRET")
    if api_key:
        app.state.client = SplitwiseClient(api_key=api_key)
    elif consumer_key and consumer_secret:
        app.state.client = SplitwiseClient(
            consumer_key=consumer_key, consumer_secret=consumer_secret
        )
    else:
        raise RuntimeError(
            "You must set either SPLITWISE_API_KEY or both SPLITWISE_CONSUMER_KEY and SPLITWISE_CONSUMER_SECRET in the environment"
        )
    yield
    # Shutdown (if needed)


app = FastAPI(title="Splitwise MCP Service", version="0.1.0", lifespan=lifespan)


# Request logging middleware to debug invalid HTTP requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests for debugging invalid request warnings."""
    try:
        # Log basic request info
        logging.info(
            f"Request: {request.method} {request.url.path} from {request.client}"
        )
        response = await call_next(request)
        return response
    except Exception as e:
        logging.error(f"Request processing error: {e}")
        raise


# Allow all CORS origins for ease of testing; adjust as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP MCP endpoints for ChatGPT Developer Mode integration
# These are different from the stdio-based MCP server - they're HTTP REST endpoints


@app.get("/mcp/ping")
async def mcp_ping() -> dict[str, str]:
    """MCP ping endpoint for ChatGPT health checks."""
    return {"status": "pong", "message": "Splitwise MCP server is operational"}


@app.get("/mcp/list_groups")
async def mcp_list_groups(request: Request) -> dict[str, Any]:
    """List all groups via HTTP MCP endpoint for ChatGPT."""
    try:
        client: SplitwiseClient = request.app.state.client
        result = await asyncio.to_thread(client.call_mapped_method, "list_groups")
        response_data = client.convert(result)

        # Persist to database
        try:
            insert_document("list_groups", {"response": response_data})
            log_operation("list_groups", "HTTP_MCP_ENDPOINT", {}, response_data)
        except Exception as db_exc:
            logging.warning(f"Database operation failed for list_groups: {db_exc}")

        return response_data
    except Exception as exc:
        logging.error(f"Error in mcp_list_groups: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/mcp/add_expense")
async def mcp_add_expense(request: Request, payload: dict[str, Any]) -> dict[str, Any]:
    """Add expense via HTTP MCP endpoint for ChatGPT."""
    try:
        client: SplitwiseClient = request.app.state.client

        # Convert payload to the format expected by create_expense
        result = await asyncio.to_thread(
            client.call_mapped_method, "create_expense", **payload
        )
        response_data = client.convert(result)

        # Persist to database
        try:
            insert_document(
                "create_expense", {"request": payload, "response": response_data}
            )
            log_operation("create_expense", "HTTP_MCP_ENDPOINT", payload, response_data)
        except Exception as db_exc:
            logging.warning(f"Database operation failed for create_expense: {db_exc}")

        return response_data
    except Exception as exc:
        logging.error(f"Error in mcp_add_expense: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/mcp/get_expenses")
async def mcp_get_expenses(
    request: Request,
    group_id: int | None = None,
    friend_id: int | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """Get expenses via HTTP MCP endpoint for ChatGPT."""
    try:
        client: SplitwiseClient = request.app.state.client

        # Build parameters
        params = {"limit": limit, "offset": offset}
        if group_id:
            params["group_id"] = group_id
        if friend_id:
            params["friend_id"] = friend_id

        result = await asyncio.to_thread(
            client.call_mapped_method, "list_expenses", **params
        )
        response_data = client.convert(result)

        # Persist to database
        try:
            insert_document(
                "list_expenses", {"request": params, "response": response_data}
            )
            log_operation("list_expenses", "HTTP_MCP_ENDPOINT", params, response_data)
        except Exception as db_exc:
            logging.warning(f"Database operation failed for list_expenses: {db_exc}")

        return response_data
    except Exception as exc:
        logging.error(f"Error in mcp_get_expenses: {exc}")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# ChatGPT Developer Mode manifest
@app.get("/.well-known/ai-plugin.json")
async def get_ai_plugin_manifest() -> dict[str, Any]:
    """Return the AI plugin manifest for ChatGPT Developer Mode discovery."""
    return {
        "schema_version": "v1",
        "name_for_model": "splitwise_mcp",
        "name_for_human": "Splitwise Expense Manager",
        "description_for_model": "Access and manage Splitwise expenses, groups, and friends. Split bills, track expenses, and manage group finances through the Splitwise API.",
        "description_for_human": "Manage your Splitwise expenses and split bills with friends and groups.",
        "auth": {"type": "none"},
        "api": {
            "type": "openapi",
            "url": f"{os.getenv('BASE_URL', 'https://sw-mcp.paulakimenko.xyz')}/openapi.json",
        },
        "logo_url": "https://www.splitwise.com/assets/press/logos/sw.svg",
        "contact_email": "support@example.com",
        "legal_info_url": "https://www.splitwise.com/terms",
    }


# Alternative MCP testing endpoint for development/testing
@app.post("/mcp-test/call-tool")
async def call_mcp_tool_test(
    request: Request, tool_name: str, arguments: dict[str, Any] | None = None
) -> Any:
    """Test endpoint to call MCP tools directly (for testing/development purposes only).

    WARNING: This endpoint uses mock contexts and is intended for development and testing only.
    In production, MCP tools should be called through the proper MCP protocol channels.
    This endpoint may be disabled in production environments.
    """
    # Development guard - check for debug environment
    if (
        os.getenv("DEBUG", "").lower() not in ("1", "true", "yes")
        and os.getenv("ENVIRONMENT", "").lower() == "production"
    ):
        raise HTTPException(
            status_code=404, detail="MCP test endpoints are not available in production"
        )

    if arguments is None:
        arguments = {}

    try:
        # Get the tool function from the MCP server
        tool_functions = {
            "get_current_user": mcp_server.get_current_user,
            "list_groups": mcp_server.list_groups,
            "get_group": mcp_server.get_group,
            "list_expenses": mcp_server.list_expenses,
            "get_expense": mcp_server.get_expense,
            "list_friends": mcp_server.list_friends,
            "get_friend": mcp_server.get_friend,
            "list_categories": mcp_server.list_categories,
            "list_currencies": mcp_server.list_currencies,
            "get_exchange_rates": mcp_server.get_exchange_rates,
            "list_notifications": mcp_server.list_notifications,
        }

        if tool_name not in tool_functions:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        tool_func = tool_functions[tool_name]

        # Create a mock context for the MCP tool using the factory function
        mock_context = _create_mock_mcp_context(request.app.state.client)

        # Call the tool with appropriate arguments
        if tool_name == "get_group":
            result = await tool_func(arguments.get("group_id"), mock_context)
        elif tool_name == "get_expense":
            result = await tool_func(arguments.get("expense_id"), mock_context)
        elif tool_name == "get_friend":
            result = await tool_func(arguments.get("friend_id"), mock_context)
        elif tool_name == "list_expenses":
            result = await tool_func(
                group_id=arguments.get("group_id"),
                friend_id=arguments.get("friend_id"),
                dated_after=arguments.get("dated_after"),
                dated_before=arguments.get("dated_before"),
                ctx=mock_context,
            )
        elif tool_name == "list_notifications":
            result = await tool_func(arguments.get("limit"), mock_context)
        else:
            # Tools that take no arguments
            result = await tool_func(mock_context)

        return {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {"content": [{"type": "text", "text": str(result)}]},
        }

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/mcp-test/list-tools")
async def list_mcp_tools_test() -> Any:
    """Test endpoint to list available MCP tools (for testing/development purposes only).

    WARNING: This endpoint is intended for development and testing only.
    It may be disabled in production environments.
    """
    # Development guard - check for debug environment
    if (
        os.getenv("DEBUG", "").lower() not in ("1", "true", "yes")
        and os.getenv("ENVIRONMENT", "").lower() == "production"
    ):
        raise HTTPException(
            status_code=404, detail="MCP test endpoints are not available in production"
        )
    tools = [
        {
            "name": "get_current_user",
            "description": "Get current authenticated user information",
        },
        {"name": "list_groups", "description": "List all groups for the current user"},
        {"name": "get_group", "description": "Get details of a specific group by ID"},
        {"name": "list_expenses", "description": "List expenses with optional filters"},
        {"name": "get_expense", "description": "Get details of a specific expense"},
        {"name": "list_friends", "description": "List all friends"},
        {"name": "get_friend", "description": "Get details of a specific friend"},
        {"name": "list_categories", "description": "List expense categories"},
        {"name": "list_currencies", "description": "List supported currencies"},
        {"name": "get_exchange_rates", "description": "Get current exchange rates"},
        {"name": "list_notifications", "description": "List notifications"},
    ]

    return {"jsonrpc": "2.0", "id": 1, "result": {"tools": tools}}


@app.get("/health", summary="Health check endpoint")
async def health_check() -> dict[str, Any]:
    """Health check endpoint with database connectivity status."""
    health_status = {
        "status": "healthy",
        "service": "splitwise-mcp",
        "database": "unknown",
    }

    # Check database connectivity
    try:
        db = get_db()
        # Simple ping to test connectivity - get the MongoDB client and ping
        client = db.client
        client.admin.command("ping")
        health_status["database"] = "connected"
    except Exception as exc:
        health_status["database"] = f"disconnected: {str(exc)}"
        health_status["status"] = "degraded"

    return health_status


def get_client(request: Request) -> SplitwiseClient:
    """Dependency to obtain a SplitwiseClient instance stored in app state."""
    return request.app.state.client


def _create_mock_mcp_context(client: SplitwiseClient) -> Any:
    """Create a mock MCP context for testing purposes.

    WARNING: This is for development/testing only and should not be used in production.
    In a real MCP environment, the context is provided by the MCP framework.
    """
    mock_context = Mock()
    mock_context.request_context.lifespan_context = {"client": client}
    return mock_context


# REST endpoints for cached data


@app.get(
    "/groups",
    summary="Return the latest cached list of groups",
)
async def get_groups() -> Any:
    try:
        doc = find_latest("list_groups")
        if not doc:
            return GenericResponse(message="No cached groups found", data=None)
        return doc.get("response") or doc.get("data")
    except Exception as exc:
        return GenericResponse(
            message=f"Database connection error: {str(exc)}", data=None
        )


@app.get(
    "/expenses",
    summary="Return the latest cached list of expenses",
)
async def get_expenses() -> Any:
    try:
        doc = find_latest("list_expenses")
        if not doc:
            return GenericResponse(message="No cached expenses found", data=None)
        return doc.get("response") or doc.get("data")
    except Exception as exc:
        return GenericResponse(
            message=f"Database connection error: {str(exc)}", data=None
        )


@app.get(
    "/friends",
    summary="Return the latest cached list of friends",
)
async def get_friends() -> Any:
    try:
        doc = find_latest("list_friends")
        if not doc:
            return GenericResponse(message="No cached friends found", data=None)
        return doc.get("response") or doc.get("data")
    except Exception as exc:
        return GenericResponse(
            message=f"Database connection error: {str(exc)}", data=None
        )


@app.get(
    "/logs",
    summary="Return the latest 50 log entries",
)
async def get_logs() -> Any:
    try:
        db = get_db()
        logs = list(db["logs"].find().sort("timestamp", -1).limit(50))
        # Convert ObjectId to string for JSON serialisation
        for log in logs:
            if "_id" in log:
                log["_id"] = str(log["_id"])
        return logs
    except Exception as exc:
        return GenericResponse(
            message=f"Database connection error: {str(exc)}", data=[]
        )


# Custom helper endpoints


@app.get(
    "/custom/expenses_by_month",
    summary="List expenses for a group during a given month",
)
async def custom_expenses_by_month(
    request: Request, group_name: str, month: str
) -> Any:
    client: SplitwiseClient = request.app.state.client
    try:
        result = await custom_methods.expenses_by_month(client, group_name, month)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result


@app.get(
    "/custom/monthly_report",
    summary="Generate a category report for a group and month",
)
async def custom_monthly_report(request: Request, group_name: str, month: str) -> Any:
    client: SplitwiseClient = request.app.state.client
    try:
        result = await custom_methods.monthly_report(client, group_name, month)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result


@app.post(
    "/custom/add_expense_equal_split",
    summary="Add an expense split equally between current user and another participant",
)
async def custom_add_expense_equal(
    request: Request, payload: AddExpenseEqualSplitRequest
) -> Any:
    client: SplitwiseClient = request.app.state.client
    # Implementation stub: Creating an expense through the Splitwise
    # SDK requires constructing Expense and ExpenseUser objects.  We
    # attempt to perform these operations and fall back to an error if
    # the SDK is not available or the operation fails.
    try:
        group = client.get_group_by_name(payload.group_name)
        if not group:
            raise ValueError(f"Group '{payload.group_name}' not found")
        group_id = getattr(group, "id", None)
        if group_id is None:
            raise ValueError("Group ID missing")
        participant = client.get_user_from_group(group, payload.participant_name)
        if not participant:
            raise ValueError(
                f"Participant '{payload.participant_name}' not found in group"
            )
        me_id = client.get_current_user_id()
        if me_id is None:
            raise ValueError("Could not determine current user ID")

        # Check if splitwise SDK classes are available
        if Expense is None or ExpenseUser is None:
            raise ValueError("Splitwise SDK is not available")

        expense = Expense()
        expense.setCost(str(payload.amount))
        expense.setDescription(payload.description)
        expense.setGroupId(group_id)
        expense.setCurrencyCode(payload.currency_code)
        # Create two ExpenseUser objects with equal owed shares
        half = float(payload.amount) / 2.0
        u1 = ExpenseUser()
        u1.setId(me_id)
        u1.setPaidShare(str(payload.amount))
        u1.setOwedShare(str(half))
        u2 = ExpenseUser()
        u2.setId(participant.id)
        u2.setPaidShare("0.0")
        u2.setOwedShare(str(half))

        expense.setUsers([u1, u2])
        # Create the expense
        created = await asyncio.to_thread(client.raw_client.createExpense, expense)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    # Convert result and persist
    response_data = client.convert(created)

    # Try to persist to database, but don't fail if database is unavailable
    try:
        insert_document("custom_add_expense_equal_split", {"response": response_data})
        log_operation(
            endpoint="/custom/add_expense_equal_split",
            method="POST",
            params=payload.model_dump(),
            response=response_data,
        )
    except Exception as db_exc:
        # Log database connection issues but continue operation
        logging.warning(
            f"Database operation failed for add_expense_equal_split: {db_exc}"
        )

    return response_data
