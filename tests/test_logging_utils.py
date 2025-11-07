"""Tests for logging utilities with PII masking."""

from __future__ import annotations

from unittest.mock import patch

from app.logging_utils import (
    log_operation,
    mask_email,
    mask_name,
    mask_pii,
    mask_pii_in_string,
)


class TestPIIMasking:
    """Test PII masking functions."""

    def test_mask_email_standard(self):
        """Test masking of standard email addresses."""
        assert mask_email("john.doe@example.com") == "j***@example.com"
        assert mask_email("alice@test.org") == "a***@test.org"

    def test_mask_email_short_local(self):
        """Test masking of email with single character local part."""
        assert mask_email("a@example.com") == "*@example.com"

    def test_mask_email_invalid(self):
        """Test handling of invalid email formats."""
        assert mask_email("not-an-email") == "not-an-email"
        assert mask_email("") == ""

    def test_mask_name_single_word(self):
        """Test masking of single-word names."""
        assert mask_name("John") == "J***"
        assert mask_name("A") == "***"

    def test_mask_name_multiple_words(self):
        """Test masking of multi-word names."""
        assert mask_name("John Doe") == "J*** D***"
        assert mask_name("Mary Jane Watson") == "M*** J*** W***"

    def test_mask_name_empty(self):
        """Test handling of empty names."""
        assert mask_name("") == "***"

    def test_mask_pii_in_string(self):
        """Test email masking in arbitrary strings."""
        text = "Contact us at support@example.com or admin@test.org"
        result = mask_pii_in_string(text)
        assert "s***@example.com" in result
        assert "a***@test.org" in result
        assert "support@example.com" not in result

    def test_mask_pii_dict_with_names(self):
        """Test masking of name fields in dictionaries."""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
        }
        masked = mask_pii(data)
        assert masked["first_name"] == "J***"
        assert masked["last_name"] == "D***"
        assert masked["age"] == 30

    def test_mask_pii_dict_with_email(self):
        """Test masking of email fields in dictionaries."""
        data = {
            "email": "john@example.com",
            "user_email": "admin@test.org",
            "id": 123,
        }
        masked = mask_pii(data)
        assert masked["email"] == "j***@example.com"
        assert masked["user_email"] == "a***@test.org"
        assert masked["id"] == 123

    def test_mask_pii_nested_dict(self):
        """Test masking in nested dictionaries."""
        data = {
            "user": {
                "first_name": "Alice",
                "email": "alice@example.com",
                "profile": {
                    "last_name": "Smith",
                },
            },
            "count": 5,
        }
        masked = mask_pii(data)
        assert masked["user"]["first_name"] == "A***"
        assert masked["user"]["email"] == "a***@example.com"
        assert masked["user"]["profile"]["last_name"] == "S***"
        assert masked["count"] == 5

    def test_mask_pii_list(self):
        """Test masking in lists."""
        data = [
            {"first_name": "John", "id": 1},
            {"first_name": "Jane", "id": 2},
        ]
        masked = mask_pii(data)
        assert masked[0]["first_name"] == "J***"
        assert masked[1]["first_name"] == "J***"
        assert masked[0]["id"] == 1

    def test_mask_pii_mixed_structure(self):
        """Test masking in complex mixed structures."""
        data = {
            "users": [
                {"first_name": "Alice", "email": "alice@test.com"},
                {"first_name": "Bob", "email": "bob@test.com"},
            ],
            "message": "Contact support@example.com for help",
            "count": 2,
        }
        masked = mask_pii(data)
        assert masked["users"][0]["first_name"] == "A***"
        assert masked["users"][0]["email"] == "a***@test.com"
        assert "s***@example.com" in masked["message"]
        assert masked["count"] == 2

    def test_mask_pii_primitives(self):
        """Test that primitives are returned unchanged."""
        assert mask_pii(123) == 123
        assert mask_pii(45.67) == 45.67
        assert mask_pii(True) is True
        assert mask_pii(None) is None

    def test_mask_pii_string_with_email(self):
        """Test masking emails in plain strings."""
        text = "Send to admin@example.com"
        masked = mask_pii(text)
        assert "a***@example.com" in masked
        assert "admin@example.com" not in masked


