"""Tests for app.db module."""

from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest

from app.db import find_all, find_latest, get_client, get_db, insert_document


class TestDatabaseConnection:
    """Test database connection functions."""

    @patch("app.db.MongoClient")
    def test_get_client_default_uri(self, mock_mongo_client):
        """Test getting client with default URI."""
        with patch.dict("os.environ", {}, clear=True):
            # Clear the global client to force new connection
            import app.db

            app.db._client = None

            get_client()
            mock_mongo_client.assert_called_once_with("mongodb://localhost:27017")

    @patch("app.db.MongoClient")
    def test_get_client_custom_uri(self, mock_mongo_client):
        """Test getting client with custom URI."""
        with patch.dict("os.environ", {"MONGO_URI": "mongodb://custom:27017"}):
            # Clear the global client to force new connection
            import app.db

            app.db._client = None

            get_client()
            mock_mongo_client.assert_called_once_with("mongodb://custom:27017")

    @patch("app.db.get_client")
    def test_get_db_default_name(self, mock_get_client):
        """Test getting database with default name."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        with patch.dict("os.environ", {}, clear=True):
            get_db()
            mock_client.__getitem__.assert_called_once_with("splitwise")

    @patch("app.db.get_client")
    def test_get_db_custom_name(self, mock_get_client):
        """Test getting database with custom name."""
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        with patch.dict("os.environ", {"DB_NAME": "custom_db"}):
            get_db()
            mock_client.__getitem__.assert_called_once_with("custom_db")


class TestDatabaseOperations:
    """Test database operations."""

    @patch("app.db.get_db")
    def test_insert_document(self, mock_get_db):
        """Test inserting a document."""
        mock_db = MagicMock()
        mock_collection = Mock()
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db

        # Mock the insert result
        mock_result = Mock()
        mock_result.inserted_id = "test_id"
        mock_collection.insert_one.return_value = mock_result

        document = {"test": "data"}
        result = insert_document("test_collection", document)

        # Verify the document was inserted with timestamp
        assert mock_collection.insert_one.called
        inserted_doc = mock_collection.insert_one.call_args[0][0]
        assert inserted_doc["test"] == "data"
        assert "timestamp" in inserted_doc
        assert isinstance(inserted_doc["timestamp"], datetime)
        assert result == "test_id"

    @patch("app.db.get_db")
    def test_find_latest(self, mock_get_db):
        """Test finding latest document."""
        mock_db = MagicMock()
        mock_collection = Mock()
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db

        expected_doc = {"id": 1, "data": "latest"}
        mock_collection.find_one.return_value = expected_doc

        result = find_latest("test_collection")

        mock_collection.find_one.assert_called_once_with(sort=[("timestamp", -1)])
        assert result == expected_doc

    @patch("app.db.get_db")
    def test_find_latest_empty(self, mock_get_db):
        """Test finding latest document when collection is empty."""
        mock_db = MagicMock()
        mock_collection = Mock()
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db

        mock_collection.find_one.return_value = None

        result = find_latest("test_collection")

        assert result is None

    @patch("app.db.get_db")
    def test_find_all_no_filter(self, mock_get_db):
        """Test finding all documents without filter."""
        mock_db = MagicMock()
        mock_collection = Mock()
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db

        expected_docs = [{"id": 1}, {"id": 2}]
        mock_collection.find.return_value = expected_docs

        result = find_all("test_collection")

        mock_collection.find.assert_called_once_with({})
        assert result == expected_docs

    @patch("app.db.get_db")
    def test_find_all_with_filter(self, mock_get_db):
        """Test finding all documents with filter."""
        mock_db = MagicMock()
        mock_collection = Mock()
        mock_db.__getitem__.return_value = mock_collection
        mock_get_db.return_value = mock_db

        expected_docs = [{"id": 1, "status": "active"}]
        mock_collection.find.return_value = expected_docs

        filter_query = {"status": "active"}
        result = find_all("test_collection", filter_query)

        mock_collection.find.assert_called_once_with(filter_query)
        assert result == expected_docs
