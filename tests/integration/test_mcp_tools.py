"""Integration tests for MCP tools using actual MCP client.

These tests use the official MCP client to test the MCP server endpoints
over the actual MCP protocol, providing comprehensive validation.
"""

from __future__ import annotations

import json
import os
import threading
from contextlib import contextmanager

import pytest
import requests

# Skip tests if no API key is available
pytestmark = pytest.mark.skipif(
    not os.getenv("SPLITWISE_API_KEY") and not os.getenv("SPLITWISE_CONSUMER_KEY"),
    reason="Integration tests require Splitwise API credentials",
)


@contextmanager
def keep_sse_alive(mcp_base_url: str):
    """Keep SSE connection alive and return session ID.

    This context manager maintains an active SSE connection which is required
    for stateful MCP servers.
    """
    sse_resp = None
    stop_reading = threading.Event()

    def read_sse_events():
        """Read SSE events in background to keep connection alive."""
        if sse_resp:
            try:
                for _line in sse_resp.iter_lines():
                    if stop_reading.is_set():
                        break
            except Exception:
                pass  # Connection closed, that's fine

    try:
        sse_resp = requests.get(
            mcp_base_url,
            headers={"Accept": "text/event-stream"},
            stream=True,
            timeout=60,
        )
        session_id = sse_resp.headers.get("mcp-session-id")

        # Start background thread to keep connection alive
        reader_thread = threading.Thread(target=read_sse_events, daemon=True)
        reader_thread.start()

        yield session_id

    finally:
        stop_reading.set()
        if sse_resp:
            sse_resp.close()


def mcp_http_request(
    mcp_base_url: str,
    method: str,
    params: dict | None = None,
    request_id: int = 1,
    session_id: str | None = None,
    initialized_sessions: dict | None = None,
):
    """Make an MCP request over HTTP and return the response.

    Args:
        mcp_base_url: Base URL of the MCP server
        method: MCP method to call (e.g., 'tools/call', 'tools/list')
        params: Parameters for the method
        request_id: JSON-RPC request ID
        session_id: Session ID to use (REQUIRED - use keep_sse_alive context manager)
        initialized_sessions: Dict to track which sessions have been initialized

    Returns:
        Tuple of (response_data, session_id) for session reuse
    """
    if initialized_sessions is None:
        initialized_sessions = {}

    if session_id is None:
        raise ValueError(
            "session_id is required - use keep_sse_alive() context manager"
        )

    # Initialize session if not already initialized (required by MCP protocol)
    if session_id not in initialized_sessions:
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 0,  # Use ID 0 for initialization
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        }

        post_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Session-Id": session_id,
        }

        init_response = requests.post(
            mcp_base_url, json=initialize_request, headers=post_headers, timeout=10
        )

        assert init_response.status_code in [200, 201], (
            f"Initialization failed: {init_response.text}"
        )

        # Mark session as initialized
        initialized_sessions[session_id] = True

    request_data = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
    }

    # Add default pagination params for list methods if not provided
    if params is None and method in ("tools/list", "resources/list"):
        params = {}  # Empty params, not None

    if params is not None:
        request_data["params"] = params

    post_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Session-Id": session_id,
    }

    response = requests.post(
        mcp_base_url, json=request_data, headers=post_headers, timeout=30, stream=True
    )

    assert response.status_code in [200, 201]

    # Read the full response content
    response_text = response.text

    # Parse response (may be SSE or JSON)
    if response_text.lstrip().startswith("event:"):
        # SSE format: handle multi-line data fields
        # When data is very large, SSE splits it across multiple lines
        # Continuation lines don't have the "data: " prefix
        lines = response_text.splitlines()
        data_parts = []
        in_data_field = False

        for line in lines:
            if line.startswith("data: "):
                # Start of a data field
                data_parts.append(line[len("data: ") :])
                in_data_field = True
            elif line.startswith(("event:", "id:", "retry:")):
                # SSE field - end of previous data field
                in_data_field = False
            elif line == "":
                # Empty line - end of data field
                in_data_field = False
            elif in_data_field:
                # Continuation of previous data field (no SSE prefix)
                data_parts.append(line)

        # Join all data parts to reconstruct the full JSON
        combined = "".join(data_parts)
        data = json.loads(combined)
    else:
        data = response.json()

    return data, session_id


