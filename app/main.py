"""Pure MCP server implementation using only the official MCP Python SDK.

This module provides a complete MCP server using the official Python SDK,
categorizing Splitwise API methods as resources (GET) or tools (POST).
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager, suppress
from typing import Any
from urllib.parse import unquote

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations

from . import custom_methods
from .cached_splitwise_client import CachedSplitwiseClient
from .logging_utils import log_operation


@asynccontextmanager
async def mcp_lifespan(server: FastMCP):
    """Manage MCP server startup and shutdown lifecycle."""
    # Initialize Splitwise client on startup
    api_key = os.environ.get("SPLITWISE_API_KEY")
    consumer_key = os.environ.get("SPLITWISE_CONSUMER_KEY")
    consumer_secret = os.environ.get("SPLITWISE_CONSUMER_SECRET")

    if api_key:
        client = CachedSplitwiseClient(api_key=api_key)
    elif consumer_key and consumer_secret:
        client = CachedSplitwiseClient(
            consumer_key=consumer_key, consumer_secret=consumer_secret
        )
    else:
        raise ValueError(
            "Either SPLITWISE_API_KEY or SPLITWISE_CONSUMER_KEY/SECRET must be set"
        )

    try:
        yield {"client": client}
    finally:
        # Cleanup if needed
        pass


# Create MCP server with lifespan management
mcp = FastMCP("Splitwise MCP Server", lifespan=mcp_lifespan)


async def _call_splitwise_resource(
    ctx: Context, method_name: str, **kwargs: Any
) -> str:
    """Helper function for MCP resources - returns string content."""
    client = ctx.request_context.lifespan_context["client"]

    try:
        result = await asyncio.to_thread(
            client.call_mapped_method, method_name, **kwargs
        )
        response_data = client.convert(result)

        return json.dumps(response_data)
    except Exception as exc:
        with suppress(Exception):
            log_operation(method_name, "ERROR", kwargs, {"error": str(exc)})
        raise


async def _call_splitwise_tool(
    ctx: Context, method_name: str, **kwargs: Any
) -> dict[str, Any]:
    """Helper function for MCP tools - returns structured data."""
    client = ctx.request_context.lifespan_context["client"]

    try:
        result = await asyncio.to_thread(
            client.call_mapped_method, method_name, **kwargs
        )
        response_data = client.convert(result)

        # Ensure response is always a dictionary for MCP tool compatibility
        if not isinstance(response_data, dict):
            # If response is a list, wrap it in a dict
            if isinstance(response_data, list):
                response_data = {"items": response_data}
            else:
                # For other types (primitives), wrap in a dict
                response_data = {"result": response_data}

        return response_data
    except Exception as exc:
        with suppress(Exception):
            log_operation(method_name, "ERROR", kwargs, {"error": str(exc)})
        raise


# MCP Resources for GET methods (read-only data access)


@mcp.resource("splitwise://current_user")
async def current_user_resource(ctx: Context) -> str:
    """Get current authenticated user information as a resource."""
    return await _call_splitwise_resource(ctx, "get_current_user")


@mcp.resource("splitwise://groups")
async def groups_resource(ctx: Context) -> str:
    """List all groups for the current user as a resource."""
    return await _call_splitwise_resource(ctx, "list_groups")


@mcp.resource("splitwise://group/{group_id}")
async def group_resource(group_id: str, ctx: Context) -> str:
    """Get details of a specific group by ID or name as a resource."""
    # Try to parse as integer (group ID) first
    try:
        return await _call_splitwise_resource(ctx, "get_group", id=int(group_id))
    except ValueError:
        # If not an integer, treat as group name
        client = ctx.request_context.lifespan_context["client"]
        # URL decode the name in case it contains special characters
        decoded_name = unquote(group_id)
        group = client.get_group_by_name(decoded_name)
        if group is None:
            raise ValueError(f"Group not found: {decoded_name}") from None
        response_data = client.convert(group)

        return json.dumps(response_data)


@mcp.resource("splitwise://expenses")
async def expenses_resource(ctx: Context) -> str:
    """List all expenses for the current user as a resource."""
    return await _call_splitwise_resource(ctx, "list_expenses")


@mcp.resource("splitwise://expense/{expense_id}")
async def expense_resource(expense_id: str, ctx: Context) -> str:
    """Get details of a specific expense by ID as a resource."""
    return await _call_splitwise_resource(ctx, "get_expense", id=int(expense_id))


@mcp.resource("splitwise://friends")
async def friends_resource(ctx: Context) -> str:
    """List all friends for the current user as a resource."""
    return await _call_splitwise_resource(ctx, "list_friends")


@mcp.resource("splitwise://friend/{friend_id}")
async def friend_resource(friend_id: str, ctx: Context) -> str:
    """Get details of a specific friend by ID as a resource."""
    return await _call_splitwise_resource(ctx, "get_friend", id=int(friend_id))


@mcp.resource("splitwise://categories")
async def categories_resource(ctx: Context) -> str:
    """List all expense categories as a resource."""
    return await _call_splitwise_resource(ctx, "list_categories")


@mcp.resource("splitwise://currencies")
async def currencies_resource(ctx: Context) -> str:
    """List all supported currencies as a resource."""
    return await _call_splitwise_resource(ctx, "list_currencies")


@mcp.resource("splitwise://exchange_rates")
async def exchange_rates_resource(ctx: Context) -> str:
    """Get current exchange rates as a resource."""
    return await _call_splitwise_resource(ctx, "get_exchange_rates")


@mcp.resource("splitwise://notifications")
async def notifications_resource(ctx: Context) -> str:
    """List notifications as a resource."""
    return await _call_splitwise_resource(ctx, "list_notifications")


# MCP Tools for ChatGPT Connector Compatibility (REQUIRED)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def search(query: str, ctx: Context) -> dict[str, Any]:
    """Search across Splitwise data (expenses, groups, friends) based on query.

    This tool is REQUIRED for ChatGPT connectors.
    Returns a list of search results with id, title, and url for each match.
    """
    client = ctx.request_context.lifespan_context["client"]
    results = []

    try:
        # Search in groups
        groups_data = await asyncio.to_thread(client.call_mapped_method, "list_groups")
        groups = client.convert(groups_data)
        if isinstance(groups, list):
            for group in groups:
                if query.lower() in str(group.get("name", "")).lower():
                    results.append(
                        {
                            "id": f"group_{group.get('id')}",
                            "title": f"Group: {group.get('name')}",
                            "url": f"splitwise://group/{group.get('id')}",
                        }
                    )

        # Search in expenses
        expenses_data = await asyncio.to_thread(
            client.call_mapped_method, "list_expenses", limit=100
        )
        expenses = client.convert(expenses_data)
        if isinstance(expenses, list):
            for expense in expenses:
                desc = str(expense.get("description", ""))
                if query.lower() in desc.lower():
                    results.append(
                        {
                            "id": f"expense_{expense.get('id')}",
                            "title": f"Expense: {desc} - ${expense.get('cost', 0)}",
                            "url": f"splitwise://expense/{expense.get('id')}",
                        }
                    )

        # Search in friends
        friends_data = await asyncio.to_thread(
            client.call_mapped_method, "list_friends"
        )
        friends = client.convert(friends_data)
        if isinstance(friends, list):
            for friend in friends:
                name = f"{friend.get('first_name', '')} {friend.get('last_name', '')}".strip()
                if query.lower() in name.lower():
                    results.append(
                        {
                            "id": f"friend_{friend.get('id')}",
                            "title": f"Friend: {name}",
                            "url": f"splitwise://friend/{friend.get('id')}",
                        }
                    )

        # Limit to top 10 results
        results = results[:10]

        # Return in the exact format ChatGPT expects
        return {"results": results}

    except Exception as exc:
        logging.error(f"Search failed: {exc}")
        with suppress(Exception):
            log_operation("search", "ERROR", {"query": query}, {"error": str(exc)})
        raise


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def fetch(id: str, ctx: Context) -> dict[str, Any]:
    """Fetch full details of a specific item by ID.

    This tool is REQUIRED for ChatGPT connectors.
    Returns complete information about a group, expense, or friend.
    """
    client = ctx.request_context.lifespan_context["client"]

    try:
        # Parse the ID to determine type and actual ID
        if id.startswith("group_"):
            actual_id = int(id.replace("group_", ""))
            data = await asyncio.to_thread(
                client.call_mapped_method, "get_group", id=actual_id
            )
            result_data = client.convert(data)

            result = {
                "id": id,
                "title": f"Group: {result_data.get('name')}",
                "text": json.dumps(result_data, indent=2),
                "url": f"splitwise://group/{actual_id}",
                "metadata": {
                    "type": "group",
                    "member_count": len(result_data.get("members", [])),
                },
            }

        elif id.startswith("expense_"):
            actual_id = int(id.replace("expense_", ""))
            data = await asyncio.to_thread(
                client.call_mapped_method, "get_expense", id=actual_id
            )
            result_data = client.convert(data)

            result = {
                "id": id,
                "title": f"Expense: {result_data.get('description')}",
                "text": json.dumps(result_data, indent=2),
                "url": f"splitwise://expense/{actual_id}",
                "metadata": {
                    "type": "expense",
                    "amount": result_data.get("cost"),
                    "currency": result_data.get("currency_code"),
                },
            }

        elif id.startswith("friend_"):
            actual_id = int(id.replace("friend_", ""))
            data = await asyncio.to_thread(
                client.call_mapped_method, "get_friend", id=actual_id
            )
            result_data = client.convert(data)

            name = f"{result_data.get('first_name', '')} {result_data.get('last_name', '')}".strip()
            result = {
                "id": id,
                "title": f"Friend: {name}",
                "text": json.dumps(result_data, indent=2),
                "url": f"splitwise://friend/{actual_id}",
                "metadata": {"type": "friend", "email": result_data.get("email")},
            }
        else:
            raise ValueError(f"Invalid ID format: {id}")

        return result

    except Exception as exc:
        logging.error(f"Fetch failed for {id}: {exc}")
        with suppress(Exception):
            log_operation("fetch", "ERROR", {"id": id}, {"error": str(exc)})
        raise


# MCP Tools for POST methods (actions with side effects)


@mcp.tool()
async def create_expense(
    cost: str,
    description: str,
    ctx: Context,
    group_id: int | None = None,
    currency_code: str = "USD",
    split_equally: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
    """Create a new expense."""
    # Build the expense creation parameters
    params = {
        "cost": cost,
        "description": description,
        "currency_code": currency_code,
        **kwargs,
    }

    if group_id is not None:
        params["group_id"] = group_id
    if split_equally:
        params["split_equally"] = split_equally

    return await _call_splitwise_tool(ctx, "create_expense", **params)


@mcp.tool()
async def create_group(
    name: str, ctx: Context, group_type: str = "other", **kwargs: Any
) -> dict[str, Any]:
    """Create a new group."""
    params = {
        "name": name,
        "group_type": group_type,
        **kwargs,
    }
    return await _call_splitwise_tool(ctx, "create_group", **params)


@mcp.tool()
async def update_expense(
    expense_id: int, ctx: Context, **kwargs: Any
) -> dict[str, Any]:
    """Update an existing expense."""
    return await _call_splitwise_tool(ctx, "update_expense", id=expense_id, **kwargs)


@mcp.tool()
async def delete_expense(expense_id: int, ctx: Context) -> dict[str, Any]:
    """Delete an expense."""
    return await _call_splitwise_tool(ctx, "delete_expense", id=expense_id)


@mcp.tool()
async def create_friend(
    user_email: str,
    user_first_name: str,
    ctx: Context,
    user_last_name: str | None = None,
) -> dict[str, Any]:
    """Add a new friend."""
    params = {
        "user_email": user_email,
        "user_first_name": user_first_name,
    }
    if user_last_name:
        params["user_last_name"] = user_last_name

    return await _call_splitwise_tool(ctx, "create_friend", **params)


@mcp.tool()
async def delete_friend(friend_id: int, ctx: Context) -> dict[str, Any]:
    """Delete a friend relationship."""
    return await _call_splitwise_tool(ctx, "delete_friend", id=friend_id)


@mcp.tool()
async def add_user_to_group(
    group_id: int, ctx: Context, user_id: int | None = None, **kwargs: Any
) -> dict[str, Any]:
    """Add a user to a group."""
    params = {"group_id": group_id, **kwargs}
    if user_id is not None:
        params["user_id"] = user_id

    return await _call_splitwise_tool(ctx, "add_user_to_group", **params)


@mcp.tool()
async def remove_user_from_group(
    group_id: int, user_id: int, ctx: Context
) -> dict[str, Any]:
    """Remove a user from a group."""
    return await _call_splitwise_tool(
        ctx, "remove_user_from_group", group_id=group_id, user_id=user_id
    )


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_monthly_expenses(
    group_name: str, month: str, ctx: Context
) -> dict[str, Any]:
    """Get all expenses for a specific group and month."""
    client = ctx.request_context.lifespan_context["client"]
    try:
        expenses = await custom_methods.expenses_by_month(client, group_name, month)

        return {"expenses": expenses, "count": len(expenses)}
    except Exception as exc:
        with suppress(Exception):
            log_operation(
                "get_monthly_expenses",
                "ERROR",
                {"group_name": group_name, "month": month},
                {"error": str(exc)},
            )
        raise


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def generate_monthly_report(
    group_name: str, month: str, ctx: Context
) -> dict[str, Any]:
    """Generate a detailed monthly expense report for a group."""
    client = ctx.request_context.lifespan_context["client"]
    try:
        report = await custom_methods.monthly_report(client, group_name, month)

        return report
    except Exception as exc:
        with suppress(Exception):
            log_operation(
                "generate_monthly_report",
                "ERROR",
                {"group_name": group_name, "month": month},
                {"error": str(exc)},
            )
        raise


# MCP Tools for GET methods (read operations for testing compatibility)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_current_user(ctx: Context) -> dict[str, Any]:
    """Get current authenticated user information."""
    return await _call_splitwise_tool(ctx, "get_current_user")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def list_groups(ctx: Context) -> dict[str, Any]:
    """List all groups for the current user."""
    return await _call_splitwise_tool(ctx, "list_groups")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_group(group_id: int, ctx: Context) -> dict[str, Any]:
    """Get information about a specific group."""
    return await _call_splitwise_tool(ctx, "get_group", id=group_id)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def list_expenses(
    ctx: Context,
    group_id: int | None = None,
    friend_id: int | None = None,
    dated_after: str | None = None,
    dated_before: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> dict[str, Any]:
    """List expenses with optional filters."""
    params = {"limit": limit, "offset": offset}
    if group_id is not None:
        params["group_id"] = group_id
    if friend_id is not None:
        params["friend_id"] = friend_id
    if dated_after is not None:
        params["dated_after"] = dated_after
    if dated_before is not None:
        params["dated_before"] = dated_before

    return await _call_splitwise_tool(ctx, "list_expenses", **params)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_expense(expense_id: int, ctx: Context) -> dict[str, Any]:
    """Get information about a specific expense."""
    return await _call_splitwise_tool(ctx, "get_expense", id=expense_id)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def list_friends(ctx: Context) -> dict[str, Any]:
    """List all friends for the current user."""
    return await _call_splitwise_tool(ctx, "list_friends")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_friend(friend_id: int, ctx: Context) -> dict[str, Any]:
    """Get information about a specific friend."""
    return await _call_splitwise_tool(ctx, "get_friend", id=friend_id)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def list_categories(ctx: Context) -> dict[str, Any]:
    """List all available expense categories."""
    return await _call_splitwise_tool(ctx, "list_categories")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def list_currencies(ctx: Context) -> dict[str, Any]:
    """List all supported currencies."""
    return await _call_splitwise_tool(ctx, "list_currencies")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def get_exchange_rates(ctx: Context) -> dict[str, Any]:
    """Get current exchange rates."""
    return await _call_splitwise_tool(ctx, "get_exchange_rates")


# Additional helper resources


@mcp.resource("splitwise://group/by_name/{name}")
async def group_by_name_resource(name: str, ctx: Context) -> str:
    """Get group information by name as a resource."""
    client = ctx.request_context.lifespan_context["client"]
    # URL decode the name in case it contains special characters
    decoded_name = unquote(name)
    group = client.get_group_by_name(decoded_name)
    if not group:
        raise ValueError(f"Group '{decoded_name}' not found")

    converted = client.convert(group)
    return json.dumps(converted)


@mcp.resource("splitwise://group/{group_id}/expenses")
async def group_expenses_resource(group_id: str, ctx: Context) -> str:
    """Get all expenses for a specific group as a resource."""
    return await _call_splitwise_resource(ctx, "list_expenses", group_id=int(group_id))


# MCP Prompts for common workflows


@mcp.prompt()
def expense_creation_prompt(
    description: str = "Dinner", amount: str = "25.00", group_name: str = "My Group"
) -> str:
    """Generate a prompt for creating a new expense with equal splitting."""
    return f"""Please help me create a new expense in Splitwise with the following details:
