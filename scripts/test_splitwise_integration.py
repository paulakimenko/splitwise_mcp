#!/usr/bin/env python3
"""
Splitwise MCP Integration Test Script

Tests the Splitwise MCP connector using proper MCP JSON-RPC protocol.
Validates that search and fetch tools work correctly (required for ChatGPT connectors).
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, Optional

import httpx


class SplitwiseMCPTester:
    """Test client for Splitwise MCP connector using JSON-RPC protocol."""

    def __init__(self, base_url: str):
        """Initialize the tester with MCP server URL."""
        self.base_url = base_url.rstrip("/")
        self.mcp_url = f"{self.base_url}/mcp"
        self.session_id: Optional[str] = None
        self.request_id = 0
        self.client = httpx.AsyncClient(timeout=30.0)

    def _next_id(self) -> int:
        """Generate next request ID for JSON-RPC."""
        self.request_id += 1
        return self.request_id

    async def _initialize_session(self) -> str:
        """Initialize MCP session and get session ID."""
        print("🔄 Initializing MCP session...")

        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "splitwise-integration-test",
                    "version": "1.0.0"
                }
            }
        }

        response = await self.client.post(self.mcp_url, json=payload)
        
        # Extract session ID from header
        session_id = response.headers.get("Mcp-Session-Id")
        if not session_id:
            raise ValueError("No Mcp-Session-Id in initialize response")

        print(f"✅ Session initialized: {session_id[:20]}...")
        return session_id

    async def call_tool(
        self, 
        tool_name: str, 
        arguments: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Call an MCP tool using JSON-RPC protocol.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments (optional)
            
        Returns:
            Tool response data
        """
        if not self.session_id:
            self.session_id = await self._initialize_session()

        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }

        headers = {
            "Mcp-Session-Id": self.session_id
        }

        response = await self.client.post(self.mcp_url, json=payload, headers=headers)

        # Parse SSE response format
        response_text = response.text
        lines = response_text.strip().split("\n")
        
        # Extract JSON from SSE data lines
        for line in lines:
            if line.startswith("data: "):
                json_str = line[6:]  # Remove "data: " prefix
                data = json.loads(json_str)
                
                # Check for JSON-RPC error
                if "error" in data:
                    error = data["error"]
                    raise ValueError(f"JSON-RPC error: {error.get('message', error)}")
                
                # Return result
                if "result" in data:
                    result = data["result"]
                    
                    # Check for tool execution error
                    if isinstance(result, dict) and result.get("isError"):
                        content = result.get("content", [])
                        error_msg = "Unknown error"
                        if content and isinstance(content[0], dict):
                            error_msg = content[0].get("text", error_msg)
                        raise ValueError(f"Tool error: {error_msg}")
                    
                    return result

        raise ValueError(f"No valid JSON-RPC response found in: {response_text[:200]}")

    async def test_get_current_user(self) -> Dict[str, Any]:
        """Test get_current_user tool."""
        print("\n� Testing: get_current_user")
        result = await self.call_tool("get_current_user")
        
        # Parse text content
        content = result.get("content", [])
        if content and isinstance(content[0], dict):
            text = content[0].get("text", "{}")
            data = json.loads(text)
            
            # Validate response
            assert "first_name" in data, "Missing first_name"
            assert "last_name" in data, "Missing last_name"
            assert "id" in data, "Missing id"
            
            print(f"   ✅ Tool call succeeded (get_current_user) - Response: {json.dumps(data, indent=2)[:100]}...")
            return data
        
        raise ValueError("Invalid response format")

    async def test_list_groups(self) -> Dict[str, Any]:
        """Test list_groups tool."""
        print("\n� Testing: list_groups")
        result = await self.call_tool("list_groups")
        
        # Parse text content
        content = result.get("content", [])
        if content and isinstance(content[0], dict):
            text = content[0].get("text", "{}")
            data = json.loads(text)
            
            # Validate response
            assert "groups" in data, "Missing groups"
            assert isinstance(data["groups"], list), "groups should be a list"
            
            print(f"   ✅ Tool call succeeded (list_groups) - Response: {json.dumps(data, indent=2)[:100]}...")
            return data
        
        raise ValueError("Invalid response format")

    async def test_list_expenses(self) -> Dict[str, Any]:
        """Test list_expenses tool with arguments."""
        print("\n� Testing: list_expenses (limit=5)")
        result = await self.call_tool("list_expenses", {"limit": 5})
        
        # Parse text content
        content = result.get("content", [])
        if content and isinstance(content[0], dict):
            text = content[0].get("text", "{}")
            data = json.loads(text)
            
            # Validate response
            assert "expenses" in data, "Missing expenses"
            assert isinstance(data["expenses"], list), "expenses should be a list"
            
            print(f"   ✅ Tool call succeeded (list_expenses) - Response: {json.dumps(data, indent=2)[:100]}...")
            return data
        
        raise ValueError("Invalid response format")

    async def test_search(self) -> Dict[str, Any]:
        """Test search tool (required for ChatGPT connectors)."""
        print("\n📝 Testing: search (query='grocery')")
        result = await self.call_tool("search", {"query": "grocery"})
        
        # Parse text content
        content = result.get("content", [])
        if content and isinstance(content[0], dict):
            text = content[0].get("text", "{}")
            data = json.loads(text)
            
            # Validate response
            assert "results" in data, "Missing results"
            assert isinstance(data["results"], list), "results should be a list"
            
            print(f"   ✅ Tool call succeeded (search) - Response: {json.dumps(data, indent=2)[:100]}...")
            return data
        
        raise ValueError("Invalid response format")

    async def test_fetch(self, expense_id: str) -> Dict[str, Any]:
        """Test fetch tool (required for ChatGPT connectors)."""
        print(f"\n📝 Testing: fetch (id='{expense_id}')")
        result = await self.call_tool("fetch", {"id": expense_id})
        
        # Parse text content
        content = result.get("content", [])
        if content and isinstance(content[0], dict):
            text = content[0].get("text", "{}")
            
            # Handle both error responses and successful responses
            try:
                data = json.loads(text)
                print(f"   ✅ Tool call succeeded (fetch) - Response: {json.dumps(data, indent=2)[:100]}...")
                return data
            except json.JSONDecodeError:
                # Text response is OK too
                print(f"   ✅ Tool call succeeded (fetch) - Response: {text[:100]}...")
                return {"text": text}
        
        raise ValueError("Invalid response format")

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    def print_summary(self, passed: int, failed: int, failures: list):
        """Print test summary."""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {passed + failed}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        
        if failed > 0:
            print("\n⚠️ Failed Tests:")
            for name, error in failures:
                print(f"   - {name}: {error}")
            print("\n💡 Troubleshooting:")
            print("   1. Verify MCP server is running at the correct URL")
            print("   2. Check that SPLITWISE_API_KEY is set correctly")
            print("   3. Ensure the MCP server supports JSON-RPC protocol")
        else:
            print("\n🎉 ALL TESTS PASSED!")
        
        print("=" * 80)


