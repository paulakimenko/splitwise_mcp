#!/usr/bin/env python3
"""Test the MCP server functionality using the official MCP CLI."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def test_mcp_server():
    """Test the MCP server using mcp CLI commands."""

    # Create a temporary MCP config for testing
    test_config = {
        "mcpServers": {
            "splitwise": {
                "command": "python",
                "args": ["-m", "app.mcp_server"],
                "env": {
                    "SPLITWISE_API_KEY": "test_key_123",  # Mock key for testing
                    "MONGO_URI": "mongodb://localhost:27017",
                    "DB_NAME": "splitwise_test"
                }
            }
        }
    }

    # Write config to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_config, f, indent=2)
        config_path = f.name

    try:
        # Test 1: List available tools
        print("Testing MCP server tool list...")
        result = subprocess.run([
            'mcp', 'list', 'tools', config_path, 'splitwise'
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("✅ MCP server tools listed successfully")
            print(f"Tools output:\n{result.stdout}")
        else:
            print("❌ Failed to list MCP tools")
            print(f"Error: {result.stderr}")

        # Test 2: Call a simple tool
        print("\nTesting MCP tool call...")
        result = subprocess.run([
            'mcp', 'call', 'get_current_user', '{}', config_path, 'splitwise'
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print("✅ MCP tool call succeeded")
            print(f"Tool output:\n{result.stdout}")
        else:
            print("❌ MCP tool call failed")
            print(f"Error: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("❌ MCP commands timed out")
    except FileNotFoundError:
        print("❌ mcp CLI not found. Install with: pip install mcp")
    except Exception as exc:
        print(f"❌ Test failed with error: {exc}")
    finally:
        # Clean up temp config file
        config_file = Path(config_path)
        if config_file.exists():
            config_file.unlink()


def test_direct_mcp_server():
    """Test running the MCP server directly."""
    print("Testing direct MCP server execution...")

    # Set test environment
    test_env = os.environ.copy()
    test_env.update({
        'SPLITWISE_API_KEY': 'test_key_123',
        'MONGO_URI': 'mongodb://localhost:27017',
        'DB_NAME': 'splitwise_test'
    })

    try:
        # Try to start the server and send a simple request
        proc = subprocess.Popen([
            sys.executable, '-m', 'app.mcp_server'
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=test_env,
        text=True
        )

        # Send a capabilities request
        request = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}

        stdout, stderr = proc.communicate(
            input=json.dumps(request) + '\n',
            timeout=10
        )

        if proc.returncode == 0 or "capabilities" in stdout:
            print("✅ MCP server started and responded to initialize")
            print(f"Server response:\n{stdout}")
        else:
            print("❌ MCP server failed to start properly")
            print(f"Error: {stderr}")

    except subprocess.TimeoutExpired:
        print("❌ MCP server startup timed out")
        proc.kill()
    except Exception as exc:
        print(f"❌ Direct server test failed: {exc}")


if __name__ == "__main__":
    print("🧪 Testing Splitwise MCP Server\n")

    # Test the server directly first
    test_direct_mcp_server()

    print("\n" + "="*50 + "\n")

    # Test via MCP CLI
    test_mcp_server()

    print("\n🏁 MCP server tests complete!")
