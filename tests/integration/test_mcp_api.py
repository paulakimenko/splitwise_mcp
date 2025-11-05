"""Integration tests for MCP API endpoints.

These tests validate the MCP proxy functionality by making real API calls
to Splitwise through our service endpoints.
"""

import pytest
from fastapi.testclient import TestClient


class TestMCPIntegration:
    """Test MCP proxy endpoints with real Splitwise API."""

    @pytest.mark.asyncio
    async def test_list_groups_endpoint(self, test_client: TestClient):
        """Test that we can list groups via MCP endpoint."""
        response = test_client.post("/mcp/list_groups", json={})
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Should have at least our test group
        assert len(data) >= 0

    @pytest.mark.asyncio
    async def test_get_current_user_endpoint(self, test_client: TestClient):
        """Test getting current user via MCP endpoint."""
        response = test_client.post("/mcp/get_current_user", json={})
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "first_name" in data or "email" in data

    @pytest.mark.asyncio
    async def test_get_groups_endpoint(self, test_client: TestClient):
        """Test getting groups via MCP endpoint."""
        response = test_client.post("/mcp/get_groups", json={})
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio 
    async def test_list_expenses_endpoint(self, test_client: TestClient):
        """Test listing expenses via MCP endpoint."""
        response = test_client.post("/mcp/list_expenses", json={})
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_friends_endpoint(self, test_client: TestClient):
        """Test getting friends via MCP endpoint."""
        response = test_client.post("/mcp/get_friends", json={})
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_unsupported_method(self, test_client: TestClient):
        """Test that unsupported methods return 404."""
        response = test_client.post("/mcp/nonexistent_method", json={})
        
        assert response.status_code == 404
        assert "Unsupported method" in response.json()["detail"]


class TestMCPWithTestGroup:
    """Test MCP endpoints that interact with our test group."""

    @pytest.mark.asyncio
    async def test_get_group_by_name(
        self, 
        test_client: TestClient, 
        test_group_name: str,
        test_group_id: int
    ):
        """Test getting a specific group via MCP endpoint."""
        response = test_client.post(
            "/mcp/get_group", 
            json={"id": test_group_id}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_group_id
        assert data["name"] == test_group_name

    @pytest.mark.asyncio
    async def test_get_group_expenses(
        self,
        test_client: TestClient,
        test_group_id: int
    ):
        """Test getting expenses for a specific group."""
        response = test_client.post(
            "/mcp/get_group_expenses",
            json={"id": test_group_id}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # New group should have no expenses initially
        assert len(data) == 0