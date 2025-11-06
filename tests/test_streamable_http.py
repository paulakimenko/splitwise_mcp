"""Tests for MCP server Streamable HTTP transport configuration.

These tests validate the transport mode detection and configuration
without requiring a running server.
"""

from __future__ import annotations

import os
from unittest.mock import Mock, patch

import pytest

from app.mcp_server import run_mcp_server


class TestStreamableHTTPTransport:
    """Test Streamable HTTP transport configuration."""

    def test_default_stdio_transport(self):
        """Test that stdio transport is used by default."""
        with (
            patch.dict(os.environ, {}, clear=True),  # Clear environment
            patch("app.mcp_server.mcp") as mock_mcp,
        ):
            # Mock the server run method
            mock_mcp.run = Mock()

            run_mcp_server()

            # Should call run() with no arguments (stdio default)
            mock_mcp.run.assert_called_once_with()

    def test_streamable_http_transport(self):
        """Test that streamable-http transport is configured correctly."""
        with (
            patch.dict(
                os.environ,
                {
                    "MCP_TRANSPORT": "streamable-http",
                    "MCP_HOST": "127.0.0.1",
                    "MCP_PORT": "9000",
                },
            ),
            patch("app.mcp_server.mcp") as mock_mcp,
        ):
            # Mock the server run method
            mock_mcp.run = Mock()

            run_mcp_server()

            # Should call run() with HTTP transport parameters
            mock_mcp.run.assert_called_once_with(
                transport="streamable-http", host="127.0.0.1", port=9000
            )

    def test_streamable_http_default_values(self):
        """Test that HTTP transport uses correct default host and port."""
        with (
            patch.dict(
                os.environ,
                {
                    "MCP_TRANSPORT": "streamable-http"
                    # No MCP_HOST or MCP_PORT - should use defaults
                },
                clear=True,
            ),
            patch("app.mcp_server.mcp") as mock_mcp,
        ):
            # Mock the server run method
            mock_mcp.run = Mock()

            run_mcp_server()

            # Should call run() with default host and port
            mock_mcp.run.assert_called_once_with(
                transport="streamable-http", host="0.0.0.0", port=8000
            )

    def test_invalid_port_handling(self):
        """Test that invalid port values are handled correctly."""
        with (
            patch.dict(
                os.environ,
                {"MCP_TRANSPORT": "streamable-http", "MCP_PORT": "invalid_port"},
            ),
            patch("app.mcp_server.mcp") as mock_mcp,
        ):
            # Mock the server run method
            mock_mcp.run = Mock()

            # Should raise ValueError for invalid port
            with pytest.raises(ValueError):
                run_mcp_server()

    def test_transport_mode_detection(self):
        """Test different transport mode values."""
        test_cases = [
            ("stdio", "stdio"),
            ("streamable-http", "streamable-http"),
            ("invalid-transport", "stdio"),  # Falls back to stdio for unknown values
            ("", "stdio"),  # Empty string falls back to stdio
        ]

        for env_value, expected_behavior in test_cases:
            with (
                patch.dict(os.environ, {"MCP_TRANSPORT": env_value}),
                patch("app.mcp_server.mcp") as mock_mcp,
            ):
                # Mock the server run method
                mock_mcp.run = Mock()

                run_mcp_server()

                if expected_behavior == "streamable-http":
                    # Should call with HTTP parameters
                    mock_mcp.run.assert_called_once_with(
                        transport="streamable-http", host="0.0.0.0", port=8000
                    )
                else:
                    # Should call with stdio (default)
                    mock_mcp.run.assert_called_once_with()

    @patch("builtins.print")
    def test_startup_messages(self, mock_print):
        """Test that appropriate startup messages are printed."""
        # Test stdio message
        with (
            patch.dict(os.environ, {}, clear=True),
            patch("app.mcp_server.mcp") as mock_mcp,
        ):
            mock_mcp.run = Mock()
            run_mcp_server()
            mock_print.assert_called_with(
                "Starting Splitwise MCP server with stdio transport"
            )

        # Test HTTP message
        with (
            patch.dict(
                os.environ,
                {
                    "MCP_TRANSPORT": "streamable-http",
                    "MCP_HOST": "localhost",
                    "MCP_PORT": "8080",
                },
            ),
            patch("app.mcp_server.mcp") as mock_mcp,
        ):
            mock_mcp.run = Mock()
            run_mcp_server()
            mock_print.assert_called_with(
                "Starting Splitwise MCP server with Streamable HTTP transport on localhost:8080"
            )

    def test_docker_environment_simulation(self):
        """Test configuration that matches Docker environment."""
        docker_env = {
            "MCP_TRANSPORT": "streamable-http",
            "MCP_HOST": "0.0.0.0",
            "MCP_PORT": "8000",
            "SPLITWISE_API_KEY": "test_key",
            "MONGO_URI": "mongodb://mongo:27017",
            "DB_NAME": "splitwise",
        }

        with (
            patch.dict(os.environ, docker_env),
            patch("app.mcp_server.mcp") as mock_mcp,
        ):
            mock_mcp.run = Mock()

            run_mcp_server()

            # Should configure for Docker environment
            mock_mcp.run.assert_called_once_with(
                transport="streamable-http", host="0.0.0.0", port=8000
            )
