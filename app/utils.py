"""Utility functions for object conversion and date handling."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict


def object_to_dict(obj: Any) -> Any:
    """Recursively convert Splitwise objects into JSON‑serialisable dicts.

    Many objects returned by the `splitwise` library are custom classes
    without a built‑in JSON representation.  This helper attempts to
    traverse such objects and convert them into dictionaries, lists,
    primitives or strings so they can be logged and stored.

    The implementation ignores attributes starting with an underscore
    and callable attributes.  If an attribute cannot be serialised, it
    falls back to `str(value)`.
    """
    # Primitives remain unchanged
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj

    # Lists/tuples
    if isinstance(obj, (list, tuple, set)):
        return [object_to_dict(item) for item in obj]

    # Dictionaries
    if isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items()}

    # Datetime
    if isinstance(obj, datetime):
        return obj.isoformat()

    # Objects with __dict__
    if hasattr(obj, "__dict__"):
        result: Dict[str, Any] = {}
        for attr, value in obj.__dict__.items():
            # Skip private or protected attributes
            if attr.startswith("_"):
                continue
            if callable(value):
                continue
            result[attr] = object_to_dict(value)
        return result

    # Fallback to string representation
    return str(obj)


def month_range(month: str) -> tuple[datetime, datetime]:
    """Given a month in YYYY‑MM format return the start and end datetimes.

    The end datetime is the first moment of the following month.  If the
    provided month string is invalid this function raises a ValueError.
    """
    try:
        start = datetime.strptime(month, "%Y-%m")
    except ValueError:
        raise ValueError("Month must be in 'YYYY-MM' format")
    # Compute end of month by advancing a month
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    return start, end
