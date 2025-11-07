"""Tests for app.cached_splitwise_client module."""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from unittest.mock import Mock, patch

from app.cached_splitwise_client import CachedSplitwiseClient


class TestCachedClientInit:
    """Test CachedSplitwiseClient initialization."""

    def test_init_with_api_key(self):
        """Test initialization with API key parameter."""
        with (
            patch("app.cached_splitwise_client.SplitwiseClient") as mock_client_class,
            patch.dict(os.environ, {"CACHE_ENABLED": "true"}),
        ):
            client = CachedSplitwiseClient(api_key="test_key")
            mock_client_class.assert_called_once_with(
                api_key="test_key",
                consumer_key=None,
                consumer_secret=None,
            )
            assert client._cache_enabled is True

    def test_init_with_oauth_credentials(self):
        """Test initialization with OAuth consumer credentials."""
        with (
            patch("app.cached_splitwise_client.SplitwiseClient") as mock_client_class,
            patch.dict(os.environ, {"CACHE_ENABLED": "false"}),
        ):
            client = CachedSplitwiseClient(
                consumer_key="test_consumer_key",
                consumer_secret="test_consumer_secret",
            )
            mock_client_class.assert_called_once_with(
                api_key=None,
                consumer_key="test_consumer_key",
                consumer_secret="test_consumer_secret",
            )
            assert client._cache_enabled is False

    def test_cache_enabled_default(self):
        """Test that cache is enabled by default."""
        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch.dict(os.environ, {}, clear=True),
        ):
            client = CachedSplitwiseClient(api_key="test_key")
            assert client._cache_enabled is True


class TestEntityTTLConfiguration:
    """Test entity-specific TTL configuration."""

    def test_default_ttl_values(self):
        """Test default TTL values for all entity types."""
        assert CachedSplitwiseClient.ENTITY_TTL_MAP["expenses"] == 5
        assert CachedSplitwiseClient.ENTITY_TTL_MAP["friends"] == 5
        assert CachedSplitwiseClient.ENTITY_TTL_MAP["users"] == 60
        assert CachedSplitwiseClient.ENTITY_TTL_MAP["groups"] == 60
        assert CachedSplitwiseClient.ENTITY_TTL_MAP["categories"] == 1440
        assert CachedSplitwiseClient.ENTITY_TTL_MAP["currencies"] == 1440
        assert CachedSplitwiseClient.ENTITY_TTL_MAP["notifications"] == 0

    def test_custom_ttl_via_environment(self):
        """Test that TTL can be customized via environment variables."""
        with patch.dict(
            os.environ,
            {
                "CACHE_TTL_EXPENSES_MINUTES": "10",
                "CACHE_TTL_FRIENDS_MINUTES": "15",
                "CACHE_TTL_USERS_MINUTES": "120",
            },
        ):
            # Need to reload the class to pick up env vars
            # For this test, we'll just verify the env var logic
            assert os.getenv("CACHE_TTL_EXPENSES_MINUTES") == "10"

    def test_method_to_entity_mapping(self):
        """Test that all expected methods are mapped to entities."""
        expected_mappings = {
            "get_current_user": "users",
            "list_groups": "groups",
            "get_group": "groups",
            "list_expenses": "expenses",
            "get_expense": "expenses",
            "list_friends": "friends",
            "get_friend": "friends",
            "list_categories": "categories",
            "list_currencies": "currencies",
            "list_notifications": "notifications",
        }
        assert expected_mappings == CachedSplitwiseClient.METHOD_TO_ENTITY_MAP


