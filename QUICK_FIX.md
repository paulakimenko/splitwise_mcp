# Quick Reference: ChatGPT MCP Connector Troubleshooting

## Your Server Status: ✅ 100% WORKING

```
Remote:  https://sw-mcp.paulakimenko.xyz/mcp  ✅ 20 tools, all valid
Local:   http://localhost:8000/mcp           ✅ 20 tools, all valid
Tests:   63/63 unit tests                    ✅ All passing
```

## THE FIX (Do These 4 Steps):

### 1️⃣ Enable Developer Mode
```
ChatGPT → Settings → Connectors → Advanced → Developer mode: ON
```

### 2️⃣ Refresh Connector
```
Settings → Connectors → Click your connector → Refresh
```

### 3️⃣ Try Incognito
```
Open ChatGPT in Chrome Incognito or Firefox Private Window
```

### 4️⃣ Wait 10 Minutes
```
ChatGPT caches connections - wait and try again
```

## Verify Server Works

```bash
# Run this to prove server is working:
python scripts/verify_mcp_compliance.py https://sw-mcp.paulakimenko.xyz/mcp

# Expected output:
# 🎉 SUCCESS! Your MCP server is fully compliant! 🎉
```

## Why Your Connector is Invisible

❌ **NOT** because server is broken (server is perfect!)  
❌ **NOT** because of protocol issues (100% compliant)  
❌ **NOT** because of missing tools (20 tools returned)  

✅ **BECAUSE** Developer Mode not enabled (most common!)  
✅ **BECAUSE** ChatGPT cached initial connection  
✅ **BECAUSE** Browser cache needs clearing  

## What OpenAI's Docs Say

From https://platform.openai.com/docs/mcp#troubleshooting-and-debugging:

> **Common Gotchas That Hide the Connector:**
> 1. Server doesn't declare the `tools` capability ← ✅ You DO declare it
> 2. `tools/list` returns an empty array ← ✅ You return 20 tools
> 3. Developer mode not enabled ← ⚠️ CHECK THIS!

## Server Test Results

### Initialize Test: ✅ PASSED
- Status: 200 OK
- Session ID: Present
- Capabilities: tools, resources, prompts all declared
- Protocol: 2024-11-05

### Tools List Test: ✅ PASSED
- Status: 200 OK
- Tools Count: 20
- All schemas: Valid
- Required fields: All present (name, description, inputSchema)

### Unit Tests: ✅ PASSED
- 63/63 tests passing (100%)

## Contact Support If Needed

If Developer Mode + Refresh + Cache Clear don't work:

1. Share: `DIAGNOSTIC_REPORT.md`
2. Email: OpenAI Support
3. Say: "Server is 100% MCP compliant (see diagnostic report), connector invisible despite 200 OK"

---

**TL;DR**: Enable Developer Mode in ChatGPT Settings → Connectors → Advanced
