"""Integration test configuration and fixtures."""

import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.main import app
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
def test_client(splitwise_client: SplitwiseClient):
    """Create a test client for the FastAPI app with proper state setup."""
    # Create test client with lifespan events disabled to avoid startup issues
    with TestClient(app) as client:
        # Manually set the client in app state since lifespan won't run in test mode
        app.state.client = splitwise_client
        yield client


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
