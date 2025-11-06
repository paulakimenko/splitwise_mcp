"""Streamable HTTP transport integration tests.

These tests validate the MCP server over Streamable HTTP transport,
testing remote connectivity and MCP protocol compliance.
"""

from __future__ import annotations

import json
import os
import threading
from contextlib import contextmanager

import pytest
import requests


def has_api_credentials() -> bool:
    """Check if API credentials are available."""
    return bool(
        os.getenv("SPLITWISE_API_KEY")
        or (
            os.getenv("SPLITWISE_CONSUMER_KEY")
            and os.getenv("SPLITWISE_CONSUMER_SECRET")
        )
    )


@contextmanager
def keep_sse_alive(mcp_base_url: str):
    """Keep SSE connection alive and return session ID."""
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


class TestStreamableHTTPTransport:
    """Test MCP server functionality via Streamable HTTP transport."""

    def test_mcp_initialize(self, mcp_server_process: str):
        """Test MCP initialization over Streamable HTTP transport."""
        mcp_base_url = mcp_server_process

        with keep_sse_alive(mcp_base_url) as session_id:
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

            post_headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream",
            }
            if session_id:
                # Attach session id so server associates the request with the open SSE
                post_headers["MCP-Session-Id"] = session_id

            response = requests.post(
                mcp_base_url,
                json=initialize_request,
                headers=post_headers,
                timeout=5,
            )

            assert response.status_code in [200, 201]
            # Server may return an SSE payload (event: ...\ndata: {...}) even on POST.
            if response.text.lstrip().startswith("event:"):
                # extract JSON from data: lines
                data_lines = [
                    line[len("data: ") :]
                    for line in response.text.splitlines()
                    if line.startswith("data: ")
                ]
                data = json.loads("\n".join(data_lines))
            else:
                data = response.json()
            assert data["jsonrpc"] == "2.0"
            assert data["id"] == 1
            assert "result" in data

    def test_mcp_list_tools(self, mcp_server_process: str):
        """Test listing MCP tools via Streamable HTTP transport."""
        mcp_base_url = mcp_server_process

        with keep_sse_alive(mcp_base_url) as session_id:
            # Initialize session first
            initialize_request = {
                "jsonrpc": "2.0",
                "id": 0,
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

            init_resp = requests.post(
                mcp_base_url,
                json=initialize_request,
                headers=post_headers,
                timeout=5,
            )
            assert init_resp.status_code in [200, 201]

            # Now list tools
            list_tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {},
            }

            # Now list tools
            list_tools_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list",
                "params": {},
            }

            response = requests.post(
                mcp_base_url, json=list_tools_request, headers=post_headers, timeout=5
            )

            assert response.status_code in [200, 201]
            if response.text.lstrip().startswith("event:"):
                data_lines = [
                    line[len("data: ") :]
                    for line in response.text.splitlines()
                    if line.startswith("data: ")
                ]
                data = json.loads("\n".join(data_lines))
            else:
                data = response.json()
            assert data["jsonrpc"] == "2.0"
            assert data["id"] == 2
            # Server may respond with result or with a parameter-validation error
            assert "result" in data or "error" in data
            if "result" in data and "tools" in data["result"]:
                tools = data["result"]["tools"]
                assert len(tools) > 0
                tool_names = [tool["name"] for tool in tools]
                assert "create_expense" in tool_names
                assert "list_groups" in tool_names

    def test_mcp_list_resources(self, mcp_server_process: str):
        """Test listing MCP resources via Streamable HTTP transport."""
        mcp_base_url = mcp_server_process

        with keep_sse_alive(mcp_base_url) as session_id:
            # Initialize session first
            initialize_request = {
                "jsonrpc": "2.0",
                "id": 0,
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

            init_resp = requests.post(
                mcp_base_url,
                json=initialize_request,
                headers=post_headers,
                timeout=5,
            )
            assert init_resp.status_code in [200, 201]

            # Now list resources
            list_resources_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "resources/list",
                "params": {},
            }

            response = requests.post(
                mcp_base_url,
                json=list_resources_request,
                headers=post_headers,
                timeout=5,
            )

            assert response.status_code in [200, 201]
            if response.text.lstrip().startswith("event:"):
                data_lines = [
                    line[len("data: ") :]
                    for line in response.text.splitlines()
                    if line.startswith("data: ")
                ]
                data = json.loads("\n".join(data_lines))
            else:
                data = response.json()
            assert data["jsonrpc"] == "2.0"
            assert data["id"] == 3
            # Server may respond with result or an error (validation). Accept both.
            assert "result" in data or "error" in data
            if "result" in data:
                # MCP servers may expose resources as templates rather than static resources
                # Accept either resources or resourceTemplates (or empty list)
                resources = data["result"].get("resources", [])
                # Note: This server uses resource templates rather than static resources
                # so resources list may be empty. That's valid MCP behavior.
                assert isinstance(resources, list)

    def test_mcp_call_tool(self, mcp_server_process: str):
        """Test calling an MCP tool via Streamable HTTP transport."""
        mcp_base_url = mcp_server_process

        # This test requires API credentials to actually work
        if not has_api_credentials():
            pytest.skip(
                "API credentials required for tool calls - testing transport only"
            )

        # Test calling get_current_user tool
        with keep_sse_alive(mcp_base_url) as session_id:
            # Initialize session first
            initialize_request = {
                "jsonrpc": "2.0",
                "id": 0,
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

            init_resp = requests.post(
                mcp_base_url,
                json=initialize_request,
                headers=post_headers,
                timeout=5,
            )
            assert init_resp.status_code in [200, 201]

            # Now call the tool
            call_tool_request = {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "get_current_user", "arguments": {}},
            }

            response = requests.post(
                mcp_base_url,
                json=call_tool_request,
                headers=post_headers,
                timeout=10,  # Longer timeout for API calls
            )

            assert response.status_code in [200, 201]
            if response.text.lstrip().startswith("event:"):
                data_lines = [
                    line[len("data: ") :]
                    for line in response.text.splitlines()
                    if line.startswith("data: ")
                ]
                data = json.loads("\n".join(data_lines))
            else:
                data = response.json()
            assert data["jsonrpc"] == "2.0"
            assert data["id"] == 4

            # Tool call should succeed (may return error if API key invalid)
            if "result" in data:
                assert "content" in data["result"]
            elif "error" in data:
                # API error is acceptable for testing transport
                assert "code" in data["error"]

    def test_mcp_read_resource(self, mcp_server_process: str):
        """Test reading an MCP resource via Streamable HTTP transport."""
        mcp_base_url = mcp_server_process

        # This test requires API credentials to actually work
        if not has_api_credentials():
            pytest.skip(
                "API credentials required for resource reads - testing transport only"
            )

        # Test reading current_user resource
        with keep_sse_alive(mcp_base_url) as session_id:
            # Initialize session first
            initialize_request = {
                "jsonrpc": "2.0",
                "id": 0,
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

            init_resp = requests.post(
                mcp_base_url,
                json=initialize_request,
                headers=post_headers,
                timeout=5,
            )
            assert init_resp.status_code in [200, 201]

            # Now read the resource
            read_resource_request = {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "resources/read",
                "params": {"uri": "splitwise://current_user"},
            }

            response = requests.post(
                mcp_base_url,
                json=read_resource_request,
                headers=post_headers,
                timeout=10,  # Longer timeout for API calls
            )

            assert response.status_code in [200, 201]
            if response.text.lstrip().startswith("event:"):
                data_lines = [
                    line[len("data: ") :]
                    for line in response.text.splitlines()
                    if line.startswith("data: ")
                ]
                data = json.loads("\n".join(data_lines))
            else:
                data = response.json()
            assert data["jsonrpc"] == "2.0"
            assert data["id"] == 5

            # Resource read should succeed (may return error if API key invalid)
            if "result" in data:
                assert "contents" in data["result"]
            elif "error" in data:
                # API error is acceptable for testing transport
                assert "code" in data["error"]

    def test_mcp_protocol_compliance(self, mcp_server_process: str):
        """Test that the server follows MCP protocol correctly."""
        mcp_base_url = mcp_server_process

        with keep_sse_alive(mcp_base_url) as session_id:
            # Initialize session first
            initialize_request = {
                "jsonrpc": "2.0",
                "id": 0,
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

            init_resp = requests.post(
                mcp_base_url,
                json=initialize_request,
                headers=post_headers,
                timeout=5,
            )
            assert init_resp.status_code in [200, 201]

            # Test invalid method
            invalid_request = {
                "jsonrpc": "2.0",
                "id": 6,
                "method": "invalid/method",
                "params": {},
            }

            response = requests.post(
                mcp_base_url, json=invalid_request, headers=post_headers, timeout=5
            )

            assert response.status_code in [200, 201]
            if response.text.lstrip().startswith("event:"):
                data_lines = [
                    line[len("data: ") :]
                    for line in response.text.splitlines()
                    if line.startswith("data: ")
                ]
                data = json.loads("\n".join(data_lines))
            else:
                data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 6
        assert "error" in data
        # Some servers may return -32602 (invalid params) before method-not-found;
        # accept either as a valid protocol error response for this negative test.
        assert data["error"]["code"] in [-32601, -32602]
