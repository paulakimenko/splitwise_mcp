#!/usr/bin/env python3
"""Test SSE parsing for large responses."""

import json

import requests

url = "http://localhost:8000/mcp"

# Initialize
init_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "Test", "version": "1.0"},
    },
}

response = requests.post(
    url,
    json=init_request,
    headers={
        "Content-Type": "application/json",
        "Accept": "text/event-stream, application/json",
    },
)
session_id = response.headers.get("Mcp-Session-Id")
print(f"Session ID: {session_id}\n")

# List tools
tools_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

response = requests.post(
    url,
    json=tools_request,
    headers={
        "Content-Type": "application/json",
        "Accept": "text/event-stream, application/json",
        "Mcp-Session-Id": session_id,
    },
)

print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")
print(f"\nRaw Response Length: {len(response.text)} bytes\n")
print("=" * 80)
print("RAW RESPONSE:")
print("=" * 80)
print(response.text)
print("=" * 80)

# Try to parse SSE properly
print("\nParsing SSE...")
lines = response.text.split("\n")
print(f"Number of lines: {len(lines)}\n")

data_buffer = ""
for i, line in enumerate(lines):
    print(f"Line {i}: {repr(line[:80])}")
    if line.startswith("data: "):
        data_buffer += line[6:]
    elif line.startswith("data:"):
        data_buffer += line[5:]
    elif line == "" and data_buffer:
        # Empty line signals end of message
        try:
            parsed = json.loads(data_buffer)
            print("\n✅ Successfully parsed JSON")
            print(json.dumps(parsed, indent=2))
            break
        except json.JSONDecodeError as e:
            print(f"\n❌ JSON parse error: {e}")
            print(f"Buffer length: {len(data_buffer)}")
            print(f"Buffer content:\n{data_buffer}")
            data_buffer = ""
    else:
        # Continuation line (no "data: " prefix)
        data_buffer += line

# Try parsing the full buffer if we haven't succeeded
if data_buffer and data_buffer.strip():
    print(f"\nTrying to parse remaining buffer ({len(data_buffer)} bytes)...")
    try:
        parsed = json.loads(data_buffer)
        print("✅ Successfully parsed JSON from buffer")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"Buffer:\n{data_buffer}")
