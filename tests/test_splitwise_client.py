"""Tests for app.splitwise_client module."""

import os
from unittest.mock import Mock, patch

import pytest

from app.splitwise_client import SplitwiseClient


class TestSplitwiseClientInit:
    """Test SplitwiseClient initialization."""

    def test_init_with_api_key(self):
        """Test initialization with API key parameter."""
        with patch("app.splitwise_client.Splitwise") as mock_splitwise:
            client = SplitwiseClient(api_key="test_key")
            mock_splitwise.assert_called_once_with(
                consumer_key="", consumer_secret="", api_key="test_key"
            )
            assert client.raw_client == mock_splitwise.return_value

    def test_init_with_oauth_credentials(self):
        """Test initialization with OAuth consumer credentials."""
        with patch("app.splitwise_client.Splitwise") as mock_splitwise:
            client = SplitwiseClient(
                consumer_key="test_consumer_key", consumer_secret="test_consumer_secret"
            )
            mock_splitwise.assert_called_once_with(
                consumer_key="test_consumer_key", consumer_secret="test_consumer_secret"
            )
            assert client.raw_client == mock_splitwise.return_value

    def test_init_with_env_var_api_key(self):
        """Test initialization with API key environment variable."""
        with (
            patch("app.splitwise_client.Splitwise") as mock_splitwise,
            patch.dict(os.environ, {"SPLITWISE_API_KEY": "env_key"}),
        ):
            SplitwiseClient()
            mock_splitwise.assert_called_once_with(
                consumer_key="", consumer_secret="", api_key="env_key"
            )

    def test_init_with_env_var_oauth(self):
        """Test initialization with OAuth environment variables."""
        with (
            patch("app.splitwise_client.Splitwise") as mock_splitwise,
            patch.dict(
                os.environ,
                {
                    "SPLITWISE_CONSUMER_KEY": "env_consumer_key",
                    "SPLITWISE_CONSUMER_SECRET": "env_consumer_secret",
                },
            ),
        ):
            client = SplitwiseClient()
            mock_splitwise.assert_called_once_with(
                consumer_key="env_consumer_key",
                consumer_secret="env_consumer_secret",
            )

    def test_init_api_key_takes_priority(self):
        """Test that API key takes priority over OAuth credentials when both are present."""
        with (
            patch("app.splitwise_client.Splitwise") as mock_splitwise,
            patch.dict(
                os.environ,
                {
                    "SPLITWISE_CONSUMER_KEY": "env_consumer_key",
                    "SPLITWISE_CONSUMER_SECRET": "env_consumer_secret",
                    "SPLITWISE_API_KEY": "env_api_key",
                },
            ),
        ):
            SplitwiseClient()
            mock_splitwise.assert_called_once_with(
                consumer_key="", consumer_secret="", api_key="env_api_key"
            )

    def test_init_without_credentials(self):
        """Test initialization fails without any credentials."""
        with (
            patch.dict(os.environ, {}, clear=True),
            pytest.raises(
                ValueError,
                match="Either SPLITWISE_CONSUMER_KEY and SPLITWISE_CONSUMER_SECRET, or SPLITWISE_API_KEY environment variables must be set",
            ),
        ):
            SplitwiseClient()


class TestMethodMapping:
    """Test method mapping functionality."""

    def test_call_mapped_method_valid(self, mock_splitwise_client):
        """Test calling a valid mapped method."""
        mock_splitwise_client._client.getGroups.return_value = ["group1", "group2"]

        result = mock_splitwise_client.call_mapped_method("list_groups")

        mock_splitwise_client._client.getGroups.assert_called_once_with()
        assert result == ["group1", "group2"]

    def test_call_mapped_method_with_kwargs(self, mock_splitwise_client):
        """Test calling mapped method with arguments."""
        mock_splitwise_client._client.getGroup.return_value = {
            "id": 1,
            "name": "Test Group",
        }

        result = mock_splitwise_client.call_mapped_method("get_group", id=1)

        mock_splitwise_client._client.getGroup.assert_called_once_with(id=1)
        assert result == {"id": 1, "name": "Test Group"}

    def test_call_mapped_method_unsupported(self, mock_splitwise_client):
        """Test calling unsupported method raises error."""
        with pytest.raises(AttributeError, match="Unsupported method 'invalid_method'"):
            mock_splitwise_client.call_mapped_method("invalid_method")

    def test_call_mapped_method_sdk_missing(self, mock_splitwise_client):
        """Test calling method not available in SDK."""
        # Remove the method from the mock
        del mock_splitwise_client._client.getGroups

        with pytest.raises(
            AttributeError, match="Splitwise SDK has no method 'getGroups'"
        ):
            mock_splitwise_client.call_mapped_method("list_groups")