async def main():
    """Run all integration tests."""
    # Get MCP server URL from environment
    base_url = os.getenv("SPLITWISE_MCP_URL", "https://sw-mcp.paulakimenko.xyz")
    
    print("=" * 80)
    print("SPLITWISE MCP INTEGRATION CHECK")
    print("=" * 80)
    print(f"Base URL: {base_url}")
    print("=" * 80)
    
    tester = SplitwiseMCPTester(base_url)
    passed = 0
    failed = 0
    failures = []
    
    try:
        # Test 1: get_current_user
        try:
            await tester.test_get_current_user()
            passed += 1
        except Exception as e:
            failed += 1
            failures.append(("get_current_user", str(e)))
            print(f"   ❌ get_current_user FAILED: {e}")
        
        # Test 2: list_groups
        try:
            await tester.test_list_groups()
            passed += 1
        except Exception as e:
            failed += 1
            failures.append(("list_groups", str(e)))
            print(f"   ❌ list_groups FAILED: {e}")
        
        # Test 3: list_expenses
        try:
            expenses_data = await tester.test_list_expenses()
            passed += 1
            
            # We'll get the expense ID from search results instead
            expense_id = None
        except Exception as e:
            failed += 1
            failures.append(("list_expenses", str(e)))
            print(f"   ❌ list_expenses FAILED: {e}")
            expense_id = None
        
        # Test 4: search (required for ChatGPT)
        try:
            search_data = await tester.test_search()
            passed += 1
            
            # Extract ID from search results - use the formatted ID directly
            if search_data.get("results"):
                first_result = search_data["results"][0]
                # Use the formatted ID directly (e.g., "expense_4135754641")
                expense_id = first_result.get("id", "")
        except Exception as e:
            failed += 1
            failures.append(("search", str(e)))
            print(f"   ❌ search FAILED: {e}")
        
        # Test 5: fetch (required for ChatGPT)
        # If search didn't return results, try to construct an ID from list_expenses
        if not expense_id and expenses_data and expenses_data.get("expenses"):
            first_expense = expenses_data["expenses"][0]
            numeric_id = first_expense.get("id")
            if numeric_id:
                expense_id = f"expense_{numeric_id}"
                print(f"\n💡 Using expense ID from list_expenses: {expense_id}")
        
        if expense_id:
            try:
                await tester.test_fetch(expense_id)
                passed += 1
            except Exception as e:
                failed += 1
                failures.append(("fetch", str(e)))
                print(f"   ❌ fetch FAILED: {e}")
        else:
            print("\n⚠️ Skipping fetch test - no expense ID available")
            failed += 1
            failures.append(("fetch", "No expense ID available for testing"))
        
        # Print summary
        tester.print_summary(passed, failed, failures)
        
    finally:
        await tester.close()
    
    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
