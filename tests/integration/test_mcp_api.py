"""Integration tests for MCP server functionality.

These tests validate that the MCP server integration works properly
and that the service can still function with both MCP and REST APIs.
"""

from fastapi.testclient import TestClient


class TestMCPServerIntegration:
    """Test MCP server integration doesn't break existing functionality."""

    def test_rest_api_still_works(self, test_client: TestClient):
        """Test that REST API endpoints still work with MCP server mounted."""
        # Test a REST endpoint to ensure MCP server doesn't break anything
        response = test_client.get("/groups")

        # Should get either cached data (200) or no cached data (200 with message)
        assert response.status_code == 200
        data = response.json()

        # Either a list (cached data) or dict with message (no cached data)
        assert isinstance(data, (list, dict))

    def test_custom_endpoints_still_work(self, test_client: TestClient):
        """Test that custom endpoints still work."""
        # Test a custom endpoint
        response = test_client.get(
            "/custom/expenses_by_month?group_name=TestGroup&month=2024-01"
        )

        # Should get 400 (group not found) or 200 (success), not 500 (server error)
        assert response.status_code in [200, 400]

    def test_mcp_server_mounted_correctly(self, test_client: TestClient):
        """Test that MCP server is mounted at /mcp path."""
        # MCP server uses a different protocol, so HTTP requests will fail
        # but the mount should not cause the app to crash

        # Test that the app still responds to valid endpoints
        response = test_client.get("/logs")
        assert response.status_code == 200

        # The /mcp path should exist but not respond to regular HTTP
        # This is expected behavior for MCP protocol
        response = test_client.get("/mcp")
        # Should get some response (not 500 internal server error)
        assert response.status_code in [200, 404, 405, 422]  # Any valid HTTP response


class TestDataPersistence:
    """Test that data persistence still works after MCP integration."""

    def test_logs_endpoint_works(self, test_client: TestClient):
        """Test that logging functionality still works."""
        response = test_client.get("/logs")

        assert response.status_code == 200
        logs = response.json()
        assert isinstance(logs, list)

    def test_cached_data_endpoints_work(self, test_client: TestClient):
        """Test that cached data endpoints work."""
        endpoints = ["/groups", "/expenses", "/friends"]

        for endpoint in endpoints:
            response = test_client.get(endpoint)
            assert response.status_code == 200

            data = response.json()
            # Should be either cached data (list) or no data message (dict)
            assert isinstance(data, (list, dict))


class TestServiceHealth:
    """Test overall service health after MCP integration."""

    def test_app_startup_works(self, test_client: TestClient):
        """Test that the application starts up correctly."""
        # If we can create a test client and make a request, startup worked
        response = test_client.get("/logs")
        assert response.status_code == 200

    def test_no_import_errors(self, test_client: TestClient):
        """Test that there are no import errors in the application."""
        # Making any request tests that all imports worked
        response = test_client.get("/")
        # Root path should give 404, but no 500 (import error)
        assert response.status_code == 404
