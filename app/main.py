"""Main FastAPI application for the Splitwise MCP service."""

from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from . import custom_methods
from .db import find_latest, get_db, insert_document
from .logging_utils import log_operation
from .mcp_server import mcp
from .models import (
    AddExpenseEqualSplitRequest,
    GenericResponse,
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

# Mount the official MCP server at /mcp path
app.mount("/mcp", mcp.streamable_http_app())


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
