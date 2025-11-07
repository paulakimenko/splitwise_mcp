"""Custom helper endpoints built atop Splitwise and the local database.

These functions encapsulate higher-level behaviours described by the
user, such as splitting an expense evenly, filtering expenses by
month, and generating simple reports.  Each helper function receives
a `SplitwiseClient` instance and interacts with the database via
functions from `app.db`.

Many of these operations are read-only and operate on cached data
stored in MongoDB.  When interacting with the Splitwise API
directly (e.g. to create or update an expense) we call methods on
the provided client.
"""

from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Any

from dateutil import parser as date_parser  # type: ignore

from .db import find_all
from .utils import month_range

if TYPE_CHECKING:
    from .splitwise_client import SplitwiseClient


async def expenses_by_month(
    client: SplitwiseClient, group_name: str, month: str
) -> list[dict[str, Any]]:
    """Return expenses from a group for the specified month (YYYY-MM).

    This helper does not call the Splitwise API directly - it reads
    from the cached `list_expenses` collection.  It attempts to
    normalise dates using `dateutil.parser.parse`.  Expenses whose
    date falls within the month and whose group matches the given
    name are returned.
    """
    start, end = month_range(month)
    # Determine group ID by name via Splitwise
    group = client.get_group_by_name(group_name)
    if not group:
        raise ValueError(f"Group '{group_name}' not found")

    # Handle both object attributes and dict-like access
    if hasattr(group, "id"):
        group_id = group.id
    elif isinstance(group, dict):
        group_id = group.get("id")
    else:
        group_id = getattr(group, "id", None)

    if group_id is None:
        raise ValueError(f"Group '{group_name}' does not have an ID")
    # Fetch all cached expense lists
    docs = find_all("list_expenses")
    results: list[dict[str, Any]] = []
    for doc in docs:
        expenses = doc.get("response") or doc.get("data")
        if not expenses:
            continue
        for exp in expenses:
            try:
                if exp.get("group_id") != group_id:
                    continue
                # Some expense objects may have `date` or `created_at`
                date_str = (
                    exp.get("date")
                    or exp.get("created_at")
                    or exp.get("created_at_object")
                )
                if not date_str:
                    continue
                date_obj = date_parser.parse(date_str)
                # Convert to naive datetime for comparison if timezone-aware
                if date_obj.tzinfo is not None:
                    date_obj = date_obj.replace(tzinfo=None)
                if start <= date_obj < end:
                    results.append(exp)
            except Exception:
                continue
    return results


async def monthly_report(
    client: SplitwiseClient, group_name: str, month: str
) -> dict[str, Any]:
    """Generate a simple report of expenses by category for a month.

    This report reads cached expenses from the database, groups them
    by their `category_id` (and optionally `category_name`), sums
    their costs and returns a summary.  It also emits rudimentary
    recommendations, for example highlighting categories with
    unusually high spend.
    """
    expenses = await expenses_by_month(client, group_name, month)
    if not expenses:
        return {
            "summary": {},
            "total": 0,
            "recommendations": ["No expenses found for the given group and month."],
        }
    category_totals: dict[str, float] = defaultdict(float)
    total_cost = 0.0
    for exp in expenses:
        # Cost may be string; convert to float if possible
        cost_str = exp.get("cost") or exp.get("amount")
        try:
            cost = float(cost_str)
        except Exception:
            cost = 0.0
        total_cost += cost
        # Category: prefer nested object names but fall back to id
        cat_name = None
        cat = exp.get("category") or exp.get("category_id")
        if isinstance(cat, dict):
            cat_name = cat.get("name") or cat.get("name_en")
        elif isinstance(cat, str):
            cat_name = cat
        elif cat is not None:
            cat_name = str(cat)
        cat_name = cat_name or "Unknown"
        category_totals[cat_name] += cost
    # Build recommendations: mark categories exceeding 50% of total
    recommendations: list[str] = []
    for cat_name, cost in category_totals.items():
        if total_cost > 0 and cost / total_cost > 0.5:
            recommendations.append(
                f"Expenses in category '{cat_name}' exceed 50% of total amount. Consider reducing spending in this area."
            )
    return {
        "summary": category_totals,
        "total": total_cost,
        "recommendations": recommendations,
    }
