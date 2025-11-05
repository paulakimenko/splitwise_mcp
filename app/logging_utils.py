"""Simple logging utilities for request/response auditing.

Each operation against the Splitwise API or internal logic should be
logged into a dedicated `logs` collection.  The log document
captures the endpoint, HTTP method, parameters, outcome and any
error message.  Timestamps are added automatically.
"""

from __future__ import annotations

from typing import Any

from .db import insert_document


def log_operation(
    endpoint: str,
    method: str,
    params: dict[str, Any] | None,
    response: Any,
    error: str | None = None,
) -> None:
    """Insert a log entry describing an operation.

    Parameters
    ----------
    endpoint: str
        The path or logical name of the invoked endpoint (e.g. `/mcp/list_groups`).
    method: str
        The HTTP method used (e.g. "GET", "POST").
    params: dict | None
        The request body or query parameters sent.  None if no parameters.
    response: Any
        The response data returned to the caller.  Can be JSON serialisable
        or an error description.
    error: str | None
        Optional error message if an exception occurred.
    """
    log_doc: dict[str, Any] = {
        "endpoint": endpoint,
        "method": method,
        "params": params,
        "response": response,
        "error": error,
    }
    insert_document("logs", log_doc)
