"""Tests for app.main module (FastAPI application)."""

from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def test_client():
    """Create test client for FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_app_client():
    """Mock the app state client."""
    mock_client = Mock()
    mock_client.call_mapped_method = Mock()
    mock_client.convert = Mock(return_value={"converted": "data"})
    mock_client.get_group_by_name = Mock()
    mock_client.get_user_from_group = Mock()
    mock_client.get_current_user_id = Mock(return_value=12345)
    return mock_client


class TestStartupEvent:
    """Test application startup."""

    @pytest.mark.asyncio
    async def test_startup_without_api_key(self):
        """Test startup fails without API key."""
        with (
            patch.dict("os.environ", {}, clear=True),
            pytest.raises(
                RuntimeError,
                match="You must set either SPLITWISE_API_KEY or both SPLITWISE_CONSUMER_KEY and SPLITWISE_CONSUMER_SECRET in the environment",
            ),
        ):
            from unittest.mock import MagicMock

            from app.main import lifespan

            mock_app = MagicMock()
            async with lifespan(mock_app):
                pass

    @pytest.mark.asyncio
    @patch("app.main.SplitwiseClient")
    async def test_startup_with_api_key(self, mock_splitwise_client):
        """Test successful startup with API key."""
        with patch.dict("os.environ", {"SPLITWISE_API_KEY": "test_key"}):
            from unittest.mock import MagicMock

            from app.main import lifespan

            mock_app = MagicMock()
            async with lifespan(mock_app):
                pass
            mock_splitwise_client.assert_called_once_with(api_key="test_key")


class TestMCPServer:
    """Test MCP server integration."""

    def test_mcp_server_mounted(self, test_client):
        """Test that MCP server is properly mounted."""
        # The MCP server is mounted at /mcp but uses MCP protocol, not HTTP
        # We can test that the mount doesn't break the app
        response = test_client.get("/")
        # Should get 404 for root path, but app should still work
        assert response.status_code == 404

    def test_mcp_server_does_not_interfere_with_rest_api(self, test_client):
        """Test that MCP server doesn't interfere with REST endpoints."""
        with patch("app.main.find_latest") as mock_find:
            mock_find.return_value = {"response": [{"id": 1, "name": "Test Group"}]}

            # REST endpoints should still work
            response = test_client.get("/groups")
            assert response.status_code == 200


class TestRESTEndpoints:
    """Test REST endpoints for cached data."""

    def test_get_groups_success(self, test_client):
        """Test successful groups retrieval."""
        with patch("app.main.find_latest") as mock_find:
            mock_find.return_value = {"response": [{"id": 1, "name": "Test Group"}]}

            response = test_client.get("/groups")

            assert response.status_code == 200
            assert response.json() == [{"id": 1, "name": "Test Group"}]

    def test_get_groups_no_data(self, test_client):
        """Test groups endpoint with no cached data."""
        with patch("app.main.find_latest") as mock_find:
            mock_find.return_value = None

            response = test_client.get("/groups")

            assert response.status_code == 200
            result = response.json()
            assert result["message"] == "No cached groups found"
            assert result["data"] is None

    def test_get_expenses_success(self, test_client):
        """Test successful expenses retrieval."""
        with patch("app.main.find_latest") as mock_find:
            mock_find.return_value = {"response": [{"id": 1, "cost": "100.0"}]}

            response = test_client.get("/expenses")

            assert response.status_code == 200
            assert response.json() == [{"id": 1, "cost": "100.0"}]

    def test_get_friends_success(self, test_client):
        """Test successful friends retrieval."""
        with patch("app.main.find_latest") as mock_find:
            mock_find.return_value = {"data": [{"id": 1, "name": "John Doe"}]}

            response = test_client.get("/friends")

            assert response.status_code == 200
            assert response.json() == [{"id": 1, "name": "John Doe"}]

    def test_get_logs_success(self, test_client):
        """Test logs endpoint."""
        with patch("app.main.get_db") as mock_get_db:
            mock_db = MagicMock()
            mock_collection = MagicMock()
            mock_cursor = MagicMock()

            # Setup the chain: db["logs"].find().sort().limit()
            mock_db.__getitem__.return_value = mock_collection
            mock_collection.find.return_value = mock_cursor
            mock_cursor.sort.return_value = mock_cursor
            mock_cursor.limit.return_value = [
                {"_id": "507f1f77bcf86cd799439011", "message": "test log"}
            ]

            mock_get_db.return_value = mock_db

            response = test_client.get("/logs")

            assert response.status_code == 200
            logs = response.json()
            assert len(logs) == 1
            assert logs[0]["_id"] == "507f1f77bcf86cd799439011"

    def test_health_check_database_connected(self, test_client):
        """Test health endpoint with database connected."""
        with patch("app.main.get_db") as mock_get_db:
            mock_db = MagicMock()
            mock_client = MagicMock()
            mock_admin = MagicMock()

            # Setup the chain: db.client.admin.command('ping')
            mock_db.client = mock_client
            mock_client.admin = mock_admin
            mock_admin.command.return_value = {"ok": 1}

            mock_get_db.return_value = mock_db

            response = test_client.get("/health")

            assert response.status_code == 200
            result = response.json()
            assert result["status"] == "healthy"
            assert result["service"] == "splitwise-mcp"
            assert result["database"] == "connected"

    def test_health_check_database_disconnected(self, test_client):
        """Test health endpoint with database disconnected."""
        with patch("app.main.get_db") as mock_get_db:
            mock_get_db.side_effect = Exception("Connection refused")

            response = test_client.get("/health")

            assert response.status_code == 200
            result = response.json()
            assert result["status"] == "degraded"
            assert result["service"] == "splitwise-mcp"
            assert "disconnected: Connection refused" in result["database"]


