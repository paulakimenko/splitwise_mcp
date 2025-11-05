"""Integration tests for Splitwise MCP Service.

These tests run against the actual Splitwise API to validate end-to-end functionality.
They create a test group and perform real API operations to ensure the MCP proxy
service works correctly with the Splitwise service.

IMPORTANT: These tests require a valid SPLITWISE_API_KEY in the environment.
They will create and clean up test data, but should not modify existing data.
"""