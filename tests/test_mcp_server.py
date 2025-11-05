"""Tests for app.mcp_server module (MCP server implementation)."""

import asyncio
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, Mock, patch

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from app.mcp_server import mcp
from app.splitwise_client import SplitwiseClient


@pytest.fixture
def mock_splitwise_client():
    """Mock SplitwiseClient for testing."""
    client = Mock(spec=SplitwiseClient)
    client.call_mapped_method = Mock(return_value={"test": "data"})
    client.convert = Mock(return_value={"converted": "data"})
    client.get_group_by_name = Mock()
    client.get_user_from_group = Mock()
    client.get_current_user_id = Mock(return_value=12345)
    return client


@pytest.fixture
def mock_lifespan_context(mock_splitwise_client):
    """Mock lifespan context with client."""
    return {"client": mock_splitwise_client}


@pytest.fixture
def mock_context(mock_lifespan_context):
    """Mock MCP Context object."""
    context = Mock()
    context.request_context.lifespan_context = mock_lifespan_context
    return context


class TestMCPTools:
    """Test MCP tool implementations."""

    @pytest.mark.asyncio
    async def test_get_current_user_success(self, mock_context):
        """Test get_current_user tool success."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.insert_document") as mock_insert,
            patch("app.mcp_server.log_operation") as mock_log,
        ):
            # Import the function from the server module
            from app.mcp_server import get_current_user

            mock_to_thread.return_value = {"id": 12345, "name": "Test User"}

            result = await get_current_user(mock_context)

            assert result == {"converted": "data"}
            mock_to_thread.assert_called_once()
            mock_insert.assert_called_once()
            mock_log.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_current_user_error(self, mock_context):
        """Test get_current_user tool with error."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.log_operation") as mock_log,
        ):
            from app.mcp_server import get_current_user

            mock_to_thread.side_effect = Exception("API Error")

            with pytest.raises(Exception, match="API Error"):
                await get_current_user(mock_context)

            mock_log.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_groups_success(self, mock_context):
        """Test list_groups tool success."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.insert_document") as mock_insert,
            patch("app.mcp_server.log_operation") as mock_log,
        ):
            from app.mcp_server import list_groups

            mock_to_thread.return_value = [{"id": 1, "name": "Test Group"}]

            result = await list_groups(mock_context)

            assert result == {"converted": "data"}
            mock_to_thread.assert_called_once()
            mock_insert.assert_called_once()
            mock_log.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_group_success(self, mock_context):
        """Test get_group tool success."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.insert_document") as mock_insert,
            patch("app.mcp_server.log_operation") as mock_log,
        ):
            from app.mcp_server import get_group

            mock_to_thread.return_value = {"id": 123, "name": "Test Group"}

            result = await get_group(123, mock_context)

            assert result == {"converted": "data"}
            mock_to_thread.assert_called_once()
            mock_insert.assert_called_once()
            mock_log.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_expenses_with_filters(self, mock_context):
        """Test list_expenses tool with filters."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.insert_document") as mock_insert,
            patch("app.mcp_server.log_operation") as mock_log,
        ):
            from app.mcp_server import list_expenses

            mock_to_thread.return_value = [{"id": 1, "cost": "100.00"}]

            result = await list_expenses(
                group_id=123,
                friend_id=456,
                dated_after="2024-01-01",
                dated_before="2024-12-31",
                ctx=mock_context,
            )

            assert result == {"converted": "data"}
            mock_to_thread.assert_called_once()
            # Verify arguments passed to the helper
            args, kwargs = mock_to_thread.call_args
            assert "list_expenses" in args
            assert kwargs.get("group_id") == 123
            assert kwargs.get("friend_id") == 456
            assert kwargs.get("dated_after") == "2024-01-01"
            assert kwargs.get("dated_before") == "2024-12-31"

    @pytest.mark.asyncio
    async def test_list_expenses_no_filters(self, mock_context):
        """Test list_expenses tool without filters."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.insert_document"),
            patch("app.mcp_server.log_operation"),
        ):
            from app.mcp_server import list_expenses

            mock_to_thread.return_value = [{"id": 1, "cost": "100.00"}]

            result = await list_expenses(ctx=mock_context)

            assert result == {"converted": "data"}
            # Verify no extra arguments passed when filters are None
            args, kwargs = mock_to_thread.call_args
            assert "list_expenses" in args
            # Should only have the method name, no filter args
            assert len([k for k in kwargs if k != "method_name"]) == 0

    @pytest.mark.asyncio
    async def test_list_notifications_with_limit(self, mock_context):
        """Test list_notifications tool with limit."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.insert_document"),
            patch("app.mcp_server.log_operation"),
        ):
            from app.mcp_server import list_notifications

            mock_to_thread.return_value = [{"id": 1, "content": "Test notification"}]

            result = await list_notifications(limit=5, ctx=mock_context)

            assert result == {"converted": "data"}
            args, kwargs = mock_to_thread.call_args
            assert kwargs.get("limit") == 5

    @pytest.mark.asyncio
    async def test_list_notifications_no_limit(self, mock_context):
        """Test list_notifications tool without limit."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.insert_document"),
            patch("app.mcp_server.log_operation"),
        ):
            from app.mcp_server import list_notifications

            mock_to_thread.return_value = []

            result = await list_notifications(ctx=mock_context)

            assert result == {"converted": "data"}
            args, kwargs = mock_to_thread.call_args
            # Should not include limit when it's 0
            assert "limit" not in kwargs


