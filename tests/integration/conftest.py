"""Integration test configuration and fixtures."""

import os
import subprocess
import time
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv

from app.splitwise_client import SplitwiseClient

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session")
def splitwise_client() -> SplitwiseClient:
    """Create a Splitwise client for integration tests."""
    # Check for any valid credentials
    api_key = os.getenv("SPLITWISE_API_KEY")
    consumer_key = os.getenv("SPLITWISE_CONSUMER_KEY")
    consumer_secret = os.getenv("SPLITWISE_CONSUMER_SECRET")

    if not api_key and not (consumer_key and consumer_secret):
        pytest.skip(
            "Neither SPLITWISE_API_KEY nor SPLITWISE_CONSUMER_KEY/SECRET set - skipping integration tests"
        )

    return SplitwiseClient()


@pytest.fixture(scope="session")
def mcp_client(splitwise_client: SplitwiseClient):
    """Create an MCP client for testing MCP server functionality."""
    # For MCP server testing, we primarily use the splitwise_client directly
    # since the MCP server uses it internally
    return splitwise_client


@pytest.fixture(scope="session")
def test_group_name() -> str:
    """Generate a unique test group name."""
    import time

    timestamp = int(time.time())
    return f"MCP_Test_Group_{timestamp}"


@pytest.fixture(scope="session")
def test_group_id(splitwise_client: SplitwiseClient, test_group_name: str):
    """Create a test group for integration tests and clean it up afterward."""
    group_id = None
    try:
        # Create test group
        from splitwise.group import Group

        group = Group()
        group.setName(test_group_name)
        group.setType("apartment")  # Use apartment type for test group

        # Create the group via Splitwise API
        result = splitwise_client.raw_client.createGroup(group)
        # createGroup returns a tuple (Group, None), so get the first element
        created_group = result[0] if isinstance(result, tuple) else result
        group_id = created_group.id
        print(f"Created test group '{test_group_name}' with ID: {group_id}")

        yield group_id

    finally:
        # Cleanup: Delete the test group (only if it was created)
        if group_id is not None:
            try:
                splitwise_client.raw_client.deleteGroup(group_id)
                print(f"Cleaned up test group '{test_group_name}' (ID: {group_id})")
            except Exception as e:
                print(f"Warning: Failed to delete test group {group_id}: {e}")
        else:
            print("Warning: Could not clean up test group (group creation failed)")


@pytest.fixture(scope="session")
def current_user_id(splitwise_client: SplitwiseClient) -> int:
    """Get the current user's ID."""
    user_id = splitwise_client.get_current_user_id()
    if not user_id:
        pytest.skip("Could not get current user ID - authentication may be invalid")
    return user_id


# MCP-specific configuration
def pytest_configure(config):
    """Configure pytest for MCP testing."""
    # Add custom markers for MCP tests
    config.addinivalue_line(
        "markers", "mcp: mark test as MCP-specific integration test"
    )
    config.addinivalue_line(
        "markers", "mcp_slow: mark test as slow MCP test (may create/delete data)"
    )


@pytest.fixture(scope="session")
def mcp_test_config():
    """Configuration for MCP tests."""
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    return {
        "base_url": f"{base_url}/mcp",
        "timeout": int(os.getenv("MCP_TEST_TIMEOUT", "10")),
        "has_api_key": bool(
            os.getenv("SPLITWISE_API_KEY") or os.getenv("SPLITWISE_CONSUMER_KEY")
        ),
    }


@pytest.fixture(scope="session")
def mcp_server_process():
    """Start MCP server for HTTP testing."""
    # Check if server is already running
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    mcp_endpoint = f"{base_url}/mcp"

    def is_server_running():
        try:
            requests.get(base_url, timeout=2)
            return True
        except requests.exceptions.RequestException:
            return False

    if is_server_running():
        print(f"MCP server already running at {mcp_endpoint}")
        yield mcp_endpoint
        return

    # Start the MCP server with HTTP transport
    server_process = None
    try:
        # Set environment variables for HTTP transport
        env = os.environ.copy()
        env.update(
            {
                "MCP_TRANSPORT": "streamable-http",
                "MCP_HOST": "127.0.0.1",
                "MCP_PORT": "8000",
            }
        )

        print("Starting MCP server for HTTP testing...")
        server_process = subprocess.Popen(
            [".venv/bin/python", "-m", "app.main"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=Path(__file__).parent.parent.parent,
        )

        # Wait for server to start
        max_attempts = 30
        for _attempt in range(max_attempts):
            if is_server_running():
                print(f"MCP server started successfully at {mcp_endpoint}")
                break
            time.sleep(1)
        else:
            # Server didn't start - get error output
            stdout, stderr = server_process.communicate(timeout=5)
            raise RuntimeError(
                f"MCP server failed to start after {max_attempts}s. "
                f"stdout: {stdout.decode()}, stderr: {stderr.decode()}"
            )

        yield mcp_endpoint

    finally:
        # Clean up server process
        if server_process and server_process.poll() is None:
            print("Shutting down MCP server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server_process.kill()
                server_process.wait()
