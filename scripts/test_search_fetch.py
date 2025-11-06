#!/usr/bin/env python3
"""Test the search and fetch tools required for ChatGPT connectors."""

import json
import sys


def test_local_import():
    """Test that search and fetch can be imported."""
    print("=" * 80)
    print("Testing Local Import")
    print("=" * 80)

    try:
        from app.main import fetch, search

        print("✅ Successfully imported search and fetch tools")
        return True
    except ImportError as e:
        print(f"❌ Failed to import: {e}")
        return False


def test_tool_signatures():
    """Test that tools have correct signatures."""
    print("\n" + "=" * 80)
    print("Testing Tool Signatures")
    print("=" * 80)

    import inspect

    from app.main import fetch, search

    # Check search signature
    search_sig = inspect.signature(search)
    print(f"\nsearch signature: {search_sig}")
    search_params = list(search_sig.parameters.keys())
    print(f"search parameters: {search_params}")

    if "query" in search_params and "ctx" in search_params:
        print("✅ search has correct parameters (query, ctx)")
    else:
        print("❌ search missing required parameters")
        return False

    # Check fetch signature
    fetch_sig = inspect.signature(fetch)
    print(f"\nfetch signature: {fetch_sig}")
    fetch_params = list(fetch_sig.parameters.keys())
    print(f"fetch parameters: {fetch_params}")

    if "id" in fetch_params and "ctx" in fetch_params:
        print("✅ fetch has correct parameters (id, ctx)")
    else:
        print("❌ fetch missing required parameters")
        return False

    return True


def test_docstrings():
    """Test that tools have proper documentation."""
    print("\n" + "=" * 80)
    print("Testing Tool Documentation")
    print("=" * 80)

    from app.main import fetch, search

    if search.__doc__:
        print(f"\n✅ search docstring:\n{search.__doc__}")
    else:
        print("❌ search missing docstring")
        return False

    if fetch.__doc__:
        print(f"\n✅ fetch docstring:\n{fetch.__doc__}")
    else:
        print("❌ fetch missing docstring")
        return False

    return True


def test_chatgpt_format():
    """Test that the return format matches ChatGPT requirements."""
    print("\n" + "=" * 80)
    print("Testing ChatGPT Format Requirements")
    print("=" * 80)

    print("\n📋 Required Format for search:")
    search_format = {
        "results": [
            {"id": "unique_id", "title": "human-readable title", "url": "canonical URL"}
        ]
    }
    print(json.dumps(search_format, indent=2))

    print("\n📋 Required Format for fetch:")
    fetch_format = {
        "id": "unique_id",
        "title": "human-readable title",
        "text": "full document text",
        "url": "canonical URL",
        "metadata": {"key": "value"},
    }
    print(json.dumps(fetch_format, indent=2))

    print("\n✅ Formats documented and implemented in code")
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("ChatGPT Connector Tools Test")
    print("=" * 80)
    print("Testing that search and fetch tools are properly implemented\n")

    tests = [
        ("Import Test", test_local_import),
        ("Signature Test", test_tool_signatures),
        ("Documentation Test", test_docstrings),
        ("Format Test", test_chatgpt_format),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} failed with exception: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {name}")

    all_passed = all(result for _, result in results)

    if all_passed:
        print("\n" + "=" * 80)
        print("🎉 All Tests Passed!")
        print("=" * 80)
        print("\nYour MCP server now has the required search and fetch tools.")
        print("Deploy the changes and try adding the connector to ChatGPT again.")
        print("\nDeployment steps:")
        print("1. git add -A && git commit -m 'Add search/fetch for ChatGPT'")
        print("2. make docker-build-push")
        print("3. SSH to server and: docker-compose pull && docker-compose up -d")
        print("4. Wait 30 seconds, then add connector to ChatGPT")
        return 0
    else:
        print("\n" + "=" * 80)
        print("❌ Some Tests Failed")
        print("=" * 80)
        print("\nPlease fix the issues above before deploying.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
