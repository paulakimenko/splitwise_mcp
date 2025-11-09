"""Shared constants for the Splitwise MCP service.

This module centralizes all API method names, environment variable names,
and entity field names used throughout the application.
"""

from __future__ import annotations

# =============================================================================
# Environment Variable Names
# =============================================================================

# Splitwise Authentication
ENV_SPLITWISE_API_KEY = "SPLITWISE_API_KEY"
ENV_SPLITWISE_CONSUMER_KEY = "SPLITWISE_CONSUMER_KEY"
ENV_SPLITWISE_CONSUMER_SECRET = "SPLITWISE_CONSUMER_SECRET"

# MCP Transport Configuration
ENV_MCP_TRANSPORT = "MCP_TRANSPORT"
ENV_MCP_HOST = "MCP_HOST"
ENV_MCP_PORT = "MCP_PORT"

# =============================================================================
# API Method Names (snake_case - used in MCP layer)
# =============================================================================

# GET Methods (Read Operations)
METHOD_GET_CURRENT_USER = "get_current_user"
METHOD_LIST_GROUPS = "list_groups"
METHOD_GET_GROUP = "get_group"
METHOD_LIST_EXPENSES = "list_expenses"
METHOD_GET_EXPENSE = "get_expense"
METHOD_LIST_FRIENDS = "list_friends"
METHOD_GET_FRIEND = "get_friend"
METHOD_LIST_CATEGORIES = "list_categories"
METHOD_LIST_CURRENCIES = "list_currencies"
METHOD_GET_EXCHANGE_RATES = "get_exchange_rates"
METHOD_LIST_NOTIFICATIONS = "list_notifications"
METHOD_GET_COMMENTS = "get_comments"
# POST Methods (Write Operations)
METHOD_CREATE_EXPENSE = "create_expense"
METHOD_CREATE_GROUP = "create_group"
METHOD_UPDATE_EXPENSE = "update_expense"
METHOD_DELETE_EXPENSE = "delete_expense"
METHOD_UNDELETE_EXPENSE = "undelete_expense"
METHOD_CREATE_FRIEND = "create_friend"
METHOD_CREATE_FRIENDS = "create_friends"
METHOD_DELETE_FRIEND = "delete_friend"
METHOD_ADD_USER_TO_GROUP = "add_user_to_group"
METHOD_REMOVE_USER_FROM_GROUP = "remove_user_from_group"
METHOD_DELETE_GROUP = "delete_group"
METHOD_UNDELETE_GROUP = "undelete_group"
METHOD_UPDATE_USER = "update_user"
METHOD_CREATE_COMMENT = "create_comment"
METHOD_DELETE_COMMENT = "delete_comment"

# =============================================================================
# Log Operation Types
# =============================================================================

LOG_OP_API_ERROR = "API_ERROR"

# =============================================================================
# MCP Protocol Constants
# =============================================================================

# URI Schemes
URI_SCHEME_SPLITWISE = "splitwise"

# Resource URI patterns
RESOURCE_CURRENT_USER = f"{URI_SCHEME_SPLITWISE}://current_user"
RESOURCE_GROUPS = f"{URI_SCHEME_SPLITWISE}://groups"
RESOURCE_GROUP_BY_ID = f"{URI_SCHEME_SPLITWISE}://group/{{id}}"
RESOURCE_EXPENSES = f"{URI_SCHEME_SPLITWISE}://expenses"
RESOURCE_EXPENSE_BY_ID = f"{URI_SCHEME_SPLITWISE}://expense/{{id}}"
RESOURCE_FRIENDS = f"{URI_SCHEME_SPLITWISE}://friends"
RESOURCE_FRIEND_BY_ID = f"{URI_SCHEME_SPLITWISE}://friend/{{id}}"
RESOURCE_CATEGORIES = f"{URI_SCHEME_SPLITWISE}://categories"
RESOURCE_CURRENCIES = f"{URI_SCHEME_SPLITWISE}://currencies"
RESOURCE_NOTIFICATIONS = f"{URI_SCHEME_SPLITWISE}://notifications"
RESOURCE_COMMENTS_BY_EXPENSE = f"{URI_SCHEME_SPLITWISE}://comments/{{expense_id}}"

# =============================================================================
# Default Values
# =============================================================================

# MCP Transport defaults
DEFAULT_MCP_TRANSPORT = "stdio"
DEFAULT_MCP_HOST = "0.0.0.0"
DEFAULT_MCP_PORT = 8000
