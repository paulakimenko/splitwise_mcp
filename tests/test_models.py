"""Tests for app.models module."""

import pytest
from pydantic import ValidationError

from app.models import (
    MCPCallRequest,
    AddExpenseEqualSplitRequest,
    MonthlyReportRequest,
    GenericResponse
)


class TestMCPCallRequest:
    """Test MCPCallRequest model."""
    
    def test_empty_args(self):
        """Test creating request with empty args."""
        request = MCPCallRequest()
        assert request.args == {}
    
    def test_with_args(self):
        """Test creating request with args."""
        args = {"param1": "value1", "param2": 123}
        request = MCPCallRequest(args=args)
        assert request.args == args


class TestAddExpenseEqualSplitRequest:
    """Test AddExpenseEqualSplitRequest model."""
    
    def test_valid_request(self):
        """Test creating valid expense request."""
        request = AddExpenseEqualSplitRequest(
            group_name="Test Group",
            amount=100.50,
            currency_code="uah",
            participant_name="John Doe",
            description="Test expense"
        )
        assert request.group_name == "Test Group"
        assert request.amount == 100.50
        assert request.currency_code == "UAH"  # Should be uppercase
        assert request.participant_name == "John Doe"
        assert request.description == "Test expense"
    
    def test_currency_code_uppercase(self):
        """Test that currency code is converted to uppercase."""
        request = AddExpenseEqualSplitRequest(
            group_name="Test Group",
            amount=50.0,
            currency_code="usd",
            participant_name="Jane",
            description="Test"
        )
        assert request.currency_code == "USD"
    
    def test_missing_required_fields(self):
        """Test validation errors for missing fields."""
        with pytest.raises(ValidationError):
            AddExpenseEqualSplitRequest()
    
    def test_invalid_amount_type(self):
        """Test validation error for invalid amount type."""
        with pytest.raises(ValidationError):
            AddExpenseEqualSplitRequest(
                group_name="Test",
                amount="invalid",
                currency_code="USD",
                participant_name="John",
                description="Test"
            )


class TestMonthlyReportRequest:
    """Test MonthlyReportRequest model."""
    
    def test_valid_request(self):
        """Test creating valid monthly report request."""
        request = MonthlyReportRequest(
            group_name="Test Group",
            month="2025-10"
        )
        assert request.group_name == "Test Group"
        assert request.month == "2025-10"
    
    def test_missing_fields(self):
        """Test validation errors for missing fields."""
        with pytest.raises(ValidationError):
            MonthlyReportRequest()


class TestGenericResponse:
    """Test GenericResponse model."""
    
    def test_response_with_data(self):
        """Test creating response with data."""
        data = {"key": "value"}
        response = GenericResponse(message="Success", data=data)
        assert response.message == "Success"
        assert response.data == data
    
    def test_response_without_data(self):
        """Test creating response without data."""
        response = GenericResponse(message="No data found")
        assert response.message == "No data found"
        assert response.data is None