- Description: {description}
- Amount: ${amount}
- Group: {group_name}
- Split: Equally among all group members

Use the create_expense tool to add this expense to the specified group."""


@mcp.prompt()
def monthly_report_prompt(group_name: str = "My Group", month: str = "2025-01") -> str:
    """Generate a prompt for creating a monthly expense report."""
    return f"""Please generate a monthly expense report for the following:
- Group: {group_name}
- Month: {month}

1. First, get all expenses for the group using the expenses resource
2. Filter expenses by the specified month
3. Categorize expenses by type
4. Calculate totals per person
5. Provide a summary with insights and recommendations

Format the report in a clear, readable structure with categories, amounts, and analysis."""


@mcp.prompt()
def group_balance_prompt(group_name: str = "My Group") -> str:
    """Generate a prompt for checking group balances and suggesting settlements."""
    return f"""Please analyze the current balance situation for the group '{group_name}':

1. Get the group information using the group resource
2. Show current balances for all members
3. Calculate who owes money and who is owed money
4. Suggest the minimum number of transactions to settle all debts
5. Provide clear payment instructions

Focus on practical next steps for settling up the group expenses."""


@mcp.prompt()
def expense_search_prompt(
    keywords: str = "restaurant", group_name: str = "My Group"
) -> str:
    """Generate a prompt for searching and analyzing specific types of expenses."""
    return f"""Please search and analyze expenses containing '{keywords}' in the group '{group_name}':

1. Get all expenses for the group
2. Filter expenses containing the keywords in description or notes
3. Calculate total amount spent on this category
4. Show expense history and patterns
5. Identify top spending periods and amounts

Provide insights about spending habits in this category."""


# Entry point for running the MCP server
def run_mcp_server():
    """Run the MCP server using the official SDK."""
    # Check environment to determine transport mode
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8000"))

    if transport == "streamable-http":
        # Configure server settings for HTTP transport
        mcp.settings.host = host
        mcp.settings.port = port
        print(
            f"Starting Splitwise MCP server with Streamable HTTP transport on {host}:{port}"
        )
        mcp.run(transport="streamable-http")
    else:
        print("Starting Splitwise MCP server with stdio transport")
        mcp.run()


if __name__ == "__main__":
    run_mcp_server()