class TestCustomEndpoints:
    """Test custom helper endpoints."""

    def test_expenses_by_month_success(self, test_client):
        """Test expenses by month endpoint."""
        with patch("app.main.custom_methods.expenses_by_month") as mock_expenses:
            mock_expenses.return_value = [{"id": 1, "cost": "100.0"}]

            mock_client = Mock()
            app.state.client = mock_client

            response = test_client.get(
                "/custom/expenses_by_month?group_name=Test&month=2025-10"
            )

            assert response.status_code == 200
            assert response.json() == [{"id": 1, "cost": "100.0"}]

    def test_expenses_by_month_error(self, test_client):
        """Test expenses by month endpoint with error."""
        with patch("app.main.custom_methods.expenses_by_month") as mock_expenses:
            mock_expenses.side_effect = Exception("Group not found")

            mock_client = Mock()
            app.state.client = mock_client

            response = test_client.get(
                "/custom/expenses_by_month?group_name=Invalid&month=2025-10"
            )

            assert response.status_code == 400
            assert "Group not found" in response.json()["detail"]

    def test_monthly_report_success(self, test_client):
        """Test monthly report endpoint."""
        with patch("app.main.custom_methods.monthly_report") as mock_report:
            mock_report.return_value = {"total": 100.0, "summary": {"Food": 100.0}}

            mock_client = Mock()
            app.state.client = mock_client

            response = test_client.get(
                "/custom/monthly_report?group_name=Test&month=2025-10"
            )

            assert response.status_code == 200
            assert response.json() == {"total": 100.0, "summary": {"Food": 100.0}}

    def test_add_expense_equal_split_success(self, test_client):
        """Test add expense equal split endpoint."""
        with (
            patch("app.main.asyncio.to_thread") as mock_to_thread,
            patch("app.main.insert_document"),
            patch("app.main.log_operation"),
            patch("splitwise.expense.Expense") as mock_expense_class,
            patch("splitwise.expense.ExpenseUser") as mock_expense_user_class,
        ):
            # Mock the client and its methods
            mock_client = Mock()
            mock_group = Mock()
            mock_group.id = 1
            mock_participant = Mock()
            mock_participant.id = 67890

            mock_client.get_group_by_name.return_value = mock_group
            mock_client.get_user_from_group.return_value = mock_participant
            mock_client.get_current_user_id.return_value = 12345
            mock_client.convert.return_value = {"id": 123, "cost": "100.0"}

            app.state.client = mock_client

            # Mock the splitwise SDK classes
            mock_expense = Mock()
            mock_expense_class.return_value = mock_expense

            mock_user1 = Mock()
            mock_user2 = Mock()
            mock_expense_user_class.side_effect = [
                mock_user1,
                mock_user2,
            ]

            # Mock the createExpense call
            mock_created_expense = Mock()
            mock_to_thread.return_value = mock_created_expense

            payload = {
                "group_name": "Test Group",
                "amount": 100.0,
                "currency_code": "USD",
                "participant_name": "John Doe",
                "description": "Test expense",
            }

            response = test_client.post("/custom/add_expense_equal_split", json=payload)

            if response.status_code != 200:
                print(f"Error response: {response.json()}")
            assert response.status_code == 200
            assert response.json() == {"id": 123, "cost": "100.0"}

    def test_add_expense_equal_split_group_not_found(self, test_client):
        """Test add expense with group not found."""
        mock_client = Mock()
        mock_client.get_group_by_name.return_value = None

        app.state.client = mock_client

        payload = {
            "group_name": "Invalid Group",
            "amount": 100.0,
            "currency_code": "USD",
            "participant_name": "John Doe",
            "description": "Test expense",
        }

        response = test_client.post("/custom/add_expense_equal_split", json=payload)

        assert response.status_code == 400
        assert "Group 'Invalid Group' not found" in response.json()["detail"]
