#!/usr/bin/env python3
"""
Test script to simulate ChatGPT's MCP connector behavior.

This script reproduces what ChatGPT does when trying to connect to an MCP server:
1. Initialize connection to the MCP endpoint
2. List available tools
3. Verify the response format

Usage:
    python scripts/test_chatgpt_connector.py [url]
    
    url: MCP server URL (default: http://localhost:8000/mcp)
"""

import json
import sys
import requests
from typing import Any, Dict, List


def test_mcp_initialization(base_url: str) -> Dict[str, Any]:
    """
    Test MCP initialization - simulates ChatGPT's initial connection.
    
    ChatGPT expects:
    1. POST to /mcp with initialize request
    2. Response with server capabilities
    3. Session ID in Mcp-Session-Id header
    """
    print(f"\n{'='*80}")
    print(f"Testing MCP Initialization")
    print(f"{'='*80}")
    print(f"URL: {base_url}")
    
    # MCP initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {
                    "listChanged": True
                },
                "sampling": {}
            },
            "clientInfo": {
                "name": "ChatGPT-Test",
                "version": "1.0.0"
            }
        }
    }
    
    try:
        print(f"\nSending initialize request...")
        print(f"Request body: {json.dumps(init_request, indent=2)}")
        
        response = requests.post(
            base_url,
            json=init_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "text/event-stream, application/json"
            },
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        # Check for session ID
        session_id = response.headers.get('Mcp-Session-Id')
        if session_id:
            print(f"\n✅ Session ID found: {session_id}")
        else:
            print(f"\n❌ No Mcp-Session-Id header found!")
        
        # Parse response
        content_type = response.headers.get('Content-Type', '')
        
        if 'text/event-stream' in content_type:
            print(f"\nResponse Format: Server-Sent Events (SSE)")
            print(f"Raw Response:\n{response.text[:500]}...")
            
            # Parse SSE - handle multi-line responses with \r\n line endings
            result = None
            buffer = ""
            
            # Split by newlines and clean up carriage returns
            lines = response.text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
            
            for line in lines:
                if line.startswith('event:'):
                    # Event type line - ignore
                    continue
                elif line.startswith('data: '):
                    # Data line - add to buffer
                    buffer += line[6:]
                elif line.startswith('data:'):
                    # Data line without space
                    buffer += line[5:]
                elif line == "" and buffer:
                    # Empty line signals end of message
                    try:
                        result = json.loads(buffer)
                        break
                    except json.JSONDecodeError:
                        buffer = ""
                        continue
            
            # If we didn't find an empty line, try to parse what we have
            if not result and buffer.strip():
                try:
                    result = json.loads(buffer)
                except json.JSONDecodeError:
                    pass
            
            if result:
                print(f"\nParsed JSON Response:")
                print(json.dumps(result, indent=2))
                return {"session_id": session_id, "response": result}
            else:
                print(f"\n❌ Failed to parse SSE response")
                return {"error": "Failed to parse SSE", "raw": response.text}
        
        elif 'application/json' in content_type:
            print(f"\nResponse Format: JSON")
            result = response.json()
            print(f"Response:")
            print(json.dumps(result, indent=2))
            return {"session_id": session_id, "response": result}
        
        else:
            print(f"\n❌ Unexpected Content-Type: {content_type}")
            print(f"Response body:\n{response.text[:500]}")
            return {"error": "Unexpected content type", "content_type": content_type}
    
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return {"error": str(e)}


