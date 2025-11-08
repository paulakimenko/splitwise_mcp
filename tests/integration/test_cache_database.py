"""Integration tests for cache database validation.

These tests verify that cached data in MongoDB matches the request parameters
and that the cache requirements from CACHED_SPLITWISE_CLIENT.md are met.

Note: This test module uses the test_group_id fixture from conftest.py,
which creates a temporary test group for testing and cleans it up afterwards.
"""

from __future__ import annotations

import contextlib
import os
import time
from datetime import datetime

import pytest

from app.cached_splitwise_client import CachedSplitwiseClient
from app.db import get_db

# Skip tests if no API key is available
pytestmark = pytest.mark.skipif(
    not os.getenv("SPLITWISE_API_KEY") and not os.getenv("SPLITWISE_CONSUMER_KEY"),
    reason="Integration tests require Splitwise API credentials",
)


@pytest.fixture
def cached_client():
    """Create a cached Splitwise client for testing."""
    return CachedSplitwiseClient()


@pytest.fixture
def db():
    """Get MongoDB database for testing."""
    return get_db()


@pytest.fixture(autouse=True)
def cleanup_cache(db):
    """Clean up cache collections before and after each test."""
    # Clean before test
    if db is not None:
        for collection_name in ["expenses", "groups", "friends", "users"]:
            with contextlib.suppress(Exception):
                db[collection_name].delete_many({})

    yield

    # Clean after test
    if db is not None:
        for collection_name in ["expenses", "groups", "friends", "users"]:
            with contextlib.suppress(Exception):
                db[collection_name].delete_many({})