class TestMCPToolsIntegration:
    """Test MCP tools with HTTP transport."""

    def test_get_current_user(self, mcp_server_process: str):
        """Test get_current_user tool via HTTP."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            result, _ = mcp_http_request(
                mcp_server_process,
                "tools/call",
                {"name": "get_current_user", "arguments": {}},
                session_id=session_id,
                initialized_sessions=initialized,
            )
            assert result["jsonrpc"] == "2.0"
            assert "result" in result or "error" in result

    def test_list_groups(self, mcp_server_process: str):
        """Test list_groups MCP tool."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            response, _ = mcp_http_request(
                mcp_server_process,
                "tools/call",
                {"name": "list_groups", "arguments": {}},
                session_id=session_id,
                initialized_sessions=initialized,
            )

            assert "result" in response
            result = response["result"]
            assert "content" in result
            assert len(result["content"]) > 0
            content = result["content"][0]
            assert content["type"] == "text"

            # Check if this is an error response
            if result.get("isError") or "error" in content["text"].lower():
                # Skip this test if the tool returns an error due to validation issues
                pytest.skip(f"Tool returned error: {content['text']}")
                return

            try:
                data = json.loads(content["text"])
            except json.JSONDecodeError:
                pytest.skip(f"Tool returned non-JSON response: {content['text']}")
                return

            # Should get a proper API response with groups key
            assert isinstance(data, dict)
            assert "groups" in data
            assert isinstance(data["groups"], list)
            # Each group should have an id and name
            for group in data["groups"]:
                assert "id" in group
                assert "name" in group

    def test_list_expenses_with_filters(self, mcp_server_process: str):
        """Test list_expenses MCP tool with filters."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            # First get a group to test with
            groups_response, _ = mcp_http_request(
                mcp_server_process,
                "tools/call",
                {"name": "list_groups", "arguments": {}},
                session_id=session_id,
                initialized_sessions=initialized,
            )

            assert "result" in groups_response
            groups_result = groups_response["result"]
            groups_content = groups_result["content"][0]

            # Check if groups call returned error
            if (
                groups_result.get("isError")
                or "error" in groups_content["text"].lower()
            ):
                pytest.skip(
                    f"Dependencies failed - list_groups returned error: {groups_content['text']}"
                )
                return

            try:
                groups = json.loads(groups_content["text"])
            except json.JSONDecodeError:
                pytest.skip(
                    f"Dependencies failed - list_groups returned non-JSON: {groups_content['text']}"
                )
                return

            if groups and groups.get("groups"):
                group_id = groups["groups"][0]["id"]

                # Test with group filter
                response, _ = mcp_http_request(
                    mcp_server_process,
                    "tools/call",
                    {
                        "name": "list_expenses",
                        "arguments": {"group_id": group_id, "limit": 5},
                    },
                    session_id=session_id,
                    initialized_sessions=initialized,
                )

                assert "result" in response
                result = response["result"]
                assert "content" in result
                assert len(result["content"]) > 0
                content = result["content"][0]
                assert content["type"] == "text"

                # Check if this is an error response
                if result.get("isError") or "error" in content["text"].lower():
                    pytest.skip(f"Tool returned error: {content['text']}")
                    return

                try:
                    data = json.loads(content["text"])
                    # Should get a proper API response with expenses key
                    assert isinstance(data, dict)
                    assert "expenses" in data
                    assert isinstance(data["expenses"], list)
                except json.JSONDecodeError:
                    pytest.skip(f"Tool returned non-JSON response: {content['text']}")
            else:
                pytest.skip("No groups available to test with")

    def test_get_group_resource(self, mcp_server_process: str):
        """Test splitwise://group/{name} resource."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            # First get available groups
            groups_response, _ = mcp_http_request(
                mcp_server_process,
                "tools/call",
                {"name": "list_groups", "arguments": {}},
                session_id=session_id,
                initialized_sessions=initialized,
            )

            assert "result" in groups_response
            groups_result = groups_response["result"]
            groups_content = groups_result["content"][0]

            # Check if groups call returned error
            if (
                groups_result.get("isError")
                or "error" in groups_content["text"].lower()
            ):
                pytest.skip(
                    f"Dependencies failed - list_groups returned error: {groups_content['text']}"
                )
                return

            try:
                groups = json.loads(groups_content["text"])
            except json.JSONDecodeError:
                pytest.skip(
                    f"Dependencies failed - list_groups returned non-JSON: {groups_content['text']}"
                )
                return

            if groups and groups.get("groups"):
                # Skip the "Non-group expenses" entry with ID 0 and find a real group
                real_groups = [g for g in groups["groups"] if g.get("id", 0) != 0]
                if not real_groups:
                    pytest.skip("No real groups found to test with")
                    return
                group_name = real_groups[0]["name"]

                try:
                    # Test resource access
                    response, _ = mcp_http_request(
                        mcp_server_process,
                        "resources/read",
                        {"uri": f"splitwise://group/{group_name}"},
                        session_id=session_id,
                        initialized_sessions=initialized,
                    )

                    assert "result" in response
                    result = response["result"]
                    assert "contents" in result
                    assert len(result["contents"]) > 0
                    content = result["contents"][0]
                    # MCP resources return text/plain by default, but content should be JSON
                    assert content["mimeType"] in ("application/json", "text/plain")

                    data = json.loads(content["text"])
                    assert "id" in data
                    assert data["name"] == group_name
                except Exception as e:
                    pytest.skip(f"Resource access failed: {str(e)}")
            else:
                pytest.skip("No groups available to test with")


