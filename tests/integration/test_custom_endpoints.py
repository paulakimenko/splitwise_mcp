"""Integration tests for custom helper endpoints.

These tests validate the custom business logic endpoints work correctly
with real Splitwise data and our test group.
"""

from fastapi.testclient import TestClient


class TestCustomEndpointsIntegration:
    """Test custom helper endpoints with real data."""

    def test_expenses_by_month_with_empty_group(
        self, test_client: TestClient, test_group_name: str, test_group_id: int
    ):
        """Test expenses by month endpoint with a new empty group."""

        # First, populate the cache with expenses data
        test_client.post("/mcp/list_expenses", json={})

        # Test the expenses by month endpoint
        response = test_client.get(
            f"/custom/expenses_by_month?group_name={test_group_name}&month=2024-11"
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # New group should have no expenses
        assert len(data) == 0

    def test_monthly_report_with_empty_group(
        self, test_client: TestClient, test_group_name: str, test_group_id: int
    ):
        """Test monthly report endpoint with a new empty group."""

        # First, populate the cache with expenses data
        test_client.post("/mcp/list_expenses", json={})

        # Test the monthly report endpoint
        response = test_client.get(
            f"/custom/monthly_report?group_name={test_group_name}&month=2024-11"
        )

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

        # Prepare expense data with a non-existent participant
        # This should fail gracefully since the test group only has current user
        expense_data = {
            "group_name": test_group_name,
            "amount": 20.00,
            "participant_name": "NonExistentUser",  # This user doesn't exist in the group
            "currency_code": "USD",
            "description": "Integration Test Expense",
        }

        # Create the expense - this should fail since participant doesn't exist
        response = test_client.post(
            "/custom/add_expense_equal_split", json=expense_data
        )

        # Should return 400 error since participant not found
        assert response.status_code == 400
        data = response.json()
        assert "not found in group" in data["detail"]

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