class TestHelperMethods:
    """Test helper methods."""

    def test_get_current_user_id_with_id_attr(self, mock_splitwise_client):
        """Test getting current user ID when user has id attribute."""
        mock_user = Mock()
        mock_user.id = 12345
        mock_splitwise_client._client.getCurrentUser.return_value = mock_user

        user_id = mock_splitwise_client.get_current_user_id()

        assert user_id == 12345

    def test_get_current_user_id_dict(self, mock_splitwise_client):
        """Test getting current user ID when user is dict."""
        mock_splitwise_client._client.getCurrentUser.return_value = {"id": 67890}

        user_id = mock_splitwise_client.get_current_user_id()

        assert user_id == 67890

    def test_get_current_user_id_none(self, mock_splitwise_client):
        """Test getting current user ID when no ID available."""
        mock_splitwise_client._client.getCurrentUser.return_value = Mock()
        # Remove id attribute
        del mock_splitwise_client._client.getCurrentUser.return_value.id

        user_id = mock_splitwise_client.get_current_user_id()

        assert user_id is None

    def test_get_group_by_name_found(self, mock_splitwise_client):
        """Test finding group by name when group exists."""
        mock_group1 = Mock()
        mock_group1.name = "Group 1"
        mock_group2 = Mock()
        mock_group2.name = "Test Group"

        mock_splitwise_client._client.getGroups.return_value = [
            mock_group1,
            mock_group2,
        ]

        result = mock_splitwise_client.get_group_by_name("Test Group")

        assert result == mock_group2

    def test_get_group_by_name_not_found(self, mock_splitwise_client):
        """Test finding group by name when group doesn't exist."""
        mock_group = Mock()
        mock_group.name = "Different Group"

        mock_splitwise_client._client.getGroups.return_value = [mock_group]

        result = mock_splitwise_client.get_group_by_name("Nonexistent Group")

        assert result is None

    def test_get_user_from_group_by_first_name(self, mock_splitwise_client):
        """Test finding user from group by first name."""
        mock_member1 = Mock()
        mock_member1.first_name = "John"
        mock_member1.last_name = "Doe"

        mock_member2 = Mock()
        mock_member2.first_name = "Jane"
        mock_member2.last_name = "Smith"

        mock_group = Mock()
        mock_group.members = [mock_member1, mock_member2]

        result = mock_splitwise_client.get_user_from_group(mock_group, "Jane")

        assert result == mock_member2

    def test_get_user_from_group_by_full_name(self, mock_splitwise_client):
        """Test finding user from group by full name."""
        mock_member = Mock()
        mock_member.first_name = "John"
        mock_member.last_name = "Doe"

        mock_group = Mock()
        mock_group.members = [mock_member]

        result = mock_splitwise_client.get_user_from_group(mock_group, "John Doe")

        assert result == mock_member

    def test_get_user_from_group_not_found(self, mock_splitwise_client):
        """Test finding user from group when user doesn't exist."""
        mock_member = Mock()
        mock_member.first_name = "John"
        mock_member.last_name = "Doe"

        mock_group = Mock()
        mock_group.members = [mock_member]

        result = mock_splitwise_client.get_user_from_group(mock_group, "Jane Smith")

        assert result is None

    def test_get_user_from_group_members_list_attr(self, mock_splitwise_client):
        """Test finding user with members_list attribute."""
        mock_member = Mock()
        mock_member.first_name = "John"
        mock_member.last_name = "Doe"

        mock_group = Mock()
        # Use members_list instead of members
        mock_group.members = []
        mock_group.members_list = [mock_member]

        result = mock_splitwise_client.get_user_from_group(mock_group, "John")

        assert result == mock_member

    @patch("app.splitwise_client.object_to_dict")
    def test_convert(self, mock_object_to_dict, mock_splitwise_client):
        """Test object conversion."""
        test_obj = {"test": "data"}
        mock_object_to_dict.return_value = {"converted": "data"}

        result = mock_splitwise_client.convert(test_obj)

        mock_object_to_dict.assert_called_once_with(test_obj)
        assert result == {"converted": "data"}
