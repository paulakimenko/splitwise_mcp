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

# MongoDB Configuration
ENV_MONGO_URI = "MONGO_URI"
ENV_DB_NAME = "DB_NAME"

# Caching Configuration
ENV_CACHE_ENABLED = "CACHE_ENABLED"
ENV_CACHE_TTL_EXPENSES_MINUTES = "CACHE_TTL_EXPENSES_MINUTES"
ENV_CACHE_TTL_FRIENDS_MINUTES = "CACHE_TTL_FRIENDS_MINUTES"
ENV_CACHE_TTL_USERS_MINUTES = "CACHE_TTL_USERS_MINUTES"
ENV_CACHE_TTL_GROUPS_MINUTES = "CACHE_TTL_GROUPS_MINUTES"
ENV_CACHE_TTL_CATEGORIES_MINUTES = "CACHE_TTL_CATEGORIES_MINUTES"
ENV_CACHE_TTL_CURRENCIES_MINUTES = "CACHE_TTL_CURRENCIES_MINUTES"
ENV_CACHE_TTL_NOTIFICATIONS_MINUTES = "CACHE_TTL_NOTIFICATIONS_MINUTES"

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
METHOD_GET_BALANCE = "get_balance"

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
# Entity Types (used for caching and collections)
# =============================================================================

ENTITY_EXPENSES = "expenses"
ENTITY_FRIENDS = "friends"
ENTITY_USERS = "users"
ENTITY_GROUPS = "groups"
ENTITY_CATEGORIES = "categories"
ENTITY_CURRENCIES = "currencies"
ENTITY_NOTIFICATIONS = "notifications"

# =============================================================================
# Entity Field Names
# =============================================================================

# Common fields
FIELD_ID = "id"
FIELD_TIMESTAMP = "timestamp"
FIELD_RESPONSE_DATA = "response_data"

# Expense fields
FIELD_EXPENSE_COST = "cost"
FIELD_EXPENSE_DESCRIPTION = "description"
FIELD_EXPENSE_DATE = "date"
FIELD_EXPENSE_CATEGORY_ID = "category_id"
FIELD_EXPENSE_GROUP_ID = "group_id"
FIELD_EXPENSE_CURRENCY_CODE = "currency_code"
FIELD_EXPENSE_CREATED_AT = "created_at"
FIELD_EXPENSE_UPDATED_AT = "updated_at"

# Group fields
FIELD_GROUP_NAME = "name"
FIELD_GROUP_TYPE = "group_type"
FIELD_GROUP_MEMBERS = "members"

# User fields
FIELD_USER_FIRST_NAME = "first_name"
FIELD_USER_LAST_NAME = "last_name"
FIELD_USER_EMAIL = "email"

# Comment fields
FIELD_COMMENT_CONTENT = "content"
FIELD_COMMENT_EXPENSE_ID = "expense_id"

# Category fields
FIELD_CATEGORY_NAME = "name"

# =============================================================================
# Log Operation Types
# =============================================================================

LOG_OP_TOOL_CALL = "TOOL_CALL"
LOG_OP_RESOURCE_READ = "RESOURCE_READ"
LOG_OP_CACHE_HIT = "CACHE_HIT"
LOG_OP_CACHE_MISS = "CACHE_MISS"
LOG_OP_CACHE_FALLBACK = "CACHE_FALLBACK"
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

DEFAULT_MONGO_URI = "mongodb://localhost:27017"
DEFAULT_DB_NAME = "splitwise"
DEFAULT_CACHE_ENABLED = "true"

# Default TTL values (in minutes)
DEFAULT_TTL_EXPENSES = 5
DEFAULT_TTL_FRIENDS = 5
DEFAULT_TTL_USERS = 60
DEFAULT_TTL_GROUPS = 60
DEFAULT_TTL_CATEGORIES = 1440  # 24 hours
DEFAULT_TTL_CURRENCIES = 1440  # 24 hours
DEFAULT_TTL_NOTIFICATIONS = 0  # Never cache

# MCP Transport defaults
DEFAULT_MCP_TRANSPORT = "stdio"
DEFAULT_MCP_HOST = "0.0.0.0"
DEFAULT_MCP_PORT = 8000
