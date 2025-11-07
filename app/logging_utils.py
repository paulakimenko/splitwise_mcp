"""Logging utilities with PII masking for privacy compliance.

This module provides structured logging using Python's standard logging
library with automatic masking of Personally Identifiable Information (PII)
such as user names and email addresses.

MongoDB logging is deprecated in favor of standard stdout/stderr logging.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from typing import Any

# Configure standard Python logger using root logger for visibility
# Using root logger ensures logs appear in all environments (local, Docker, remote)
logger = logging.getLogger("splitwise_mcp")
logger.setLevel(logging.INFO)
logger.propagate = False  # Disable propagation to avoid duplicate logs

# Add stdout handler if not already configured
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "[%(asctime)s] SPLITWISE - %(levelname)s - %(message)s",
        datefmt="%m/%d/%y %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Force flush to ensure logs appear immediately
handler.flush = lambda: sys.stdout.flush()

# PII field patterns to mask
PII_FIELDS = {
    "first_name",
    "last_name",
    "email",
    "user_email",
    "user_first_name",
    "user_last_name",
}

# Email regex pattern for additional email detection
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")


def mask_email(email: str) -> str:
    """Mask an email address, preserving domain for debugging.

    Example: john.doe@example.com -> j***@example.com
    """
    if not email or "@" not in email:
        return email

    local, domain = email.split("@", 1)
    masked_local = "*" if len(local) <= 1 else local[0] + "***"

    return f"{masked_local}@{domain}"


def mask_name(name: str) -> str:
    """Mask a person's name.

    Example: John Doe -> J*** D***
    """
    if not name or len(name) <= 1:
        return "***"

    # If it's a multi-word name, mask each part
    if " " in name:
        parts = name.split()
        return " ".join(part[0] + "***" if len(part) > 1 else "***" for part in parts)

    return name[0] + "***"


def mask_pii_in_string(text: str) -> str:
    """Mask email addresses found in strings."""
    return EMAIL_PATTERN.sub(lambda m: mask_email(m.group(0)), text)


def mask_pii(data: Any) -> Any:
    """Recursively mask PII fields in data structures.

    Masks first_name, last_name, and email fields in dictionaries,
    and processes nested structures (lists, dicts).

    Parameters
    ----------
    data : Any
        The data structure to mask (dict, list, or primitive)

    Returns
    -------
    Any
        A copy of the data with PII fields masked
    """
    if isinstance(data, dict):
        masked = {}
        for key, value in data.items():
            # Check if this is a PII field
            if key in PII_FIELDS:
                if key == "email" or key.endswith("_email"):
                    masked[key] = mask_email(str(value)) if value else value
                elif "name" in key:
                    masked[key] = mask_name(str(value)) if value else value
                else:
                    masked[key] = "***"
            else:
                # Recursively mask nested structures
                masked[key] = mask_pii(value)
        return masked

    elif isinstance(data, list):
        return [mask_pii(item) for item in data]

    elif isinstance(data, str):
        # Mask any email addresses found in strings
        return mask_pii_in_string(data)

    else:
        # Return primitives as-is
        return data


def log_operation(
    endpoint: str,
    method: str,
    params: dict[str, Any] | None,
    response: Any,
    error: str | None = None,
) -> None:
    """Log an operation with PII masking to standard output.

    This function replaces the previous MongoDB-based logging with
    standard Python logging to stdout. All PII fields (names, emails)
    are automatically masked for privacy compliance.

    Parameters
    ----------
    endpoint : str
        The path or logical name of the invoked endpoint (e.g. 'list_groups').
    method : str
        The operation type (e.g. "TOOL_CALL", "RESOURCE_READ", "CACHE_HIT").
    params : dict | None
        The request parameters. PII fields will be masked.
    response : Any
        The response data. PII fields will be masked.
    error : str | None
        Optional error message if an exception occurred.
    """
    try:
        # Mask PII in params and response
        masked_params = mask_pii(params) if params else None
        masked_response = mask_pii(response)

        # Build log entry
        log_entry = {
            "endpoint": endpoint,
            "method": method,
            "params": masked_params,
            "error": error,
        }

        # Add response summary (avoid logging huge responses)
        if isinstance(masked_response, dict):
            # For dict responses, log structure info
            log_entry["response_keys"] = list(masked_response.keys())
            if "error" in masked_response or "errors" in masked_response:
                log_entry["response_error"] = masked_response.get(
                    "error"
                ) or masked_response.get("errors")
        elif isinstance(masked_response, list):
            log_entry["response_count"] = len(masked_response)
        else:
            log_entry["response_type"] = type(masked_response).__name__

        # Create human-readable summary for visibility
        summary_parts = [f"{method}"]
        if endpoint:
            summary_parts.append(f"endpoint={endpoint}")
        if masked_params:
            param_summary = ", ".join(
                f"{k}={v}" for k, v in list(masked_params.items())[:3]
            )
            if len(masked_params) > 3:
                param_summary += "..."
            summary_parts.append(f"params=({param_summary})")
        if error:
            summary_parts.append(f"ERROR: {error}")

        summary = " | ".join(summary_parts)

        # Log with both human-readable summary and full JSON
        log_message = f"{summary} | {json.dumps(log_entry)}"

        # Log based on error status
        if error:
            logger.error(log_message)
        else:
            logger.info(log_message)

    except Exception as logging_exc:
        # If logging fails, report to stderr without breaking the operation
        logger.exception(f"Failed to log operation {endpoint} {method}: {logging_exc}")
