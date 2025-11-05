"""Integration test configuration and fixtures."""

import asyncio
import os
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.splitwise_client import SplitwiseClient


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def splitwise_api_key() -> str:
    """Get Splitwise API key from environment."""
    api_key = os.getenv("SPLITWISE_API_KEY")
    if not api_key:
        pytest.skip("SPLITWISE_API_KEY not set - skipping integration tests")
    return api_key


@pytest.fixture(scope="session")
def splitwise_client(splitwise_api_key: str) -> SplitwiseClient:
    """Create a Splitwise client for integration tests."""
    return SplitwiseClient(api_key=splitwise_api_key)


@pytest.fixture(scope="session")
def test_client(splitwise_client: SplitwiseClient):
    """Create a test client for the FastAPI app with proper state setup."""
    # Create test client with lifespan events disabled to avoid startup issues
    with TestClient(app) as client:
        # Manually set the client in app state since lifespan won't run in test mode
        app.state.client = splitwise_client
        yield client


@pytest.fixture(scope="session")
async def test_group_name() -> str:
    """Generate a unique test group name."""
    import time

    timestamp = int(time.time())
    return f"MCP_Test_Group_{timestamp}"


@pytest.fixture(scope="session")
async def test_group_id(
    splitwise_client: SplitwiseClient, test_group_name: str
) -> AsyncGenerator[int, None]:
    """Create a test group for integration tests and clean it up afterward."""
    try:
        # Create test group
        from splitwise.group import Group

        group = Group()
        group.setName(test_group_name)
        group.setType("apartment")  # Use apartment type for test group

        # Create the group via Splitwise API
        created_group = await asyncio.to_thread(
            splitwise_client.raw_client.createGroup, group
        )

        group_id = created_group.id
        print(f"Created test group '{test_group_name}' with ID: {group_id}")

        yield group_id

    finally:
        # Cleanup: Delete the test group
        try:
            await asyncio.to_thread(splitwise_client.raw_client.deleteGroup, group_id)
            print(f"Cleaned up test group '{test_group_name}' (ID: {group_id})")
        except Exception as e:
            print(f"Warning: Failed to delete test group {group_id}: {e}")


@pytest.fixture
async def current_user_id(splitwise_client: SplitwiseClient) -> int:
    """Get the current user's ID."""
    return splitwise_client.get_current_user_id()
