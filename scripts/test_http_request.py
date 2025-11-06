#!/usr/bin/env python3
"""Test script to manually send HTTP requests to the MCP server."""

import json

import requests

BASE_URL = "http://localhost:8000/mcp"


def test_mcp_request():
    """Test MCP HTTP request flow."""
    print("=== Testing MCP HTTP Request Flow ===\n")

    # Step 1: Open SSE connection to get session ID from headers
    print("Step 1: Opening SSE connection...")
    response = requests.get(
        BASE_URL, headers={"Accept": "text/event-stream"}, stream=True, timeout=10
    )

    session_id = response.headers.get("mcp-session-id") or response.headers.get(
        "MCP-Session-Id"
    )

    print(f"Response headers: {dict(response.headers)}")
    print(f"Session ID: {session_id}\n")

    if not session_id:
        print("✗ Failed to get session ID from headers")
        return

    print(f"✓ Got session ID: {session_id}\n")

    # Close the SSE connection
    response.close()

    # Step 2: Initialize the session (REQUIRED by MCP protocol)
    print("Step 2: Initializing MCP session...")
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

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "MCP-Session-Id": session_id,
    }

    print(f"Request: {json.dumps(initialize_request, indent=2)}")

    response = requests.post(
        BASE_URL, json=initialize_request, headers=headers, timeout=10
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}\n")

    # Parse SSE or JSON response
    if response.text.lstrip().startswith("event:"):
        data_lines = [
            line[len("data: ") :]
            for line in response.text.splitlines()
            if line.startswith("data: ")
        ]
        data = json.loads("\n".join(data_lines))
        if "result" in data:
            print("✓ Initialization successful\n")
        else:
            print(f"✗ Initialization failed: {data}\n")
            return

    # Step 3: Test get_current_user (should work after initialization)
    print("Step 3: Testing get_current_user tool...")
    request_data = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "get_current_user", "arguments": {}},
    }

    print(f"Request: {json.dumps(request_data, indent=2)}")
    print(f"Headers: {headers}\n")

    response = requests.post(BASE_URL, json=request_data, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}\n")

    # Step 4: Test list_groups (this one fails with -32602)
    print("Step 4: Testing list_groups tool...")
    request_data = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "list_groups", "arguments": {}},
    }

    print(f"Request: {json.dumps(request_data, indent=2)}")
    print(f"Headers: {headers}\n")

    response = requests.post(BASE_URL, json=request_data, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}\n")

    # Step 5: Test tools/list
    print("Step 5: Testing tools/list...")
    request_data = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/list",
        "params": {"limit": 100, "offset": 0},
    }

    print(f"Request: {json.dumps(request_data, indent=2)}")

    response = requests.post(BASE_URL, json=request_data, headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}\n")


if __name__ == "__main__":
    test_mcp_request()