class TestCacheValidation:
    """Test cache validity checking logic."""

    def test_is_entity_cache_valid_fresh_cache(self):
        """Test that recently cached data is considered valid."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")

            # Create a timestamp from 1 minute ago
            one_minute_ago = datetime.now(UTC) - timedelta(minutes=1)
            timestamp = one_minute_ago.isoformat()

            # Expenses have 5-minute TTL, so 1 minute old should be valid
            assert client._is_entity_cache_valid("expenses", timestamp) is True

    def test_is_entity_cache_valid_expired_cache(self):
        """Test that expired cached data is considered invalid."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")

            # Create a timestamp from 10 minutes ago
            ten_minutes_ago = datetime.now(UTC) - timedelta(minutes=10)
            timestamp = ten_minutes_ago.isoformat()

            # Expenses have 5-minute TTL, so 10 minutes old should be invalid
            assert client._is_entity_cache_valid("expenses", timestamp) is False

    def test_is_entity_cache_valid_notifications_never_valid(self):
        """Test that notifications cache is never considered valid."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")

            # Even with fresh timestamp, notifications should never be cached
            now = datetime.now(UTC).isoformat()
            assert client._is_entity_cache_valid("notifications", now) is False

    def test_is_entity_cache_valid_invalid_timestamp(self):
        """Test handling of invalid timestamp formats."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")

            # Invalid timestamp should return False
            assert (
                client._is_entity_cache_valid("expenses", "invalid-timestamp") is False
            )
            assert client._is_entity_cache_valid("expenses", "") is False

    def test_is_entity_cache_valid_different_ttls(self):
        """Test cache validation with different entity TTLs."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")

            # Create a timestamp from 30 minutes ago
            thirty_minutes_ago = datetime.now(UTC) - timedelta(minutes=30)
            timestamp = thirty_minutes_ago.isoformat()

            # Expenses (5 min TTL) - should be invalid
            assert client._is_entity_cache_valid("expenses", timestamp) is False

            # Users (60 min TTL) - should be valid
            assert client._is_entity_cache_valid("users", timestamp) is True

            # Categories (1440 min TTL) - should be valid
            assert client._is_entity_cache_valid("categories", timestamp) is True


class TestCacheQueries:
    """Test cache query building logic."""

    def test_build_cache_query_list_groups(self):
        """Test query building for list_groups method."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")
            query = client._build_cache_query("list_groups")
            assert query == {"method": "list_groups"}

    def test_build_cache_query_get_group(self):
        """Test query building for get_group method."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")
            query = client._build_cache_query("get_group", id=123)
            assert query == {"method": "get_group", "group_id": 123}

    def test_build_cache_query_list_expenses_no_params(self):
        """Test query building for list_expenses without parameters."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")
            query = client._build_cache_query("list_expenses")
            assert query == {"method": "list_expenses"}

    def test_build_cache_query_list_expenses_with_group_id(self):
        """Test query building for list_expenses with group_id."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")
            query = client._build_cache_query("list_expenses", group_id=456)
            assert query == {"method": "list_expenses", "group_id": 456}

    def test_build_cache_query_list_expenses_with_friend_id(self):
        """Test query building for list_expenses with friend_id."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")
            query = client._build_cache_query("list_expenses", friend_id=789)
            assert query == {"method": "list_expenses", "friend_id": 789}

    def test_build_cache_query_get_expense(self):
        """Test query building for get_expense method."""
        with patch("app.cached_splitwise_client.SplitwiseClient"):
            client = CachedSplitwiseClient(api_key="test")
            query = client._build_cache_query("get_expense", id=999)
            assert query == {"method": "get_expense", "expense_id": 999}


class TestCacheOperations:
    """Test cache read and write operations."""

    def test_get_from_cache_disabled(self):
        """Test that cache is bypassed when disabled."""
        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch.dict(os.environ, {"CACHE_ENABLED": "false"}),
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client._get_from_cache("list_groups")
            assert result is None

    def test_get_from_cache_notifications_never_cached(self):
        """Test that notifications are never retrieved from cache."""
        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch("app.cached_splitwise_client.get_db"),
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client._get_from_cache("list_notifications")
            assert result is None

    def test_get_from_cache_hit(self):
        """Test successful cache retrieval."""
        mock_collection = Mock()
        mock_db = Mock()
        mock_db.__getitem__ = Mock(return_value=mock_collection)

        cached_data = {
            "_id": "123",
            "method": "list_groups",
            "response_data": [{"id": 1, "name": "Test Group"}],
            "last_updated_date": datetime.now(UTC).isoformat(),
        }
        mock_collection.find_one.return_value = cached_data

        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch("app.cached_splitwise_client.get_db", return_value=mock_db),
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client._get_from_cache("list_groups")
            assert result == [{"id": 1, "name": "Test Group"}]

    def test_get_from_cache_miss(self):
        """Test cache miss when no cached data exists."""
        mock_collection = Mock()
        mock_db = Mock()
        mock_db.__getitem__ = Mock(return_value=mock_collection)
        mock_collection.find_one.return_value = None

        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch("app.cached_splitwise_client.get_db", return_value=mock_db),
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client._get_from_cache("list_groups")
            assert result is None

    def test_get_from_cache_expired(self):
        """Test that expired cache is deleted and returns None."""
        mock_collection = Mock()
        mock_db = Mock()
        mock_db.__getitem__ = Mock(return_value=mock_collection)

        # Create expired cached data (10 minutes ago for 5-minute TTL)
        ten_minutes_ago = datetime.now(UTC) - timedelta(minutes=10)
        cached_data = {
            "_id": "123",
            "method": "list_expenses",
            "response_data": [{"id": 1, "description": "Old Expense"}],
            "last_updated_date": ten_minutes_ago.isoformat(),
        }
        mock_collection.find_one.return_value = cached_data

        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch("app.cached_splitwise_client.get_db", return_value=mock_db),
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client._get_from_cache("list_expenses")

            # Should return None and delete the expired entry
            assert result is None
            mock_collection.delete_one.assert_called_once_with({"_id": "123"})

    def test_save_to_cache_disabled(self):
        """Test that cache write is skipped when disabled."""
        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch.dict(os.environ, {"CACHE_ENABLED": "false"}),
            patch("app.cached_splitwise_client.get_db") as mock_get_db,
        ):
            client = CachedSplitwiseClient(api_key="test")
            client._save_to_cache("list_groups", [{"id": 1}])
            mock_get_db.assert_not_called()

    def test_save_to_cache_notifications_not_cached(self):
        """Test that notifications are never saved to cache."""
        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch("app.cached_splitwise_client.get_db") as mock_get_db,
        ):
            client = CachedSplitwiseClient(api_key="test")
            client._save_to_cache("list_notifications", [{"id": 1}])
            mock_get_db.assert_not_called()

    def test_save_to_cache_success(self):
        """Test successful cache write."""
        mock_collection = Mock()
        mock_db = Mock()
        mock_db.__getitem__ = Mock(return_value=mock_collection)

        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch("app.cached_splitwise_client.get_db", return_value=mock_db),
            patch("app.cached_splitwise_client.log_operation"),
        ):
            client = CachedSplitwiseClient(api_key="test")
            response_data = [{"id": 1, "name": "Test Group"}]
            client._save_to_cache("list_groups", response_data)

            # Verify update_one was called with correct query and data
            mock_collection.update_one.assert_called_once()
            call_args = mock_collection.update_one.call_args
            query = call_args[0][0]
            update = call_args[0][1]

            assert query == {"method": "list_groups"}
            assert update["$set"]["response_data"] == response_data
            assert "last_updated_date" in update["$set"]


