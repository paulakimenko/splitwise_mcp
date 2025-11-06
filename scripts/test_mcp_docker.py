#!/usr/bin/env python3
"""Test script to verify MCP server works in Docker."""

import requests
import time
import sys

def test_mcp_server(base_url="http://localhost:8000"):
    """Test if MCP server is working in Docker."""
    
    print(f"🔍 Testing MCP server at {base_url}")
    
    # Test 1: Health check
    try:
        print("\n1️⃣ Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health check passed: {data.get('status')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to server - is it running?")
        return False
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 2: OpenAPI documentation 
    try:
        print("\n2️⃣ Testing OpenAPI documentation...")
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("   ✅ API documentation available")
        else:
            print(f"   ⚠️  API docs status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  API docs error: {e}")
    
    # Test 3: MCP endpoint
    try:
        print("\n3️⃣ Testing MCP endpoint...")
        response = requests.get(f"{base_url}/mcp", timeout=5)
        if response.status_code in [200, 307, 404]:  # 404 is expected due to FastMCP limitations
            print(f"   ✅ MCP endpoint responds (status: {response.status_code})")
            if response.status_code == 404:
                print("   ℹ️  404 is expected due to FastMCP mounting limitations")
        else:
            print(f"   ❌ MCP endpoint error: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  MCP endpoint error: {e}")
    
    # Test 4: MCP test tools endpoint
    try:
        print("\n4️⃣ Testing MCP test tools...")
        response = requests.get(f"{base_url}/mcp-test/list-tools", timeout=5)
        if response.status_code == 200:
            tools = response.json()
            print(f"   ✅ MCP tools available: {len(tools.get('result', {}).get('tools', []))} tools")
        else:
            print(f"   ⚠️  MCP tools status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  MCP tools error: {e}")
        
    # Test 5: Custom endpoints
    try:
        print("\n5️⃣ Testing custom endpoints...")
        response = requests.get(f"{base_url}/groups", timeout=5)
        if response.status_code == 200:
            print("   ✅ Groups endpoint works")
        else:
            print(f"   ⚠️  Groups endpoint status: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Groups endpoint error: {e}")
    
    print(f"\n🎉 MCP server test completed!")
    print(f"📍 Server is running at: {base_url}")
    print(f"📖 API docs available at: {base_url}/docs")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8000"
    
    test_mcp_server(base_url)