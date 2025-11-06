"""Streamable HTTP transport integration tests.

These tests validate the MCP server over Streamable HTTP transport,
testing remote connectivity and MCP protocol compliance.
"""

from __future__ import annotations

import os

import pytest
import requests

# Skip tests if no API key is available
pytestmark = pytest.mark.skipif(
    not os.getenv("SPLITWISE_API_KEY") and not os.getenv("SPLITWISE_CONSUMER_KEY"),
    reason="Integration tests require Splitwise API credentials",
)


class TestStreamableHTTPTransport:
    """Test MCP server functionality via Streamable HTTP transport."""

    @pytest.fixture
    def mcp_base_url(self) -> str:
        """Base URL for the MCP server using Streamable HTTP transport."""
        return os.getenv("MCP_BASE_URL", "http://localhost:8000/mcp")

    def _check_mcp_server_available(self, mcp_base_url: str) -> bool:
        """Check if MCP server is available via Streamable HTTP transport."""
        try:
            # Try to make a simple MCP initialize request
            response = requests.post(
                mcp_base_url,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "test-client", "version": "1.0.0"},
                    },
                },
                headers={"Content-Type": "application/json"},
                timeout=5,
            )
            return response.status_code in [200, 201]
        except requests.exceptions.ConnectionError:
            return False

    def test_mcp_initialize(self, mcp_base_url: str):
        """Test MCP initialization over Streamable HTTP transport."""
        if not self._check_mcp_server_available(mcp_base_url):
            pytest.skip(
                "MCP server not available - tests require a running MCP server with Streamable HTTP transport"
            )

        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        }

        response = requests.post(
            mcp_base_url,
            json=initialize_request,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        assert "result" in data

    def test_mcp_list_tools(self, mcp_base_url: str):
        """Test listing MCP tools via Streamable HTTP transport."""
        if not self._check_mcp_server_available(mcp_base_url):
            pytest.skip(
                "MCP server not available - tests require a running MCP server with Streamable HTTP transport"
            )

        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        }

        response = requests.post(
            mcp_base_url,
            json=list_tools_request,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 2
        assert "result" in data
        assert "tools" in data["result"]

        # Should have MCP tools defined in the server
        tools = data["result"]["tools"]
        assert len(tools) > 0

        # Check for some expected tools
        tool_names = [tool["name"] for tool in tools]
        assert "create_expense" in tool_names
        assert "list_groups" in tool_names

    def test_mcp_list_resources(self, mcp_base_url: str):
        """Test listing MCP resources via Streamable HTTP transport."""
        if not self._check_mcp_server_available(mcp_base_url):
            pytest.skip(
                "MCP server not available - tests require a running MCP server with Streamable HTTP transport"
            )

        list_resources_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {},
        }

        response = requests.post(
            mcp_base_url,
            json=list_resources_request,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 3
        assert "result" in data
        assert "resources" in data["result"]

        # Should have MCP resources defined in the server
        resources = data["result"]["resources"]
        assert len(resources) > 0

        # Check for some expected resources
        resource_uris = [resource["uri"] for resource in resources]
        assert "splitwise://current_user" in resource_uris
        assert "splitwise://groups" in resource_uris

    def test_mcp_call_tool(self, mcp_base_url: str):
        """Test calling an MCP tool via Streamable HTTP transport."""
        if not self._check_mcp_server_available(mcp_base_url):
            pytest.skip(
                "MCP server not available - tests require a running MCP server with Streamable HTTP transport"
            )

        # Test calling get_current_user tool
        call_tool_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "get_current_user", "arguments": {}},
        }

        response = requests.post(
            mcp_base_url,
            json=call_tool_request,
            headers={"Content-Type": "application/json"},
            timeout=10,  # Longer timeout for API calls
        )

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 4

        # Tool call should succeed (may return error if API key invalid)
        if "result" in data:
            assert "content" in data["result"]
        elif "error" in data:
            # API error is acceptable for testing transport
            assert "code" in data["error"]

    def test_mcp_read_resource(self, mcp_base_url: str):
        """Test reading an MCP resource via Streamable HTTP transport."""
        if not self._check_mcp_server_available(mcp_base_url):
            pytest.skip(
                "MCP server not available - tests require a running MCP server with Streamable HTTP transport"
            )

        # Test reading current_user resource
        read_resource_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "resources/read",
            "params": {"uri": "splitwise://current_user"},
        }

        response = requests.post(
            mcp_base_url,
            json=read_resource_request,
            headers={"Content-Type": "application/json"},
            timeout=10,  # Longer timeout for API calls
        )

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 5

        # Resource read should succeed (may return error if API key invalid)
        if "result" in data:
            assert "contents" in data["result"]
        elif "error" in data:
            # API error is acceptable for testing transport
            assert "code" in data["error"]

    def test_mcp_protocol_compliance(self, mcp_base_url: str):
        """Test that the server follows MCP protocol correctly."""
        if not self._check_mcp_server_available(mcp_base_url):
            pytest.skip(
                "MCP server not available - tests require a running MCP server with Streamable HTTP transport"
            )

        # Test invalid method
        invalid_request = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "invalid/method",
            "params": {},
        }

        response = requests.post(
            mcp_base_url,
            json=invalid_request,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 6
        assert "error" in data
        assert data["error"]["code"] == -32601  # Method not found
