#!/usr/bin/env python3
"""Manual MCP testing CLI tool.

This script provides a convenient way to manually test MCP endpoints
from the command line during development.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from contextlib import asynccontextmanager
from typing import Any

import httpx


@asynccontextmanager
async def mcp_http_session(base_url: str = "http://localhost:8000/mcp"):
    """Create HTTP session for MCP testing."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client, base_url


async def call_mcp_tool(client: httpx.AsyncClient, base_url: str, tool_name: str, arguments: dict[str, Any]):
    """Call an MCP tool over HTTP."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments
        }
    }
    
    response = await client.post(
        base_url,
        headers={"Content-Type": "application/json"},
        json=request
    )
    
    return response.status_code, response.json()


async def read_mcp_resource(client: httpx.AsyncClient, base_url: str, uri: str):
    """Read an MCP resource over HTTP."""
    request = {
        "jsonrpc": "2.0", 
        "id": 2,
        "method": "resources/read",
        "params": {
            "uri": uri
        }
    }
    
    response = await client.post(
        base_url,
        headers={"Content-Type": "application/json"},
        json=request
    )
    
    return response.status_code, response.json()


async def list_tools(client: httpx.AsyncClient, base_url: str) -> dict[str, Any]:
    """List available MCP tools."""
    # Use the alternative REST endpoint
    response = await client.get(f"{base_url}/list-tools")
    response.raise_for_status()
    return response.json()


async def call_tool(client: httpx.AsyncClient, base_url: str, tool_name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    """Call a specific MCP tool."""
    # Use the alternative REST endpoint with query parameter format
    params = {"tool_name": tool_name}
    request_data = arguments or {}
    
    response = await client.post(f"{base_url}/call-tool", params=params, json=request_data)
    response.raise_for_status()
    return response.json()


async def list_mcp_resources(client: httpx.AsyncClient, base_url: str):
    """List available MCP resources.""" 
    # For now, return empty resources since we haven't implemented this endpoint yet
    return 200, {"resources": []}


async def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Manual MCP testing tool")
    parser.add_argument("--url", default="http://localhost:8000/mcp-test", help="MCP server URL")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List tools command
    subparsers.add_parser("list-tools", help="List available MCP tools")
    
    # List resources command  
    subparsers.add_parser("list-resources", help="List available MCP resources")
    
    # Call tool command
    call_parser = subparsers.add_parser("call", help="Call an MCP tool")
    call_parser.add_argument("tool_name", help="Name of the tool to call")
    call_parser.add_argument("--args", default="{}", help="Tool arguments as JSON")
    
    # Read resource command
    read_parser = subparsers.add_parser("read", help="Read an MCP resource") 
    read_parser.add_argument("uri", help="Resource URI to read")
    
    # Quick test command
    subparsers.add_parser("quick-test", help="Run a quick test of common tools")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        async with mcp_http_session(args.url) as (client, base_url):
            if args.command == "list-tools":
                try:
                    response = await list_tools(client, base_url)
                    print("Status: 200")
                    print(json.dumps(response, indent=2))
                except Exception as e:
                    print(f"Error: {e}")
                
            elif args.command == "list-resources":
                status, response = await list_mcp_resources(client, base_url) 
                print(f"Status: {status}")
                print(json.dumps(response, indent=2))
                
            elif args.command == "call":
                try:
                    arguments = json.loads(args.args)
                except json.JSONDecodeError:
                    print(f"Error: Invalid JSON arguments: {args.args}")
                    return
                
                try:
                    response = await call_tool(client, base_url, args.tool_name, arguments)
                    print("Status: 200")
                    print(json.dumps(response, indent=2))
                except Exception as e:
                    print(f"Status: 404")
                    print(json.dumps({"detail": str(e)}, indent=2))
                
            elif args.command == "read":
                status, response = await read_mcp_resource(client, base_url, args.uri)
                print(f"Status: {status}")
                print(json.dumps(response, indent=2))
                
            elif args.command == "quick-test":
                print("Running quick MCP test...")
                
                # Test 1: List tools
                print("\n1. Testing list tools...")
                try:
                    response = await list_tools(client, base_url)
                    print("   Status: 200")
                    if "tools" in response:
                        tools = response["tools"]
                        print(f"   Found {len(tools)} tools")
                        for tool in tools[:3]:  # Show first 3
                            print(f"   - {tool['name']}")
                except Exception as e:
                    print(f"   Error: {e}")
                
                # Test 2: Get current user
                print("\n2. Testing get_current_user...")
                try:
                    response = await call_tool(client, base_url, "get_current_user", {})
                    print("   Status: 200")
                    if response:
                        print("   ✅ get_current_user succeeded")
                except Exception as e:
                    print(f"   Error: {e}")
                
                # Test 3: List groups
                print("\n3. Testing list_groups...")  
                status, response = await call_mcp_tool(client, base_url, "list_groups", {})
                print(f"   Status: {status}")
                if status == 200 and "result" in response:
                    print("   ✅ list_groups succeeded")
                
                # Test 4: Read balance resource
                print("\n4. Testing balance resource...")
                status, response = await read_mcp_resource(client, base_url, "splitwise://balance") 
                print(f"   Status: {status}")
                if status == 200 and "result" in response:
                    print("   ✅ balance resource succeeded")
                
                print("\nQuick test complete!")
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Check for required environment variables
    if not os.getenv("SPLITWISE_API_KEY") and not os.getenv("SPLITWISE_CONSUMER_KEY"):
        print("Warning: No Splitwise API credentials found. Some tests may fail.", file=sys.stderr)
        print("Set SPLITWISE_API_KEY or SPLITWISE_CONSUMER_KEY/SPLITWISE_CONSUMER_SECRET", file=sys.stderr)
    
    asyncio.run(main())