class TestLogOperation:
    """Test log_operation function."""

    @patch("app.logging_utils.logger")
    def test_log_operation_success(self, mock_logger):
        """Test successful operation logging."""
        params = {"group_id": 123}
        response = {"groups": [{"name": "Test"}]}

        log_operation("list_groups", "TOOL_CALL", params, response)

        # Should log at INFO level
        assert mock_logger.info.called
        call_args = mock_logger.info.call_args[0][0]
        assert "list_groups" in call_args
        assert "TOOL_CALL" in call_args

    @patch("app.logging_utils.logger")
    def test_log_operation_with_error(self, mock_logger):
        """Test operation logging with error."""
        error_msg = "API connection failed"

        log_operation("list_groups", "API_ERROR", None, None, error_msg)

        # Should log at ERROR level when error is present
        assert mock_logger.error.called
        call_args = mock_logger.error.call_args[0][0]
        assert "API_ERROR" in call_args
        assert "API connection failed" in call_args

    @patch("app.logging_utils.logger")
    def test_log_operation_masks_pii_in_params(self, mock_logger):
        """Test that PII in params is masked."""
        params = {
            "first_name": "John",
            "email": "john@example.com",
            "group_id": 123,
        }
        response = {"success": True}

        log_operation("create_friend", "TOOL_CALL", params, response)

        call_args = mock_logger.info.call_args[0][0]
        # PII should be masked
        assert "john@example.com" not in call_args
        assert "j***@example.com" in call_args or "J***" in call_args

    @patch("app.logging_utils.logger")
    def test_log_operation_masks_pii_in_response(self, mock_logger):
        """Test that PII in response is masked."""
        response = {
            "user": {
                "first_name": "Alice",
                "last_name": "Smith",
                "email": "alice@example.com",
            }
        }

        log_operation("get_current_user", "RESOURCE_READ", None, response)

        call_args = mock_logger.info.call_args[0][0]
        # PII should be masked
        assert "alice@example.com" not in call_args
        assert "Alice" not in call_args or "A***" in call_args

    @patch("app.logging_utils.logger")
    def test_log_operation_with_list_response(self, mock_logger):
        """Test logging with list response."""
        response = [{"id": 1}, {"id": 2}, {"id": 3}]

        log_operation("list_groups", "TOOL_CALL", None, response)

        call_args = mock_logger.info.call_args[0][0]
        # Should include count
        assert '"response_count": 3' in call_args

    @patch("app.logging_utils.logger")
    def test_log_operation_with_dict_response(self, mock_logger):
        """Test logging with dict response."""
        response = {"groups": [], "count": 0, "status": "ok"}

        log_operation("list_groups", "TOOL_CALL", None, response)

        call_args = mock_logger.info.call_args[0][0]
        # Should include response keys
        assert "response_keys" in call_args

    @patch("app.logging_utils.logger")
    def test_log_operation_exception_handling(self, mock_logger):
        """Test that logging exceptions don't break the operation."""
        # Make logger.info raise an exception
        mock_logger.info.side_effect = Exception("Logging failed")

        # Should not raise exception
        log_operation("test", "TEST", None, None)

        # Should call exception handler
        assert mock_logger.exception.called

    @patch("app.logging_utils.logger")
    def test_log_operation_none_params(self, mock_logger):
        """Test logging with None params."""
        log_operation("test", "TEST", None, {"result": "ok"})

        # Should not raise exception
        assert mock_logger.info.called

    @patch("app.logging_utils.logger")
    def test_log_operation_response_with_error_key(self, mock_logger):
        """Test logging response that contains error key."""
        response = {
            "error": "Something went wrong",
            "code": 400,
        }

        log_operation("create_expense", "TOOL_CALL", None, response)

        call_args = mock_logger.info.call_args[0][0]
        assert "response_error" in call_args
        assert "Something went wrong" in call_args
