"""Cached wrapper around SplitwiseClient with MongoDB-based caching.

This module implements entity-specific caching with configurable TTLs
for different data types (expenses, groups, friends, users, etc.).
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any, ClassVar

from . import constants as const
from .db import get_db
from .logging_utils import log_operation
from .splitwise_client import SplitwiseClient


class CachedSplitwiseClient:
    """Cached wrapper for SplitwiseClient with entity-specific TTLs.

    This client wraps the SplitwiseClient and adds MongoDB-based caching
    with different TTL values for different entity types:
    - Expenses: 5 minutes (frequent updates)
    - Friends: 5 minutes (balance changes)
    - Users: 1 hour (profile changes rare)
    - Groups: 1 hour (membership changes rare)
    - Categories: 24 hours (static data)
    - Currencies: 24 hours (static data)
    - Notifications: No cache (always fresh)
    """

    # Entity-specific TTL configuration (in minutes)
    ENTITY_TTL_MAP: ClassVar[dict[str, int]] = {
        const.ENTITY_EXPENSES: int(
            os.getenv(
                const.ENV_CACHE_TTL_EXPENSES_MINUTES, str(const.DEFAULT_TTL_EXPENSES)
            )
        ),
        const.ENTITY_FRIENDS: int(
            os.getenv(
                const.ENV_CACHE_TTL_FRIENDS_MINUTES, str(const.DEFAULT_TTL_FRIENDS)
            )
        ),
        const.ENTITY_USERS: int(
            os.getenv(const.ENV_CACHE_TTL_USERS_MINUTES, str(const.DEFAULT_TTL_USERS))
        ),
        const.ENTITY_GROUPS: int(
            os.getenv(const.ENV_CACHE_TTL_GROUPS_MINUTES, str(const.DEFAULT_TTL_GROUPS))
        ),
        const.ENTITY_CATEGORIES: int(
            os.getenv(
                const.ENV_CACHE_TTL_CATEGORIES_MINUTES,
                str(const.DEFAULT_TTL_CATEGORIES),
            )
        ),
        const.ENTITY_CURRENCIES: int(
            os.getenv(
                const.ENV_CACHE_TTL_CURRENCIES_MINUTES,
                str(const.DEFAULT_TTL_CURRENCIES),
            )
        ),
        const.ENTITY_NOTIFICATIONS: const.DEFAULT_TTL_NOTIFICATIONS,  # Never cache - always fetch fresh
    }

    # Mapping of method names to entity types for cache lookup
    METHOD_TO_ENTITY_MAP: ClassVar[dict[str, str]] = {
        const.METHOD_GET_CURRENT_USER: const.ENTITY_USERS,
        const.METHOD_LIST_GROUPS: const.ENTITY_GROUPS,
        const.METHOD_GET_GROUP: const.ENTITY_GROUPS,
        const.METHOD_LIST_EXPENSES: const.ENTITY_EXPENSES,
        const.METHOD_GET_EXPENSE: const.ENTITY_EXPENSES,
        const.METHOD_LIST_FRIENDS: const.ENTITY_FRIENDS,
        const.METHOD_GET_FRIEND: const.ENTITY_FRIENDS,
        const.METHOD_LIST_CATEGORIES: const.ENTITY_CATEGORIES,
        const.METHOD_LIST_CURRENCIES: const.ENTITY_CURRENCIES,
        const.METHOD_LIST_NOTIFICATIONS: const.ENTITY_NOTIFICATIONS,
    }

    def __init__(
        self,
        api_key: str | None = None,
        consumer_key: str | None = None,
        consumer_secret: str | None = None,
    ) -> None:
        """Initialize the cached client with underlying SplitwiseClient."""
        self._client = SplitwiseClient(
            api_key=api_key,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
        )
        self._cache_enabled = (
            os.getenv(const.ENV_CACHE_ENABLED, const.DEFAULT_CACHE_ENABLED).lower()
            == "true"
        )

    @property
    def raw_client(self):
        """Access to underlying Splitwise client."""
        return self._client.raw_client

    def _get_cache_collection_name(self, method_name: str) -> str:
        """Get the MongoDB collection name for a method."""
        entity_type = self.METHOD_TO_ENTITY_MAP.get(method_name)
        if not entity_type:
            # For unknown methods, use the method name as collection
            return f"cache_{method_name}"
        return entity_type

    def _is_entity_cache_valid(self, entity_type: str, entity_timestamp: str) -> bool:
        """Check if cached entity is still valid based on entity-specific TTL.

        Args:
            entity_type: Type of entity (e.g., "expenses", "friends", "users")
            entity_timestamp: ISO 8601 timestamp of last cache update

        Returns:
            True if cache is still valid, False if expired
        """
        ttl_minutes = self.ENTITY_TTL_MAP.get(entity_type, 5)

        # Notifications are never cached
        if ttl_minutes == 0:
            return False

        try:
            entity_time = datetime.fromisoformat(
                entity_timestamp.replace("Z", "+00:00")
            )
            now = datetime.now(UTC)
            age_minutes = (now - entity_time).total_seconds() / 60
            return age_minutes < ttl_minutes
        except (ValueError, AttributeError):
            # Invalid timestamp format - consider cache invalid
            return False

    def _get_from_cache(
        self, method_name: str, allow_stale: bool = False, **kwargs: Any
    ) -> Any | None:
        """Attempt to retrieve data from cache.

        Args:
            method_name: Name of the Splitwise method
            allow_stale: If True, return stale cache data even if expired
            **kwargs: Method parameters for cache key

        Returns:
            Cached data if valid (or stale if allow_stale=True), None if cache miss
        """
        if not self._cache_enabled:
            return None

        entity_type = self.METHOD_TO_ENTITY_MAP.get(method_name)
        if not entity_type:
            return None

        # Notifications are never cached
        if entity_type == const.ENTITY_NOTIFICATIONS:
            return None

        try:
            db = get_db()
            collection = db[entity_type]

            # Build query based on method and parameters
            query = self._build_cache_query(method_name, **kwargs)
            if not query:
                return None

            # Find cached document
            cached = collection.find_one(query)
            if not cached:
                return None

            # If allowing stale data, return immediately (fallback mode)
            if allow_stale:
                return cached.get("response_data")

            # Check if cache is still valid
            last_updated = cached.get("last_updated_date")
            if not last_updated:
                return None

            if not self._is_entity_cache_valid(entity_type, last_updated):
                # Cache expired - delete it
                collection.delete_one({"_id": cached["_id"]})
                return None

            # Return cached response data
            return cached.get("response_data")

        except Exception as exc:
            log_operation(
                "cache", "CACHE_ERROR", {"method": method_name, "error": str(exc)}, {}
            )
            return None

    def _build_cache_query(
        self, method_name: str, **kwargs: Any
    ) -> dict[str, Any] | None:
        """Build MongoDB query for cache lookup based on method and parameters.

        CRITICAL: All filter parameters that affect the API response MUST be included
        in the cache query. Otherwise, different queries will incorrectly share the same
        cached data, leading to incorrect results.

        For example:
        - list_expenses(dated_after="2025-10-01") and list_expenses(dated_after="2025-09-01")
          must have separate cache entries, not share the same cache.
        """
        # For list methods without parameters, use a simple query
        if method_name == "list_groups":
            return {"method": method_name}
        elif method_name == "get_group" and "id" in kwargs:
            return {"method": method_name, "group_id": kwargs["id"]}
        elif method_name == "list_expenses":
            # CRITICAL: Include ALL filter parameters that affect the response
            # Without this, different date ranges/limits would share the same cache
            query = {"method": method_name}
            if "group_id" in kwargs:
                query["group_id"] = kwargs["group_id"]
            if "friend_id" in kwargs:
                query["friend_id"] = kwargs["friend_id"]
            # Date range filters - MUST be included in cache key
            if "dated_after" in kwargs:
                query["dated_after"] = kwargs["dated_after"]
            if "dated_before" in kwargs:
                query["dated_before"] = kwargs["dated_before"]
            if "updated_after" in kwargs:
                query["updated_after"] = kwargs["updated_after"]
            if "updated_before" in kwargs:
                query["updated_before"] = kwargs["updated_before"]
            # Pagination parameters - MUST be included in cache key
            if "limit" in kwargs:
                query["limit"] = kwargs["limit"]
            if "offset" in kwargs:
                query["offset"] = kwargs["offset"]
            return query
        elif method_name == "get_expense" and "id" in kwargs:
            return {"method": method_name, "expense_id": kwargs["id"]}
        elif method_name == "list_friends":
            return {"method": method_name}
        elif method_name == "get_friend" and "id" in kwargs:
            return {"method": method_name, "friend_id": kwargs["id"]}
        elif (
            method_name == "get_current_user"
            or method_name == "list_categories"
            or method_name == "list_currencies"
        ):
            return {"method": method_name}

        return None

    def _save_to_cache(
        self, method_name: str, response_data: Any, **kwargs: Any
    ) -> None:
        """Save API response to cache with timestamp."""
        if not self._cache_enabled:
            return

        entity_type = self.METHOD_TO_ENTITY_MAP.get(method_name)
        if not entity_type:
            return

        # Don't cache notifications
        if entity_type == "notifications":
            return

        try:
            db = get_db()
            collection = db[entity_type]

            # Build cache document
            query = self._build_cache_query(method_name, **kwargs)
            if not query:
                return

            cache_doc = {
                **query,
                "response_data": response_data,
                "last_updated_date": datetime.now(UTC).isoformat(),
            }

            # Upsert (update or insert)
            collection.update_one(query, {"$set": cache_doc}, upsert=True)

            log_operation(method_name, "CACHE_WRITE", kwargs, {"cached": True})

        except Exception as exc:
            # Graceful degradation - don't fail if cache write fails
            log_operation(
                "cache",
                "CACHE_WRITE_ERROR",
                {"method": method_name, "error": str(exc)},
                {},
            )

    def call_mapped_method(self, method_name: str, **kwargs: Any) -> Any:
        """Call a Splitwise method with caching support.

        For READ methods (GET), checks cache first before calling API.
        For WRITE methods (POST), bypasses cache and invalidates affected data.

        Implements fallback mechanism: if API call fails for READ methods,
        returns stale cached data if available to maintain service availability.

        CRITICAL: Always returns the same data type (Splitwise SDK objects) regardless
        of cache hit/miss to maintain consistent behavior for callers.
        """
        # Check cache for READ methods
        if method_name in self.METHOD_TO_ENTITY_MAP:
            cached_data = self._get_from_cache(method_name, **kwargs)
            if cached_data is not None:
                log_operation(method_name, "CACHE_HIT", kwargs, {"cached": True})
                # Return cached dict directly (already converted)
                return cached_data

        # Cache miss or WRITE method - call API
        try:
            result = self._client.call_mapped_method(method_name, **kwargs)

            # Cache the result for READ methods
            if method_name in self.METHOD_TO_ENTITY_MAP:
                response_data = self._client.convert(result)
                self._save_to_cache(method_name, response_data, **kwargs)
                log_operation(method_name, "CACHE_MISS", kwargs, {"cached": False})
                # Return converted dict for consistency with cache hits
                return response_data
            else:
                # For WRITE methods, invalidate affected cache entries
                self._invalidate_cache_for_write(method_name, **kwargs)

            return result

        except Exception as exc:
            # For READ methods, try to use stale cache as fallback
            if method_name in self.METHOD_TO_ENTITY_MAP:
                stale_data = self._get_from_cache(
                    method_name, allow_stale=True, **kwargs
                )
                if stale_data is not None:
                    log_operation(
                        method_name,
                        "CACHE_FALLBACK",
                        kwargs,
                        {"cached": True, "stale": True, "error": str(exc)},
                    )
                    return stale_data

            # No cache available or WRITE method - re-raise the error
            log_operation(
                method_name,
                "API_ERROR",
                kwargs,
                None,
                str(exc),
            )
            raise

    def _invalidate_cache_for_write(self, method_name: str, **_kwargs: Any) -> None:
        """Invalidate cache entries affected by write operations."""
        if not self._cache_enabled:
            return

        try:
            db = get_db()

            # Invalidate based on write operation type
            if method_name in [
                "create_expense",
                "update_expense",
                "delete_expense",
                "undelete_expense",
            ]:
                # Invalidate all expense caches
                db["expenses"].delete_many({})
                log_operation(
                    method_name, "CACHE_INVALIDATE", {"entity": "expenses"}, {}
                )

            elif method_name in [
                "create_group",
                "delete_group",
                "undelete_group",
                "add_user_to_group",
                "remove_user_from_group",
            ]:
                # Invalidate all group caches
                db["groups"].delete_many({})
                log_operation(method_name, "CACHE_INVALIDATE", {"entity": "groups"}, {})

            elif method_name in ["create_friend", "delete_friend", "create_friends"]:
                # Invalidate all friend caches
                db["friends"].delete_many({})
                log_operation(
                    method_name, "CACHE_INVALIDATE", {"entity": "friends"}, {}
                )

            elif method_name == "update_user":
                # Invalidate user cache
                db["users"].delete_many({})
                log_operation(method_name, "CACHE_INVALIDATE", {"entity": "users"}, {})

        except Exception as exc:
            log_operation(
                "cache",
                "INVALIDATE_ERROR",
                {"method": method_name, "error": str(exc)},
                {},
            )

    # Delegate helper methods to underlying client

    def get_current_user_id(self) -> int | None:
        """Return the current authenticated user's ID or None."""
        return self._client.get_current_user_id()

    def get_group_by_name(self, name: str) -> Any:
        """Return a group object by name (case sensitive match)."""
        return self._client.get_group_by_name(name)

    def get_user_from_group(self, group: Any, participant_name: str) -> Any:
        """Find a user within a group by matching first or full name."""
        return self._client.get_user_from_group(group, participant_name)

    def convert(self, obj: Any) -> Any:
        """Convert Splitwise SDK objects to serialisable Python data."""
        return self._client.convert(obj)