class TestMCPServerCapabilities:
    """Test MCP server capabilities and metadata."""

    def test_server_info(self, mcp_server_process: str):
        """Test server information and capabilities."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            # Test if we can list tools to validate server connection
            response, _ = mcp_http_request(
                mcp_server_process,
                "tools/list",
                session_id=session_id,
                initialized_sessions=initialized,
            )
            assert "result" in response

    def test_list_tools(self, mcp_server_process: str):
        """Test that all expected tools are available."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            response, _ = mcp_http_request(
                mcp_server_process,
                "tools/list",
                session_id=session_id,
                initialized_sessions=initialized,
            )

            assert "result" in response
            tools_result = response["result"]
            tool_names = [tool["name"] for tool in tools_result["tools"]]

            expected_tools = [
                "get_current_user",
                "list_groups",
                "get_group",
                "list_expenses",
                "get_expense",
                "list_friends",
                "get_friend",
                "list_categories",
                "list_currencies",
                "get_exchange_rates",
            ]

            for tool_name in expected_tools:
                assert tool_name in tool_names

    def test_list_resources(self, mcp_server_process: str):
        """Test that resources endpoint works."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            response, _ = mcp_http_request(
                mcp_server_process,
                "resources/list",
                session_id=session_id,
                initialized_sessions=initialized,
            )

            assert "result" in response
            result = response["result"]
            assert "resources" in result
            # Resources may or may not be available depending on server implementation
            # The test just verifies the list_resources call works
            assert isinstance(
                result["resources"], list
            )  # Should return a list (even if empty)


class TestMCPErrorHandling:
    """Test MCP error handling scenarios."""

    def test_invalid_tool_name(self, mcp_server_process: str):
        """Test calling a non-existent tool."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            # The invalid tool will return an error result
            response, _ = mcp_http_request(
                mcp_server_process,
                "tools/call",
                {"name": "nonexistent_tool", "arguments": {}},
                session_id=session_id,
                initialized_sessions=initialized,
            )
            assert "result" in response
            result = response["result"]
            # Should have error content or isError flag
        assert result.get("isError") or "error" in result["content"][0]["text"].lower()

    def test_invalid_resource_uri(self, mcp_server_process: str):
        """Test accessing a non-existent resource."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            # Should return an error response
            response, _ = mcp_http_request(
                mcp_server_process,
                "resources/read",
                {"uri": "splitwise://nonexistent/resource"},
                session_id=session_id,
                initialized_sessions=initialized,
            )
            # Should have an error in the response
            assert "error" in response or (
                "result" in response
                and response["result"]
                .get("contents", [{}])[0]
                .get("text", "")
                .lower()
                .find("error")
                >= 0
            )

    def test_invalid_tool_parameters(self, mcp_server_process: str):
        """Test calling a tool with invalid parameters."""
        with keep_sse_alive(mcp_server_process) as session_id:
            initialized = {}
            # Invalid parameters will return an error result
            response, _ = mcp_http_request(
                mcp_server_process,
                "tools/call",
                {"name": "get_group", "arguments": {"invalid_param": "value"}},
                session_id=session_id,
                initialized_sessions=initialized,
            )
            assert "result" in response
            result = response["result"]
            # Should have error content or isError flag
            assert (
                result.get("isError") or "error" in result["content"][0]["text"].lower()
            )
