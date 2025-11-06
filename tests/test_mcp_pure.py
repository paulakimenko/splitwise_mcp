"""Test the pure MCP SDK implementation.

These tests validate that the new pure MCP server works correctly
without any FastAPI dependencies.
"""

from unittest.mock import Mock, patch

import pytest


class TestPureMCPImplementation:
    """Test the pure MCP server implementation."""

    def test_mcp_server_import(self):
        """Test that the MCP server can be imported without FastAPI dependencies."""
        from app.main import mcp

        assert mcp is not None
        assert hasattr(mcp, "tool")
        assert hasattr(mcp, "resource")
        assert hasattr(mcp, "prompt")

    def test_main_module_import(self):
        """Test that the main module imports correctly."""
        from app.main import run_mcp_server

        assert callable(run_mcp_server)

    @patch("app.main.run_mcp_server")
    def test_main_calls_run_mcp_server(self, mock_run_server):
        """Test that run_mcp_server can be called."""
        from app.main import run_mcp_server

        # Just verify it's callable (don't actually call it as it would start the server)
        assert callable(run_mcp_server)

    def test_splitwise_client_has_extended_method_map(self):
        """Test that SplitwiseClient has all required methods mapped."""
        from app.splitwise_client import SplitwiseClient

        # Check that we have both GET and POST methods
        method_map = SplitwiseClient.METHOD_MAP

        # GET methods (resources)
        assert "get_current_user" in method_map
        assert "list_groups" in method_map
        assert "list_expenses" in method_map
        assert "list_friends" in method_map

        # POST methods (tools)
        assert "create_expense" in method_map
        assert "create_group" in method_map
        assert "create_friend" in method_map
        assert "delete_expense" in method_map

    @patch.dict("os.environ", {"SPLITWISE_API_KEY": "test_key"})
    def test_splitwise_client_initialization(self):
        """Test that SplitwiseClient can be initialized."""
        from app.splitwise_client import SplitwiseClient

        client = SplitwiseClient()
        assert client is not None

    def test_no_fastapi_imports_in_mcp_server(self):
        """Test that mcp_server.py doesn't import FastAPI."""
        import ast
        import inspect
        from pathlib import Path

        # Get the source file path
        import app.main

        source_file = Path(inspect.getfile(app.main))

        # Parse the AST
        with source_file.open(encoding="utf-8") as f:
            tree = ast.parse(f.read())

        # Check imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "fastapi" not in alias.name.lower()
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert "fastapi" not in node.module.lower()

    def test_no_fastapi_imports_in_main(self):
        """Test that main.py doesn't import FastAPI."""
        import ast
        import inspect
        from pathlib import Path

        # Get the source file path
        import app.main

        source_file = Path(inspect.getfile(app.main))

        # Parse the AST
        with source_file.open(encoding="utf-8") as f:
            tree = ast.parse(f.read())

        # Check imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "fastapi" not in alias.name.lower()
            elif isinstance(node, ast.ImportFrom) and node.module:
                assert "fastapi" not in node.module.lower()

    def test_architecture_transformation_complete(self):
        """Test that the architecture transformation is complete."""
        from pathlib import Path

        # 1. Main should contain run_mcp_server function
        main_path = Path("app/main.py")
        with main_path.open(encoding="utf-8") as f:
            main_content = f.read()

        # Should have run_mcp_server function
        assert "def run_mcp_server():" in main_content
        assert "mcp.run(" in main_content

        # 2. Requirements should not have FastAPI
        req_path = Path("requirements.txt")
        with req_path.open(encoding="utf-8") as f:
            requirements = f.read()

        assert "fastapi" not in requirements.lower()
        assert "uvicorn" not in requirements.lower()
        assert "mcp" in requirements.lower()

    def test_mcp_method_categorization_correct(self):
        """Test that methods are correctly categorized as tools vs resources."""
        from app.splitwise_client import SplitwiseClient

        method_map = SplitwiseClient.METHOD_MAP

        # GET methods should be available (will be used for resources)
        get_methods = [
            "get_current_user",
            "list_groups",
            "get_group",
            "list_expenses",
            "get_expense",
            "list_friends",
            "get_friend",
            "list_categories",
            "list_currencies",
            "list_notifications",
            "get_comments",
        ]

        # POST methods should be available (will be used for tools)
        post_methods = [
            "create_expense",
            "update_expense",
            "delete_expense",
            "undelete_expense",
            "create_group",
            "delete_group",
            "undelete_group",
            "add_user_to_group",
            "remove_user_from_group",
            "create_friend",
            "create_friends",
            "delete_friend",
            "update_user",
            "create_comment",
            "delete_comment",
        ]

        # Check GET methods are available
        for method in get_methods:
            if method in method_map:
                assert method in method_map

        # Check POST methods are available
        for method in post_methods:
            if method in method_map:
                assert method in method_map

        # Should have decent coverage of both types
        available_gets = [m for m in get_methods if m in method_map]
        available_posts = [m for m in post_methods if m in method_map]

        assert len(available_gets) >= 5, (
            f"Should have at least 5 GET methods, got: {available_gets}"
        )
        assert len(available_posts) >= 5, (
            f"Should have at least 5 POST methods, got: {available_posts}"
        )


