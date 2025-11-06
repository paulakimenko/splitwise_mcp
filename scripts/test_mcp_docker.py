#!/usr/bin/env python3
"""Test script to verify MCP server works in Docker with Streamable HTTP transport."""

import sys

import requests


def test_mcp_server(base_url="http://localhost:8000"):
    """Test if MCP server is working in Docker with Streamable HTTP transport."""

    print(f"🔍 Testing MCP server at {base_url}")

    # Test 1: MCP initialization
    try:
        print("\n1️⃣ Testing MCP initialization...")
        mcp_url = f"{base_url}/mcp"

        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "docker-test-client", "version": "1.0.0"},
            },
        }

        response = requests.post(
            mcp_url,
            json=initialize_request,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code in [200, 201]:
            data = response.json()
            if "result" in data:
                print("   ✅ MCP initialization successful")
                return True
            else:
                print(f"   ❌ MCP initialization failed: {data}")
                return False
        else:
            print(f"   ❌ MCP endpoint not accessible: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(
            "   ❌ Cannot connect to MCP server - is it running with Streamable HTTP transport?"
        )
        return False
    except Exception as e:
        print(f"   ❌ MCP initialization error: {e}")
        return False

    # Test 2: List MCP tools
    try:
        print("\n2️⃣ Testing MCP tools list...")
        mcp_url = f"{base_url}/mcp"

        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        }

        response = requests.post(
            mcp_url,
            json=list_tools_request,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code in [200, 201]:
            data = response.json()
            if "result" in data and "tools" in data["result"]:
                tools = data["result"]["tools"]
                print(f"   ✅ Found {len(tools)} MCP tools")
                # Show first few tool names
                for tool in tools[:3]:
                    print(f"      - {tool['name']}")
            else:
                print(f"   ⚠️  Unexpected tools response: {data}")
        else:
            print(f"   ❌ Tools list failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Tools list error: {e}")

    # Test 3: List MCP resources
    try:
        print("\n3️⃣ Testing MCP resources list...")
        mcp_url = f"{base_url}/mcp"

        list_resources_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "resources/list",
            "params": {},
        }

        response = requests.post(
            mcp_url,
            json=list_resources_request,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )

        if response.status_code in [200, 201]:
            data = response.json()
            if "result" in data and "resources" in data["result"]:
                resources = data["result"]["resources"]
                print(f"   ✅ Found {len(resources)} MCP resources")
                # Show first few resource URIs
                for resource in resources[:3]:
                    print(f"      - {resource['uri']}")
            else:
                print(f"   ⚠️  Unexpected resources response: {data}")
        else:
            print(f"   ❌ Resources list failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Resources list error: {e}")

    # Test 4: Test tool call (if credentials available)
    try:
        print("\n4️⃣ Testing MCP tool call...")
        mcp_url = f"{base_url}/mcp"

        call_tool_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "get_current_user", "arguments": {}},
        }

        response = requests.post(
            mcp_url,
            json=call_tool_request,
            headers={"Content-Type": "application/json"},
            timeout=15,  # Longer timeout for API calls
        )

        if response.status_code in [200, 201]:
            data = response.json()
            if "result" in data:
                print("   ✅ Tool call successful")
            elif "error" in data:
                print(
                    f"   ⚠️  Tool call error (expected if no API key): {data['error'].get('message', 'Unknown error')}"
                )
            else:
                print(f"   ⚠️  Unexpected tool response: {data}")
        else:
            print(f"   ❌ Tool call failed: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Tool call error: {e}")

    print("\n🎉 MCP Streamable HTTP transport test completed!")
    print(f"📍 MCP server running at: {base_url}/mcp")
    print("� Transport: Streamable HTTP")
    print("🌐 Protocol: JSON-RPC over HTTP")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test MCP server via Docker")
    parser.add_argument(
        "--url",
        default="http://localhost:8000",
        help="Base URL for the MCP server (default: http://localhost:8000)",
    )
    parser.add_argument(
        "--quick", action="store_true", help="Run quick tests only (same as default)"
    )

    args = parser.parse_args()
    base_url = args.url

    test_mcp_server(base_url)
