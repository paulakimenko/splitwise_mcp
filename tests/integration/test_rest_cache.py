"""Integration tests for REST cache endpoints.

These tests validate that the cached REST endpoints work correctly
after MCP operations have populated the database.
"""

import pytest
from fastapi.testclient import TestClient


class TestRESTCacheIntegration:
    """Test REST cache endpoints after MCP operations."""

    @pytest.mark.asyncio
    async def test_cache_workflow(self, test_client: TestClient):
        """Test the complete workflow: MCP call -> cache -> REST endpoint."""

        # Step 1: Make MCP call to populate cache
        mcp_response = test_client.post("/mcp/list_groups", json={})
        assert mcp_response.status_code == 200

        # Step 2: Check that cache endpoint returns data
        cache_response = test_client.get("/groups")
        assert cache_response.status_code == 200

        # The cache should contain the same data as the MCP call
        mcp_data = mcp_response.json()
        cache_data = cache_response.json()
        assert cache_data == mcp_data

    @pytest.mark.asyncio
    async def test_expenses_cache_workflow(self, test_client: TestClient):
        """Test expenses cache workflow."""

        # Make MCP call to populate expenses cache
        mcp_response = test_client.post("/mcp/list_expenses", json={})
        assert mcp_response.status_code == 200

        # Check cached expenses endpoint
        cache_response = test_client.get("/expenses")
        assert cache_response.status_code == 200

        # Verify data consistency
        mcp_data = mcp_response.json()
        cache_data = cache_response.json()
        assert cache_data == mcp_data

    @pytest.mark.asyncio
    async def test_friends_cache_workflow(self, test_client: TestClient):
        """Test friends cache workflow."""

        # Make MCP call to populate friends cache
        mcp_response = test_client.post("/mcp/get_friends", json={})
        assert mcp_response.status_code == 200

        # Check cached friends endpoint
        cache_response = test_client.get("/friends")
        assert cache_response.status_code == 200

        # Verify data consistency
        mcp_data = mcp_response.json()
        cache_data = cache_response.json()
        assert cache_data == mcp_data

    @pytest.mark.asyncio
    async def test_logs_endpoint(self, test_client: TestClient):
        """Test that operations are properly logged."""

        # Make some MCP calls to generate logs
        test_client.post("/mcp/get_current_user", json={})
        test_client.post("/mcp/list_groups", json={})

        # Check logs endpoint
        response = test_client.get("/logs")
        assert response.status_code == 200

        logs = response.json()
        assert isinstance(logs, list)
        # Should have at least the operations we just made
        assert len(logs) >= 2

        # Verify log structure
        for log in logs[:2]:  # Check first 2 logs
            assert "endpoint" in log
            assert "method" in log
            assert "timestamp" in log
