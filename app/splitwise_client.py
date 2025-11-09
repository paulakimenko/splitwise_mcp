"""Wrapper around the `splitwise` Python SDK.

This class encapsulates initialisation of the Splitwise client and
provides helper methods for the MCP service.  It also exposes a
generic `call_method` which delegates to the underlying SDK methods
based on a mapping from snake_case names to the library's camelCase
method names.  See the README for details.
"""

from __future__ import annotations

import os
from typing import Any, ClassVar

from splitwise import Splitwise

from . import constants as const
from .utils import object_to_dict


class SplitwiseClient:
    """High-level wrapper for the Splitwise API.

    The client supports both personal API key authentication and OAuth consumer credentials.
    It first attempts personal API key authentication if available, then falls back to
    OAuth consumer credentials.
    """

    # Mapping from external MCP method names (snake_case) to
    # Splitwise SDK method names (camelCase).
    METHOD_MAP: ClassVar[dict[str, str]] = {
        # GET methods (read-only)
        const.METHOD_GET_CURRENT_USER: "getCurrentUser",
        const.METHOD_LIST_GROUPS: "getGroups",
        const.METHOD_GET_GROUP: "getGroup",
        const.METHOD_LIST_EXPENSES: "getExpenses",
        const.METHOD_GET_EXPENSE: "getExpense",
        const.METHOD_LIST_FRIENDS: "getFriends",
        const.METHOD_GET_FRIEND: "getFriend",
        const.METHOD_LIST_CATEGORIES: "getCategories",
        const.METHOD_LIST_CURRENCIES: "getCurrencies",
        const.METHOD_GET_EXCHANGE_RATES: "getExchangeRates",
        const.METHOD_LIST_NOTIFICATIONS: "getNotifications",
        # POST methods (actions with side effects)
        const.METHOD_CREATE_EXPENSE: "createExpense",
        const.METHOD_CREATE_GROUP: "createGroup",
        const.METHOD_UPDATE_EXPENSE: "updateExpense",
        const.METHOD_DELETE_EXPENSE: "deleteExpense",
        const.METHOD_CREATE_FRIEND: "createFriend",
        const.METHOD_DELETE_FRIEND: "deleteFriend",
        const.METHOD_ADD_USER_TO_GROUP: "addUserToGroup",
        const.METHOD_REMOVE_USER_FROM_GROUP: "removeUserFromGroup",
        const.METHOD_UNDELETE_EXPENSE: "undeleteExpense",
        const.METHOD_DELETE_GROUP: "deleteGroup",
        const.METHOD_UNDELETE_GROUP: "undeleteGroup",
        const.METHOD_UPDATE_USER: "updateUser",
        const.METHOD_CREATE_FRIENDS: "createFriends",
        const.METHOD_CREATE_COMMENT: "createComment",
        const.METHOD_DELETE_COMMENT: "deleteComment",
    }

    def __init__(
        self,
        api_key: str | None = None,
        consumer_key: str | None = None,
        consumer_secret: str | None = None,
    ) -> None:
        # Get credentials from parameters or environment
        consumer_key = consumer_key or os.environ.get(const.ENV_SPLITWISE_CONSUMER_KEY)
        consumer_secret = consumer_secret or os.environ.get(
            const.ENV_SPLITWISE_CONSUMER_SECRET
        )
        api_key = api_key or os.environ.get(const.ENV_SPLITWISE_API_KEY)

        if api_key:
            # Use personal API key (preferred method)
            # The Splitwise SDK v3.0.0+ requires consumer keys but supports personal access tokens
            # by using empty consumer keys and passing the token as the api_key parameter.
            self._client = Splitwise(
                consumer_key="", consumer_secret="", api_key=api_key
            )
        elif consumer_key and consumer_secret:
            # Use OAuth consumer credentials (requires additional access token setup)
            self._client = Splitwise(
                consumer_key=consumer_key, consumer_secret=consumer_secret
            )
        else:
            raise ValueError(
                f"Either {const.ENV_SPLITWISE_CONSUMER_KEY} and {const.ENV_SPLITWISE_CONSUMER_SECRET}, "
                f"or {const.ENV_SPLITWISE_API_KEY} environment variables must be set"
            )

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
            The result of the SDK call, automatically converted to dict/list
            using object_to_dict for JSON serialization.
        """
        sdk_name = self.METHOD_MAP.get(method_name)
        if not sdk_name:
            raise AttributeError(f"Unsupported method '{method_name}'")
        func = getattr(self._client, sdk_name, None)
        if not func:
            raise AttributeError(f"Splitwise SDK has no method '{sdk_name}'")
        result = func(**kwargs)
        # Automatically convert SDK objects to dicts for JSON serialization
        return self.convert(result)

    # Specific helper methods

    def get_current_user_id(self) -> int | None:
        """Return the current authenticated user's ID or None."""
        me = self._client.getCurrentUser()
        # Attempt to extract ID from returned object
        if hasattr(me, "id"):
            return me.id
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
            if (
                participant_name == getattr(member, "first_name", None)
                or participant_name == full
            ):
                return member
        return None

    def convert(self, obj: Any) -> Any:
        """Convert Splitwise SDK objects to serialisable Python data."""
        return object_to_dict(obj)
