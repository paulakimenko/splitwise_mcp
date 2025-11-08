# Cached Splitwise Client - Technical Design Document

**Feature Status**: Planning  
**Target Branch**: `cached_client`  
**Author**: Development Team  
**Last Updated**: 2025-11-07

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Motivation & Goals](#motivation--goals)
3. [⚠️ CRITICAL: Cache Query Parameters](#️-critical-cache-query-parameters)
4. [Architecture Overview](#architecture-overview)
5. [Data Model & Entity Normalization](#data-model--entity-normalization)
6. [Caching Strategy](#caching-strategy)
7. [Cache Invalidation Logic](#cache-invalidation-logic)
8. [MongoDB Collections Schema](#mongodb-collections-schema)
9. [API Method Coverage](#api-method-coverage)
10. [Configuration](#configuration)
11. [Data Flow Diagrams](#data-flow-diagrams)
12. [Edge Cases & Error Handling](#edge-cases--error-handling)
13. [Implementation Plan](#implementation-plan)
14. [Testing Strategy](#testing-strategy)
15. [Performance Considerations](#performance-considerations)
16. [Future Enhancements](#future-enhancements)

---

## Executive Summary

This document outlines the design for implementing a **MongoDB-based caching layer** for the Splitwise MCP service. The caching system will:

- **Reduce external API calls** to Splitwise by 60-80% for typical usage patterns
- **Improve response latency** from ~500ms (API) to ~50ms (cache hit)
- **Enable offline operation** during Splitwise API outages (graceful degradation)
- **Maintain data freshness** through intelligent notification-based and time-based invalidation
- **Normalize API responses** into entity-specific MongoDB collections for efficient querying

The cache will act as a **write-through cache** with smart invalidation rules that balance freshness and performance.

---

## Motivation & Goals

### Current Pain Points

1. **High API Latency**: Every MCP tool call requires a round-trip to Splitwise API (~300-800ms)
2. **Rate Limiting Risk**: Splitwise API has undocumented rate limits that can cause throttling
3. **Redundant Requests**: Multiple tools fetch the same data (e.g., user info, group details)
4. **No Offline Capability**: Service completely fails if Splitwise API is unavailable
5. **ChatGPT Deep Research**: Multiple sequential API calls during research tasks cause poor UX

### Success Criteria

- ✅ **Performance**: 70%+ cache hit rate for typical user sessions
- ✅ **Freshness**: User-specific data never stale (notification-based invalidation)
- ✅ **Reliability**: Service remains functional during API outages (stale cache acceptable)
- ✅ **Compatibility**: Zero breaking changes to existing MCP tool interfaces
- ✅ **Observability**: Cache hit/miss metrics exposed for monitoring

---

## ⚠️ CRITICAL: Cache Query Parameters

### The Problem: Filter Parameters MUST Be Included in Cache Keys

**This section documents a critical caching bug that was discovered and fixed.**

### Bug Description

The initial implementation of `_build_cache_query()` only included `group_id` and `friend_id` in the cache lookup key for `list_expenses`. This caused **different API queries with different filter parameters to incorrectly share the same cached data**.

#### Example Scenario That Failed ❌

```python
# Request 1: Cache expenses for last 2 months
list_expenses(dated_after="2025-09-08", dated_before="2025-11-08")
# Cache key: {"method": "list_expenses"}  ← No date filters!
# Result: Fetches from API, caches response

# Request 2: Cache expenses for last month (1 minute later)
list_expenses(dated_after="2025-10-08", dated_before="2025-11-08")
# Cache key: {"method": "list_expenses"}  ← SAME KEY!
# Result: Returns 2-month data instead of 1-month data ❌
```

**Impact**: User receives incorrect data (2 months instead of 1 month) because the cache query ignored the date range parameters.

---

### The Fix: Complete Parameter Inclusion ✅

All filter parameters that affect the API response **MUST** be included in the cache query. The fixed implementation includes:

```python
def _build_cache_query(method_name: str, **kwargs) -> dict[str, Any] | None:
    """Build MongoDB query for cache lookup based on method and parameters.
    
    CRITICAL: All filter parameters that affect the API response MUST be included
    in the cache query. Otherwise, different queries will incorrectly share the same
    cached data, leading to incorrect results.
    """
    if method_name == "list_expenses":
        query = {"method": method_name}
        
        # Entity filters
        if "group_id" in kwargs:
            query["group_id"] = kwargs["group_id"]
        if "friend_id" in kwargs:
            query["friend_id"] = kwargs["friend_id"]
        
        # Date range filters - CRITICAL for correctness
        if "dated_after" in kwargs:
            query["dated_after"] = kwargs["dated_after"]
        if "dated_before" in kwargs:
            query["dated_before"] = kwargs["dated_before"]
        if "updated_after" in kwargs:
            query["updated_after"] = kwargs["updated_after"]
        if "updated_before" in kwargs:
            query["updated_before"] = kwargs["updated_before"]
        
        # Pagination - CRITICAL for correctness
        if "limit" in kwargs:
            query["limit"] = kwargs["limit"]
        if "offset" in kwargs:
            query["offset"] = kwargs["offset"]
        
        return query
```

#### Example Scenario That Works ✅

```python
# Request 1: Cache expenses for last 2 months
list_expenses(dated_after="2025-09-08", dated_before="2025-11-08")
# Cache key: {
#   "method": "list_expenses",
#   "dated_after": "2025-09-08",
#   "dated_before": "2025-11-08"
# }
# Result: Fetches from API, caches with FULL parameter key

# Request 2: Cache expenses for last month (1 minute later)
list_expenses(dated_after="2025-10-08", dated_before="2025-11-08")
# Cache key: {
#   "method": "list_expenses",
#   "dated_after": "2025-10-08",  ← DIFFERENT date
#   "dated_before": "2025-11-08"
# }
# Result: Different cache key → Fetches from API → Correct 1-month data ✅
```

---

### Complete Analysis: All Entity Types

This section reviews **every cacheable entity** to ensure filter parameters are correctly handled.

#### 1. ✅ Expenses (`list_expenses`)

**API Parameters** (from Splitwise OpenAPI):
- `group_id` (integer) - Filter by group
- `friend_id` (integer) - Filter by friend relationship
- `dated_after` (datetime) - Filter by expense date (after)
- `dated_before` (datetime) - Filter by expense date (before)
- `updated_after` (datetime) - Filter by last update (after)
- `updated_before` (datetime) - Filter by last update (before)
- `limit` (integer, default: 20) - Pagination size
- `offset` (integer, default: 0) - Pagination offset

**Cache Query** ✅ **ALL parameters included**:
```python
{
    "method": "list_expenses",
    "group_id": 12345,              # Entity filter
    "friend_id": 67890,             # Entity filter
    "dated_after": "2025-10-01",    # Date filter
    "dated_before": "2025-11-01",   # Date filter
    "updated_after": "2025-10-15",  # Update filter
    "updated_before": "2025-10-20", # Update filter
    "limit": 50,                    # Pagination
    "offset": 100                   # Pagination
}
```

**Why This Matters**:
- Different date ranges → Different expenses → Must be separate cache entries
- Different pagination → Different results → Must be separate cache entries
- Without this: User requesting "last month" would get "last 2 months" data ❌

---

#### 2. ✅ Expense Detail (`get_expense`)

**API Parameters**:
- `id` (integer) - Expense ID

**Cache Query** ✅ **Correct**:
```python
{
    "method": "get_expense",
    "expense_id": 4142333569
}
```

**Why This Matters**:
- Single expense lookup by ID
- No filter parameters beyond the ID
- Cache behavior: **Correct** ✅

---

#### 3. ✅ Groups (`list_groups`)

**API Parameters**: None (returns all groups for current user)

**Cache Query** ✅ **Correct**:
```python
{
    "method": "list_groups"
}
```

**Why This Matters**:
- No filter parameters
- Always returns same data for a user
- TTL-based invalidation (1 hour) is appropriate
- Cache behavior: **Correct** ✅

---

#### 4. ✅ Group Detail (`get_group`)

**API Parameters**:
- `id` (integer) - Group ID

**Cache Query** ✅ **Correct**:
```python
{
    "method": "get_group",
    "group_id": 12345
}
```

**Why This Matters**:
- Single group lookup by ID
- No filter parameters beyond the ID
- Cache behavior: **Correct** ✅

---

#### 5. ✅ Friends (`list_friends`)

**API Parameters**: None (returns all friends for current user)

**Cache Query** ✅ **Correct**:
```python
{
    "method": "list_friends"
}
```

**Why This Matters**:
- No filter parameters
- Always returns same data for a user
- TTL-based invalidation (5 minutes) handles balance changes
- Cache behavior: **Correct** ✅

---

#### 6. ✅ Friend Detail (`get_friend`)

**API Parameters**:
- `id` (integer) - Friend/User ID

**Cache Query** ✅ **Correct**:
```python
{
    "method": "get_friend",
    "friend_id": 67890
}
```

**Why This Matters**:
- Single friend lookup by ID
- No filter parameters beyond the ID
- Cache behavior: **Correct** ✅

---

#### 7. ✅ Current User (`get_current_user`)

**API Parameters**: None (returns authenticated user)

**Cache Query** ✅ **Correct**:
```python
{
    "method": "get_current_user"
}
```

**Why This Matters**:
- No filter parameters
- Always returns same user
- TTL-based invalidation (1 hour) is appropriate
- Cache behavior: **Correct** ✅

---

#### 8. ✅ Categories (`list_categories`)

**API Parameters**: None (returns static category list)

**Cache Query** ✅ **Correct**:
```python
{
    "method": "list_categories"
}
```

**Why This Matters**:
- No filter parameters
- Static/rarely-changing data
- Long TTL (24 hours) is appropriate
- Cache behavior: **Correct** ✅

---

#### 9. ✅ Currencies (`list_currencies`)

**API Parameters**: None (returns static currency list)

**Cache Query** ✅ **Correct**:
```python
{
    "method": "list_currencies"
}
```

**Why This Matters**:
- No filter parameters
- Static/rarely-changing data
- Long TTL (24 hours) is appropriate
- Cache behavior: **Correct** ✅

---

#### 10. ⚠️ Notifications (`list_notifications`)

**API Parameters** (from Splitwise docs):
- `updated_after` (datetime) - Filter by update time
- `limit` (integer) - Pagination size

**Cache Query** ⚠️ **NOT CACHED** (by design):
```python
# Notifications are never cached (TTL = 0)
# Always fetch fresh from API
```

**Why This Matters**:
- Notifications must always be fresh
- TTL set to 0 to disable caching
- Cache behavior: **Correct by Design** ✅

---

### Summary: Cache Query Correctness

| Entity Type | Filter Parameters | Cache Query Includes All Filters? | Status |
|-------------|-------------------|-----------------------------------|--------|
| **Expenses** | group_id, friend_id, dated_after, dated_before, updated_after, updated_before, limit, offset | ✅ Yes (FIXED) | ✅ Correct |
| **Expense Detail** | id | ✅ Yes | ✅ Correct |
| **Groups** | None | ✅ N/A | ✅ Correct |
| **Group Detail** | id | ✅ Yes | ✅ Correct |
| **Friends** | None | ✅ N/A | ✅ Correct |
| **Friend Detail** | id | ✅ Yes | ✅ Correct |
| **Current User** | None | ✅ N/A | ✅ Correct |
| **Categories** | None | ✅ N/A | ✅ Correct |
| **Currencies** | None | ✅ N/A | ✅ Correct |
| **Notifications** | updated_after, limit | ⚠️ Not Cached | ✅ By Design |

---

### Key Takeaways

1. **Filter Parameters = Cache Key Components**: Any parameter that changes the API response MUST be in the cache query
2. **Pagination Parameters Matter**: `limit` and `offset` affect results, so they're part of the cache key
3. **Date Range Parameters Are Critical**: Different date ranges = different data = separate cache entries
4. **Entity IDs Always Included**: Single-entity lookups (get_expense, get_group, etc.) always include the ID
5. **Static Data = Simple Cache Keys**: Categories/currencies have no filters, so simple method-based keys work
6. **Notifications Never Cached**: TTL=0 ensures always-fresh notification data

---

### Testing Recommendations

**Test Case 1: Date Range Caching**
```python
# Should create separate cache entries
result1 = list_expenses(dated_after="2025-09-01", dated_before="2025-10-01")
result2 = list_expenses(dated_after="2025-10-01", dated_before="2025-11-01")
assert result1 != result2  # Different data
assert cache_has_entries(2)  # Two separate cache entries
```

**Test Case 2: Pagination Caching**
```python
# Should create separate cache entries
page1 = list_expenses(limit=20, offset=0)
page2 = list_expenses(limit=20, offset=20)
assert page1 != page2  # Different expenses
assert cache_has_entries(2)  # Two separate cache entries
```

**Test Case 3: Entity Filter Caching**
```python
# Should create separate cache entries
group_expenses = list_expenses(group_id=12345)
friend_expenses = list_expenses(friend_id=67890)
assert group_expenses != friend_expenses
assert cache_has_entries(2)  # Two separate cache entries
```

---

## Architecture Overview

### High-Level Components

```
┌─────────────────────────────────────────────────────────────────┐
│                         MCP Client                               │
│                    (ChatGPT / API Consumer)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │ MCP Protocol (stdio/HTTP)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastMCP Server                               │
│                    (app/main.py - 22 tools)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              CachedSplitwiseClient (NEW)                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Cache Decision Engine                                    │  │
│  │  • Check notification timestamp (for user data)           │  │
│  │  • Check TTL (for shared/friend data)                     │  │
│  │  • Handle API unavailability gracefully                   │  │
│  └─────────────┬──────────────────────┬─────────────────────┘  │
│                │ Cache Hit            │ Cache Miss             │
│                ▼                      ▼                         │
│  ┌─────────────────────┐   ┌─────────────────────────────┐    │
│  │  MongoDB Cache      │   │  SplitwiseClient (existing) │    │
│  │  • Normalized       │   │  • Direct SDK wrapper       │    │
│  │    entities         │   │  • API calls                │    │
│  │  • Timestamps       │   │  • Response normalization   │    │
│  └─────────────────────┘   └──────────┬──────────────────┘    │
│                                        │                        │
│                                        ▼                        │
│                             ┌──────────────────────┐           │
│                             │  Splitwise API       │           │
│                             │  v3.0 REST Endpoint  │           │
│                             └──────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **FastMCP Server** | MCP protocol handling, tool routing, context management |
| **CachedSplitwiseClient** | Cache decision logic, entity normalization, invalidation |
| **MongoDB Cache** | Persistent storage of normalized entities with timestamps |
| **SplitwiseClient** | Existing direct wrapper around Splitwise Python SDK |
| **Splitwise API** | Source of truth for expense data |

---

## Data Model & Entity Normalization

### Core Normalization Principles

**1. Each Entity Type → Separate Collection**
- Users, expenses, groups, categories, etc. each have dedicated collections
- No embedded documents (except simple value objects like `picture`, `receipt`)
- All relationships via ID references, not embedded objects

**2. Each Entity Instance → Separate Document**
- One expense = one document in `expenses` collection
- One user = one document in `users` collection
- List responses (`GET /get_expenses`) normalize each item into separate document

**3. References Instead of Embedding**
- ❌ **WRONG**: Store user object inside expense document
  ```json
  {
    "_id": "expense_123",
    "created_by": {
      "id": 8633344,
      "first_name": "Test",
      "last_name": "User",
      "email": "testuser@example.com"
    }
  }
  ```

- ✅ **CORRECT**: Store only user ID reference
  ```json
  {
    "_id": "expense_123",
    "created_by_user_id": 8633344  // Reference to users collection
  }
  ```

**4. Junction Tables for Many-to-Many Relationships**
- Expense ↔ Users: `expense_shares` collection
- Group ↔ Users: `group_members` collection
- Friend ↔ Balances: `friend_balances` collection

**5. Denormalization Only for Query Performance**
- Keep array of user IDs in expense for fast lookups: `share_user_ids`
- Keep array of member IDs in group: `member_ids`
- These are duplicates of junction table data, optimized for queries

### Entity Extraction Rules

When an API response is received, normalize it into **atomic entities** stored in separate collections:

#### Example: `GET /get_groups` Response Normalization

**API Response Structure:**
```json
{
  "groups": [
    {
      "id": 12345,
      "name": "House Expenses",
      "group_type": "home",
      "updated_at": "2025-11-03T10:15:30Z",
      "members": [
        {
          "id": 67890,
          "first_name": "Alice",
          "last_name": "Smith",
          "email": "alice@example.com",
          "picture": {"medium": "https://..."},
          "balance": [
            {"currency_code": "USD", "amount": "-45.50"}
          ]
        },
        {
          "id": 54321,
          "first_name": "Bob",
          "last_name": "Jones",
          "email": "bob@example.com",
          "picture": {"medium": "https://..."},
          "balance": [
            {"currency_code": "USD", "amount": "45.50"}
          ]
        }
      ],
      "original_debts": [...],
      "simplified_debts": [...]
    }
  ]
}
```

**Normalized Storage (References Only, No Embedded Documents):**

1. **`groups` collection** - Store group metadata with member references:
```json
{
  "_id": "group_12345",
  "id": 12345,
  "name": "House Expenses",
  "group_type": "home",
  "updated_at": "2025-11-03T10:15:30Z",
  "member_ids": [67890, 54321],  // References to users collection
  "original_debts": [...],
  "simplified_debts": [...],
  "last_updated_date": "2025-11-03T14:32:28Z"
}
```

2. **`users` collection** - Each user as separate document:
```json
{
  "_id": "user_67890",
  "id": 67890,
  "first_name": "Alice",
  "last_name": "Smith",
  "email": "alice@example.com",
  "picture": {"medium": "https://..."},
  "registration_status": "confirmed",
  "last_updated_date": "2025-11-03T14:32:28Z"
}
```

```json
{
  "_id": "user_54321",
  "id": 54321,
  "first_name": "Bob",
  "last_name": "Jones",
  "email": "bob@example.com",
  "picture": {"medium": "https://..."},
  "registration_status": "confirmed",
  "last_updated_date": "2025-11-03T14:32:28Z"
}
```

3. **`group_members` collection** - Junction documents for many-to-many relationships:
```json
{
  "_id": "group_12345_user_67890",
  "group_id": 12345,        // Reference to groups collection
  "user_id": 67890,         // Reference to users collection
  "balances": [
    {"currency_code": "USD", "amount": "-45.50"}
  ],
  "last_updated_date": "2025-11-03T14:32:28Z"
}
```

```json
{
  "_id": "group_12345_user_54321",
  "group_id": 12345,        // Reference to groups collection
  "user_id": 54321,         // Reference to users collection
  "balances": [
    {"currency_code": "USD", "amount": "45.50"}
  ],
  "last_updated_date": "2025-11-03T14:32:28Z"
}
```

### Normalization Patterns by Entity Type

| API Endpoint | Primary Entities | Nested Entities | Junction Tables |
|--------------|------------------|-----------------|-----------------|
| `GET /get_current_user` | `current_user` | - | - |
| `GET /get_user/{id}` | `users` | - | - |
| `GET /get_groups` | `groups` | `users` (from members) | `group_members` (balances) |
| `GET /get_group/{id}` | `groups` | `users`, `debts` | `group_members` |
| `GET /get_expenses` | `expenses` | `users` (shares), `comments`, `category` | `expense_shares` |
| `GET /get_expense/{id}` | `expenses` | `users`, `comments`, `receipt` | `expense_shares` |
| `GET /get_friends` | `friends` | `users`, `balances` | `friend_balances` |
| `GET /get_friend/{id}` | `friends` | `users`, `balances`, `groups` | `friend_balances` |
| `GET /get_categories` | `categories` | `subcategories` | - |
| `GET /get_currencies` | `currencies` | - | - |
| `GET /get_notifications` | `notifications` | `users` (created_by) | - |

### Complete Normalization Example: `GET /get_expense/4142333569`

**Original API Response:**
```json
{
  "id": 4142333569,
  "group_id": 35084033,
  "description": "Iqos",
  "cost": "4.8",
  "currency_code": "EUR",
  "date": "2025-11-07T17:41:32Z",
  "created_at": "2025-11-07T17:42:10Z",
  "updated_at": "2025-11-07T17:42:10Z",
  "category": {
    "id": 26,
    "name": "Food and drink - Other"
  },
  "created_by": {
    "id": 8633344,
    "first_name": "Test",
    "last_name": "User",
    "email": "testuser@example.com",
    "picture": {
      "medium": "https://splitwise.s3.amazonaws.com/uploads/user/avatar/8633344/medium_95fe87dc.jpeg"
    }
  },
  "repayments": [
    {
      "from": 34726426,
      "to": 8633344,
      "amount": "4.8"
    }
  ],
  "users": [
    {
      "user": {
        "id": 8633344,
        "first_name": "Test",
        "last_name": "User"
      },
      "paid_share": "4.8",
      "owed_share": "0.0",
      "net_balance": "4.8"
    },
    {
      "user": {
        "id": 34726426,
        "first_name": "леся",
        "last_name": "бучма"
      },
      "paid_share": "0.0",
      "owed_share": "4.8",
      "net_balance": "-4.8"
    }
  ]
}
```

**Normalized into 9 separate documents across 5 collections:**

**1. `expenses` collection** (1 document):
```json
{
  "_id": "expense_4142333569",
  "id": 4142333569,
  "group_id": 35084033,
  "description": "Iqos",
  "cost": "4.8",
  "currency_code": "EUR",
  "date": "2025-11-07T17:41:32Z",
  "created_at": "2025-11-07T17:42:10Z",
  "updated_at": "2025-11-07T17:42:10Z",
  "category_id": 26,
  "created_by_user_id": 8633344,
  "share_user_ids": [8633344, 34726426],
  "repayment_user_ids": [34726426],
  "last_updated_date": "2025-11-08T00:26:02.186588+00:00"
}
```

**2. `categories` collection** (1 document):
```json
{
  "_id": "category_26",
  "id": 26,
  "name": "Food and drink - Other",
  "last_updated_date": "2025-11-08T00:26:02.186588+00:00"
}
```

**3. `users` collection** (2 documents):
```json
{
  "_id": "user_8633344",
  "id": 8633344,
  "first_name": "Pavlo",
  "last_name": "Akimenko",
  "email": "paulakimenko@gmail.com",
  "picture": {
    "medium": "https://splitwise.s3.amazonaws.com/uploads/user/avatar/8633344/medium_95fe87dc.jpeg"
  },
  "last_updated_date": "2025-11-08T00:26:02.186588+00:00"
}
```

```json
{
  "_id": "user_34726426",
  "id": 34726426,
  "first_name": "леся",
  "last_name": "бучма",
  "last_updated_date": "2025-11-08T00:26:02.186588+00:00"
}
```

**4. `expense_shares` collection** (2 documents):
```json
{
  "_id": "expense_4142333569_user_8633344",
  "expense_id": 4142333569,
  "user_id": 8633344,
  "paid_share": "4.8",
  "owed_share": "0.0",
  "net_balance": "4.8",
  "last_updated_date": "2025-11-08T00:26:02.186588+00:00"
}
```

```json
{
  "_id": "expense_4142333569_user_34726426",
  "expense_id": 4142333569,
  "user_id": 34726426,
  "paid_share": "0.0",
  "owed_share": "4.8",
  "net_balance": "-4.8",
  "last_updated_date": "2025-11-08T00:26:02.186588+00:00"
}
```

**5. `repayments` collection** (1 document):
```json
{
  "_id": "expense_4142333569_repayment_34726426_to_8633344",
  "expense_id": 4142333569,
  "from_user_id": 34726426,
  "to_user_id": 8633344,
  "amount": "4.8",
  "currency_code": null,
  "last_updated_date": "2025-11-08T00:26:02.186588+00:00"
}
```

**Key Benefits of This Normalization:**
- ✅ **No data duplication**: User info stored once, referenced by ID
- ✅ **Atomic updates**: Updating user profile updates all expenses automatically
- ✅ **Efficient queries**: Can query expenses by user_id without scanning all expenses
- ✅ **Flexible aggregation**: Can join expense + user + category data on-demand
- ✅ **Independent TTLs**: Categories cached 24h, expenses cached 5min

---

## Caching Strategy

### Write-Through Cache Pattern

**All API responses are cached immediately upon retrieval:**

```python
async def call_cached_method(method_name: str, **kwargs) -> dict:
    """
    1. Check cache validity (see invalidation logic)
    2. If valid cache exists → return from MongoDB
    3. If invalid/missing → call Splitwise API
    4. Normalize API response into entities
    5. Upsert entities to MongoDB with current timestamp
    6. Return normalized response
    """
    pass
```

### Upsert Operations (Update or Insert)

**MongoDB Pattern:**
```python
collection.update_one(
    filter={"_id": f"user_{user_id}"},  # Primary key
    update={
        "$set": {
            **entity_data,
            "last_updated_date": datetime.now(UTC).isoformat()
        }
    },
    upsert=True  # Create if doesn't exist, update if exists
)
```

**Key Benefits:**
- Avoids duplicate entities
- Preserves historical data (if needed via versioning)
- Atomic operation (no race conditions)

### Data Retrieval & Reconstruction

**When serving cached data, we need to reconstruct the original API response format:**

```python
async def get_cached_expense(expense_id: int) -> dict:
    """
    Retrieve expense from cache and reconstruct full API response.
    
    Steps:
    1. Fetch expense document from `expenses` collection
    2. Fetch related users from `users` collection (using share_user_ids)
    3. Fetch category from `categories` collection (using category_id)
    4. Fetch expense_shares from `expense_shares` collection (using expense_id)
    5. Fetch repayments from `repayments` collection (using expense_id)
    6. Reconstruct nested response matching Splitwise API format
    """
    
    # 1. Get expense document
    expense = db.expenses.find_one({"_id": f"expense_{expense_id}"})
    
    # 2. Get all related users (parallel queries)
    user_ids = expense["share_user_ids"]
    users = list(db.users.find({"id": {"$in": user_ids}}))
    users_by_id = {u["id"]: u for u in users}
    
    # 3. Get category
    category = db.categories.find_one({"_id": f"category_{expense['category_id']}"})
    
    # 4. Get expense shares
    shares = list(db.expense_shares.find({"expense_id": expense_id}))
    
    # 5. Get repayments
    repayments = list(db.repayments.find({"expense_id": expense_id}))
    
    # 6. Reconstruct response
    return {
        "id": expense["id"],
        "group_id": expense["group_id"],
        "description": expense["description"],
        "cost": expense["cost"],
        "currency_code": expense["currency_code"],
        "date": expense["date"],
        "created_at": expense["created_at"],
        "updated_at": expense["updated_at"],
        "category": {
            "id": category["id"],
            "name": category["name"]
        },
        "created_by": {
            "id": users_by_id[expense["created_by_user_id"]]["id"],
            "first_name": users_by_id[expense["created_by_user_id"]]["first_name"],
            "last_name": users_by_id[expense["created_by_user_id"]]["last_name"],
            "email": users_by_id[expense["created_by_user_id"]].get("email"),
            "picture": users_by_id[expense["created_by_user_id"]].get("picture")
        },
        "users": [
            {
                "user": {
                    "id": users_by_id[share["user_id"]]["id"],
                    "first_name": users_by_id[share["user_id"]]["first_name"],
                    "last_name": users_by_id[share["user_id"]]["last_name"]
                },
                "paid_share": share["paid_share"],
                "owed_share": share["owed_share"],
                "net_balance": share["net_balance"]
            }
            for share in shares
        ],
        "repayments": [
            {
                "from": rep["from_user_id"],
                "to": rep["to_user_id"],
                "amount": rep["amount"]
            }
            for rep in repayments
        ]
    }
```

**Performance Optimization:**
- Use MongoDB aggregation pipelines for complex joins
- Cache frequently accessed user/category lookups in memory
- Batch fetch related entities to minimize round-trips

---

## Cache Invalidation Logic

### Decision Tree for Cache Validity

```
                     ┌─────────────────────┐
                     │ MCP Tool Invoked    │
                     │ (e.g., list_groups) │
                     └──────────┬──────────┘
                                │
                                ▼
                  ┌─────────────────────────────┐
                  │ Determine entity type       │
                  │ (expenses, friends, users,  │
                  │  groups, categories, etc.)  │
                  └──────────┬──────────────────┘
                             │
                             ▼
                ┌────────────────────────────────┐
                │ Lookup TTL for entity type     │
                │ from ENTITY_TTL_MAP            │
                └──────┬──────────────┬──────────┘
                 TTL=0 │              │ TTL>0
    (notifications)    │              │
                       ▼              ▼
              ┌──────────────┐  ┌──────────────────────────┐
              │ ALWAYS       │  │ Check entity timestamp   │
              │ FETCH        │  │ last_updated_date        │
              │ FROM API     │  └──────────┬───────────────┘
              └──────────────┘             │
                                           ▼
                              ┌────────────────────────────┐
                              │ Age < Entity TTL?          │
                              │ (5min, 1hr, or 24hr)       │
                              └──────┬─────────────┬───────┘
                                YES  │             │ NO
                                     ▼             ▼
                               ┌─────────┐   ┌──────────┐
                               │ USE     │   │ FETCH    │
                               │ CACHE   │   │ FROM API │
                               └─────────┘   └──────────┘
```

### Implementation: Invalidation Logic

#### 1. User-Specific Data (Notification-Based) [DEPRECATED]

**Note:** This notification-based approach is deprecated in favor of entity-specific TTLs. 
It's kept here for reference and potential future hybrid approaches.

**Previously Applied to:**
- `GET /get_current_user`
- `GET /get_groups` (user's groups)
- `GET /get_expenses` (user's expenses)
- `GET /get_friends` (user's friends)

**Old Algorithm (Reference Only):**
```python
async def is_user_cache_valid(entity_timestamp: str) -> bool:
    """
    Check if user-specific cached entity is still valid.
    
    Returns True if:
    - Last notification timestamp ≤ entity last_updated_date
    - OR Splitwise API is unavailable (graceful degradation)
    """
    try:
        # Fetch latest notification from cache (or API if cache miss)
        notifications = await get_cached_notifications(limit=1)
        
        if not notifications:
            return True  # No notifications = cache is valid
        
        last_notification_time = notifications[0]["created_at"]
        entity_time = datetime.fromisoformat(entity_timestamp)
        
        # Cache is valid if entity was updated AFTER last notification
        return entity_time >= datetime.fromisoformat(last_notification_time)
        
    except SplitwiseAPIUnavailable:
        # Graceful degradation: use stale cache
        logger.warning("Splitwise API unavailable, using cached data")
        return True
```

**Rationale:**
- Notifications represent changes to user's data (new expense, group update, etc.)
- If no new notifications since cache was updated → cache is fresh
- Notification endpoint is lightweight (~50-100ms) vs full data fetch (~300-800ms)

#### 2. Entity-Specific Time-Based TTL

**Entity-Specific Cache Timeouts:**

| Entity Type | Default TTL | Environment Variable | Rationale |
|-------------|-------------|---------------------|-----------|
| **Expenses** | 5 minutes | `CACHE_TTL_EXPENSES_MINUTES` | Actively managed, frequent updates during group activities |
| **Friends** | 5 minutes | `CACHE_TTL_FRIENDS_MINUTES` | Balances change with new expenses, need fresh data |
| **Users** | 1 hour | `CACHE_TTL_USERS_MINUTES` | Profile info (name, email, picture) changes rarely |
| **Groups** | 1 hour | `CACHE_TTL_GROUPS_MINUTES` | Membership and settings change infrequently |
| **Categories** | 24 hours | `CACHE_TTL_CATEGORIES_MINUTES` | Static reference data, updated monthly at most |
| **Currencies** | 24 hours | `CACHE_TTL_CURRENCIES_MINUTES` | Static reference data, exchange rates updated daily |
| **Notifications** | No cache | N/A | Always fetch fresh for cache invalidation logic |

**Algorithm:**
```python
# Entity-specific TTL configuration (in minutes)
ENTITY_TTL_MAP = {
    "expenses": int(os.getenv("CACHE_TTL_EXPENSES_MINUTES", "5")),
    "friends": int(os.getenv("CACHE_TTL_FRIENDS_MINUTES", "5")),
    "users": int(os.getenv("CACHE_TTL_USERS_MINUTES", "60")),
    "groups": int(os.getenv("CACHE_TTL_GROUPS_MINUTES", "60")),
    "categories": int(os.getenv("CACHE_TTL_CATEGORIES_MINUTES", "1440")),  # 24 hours
    "currencies": int(os.getenv("CACHE_TTL_CURRENCIES_MINUTES", "1440")),  # 24 hours
    "notifications": 0,  # Never cache - always fetch fresh
}

async def is_entity_cache_valid(entity_type: str, entity_timestamp: str) -> bool:
    """
    Check if entity data is still valid based on entity-specific TTL.
    
    Args:
        entity_type: Type of entity (e.g., "expenses", "friends", "users")
        entity_timestamp: ISO 8601 timestamp of last cache update
    
    Returns:
        True if cache is still valid, False if expired
    """
    ttl_minutes = ENTITY_TTL_MAP.get(entity_type, 5)  # Default 5 min if unknown
    
    # Notifications are never cached
    if ttl_minutes == 0:
        return False
    
    try:
        entity_time = datetime.fromisoformat(entity_timestamp)
        now = datetime.now(timezone.utc)
        age_minutes = (now - entity_time).total_seconds() / 60
        return age_minutes < ttl_minutes
        
    except SplitwiseAPIUnavailable:
        # Graceful degradation: use stale cache
        logger.warning(f"Splitwise API unavailable, using cached {entity_type} data")
        return True
```

**Usage Examples:**
```python
# Check if expense cache is valid (5 min TTL)
if await is_entity_cache_valid("expenses", expense["last_updated_date"]):
    return expense  # Use cached data

# Check if group cache is valid (1 hour TTL)
if await is_entity_cache_valid("groups", group["last_updated_date"]):
    return group  # Use cached data

# Notifications are never cached
if await is_entity_cache_valid("notifications", notification["last_updated_date"]):
    # Always returns False, triggers fresh fetch
    pass
```

**Note:** The old "Static Reference Data" section has been removed in favor of the unified entity-specific TTL approach above.

---

## MongoDB Collections Schema

### Core Collections

#### 1. `users` Collection

```python
{
    "_id": "user_67890",              # Compound key: "user_{user_id}"
    "id": 67890,                       # Splitwise user ID
    "first_name": "Alice",
    "last_name": "Smith",
    "email": "alice@example.com",
    "registration_status": "confirmed", # confirmed | dummy | invited
    "picture": {
        "small": "https://...",
        "medium": "https://...",
        "large": "https://..."
    },
    "custom_picture": false,
    "last_updated_date": "2025-11-03T14:32:28Z"  # ISO 8601 timestamp
}
```

**Indexes:**
- Primary: `_id` (automatic)
- Secondary: `id` (unique, for lookups)
- Secondary: `email` (for email-based lookups)
- TTL index: `last_updated_date` (for auto-cleanup if needed)

#### 2. `current_user` Collection

```python
{
    "_id": "current_user",             # Singleton document
    "id": 12345,
    "first_name": "CurrentUser",
    "last_name": "Name",
    "email": "current@example.com",
    "notifications_read": "2025-11-03T12:00:00Z",
    "notifications_count": 5,
    "default_currency": "USD",
    "locale": "en",
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

#### 3. `groups` Collection

```python
{
    "_id": "group_12345",
    "id": 12345,
    "name": "House Expenses",
    "group_type": "home",              # home | trip | couple | other
    "updated_at": "2025-11-03T10:15:30Z",  # From Splitwise API
    "simplify_by_default": true,
    "member_ids": [67890, 54321, 99999],  # Denormalized for quick lookups
    "original_debts": [...],
    "simplified_debts": [...],
    "avatar": {...},
    "cover_photo": {...},
    "invite_link": "https://...",
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `id` (unique)
- Secondary: `name` (for name-based lookups)
- Secondary: `member_ids` (multi-key index for "user in group" queries)

#### 4. `expenses` Collection

**Each expense as a separate document with ID references only (no embedded objects):**

```python
{
    "_id": "expense_51023",
    "id": 51023,
    "group_id": 12345,                 # Reference to groups collection (null if not in group)
    "friendship_id": null,             # Reference to friends collection (for friend-to-friend expenses)
    "cost": "125.50",
    "currency_code": "USD",
    "description": "Grocery shopping",
    "details": "Whole Foods weekly run",
    "date": "2025-11-02T18:30:00Z",
    "category_id": 15,                 # Reference to categories collection
    "payment": false,
    "repeats": false,
    "repeat_interval": "never",
    "email_reminder": false,
    "email_reminder_in_advance": -1,
    "next_repeat": null,
    "created_at": "2025-11-02T19:00:00Z",
    "updated_at": "2025-11-02T19:00:00Z",
    "deleted_at": null,
    "created_by_user_id": 67890,       # Reference to users collection
    "updated_by_user_id": null,        # Reference to users collection
    "deleted_by_user_id": null,        # Reference to users collection
    "comments_count": 2,
    "transaction_method": "none",
    "transaction_confirmed": false,
    "transaction_id": null,
    "expense_bundle_id": null,
    "receipt_large_url": "https://...",
    "receipt_original_url": "https://...",
    "share_user_ids": [67890, 54321],  # Denormalized for fast lookups
    "repayment_user_ids": [54321],     # Users who owe money (denormalized)
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `id` (unique)
- Secondary: `group_id` (for group expense queries)
- Secondary: `friendship_id` (for friend expense queries)
- Secondary: `date` (descending, for date-range queries)
- Secondary: `category_id` (for category-based queries)
- Secondary: `created_by_user_id` (for user's created expenses)
- Secondary: `share_user_ids` (multi-key, for "user's expenses" queries)
- Compound: `(group_id, date)` (optimized for monthly reports)
- Compound: `(share_user_ids, date)` (optimized for user expense history)

#### 5. `expense_shares` Collection (Junction Table)

**Each user's share in an expense as separate document:**

```python
{
    "_id": "expense_51023_user_67890",
    "expense_id": 51023,               # Reference to expenses collection
    "user_id": 67890,                  # Reference to users collection
    "paid_share": "125.50",
    "owed_share": "62.75",
    "net_balance": "62.75",
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

```python
{
    "_id": "expense_51023_user_54321",
    "expense_id": 51023,               # Reference to expenses collection
    "user_id": 54321,                  # Reference to users collection
    "paid_share": "0.00",
    "owed_share": "62.75",
    "net_balance": "-62.75",
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `expense_id` (for all shares of an expense)
- Secondary: `user_id` (for all shares of a user)
- Compound: `(user_id, expense_id)` (unique constraint)

#### 6. `repayments` Collection

**Each repayment record as separate document (part of expense):**

```python
{
    "_id": "expense_51023_repayment_54321_to_67890",
    "expense_id": 51023,               # Reference to expenses collection
    "from_user_id": 54321,             # Reference to users collection (who owes)
    "to_user_id": 67890,               # Reference to users collection (who is owed)
    "amount": "62.75",
    "currency_code": "USD",            # Can be null (inherits from expense)
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `expense_id` (for all repayments of an expense)
- Secondary: `from_user_id` (for debts owed by user)
- Secondary: `to_user_id` (for debts owed to user)
- Compound: `(from_user_id, to_user_id)` (for friend balances)

#### 7. `friends` Collection

```python
{
    "_id": "friend_54321",
    "id": 54321,                       # Friend's user ID (references users collection)
    "first_name": "Bob",
    "last_name": "Jones",
    "email": "bob@example.com",
    "picture": {"medium": "https://..."},
    "updated_at": "2025-11-01T08:00:00Z",
    "group_ids": [12345, 67890],       # References to groups collection (shared groups)
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `id` (unique)
- Secondary: `email`
- Secondary: `group_ids` (multi-key for "friends in group" queries)

#### 8. `friend_balances` Collection

**Each currency balance between current user and friend as separate document:**

```python
{
    "_id": "friend_54321_balance_USD",
    "friend_id": 54321,                # Reference to friends/users collection
    "currency_code": "USD",
    "amount": "45.50",                 # Positive = friend owes you, Negative = you owe friend
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `friend_id`
- Compound: `(friend_id, currency_code)` (unique constraint)

#### 9. `notifications` Collection

```python
{
    "_id": "notification_32514315",
    "id": 32514315,
    "type": 0,                         # 0=expense added, 1=expense updated, etc.
    "created_at": "2025-11-03T13:45:00Z",
    "created_by_user_id": 67890,       # Reference to users collection
    "source": {
        "type": "Expense",
        "id": 51023,
        "url": null
    },
    "image_url": "https://...",
    "content": "<strong>Alice</strong> added \"Grocery shopping\"",
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `created_at` (descending, for latest-first queries)
- Secondary: `type` (for filtering by notification type)

#### 10. `categories` Collection

```python
{
    "_id": "category_15",
    "id": 15,
    "name": "Groceries",
    "parent_id": 1,                    # Reference to parent category (null if top-level)
    "icon": "https://...",
    "icon_types": {"slim": {"small": "https://...", "large": "https://..."}},
    "subcategory_ids": [45, 46, 47],   # References to child categories
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `id` (unique)
- Secondary: `parent_id` (for subcategory queries)
- Secondary: `name` (for name-based lookups)

#### 11. `currencies` Collection

```python
{
    "_id": "currency_USD",
    "currency_code": "USD",
    "unit": "$",
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `currency_code` (unique)

#### 12. `comments` Collection

**Each comment as separate document:**

```python
{
    "_id": "comment_79800950",
    "id": 79800950,
    "expense_id": 51023,               # Reference to expenses collection
    "content": "Forgot to include milk!",
    "comment_type": "User",            # User | System
    "relation_type": "ExpenseComment", # Type of relation
    "relation_id": 51023,              # Same as expense_id
    "created_at": "2025-11-03T09:00:00Z",
    "deleted_at": null,
    "user_id": 67890,                  # Reference to users collection (who posted)
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

**Indexes:**
- Primary: `_id`
- Secondary: `id` (unique)
- Secondary: `expense_id` (for all comments on an expense)
- Secondary: `user_id` (for user's comments)
- Secondary: `created_at` (for chronological sorting)
    "user_id": 67890,
    "last_updated_date": "2025-11-03T14:32:28Z"
}
```

---

## API Method Coverage

### Current Implementation Status (app/splitwise_client.py)

| Method Name (MCP) | SDK Method | Endpoint | Caching Priority | Status |
|-------------------|------------|----------|------------------|--------|
| `get_current_user` | `getCurrentUser` | `GET /get_current_user` | HIGH | ✅ Implemented |
| `list_groups` | `getGroups` | `GET /get_groups` | HIGH | ✅ Implemented |
| `get_group` | `getGroup` | `GET /get_group/{id}` | HIGH | ✅ Implemented |
| `list_expenses` | `getExpenses` | `GET /get_expenses` | HIGH | ✅ Implemented |
| `get_expense` | `getExpense` | `GET /get_expense/{id}` | MEDIUM | ✅ Implemented |
| `list_friends` | `getFriends` | `GET /get_friends` | MEDIUM | ✅ Implemented |
| `get_friend` | `getFriend` | `GET /get_friend/{id}` | MEDIUM | ✅ Implemented |
| `list_categories` | `getCategories` | `GET /get_categories` | LOW (static) | ✅ Implemented |
| `list_currencies` | `getCurrencies` | `GET /get_currencies` | LOW (static) | ✅ Implemented |
| `get_exchange_rates` | `getCurrencyConversionRate` | N/A (SDK only) | LOW | ✅ Implemented |
| `list_notifications` | `getNotifications` | `GET /get_notifications` | HIGH (invalidation) | ✅ Implemented |
| `create_expense` | `createExpense` | `POST /create_expense` | N/A (write) | ✅ Implemented |
| `update_expense` | `updateExpense` | `POST /update_expense/{id}` | N/A (write) | ✅ Implemented |
| `delete_expense` | `deleteExpense` | `POST /delete_expense/{id}` | N/A (write) | ✅ Implemented |
| `undelete_expense` | `undeleteExpense` | `POST /undelete_expense/{id}` | N/A (write) | ✅ Implemented |
| `create_group` | `createGroup` | `POST /create_group` | N/A (write) | ✅ Implemented |
| `delete_group` | `deleteGroup` | `POST /delete_group/{id}` | N/A (write) | ✅ Implemented |
| `undelete_group` | `undeleteGroup` | `POST /undelete_group/{id}` | N/A (write) | ✅ Implemented |
| `add_user_to_group` | `addUserToGroup` | `POST /add_user_to_group` | N/A (write) | ✅ Implemented |
| `remove_user_from_group` | `removeUserFromGroup` | `POST /remove_user_from_group` | N/A (write) | ✅ Implemented |
| `create_friend` | `createFriend` | `POST /create_friend` | N/A (write) | ✅ Implemented |
| `create_friends` | `createFriends` | `POST /create_friends` | N/A (write) | ✅ Implemented |
| `delete_friend` | `deleteFriend` | `POST /delete_friend/{id}` | N/A (write) | ✅ Implemented |
| `update_user` | `updateUser` | `POST /update_user/{id}` | N/A (write) | ✅ Implemented |
| `create_comment` | `createComment` | `POST /create_comment` | N/A (write) | ✅ Implemented |
| `delete_comment` | `deleteComment` | `POST /delete_comment/{id}` | N/A (write) | ✅ Implemented |

### Missing Methods (From OpenAPI Spec)

| Endpoint | HTTP Method | Description | Priority | Notes |
|----------|-------------|-------------|----------|-------|
| `GET /get_user/{id}` | GET | Get another user's details | MEDIUM | Not in current METHOD_MAP |
| `GET /get_comments` | GET | Get expense comments | LOW | Comments currently fetched as part of expense |

**Recommendation**: Add these missing methods for completeness:

```python
# In app/splitwise_client.py METHOD_MAP
METHOD_MAP = {
    # ... existing mappings ...
    "get_user": "getUser",           # NEW
    "get_comments": "getComments",   # NEW (if SDK supports)
}
```

---

## Configuration

### Environment Variables

```bash
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
DB_NAME=splitwise

# Entity-Specific Cache TTLs (in minutes)
CACHE_TTL_EXPENSES_MINUTES=5         # Expenses cache timeout (default: 5 min)
CACHE_TTL_FRIENDS_MINUTES=5          # Friends cache timeout (default: 5 min)
CACHE_TTL_USERS_MINUTES=60           # Users cache timeout (default: 1 hour)
CACHE_TTL_GROUPS_MINUTES=60          # Groups cache timeout (default: 1 hour)
CACHE_TTL_CATEGORIES_MINUTES=1440    # Categories cache timeout (default: 24 hours)
CACHE_TTL_CURRENCIES_MINUTES=1440    # Currencies cache timeout (default: 24 hours)
# Note: Notifications are never cached (always fetch fresh)

# General Caching Configuration
CACHE_ENABLED=true                   # Master switch to disable caching
CACHE_WRITE_THROUGH=true             # Always write to cache (vs. write-back)

# Splitwise API
SPLITWISE_API_KEY=your_api_key_here

# MCP Server
MCP_TRANSPORT=streamable-http        # stdio | streamable-http
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

### Configuration File (Optional)

```yaml
# config/cache.yaml
cache:
  enabled: true
  
  # Entity-specific TTLs (in minutes)
  entity_ttls:
    expenses: 5
    friends: 5
    users: 60              # 1 hour
    groups: 60             # 1 hour
    categories: 1440       # 24 hours
    currencies: 1440       # 24 hours
    notifications: 0       # Never cache
  
  # MongoDB TTL indexes (auto-cleanup old data)
  collections:
    users:
      ttl_hours: 168          # 7 days (auto-cleanup)
    expenses:
      ttl_hours: 8760         # 365 days (1 year)
    notifications:
      ttl_hours: 168          # 7 days
    friends:
      ttl_hours: 720          # 30 days
    groups:
      ttl_hours: 8760         # 365 days
  
  performance:
    batch_size: 100           # Entities per batch for normalization
    max_cache_size_mb: 500    # Warning threshold
```

### TTL Configuration Best Practices

**Development/Testing:**
```bash
# Shorter TTLs for faster testing of cache invalidation
CACHE_TTL_EXPENSES_MINUTES=1
CACHE_TTL_FRIENDS_MINUTES=1
CACHE_TTL_USERS_MINUTES=5
CACHE_TTL_GROUPS_MINUTES=5
```

**Production:**
```bash
# Balanced TTLs for performance and freshness
CACHE_TTL_EXPENSES_MINUTES=5
CACHE_TTL_FRIENDS_MINUTES=5
CACHE_TTL_USERS_MINUTES=60
CACHE_TTL_GROUPS_MINUTES=60
CACHE_TTL_CATEGORIES_MINUTES=1440
CACHE_TTL_CURRENCIES_MINUTES=1440
```

**High-Traffic/Low-Latency:**
```bash
# Longer TTLs to reduce API calls (accept some staleness)
CACHE_TTL_EXPENSES_MINUTES=15
CACHE_TTL_FRIENDS_MINUTES=15
CACHE_TTL_USERS_MINUTES=120
CACHE_TTL_GROUPS_MINUTES=120
```

---

## Data Flow Diagrams

### Scenario 1: Cache Hit (Groups with 1-hour TTL)

```
User: "List my groups"
     │
     ▼
┌─────────────────────────┐
│ MCP Tool: list_groups   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ CachedSplitwiseClient.list_groups()     │
│ 1. Determine entity type: "groups"      │
│ 2. Lookup TTL: 60 minutes (1 hour)      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ MongoDB Query:                          │
│ db.groups.find({                        │
│   "member_ids": 12345  # current user   │
│ })                                      │
│ → Returns: [group1, group2, group3]     │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Check cache validity:                   │
│ - Groups last_updated_date:             │
│   "2025-11-03T14:30:00Z"                │
│ - Current time: "2025-11-03T14:45:00Z"  │
│ - Age: 15 minutes                       │
│ - TTL: 60 minutes                       │
│ - Cache valid? YES (15 < 60)            │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│ Return cached groups    │
│ Latency: ~50ms          │
└─────────────────────────┘
```

### Scenario 2: Cache Miss (Expenses TTL Expired)

```
User: "List my expenses"
     │
     ▼
┌─────────────────────────┐
│ MCP Tool: list_expenses │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ CachedSplitwiseClient.list_expenses()   │
│ 1. Determine entity type: "expenses"    │
│ 2. Lookup TTL: 5 minutes                │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ MongoDB Query:                          │
│ db.expenses.find({                      │
│   "share_user_ids": 12345               │
│ })                                      │
│ → Returns: [expense1, expense2, ...]    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Check cache validity:                   │
│ - Expenses last_updated_date:           │
│   "2025-11-03T14:30:00Z"                │
│ - Current time: "2025-11-03T14:38:00Z"  │
│ - Age: 8 minutes                        │
│ - TTL: 5 minutes                        │
│ - Cache valid? NO (8 > 5)               │
│   Cache expired, need fresh data!       │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Fetch from Splitwise API:               │
│ GET /get_expenses                       │
│ → Returns: 15 expenses with shares      │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Normalize & Cache:                      │
│ 1. Extract 15 expense entities          │
│ 2. Extract 30 user entities (shares)    │
│ 3. Extract 45 share records             │
│ 4. Extract 8 comment entities           │
│ 5. Upsert all to MongoDB collections    │
│ 6. Set last_updated_date: NOW           │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│ Return fresh expenses   │
│ Latency: ~500ms         │
└─────────────────────────┘
```

### Scenario 3: Graceful Degradation (API Unavailable)

```
User: "Show friend details"
     │
     ▼
┌─────────────────────────┐
│ MCP Tool: get_friend    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ CachedSplitwiseClient.get_friend()      │
│ 1. Check TTL-based cache validity       │
│ 2. Friend last_updated: 14:00:00        │
│ 3. Current time: 14:02:00               │
│ 4. Age: 2 minutes < 5 min TTL → VALID   │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ BUT: User manually refreshes            │
│ Cache invalidated by force-refresh flag │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Attempt API call:                       │
│ GET /get_friend/54321                   │
│ → ERROR: ConnectionTimeout              │
│ → Splitwise API is DOWN                 │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Graceful Degradation:                   │
│ 1. Log warning: "API unavailable"       │
│ 2. Return stale cache (age: 2 min)      │
│ 3. Add metadata: {                      │
│      "from_cache": true,                │
│      "cache_age_minutes": 2,            │
│      "api_unavailable": true            │
│    }                                    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────┐
│ Return stale data       │
│ Service remains UP      │
└─────────────────────────┘
```

---

## Edge Cases & Error Handling

### 1. Splitwise API Unavailable

**Scenario**: Splitwise API returns 500/503 or network timeout

**Behavior**:
- ✅ **Use stale cache** as source of truth
- ✅ Log warning with error details
- ✅ Add metadata to response: `{"from_cache": true, "api_unavailable": true}`
- ✅ Continue serving requests (no user-facing errors)

**Implementation**:
```python
try:
    api_response = await splitwise_sdk.get_expenses()
except (requests.Timeout, requests.ConnectionError, HTTPError) as e:
    logger.warning(f"Splitwise API unavailable: {e}, using cached data")
    cached_data = fetch_from_cache("expenses")
    if cached_data:
        return {**cached_data, "_meta": {"from_cache": True, "api_unavailable": True}}
    raise ServiceUnavailableError("No cached data available")
```

### 2. Cache Corruption / Invalid Schema

**Scenario**: MongoDB document has unexpected schema (e.g., missing required fields)

**Behavior**:
- ✅ Log error with document ID
- ✅ Delete corrupted document
- ✅ Fetch fresh data from API
- ✅ Cache corrected data

**Implementation**:
```python
try:
    validate_schema(cached_expense, ExpenseSchema)
except ValidationError as e:
    logger.error(f"Corrupted cache for expense {expense_id}: {e}")
    db.expenses.delete_one({"_id": f"expense_{expense_id}"})
    return await fetch_from_api_and_cache(expense_id)
```

### 3. Notification Endpoint Failure

**Scenario**: `/get_notifications` endpoint fails or times out

**Behavior**:
- ✅ **Fallback to time-based TTL** (use shared data timeout: 5 min)
- ✅ Log warning
- ✅ Continue with degraded cache freshness guarantee

**Implementation**:
```python
try:
    last_notification = await get_last_notification()
except APIError:
    logger.warning("Notification endpoint failed, using TTL fallback")
    return is_ttl_valid(entity_timestamp, timeout_minutes=5)
```

### 4. Write Operation Invalidation

**Scenario**: User creates/updates/deletes an expense via MCP tool

**Behavior**:
- ✅ **Immediately invalidate affected cache entries**:
  - Updated expense entity
  - Parent group (if expense in group)
  - All user shares
  - Current user's expense list
- ✅ Optionally re-fetch and cache updated data
- ✅ Update `last_updated_date` on all affected entities

**Implementation**:
```python
async def create_expense(**kwargs):
    # Call Splitwise API to create expense
    new_expense = await splitwise_sdk.createExpense(**kwargs)
    
    # Invalidate cache
    group_id = new_expense.group_id
    user_ids = [share.user_id for share in new_expense.users]
    
    # Delete cached entries (will be re-cached on next read)
    db.expenses.delete_many({"group_id": group_id})
    db.groups.delete_one({"_id": f"group_{group_id}"})
    
    # Or update cache immediately (write-through)
    await normalize_and_cache_expense(new_expense)
    
    return convert_to_dict(new_expense)
```

### 5. Large Response Pagination

**Scenario**: API returns 500+ expenses (exceeds memory limits)

**Behavior**:
- ✅ Process in batches (100 entities per batch)
- ✅ Stream to MongoDB (avoid loading all in memory)
- ✅ Use cursor-based pagination if API supports it

**Implementation**:
```python
async def cache_large_dataset(api_method, **kwargs):
    offset = 0
    batch_size = 100
    
    while True:
        batch = await api_method(limit=batch_size, offset=offset, **kwargs)
        if not batch:
            break
        
        # Normalize and cache batch
        await normalize_and_cache_batch(batch)
        offset += batch_size
        
        logger.info(f"Cached {offset} entities so far")
```

### 6. Concurrent Requests (Race Conditions)

**Scenario**: Two MCP tools request same data simultaneously, both trigger cache miss

**Behavior**:
- ✅ Use **request coalescing** (first request fetches, others wait)
- ✅ Prevent duplicate API calls
- ✅ Use asyncio locks per entity

**Implementation**:
```python
# Global lock manager
entity_locks = {}

async def fetch_with_coalescing(entity_type: str, entity_id: str):
    lock_key = f"{entity_type}_{entity_id}"
    
    if lock_key not in entity_locks:
        entity_locks[lock_key] = asyncio.Lock()
    
    async with entity_locks[lock_key]:
        # Check cache again (might have been populated by concurrent request)
        cached = fetch_from_cache(entity_type, entity_id)
        if cached:
            return cached
        
        # Only one request actually hits API
        return await fetch_from_api_and_cache(entity_type, entity_id)
```

### 7. Timestamp Timezone Handling

**Scenario**: Timestamps from Splitwise API vs. MongoDB have different timezones

**Behavior**:
- ✅ **Always use UTC** for all timestamps
- ✅ Convert Splitwise timestamps to UTC on ingestion
- ✅ Store in ISO 8601 format: `2025-11-03T14:32:28Z`

**Implementation**:
```python
from datetime import datetime, timezone

def normalize_timestamp(ts: str) -> str:
    """Convert any timestamp to UTC ISO 8601 format."""
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).isoformat()

# On cache write
entity["last_updated_date"] = datetime.now(timezone.utc).isoformat()
```

---

## Implementation Plan

### Phase 1: Foundation (Week 1)

**Goals**: Set up core caching infrastructure without changing existing behavior

**Tasks**:
1. ✅ Create `CachedSplitwiseClient` class in new file `app/cached_splitwise_client.py`
2. ✅ Implement MongoDB collection schemas (create indexes)
3. ✅ Add configuration management (`CACHE_TIMEOUT_MINUTES`, etc.)
4. ✅ Implement entity normalization functions:
   - `normalize_user(user_dict) -> User`
   - `normalize_group(group_dict) -> (Group, List[User], List[GroupMember])`
   - `normalize_expense(expense_dict) -> (Expense, List[User], List[Share])`
5. ✅ Implement upsert operations with timestamps
6. ✅ Add logging for cache operations (hit/miss/write)

**Deliverables**:
- Working cache write operations (no reads yet)
- All API responses persisted to MongoDB
- Unit tests for normalization functions

### Phase 2: Read Path (Week 2)

**Goals**: Implement cache reads with invalidation logic

**Tasks**:
1. ✅ Implement `is_user_cache_valid()` (notification-based)
2. ✅ Implement `is_shared_cache_valid()` (TTL-based)
3. ✅ Implement `is_static_cache_valid()` (long TTL)
4. ✅ Add cache lookup functions:
   - `get_cached_user(user_id)`
   - `get_cached_group(group_id)`
   - `get_cached_expenses(filters)`
5. ✅ Integrate cache reads into `CachedSplitwiseClient`
6. ✅ Add cache hit/miss metrics (Prometheus-compatible)

**Deliverables**:
- Full cache read/write cycle
- Cache invalidation working
- Integration tests with MongoDB

### Phase 3: Integration & Migration (Week 3)

**Goals**: Replace `SplitwiseClient` with `CachedSplitwiseClient` in MCP server

**Tasks**:
1. ✅ Update `app/main.py` to use `CachedSplitwiseClient`
2. ✅ Add feature flag: `CACHE_ENABLED` (default: `false` for safety)
3. ✅ Implement graceful degradation for API failures
4. ✅ Add request coalescing for concurrent requests
5. ✅ Update all 22 MCP tools to use cached client
6. ✅ Add cache warmup on server startup (optional)

**Deliverables**:
- Cached client in production (behind feature flag)
- Zero breaking changes to MCP tools
- End-to-end tests passing

### Phase 4: Optimization & Monitoring (Week 4)

**Goals**: Performance tuning and observability

**Tasks**:
1. ✅ Add cache metrics endpoint (`/metrics`)
   - Cache hit rate
   - Average cache age
   - API call reduction %
2. ✅ Optimize MongoDB queries (add compound indexes)
3. ✅ Implement batch operations for normalization
4. ✅ Add cache preloading for common queries
5. ✅ Performance benchmarking (before/after comparison)
6. ✅ Documentation updates

**Deliverables**:
- Metrics dashboard (Grafana-compatible)
- Performance report (cache hit rate, latency improvements)
- Updated developer documentation

---

## Testing Strategy

### Unit Tests

**Location**: `tests/test_cached_splitwise_client.py`

**Coverage**:
```python
class TestEntityNormalization:
    def test_normalize_user_complete_profile()
    def test_normalize_user_missing_optional_fields()
    def test_normalize_group_with_members()
    def test_normalize_expense_with_shares()
    def test_normalize_nested_entities()
    def test_timestamp_addition()

class TestCacheInvalidation:
    def test_user_cache_valid_no_new_notifications()
    def test_user_cache_invalid_new_notification()
    def test_shared_cache_valid_within_ttl()
    def test_shared_cache_invalid_expired_ttl()
    def test_static_cache_long_ttl()
    def test_api_unavailable_uses_stale_cache()

class TestUpsertOperations:
    def test_upsert_creates_new_entity()
    def test_upsert_updates_existing_entity()
    def test_upsert_preserves_timestamps()
    def test_concurrent_upserts_no_duplicates()
```

### Integration Tests

**Location**: `tests/integration/test_cached_mcp_tools.py`

**Coverage**:
```python
class TestCachedMCPTools:
    @pytest.mark.integration
    async def test_list_groups_cache_hit():
        """First call fetches from API, second uses cache"""
        
    @pytest.mark.integration
    async def test_create_expense_invalidates_cache():
        """Write operation invalidates related cache entries"""
    
    @pytest.mark.integration
    async def test_notification_based_invalidation():
        """New notification triggers cache refresh"""
    
    @pytest.mark.integration
    async def test_api_failure_graceful_degradation():
        """Service continues with stale cache when API down"""
```

### Performance Tests

**Location**: `tests/performance/test_cache_latency.py`

**Metrics**:
- Average latency: API vs. cache
- Cache hit rate over 1000 requests
- Memory usage with large datasets (10,000+ expenses)
- Concurrent request handling (100 simultaneous calls)

**Benchmark Goals**:
| Metric | Before Caching | After Caching | Target |
|--------|----------------|---------------|--------|
| `list_groups` latency | 500ms | 50ms | <100ms |
| `get_expense` latency | 300ms | 30ms | <50ms |
| Cache hit rate | N/A | 70% | >65% |
| API calls/session | 15 | 4 | <5 |

---

## Performance Considerations

### Cache Size Estimation

**Assumptions** (typical user):
- 10 groups
- 50 friends
- 500 expenses per year
- 1000 notifications (retained for 7 days)

**Storage per Entity**:
- User: ~500 bytes
- Group: ~2 KB
- Expense: ~1.5 KB
- Notification: ~800 bytes

**Total per User**:
```
Users: 50 × 500B = 25 KB
Groups: 10 × 2KB = 20 KB
Expenses: 500 × 1.5KB = 750 KB
Notifications: 1000 × 800B = 800 KB
─────────────────────────────────
Total: ~1.6 MB per user
```

**Scaling**:
- 1,000 users = 1.6 GB
- 10,000 users = 16 GB
- 100,000 users = 160 GB

### Memory Management

**Strategies**:
1. **TTL Indexes**: Auto-delete old documents
   ```python
   db.notifications.create_index(
       "last_updated_date",
       expireAfterSeconds=604800  # 7 days
   )
   ```

2. **Projection**: Only fetch needed fields
   ```python
   db.expenses.find(
       {"group_id": 12345},
       {"id": 1, "cost": 1, "description": 1}  # Only these fields
   )
   ```

3. **Pagination**: Limit results per query
   ```python
   db.expenses.find().limit(100).skip(offset)
   ```

### Query Optimization

**Indexes Required**:
```python
# High-priority indexes
db.groups.create_index("member_ids")  # Multi-key for "user in group"
db.expenses.create_index([("group_id", 1), ("date", -1)])  # Compound
db.expenses.create_index("share_user_ids")  # Multi-key
db.notifications.create_index([("created_at", -1)])  # Latest-first

# Medium-priority indexes
db.users.create_index("email")
db.friends.create_index("group_ids")
db.comments.create_index("expense_id")
```

**Query Patterns**:
```python
# GOOD: Uses index
db.expenses.find({"group_id": 12345}).sort([("date", -1)])

# BAD: Full collection scan
db.expenses.find({"description": {"$regex": "grocery"}})

# BETTER: Add text index for description searches
db.expenses.create_index({"description": "text"})
```

---

## Future Enhancements

### Phase 5: Advanced Features (Post-MVP)

1. **Cache Warmup on Startup**
   - Pre-fetch common data (current user, groups, recent expenses)
   - Reduces cold-start latency for first requests

2. **Predictive Prefetching**
   - If user views group → prefetch group's expenses
   - If user creates expense → prefetch updated group balances
   - ML-based prediction of next likely query

3. **Cache Compression**
   - Store large text fields (descriptions, comments) compressed
   - Decompress on read
   - Reduces storage by 40-60%

4. **Multi-Tier Caching**
   - L1: In-memory cache (Redis) for ultra-fast reads (<10ms)
   - L2: MongoDB for persistent storage
   - Write-through to both tiers

5. **Cache Analytics Dashboard**
   - Real-time cache hit/miss rates
   - Most frequently accessed entities
   - Cache efficiency by endpoint
   - Anomaly detection (sudden cache miss spike)

6. **Incremental Updates**
   - Instead of full entity fetch, use Splitwise `updated_after` parameter
   - Only fetch entities modified since last cache update
   - Reduces API bandwidth by 80%+

7. **Cache Eviction Policies**
   - LRU (Least Recently Used) eviction when cache size exceeds limit
   - Priority-based eviction (keep frequently accessed, evict stale)

8. **Distributed Caching**
   - Scale horizontally with cache sharding
   - Use consistent hashing for entity distribution
   - Support multi-region deployments

---

## Appendix

### A. Timestamp Format Standards

All timestamps use **ISO 8601 format with UTC timezone**:

```
Format: YYYY-MM-DDTHH:MM:SSZ
Example: 2025-11-03T14:32:28Z
         ^^^^-^^-^^T^^:^^:^^Z
         │   │  │  │  │  │  └─ UTC indicator
         │   │  │  │  │  └──── Seconds
         │   │  │  │  └─────── Minutes
         │   │  │  └────────── Hours (24-hour)
         │   │  └───────────── Day
         │   └──────────────── Month
         └──────────────────── Year
```

**Python Implementation**:
```python
from datetime import datetime, timezone

# Generate timestamp
now = datetime.now(timezone.utc).isoformat()
# Result: "2025-11-03T14:32:28.123456+00:00"

# Normalize to Z suffix
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
# Result: "2025-11-03T14:32:28Z"
```

### B. MongoDB Connection Best Practices

```python
# Singleton pattern for MongoDB client
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

_mongo_client = None

def get_mongo_client() -> MongoClient:
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(
            os.getenv("MONGO_URI", "mongodb://localhost:27017"),
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            maxPoolSize=50,                  # Connection pool
            retryWrites=True                 # Auto-retry failed writes
        )
    return _mongo_client

def get_db():
    client = get_mongo_client()
    db_name = os.getenv("DB_NAME", "splitwise")
    return client[db_name]
```

### C. Error Classification

| Error Type | HTTP Status | Cache Behavior | User Impact |
|------------|-------------|----------------|-------------|
| `ConnectionTimeout` | N/A | Use stale cache | None (degraded freshness) |
| `APIRateLimitExceeded` | 429 | Use stale cache | None (temporary) |
| `APIUnavailable` | 500/503 | Use stale cache | None (service continues) |
| `InvalidAPIKey` | 401 | Fail request | Critical (requires fix) |
| `ResourceNotFound` | 404 | Return empty | Expected (user deleted item) |
| `CacheCorruption` | N/A | Re-fetch from API | None (auto-recovered) |
| `MongoDBUnavailable` | N/A | Fail request | Critical (requires fix) |

### D. Monitoring Queries

**Cache Hit Rate**:
```python
# Add to cache operations
cache_hits = 0
cache_misses = 0

hit_rate = cache_hits / (cache_hits + cache_misses) * 100
```

**Cache Age Distribution**:
```python
pipeline = [
    {"$project": {
        "age_minutes": {
            "$divide": [
                {"$subtract": ["$$NOW", {"$toDate": "$last_updated_date"}]},
                60000  # Convert ms to minutes
            ]
        }
    }},
    {"$bucket": {
        "groupBy": "$age_minutes",
        "boundaries": [0, 1, 5, 15, 60, 1440],  # 0-1min, 1-5min, 5-15min, etc.
        "default": "1440+",
        "output": {"count": {"$sum": 1}}
    }}
]

distribution = db.expenses.aggregate(pipeline)
```

---

## Summary

This technical design document outlines a comprehensive caching strategy for the Splitwise MCP service that will:

1. **Improve Performance**: Reduce latency from ~500ms to ~50ms for cached requests (10x faster)
2. **Reduce API Load**: Decrease external API calls by 60-80% through intelligent caching
3. **Enhance Reliability**: Enable graceful degradation during Splitwise API outages
4. **Maintain Freshness**: Use notification-based invalidation for user data and TTL for shared data
5. **Scale Efficiently**: Normalize responses into entity collections for optimized queries

**Key Implementation Highlights**:
- MongoDB as persistent cache storage with entity normalization
- Dual invalidation strategy: notification-based (user data) + time-based TTL (shared data)
- Graceful degradation when Splitwise API is unavailable (use stale cache)
- Zero breaking changes to existing MCP tool interfaces
- Comprehensive testing and monitoring strategy

---

## Recent Critical Fix: Cache Query Parameters (2025-11-08)

### What Was Fixed

A critical bug in `_build_cache_query()` where filter parameters (date ranges, pagination) were not included in cache keys for `list_expenses`. This caused different API requests to incorrectly share cached data.

### Impact

- **Before Fix ❌**: `list_expenses(dated_after="2025-09-01")` and `list_expenses(dated_after="2025-10-01")` shared the same cache → returned wrong data (2 months instead of 1 month)
- **After Fix ✅**: Each unique combination of parameters gets its own cache entry → correct data always returned

### Changes Made

**Code Changes**:
- Updated `app/cached_splitwise_client.py::_build_cache_query()` to include ALL filter parameters in cache keys
- Added parameters to cache key: `dated_after`, `dated_before`, `updated_after`, `updated_before`, `limit`, `offset`

**Test Coverage**:
- Added 3 new tests in `tests/test_cached_client.py`:
  - `test_build_cache_query_list_expenses_with_date_filters` - Verifies date filters in cache key
  - `test_build_cache_query_list_expenses_with_all_filters` - Verifies all parameters included
  - `test_build_cache_query_list_expenses_different_date_ranges_different_keys` - Verifies different date ranges create different cache keys

**Documentation**:
- Added comprehensive "⚠️ CRITICAL: Cache Query Parameters" section (see above)
- Analyzed all 10 entity types for cache correctness
- Documented the bug scenario with before/after examples
- Added testing recommendations

### Verification

All 151 tests pass including:
- 44 cached client tests (3 new tests for this fix)
- 16 integration tests  
- All existing unit tests

### Key Takeaway

**Any parameter that affects the API response MUST be included in the cache query.** This is critical for cache correctness. The documentation now includes:
- Complete analysis of all 10 entity types
- Examples of correct vs incorrect cache key construction
- Testing recommendations to prevent similar bugs

---

## Next Steps

1. ✅ **COMPLETED**: Review cache query parameter handling for all entity types
2. ✅ **COMPLETED**: Fix `list_expenses` cache query to include all filter parameters
3. ✅ **COMPLETED**: Add comprehensive tests for date range and pagination caching
4. ✅ **COMPLETED**: Document the fix and analysis in this document
5. **PENDING**: User review of updated documentation
6. **NEXT**: Begin implementing entity normalization (see "Data Model & Entity Normalization" section)

---

**Document Version**: 1.0  
**Last Updated**: 2025-11-07  
**Status**: Draft - Awaiting Review
