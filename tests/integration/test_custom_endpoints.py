"""Integration tests for custom helper endpoints.

These tests validate the custom business logic endpoints work correctly
with real Splitwise data and our test group.
"""

import pytest
from fastapi.testclient import TestClient


class TestCustomEndpointsIntegration:
    """Test custom helper endpoints with real data."""

    @pytest.mark.asyncio
    async def test_expenses_by_month_with_empty_group(
        self,
        test_client: TestClient,
        test_group_name: str,
        test_group_id: int
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

    @pytest.mark.asyncio
    async def test_monthly_report_with_empty_group(
        self,
        test_client: TestClient,
        test_group_name: str,
        test_group_id: int
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

    @pytest.mark.asyncio 
    async def test_add_expense_equal_split_integration(
        self,
        test_client: TestClient,
        test_group_name: str,
        test_group_id: int,
        current_user_id: int,
        splitwise_client
    ):
        """Test adding an expense with equal split using the custom endpoint."""
        
        # Get current user info to use as participant
        current_user = await asyncio.to_thread(
            splitwise_client.raw_client.getCurrentUser
        )
        
        # Prepare expense data
        expense_data = {
            "group_name": test_group_name,
            "amount": 20.00,
            "participant_name": current_user.first_name,  # Use current user as participant
            "currency_code": "USD",
            "description": "Integration Test Expense"
        }
        
        # Create the expense
        response = test_client.post(
            "/custom/add_expense_equal_split",
            json=expense_data
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify expense was created
        assert "id" in data
        assert "cost" in data
        expense_id = data["id"]
        
        # Verify expense appears in group expenses
        group_expenses_response = test_client.post(
            "/mcp/get_group_expenses",
            json={"id": test_group_id}
        )
        
        assert group_expenses_response.status_code == 200
        expenses = group_expenses_response.json()
        
        # Should now have our test expense
        assert len(expenses) >= 1
        
        # Find our expense
        our_expense = None
        for expense in expenses:
            if expense.get("id") == expense_id:
                our_expense = expense
                break
        
        assert our_expense is not None
        assert our_expense["description"] == "Integration Test Expense"
        assert float(our_expense["cost"]) == 20.00
        
        # Clean up: Delete the expense
        try:
            await asyncio.to_thread(
                splitwise_client.raw_client.deleteExpense,
                expense_id
            )
            print(f"Cleaned up test expense {expense_id}")
        except Exception as e:
            print(f"Warning: Failed to delete test expense {expense_id}: {e}")

    @pytest.mark.asyncio
    async def test_invalid_group_name(self, test_client: TestClient):
        """Test custom endpoints with invalid group name."""
        
        response = test_client.get(
            "/custom/expenses_by_month?group_name=NonexistentGroup&month=2024-11"
        )
        
        assert response.status_code == 400
        assert "Group not found" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_invalid_month_format(
        self, 
        test_client: TestClient,
        test_group_name: str
    ):
        """Test custom endpoints with invalid month format."""
        
        response = test_client.get(
            f"/custom/expenses_by_month?group_name={test_group_name}&month=invalid"
        )
        
        assert response.status_code == 400
        assert "format" in response.json()["detail"].lower()


# Import asyncio for the async cleanup operations
import asyncio