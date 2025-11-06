"""Main entry point for the Splitwise MCP server using pure MCP SDK."""

from __future__ import annotations

from .mcp_server import run_mcp_server


def main():
    """Main entry point for the MCP server."""
    run_mcp_server()


if __name__ == "__main__":
    main()
