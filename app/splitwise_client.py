"""Wrapper around the `splitwise` Python SDK.

This class encapsulates initialisation of the Splitwise client and
provides helper methods for the MCP service.  It also exposes a
generic `call_method` which delegates to the underlying SDK methods
based on a mapping from snake_case names to the library's camelCase
method names.  See the README for details.
"""

from __future__ import annotations

import os
from typing import Any, Dict

from splitwise import Splitwise  # type: ignore

from .utils import object_to_dict


class SplitwiseClient:
    """High‑level wrapper for the Splitwise API.

    The client uses a personal API key (from environment variable
    `SPLITWISE_API_KEY`) to authenticate.  Only the bearer‑token
    authentication flow is currently supported.  If you need OAuth
    consumer keys and secrets, extend this class accordingly.
    """

    # Mapping from external MCP method names (snake_case) to
    # Splitwise SDK method names (camelCase).
    METHOD_MAP: Dict[str, str] = {
        "get_current_user": "getCurrentUser",
        "list_groups": "getGroups",
        "get_group": "getGroup",
        "list_expenses": "getExpenses",
        "get_expense": "getExpense",
        "list_friends": "getFriends",
        "get_friend": "getFriend",
        "list_categories": "getCategories",
        "list_currencies": "getCurrencies",
        "get_exchange_rates": "getExchangeRates",
        "list_notifications": "getNotifications",
        "get_balance": "getCurrentUser",  # Not a direct method; see notes
    }

    def __init__(self, api_key: str | None = None) -> None:
        api_key = api_key or os.environ.get("SPLITWISE_API_KEY")
        if not api_key:
            raise ValueError("SPLITWISE_API_KEY environment variable not set")
        # The Splitwise SDK accepts a personal access token directly
        # (without consumer keys) by passing the token as the first
        # argument.  See https://github.com/namaggarwal/splitwise#using-application-access-token
        self._client = Splitwise(api_key)

    @property
    def raw_client(self) -> Splitwise:
        return self._client

    def call_mapped_method(self, method_name: str, **kwargs: Any) -> Any:
        """Call a Splitwise method given an MCP snake_case name.

        Parameters
        ----------
        method_name: str
            Snake_case name used by the MCP route (e.g. "list_groups").
        kwargs: dict
            Arguments to pass to the underlying SDK method.

        Returns
        -------
        Any
            The result of the SDK call.  Complex objects are returned
            as-is; callers should convert them via `object_to_dict`.
        """
        sdk_name = self.METHOD_MAP.get(method_name)
        if not sdk_name:
            raise AttributeError(f"Unsupported method '{method_name}'")
        func = getattr(self._client, sdk_name, None)
        if not func:
            raise AttributeError(f"Splitwise SDK has no method '{sdk_name}'")
        result = func(**kwargs)
        return result

    # Specific helper methods

    def get_current_user_id(self) -> int | None:
        """Return the current authenticated user's ID or None."""
        me = self._client.getCurrentUser()
        # Attempt to extract ID from returned object
        if hasattr(me, "id"):
            return getattr(me, "id")
        if isinstance(me, dict):
            return me.get("id")
        return None

    def get_group_by_name(self, name: str) -> Any:
        """Return a group object by name (case sensitive match).

        Returns None if no group matches.
        """
        groups = self._client.getGroups()
        for group in groups:
            if getattr(group, "name", None) == name:
                return group
        return None

    def get_user_from_group(self, group: Any, participant_name: str) -> Any:
        """Find a user within a group by matching first or full name."""
        # The group object returned by Splitwise SDK may have a
        # `members` attribute.  Each member likely has `first_name`
        # and `last_name`.  We attempt to match either the first
        # name or the full name (first + space + last).
        members = getattr(group, "members", []) or getattr(group, "members_list", [])
        for member in members:
            full = f"{getattr(member, 'first_name', '')} {getattr(member, 'last_name', '')}".strip()
            if participant_name == getattr(member, "first_name", None) or participant_name == full:
                return member
        return None

    def convert(self, obj: Any) -> Any:
        """Convert Splitwise SDK objects to serialisable Python data."""
        return object_to_dict(obj)
