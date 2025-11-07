"""MongoDB connection utilities.

This module provides a lazily initialised MongoDB client and helper
functions for retrieving database and collection instances.  Using
pymongo directly keeps the service synchronous; FastAPI runs
blocking IO in a threadpool when declaring route handlers as async.
"""

from __future__ import annotations

import os
from datetime import UTC, datetime
from typing import Any

from pymongo import MongoClient

from . import constants as const

_client: MongoClient | None = None


def get_client() -> MongoClient:
    """Return a cached MongoDB client, creating it if necessary.

    The connection URI and database name are read from environment
    variables `MONGO_URI` and `DB_NAME`.  If no URI is provided,
    defaults to `mongodb://localhost:27017`.
    """
    global _client
    if _client is None:
        mongo_uri = os.environ.get(const.ENV_MONGO_URI, const.DEFAULT_MONGO_URI)
        _client = MongoClient(mongo_uri)
    return _client


def get_db() -> Any:
    """Return the configured database object."""
    client = get_client()
    db_name = os.environ.get(const.ENV_DB_NAME, const.DEFAULT_DB_NAME)
    return client[db_name]


def insert_document(collection: str, document: dict[str, Any]) -> Any:
    """Insert a document into the specified collection.

    Adds a timestamp to the document before insertion.
    Returns the inserted document's ID.
    Raises exception if MongoDB is not available.
    """
    db = get_db()
    document = {**document, "timestamp": datetime.now(UTC)}
    result = db[collection].insert_one(document)
    return result.inserted_id


def find_latest(collection: str) -> dict[str, Any] | None:
    """Return the most recently inserted document from a collection.

    This helper is used by REST endpoints to retrieve cached data.
    Returns `None` if the collection is empty.
    """
    db = get_db()
    return db[collection].find_one(sort=[("timestamp", -1)])


def find_all(
    collection: str, filter_query: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Return all documents matching the filter from a collection.

    If `filter_query` is None, all documents are returned.  Note that
    this may return many documents; consumers should filter or limit
    results as appropriate.
    """
    db = get_db()
    q = filter_query or {}
    return list(db[collection].find(q))
