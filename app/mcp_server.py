"""Official MCP server implementation using the MCP SDK.

This module provides a proper MCP server using the official Python SDK,
replacing the custom /mcp/{method_name} proxy routes with native MCP tools.
"""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any

from mcp.server.fastmcp import Context, FastMCP

from .db import insert_document
from .logging_utils import log_operation
from .splitwise_client import SplitwiseClient


@asynccontextmanager
async def mcp_lifespan(server: FastMCP):
    """Manage MCP server startup and shutdown lifecycle."""
    # Initialize Splitwise client on startup
    api_key = os.environ.get("SPLITWISE_API_KEY")
    consumer_key = os.environ.get("SPLITWISE_CONSUMER_KEY")
    consumer_secret = os.environ.get("SPLITWISE_CONSUMER_SECRET")

    if api_key:
        client = SplitwiseClient(api_key=api_key)
    elif consumer_key and consumer_secret:
        client = SplitwiseClient(
            consumer_key=consumer_key, consumer_secret=consumer_secret
        )
    else:
        raise RuntimeError(
            "You must set either SPLITWISE_API_KEY or both SPLITWISE_CONSUMER_KEY and SPLITWISE_CONSUMER_SECRET in the environment"
        )

    try:
        yield {"client": client}
    finally:
        # Cleanup if needed
        pass


# Create MCP server with lifespan management
mcp = FastMCP("Splitwise MCP Server", lifespan=mcp_lifespan)


async def _call_splitwise_method(
    ctx: Context, method_name: str, **kwargs: Any
) -> dict[str, Any]:
    """Helper function to call Splitwise methods with proper error handling and logging."""
    client = ctx.request_context.lifespan_context["client"]

    try:
        result = await asyncio.to_thread(
            client.call_mapped_method, method_name, **kwargs
        )
        response_data = client.convert(result)

        # Persist to database and log operation
        insert_document(method_name, {"response": response_data})
        log_operation(method_name, "TOOL_CALL", kwargs, response_data)

        return response_data
    except Exception as exc:
        log_operation(method_name, "TOOL_CALL", kwargs, None, str(exc))
        raise


# Tool implementations for each Splitwise API method


@mcp.tool()
async def get_current_user(ctx: Context) -> dict[str, Any]:
    """Get current authenticated user information."""
    return await _call_splitwise_method(ctx, "get_current_user")


@mcp.tool()
async def list_groups(ctx: Context) -> dict[str, Any]:
    """List all groups for the current user."""
    return await _call_splitwise_method(ctx, "list_groups")


@mcp.tool()
async def get_group(group_id: int, ctx: Context) -> dict[str, Any]:
    """Get details of a specific group by ID."""
    return await _call_splitwise_method(ctx, "get_group", id=group_id)


@mcp.tool()
async def list_expenses(
    group_id: int | None = None,
    friend_id: int | None = None,
    dated_after: str | None = None,
    dated_before: str | None = None,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """List expenses with optional filters."""
    # Build arguments dict, excluding None values
    args = {}
    if group_id is not None:
        args["group_id"] = group_id
    if friend_id is not None:
        args["friend_id"] = friend_id
    if dated_after is not None:
        args["dated_after"] = dated_after
    if dated_before is not None:
        args["dated_before"] = dated_before

    return await _call_splitwise_method(ctx, "list_expenses", **args)


@mcp.tool()
async def get_expense(expense_id: int, ctx: Context) -> dict[str, Any]:
    """Get details of a specific expense by ID."""
    return await _call_splitwise_method(ctx, "get_expense", id=expense_id)


@mcp.tool()
async def list_friends(ctx: Context) -> dict[str, Any]:
    """List all friends for the current user."""
    return await _call_splitwise_method(ctx, "list_friends")


@mcp.tool()
async def get_friend(friend_id: int, ctx: Context) -> dict[str, Any]:
    """Get details of a specific friend by ID."""
    return await _call_splitwise_method(ctx, "get_friend", id=friend_id)


@mcp.tool()
async def list_categories(ctx: Context) -> dict[str, Any]:
    """List all expense categories."""
    return await _call_splitwise_method(ctx, "list_categories")


@mcp.tool()
async def list_currencies(ctx: Context) -> dict[str, Any]:
    """List all supported currencies."""
    return await _call_splitwise_method(ctx, "list_currencies")


@mcp.tool()
async def get_exchange_rates(ctx: Context) -> dict[str, Any]:
    """Get current exchange rates."""
    return await _call_splitwise_method(ctx, "get_exchange_rates")


@mcp.tool()
async def list_notifications(
    limit: int = 0,
    ctx: Context | None = None,
) -> dict[str, Any]:
    """List notifications with optional limit."""
    args = {}
    if limit > 0:
        args["limit"] = limit

    return await _call_splitwise_method(ctx, "list_notifications", **args)


# Resource for group information by name
@mcp.resource("splitwise://group/{name}")
async def get_group_by_name(name: str, ctx: Context) -> str:
    """Get group information by name."""
    client = ctx.request_context.lifespan_context["client"]
    group = client.get_group_by_name(name)
    if not group:
        return f"Group '{name}' not found"

    converted = client.convert(group)
    return str(converted)


# Resource for user balance information
@mcp.resource("splitwise://balance")
async def get_balance(ctx: Context) -> str:
    """Get current user balance information."""
    client = ctx.request_context.lifespan_context["client"]
    result = client.call_mapped_method("get_current_user")
    converted = client.convert(result)
    return str(converted)


# Entry point for running the MCP server
def run_mcp_server():
    """Run the MCP server using the official SDK."""
    mcp.run()


if __name__ == "__main__":
    run_mcp_server()