class TestCacheDatabaseValidation:
    """Test that cached data in MongoDB matches request parameters."""

    def test_list_expenses_caches_with_date_filters(self, cached_client, db):
        """Verify that cached expenses include date filter parameters in cache key."""
        if db is None:
            pytest.skip("MongoDB not available")

        # Make API call with date filters
        dated_after = "2025-10-01T00:00:00Z"
        dated_before = "2025-11-01T00:00:00Z"

        result = cached_client.call_mapped_method(
            "list_expenses",
            dated_after=dated_after,
            dated_before=dated_before,
            limit=5,
        )

        # Verify API call succeeded
        assert result is not None
        assert isinstance(result, list)  # Returns list of Expense objects

        # Give MongoDB a moment to write
        time.sleep(0.1)

        # Check actual MongoDB document
        cached_doc = db["expenses"].find_one(
            {
                "method": "list_expenses",
                "dated_after": dated_after,
                "dated_before": dated_before,
            }
        )

        # Validate cache document exists with correct parameters
        assert cached_doc is not None, "Expense should be cached with date filters"
        assert cached_doc["method"] == "list_expenses"
        assert cached_doc["dated_after"] == dated_after
        assert cached_doc["dated_before"] == dated_before
        assert "response_data" in cached_doc
        assert "last_updated_date" in cached_doc

    def test_list_expenses_different_date_ranges_separate_cache_entries(
        self, cached_client, db
    ):
        """Verify that different date ranges create separate cache entries.

        This validates the bug fix: requests with different date ranges
        must NOT share the same cache entry.
        """
        if db is None:
            pytest.skip("MongoDB not available")

        # First request: 2-month range
        result1 = cached_client.call_mapped_method(
            "list_expenses",
            dated_after="2025-09-01T00:00:00Z",
            dated_before="2025-11-01T00:00:00Z",
            limit=5,
        )
        assert result1 is not None

        # Second request: 1-month range
        result2 = cached_client.call_mapped_method(
            "list_expenses",
            dated_after="2025-10-01T00:00:00Z",
            dated_before="2025-11-01T00:00:00Z",
            limit=5,
        )
        assert result2 is not None

        # Give MongoDB a moment to write
        time.sleep(0.1)

        # Check both cache entries exist separately
        cache1 = db["expenses"].find_one(
            {
                "method": "list_expenses",
                "dated_after": "2025-09-01T00:00:00Z",
                "dated_before": "2025-11-01T00:00:00Z",
            }
        )

        cache2 = db["expenses"].find_one(
            {
                "method": "list_expenses",
                "dated_after": "2025-10-01T00:00:00Z",
                "dated_before": "2025-11-01T00:00:00Z",
            }
        )

        # Both should exist as separate entries
        assert cache1 is not None, "First date range should be cached"
        assert cache2 is not None, "Second date range should be cached"

        # Verify they are different documents
        assert cache1["_id"] != cache2["_id"], "Should be different cache entries"
        assert cache1["dated_after"] != cache2["dated_after"], (
            "Date filters should differ"
        )

    def test_list_expenses_with_all_filters_in_cache_key(
        self, cached_client, db, test_group_id
    ):
        """Verify all filter parameters are included in cache key."""
        if db is None:
            pytest.skip("MongoDB not available")

        # Make API call with all possible filters (using real group_id)
        params = {
            "group_id": test_group_id,  # Use real test group
            "dated_after": "2025-10-01T00:00:00Z",
            "dated_before": "2025-11-01T00:00:00Z",
            "updated_after": "2025-10-15T00:00:00Z",
            "updated_before": "2025-10-20T00:00:00Z",
            "limit": 50,
            "offset": 0,  # Changed from 100 to 0 to avoid offset issues
        }

        result = cached_client.call_mapped_method("list_expenses", **params)
        assert result is not None

        # Give MongoDB a moment to write
        time.sleep(0.1)

        # Check cache document contains all parameters
        cached_doc = db["expenses"].find_one({"method": "list_expenses", **params})

        assert cached_doc is not None, "Should be cached with all filters"
        assert cached_doc["method"] == "list_expenses"
        assert cached_doc["group_id"] == test_group_id
        assert cached_doc["dated_after"] == params["dated_after"]
        assert cached_doc["dated_before"] == params["dated_before"]
        assert cached_doc["updated_after"] == params["updated_after"]
        assert cached_doc["updated_before"] == params["updated_before"]
        assert cached_doc["limit"] == params["limit"]
        assert cached_doc["offset"] == params["offset"]

    def test_list_expenses_without_filters_separate_from_filtered(
        self, cached_client, db
    ):
        """Verify unfiltered requests don't share cache with filtered requests."""
        if db is None:
            pytest.skip("MongoDB not available")

        # Request without filters
        result1 = cached_client.call_mapped_method("list_expenses", limit=5)
        assert result1 is not None

        # Request with date filter
        result2 = cached_client.call_mapped_method(
            "list_expenses",
            dated_after="2025-10-01T00:00:00Z",
            limit=5,
        )
        assert result2 is not None

        # Give MongoDB a moment to write
        time.sleep(0.1)

        # Check both exist as separate entries
        cache_unfiltered = db["expenses"].find_one(
            {"method": "list_expenses", "dated_after": {"$exists": False}}
        )

        cache_filtered = db["expenses"].find_one(
            {
                "method": "list_expenses",
                "dated_after": "2025-10-01T00:00:00Z",
            }
        )

        assert cache_unfiltered is not None, "Unfiltered request should be cached"
        assert cache_filtered is not None, "Filtered request should be cached"
        assert cache_unfiltered["_id"] != cache_filtered["_id"], (
            "Should be different entries"
        )

    def test_cache_hit_returns_cached_data(self, cached_client, db):
        """Verify second request returns cached data without API call."""
        if db is None:
            pytest.skip("MongoDB not available")

        dated_after = "2025-10-01T00:00:00Z"
        dated_before = "2025-11-01T00:00:00Z"

        # First request - should cache
        result1 = cached_client.call_mapped_method(
            "list_expenses",
            dated_after=dated_after,
            dated_before=dated_before,
            limit=5,
        )
        assert result1 is not None

        # Give MongoDB a moment to write
        time.sleep(0.1)

        # Verify it's cached
        cached_doc = db["expenses"].find_one(
            {
                "method": "list_expenses",
                "dated_after": dated_after,
                "dated_before": dated_before,
            }
        )
        assert cached_doc is not None

        # Second request - should return cached data
        result2 = cached_client.call_mapped_method(
            "list_expenses",
            dated_after=dated_after,
            dated_before=dated_before,
            limit=5,
        )

        # Results should be same length (cached returns converted dicts, not objects)
        # The first call returns Expense objects, second call returns cached dicts
        assert len(result2) == len(result1), "Cache should return same number of items"

        # Verify the second result is from cache (converted to dicts)
        if len(result2) > 0:
            assert isinstance(result2, list)
            # Cached results should be dicts (converted from objects)
            if result2:
                assert isinstance(result2[0], dict), (
                    "Cached results should be converted to dicts"
                )

    def test_list_groups_caches_correctly(self, cached_client, db):
        """Verify list_groups caching works correctly."""
        if db is None:
            pytest.skip("MongoDB not available")

        # Make API call
        result = cached_client.call_mapped_method("list_groups")
        assert result is not None

        # Give MongoDB a moment to write
        time.sleep(0.1)

        # Check cache document
        cached_doc = db["groups"].find_one({"method": "list_groups"})

        assert cached_doc is not None, "Groups should be cached"
        assert cached_doc["method"] == "list_groups"
        assert "response_data" in cached_doc
        assert "last_updated_date" in cached_doc

    def test_get_group_caches_with_group_id(self, cached_client, db, test_group_id):
        """Verify get_group caching includes group_id in cache key."""
        if db is None:
            pytest.skip("MongoDB not available")

        # Make API call
        result = cached_client.call_mapped_method("get_group", id=test_group_id)
        assert result is not None

        # Give MongoDB a moment to write
        time.sleep(0.1)

        # Check cache document
        cached_doc = db["groups"].find_one(
            {"method": "get_group", "group_id": test_group_id}
        )

        assert cached_doc is not None, "Group should be cached with group_id"
        assert cached_doc["method"] == "get_group"
        assert cached_doc["group_id"] == test_group_id
        assert "response_data" in cached_doc

    def test_cache_timestamp_format(self, cached_client, db):
        """Verify cached data has proper timestamp format."""
        if db is None:
            pytest.skip("MongoDB not available")

        # Make API call
        result = cached_client.call_mapped_method("list_groups")
        assert result is not None

        # Give MongoDB a moment to write
        time.sleep(0.1)

        # Check cache document
        cached_doc = db["groups"].find_one({"method": "list_groups"})

        assert cached_doc is not None
        assert "last_updated_date" in cached_doc

        # Verify timestamp is ISO format and parseable
        timestamp_str = cached_doc["last_updated_date"]
        try:
            parsed_time = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            assert parsed_time.tzinfo is not None, "Timestamp should include timezone"
        except (ValueError, AttributeError) as e:
            pytest.fail(f"Invalid timestamp format: {timestamp_str}, error: {e}")