def test_list_tools(base_url: str, session_id: str | None) -> Dict[str, Any]:
    """
    Test listing tools - ChatGPT needs this to build the connector.
    
    ChatGPT expects:
    1. POST to /mcp with tools/list request
    2. Response with array of tool definitions
    3. Each tool has: name, description, inputSchema
    """
    print(f"\n{'='*80}")
    print(f"Testing Tools List")
    print(f"{'='*80}")
    
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json"
        }
        
        if session_id:
            headers["Mcp-Session-Id"] = session_id
            print(f"Using session ID: {session_id}")
        
        print(f"\nSending tools/list request...")
        print(f"Request body: {json.dumps(list_tools_request, indent=2)}")
        
        response = requests.post(
            base_url,
            json=list_tools_request,
            headers=headers,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        # Parse response
        content_type = response.headers.get('Content-Type', '')
        
        if 'text/event-stream' in content_type:
            print(f"\nResponse Format: SSE")
            
            # Parse SSE - handle multi-line responses with \r\n line endings
            result = None
            buffer = ""
            
            # Split by newlines and clean up carriage returns
            lines = response.text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
            
            for line in lines:
                if line.startswith('event:'):
                    # Event type line - ignore
                    continue
                elif line.startswith('data: '):
                    # Data line - add to buffer
                    buffer += line[6:]
                elif line.startswith('data:'):
                    # Data line without space
                    buffer += line[5:]
                elif line == "" and buffer:
                    # Empty line signals end of message
                    try:
                        result = json.loads(buffer)
                        break
                    except json.JSONDecodeError:
                        buffer = ""
                        continue
            
            # If we didn't find an empty line, try to parse what we have
            if not result and buffer.strip():
                try:
                    result = json.loads(buffer)
                except json.JSONDecodeError:
                    pass
            
            if result:
                print(f"\n✅ Tools list received")
                if 'result' in result and 'tools' in result['result']:
                    tools = result['result']['tools']
                    print(f"Number of tools: {len(tools)}")
                    print(f"\nTools:")
                    for tool in tools:
                        print(f"  - {tool.get('name')}: {tool.get('description', 'No description')}")
                    return {"tools": tools}
                else:
                    print(json.dumps(result, indent=2))
                    return {"response": result}
            else:
                print(f"\n❌ Failed to parse tools list")
                print(f"Raw response:\n{response.text[:500]}")
                return {"error": "Failed to parse", "raw": response.text}
        
        elif 'application/json' in content_type:
            result = response.json()
            print(f"\n✅ Tools list received (JSON)")
            if 'result' in result and 'tools' in result['result']:
                tools = result['result']['tools']
                print(f"Number of tools: {len(tools)}")
                print(f"\nTools:")
                for tool in tools:
                    print(f"  - {tool.get('name')}: {tool.get('description', 'No description')}")
                return {"tools": tools}
            else:
                print(json.dumps(result, indent=2))
                return {"response": result}
        
        else:
            print(f"\n❌ Unexpected Content-Type: {content_type}")
            return {"error": "Unexpected content type"}
    
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {e}")
        return {"error": str(e)}


def main():
    """Main test execution."""
    # Get URL from command line or use default
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/mcp"
    
    print(f"\n{'='*80}")
    print(f"ChatGPT MCP Connector Test")
    print(f"{'='*80}")
    print(f"This simulates what ChatGPT does when connecting to an MCP server.")
    print(f"Target URL: {url}")
    
    # Test 1: Initialize
    init_result = test_mcp_initialization(url)
    
    if "error" in init_result:
        print(f"\n❌ FAILED: Initialization failed")
        print(f"Error: {init_result['error']}")
        print(f"\nThis is likely why ChatGPT shows 'Failed to build actions from MCP endpoint'")
        sys.exit(1)
    
    session_id = init_result.get("session_id")
    response = init_result.get("response", {})
    
    # Check if initialization was successful
    if "result" not in response:
        print(f"\n❌ FAILED: No 'result' in initialization response")
        print(f"ChatGPT expects a standard JSON-RPC response with 'result' field")
        sys.exit(1)
    
    print(f"\n✅ PASSED: Initialization successful")
    
    # Test 2: List Tools
    tools_result = test_list_tools(url, session_id)
    
    if "error" in tools_result:
        print(f"\n❌ FAILED: Tools list failed")
        print(f"Error: {tools_result['error']}")
        sys.exit(1)
    
    if "tools" not in tools_result:
        print(f"\n❌ FAILED: No tools array in response")
        sys.exit(1)
    
    print(f"\n✅ PASSED: Tools list successful")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"Test Summary")
    print(f"{'='*80}")
    print(f"✅ All tests passed!")
    print(f"✅ MCP server is compatible with ChatGPT connectors")
    print(f"\nYour server should work with ChatGPT at: {url}")


if __name__ == "__main__":
    main()
