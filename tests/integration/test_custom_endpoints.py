"""Integration tests for custom helper endpoints.

These tests validate the custom business logic endpoints work correctly
with real Splitwise data and our test group.
"""

import asyncio

import pytest
from fastapi.testclient import TestClient
from splitwise.user import User


class TestCustomEndpointsIntegration:
    """Test custom helper endpoints with real data."""

    def test_expenses_by_month_with_empty_group(
        self, test_client: TestClient, test_group_name: str, test_group_id: int
    ):
        """Test expenses by month endpoint with a new empty group."""

        # Test the expenses by month endpoint directly (no cache population needed)
        response = test_client.get(
            f"/custom/expenses_by_month?group_name={test_group_name}&month=2024-11"
        )

        # Skip if MongoDB is not available (connection refused)
        if response.status_code == 400 and "Connection refused" in response.text:
            pytest.skip("MongoDB not available for integration tests")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # New group should have no expenses
        assert len(data) == 0

    def test_monthly_report_with_empty_group(
        self, test_client: TestClient, test_group_name: str, test_group_id: int
    ):
        """Test monthly report endpoint with a new empty group."""

        # Test the monthly report endpoint directly (no cache population needed)
        response = test_client.get(
            f"/custom/monthly_report?group_name={test_group_name}&month=2024-11"
        )

        # Skip if MongoDB is not available (connection refused)
        if response.status_code == 400 and "Connection refused" in response.text:
            pytest.skip("MongoDB not available for integration tests")

        assert response.status_code == 200
        data = response.json()

        # Should return empty report structure
        assert "total" in data
        assert "summary" in data
        assert "recommendations" in data
        assert data["total"] == 0.0
        assert len(data["summary"]) == 0

    def test_add_expense_equal_split_integration(
        self,
        test_client: TestClient,
        test_group_name: str,
        test_group_id: int,
        current_user_id: int,
        splitwise_client,
    ):
        """Test adding an expense with equal split using the custom endpoint."""

        # First, manually add MCP TEST as a friend to the test group using the splitwise_client directly
        try:
            # Try to add MCP TEST user to the group
            # Note: This will work if MCP TEST is an existing friend
            user = User()
            user.setFirstName("MCP")
            user.setLastName("TEST")
            user.setEmail("mcp.test@example.com")

            # Add user to group using the raw client
            asyncio.run(
                asyncio.to_thread(
                    splitwise_client.raw_client.addUserToGroup, user, test_group_id
                )
            )
        except Exception:
            # If adding the user fails, skip this test
            pytest.skip(
                "Could not add MCP TEST user to test group - user may not exist as friend"
            )

        # Prepare expense data with MCP TEST as participant
        expense_data = {
            "group_name": test_group_name,
            "amount": 20.00,
            "participant_name": "MCP TEST",  # Use your friend MCP TEST
            "currency_code": "USD",
            "description": "Integration Test Expense",
        }

        # Create the expense - this should succeed now
        response = test_client.post(
            "/custom/add_expense_equal_split", json=expense_data
        )

        # Skip if MongoDB is not available (connection refused)
        if response.status_code == 400 and "Connection refused" in response.text:
            pytest.skip("MongoDB not available for integration tests")

        # Should succeed and return expense details
        assert response.status_code == 200
        data = response.json()

        # Handle tuple response from Splitwise SDK (createExpense returns [expense, None])
        expense_data = data[0] if isinstance(data, list) and len(data) > 0 else data

        assert "id" in expense_data  # Check for expense creation
        assert expense_data.get("description") == "Integration Test Expense"

    def test_invalid_group_name(self, test_client: TestClient):
        """Test custom endpoints with invalid group name."""

        response = test_client.get(
            "/custom/expenses_by_month?group_name=NonexistentGroup&month=2024-11"
        )

        assert response.status_code == 400
        assert "not found" in response.json()["detail"]

    def test_invalid_month_format(self, test_client: TestClient, test_group_name: str):
        """Test custom endpoints with invalid month format."""

        response = test_client.get(
            f"/custom/expenses_by_month?group_name={test_group_name}&month=invalid"
        )

        assert response.status_code == 400
        assert "format" in response.json()["detail"].lower()
