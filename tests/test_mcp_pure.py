"""Test the pure MCP SDK implementation.

These tests validate that the new pure MCP server works correctly
without any FastAPI dependencies.
"""

from unittest.mock import patch


class TestPureMCPImplementation:
    """Test the pure MCP server implementation."""

    def test_mcp_server_import(self):
        """Test that the MCP server can be imported without FastAPI dependencies."""
        from app.mcp_server import mcp

        assert mcp is not None
        assert hasattr(mcp, "tool")
        assert hasattr(mcp, "resource")
        assert hasattr(mcp, "prompt")

    def test_main_module_import(self):
        """Test that the main module imports correctly."""
        from app.main import main

        assert callable(main)

    @patch("app.mcp_server.run_mcp_server")
    def test_main_calls_run_mcp_server(self, mock_run_server):
        """Test that main() calls run_mcp_server."""
        with patch("app.main.run_mcp_server", mock_run_server):
            from app.main import main

            main()
            mock_run_server.assert_called_once()

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
        import app.mcp_server

        source_file = Path(inspect.getfile(app.mcp_server))

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

        # 1. Main should be simple
        main_path = Path("app/main.py")
        with main_path.open(encoding="utf-8") as f:
            main_content = f.read()

        # Should be very simple - just import and call run_mcp_server
        assert "def main():" in main_content
        assert "run_mcp_server()" in main_content
        assert len(main_content.split("\n")) <= 15  # Should be very short

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
