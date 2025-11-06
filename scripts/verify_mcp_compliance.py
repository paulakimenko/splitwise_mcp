#!/usr/bin/env python3
"""
Comprehensive MCP Server Compliance Verification Script

This script verifies that an MCP server is fully compliant with the
Model Context Protocol specification and compatible with ChatGPT connectors.

Usage:
    python scripts/verify_mcp_compliance.py <server_url>

Example:
    python scripts/verify_mcp_compliance.py https://sw-mcp.paulakimenko.xyz/mcp
"""

import json
import sys
from typing import Any

import requests


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_result(passed: bool, message: str) -> None:
    """Print a test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {message}")


def test_initialize(url: str) -> tuple[bool, dict[str, Any] | None, str | None]:
    """Test the initialize endpoint."""
    print_section("Test 1: Initialize Handshake")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"roots": {}, "sampling": {}},
            "clientInfo": {"name": "Compliance-Check", "version": "1.0"},
        },
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        # Check status code
        if response.status_code != 200:
            print_result(False, f"Status code: {response.status_code} (expected 200)")
            return False, None, None
        print_result(True, "Status code: 200 OK")

        # Check for session ID
        session_id = response.headers.get("Mcp-Session-Id")
        if not session_id:
            print_result(False, "Missing Mcp-Session-Id header")
            return False, None, None
        print_result(True, f"Session ID: {session_id}")

        # Check Content-Type
        content_type = response.headers.get("Content-Type", "")
        is_sse = "text/event-stream" in content_type
        is_json = "application/json" in content_type

        if not (is_sse or is_json):
            print_result(False, f"Invalid Content-Type: {content_type}")
            return False, None, None
        print_result(True, f"Content-Type: {content_type}")

        # Parse response
        if is_sse:
            # Parse SSE format
            lines = response.text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
            data_lines = [
                line[5:].strip() for line in lines if line.startswith("data:")
            ]
            if not data_lines:
                print_result(False, "No data in SSE response")
                return False, None, None
            response_data = json.loads(" ".join(data_lines))
        else:
            response_data = response.json()

        # Check JSON-RPC structure
        if response_data.get("jsonrpc") != "2.0":
            print_result(False, "Missing or invalid jsonrpc version")
            return False, None, None
        print_result(True, "JSON-RPC version: 2.0")

        if response_data.get("id") != 1:
            print_result(False, "Response ID doesn't match request ID")
            return False, None, None
        print_result(True, "Response ID matches request")

        # Check for result
        result = response_data.get("result")
        if not result:
            print_result(False, "Missing result field")
            return False, None, None

        # Check protocol version
        protocol = result.get("protocolVersion")
        if protocol != "2024-11-05":
            print_result(False, f"Protocol version: {protocol} (expected 2024-11-05)")
            return False, None, None
        print_result(True, f"Protocol version: {protocol}")

        # Check capabilities
        capabilities = result.get("capabilities")
        if not capabilities:
            print_result(False, "Missing capabilities")
            return False, None, None

        # Check for tools capability (CRITICAL for ChatGPT)
        if "tools" not in capabilities:
            print_result(
                False,
                "❌ CRITICAL: Missing 'tools' capability - ChatGPT won't show connector!",
            )
            return False, None, None
        print_result(True, "Tools capability declared ✨")

        # Check server info
        server_info = result.get("serverInfo")
        if not server_info:
            print_result(False, "Missing serverInfo")
            return False, None, None
        print_result(
            True, f"Server: {server_info.get('name')} v{server_info.get('version')}"
        )

        print("\n📋 Full capabilities:")
        print(json.dumps(capabilities, indent=2))

        return True, response_data, session_id

    except Exception as e:
        print_result(False, f"Request failed: {e}")
        return False, None, None


def test_tools_list(
    url: str, session_id: str | None
) -> tuple[bool, list[dict[str, Any]] | None]:
    """Test the tools/list endpoint."""
    print_section("Test 2: Tools List")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    if session_id:
        headers["Mcp-Session-Id"] = session_id

    payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        # Check status code
        if response.status_code != 200:
            print_result(False, f"Status code: {response.status_code} (expected 200)")
            return False, None
        print_result(True, "Status code: 200 OK")

        # Parse response
        content_type = response.headers.get("Content-Type", "")
        if "text/event-stream" in content_type:
            lines = response.text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
            data_lines = [
                line[5:].strip() for line in lines if line.startswith("data:")
            ]
            response_data = json.loads(" ".join(data_lines))
        else:
            response_data = response.json()

        # Check JSON-RPC structure
        result = response_data.get("result")
        if not result:
            print_result(False, "Missing result field")
            return False, None

        # Check tools array
        tools = result.get("tools")
        if tools is None:
            print_result(False, "Missing tools array")
            return False, None

        if not isinstance(tools, list):
            print_result(False, "Tools is not an array")
            return False, None

        if len(tools) == 0:
            print_result(
                False, "❌ CRITICAL: Empty tools array - ChatGPT won't show connector!"
            )
            return False, None

        print_result(True, f"Found {len(tools)} tools ✨")

        # Validate each tool
        print("\n📋 Validating tool schemas:")
        all_valid = True
        for i, tool in enumerate(tools):
            tool_name = tool.get("name", f"tool_{i}")

            # Check required fields
            missing_fields = []
            if "name" not in tool:
                missing_fields.append("name")
            if "description" not in tool:
                missing_fields.append("description")
            if "inputSchema" not in tool:
                missing_fields.append("inputSchema")

            if missing_fields:
                print_result(
                    False, f"  {tool_name}: Missing fields: {', '.join(missing_fields)}"
                )
                all_valid = False
            else:
                # Validate inputSchema
                input_schema = tool.get("inputSchema", {})
                if not isinstance(input_schema, dict):
                    print_result(False, f"  {tool_name}: inputSchema is not an object")
                    all_valid = False
                elif input_schema.get("type") != "object":
                    print_result(
                        False, f"  {tool_name}: inputSchema type must be 'object'"
                    )
                    all_valid = False
                else:
                    print_result(True, f"  {tool_name}: Valid schema")

        if all_valid:
            print("\n✅ All tools have valid schemas!")
        else:
            print("\n❌ Some tools have invalid schemas")
            return False, None

        # Print tool names
        print("\n📋 Available tools:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description'][:60]}...")

        return True, tools

    except Exception as e:
        print_result(False, f"Request failed: {e}")
        return False, None


def print_summary(init_passed: bool, tools_passed: bool, tools_count: int) -> None:
    """Print final summary."""
    print_section("Compliance Summary")

    if init_passed and tools_passed and tools_count > 0:
        print("\n🎉 SUCCESS! Your MCP server is fully compliant! 🎉\n")
        print("✅ Initialize handshake: PASSED")
        print("✅ Tools capability declared: PASSED")
        print(f"✅ Tools list endpoint: PASSED ({tools_count} tools)")
        print("✅ Tool schema validation: PASSED")
        print("\n" + "=" * 80)
        print("  Your server SHOULD work with ChatGPT connectors!")
        print("=" * 80)
        print("\nIf the connector doesn't appear in ChatGPT, check:")
        print(
            "1. Developer Mode is enabled: Settings → Connectors → Advanced → Developer mode"
        )
        print(
            "2. Refresh the connector: Settings → Connectors → Click connector → Refresh"
        )
        print("3. Clear browser cache or try incognito mode")
        print("4. Wait a few minutes (ChatGPT may cache the initial connection)")
    else:
        print("\n❌ COMPLIANCE ISSUES DETECTED ❌\n")
        if not init_passed:
            print("❌ Initialize handshake: FAILED")
        if not tools_passed:
            print("❌ Tools list endpoint: FAILED")
        if tools_count == 0:
            print("❌ No tools returned: ChatGPT won't show the connector")
        print("\nReview the errors above and fix the issues.")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python scripts/verify_mcp_compliance.py <server_url>")
        print(
            "Example: python scripts/verify_mcp_compliance.py https://sw-mcp.paulakimenko.xyz/mcp"
        )
        sys.exit(1)

    url = sys.argv[1]

    print("=" * 80)
    print("  MCP Server Compliance Verification")
    print("=" * 80)
    print(f"\nTarget URL: {url}")

    # Test initialize
    init_passed, init_data, session_id = test_initialize(url)

    # Test tools list
    tools_passed = False
    tools_count = 0
    if init_passed:
        tools_passed, tools = test_tools_list(url, session_id)
        if tools:
            tools_count = len(tools)

    # Print summary
    print_summary(init_passed, tools_passed, tools_count)

    # Exit with appropriate code
    sys.exit(0 if (init_passed and tools_passed and tools_count > 0) else 1)


if __name__ == "__main__":
    main()
