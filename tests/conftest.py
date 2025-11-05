"""Test configuration and fixtures."""

import pytest
from unittest.mock import Mock, MagicMock, patch
import asyncio
from typing import Any, Dict

from app.splitwise_client import SplitwiseClient


@pytest.fixture
def mock_splitwise_sdk():
    """Mock the Splitwise SDK."""
    mock_sdk = Mock()
    mock_sdk.getCurrentUser.return_value = Mock(id=12345, first_name="Test", last_name="User")
    mock_sdk.getGroups.return_value = [
        Mock(id=1, name="Test Group", members=[
            Mock(id=12345, first_name="Test", last_name="User"),
            Mock(id=67890, first_name="John", last_name="Doe")
        ])
    ]
    mock_sdk.getExpenses.return_value = [
        Mock(id=1, cost="100.0", description="Test expense", group_id=1, date="2025-10-15")
    ]
    mock_sdk.createExpense.return_value = Mock(id=2, cost="50.0", description="New expense")
    return mock_sdk


@pytest.fixture
def mock_splitwise_client(mock_splitwise_sdk):
    """Mock SplitwiseClient with mocked SDK."""
    with patch('app.splitwise_client.Splitwise') as mock_splitwise_class:
        mock_splitwise_class.return_value = mock_splitwise_sdk
        client = SplitwiseClient(api_key="test_key")
        return client


@pytest.fixture
def mock_db():
    """Mock MongoDB operations."""
    mock_db_client = MagicMock()
    mock_collection = Mock()
    mock_db_client.__getitem__.return_value = mock_collection
    
    with patch('app.db.get_client') as mock_get_client:
        mock_get_client.return_value = Mock()
        with patch('app.db.get_db') as mock_get_db:
            mock_get_db.return_value = mock_db_client
            yield mock_db_client


@pytest.fixture
def sample_expenses():
    """Sample expense data for testing."""
    return [
        {
            "id": 1,
            "cost": "100.0",
            "description": "Groceries",
            "group_id": 1,
            "date": "2025-10-15",
            "category": {"name": "Food"}
        },
        {
            "id": 2,
            "cost": "50.0",
            "description": "Gas",
            "group_id": 1,
            "date": "2025-10-20",
            "category": {"name": "Transportation"}
        }
    ]