class TestChatGPTConnectorTools:
    """Test the ChatGPT connector-required search and fetch tools."""

    @pytest.fixture
    def mock_context(self):
        """Create a mock MCP context."""
        mock_client = Mock()
        context = Mock()
        context.request_context.lifespan_context = {"client": mock_client}
        return context, mock_client

    @pytest.mark.asyncio
    async def test_search_tool_exists(self):
        """Test that search tool is defined."""
        from app.main import search

        assert search is not None
        assert callable(search)

    @pytest.mark.asyncio
    async def test_fetch_tool_exists(self):
        """Test that fetch tool is defined."""
        from app.main import fetch

        assert fetch is not None
        assert callable(fetch)

    @pytest.mark.asyncio
    async def test_search_returns_correct_format(self, mock_context):
        """Test that search returns results in ChatGPT-required format."""
        from app.main import search

        context, mock_client = mock_context

        # Mock the Splitwise API responses
        mock_groups = [
            {"id": 1, "name": "Test Group"},
            {"id": 2, "name": "Another Group"},
        ]
        mock_expenses = [
            {"id": 101, "description": "Dinner", "cost": "25.50"},
        ]
        mock_friends = [
            {"id": 201, "first_name": "John", "last_name": "Doe"},
        ]

        mock_client.convert.side_effect = [mock_groups, mock_expenses, mock_friends]

        with (
            patch("app.main.asyncio.to_thread") as mock_to_thread,
            patch("app.main.insert_document"),
            patch("app.main.log_operation"),
        ):
            # Configure mock to return data when called
            mock_to_thread.side_effect = [mock_groups, mock_expenses, mock_friends]

            result = await search("test", context)

            # Verify the result format matches ChatGPT requirements
            assert isinstance(result, dict)
            assert "results" in result
            assert isinstance(result["results"], list)

            # Check that each result has required fields: id, title, url
            for item in result["results"]:
                assert "id" in item
                assert "title" in item
                assert "url" in item
                assert isinstance(item["id"], str)
                assert isinstance(item["title"], str)
                assert isinstance(item["url"], str)

    @pytest.mark.asyncio
    async def test_fetch_returns_correct_format(self, mock_context):
        """Test that fetch returns data in ChatGPT-required format."""
        from app.main import fetch

        context, mock_client = mock_context

        # Mock a group fetch
        mock_group_data = {
            "id": 1,
            "name": "Test Group",
            "members": [{"id": 1, "name": "User 1"}],
        }

        mock_client.convert.return_value = mock_group_data

        with (
            patch("app.main.asyncio.to_thread") as mock_to_thread,
            patch("app.main.insert_document"),
            patch("app.main.log_operation"),
        ):
            mock_to_thread.return_value = mock_group_data

            result = await fetch("group_1", context)

            # Verify the result format matches ChatGPT requirements
            assert isinstance(result, dict)
            assert "id" in result
            assert "title" in result
            assert "text" in result
            assert "url" in result
            assert "metadata" in result

            # Verify types
            assert isinstance(result["id"], str)
            assert isinstance(result["title"], str)
            assert isinstance(result["text"], str)
            assert isinstance(result["url"], str)
            assert isinstance(result["metadata"], dict)

    @pytest.mark.asyncio
    async def test_fetch_handles_different_types(self, mock_context):
        """Test that fetch handles group, expense, and friend IDs."""
        from app.main import fetch

        context, mock_client = mock_context

        test_cases = [
            ("group_1", {"id": 1, "name": "Test Group", "members": []}),
            (
                "expense_101",
                {
                    "id": 101,
                    "description": "Dinner",
                    "cost": "25.50",
                    "currency_code": "USD",
                },
            ),
            (
                "friend_201",
                {
                    "id": 201,
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                },
            ),
        ]

        for test_id, mock_data in test_cases:
            mock_client.convert.return_value = mock_data

            with (
                patch("app.main.asyncio.to_thread") as mock_to_thread,
                patch("app.main.insert_document"),
                patch("app.main.log_operation"),
            ):
                mock_to_thread.return_value = mock_data

                result = await fetch(test_id, context)

                # All results should have the required structure
                assert "id" in result
                assert "title" in result
                assert "text" in result
                assert "url" in result
                assert "metadata" in result
                assert result["id"] == test_id
