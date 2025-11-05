"""Main FastAPI application for the Splitwise MCP service."""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Path, Request, status
from fastapi.middleware.cors import CORSMiddleware

from . import custom_methods
from .db import find_latest, insert_document
from .logging_utils import log_operation
from .models import (
    AddExpenseEqualSplitRequest,
    GenericResponse,
    MCPCallRequest,
)
from .splitwise_client import SplitwiseClient


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

# Allow all CORS origins for ease of testing; adjust as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_client(request: Request) -> SplitwiseClient:
    """Dependency to obtain a SplitwiseClient instance stored in app state."""
    return request.app.state.client


@app.post(
    "/mcp/{method_name}",
    responses={
        404: {"description": "Method not found"},
        400: {"description": "Bad request"},
        500: {"description": "Internal error"},
    },
    summary="Invoke a Splitwise API method via MCP",
)
async def call_mcp_method(
    request: Request,
    method_name: str = Path(..., description="Snake_case name of the method"),
    body: MCPCallRequest | None = None,
) -> Any:
    """
    Generic route to invoke methods on the Splitwise client.  The
    request body must contain a JSON object `args` mapping to the
    parameters expected by the underlying Splitwise SDK method.  The
    result is converted to JSON‑serialisable data and persisted in
    the database under a collection named after `method_name`.
    """
    client: SplitwiseClient = request.app.state.client
    args = body.args if body else {}
    try:
        # Because the Splitwise SDK is synchronous, run in thread
        result = await asyncio.to_thread(client.call_mapped_method, method_name, **args)
    except AttributeError as exc:
        log_operation(
            endpoint=f"/mcp/{method_name}",
            method="POST",
            params=args,
            response=None,
            error=str(exc),
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        log_operation(
            endpoint=f"/mcp/{method_name}",
            method="POST",
            params=args,
            response=None,
            error=str(exc),
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    # Convert complex objects to dicts for storage and response
    response_data = client.convert(result)
    # Persist into database
    insert_document(method_name, {"response": response_data})
    # Log operation
    log_operation(
        endpoint=f"/mcp/{method_name}",
        method="POST",
        params=args,
        response=response_data,
    )
    return response_data


# REST endpoints for cached data


@app.get(
    "/groups",
    summary="Return the latest cached list of groups",
)
async def get_groups() -> Any:
    doc = find_latest("list_groups")
    if not doc:
        return GenericResponse(message="No cached groups found", data=None)
    return doc.get("response") or doc.get("data")


@app.get(
    "/expenses",
    summary="Return the latest cached list of expenses",
)
async def get_expenses() -> Any:
    doc = find_latest("list_expenses")
    if not doc:
        return GenericResponse(message="No cached expenses found", data=None)
    return doc.get("response") or doc.get("data")


@app.get(
    "/friends",
    summary="Return the latest cached list of friends",
)
async def get_friends() -> Any:
    doc = find_latest("list_friends")
    if not doc:
        return GenericResponse(message="No cached friends found", data=None)
    return doc.get("response") or doc.get("data")


@app.get(
    "/logs",
    summary="Return the latest 50 log entries",
)
async def get_logs() -> Any:
    from .db import get_db

    db = get_db()
    logs = list(db["logs"].find().sort("timestamp", -1).limit(50))
    # Convert ObjectId to string for JSON serialisation
    for log in logs:
        if "_id" in log:
            log["_id"] = str(log["_id"])
    return logs


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
        # Import classes from splitwise SDK lazily
        from splitwise.expense import (
            Expense,  # type: ignore
            ExpenseUser,  # type: ignore
        )

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
    insert_document("custom_add_expense_equal_split", {"response": response_data})
    log_operation(
        endpoint="/custom/add_expense_equal_split",
        method="POST",
        params=payload.model_dump(),
        response=response_data,
    )
    return response_data
