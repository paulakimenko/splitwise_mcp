# Splitwise MCP Service Requirements
This document captures key requirements and constraints discovered while evaluating the current Splitwise MCP service running at https://sw-mcp.paulakimenko.xyz. The goal is to enable the server to be used as a fully‑functional Model‑Client Plugin (MCP) for tools such as ChatGPT Developer Mode.

## 1. Health endpoint
The service must expose a health‑check route, typically at /health.
The endpoint should return a JSON object that at least includes:
status (expected value: "healthy" when the service is operational).
service (e.g., "splitwise-mcp").
database indicating the state of the backing MongoDB connection (e.g., "connected").
A successful response from /health indicates that the application is running and the database is reachable; this should be maintained.
## 2. MCP API routing
The server must expose the MCP endpoints under a consistent base path (e.g., /mcp). Currently, requests to /mcp and /mcp/list_groups return 404 Not Found, so these routes need to be registered.
Each tool defined in the MCP specification should map to a corresponding endpoint. Examples:
GET /mcp/ping – returns a simple “pong” or health confirmation.
POST /mcp/list_groups – returns the list of Splitwise groups for the authenticated user.
POST /mcp/add_expense – creates a new expense entry.
The endpoints should accept JSON requests and return JSON responses conforming to the expected schemas. Error responses should include meaningful messages and HTTP status codes.
## 3. HTTPS and public availability
The MCP service must be publicly accessible via HTTPS. ChatGPT Developer Mode only connects to remote services; local or HTTP‑only services are not supported.
A valid TLS certificate should be installed for the domain (e.g., via Let’s Encrypt). The certificate must remain current to avoid connection failures.
DNS should point the domain (e.g., sw-mcp.paulakimenko.xyz) to the public IP where the service is hosted.
## 4. Manifest and tool descriptions
A manifest file should be published (commonly at /.well-known/ai-plugin.json), describing the available MCP tools, endpoints, and their arguments. This allows ChatGPT Developer Mode to discover and use the service.
The manifest must list each tool name, its HTTP method and route, the expected JSON schema for input and output, and any authentication requirements.
Tool definitions should be kept up to date with the actual server implementation to avoid mismatches.
## 5. Authentication and authorization
If the MCP service requires authentication to access Splitwise data, Bearer tokens or another secure method should be implemented.
The authentication mechanism should be documented in the manifest and must not expose sensitive credentials in responses.
For initial testing, endpoints may allow unsecured access, but production usage should always verify tokens or API keys.
## 6. Cross‑origin considerations
If the MCP service will be accessed by web clients (e.g., a front‑end), CORS headers should be configured appropriately.
At minimum, set Access-Control-Allow-Origin for trusted domains and specify allowed methods/headers to prevent cross‑site request issues.
## 7. Database connectivity and stability
The service relies on a MongoDB database. The connection string should be configurable via environment variables and handled lazily to avoid startup failures.
Connection errors should be logged and surfaced through the health‑check endpoint.
All operations (e.g., listing groups, adding expenses) should handle database failures gracefully with appropriate error codes.
## 8. Optional enhancements
Streaming/Server‑Sent Events (SSE): If long‑running operations (e.g., generating reports) are needed, consider implementing SSE endpoints for incremental updates.
Logging and metrics: Provide structured logs and metrics (e.g., request counts, latency) for debugging and monitoring.
Versioning: Include a version identifier in API responses or as part of the URL (e.g., /v1/mcp/ping) to allow for future changes without breaking clients.
By addressing these requirements—implementing the missing MCP endpoints, ensuring HTTPS accessibility, providing a proper manifest and authentication, and maintaining database connectivity—the Splitwise MCP service can be successfully integrated as a remote plugin for tools like ChatGPT Developer Mode.