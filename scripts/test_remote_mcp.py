#!/usr/bin/env python3
"""Test script to debug remote MCP server connection."""

import json
import requests

# Your remote server URL
BASE_URL = "https://sw-mcp.paulakimenko.xyz/mcp"


def test_remote_mcp():
    """Test remote MCP HTTP request flow."""
    print("=== Testing Remote MCP Server ===\n")
    print(f"Server URL: {BASE_URL}\n")
    
    # Step 1: Check if server is reachable
    print("Step 1: Checking server connectivity...")
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"✓ Server is reachable")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}\n")
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot reach server: {e}\n")
        return
    
    # Step 2: Try to open SSE connection
    print("Step 2: Opening SSE connection to get session ID...")
    try:
        response = requests.get(
            BASE_URL,
            headers={"Accept": "text/event-stream"},
            stream=True,
            timeout=10
        )
        
        # Check for session ID in headers (case-insensitive)
        session_id = None
        for header_name in response.headers:
            if header_name.lower() == "mcp-session-id":
                session_id = response.headers[header_name]
                break
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        print(f"\nSession ID: {session_id}")
        
        if not session_id:
            print("✗ No session ID found in headers")
            print("\nFirst 500 chars of response:")
            print(response.text[:500])
            return
        
        print(f"✓ Got session ID: {session_id}\n")
        response.close()
        
        # Step 3: Try to list tools (this is what the UI is trying to do)
        print("Step 3: Attempting to list MCP tools...")
        
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "MCP-Session-Id": session_id
        }
        
        print(f"Request: {json.dumps(request_data, indent=2)}")
        print(f"Headers: {headers}\n")
        
        response = requests.post(BASE_URL, json=request_data, headers=headers, timeout=30)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response (first 1000 chars):")
        print(response.text[:1000])
        
        # Try to parse response
        if response.status_code == 200:
            try:
                # Check if it's SSE format
                if response.text.lstrip().startswith("event:"):
                    print("\n✓ Got SSE response")
                    data_lines = [line[len("data: "):] for line in response.text.splitlines() if line.startswith("data: ")]
                    if data_lines:
                        combined = "\n".join(data_lines)
                        data = json.loads(combined)
                        print(f"\nParsed response: {json.dumps(data, indent=2)[:500]}")
                        
                        if "error" in data:
                            print(f"\n✗ Error in response: {data['error']}")
                        elif "result" in data:
                            print(f"\n✓ Success! Found {len(data.get('result', {}).get('tools', []))} tools")
                else:
                    # Try as JSON
                    data = response.json()
                    print(f"\n✓ Got JSON response: {json.dumps(data, indent=2)[:500]}")
            except Exception as e:
                print(f"\n✗ Error parsing response: {e}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}\n")
        return


if __name__ == "__main__":
    test_remote_mcp()