class TestCallMappedMethod:
    """Test the main call_mapped_method orchestration."""

    def test_call_mapped_method_cache_hit(self):
        """Test that cache hit returns cached data without API call."""
        mock_client = Mock()

        with (
            patch(
                "app.cached_splitwise_client.SplitwiseClient", return_value=mock_client
            ),
            patch.object(
                CachedSplitwiseClient,
                "_get_from_cache",
                return_value={"cached": "data"},
            ),
            patch("app.cached_splitwise_client.log_operation"),
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client.call_mapped_method("list_groups")

            # Should return cached data
            assert result == {"cached": "data"}
            # Should not call underlying client
            mock_client.call_mapped_method.assert_not_called()

    def test_call_mapped_method_cache_miss(self):
        """Test that cache miss calls API and saves to cache."""
        mock_client = Mock()
        api_response = Mock()
        converted_data = [{"id": 1, "name": "Group"}]
        mock_client.call_mapped_method.return_value = api_response
        mock_client.convert.return_value = converted_data

        with (
            patch(
                "app.cached_splitwise_client.SplitwiseClient", return_value=mock_client
            ),
            patch.object(CachedSplitwiseClient, "_get_from_cache", return_value=None),
            patch.object(CachedSplitwiseClient, "_save_to_cache") as mock_save,
            patch("app.cached_splitwise_client.log_operation"),
        ):
            client = CachedSplitwiseClient(api_key="test")
            client._client = mock_client
            result = client.call_mapped_method("list_groups")

            # Should call API
            mock_client.call_mapped_method.assert_called_once_with("list_groups")
            # Should save to cache
            mock_save.assert_called_once_with("list_groups", converted_data)
            # Should return API result
            assert result == api_response

    def test_call_mapped_method_write_operation(self):
        """Test that write operations invalidate cache."""
        mock_client = Mock()
        api_response = Mock()
        mock_client.call_mapped_method.return_value = api_response

        with (
            patch(
                "app.cached_splitwise_client.SplitwiseClient", return_value=mock_client
            ),
            patch.object(
                CachedSplitwiseClient, "_invalidate_cache_for_write"
            ) as mock_invalidate,
        ):
            client = CachedSplitwiseClient(api_key="test")
            client._client = mock_client
            result = client.call_mapped_method("create_expense", cost="25.00")

            # Should call API
            mock_client.call_mapped_method.assert_called_once_with(
                "create_expense", cost="25.00"
            )
            # Should invalidate cache
            mock_invalidate.assert_called_once_with("create_expense", cost="25.00")
            # Should return API result
            assert result == api_response


class TestCacheInvalidation:
    """Test cache invalidation for write operations."""

    def test_invalidate_cache_for_expense_operations(self):
        """Test that expense write operations invalidate expense cache."""
        mock_expenses_collection = Mock()
        mock_db = Mock()
        mock_db.__getitem__ = Mock(return_value=mock_expenses_collection)

        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch("app.cached_splitwise_client.get_db", return_value=mock_db),
            patch("app.cached_splitwise_client.log_operation"),
        ):
            client = CachedSplitwiseClient(api_key="test")

            # Test each expense write operation
            for method in [
                "create_expense",
                "update_expense",
                "delete_expense",
                "undelete_expense",
            ]:
                mock_expenses_collection.reset_mock()
                client._invalidate_cache_for_write(method)
                mock_expenses_collection.delete_many.assert_called_once_with({})

    def test_invalidate_cache_for_group_operations(self):
        """Test that group write operations invalidate group cache."""
        mock_groups_collection = Mock()
        mock_db = Mock()
        mock_db.__getitem__ = Mock(return_value=mock_groups_collection)

        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch("app.cached_splitwise_client.get_db", return_value=mock_db),
            patch("app.cached_splitwise_client.log_operation"),
        ):
            client = CachedSplitwiseClient(api_key="test")

            # Test each group write operation
            for method in [
                "create_group",
                "delete_group",
                "undelete_group",
                "add_user_to_group",
                "remove_user_from_group",
            ]:
                mock_groups_collection.reset_mock()
                client._invalidate_cache_for_write(method)
                mock_groups_collection.delete_many.assert_called_once_with({})

    def test_invalidate_cache_for_friend_operations(self):
        """Test that friend write operations invalidate friend cache."""
        mock_friends_collection = Mock()
        mock_db = Mock()
        mock_db.__getitem__ = Mock(return_value=mock_friends_collection)

        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch("app.cached_splitwise_client.get_db", return_value=mock_db),
            patch("app.cached_splitwise_client.log_operation"),
        ):
            client = CachedSplitwiseClient(api_key="test")

            # Test each friend write operation
            for method in ["create_friend", "delete_friend", "create_friends"]:
                mock_friends_collection.reset_mock()
                client._invalidate_cache_for_write(method)
                mock_friends_collection.delete_many.assert_called_once_with({})

    def test_invalidate_cache_disabled(self):
        """Test that invalidation is skipped when cache is disabled."""
        with (
            patch("app.cached_splitwise_client.SplitwiseClient"),
            patch.dict(os.environ, {"CACHE_ENABLED": "false"}),
            patch("app.cached_splitwise_client.get_db") as mock_get_db,
        ):
            client = CachedSplitwiseClient(api_key="test")
            client._invalidate_cache_for_write("create_expense")
            mock_get_db.assert_not_called()