class TestMCPResources:
    """Test MCP resource implementations."""

    @pytest.mark.asyncio
    async def test_group_resource(self, mock_context):
        """Test group resource."""
        from app.mcp_server import get_group_by_name

        mock_client = mock_context.request_context.lifespan_context["client"]
        mock_group = Mock()
        mock_group.name = "Test Group"
        mock_group.id = 123
        mock_client.get_group_by_name.return_value = mock_group
        mock_client.convert.return_value = {"id": 123, "name": "Test Group"}

        result = await get_group_by_name("Test Group", mock_context)

        assert result == "{'id': 123, 'name': 'Test Group'}"
        mock_client.get_group_by_name.assert_called_once_with("Test Group")

    @pytest.mark.asyncio
    async def test_group_resource_not_found(self, mock_context):
        """Test group resource when group not found."""
        from app.mcp_server import get_group_by_name

        mock_client = mock_context.request_context.lifespan_context["client"]
        mock_client.get_group_by_name.return_value = None

        result = await get_group_by_name("NonExistent", mock_context)
        assert result == "Group 'NonExistent' not found"

    @pytest.mark.asyncio
    async def test_balance_resource(self, mock_context):
        """Test balance resource."""
        from app.mcp_server import get_balance

        mock_client = mock_context.request_context.lifespan_context["client"]
        mock_client.call_mapped_method.return_value = {"total_balance": "150.00"}
        mock_client.convert.return_value = {"converted": "data"}

        result = await get_balance(mock_context)

        assert result == "{'converted': 'data'}"
        mock_client.call_mapped_method.assert_called_once_with("get_current_user")


class TestHelperFunction:
    """Test the _call_splitwise_method helper function."""

    @pytest.mark.asyncio
    async def test_call_splitwise_method_success(self, mock_context):
        """Test _call_splitwise_method success case."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.insert_document") as mock_insert,
            patch("app.mcp_server.log_operation") as mock_log,
        ):
            from app.mcp_server import _call_splitwise_method

            mock_to_thread.return_value = {"test": "result"}

            result = await _call_splitwise_method(
                mock_context, "test_method", arg1="value1"
            )

            assert result == {"converted": "data"}

            # Verify the async call
            mock_to_thread.assert_called_once()
            args, kwargs = mock_to_thread.call_args
            client = mock_context.request_context.lifespan_context["client"]
            assert args == (client.call_mapped_method, "test_method")
            assert kwargs == {"arg1": "value1"}

            # Verify database and logging
            mock_insert.assert_called_once_with(
                "test_method", {"response": {"converted": "data"}}
            )
            mock_log.assert_called_once_with(
                "test_method", "TOOL_CALL", {"arg1": "value1"}, {"converted": "data"}
            )

    @pytest.mark.asyncio
    async def test_call_splitwise_method_error(self, mock_context):
        """Test _call_splitwise_method error case."""
        with (
            patch("app.mcp_server.asyncio.to_thread") as mock_to_thread,
            patch("app.mcp_server.log_operation") as mock_log,
        ):
            from app.mcp_server import _call_splitwise_method

            mock_to_thread.side_effect = Exception("API Error")

            with pytest.raises(Exception, match="API Error"):
                await _call_splitwise_method(mock_context, "test_method")

            mock_log.assert_called_once_with(
                "test_method", "TOOL_CALL", {}, None, "API Error"
            )


class TestMCPLifespan:
    """Test MCP lifespan management."""

    @pytest.mark.asyncio
    async def test_mcp_lifespan_success(self):
        """Test MCP lifespan with valid API key."""
        with (
            patch.dict("os.environ", {"SPLITWISE_API_KEY": "test_key"}),
            patch("app.mcp_server.SplitwiseClient") as mock_client_class,
        ):
            from app.mcp_server import mcp_lifespan

            mock_client = Mock()
            mock_client_class.return_value = mock_client
            mock_server = Mock()

            # Test the async context manager
            async with mcp_lifespan(mock_server) as lifespan_context:
                assert lifespan_context["client"] == mock_client

            mock_client_class.assert_called_once_with(api_key="test_key")

    @pytest.mark.asyncio
    async def test_mcp_lifespan_no_api_key(self):
        """Test MCP lifespan fails without API key."""
        with patch.dict("os.environ", {}, clear=True):
            from app.mcp_server import mcp_lifespan

            mock_server = Mock()

            with pytest.raises(
                RuntimeError,
                match="You must set either SPLITWISE_API_KEY or both SPLITWISE_CONSUMER_KEY and SPLITWISE_CONSUMER_SECRET in the environment",
            ):
                async with mcp_lifespan(mock_server):
                    pass
