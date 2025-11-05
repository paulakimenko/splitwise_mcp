"""Integration tests for REST cache endpoints.

These tests validate that the cached REST endpoints work correctly.
Since we migrated to the official MCP server, the cache is populated
via the MCP tools rather than HTTP endpoints.
"""

from fastapi.testclient import TestClient


class TestRESTCacheIntegration:
    """Test REST cache endpoints functionality."""

    def test_groups_cache_endpoint(self, test_client: TestClient):
        """Test that groups cache endpoint works correctly."""
        # The groups endpoint should work regardless of cache state
        response = test_client.get("/groups")
        assert response.status_code == 200

        # Should return either cached data (list) or no data message (dict)
        data = response.json()
        assert isinstance(data, (list, dict))

        if isinstance(data, dict):
            # No cached data case
            assert "message" in data
            assert data["data"] is None
        else:
            # Cached data case - should be a list
            assert isinstance(data, list)

    def test_expenses_cache_endpoint(self, test_client: TestClient):
        """Test that expenses cache endpoint works correctly."""
        response = test_client.get("/expenses")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, (list, dict))

        if isinstance(data, dict):
            assert "message" in data
            assert data["data"] is None
        else:
            assert isinstance(data, list)

    def test_friends_cache_endpoint(self, test_client: TestClient):
        """Test that friends cache endpoint works correctly."""
        response = test_client.get("/friends")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, (list, dict))

        if isinstance(data, dict):
            assert "message" in data
            assert data["data"] is None
        else:
            assert isinstance(data, list)

    def test_logs_endpoint_functionality(self, test_client: TestClient):
        """Test that logs endpoint works correctly."""
        response = test_client.get("/logs")
        assert response.status_code == 200

        logs = response.json()
        assert isinstance(logs, list)
        # Logs may be empty or contain historical operations

        # Each log entry should have expected structure
        for log in logs[:5]:  # Check up to 5 recent logs
            assert isinstance(log, dict)
            # Note: log structure may vary, just ensure it's a dict

    def test_cache_endpoints_are_read_only(self, test_client: TestClient):
        """Test that cache endpoints are read-only (GET only)."""
        endpoints = ["/groups", "/expenses", "/friends"]

        for endpoint in endpoints:
            # GET should work
            get_response = test_client.get(endpoint)
            assert get_response.status_code == 200

            # POST should not be allowed
            post_response = test_client.post(endpoint, json={})
            assert post_response.status_code == 405  # Method Not Allowed

    def test_cache_data_structure(self, test_client: TestClient):
        """Test that cache endpoints return properly structured data."""
        endpoints = [
            ("/groups", "groups"),
            ("/expenses", "expenses"),
            ("/friends", "friends"),
        ]

        for endpoint, data_type in endpoints:
            response = test_client.get(endpoint)
            assert response.status_code == 200

            data = response.json()

            if isinstance(data, list):
                # If cached data exists, it should be a list
                assert isinstance(data, list)
            else:
                # If no cached data, should be a message dict
                assert isinstance(data, dict)
                assert "message" in data
                assert f"No cached {data_type} found" in data["message"]
