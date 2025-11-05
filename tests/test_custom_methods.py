"""Tests for app.custom_methods module."""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.custom_methods import expenses_by_month, monthly_report


class TestExpensesByMonth:
    """Test expenses_by_month function."""

    @pytest.mark.asyncio
    async def test_expenses_by_month_success(self):
        """Test successful expense filtering by month."""
        # Setup mock group
        mock_group = Mock()
        mock_group.id = 1

        mock_client = Mock()
        mock_client.get_group_by_name.return_value = mock_group

        # Setup mock expenses data
        expenses_data = [
            {
                "id": 1,
                "group_id": 1,
                "date": "2025-10-15T10:00:00Z",
                "cost": "100.0",
                "description": "Groceries",
            },
            {
                "id": 2,
                "group_id": 1,
                "date": "2025-09-15T10:00:00Z",  # Different month
                "cost": "50.0",
                "description": "Gas",
            },
            {
                "id": 3,
                "group_id": 2,  # Different group
                "date": "2025-10-20T10:00:00Z",
                "cost": "75.0",
                "description": "Dinner",
            },
        ]

        with patch("app.custom_methods.find_all") as mock_find_all:
            mock_find_all.return_value = [{"response": expenses_data}]

            result = await expenses_by_month(mock_client, "Test Group", "2025-10")

            # Should only return expense from correct group and month
            assert len(result) == 1
            assert result[0]["id"] == 1
            assert result[0]["description"] == "Groceries"

    @pytest.mark.asyncio
    async def test_expenses_by_month_group_not_found(self):
        """Test when group is not found."""
        mock_client = Mock()
        mock_client.get_group_by_name.return_value = None

        with pytest.raises(ValueError, match="Group 'Nonexistent Group' not found"):
            await expenses_by_month(mock_client, "Nonexistent Group", "2025-10")

    @pytest.mark.asyncio
    async def test_expenses_by_month_no_group_id(self):
        """Test when group has no ID."""
        mock_group = Mock()
        mock_group.id = None
        mock_client = Mock()
        mock_client.get_group_by_name.return_value = mock_group

        with pytest.raises(ValueError, match="Group 'Test Group' does not have an ID"):
            await expenses_by_month(mock_client, "Test Group", "2025-10")

    @pytest.mark.asyncio
    async def test_expenses_by_month_no_cached_data(self):
        """Test when no cached data is available."""
        mock_group = Mock()
        mock_group.id = 1
        mock_client = Mock()
        mock_client.get_group_by_name.return_value = mock_group

        with patch("app.custom_methods.find_all") as mock_find_all:
            mock_find_all.return_value = []

            result = await expenses_by_month(mock_client, "Test Group", "2025-10")

            assert result == []

    @pytest.mark.asyncio
    async def test_expenses_by_month_various_date_fields(self):
        """Test handling different date field names."""
        mock_group = Mock()
        mock_group.id = 1
        mock_client = Mock()
        mock_client.get_group_by_name.return_value = mock_group

        expenses_data = [
            {
                "id": 1,
                "group_id": 1,
                "date": "2025-10-15T10:00:00Z",  # Use date field for consistency
                "cost": "100.0",
            },
            {
                "id": 2,
                "group_id": 1,
                "created_at": "2025-10-20T10:00:00Z",  # Using created_at
                "cost": "50.0",
            },
        ]

        with patch("app.custom_methods.find_all") as mock_find_all:
            mock_find_all.return_value = [{"response": expenses_data}]

            result = await expenses_by_month(mock_client, "Test Group", "2025-10")

            assert len(result) == 2


class TestMonthlyReport:
    """Test monthly_report function."""

    @pytest.mark.asyncio
    async def test_monthly_report_success(self, mock_splitwise_client):
        """Test successful monthly report generation."""
        # Mock expenses_by_month to return test data
        with patch("app.custom_methods.expenses_by_month") as mock_expenses_by_month:
            mock_expenses_by_month.return_value = [
                {"cost": "100.0", "category": {"name": "Food"}},
                {"cost": "50.0", "category": {"name": "Transportation"}},
                {
                    "cost": "200.0",
                    "category": {"name": "Food"},  # Same category
                },
            ]

            result = await monthly_report(
                mock_splitwise_client, "Test Group", "2025-10"
            )

            assert result["total"] == 350.0
            assert result["summary"]["Food"] == 300.0
            assert result["summary"]["Transportation"] == 50.0
            # Food category exceeds 50% (300/350 > 0.5)
            assert len(result["recommendations"]) == 1
            assert "Food" in result["recommendations"][0]

    @pytest.mark.asyncio
    async def test_monthly_report_no_expenses(self, mock_splitwise_client):
        """Test monthly report with no expenses."""
        with patch("app.custom_methods.expenses_by_month") as mock_expenses_by_month:
            mock_expenses_by_month.return_value = []

            result = await monthly_report(
                mock_splitwise_client, "Test Group", "2025-10"
            )

            assert result["total"] == 0
            assert result["summary"] == {}
            assert len(result["recommendations"]) == 1
            assert "No expenses found" in result["recommendations"][0]

    @pytest.mark.asyncio
    async def test_monthly_report_various_category_formats(self, mock_splitwise_client):
        """Test handling different category formats."""
        with patch("app.custom_methods.expenses_by_month") as mock_expenses_by_month:
            mock_expenses_by_month.return_value = [
                {
                    "cost": "100.0",
                    "category": {"name": "Food"},  # Dict with name
                },
                {
                    "cost": "50.0",
                    "category": "Transportation",  # String
                },
                {
                    "cost": "75.0",
                    "category_id": 123,  # Numeric category_id
                },
                {
                    "cost": "25.0",
                    # No category info
                },
            ]

            result = await monthly_report(
                mock_splitwise_client, "Test Group", "2025-10"
            )

            assert result["summary"]["Food"] == 100.0
            assert result["summary"]["Transportation"] == 50.0
            assert result["summary"]["123"] == 75.0
            assert result["summary"]["Unknown"] == 25.0

    @pytest.mark.asyncio
    async def test_monthly_report_invalid_cost_handling(self, mock_splitwise_client):
        """Test handling invalid cost values."""
        with patch("app.custom_methods.expenses_by_month") as mock_expenses_by_month:
            mock_expenses_by_month.return_value = [
                {"cost": "100.0", "category": {"name": "Food"}},
                {
                    "cost": "invalid",  # Invalid cost
                    "category": {"name": "Transportation"},
                },
                {
                    "amount": "50.0",  # Using 'amount' instead of 'cost'
                    "category": {"name": "Entertainment"},
                },
            ]

            result = await monthly_report(
                mock_splitwise_client, "Test Group", "2025-10"
            )

            assert result["summary"]["Food"] == 100.0
            assert result["summary"]["Transportation"] == 0.0  # Invalid cost becomes 0
            assert result["summary"]["Entertainment"] == 50.0  # 'amount' field works
            assert result["total"] == 150.0

    @pytest.mark.asyncio
    async def test_monthly_report_no_high_categories(self, mock_splitwise_client):
        """Test report with no categories exceeding 50%."""
        with patch("app.custom_methods.expenses_by_month") as mock_expenses_by_month:
            mock_expenses_by_month.return_value = [
                {"cost": "40.0", "category": {"name": "Food"}},
                {"cost": "30.0", "category": {"name": "Transportation"}},
                {"cost": "30.0", "category": {"name": "Entertainment"}},
            ]

            result = await monthly_report(
                mock_splitwise_client, "Test Group", "2025-10"
            )

            assert result["total"] == 100.0
            assert len(result["recommendations"]) == 0  # No category exceeds 50%