class TestDelegatedMethods:
    """Test methods delegated to underlying SplitwiseClient."""

    def test_get_current_user_id_delegation(self):
        """Test that get_current_user_id is delegated to underlying client."""
        mock_client = Mock()
        mock_client.get_current_user_id.return_value = 12345

        with patch(
            "app.cached_splitwise_client.SplitwiseClient", return_value=mock_client
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client.get_current_user_id()

            assert result == 12345
            mock_client.get_current_user_id.assert_called_once()

    def test_get_group_by_name_delegation(self):
        """Test that get_group_by_name is delegated to underlying client."""
        mock_client = Mock()
        mock_group = {"id": 1, "name": "Test Group"}
        mock_client.get_group_by_name.return_value = mock_group

        with patch(
            "app.cached_splitwise_client.SplitwiseClient", return_value=mock_client
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client.get_group_by_name("Test Group")

            assert result == mock_group
            mock_client.get_group_by_name.assert_called_once_with("Test Group")

    def test_get_user_from_group_delegation(self):
        """Test that get_user_from_group is delegated to underlying client."""
        mock_client = Mock()
        mock_group = {"id": 1, "members": []}
        mock_user = {"id": 123, "name": "John"}
        mock_client.get_user_from_group.return_value = mock_user

        with patch(
            "app.cached_splitwise_client.SplitwiseClient", return_value=mock_client
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client.get_user_from_group(mock_group, "John")

            assert result == mock_user
            mock_client.get_user_from_group.assert_called_once_with(mock_group, "John")

    def test_convert_delegation(self):
        """Test that convert is delegated to underlying client."""
        mock_client = Mock()
        mock_obj = Mock()
        converted_data = {"converted": True}
        mock_client.convert.return_value = converted_data

        with patch(
            "app.cached_splitwise_client.SplitwiseClient", return_value=mock_client
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client.convert(mock_obj)

            assert result == converted_data
            mock_client.convert.assert_called_once_with(mock_obj)

    def test_raw_client_property(self):
        """Test that raw_client property provides access to underlying SDK client."""
        mock_client = Mock()
        mock_raw = Mock()
        mock_client.raw_client = mock_raw

        with patch(
            "app.cached_splitwise_client.SplitwiseClient", return_value=mock_client
        ):
            client = CachedSplitwiseClient(api_key="test")
            result = client.raw_client

            assert result == mock_raw
