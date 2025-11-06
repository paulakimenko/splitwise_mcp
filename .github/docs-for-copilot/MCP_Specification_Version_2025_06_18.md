# Model Context Protocol (MCP) Specification – Version 2025-06-18

**Model Context Protocol (MCP)** is an open protocol that enables seamless integration between LLM applications and external data sources and tools[\[1\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Model%20Context%20Protocol%20,%E2%80%9CSHOULD%20NOT%E2%80%9D%2C%20%E2%80%9CRECOMMENDED%E2%80%9D%2C%20%E2%80%9CNOT%20RECOMMENDED%E2%80%9D). Whether you’re building an AI-powered IDE, enhancing a chat interface, or creating custom AI workflows, MCP provides a standardized way to connect LLMs with the context they need. This specification defines the authoritative protocol requirements (based on the TypeScript schema in the MCP repository[\[2\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=protocol%20requirements%2C%20based%20on%20the,all%20capitals%2C%20as%20shown%20here)). The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in **BCP 14** (see RFC2119 and RFC8174)[\[3\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=schema,all%20capitals%2C%20as%20shown%20here) when, and only when, they appear in all capitals, as shown here.

## Overview

MCP provides a standardized way for applications to:

* Share contextual information with language models[\[4\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=MCP%20provides%20a%20standardized%20way,for%20applications%20to)

* Expose tools and capabilities to AI systems[\[4\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=MCP%20provides%20a%20standardized%20way,for%20applications%20to)

* Build composable integrations and workflows[\[4\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=MCP%20provides%20a%20standardized%20way,for%20applications%20to)

The protocol uses **JSON-RPC 2.0** messages[\[5\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=The%20protocol%20uses%20JSON,messages%20to%20establish%20communication%20between) to establish communication between:

* **Hosts** – LLM applications that initiate connections

* **Clients** – Connectors within the host application

* **Servers** – Services that provide context and capabilities

MCP takes inspiration from the *Language Server Protocol*[\[6\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=MCP%20takes%20some%20inspiration%20from,the%20ecosystem%20of%20AI%20applications), which standardizes how to add support for programming languages across development tools. Similarly, MCP standardizes how to integrate additional context and tools into the ecosystem of AI applications.

## Key Details

### Base Protocol

* **JSON-RPC message format**[\[7\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Base%20Protocol)

* **Stateful connections** (persistent sessions)[\[8\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=%2A%20JSON,Server%20and%20client%20capability%20negotiation)

* **Server and client capability negotiation**[\[8\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=%2A%20JSON,Server%20and%20client%20capability%20negotiation)

### Features

**Servers** may offer any of the following features to clients[\[9\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Servers%20offer%20any%20of%20the,following%20features%20to%20clients):

* **Resources** – Context and data for the user or the AI model to use

* **Prompts** – Templated messages and workflows for users

* **Tools** – Functions for the AI model to execute

**Clients** may offer the following features to servers[\[10\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Clients%20may%20offer%20the%20following,features%20to%20servers):

* **Sampling** – Server-initiated agentic behaviors and recursive LLM interactions

* **Roots** – Server-initiated inquiries into URI or filesystem boundaries to operate in

* **Elicitation** – Server-initiated requests for additional information from users

### Additional Utilities

* **Configuration** – e.g. setting log verbosity

* **Progress tracking** – Status notifications for long-running operations

* **Cancellation** – Canceling in-progress requests

* **Error reporting** – Standardized error codes and messages

* **Logging** – Structured logs and debug information

All implementations **MUST** support the base protocol and lifecycle management components. Other components **MAY** be implemented based on specific application needs[\[11\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=All%20implementations%20MUST%20support%20the,exactly%20the%20features%20they%20need). These protocol layers establish clear separation of concerns while enabling rich interactions between clients and servers. The modular design allows implementations to support exactly the features they need[\[11\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=All%20implementations%20MUST%20support%20the,exactly%20the%20features%20they%20need).

## Security and Trust & Safety

The Model Context Protocol enables powerful capabilities through arbitrary data access and code execution paths. With this power comes important security and trust considerations that all implementors must carefully address[\[12\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=The%20Model%20Context%20Protocol%20enables,all%20implementors%20must%20carefully%20address).

### Key Principles

1. **User Consent and Control** – Users must explicitly consent to and understand all data access and operations. Users must retain control over what data is shared and what actions are taken. Implementors should provide clear UIs for reviewing and authorizing activities[\[13\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=1,before%20exposing%20user%20data%20to).

2. **Data Privacy** – Hosts must obtain explicit user consent before exposing user data to servers. Hosts must not transmit resource data elsewhere without user consent. User data should be protected with appropriate access controls[\[14\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=2.%20Data%20Privacy%20,Tool%20Safety).

3. **Tool Safety** – Tools represent arbitrary code execution and must be treated with appropriate caution. Descriptions of tool behavior (such as annotations) should be considered untrusted unless obtained from a trusted server. Hosts must obtain explicit user consent before invoking any tool, and users should understand what each tool does before authorizing its use[\[15\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=3.%20Tool%20Safety%20,LLM%20Sampling%20Controls).

4. **LLM Sampling Controls** – Users must explicitly approve any LLM sampling requests. Users should control whether sampling occurs at all, the actual prompt that will be sent, and what results the server can see[\[16\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=4.%20LLM%20Sampling%20Controls%20,limits%20server%20visibility%20into%20prompts). The protocol intentionally limits server visibility into prompts to enforce this principle[\[16\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=4.%20LLM%20Sampling%20Controls%20,limits%20server%20visibility%20into%20prompts).

### Implementation Guidelines

While MCP itself cannot enforce these security principles at the protocol level, implementors **SHOULD**[\[17\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Implementation%20Guidelines):

1. Build robust consent and authorization flows into their applications.

2. Provide clear documentation of security implications.

3. Implement appropriate access controls and data protections.

4. Follow security best practices in their integrations.

5. Consider privacy implications in feature designs.

*(The following sections detail each component of the MCP specification, including protocol architecture, base protocol requirements, client features, server features, utilities, and a full schema reference.)*

## Key Changes

This section lists changes made to the MCP specification in this 2025-06-18 revision (relative to the previous 2025-03-26 revision)[\[18\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=This%20document%20lists%20changes%20made,26):

**Major changes:**

1. **Removed JSON-RPC Batching:** JSON-RPC request **batching** is no longer supported[\[19\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=Major%20changes).

2. **Structured Tool Output:** Added support for structured tool outputs (tools can return structured results in addition to text)[\[20\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=1.%20Remove%20support%20for%20JSON,371).

3. **OAuth Resource Server Model:** MCP servers are now classified as OAuth 2.1 Resource Servers, including protected resource metadata to discover the corresponding Authorization Server[\[21\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=2,in%20a%20new%20%2013).

4. **Resource Indicators Required:** MCP clients must implement OAuth 2.0 Resource Indicators (RFC 8707\)[\[22\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=4,603) to prevent malicious servers from obtaining tokens intended for other services.

5. **Security Best Practices Clarified:** Expanded security considerations and best practices in the Authorization spec and a new Security Best Practices document[\[23\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=access%20tokens.%20%28PR%20,enabling%20servers%20to%20request%20additional).

6. **Elicitation Feature:** Added support for **elicitation** (servers can request additional info from users during interactions)[\[24\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=authorization%20spec%20and%20in%20a,%28PR).

7. **Resource Links in Tool Results:** Tools can now return **resource links** (reference to server resources) in their results[\[25\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=information%20from%20users%20during%20interactions,Protocol).

8. **Explicit Protocol Version Header:** When using HTTP, the negotiated MCP protocol version **MUST** be specified via the MCP-Protocol-Version HTTP header on subsequent requests[\[26\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=,548).

9. **Lifecycle Clarification:** The Lifecycle phase description was updated (e.g. a recommendation was changed from SHOULD to MUST in the Operation phase)[\[27\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=Version,to%20MUST%20in%20Lifecycle%20Operation).

**Other schema changes:**

1. Added \_meta field to additional interface types and specified its proper usage[\[28\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=Other%20schema%20changes).

2. Added a context field to CompletionRequest to include previously-resolved variables in completion requests[\[29\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=1.%20Add%20,resolved%20variables%20%28PR%20%23598).

3. Added a title field to various objects for human-friendly display names, allowing name to serve as a stable programmatic identifier[\[30\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=2.%20Add%20,663).

*(For a complete list of changes since the last revision, see the full changelog on GitHub[\[31\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=Full%20changelog).)*

## Architecture

MCP follows a **client–host–server** architecture where each host can run multiple client instances[\[32\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=The%20Model%20Context%20Protocol%20,coordination%20between%20clients%20and%20servers). This enables users to integrate AI capabilities across applications while maintaining clear security boundaries and isolating concerns. Built on JSON-RPC, MCP provides a stateful session protocol focused on context exchange and sampling coordination between clients and servers[\[32\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=The%20Model%20Context%20Protocol%20,coordination%20between%20clients%20and%20servers).

### Core Components

**Host:** The host process acts as the container and coordinator[\[33\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=The%20host%20process%20acts%20as,the%20container%20and%20coordinator):

* Creates and manages multiple client instances

* Controls client connection permissions and lifecycle

* Enforces security policies and consent requirements

* Handles user authorization decisions

* Coordinates AI/LLM integration and sampling

* Manages context aggregation across clients

**Clients:** Each client is created by the host and maintains an isolated server connection[\[34\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=Clients):

* Establishes one stateful session per server

* Handles protocol negotiation and capability exchange

* Routes protocol messages bidirectionally

* Manages subscriptions and notifications

* Maintains security boundaries between servers

A host application may create and manage multiple clients, with each client having a 1:1 relationship with a particular server[\[35\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,Maintains%20security%20boundaries%20between%20servers).

**Servers:** Servers provide specialized context and capabilities[\[36\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=Servers):

* Expose resources, tools, and prompts via MCP primitives

* Operate independently with focused responsibilities

* Request sampling via client interfaces

* Must respect security constraints

* Can be local processes or remote services

### Design Principles

MCP’s design principles inform its architecture[\[37\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=MCP%20is%20built%20on%20several,inform%20its%20architecture%20and%20implementation)[\[38\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,are%20controlled%20by%20the%20host):

1. **Ease of Building Servers:** Servers should be extremely easy to build. Host applications handle complex orchestration, so servers can focus on specific, well-defined capabilities. Simple interfaces minimize implementation overhead and clear separation enables maintainable code[\[39\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=1,Shared%20protocol%20enables%20interoperability).

2. **High Composability:** Servers should be highly composable. Each server provides focused functionality in isolation, and multiple servers can be combined seamlessly. A shared protocol enables interoperability and a modular design supports extensibility[\[40\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,receive%20only%20necessary%20contextual%20information).

3. **Isolation:** Servers should **not** be able to read the whole conversation nor see into other servers. Servers receive only necessary contextual information; full conversation history stays with the host. Each server connection remains isolated, and any cross-server interactions are controlled by the host (which enforces security boundaries)[\[41\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,Host%20process%20enforces%20security%20boundaries).

4. **Extensibility:** Features can be added to servers and clients progressively. The core protocol provides minimal required functionality, and additional capabilities can be negotiated as needed. Servers and clients can evolve independently. The protocol is designed for future extensibility while maintaining backwards compatibility[\[42\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,Backwards%20compatibility%20is%20maintained).

### Capability Negotiation

MCP uses capability-based negotiation: clients and servers explicitly declare their supported features during initialization[\[43\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=Capability%20Negotiation). Capabilities determine which protocol features and primitives are available during a session[\[43\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=Capability%20Negotiation). For example[\[44\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=Each%20capability%20unlocks%20specific%20protocol,For%20example):

* **Server capabilities** might include prompts, resources, tools, logging, completions, etc. These must be advertised by the server if those features are implemented[\[45\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,declare%20support%20in%20its%20capabilities). For instance, tool invocation requires the server to declare the tools capability; emitting resource subscription notifications requires declaring resources.subscribe; providing prompt templates requires prompts, and so on[\[45\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,declare%20support%20in%20its%20capabilities).

* **Client capabilities** might include roots, sampling, elicitation, etc., indicating support for those server-initiated features[\[46\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Category%20Capability%20Description%20Client%20,standard%20experimental%20features). For example, a client declares roots if it can provide a list of filesystem roots, sampling if it supports server-initiated LLM calls, etc.[\[46\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Category%20Capability%20Description%20Client%20,standard%20experimental%20features).

Both parties **MUST** respect the declared capabilities throughout the session[\[47\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,through%20extensions%20to%20the%20protocol). Additional capabilities can be negotiated through protocol extensions in the future[\[47\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,through%20extensions%20to%20the%20protocol). This mechanism ensures that clients and servers have a mutual understanding of supported functionality while preserving extensibility.

*(See also the* *Version Negotiation* *section under Lifecycle for how protocol versions are agreed upon.)*

## Base Protocol

### Overview

**Protocol Revision:** 2025-06-18[\[48\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Protocol%20Revision%3A%202025)

The Model Context Protocol consists of several key components that work together[\[49\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=The%20Model%20Context%20Protocol%20consists,key%20components%20that%20work%20together):

* **Base Protocol:** Core JSON-RPC message types (requests, responses, notifications)

* **Lifecycle Management:** Connection initialization, capability negotiation, and session control

* **Authorization:** Authentication and authorization framework for HTTP-based transports

* **Server Features:** Resources, prompts, and tools exposed by servers

* **Client Features:** Sampling and root directory listing provided by clients

* **Utilities:** Cross-cutting concerns like logging, progress tracking, and cancellation

All implementations **MUST** support the base protocol and lifecycle management components[\[11\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=All%20implementations%20MUST%20support%20the,exactly%20the%20features%20they%20need). Other components **MAY** be implemented as needed by the application. These layers provide separation of concerns while enabling rich interactions. The design is modular so implementations can include only the features they require[\[11\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=All%20implementations%20MUST%20support%20the,exactly%20the%20features%20they%20need).

#### *Messages*

All messages between MCP clients and servers **MUST** follow the JSON-RPC 2.0 specification[\[50\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=All%20messages%20between%20MCP%20clients,defines%20these%20types%20of%20messages). The protocol defines these types of messages:

* **Requests:** Sent from client to server *or* server to client to initiate an operation.

* **Responses:** Sent in reply to requests, containing the result or error of the operation.

* **Notifications:** One-way messages sent from client to server or vice versa, which do not expect a response.

**Requests:** Requests must conform to the JSON-RPC request object format[\[51\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Copy):

{  
  "jsonrpc": "2.0",  
  "id": string | number,  
  "method": string,  
  "params": {  
    // request parameters (object)  
  }  
}

* Requests **MUST** include a string or integer id[\[52\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,requestor%20within%20the%20same%20session) (note: unlike base JSON-RPC, the ID must not be null).

* The request id **MUST NOT** have been previously used by the requestor within the same session[\[52\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,requestor%20within%20the%20same%20session).

**Responses:** Responses return the result or error for a given request[\[53\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Responses):

{  
  "jsonrpc": "2.0",  
  "id": string | number,  
  "result": { ... } ,  
  "error": {  
    "code": number,  
    "message": string,  
    "data": { ... }  
  }  
}

* Responses **MUST** include the same id as the request they correspond to[\[54\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,Error%20codes%20MUST%20be%20integers).

* A response contains either a result (on success) or an error (on failure). **Either** result **or** error **MUST** be set, but not both[\[54\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,Error%20codes%20MUST%20be%20integers).

* If present, result can be any JSON object. If an error occurred, error must include at least an integer code and a string message (with optional data for additional info)[\[55\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=errors.%20Either%20a%20,Error%20codes%20MUST%20be%20integers).

* Error code values **MUST** be integers[\[56\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,Error%20codes%20MUST%20be%20integers). (Specific error codes for common conditions are defined later.)

**Notifications:** Notifications are one-way JSON-RPC messages with no response[\[57\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Notifications):

{  
  "jsonrpc": "2.0",  
  "method": string,  
  "params": { ... }  
}

* Notifications **MUST NOT** include an id (since no response will be sent)[\[58\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=).

#### *Auth*

MCP provides an **Authorization** framework for use with HTTP transports[\[59\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Auth). Implementations using HTTP **SHOULD** conform to this spec (see the “Authorization” section), whereas implementations using STDIO **SHOULD NOT** follow that spec and instead retrieve credentials from the environment[\[60\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=MCP%20provides%20an%20Authorization%20framework,the%20future%20of%20the%20protocol). Clients and servers **MAY** also negotiate custom authentication/authorization strategies. *(For ongoing discussions or proposed changes to MCP auth mechanisms, see the MCP GitHub discussions forum[\[61\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=implementations%20using%20STDIO%20transport%20SHOULD,the%20future%20of%20the%20protocol).)*

#### *Schema*

The full specification of the protocol is formally defined in a TypeScript schema in the MCP repository[\[62\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=The%20full%20specification%20of%20the,use%20with%20various%20automated%20tooling). This TypeScript schema is the source of truth for all protocol messages and structures. A corresponding **JSON Schema** is also provided (automatically generated from the TypeScript source) for use with various tools[\[62\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=The%20full%20specification%20of%20the,use%20with%20various%20automated%20tooling).

#### *General fields – \_meta*

The \_meta property/parameter is **reserved** by MCP to allow clients and servers to attach additional metadata to their interactions[\[63\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=). Certain key names in \_meta are reserved by MCP for protocol-level metadata (see below); implementations MUST NOT make assumptions about values at these keys[\[64\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=The%20,Prefix). Additionally, definitions in the schema may reserve particular names in \_meta for specific purposes (as declared in those definitions)[\[64\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=The%20,Prefix).

**Key name format:** valid \_meta key names have two segments: an optional **prefix** and a **name**[\[65\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=names%20have%20two%20segments%3A%20an,Prefix).

* If a prefix is specified, it must consist of one or more labels separated by dots (.), followed by a slash (/). Each label must start with a letter and end with a letter or digit (interior characters can be letters, digits, or hyphens)[\[66\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,are%20all%20reserved).

* Any prefix beginning with zero or more valid labels, followed by modelcontextprotocol or mcp, followed by any valid label, is **reserved for MCP use**[\[67\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,are%20all%20reserved). *Examples:* modelcontextprotocol.io/, mcp.dev/, api.modelcontextprotocol.org/, and tools.mcp.com/ are reserved by MCP[\[67\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,are%20all%20reserved).

The **name** segment (after the prefix, if any) must begin and end with an alphanumeric character (\[A-Za-z0-9\]). It may contain hyphens (\-), underscores (\_), dots (.), and alphanumeric characters in between[\[68\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Name%3A).

*(Specific \_meta fields used by the protocol include progressToken for progress updates, etc., which are described later.)*

### Lifecycle

**Protocol Revision:** 2025-06-18[\[69\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Protocol%20Revision%3A%202025)

MCP defines a rigorous **lifecycle** for client–server connections that ensures proper capability negotiation and state management[\[70\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=The%20Model%20Context%20Protocol%20,capability%20negotiation%20and%20state%20management). The lifecycle has three phases[\[71\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=1,Graceful%20termination%20of%20the%20connection):

1. **Initialization:** Capability negotiation and protocol version agreement

2. **Operation:** Normal bidirectional protocol communication

3. **Shutdown:** Graceful termination of the connection

#### *Lifecycle Phases*

**Initialization:** This must be the first interaction between client and server[\[72\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Initialization). During initialization, the client and server:

* Establish protocol version compatibility

* Exchange and negotiate capabilities

* Share implementation details (e.g. software version, etc.)

The client **MUST** initiate initialization by sending an initialize request containing[\[73\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=The%20client%20MUST%20initiate%20this,request%20containing):

* The protocol version it supports

* The client’s capabilities

* Client implementation information (name, version, etc.)

**Example – Initialize Request:** (client \-\> server)

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "method": "initialize",  
  "params": {  
    "protocolVersion": "2024-11-05",  
    "capabilities": {  
      "roots": { "listChanged": true },  
      "sampling": {},  
      "elicitation": {}  
    },  
    "clientInfo": {  
      "name": "ExampleClient",  
      "title": "Example Client Display Name",  
      "version": "1.0.0"  
    }  
  }  
}

The server **MUST** respond with its own capabilities and information[\[74\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=The%20server%20MUST%20respond%20with,its%20own%20capabilities%20and%20information):

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "result": {  
    "protocolVersion": "2024-11-05",  
    "capabilities": {  
      "logging": {},  
      "prompts": { "listChanged": true },  
      "resources": { "subscribe": true, "listChanged": true },  
      "tools": { "listChanged": true }  
    },  
    "serverInfo": {  
      "name": "ExampleServer",  
      "title": "Example Server Display Name",  
      "version": "1.0.0"  
    },  
    "instructions": "Optional instructions for the client"  
  }  
}

After successful initialization, the client **MUST** send an initialized notification to indicate it is ready to begin normal operations[\[75\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=):

{  
  "jsonrpc": "2.0",  
  "method": "notifications/initialized"  
}

* The client **SHOULD NOT** send any requests (other than pings) before the server has responded to initialize[\[76\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=,notification).

* The server **SHOULD NOT** send any requests (other than pings or logging notifications) before receiving the initialized notification[\[77\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=,notification).

**Version Negotiation:** During initialization, the client sends a protocol version it supports in the initialize request. This should be the latest version the client supports[\[78\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Version%20Negotiation). If the server supports that version, it responds with the same version. Otherwise, the server **MUST** respond with another protocol version it supports (preferably its latest)[\[79\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=In%20the%20,server%E2%80%99s%20response%2C%20it%20SHOULD%20disconnect). If the client does not support the version proposed by the server, it **SHOULD** disconnect[\[80\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=server%20supports%20the%20requested%20protocol,server%E2%80%99s%20response%2C%20it%20SHOULD%20disconnect).

When using HTTP, after version negotiation the client must include an MCP-Protocol-Version: \<protocol-version\> header on all subsequent HTTP requests to the server[\[81\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=If%20using%20HTTP%2C%20the%20client,Version%20Header%20section%20in%20Transports). (See **Protocol Version Header** under Transports.)

**Capability Negotiation:** As part of initialization, client and server exchange capability objects to establish which optional protocol features will be available during the session[\[82\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Capability%20Negotiation). Key capabilities include[\[46\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Category%20Capability%20Description%20Client%20,standard%20experimental%20features):

| Category | Capability | Description |
| :---- | :---- | :---- |
| Client | roots | Ability to provide filesystem **roots** (list of directories)[\[83\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Category%20Capability%20Description%20Client%20,for%20LLM%20%2015%20requests) |
| Client | sampling | Support for LLM **sampling** requests[\[84\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Category%20Capability%20Description%20Client%20,Support%20for%20server%20elicitation%20requests) |
| Client | elicitation | Support for server-initiated **elicitation** requests[\[85\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Client%20,standard%20experimental%20features) |
| Client | experimental | Support for non-standard experimental features (client-defined)[\[86\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Client%20,standard%20experimental%20features) |
| Server | prompts | Offers **prompt templates** to the client[\[87\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,Exposes%20callable%20tools) |
| Server | resources | Provides readable **resources** (data context)[\[88\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,Emits%20structured%20%2023) |
| Server | tools | Exposes callable **tools**[\[89\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,Emits%20structured%20%2023) |
| Server | logging | Emits structured **log messages** to client[\[90\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,Supports%20argument%20%2025) |
| Server | completions | Supports argument **autocompletion** via the completion API[\[91\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,standard%20experimental%20features) |
| Server | experimental | Support for other experimental features (server-defined)[\[92\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,standard%20experimental%20features) |

Capability objects may describe sub-capabilities, such as[\[93\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Capability%20objects%20can%20describe%20sub,like):

* listChanged: support for “list changed” notifications (for prompts, resources, tools)

* subscribe: support for subscribing to individual item changes (for resources only)

**Operation:** During the operation phase, the client and server exchange messages according to the negotiated capabilities[\[94\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Operation). Both parties **MUST**:

* Respect the negotiated protocol version

* Only use capabilities that were successfully negotiated

(This effectively means no unsupported method calls or feature use should occur outside what was agreed upon in initialization.)

**Shutdown:** During the shutdown phase, one side (usually the client) cleanly terminates the protocol connection[\[95\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Shutdown). No specific MCP shutdown messages are defined – instead, the underlying transport’s mechanism is used to close the connection[\[96\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=During%20the%20shutdown%20phase%2C%20one,used%20to%20signal%20connection%20termination).

For **STDIO transport**, the client should initiate shutdown by[\[97\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=stdio): (1) closing the input stream to the server process, (2) waiting for the server process to exit (or sending SIGTERM if it does not exit in a reasonable time), and (3) sending SIGKILL if the server still does not exit after that[\[98\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=For%20the%20stdio%20transport%2C%20the,client%20SHOULD%20initiate%20shutdown%20by). The server may also initiate shutdown by closing its output stream and exiting[\[99\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=after%20).

For **HTTP transport**, shutdown is indicated by closing the HTTP connection(s) associated with the session[\[100\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=HTTP).

#### *Timeouts*

Implementations **SHOULD** establish timeouts for all requests, to prevent hung connections or resource exhaustion[\[101\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Timeouts). If a request has not received a success or error response within the timeout period, the sender **SHOULD** issue a cancellation notification for that request and stop waiting for a response[\[102\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Implementations%20SHOULD%20establish%20timeouts%20for,progress%20notifications%2C%20to%20limit%20the). (Clients/servers may reset the timeout when receiving a progress notification for that request, since that implies work is ongoing, but a maximum timeout should still be enforced to handle misbehaving peers)[\[103\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=SDKs%20and%20other%20middleware%20SHOULD,a%20misbehaving%20client%20or%20server).

#### *Error Handling (Lifecycle)*

Implementations **SHOULD** be prepared to handle error cases including[\[104\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Error%20Handling):

* Protocol version mismatch

* Failure to negotiate required capabilities

* Request timeouts

**Example – Initialization Error:** If negotiation fails (e.g. unsupported version), an error response might look like[\[105\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=):

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "error": {  
    "code": \-32602,  
    "message": "Unsupported protocol version",  
    "data": {  
      "supported": \["2024-11-05"\],  
      "requested": "1.0.0"  
    }  
  }  
}

### Transports

**Protocol Revision:** 2025-06-18[\[106\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Protocol%20Revision%3A%202025)

MCP uses JSON-RPC to encode messages. JSON-RPC messages **MUST** be UTF-8 encoded. The protocol currently defines two standard transport mechanisms for client–server communication[\[107\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=MCP%20uses%20JSON,server%20communication):

1. **stdio** – communication over standard input/output streams

2. **Streamable HTTP** – HTTP long-polling / SSE-based communication

Clients **SHOULD** support stdio whenever possible[\[108\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,Streamable%20HTTP). Clients and servers can also implement custom transports in a pluggable fashion (see “Custom Transports” below).

#### *stdio*

In the stdio transport[\[109\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=stdio):

* The client launches the MCP server as a subprocess.

* The server reads JSON-RPC messages from its standard input (stdin) and sends messages to its standard output (stdout).

* Messages are individual JSON-RPC requests, notifications, or responses, delimited by newlines (and **MUST NOT** contain embedded newlines within a message)[\[110\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=sends%20messages%20to%20its%20standard,MUST%20NOT%20contain%20embedded%20newlines).

* The server **MAY** write UTF-8 strings to its standard error (stderr) for logging; clients **MAY** capture or ignore this logging[\[111\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,is%20not%20a%20valid%20MCP).

* The server **MUST NOT** write anything to stdout that is not a valid MCP message (to avoid protocol confusion)[\[112\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,not%20a%20valid%20MCP%20message).

* The client **MUST NOT** write anything to the server’s stdin that is not a valid MCP message[\[113\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,not%20a%20valid%20MCP%20message).

**Sequence Diagram – stdio Transport:** The following diagram illustrates a typical stdio transport lifecycle:

sequenceDiagram  
    participant Client  
    participant Server\_Process  
    Client-\>\>+Server\_Process: Launch subprocess  
    loop Message Exchange   
        Client-\>\>Server\_Process: Write to stdin   
        Server\_Process--\>\>Client: Write to stdout   
        Server\_Process--) Client: (Optional logs on stderr)  
    end  
    Client-\>\>Server\_Process: Close stdin (terminate subprocess)  
    deactivate Server\_Process

#### *Streamable HTTP*

*(The Streamable HTTP transport replaces the older HTTP+SSE transport used in MCP version 2024-11-05[\[114\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=This%20replaces%20the%20HTTP%2BSSE%20transport,the%20backwards%20compatibility%20guide%20below). See* *Backwards Compatibility* *below.)*

In the Streamable HTTP transport, the server runs as an independent process that can handle multiple client connections[\[115\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=In%20the%20Streamable%20HTTP%20transport%2C,https%3A%2F%2Fexample.com%2Fmcp). This transport uses HTTP POST and GET requests. The server can optionally use **Server-Sent Events (SSE)**[\[116\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=that%20can%20handle%20multiple%20client,https%3A%2F%2Fexample.com%2Fmcp) to stream multiple messages to the client.

The server **MUST** provide a single HTTP endpoint (the *MCP endpoint*) that supports both POST and GET methods (e.g. https://example.com/mcp)[\[117\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Events%20en,https%3A%2F%2Fexample.com%2Fmcp).

**Security Warning:** When implementing Streamable HTTP[\[118\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Security%20Warning):

1. Servers **MUST** validate the Origin header on all incoming connections to prevent DNS rebinding attacks.

2. When running locally, servers **SHOULD** bind only to localhost (127.0.0.1) rather than all interfaces (0.0.0.0).

3. Servers **SHOULD** implement proper authentication for all connections.

Without these protections, attackers could use DNS rebinding to interact with local MCP servers from remote websites[\[119\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,proper%20authentication%20for%20all%20connections).

##### Sending Messages to the Server

Every JSON-RPC message from client to server is sent as a new HTTP POST to the MCP endpoint[\[120\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Sending%20Messages%20to%20the%20Server):

1. The client **MUST** use HTTP POST for JSON-RPC messages to the endpoint[\[121\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Every%20JSON,request%20to%20the%20MCP%20endpoint).

2. The client **MUST** include an Accept header indicating it can accept application/json and text/event-stream (for SSE)[\[122\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,202%20Accepted%20with%20no%20body).

3. The POST body **MUST** be a single JSON-RPC request, notification, or response[\[123\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=2,body%20MAY%20comprise%20a%20JSON).

4. If the input is a JSON-RPC **response** or **notification**:

5. If accepted, the server returns HTTP 202 Accepted with no body.

6. If not accepted, the server returns an HTTP error (e.g. 400 Bad Request). The response body **MAY** include a JSON-RPC error object (with no id)[\[124\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=4,client%20MUST%20support%20both%20these).

7. If the input is a JSON-RPC **request**, the server must either:

8. Return Content-Type: text/event-stream to initiate an SSE stream, **or**

9. Return Content-Type: application/json to send a single JSON response.  
   The client **MUST** support both cases[\[125\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=status%20code%20%28e,MUST%20support%20both%20these%20cases).

10. If the server initiates an SSE stream in response to a request[\[126\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=cases,request%2C%20unless%20the%20session%20expires):

11. The SSE stream **SHOULD** eventually include a JSON-RPC **response** for the original request.

12. The server **MAY** send JSON-RPC **requests** and **notifications** on the stream *before* sending the response (these messages should relate to the originating request).

13. The server **SHOULD NOT** close the SSE stream until it has sent the JSON-RPC response for the request (unless the session expires)[\[127\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,the%20server%20SHOULD%20close%20the).

14. After sending the JSON-RPC response, the server **SHOULD** close the SSE stream[\[128\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=request.%20,SHOULD%20close%20the%20SSE%20stream).

15. Disconnections **MAY** occur at any time (e.g. network issues). Therefore:

    * A disconnect **SHOULD NOT** be interpreted as the client canceling its request[\[129\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=SSE%20stream.%20,CancelledNotification). (To cancel, the client must explicitly send a Cancelled notification.)

    * To avoid message loss on disconnect, the server **MAY** make the stream *resumable* (see Resumability below)[\[130\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Therefore%3A%20,the%20server%20MAY%20make%20the).

##### Listening for Messages from the Server

1. The client **MAY** issue an HTTP GET to the MCP endpoint to open an SSE stream for server-\>client messages without a preceding client request[\[131\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,server%20initiates%20an%20SSE%20stream).

2. The client **MUST** include Accept: text/event-stream in this GET request[\[132\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,Method%20Not%20Allowed%2C%20indicating%20that).

3. The server must either:

4. Respond with Content-Type: text/event-stream (open SSE stream), **or**

5. Respond with HTTP 405 Method Not Allowed (indicating it doesn’t offer an SSE stream at that endpoint)[\[133\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=the%20client%20first%20sending%20data,RPC).

6. If an SSE stream is opened by the server[\[134\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=4,SSE%20stream%20at%20any%20time):

7. The server **MAY** send JSON-RPC **requests** and **notifications** on the stream.

8. These stream messages **SHOULD** be unrelated to any concurrently-running client request (i.e. truly server-initiated).

9. The server **MUST NOT** send a JSON-RPC **response** on this stream *unless* it is resuming a stream for a previous client request (see Resumability)[\[135\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,with%20a%20previous%20client%20request).

10. The server or client **MAY** close the SSE stream at any time[\[136\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,SSE%20stream%20at%20any%20time).

##### Multiple Connections

A client **MAY** have multiple SSE connections open to the server simultaneously[\[137\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Multiple%20Connections). The server **MUST** send each JSON-RPC message on exactly one stream (no broadcasting the same message on all streams)[\[138\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,by%20making%20the%20stream%20resumable). To mitigate message loss, streams may be made resumable (see below).

##### Resumability and Redelivery

To support resuming broken SSE connections and redelivering lost messages[\[139\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Resumability%20and%20Redelivery):

* Servers **MAY** attach an id field to SSE events as per the SSE standard[\[140\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,messages%20that%20would%20have%20been). If present, the ID must be globally unique across all streams in the session (or all streams per client, if no session management).

* If a client wants to resume after a break, it **SHOULD** reconnect with a GET and include the Last-Event-ID header with the last received event ID[\[141\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=2,delivered%20on%20a%20different%20stream).

* The server **MAY** use this to replay messages that came after that ID on the lost stream and resume from that point[\[142\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=an%20HTTP%20GET%20to%20the,delivered%20on%20a%20different%20stream).

* The server **MUST NOT** replay messages from a different stream (IDs are per-stream)[\[143\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,delivered%20on%20a%20different%20stream).

In other words, event IDs should be per stream, acting as a cursor for that stream’s messages[\[144\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=different%20stream).

##### Session Management

An MCP “session” consists of interactions between a client and server beginning with initialization[\[145\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Session%20Management). To support stateful sessions over HTTP:

1. A server using Streamable HTTP **MAY** assign a session ID during initialization, by including an Mcp-Session-Id header in its HTTP response to the Initialize request[\[146\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,Session).

2. The session ID should be globally unique and securely generated (e.g. a UUID or cryptographic random token).

3. The session ID must only contain visible ASCII characters (0x21 to 0x7E)[\[147\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=initialization%20time%2C%20by%20including%20it,of%20their%20subsequent%20HTTP%20requests).

4. If a session ID was provided by the server, the client **MUST** include it in an Mcp-Session-Id header on all subsequent HTTP requests[\[148\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=0x21%20to%200x7E%29,with%20HTTP%20404%20Not%20Found).

5. If the server requires a session ID and a request is missing it (after initialization), the server should respond with HTTP 400 Bad Request[\[149\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=clients%20using%20the%20Streamable%20HTTP,time%2C%20after%20which%20it%20MUST).

6. The server **MAY** terminate a session at any time (e.g. due to timeout); after termination it **MUST** respond to requests with that session ID with HTTP 404 Not Found[\[150\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,DELETE%20to%20the%20MCP%20endpoint).

7. If a client receives 404 Not Found for a request with a session ID, it **MUST** start a new session via a fresh Initialize (without a session ID)[\[151\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=respond%20to%20requests%20containing%20that,HTTP%20405%20Method%20Not%20Allowed).

8. If a client no longer needs a session (e.g. user closed app), it **SHOULD** send an HTTP DELETE to the MCP endpoint with the Mcp-Session-Id to explicitly terminate the session[\[152\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,allow%20clients%20to%20terminate%20sessions).

9. The server **MAY** respond to DELETE with HTTP 405 Method Not Allowed if it doesn’t allow client-initiated termination[\[153\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=leaving%20the%20client%20application,allow%20clients%20to%20terminate%20sessions).

*(In practice, sessions help maintain state like subscriptions or auth without requiring re-initialization each connection.)*

##### Sequence Diagram

*(The specification includes a sequence diagram illustrating a typical message flow for the Streamable HTTP transport. It shows client POST and GET requests, SSE streams, and reconnection with Last-Event-ID for resuming. This has been omitted here for brevity.)*

##### Protocol Version Header

For HTTP transports, after version negotiation the client **MUST** include an MCP-Protocol-Version: \<version\> HTTP header on all subsequent requests[\[154\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Protocol%20Version%20Header). For example: MCP-Protocol-Version: 2025-06-18. The version sent should be the one **negotiated during initialization**[\[155\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=If%20using%20HTTP%2C%20the%20client,server%20SHOULD%20assume%20protocol%20version).

For backwards compatibility, if a server doesn’t receive this header and cannot otherwise determine version (e.g. by context of session), it **SHOULD** assume 2025-03-26 (the previous version)[\[156\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=MCP%20server%20to%20respond%20based,400%20Bad%20Request). If the server receives an invalid or unsupported version in the header, it **MUST** respond with HTTP 400 Bad Request[\[157\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=the%20one%20negotiated%20during%20initialization,400%20Bad%20Request).

##### Backwards Compatibility

For compatibility with the **deprecated HTTP+SSE transport** (from version 2024-11-05)[\[158\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Clients%20and%20servers%20can%20maintain,to%20support%20older%20clients%20should):

* Servers that want to support older clients should continue to host the old SSE and POST endpoints alongside the new MCP endpoint[\[159\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=HTTP%2BSSE%20transport%20,to%20support%20older%20clients%20should). *(It is possible to combine the old POST endpoint and new endpoint, but that may add complexity.)*

* Clients that want to support older servers should[\[160\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Clients%20wanting%20to%20support%20older,servers%20should):

* Accept an MCP server URL from the user (which may point to either an old or new transport server).

* Attempt to POST an Initialize to the URL with the new Accept header;

  * If it succeeds, the server supports the new Streamable HTTP transport.

  * If it fails with a 4xx (e.g. 405 or 404), then:

  * Issue a GET to the URL, expecting it to open an SSE stream and send an endpoint event first[\[161\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,event%20as%20the%20first%20event).

  * When an endpoint event arrives, assume the server is running the old HTTP+SSE transport and use that for subsequent communication[\[162\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,transport%20for%20all%20subsequent%20communication).

##### Custom Transports

Clients and servers **MAY** implement additional custom transport mechanisms (e.g. WebSocket, Unix domain sockets, etc.) as needed. The protocol is transport-agnostic and can be implemented over any bidirectional channel that supports message exchange[\[163\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Custom%20Transports). However, custom transports **MUST** preserve the JSON-RPC message format and lifecycle requirements defined by MCP[\[164\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Clients%20and%20servers%20MAY%20implement,exchange%20patterns%20to%20aid%20interoperability). Custom transport implementors **SHOULD** document their connection establishment and message exchange patterns for interoperability[\[164\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Clients%20and%20servers%20MAY%20implement,exchange%20patterns%20to%20aid%20interoperability).

### Authorization

**Protocol Revision:** 2025-06-18[\[165\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Protocol%20Revision%3A%202025)

*(This section defines an OAuth2-based authorization flow for MCP over HTTP. It is* *OPTIONAL* *and only applicable if HTTP transport is used; STDIO transport does not use this.)*

#### *Introduction*

MCP’s authorization framework enables MCP clients to make requests to protected MCP servers on behalf of resource owners (end-users)[\[166\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=The%20Model%20Context%20Protocol%20provides,based%20transports). It defines how an *Authorization Server* issues tokens and how an MCP *Resource Server* (the MCP server) uses them to protect resources. This specification focuses on HTTP-based transports; STDIO implementations should not use this and can obtain credentials via other means[\[167\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Authorization%20is%20OPTIONAL%20for%20MCP,When%20supported).

The mechanism is based on OAuth 2.1 (latest draft) and related specs, implementing a subset to ensure security and interoperability with simplicity[\[168\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Standards%20Compliance). Notably:

* *OAuth 2.1 (IETF draft)*[\[169\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=interoperability%20while%20maintaining%20simplicity%3A)

* *OAuth 2.0 Authorization Server Metadata* (RFC 8414\)[\[170\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,RFC7591)

* *OAuth 2.0 Dynamic Client Registration* (RFC 7591\)[\[171\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,RFC7591)

* *OAuth 2.0 Protected Resource Metadata* (RFC 9728\)[\[172\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,0%20Protected%20Resource%20Metadata%20%28RFC9728)

#### *Purpose and Scope*

Authorization in MCP is **OPTIONAL**. When supported[\[167\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Authorization%20is%20OPTIONAL%20for%20MCP,When%20supported):

* HTTP-based transports **SHOULD** follow this spec (OAuth2 authorization flow).

* STDIO transports **SHOULD NOT** follow this spec (since STDIO cannot easily perform OAuth flows); they should get credentials from environment or config.

* Alternative transports **MUST** follow appropriate security best practices for authorization.

#### *Protocol Requirements*

*(Summarized above: basically that OAuth2 flows are used for HTTP when needed, etc.)*

#### *Standards Compliance*

This spec builds on established OAuth2 standards (listed above) but only uses a subset of their features, balancing security and simplicity[\[168\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Standards%20Compliance).

#### *Authorization Flow*

**Roles:** In this model[\[173\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Roles):

* The MCP **server** acts as an **OAuth 2.1 Resource Server**[\[173\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Roles), i.e. it serves protected resources and accepts access tokens.

* The MCP **client** acts as an **OAuth 2.1 Client**[\[174\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=A%20protected%20MCP%20server%20acts,It%20may%20be), obtaining tokens (on behalf of the user) and including them in requests to the MCP server.

* An **Authorization Server** issues access tokens for use at the MCP server. (Its implementation is out of scope; it could be co-hosted with the MCP server or separate.)

The *Authorization Server Discovery* mechanism allows an MCP server to indicate to clients where its auth server is[\[175\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=server%20is%20responsible%20for%20interacting,authorization%20server%20to%20a%20client).

**Overview of Flow:**[\[176\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Overview)

1. Authorization servers (AuthZ) must implement OAuth 2.1 with proper security for both confidential and public clients.

2. They (AuthZ) and MCP clients should support OAuth 2.0 Dynamic Client Registration (RFC 7591\)[\[177\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=1,0).

3. MCP servers must implement OAuth 2.0 Protected Resource Metadata (RFC 9728), and MCP clients must use it for discovery of the auth server[\[178\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=2,0%20Authorization%20Server%20Metadata).

4. Authorization servers must provide OAuth 2.0 Authorization Server Metadata (RFC 8414), and MCP clients must use it[\[179\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=3,0%20Authorization%20Server%20Metadata).

*(In essence: the MCP server advertises its auth server; the client uses standard OAuth discovery and possibly dynamic registration, then obtains tokens to include in requests.)*

#### *Authorization Server Discovery*

MCP servers use OAuth 2.0 Protected Resource Metadata (RFC 9728\) to advertise their authorization server(s)[\[180\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Authorization%20Server%20Location). An MCP server’s metadata document (at a known URL) includes an authorization\_servers field listing one or more auth server URIs[\[181\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20servers%20MUST%20implement%20the,lies%20with%20the%20MCP%20client). The client can pick one (if multiple) as per RFC 9728 Section 7.6[\[182\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Resource%20Metadata%20,MUST%20be%20able%20to%20parse). Additionally, when the MCP server returns an HTTP 401 Unauthorized, it **MUST** include a WWW-Authenticate header pointing to the resource server metadata URL (per RFC 9728 Section 5.1)[\[183\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=following%20the%20guidelines%20specified%20in,responses%20from%20the%20MCP%20server). MCP clients **MUST** parse WWW-Authenticate headers to find the auth server location[\[183\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=following%20the%20guidelines%20specified%20in,responses%20from%20the%20MCP%20server).

*(This allows the client to find the authorization server either via a known metadata URL or on encountering a 401 with appropriate header.)*

#### *Authorization Server Location*

*(Combined above with discovery: basically the location is obtained from authorization\_servers metadata or WWW-Authenticate response.)*

#### *Server Metadata Discovery*

Once the client knows the authorization server’s URL, it fetches the OAuth 2.0 Authorization Server Metadata (RFC 8414\)[\[184\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Server%20Metadata%20Discovery). This provides endpoints (token endpoint, auth endpoint, etc.) and capabilities of the auth server[\[184\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Server%20Metadata%20Discovery).

#### *Sequence Diagram*

The following diagram outlines an example OAuth authorization flow involving an MCP Client, an MCP Server (resource server), and an Authorization Server:

sequenceDiagram  
    participant C as Client  
    participant M as MCP Server (Resource Server)  
    participant A as Authorization Server  
    C-\>\>M: MCP request without token  
    M--\>\>C: HTTP 401 Unauthorized (WWW-Authenticate header with auth server URL)  
    Note over C,A: Authorization Code Grant (browser redirects, user login, etc.)  
    C-\>\>A: OAuth authorization request (client credentials or PKCE)  
    A--\>\>C: Authorization code (after user consents)  
    C-\>\>A: Token request (with authorization code)  
    A--\>\>C: Access token (and possibly refresh token)  
    C-\>\>M: Retry MCP request with \`Authorization: Bearer \<token\>\`  
    M--\>\>C: Protected resource response (success)

*(This mermaid diagram illustrates that the client, upon 401, interacts with the auth server to obtain a token, then retries with the token.)*

#### *Dynamic Client Registration*

MCP clients and auth servers **SHOULD** support OAuth 2.0 Dynamic Client Registration (RFC 7591\)[\[185\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Dynamic%20Client%20Registration). This allows the MCP client to obtain OAuth client credentials automatically, which is important because:  
\- Clients may not know all possible MCP servers and their auth servers in advance.  
\- Manual registration would be burdensome for users.  
\- It allows seamless connection to new servers.  
\- Auth servers can implement custom registration policies[\[186\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,implement%20their%20own%20registration%20policies).

If an authorization server does not support dynamic registration, it must provide alternative ways to obtain a client ID (and secret if needed). In such cases, the MCP client will either[\[187\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Any%20authorization%20servers%20that%20do,clients%20will%20have%20to%20either):  
1\. Have a hardcoded client ID (and secret, if applicable) for that auth server, **or**  
2\. Prompt the user to manually enter a client ID/secret after registering the client through some provided interface[\[188\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=to%20provide%20alternative%20ways%20to,clients%20will%20have%20to%20either).

*(In short, dynamic registration is preferred; otherwise, manual configuration is required.)*

#### *Authorization Flow Steps*

**Complete Flow:** The high-level steps of the OAuth authorization flow for MCP are as follows[\[189\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=The%20complete%20Authorization%20flow%20proceeds,as%20follows):

1. (Discovery) The MCP client finds the MCP server’s authorization server (via metadata or 401 header).

2. (Registration) The client ensures it has OAuth client credentials (dynamically registers if needed).

3. (Authorization) The client initiates an OAuth authorization code flow with the authorization server (possibly involving user consent).

4. (Token Exchange) The client obtains an access token (and possibly refresh token).

5. (API Request) The client includes the access token in its requests to the MCP server.

6. (Renewal) If the token expires, the client uses refresh token or repeats the flow as needed.

*(Steps like dynamic registration and use of refresh tokens are optional depending on support.)*

##### Resource Parameter Implementation

MCP clients **MUST** implement *Resource Indicators for OAuth 2.0* (RFC 8707\) by including a resource parameter in auth requests[\[190\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Resource%20Parameter%20Implementation). This explicitly specifies the target resource (the MCP server) for which the token is requested.

* The resource parameter **MUST** be included in both the authorization request and token request[\[191\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=which%20the%20token%20is%20being,parameter).

* It **MUST** identify the MCP server the token will be used with, using the **canonical URI** of the MCP server[\[192\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=1,in%20RFC%208707%20Section%202). According to RFC 8707, this is typically the base URL (scheme and host, possibly path) of the resource server.

**Canonical Server URI:** For MCP, the canonical URI of a server is its resource identifier (per RFC 8707 Section 2\)[\[193\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=For%20the%20purposes%20of%20this,Examples%20of%20valid%20canonical). MCP clients should use the most specific URI possible for the server, following RFC 8707 guidance[\[194\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=defined%20as%20the%20resource%20identifier,Examples%20of%20valid%20canonical%20URIs). (Lowercase scheme/host, etc. Trailing slash usage should be consistent but is not highly significant unless required by context[\[195\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,significant%20for%20the%20specific%20resource).)

**Examples of valid resource URIs**[\[196\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=in%20RFC%208707,Examples%20of%20valid%20canonical%20URIs):  
\- https://mcp.example.com/mcp  
\- https://mcp.example.com  
\- https://mcp.example.com:8443 (with port)  
\- https://mcp.example.com/server/mcp (if needed to identify a specific server instance)

**Invalid examples**[\[197\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Examples%20of%20invalid%20canonical%20URIs%3A):  
\- mcp.example.com (missing scheme)  
\- https://mcp.example.com\#fragment (contains a fragment)

*Note:* Both https://mcp.example.com/ (with slash) and https://mcp.example.com (no slash) are technically valid; implementations should consistently use one form (preferably without trailing slash) unless a slash is semantically significant[\[198\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=%2A%20%60https%3A%2F%2Fmcp.example.com).

For instance, if the MCP server is at https://mcp.example.com, the authorization request would include \&resource=https%3A%2F%2Fmcp.example.com (URL-encoded)[\[199\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=For%20example%2C%20if%20accessing%20an,the%20authorization%20request%20would%20include). MCP clients **MUST** send the resource parameter *regardless* of whether the auth server explicitly supports it[\[200\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20clients%20MUST%20send%20this,whether%20authorization%20servers%20support%20it). This ensures token audience binding (explained below).

*(In summary, including resource=\<MCP-server-URI\> in token requests is mandatory.)*

#### *Access Token Usage*

Once an access token is obtained, every HTTP request from client to server must include it.

##### Token Requirements

When making requests to MCP servers, access token usage must conform to OAuth 2.1 resource request requirements[\[201\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Token%20Requirements). Specifically[\[202\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=1,1):

* The MCP client **MUST** use the HTTP Authorization header with scheme Bearer to present the access token (per OAuth 2.1 Sec 5.1.1)[\[202\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=1,1):

**Example:**  
http Authorization: Bearer \<access-token\>[\[202\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=1,1)

* The Authorization header (with Bearer token) **MUST** be included in **every** HTTP request from client to server, even within a persistent session[\[203\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Authorization%3A%20Bearer%20%3Caccess). (No assumption that earlier token applies to later requests without sending it each time.)

* Access tokens **MUST NOT** be included in URI query parameters[\[204\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Note%20that%20authorization%20MUST%20be,of%20the%20same%20logical%20session) (to avoid leaks in logs, etc.).

**Example HTTP request with token:**[\[205\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Example%20request%3A)

GET /mcp HTTP/1.1  
Host: mcp.example.com  
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...\<token\>...

##### Token Handling

On the server side, MCP servers (as OAuth resource servers) **MUST** validate access tokens as described in OAuth 2.1 (draft) Sec 5.2[\[206\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20servers%2C%20acting%20in%20their,MUST%20NOT%20accept%20or%20transit). They must ensure tokens were issued specifically for them (intended audience), following RFC 8707 guidelines[\[207\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=access%20tokens%20as%20described%20in,MUST%20NOT%20accept%20or%20transit). If validation fails, servers must return appropriate errors per OAuth 2.1 Sec 5.3 (401 for invalid/expired tokens, etc.)[\[208\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=as%20the%20intended%20audience%2C%20according,MUST%20NOT%20accept%20or%20transit). Specifically[\[209\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=as%20the%20intended%20audience%2C%20according,or%20transit%20any%20other%20tokens):

* Invalid or expired tokens **MUST** get an HTTP 401 Unauthorized.

* Clients **MUST NOT** send tokens to an MCP server that weren’t issued by that server’s auth server.

* Authorization servers **MUST** only issue tokens valid for their own resources.

* MCP servers **MUST NOT** accept or forward any tokens not intended for themselves.

*(This again is about token audience restriction – see Security Considerations below.)*

#### *Error Handling (Authorization)*

Servers should use proper HTTP status codes for authorization errors[\[210\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Error%20Handling):

* **401 Unauthorized:** when authentication is required or token is invalid.

* **403 Forbidden:** when token is valid but insufficient scope/permission.

* **400 Bad Request:** for malformed auth requests (e.g. missing token format).

These follow standard OAuth 2.1 error handling.

### Security Considerations (Authorization)

Implementations **MUST** follow OAuth 2.1 security best practices (see OAuth 2.1 Sec 7\)[\[211\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Security%20Considerations). Key points:

#### *Token Audience Binding and Validation*

Resource Indicators (RFC 8707\) bind tokens to their intended audience. MCP clients **MUST** always include resource in token requests, and MCP servers **MUST** validate that incoming tokens were issued for them[\[212\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=RFC%208707%20Resource%20Indicators%20provide,enable%20current%20and%20future%20adoption). (Token passthrough is explicitly forbidden – explained shortly.) This ensures tokens cannot be reused maliciously across different services.

*(A separate “Security Best Practices” document goes into detail on why audience validation is crucial and token passthrough is disallowed[\[213\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=issued%20for%20their%20use).)*

#### *Token Theft*

If an attacker obtains a token (from the client’s storage or server’s cache/logs), they could use it to impersonate the user at the resource server[\[214\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Attackers%20who%20obtain%20tokens%20stored,1%20%E2%80%9CToken%20Endpoint%20Extension%E2%80%9D). Thus:  
\- Clients and servers **MUST** implement secure storage for tokens and follow OAuth best practices (e.g. short-lived access tokens, rotating refresh tokens for public clients)[\[214\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Attackers%20who%20obtain%20tokens%20stored,1%20%E2%80%9CToken%20Endpoint%20Extension%E2%80%9D).  
\- Authorization servers **SHOULD** issue short-lived tokens to limit their usefulness if stolen[\[215\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=to%20resource%20servers,1%20%E2%80%9CToken%20Endpoint%20Extension%E2%80%9D).  
\- For public clients, authorization servers **MUST** rotate refresh tokens per OAuth 2.1 Section 4.3.1 (to prevent reuse)[\[216\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=follow%20OAuth%20best%20practices%2C%20as,1%20%E2%80%9CToken%20Endpoint%20Extension%E2%80%9D).

#### *Communication Security*

All auth server endpoints **MUST** use HTTPS (TLS)[\[217\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Communication%20Security). Redirect URIs must either be localhost or use HTTPS[\[218\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Implementations%20MUST%20follow%20OAuth%202,Specifically). (No plain HTTP for token or auth flows.)

#### *Authorization Code Protection*

Authorization codes can be intercepted by attackers if not protected, leading to token theft[\[219\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Authorization%20Code%20Protection). MCP clients **MUST** implement PKCE (Proof Key for Code Exchange) as per OAuth 2.1 Sec 7.5.2[\[220\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=token%20or%20otherwise%20make%20use,requestor%20can%20exchange%20an%20authorization). This mitigates interception by requiring a code verifier.

#### *Open Redirection*

Open redirectors can be abused in OAuth flows to send users to malicious sites. MCP clients **MUST** register redirect URIs and auth servers **MUST** strictly validate them against what’s registered[\[221\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Open%20Redirection). Clients **SHOULD** use state parameters and verify them on response[\[222\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=An%20attacker%20may%20craft%20malicious,Authorization%20servers%20SHOULD%20only%20automatically). Auth servers **MUST** prevent redirecting to untrusted URIs (OAuth 2.1 Sec 7.12.2)[\[223\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=parameters%20in%20the%20authorization%20code,to%20make%20the%20correct%20decision).

#### *Confused Deputy Problem*

This is a scenario where an MCP server (acting as an OAuth client to a third-party API) could be tricked into obtaining tokens not meant for it, due to static client IDs and reusing user consent cookies[\[224\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Confused%20Deputy%20Problem)[\[225\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Attack%20Description). To mitigate: if an MCP server proxies to third-party APIs with a static client ID, it **MUST** obtain user consent for each third-party integration and generally avoid skipping consent due to prior cookies[\[226\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=MCP%20proxy%20servers%20using%20static,which%20may%20require%20additional%20consent). (Detailed attack example omitted for brevity.)

*(In summary: ensure the user explicitly consents when an MCP server uses one client ID to access multiple user accounts on a third-party auth, to avoid silent token issuance with stale consent.)*

#### *Access Token Privilege Restriction*

If an MCP server accepts tokens that were not specifically issued for it (audience not checked) or even forwards them to other services, major vulnerabilities arise[\[227\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Access%20Token%20Privilege%20Restriction)[\[228\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20servers%20MUST%20validate%20access,Practices%20Token%20Passthrough%20section%20for):

1. **Audience validation failure:** Accepting tokens for other services breaks OAuth’s trust boundaries[\[229\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=two%20critical%20dimensions%3A). Attackers could reuse a token from Service A on Service B.

2. **Token passthrough:** If an MCP server not only accepts tokens with wrong audience but also passes them to downstream APIs, it becomes a confused deputy allowing illegitimate access[\[230\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=2,Practices%20guide%20for%20additional%20details).

Therefore, MCP servers **MUST** validate tokens before using them (only accept if they are intended for itself)[\[231\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20servers%20MUST%20validate%20access,it%20may%20act%20as%20an). MCP servers **MUST** reject tokens that do not list the server as an intended audience, and never forward a client’s token to other services[\[232\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=server%20MUST%20follow%20the%20guidelines,MCP%20clients%20MUST%20implement). If an MCP server calls upstream APIs, it should obtain a separate token from that upstream’s auth (acting as its own client), rather than reusing the user’s token[\[233\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=token,This%20requirement%20aligns%20with). MCP clients **MUST** use the resource parameter as discussed to make these audience restrictions possible[\[234\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=OAuth%20client%20to%20them,be%20misused%20across%20different%20services) (and this aligns with RFC 9728 Sec 7.4 recommendations).

*(See the Security Best Practices guide’s section on “Token Passthrough” for more details[\[230\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=2,Practices%20guide%20for%20additional%20details).)*

### Security Best Practices (Guide)

*(This section is a supplementary document focusing on known security risks and mitigations. It is not normative but strongly recommended reading for implementors.)*

**Purpose and Scope:** This guide identifies security risks, attack vectors, and best practices specific to MCP implementations, particularly around authorization flows and token handling. It is intended for developers and security reviewers, and should be read alongside the main Authorization spec and general OAuth 2.0 security guidance[\[235\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=This%20document%20provides%20security%20considerations,0%20security%20best%20practices).

#### *Attacks and Mitigations*

Several attack scenarios are considered:

##### Confused Deputy Problem (Revisited)

If an MCP server proxies requests to a third-party API using a static OAuth client ID, an attacker can exploit a previously given user consent to gain access without new consent[\[225\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Attack%20Description). (Scenario: user consents once to static ID; attacker crafts an auth request for a malicious redirect, uses existing consent cookie so user isn’t prompted, gets auth code, obtains token for MCP server without user realizing[\[236\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=When%20an%20MCP%20proxy%20server,the%20following%20attack%20becomes%20possible)[\[237\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=dynamically%20registered%20client%20ID%204,without%20the%20user%E2%80%99s%20explicit%20approval)). Then attacker can call third-party API with the user’s token[\[238\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=,API%20as%20the%20compromised%20user).

**Mitigation:** MCP proxy servers using static client IDs **MUST** require user consent for each dynamically registered client before forwarding to third-party auth servers[\[239\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=MCP%20proxy%20servers%20using%20static,which%20may%20require%20additional%20consent). In practice, ensure even if a third-party auth sees an existing consent cookie, the MCP server still asks the user to confirm linking the new dynamic client (or uses separate client IDs per user to avoid shared consent).

##### Token Passthrough

“Token passthrough” means an MCP server accepts a token from the client and directly uses it to call another service without validating or exchanging it[\[240\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Token%20Passthrough). This is explicitly forbidden in MCP[\[241\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Risks) because it can bypass important security controls:

* **Circumvention of controls:** Downstream APIs might rely on audience or role restrictions in tokens. If tokens are passed through, those controls are bypassed[\[242\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=,Accountability%20and%20Audit%20Trail%20Issues).

* **Audit trail issues:** The MCP server cannot identify which client (user) made a request if the token was not minted for the MCP server, and downstream logs will show the wrong source[\[243\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=service%2C%20they%20bypass%20these%20controls,is%20actually%20forwarding%20the%20tokens). This hampers incident response[\[244\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=service%2C%20they%20bypass%20these%20controls,investigation%2C%20controls%2C%20and%20auditing%20more).

* **Proxy for stolen tokens:** If an attacker steals a token, they could use the MCP server as a proxy to exfiltrate data, since the MCP server might forward the token blindly[\[245\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=server%20that%20is%20actually%20forwarding,Trust%20Boundary%20Issues).

* **Trust boundary issues:** Downstream services trust tokens from specific issuers. Accepting and forwarding tokens across boundaries breaks that trust model[\[246\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=,it%20might%20need%20to%20add).

* **Future compatibility risk:** If an MCP server starts as a pure proxy but later needs to enforce security controls, having proper audience separation from the start makes it easier[\[247\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=,to%20evolve%20the%20security%20model).

**Mitigation:** MCP servers **MUST NOT** accept tokens not explicitly issued for them[\[248\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Mitigation). (So if an access token doesn’t list the MCP server as audience, reject it. And never pass tokens through unvalidated.)

*(In summary, always perform token exchange or separate auth when bridging to other services instead of blindly forwarding user tokens.)*

##### Session Hijacking

If an attacker obtains an MCP session ID, they could impersonate the legitimate client on that session[\[249\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Session%20Hijacking). Two attack variants are considered: *Prompt Injection* and *Impersonation*.

* *Session Hijack Prompt Injection:* If multiple stateless servers share a queue, an attacker could inject an event with a stolen session ID into another server’s queue, causing the legitimate server to send a malicious payload to the client as if it were part of an ongoing session[\[250\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=When%20you%20have%20multiple%20stateful,possible%3A%20Session%20Hijack%20Prompt%20Injection)[\[251\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=affect%20the%20tools%20that%20are,malicious%20payload%2C%20leading%20to%20potential). For example, terminating a connection and resuming on another server might allow this if session IDs aren’t bound to user.

* *Session Hijack Impersonation:* If an attacker just uses a stolen session ID to directly call the MCP server’s endpoints, and the server doesn’t further verify identity, the attacker can perform actions as the user[\[252\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Session%20Hijack%20Impersonation).

**Mitigations:**[\[253\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Mitigation)  
\- MCP servers with authorization **MUST** verify all inbound requests (i.e. require valid auth tokens in addition to session ID).  
\- MCP servers **MUST NOT** use sessions as the sole means of authentication (don’t treat possession of session ID as identity).  
\- Session IDs must be secure, non-guessable, and tied to user context. Use strong random values (UUIDs, cryptographically random)[\[254\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=verify%20all%20inbound%20requests,ensures%20that%20even%20if%20an). Avoid predictable IDs.  
\- Consider rotating or expiring session IDs regularly[\[255\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Generated%20session%20IDs%20%28e,ensures%20that%20even%20if%20an).  
\- Servers **SHOULD** bind session IDs to user-specific info (e.g. include a user identifier in the session key or in stored session state)[\[256\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=attacker,optionally%20leverage%20additional%20unique%20identifiers). For example, store sessions as \<user\_id\>:\<session\_id\> so that even if an attacker guesses a session ID, they cannot use it unless they also have the corresponding user’s credentials/token[\[256\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=attacker,optionally%20leverage%20additional%20unique%20identifiers).

*(By combining session ID with user-specific secret, you ensure session ID alone isn’t enough to hijack.)*

## Client Features

### Roots

**Protocol Revision:** 2025-06-18[\[257\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Protocol%20Revision%3A%202025)

The MCP provides a standardized way for clients to expose filesystem “**roots**” to servers[\[258\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=The%20Model%20Context%20Protocol%20,notifications%20when%20that%20list%20changes). *Roots* define the boundaries of where servers can operate in the filesystem, allowing servers to know which directories/files they have access to. Servers can request the list of roots from supporting clients and receive notifications when that list changes[\[258\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=The%20Model%20Context%20Protocol%20,notifications%20when%20that%20list%20changes).

#### *User Interaction Model*

Roots are typically exposed through workspace or project selection UIs[\[259\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=User%20Interaction%20Model). For example, an implementation might show a workspace picker that lets the user choose directories/files the server can access. Some may auto-detect projects (via git repositories or project files). The protocol does not mandate a specific UI – implementations can choose any pattern suitable to their app[\[260\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Roots%20in%20MCP%20are%20typically,any%20specific%20user%20interaction%20model).

#### *Capabilities*

Clients that support roots **MUST** declare the roots capability during initialization[\[261\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Capabilities). For example, a client advertises support with an object indicating any sub-capabilities:

{  
  "capabilities": {  
    "roots": {  
      "listChanged": true  
    }  
  }  
}

Here, listChanged: true indicates the client will send notifications when the list of roots changes[\[262\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=).

#### *Protocol Messages*

**Listing Roots:** To retrieve the list of roots, the server sends a roots/list request[\[263\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Listing%20Roots).

* **Request:** {"jsonrpc":"2.0", "id":X, "method":"roots/list"}[\[264\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=To%20retrieve%20roots%2C%20servers%20send,request%3A%20Request)

* **Response:** The client responds with a list of roots. Example[\[265\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Response%3A):

{  
  "jsonrpc": "2.0",  
  "id": X,  
  "result": {  
    "roots": \[  
      {  
        "uri": "file:///home/user/projects/myproject",  
        "name": "My Project"  
      }  
    \]  
  }  
}

**Root List Changes:** If roots change (e.g. user adds/removes a workspace), a client that supports listChanged **MUST** send a notifications/roots/list\_changed notification[\[266\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Root%20List%20Changes):

{  
  "jsonrpc": "2.0",  
  "method": "notifications/roots/list\_changed"  
}

*(No params are needed; the server should then call roots/list again to get the new list.)*

#### *Data Types*

**Root:** Each root is defined by[\[267\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Root):

* uri – a unique identifier (must be a file:// URI in the current spec)[\[268\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=A%20root%20definition%20includes%3A).

* name – an optional human-readable name for display[\[269\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=A%20root%20definition%20includes%3A).

**Example:** A project directory root[\[270\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Project%20Directory):

{  
  "uri": "file:///home/user/projects/myproject",  
  "name": "My Project"  
}

**Multiple Repositories Example:** A list of roots could contain multiple entries[\[271\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Multiple%20Repositories):

\[  
  {  
    "uri": "file:///home/user/repos/frontend",  
    "name": "Frontend Repository"  
  },  
  {  
    "uri": "file:///home/user/repos/backend",  
    "name": "Backend Repository"  
  }  
\]

#### *Error Handling*

If a server requests roots but the client doesn’t support it (or fails), the client should return standard JSON-RPC errors[\[272\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Error%20Handling). Typical errors:

* If client does not support roots: error code \-32601 (Method not found)[\[273\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Clients%20SHOULD%20return%20standard%20JSON,errors%20for%20common%20failure%20cases).

* Internal errors: \-32603 (Internal error).

**Example:** If roots are not supported[\[274\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=,32603):

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "error": {  
    "code": \-32601,  
    "message": "Roots not supported",  
    "data": {  
      "reason": "Client does not have roots capability"  
    }  
  }  
}

#### *Security Considerations*

1. Clients **MUST** only expose roots that the user has permitted, and should validate all root URIs to prevent path traversal or unauthorized access[\[275\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Security%20Considerations). Appropriate access controls must be in place, and root accessibility should be monitored.

2. Servers **SHOULD** handle cases where a previously available root becomes unavailable (e.g. network drive unmounted) and always respect the root boundaries during any operation[\[276\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=,all%20paths%20against%20provided%20roots). Any file paths used by the server should be validated against the provided roots.

#### *Implementation Guidelines*

* Clients **SHOULD** prompt users for consent before exposing any root to a server[\[277\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=1.%20Clients%20SHOULD%3A%20,Respect%20root%20boundaries%20in%20operations). They should provide UI for managing roots (adding/removing) and ensure each root is accessible (exists, etc.) before advertising it[\[277\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=1.%20Clients%20SHOULD%3A%20,Respect%20root%20boundaries%20in%20operations). They should also monitor roots for changes (if the underlying file is moved, etc.).

* Servers **SHOULD** always check if the client declared roots capability before attempting to use roots, and handle list\_changed notifications gracefully (e.g. refresh their cached list of roots)[\[278\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=1.%20Clients%20SHOULD%3A%20,Handle%20root%20list%20changes%20gracefully).

### Sampling

**Protocol Revision:** 2025-06-18[\[279\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Protocol%20Revision%3A%202025)

MCP provides a standardized way for servers to request LLM **sampling** (generations/completions) via the client[\[280\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=The%20Model%20Context%20Protocol%20,MCP%20servers%20in%20their%20prompts). This allows servers to trigger LLM calls (text, audio, or image completions) while the client retains control over model access, selection, and permissions[\[280\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=The%20Model%20Context%20Protocol%20,MCP%20servers%20in%20their%20prompts). The server does *not* need its own API key for the model; it leverages the client’s connection to an LLM.

#### *User Interaction Model*

Sampling allows servers to implement *agentic behaviors*, i.e. making LLM calls nested within other operations[\[281\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=User%20Interaction%20Model). Importantly, **there should always be a human in the loop** with the ability to approve or deny sampling requests for trust & safety[\[282\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=For%20trust%20%26%20safety%20and,Applications%20SHOULD). Applications **SHOULD**[\[282\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=For%20trust%20%26%20safety%20and,Applications%20SHOULD):

* Provide a UI for users to review sampling requests (e.g. a prompt asking for permission to proceed).

* Allow users to view and edit the prompt that will be sent to the model before it’s sent.

* Optionally present the generated response to the user for approval before it’s delivered back to the server.

*(This ensures users maintain oversight over any AI-generated content or actions.)*

#### *Capabilities*

Clients that support sampling **MUST** declare the sampling capability during initialization[\[283\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Capabilities):

{  
  "capabilities": {  
    "sampling": {}  
  }  
}

*(No sub-fields are needed; presence of the object indicates support.)*

#### *Protocol Messages*

**Creating Messages (Sampling Request):** To request an LLM generation, the server sends a sampling/createMessage request[\[284\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Creating%20Messages).

* **Request:** The server provides the conversation context, model preferences, etc.[\[284\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Creating%20Messages). For example:

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "method": "sampling/createMessage",  
  "params": {  
    "messages": \[  
      {  
        "role": "user",  
        "content": {  
          "type": "text",  
          "text": "What is the capital of France?"  
        }  
      }  
    \],  
    "modelPreferences": {  
      "hints": \[ { "name": "claude-3-sonnet" } \],  
      "intelligencePriority": 0.8,  
      "speedPriority": 0.5  
    },  
    "systemPrompt": "You are a helpful assistant.",  
    "maxTokens": 100  
  }  
}

In this example[\[285\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=,)[\[286\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=%5D%2C%20,0.5):  
\- The conversation has one user message asking a question.  
\- modelPreferences suggests a preference for the "claude-3-sonnet" model with certain priorities (more on this below).  
\- A systemPrompt is provided (acts as an AI system instruction).  
\- maxTokens is the maximum tokens to generate.

* **Response:** The client, after possibly showing the prompt to the user and invoking the LLM, returns a result or error. A successful result looks like[\[287\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Response%3A)[\[288\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=,20240307%22%2C%20%22stopReason%22%3A%20%22endTurn%22%20%7D):

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "result": {  
    "role": "assistant",  
    "content": {  
      "type": "text",  
      "text": "The capital of France is Paris."  
    },  
    "model": "claude-3-sonnet-20240307",  
    "stopReason": "endTurn"  
  }  
}

Here, the assistant’s reply is provided, along with the model that was used and a stop reason (end of turn)[\[289\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=,20240307%22%2C%20%22stopReason%22%3A%20%22endTurn%22).

*(If the user denied the request or something went wrong, an error would be returned instead, e.g. code \-1 with message "User rejected sampling request".)*

#### *Message Flow*

*(Not explicitly described here, but basically the server requests a completion, the client may prompt user and then perform it, and returns the answer. The client should not allow the server to directly call the model without user oversight.)*

#### *Data Types*

**Messages:** A sampling message (similar to chat message) contains[\[290\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Messages):  
\- role: "user" or "assistant" (who said the message)[\[291\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=%7B%20,to%20any%20Claude%20model).  
\- content: which can be text, image, or audio.

**Text Content:** Example[\[292\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=):

{ "type": "text", "text": "The message content" }

**Image Content:** Example[\[293\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Image%20Content):

{   
  "type": "image",  
  "data": "base64-encoded-image-data",  
  "mimeType": "image/jpeg"  
}

**Audio Content:** Example[\[294\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Audio%20Content):

{   
  "type": "audio",  
  "data": "base64-encoded-audio-data",  
  "mimeType": "audio/wav"  
}

*(The client will handle actually converting image/audio data if needed for the model API.)*

**Model Preferences:** Because servers and clients might use different AI providers or models, a server cannot simply specify an exact model name and assume the client has it. Instead, MCP uses a preference system with numeric priorities and optional *hints*[\[295\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Model%20Preferences).

* **Capability Priorities:** Servers express their needs via three priority values (0.0 to 1.0)[\[296\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Capability%20Priorities):

* costPriority – importance of minimizing cost (higher \= prefer cheaper models).

* speedPriority – importance of low latency (higher \= prefer faster models).

* intelligencePriority – importance of advanced capabilities (higher \= prefer more capable models even if slower/expensive).

* **Model Hints:** In addition to or instead of numeric priorities, servers can provide hints (suggestions) for model selection[\[297\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Model%20Hints). Hints are treated as substrings to match model names. Multiple hints are evaluated in order, and the client may map hints to equivalent models from other providers[\[298\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=While%20priorities%20help%20select%20models,specific%20models%20or%20model%20families). They are advisory; the client makes the final selection[\[299\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=,advisory%E2%80%94clients%20make%20final%20model%20selection).

**Example Model Preferences with hints:**[\[300\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Copy)

{  
  "hints": \[  
    { "name": "claude-3-sonnet" },   // prefer Sonnet-class Claude model  
    { "name": "claude" }            // fall back to any Claude model  
  \],  
  "costPriority": 0.3,  
  "speedPriority": 0.8,  
  "intelligencePriority": 0.5  
}

The client would try to satisfy these by, say, picking a Claude model if available; if not, maybe mapping "sonnet" to an equivalent from another provider (e.g. Anthropic’s Claude vs. an OpenAI model)[\[301\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=The%20client%20processes%20these%20preferences,pro%60%20based%20on%20similar%20capabilities). These preferences are always hints – the client can ignore or interpret them as it sees fit for the user’s settings[\[301\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=The%20client%20processes%20these%20preferences,pro%60%20based%20on%20similar%20capabilities).

#### *Error Handling*

Clients **SHOULD** return errors for common failure cases (like user declined, or model error). For instance, if the user rejects the sampling request, the client might respond with an error:

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "error": {  
    "code": \-1,  
    "message": "User rejected sampling request"  
  }  
}

(This is not a standard JSON-RPC error code, but an application-level code indicating the request was not fulfilled due to user action.)

#### *Security Considerations*

1. Clients **SHOULD** implement user approval for any sampling – never allow a server to trigger an LLM call without user knowledge.

2. Both clients and servers **SHOULD** validate the content of messages (e.g. no obviously malicious or disallowed content is being sent to the model, depending on safety policies).

3. Clients **SHOULD** respect model preference hints as much as practical, but not at the expense of safety or user settings.

4. Clients **SHOULD** implement rate limiting on sampling requests to prevent abuse (e.g. a server attempting to spam the model with requests).

5. Both parties **MUST** handle sensitive data carefully – e.g. if a server asks the model something containing user data, ensure the user is aware.

*(In short, sampling requests should be treated with the same caution as if the user themselves were initiating an AI query, with oversight and controls in place.)*

### Elicitation

**Protocol Revision:** 2025-06-18[\[302\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Protocol%20Revision%3A%202025)

*Elicitation* is a feature (introduced in this version) that allows servers to request additional information from the user via the client[\[303\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Elicitation%20is%20newly%20introduced%20in,evolve%20in%20future%20protocol%20versions). It’s a way for servers to say: "I need the user to provide X" in the middle of an interaction. The client will then prompt the user and return the response. This feature lets servers gather necessary information dynamically while the client ensures the user remains in control of what data is shared[\[304\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=The%20Model%20Context%20Protocol%20,JSON%20schemas%20to%20validate%20responses).

*(For example, a server might need an API key from the user to proceed, or ask the user a disambiguation question.)*

#### *User Interaction Model*

Elicitation allows interactive workflows: a server can, during an operation, ask the user for input through the client[\[305\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=User%20Interaction%20Model). The user will see a prompt (likely generated by the server) and can respond or cancel. Implementations can use any UI pattern to get user input (modal dialog, chat prompt, form, etc.). The protocol itself doesn’t mandate UI specifics[\[306\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Elicitation%20in%20MCP%20allows%20servers,any%20specific%20user%20interaction%20model).

**Security Note:** Servers **MUST NOT** abuse elicitation to ask for sensitive info (passwords, tokens, etc.)[\[307\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=For%20trust%20%26%20safety%20and,security). Clients should enforce this by design/permission, and users should always have the option to decline or cancel.

Applications **SHOULD**[\[308\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=,elicitation%20to%20request%20sensitive%20information):

* Clearly indicate which server is asking for information (so the user knows who will receive it).

* Allow users to review/modify their response before sending.

* Provide obvious options to decline or cancel the request.

#### *Capabilities*

Clients that support elicitation **MUST** declare the elicitation capability during initialization[\[309\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Capabilities):

{  
  "capabilities": {  
    "elicitation": {}  
  }  
}

*(No subfields — its presence indicates support.)*

#### *Protocol Messages*

**Creating Elicitation Requests:** The server initiates by sending an elicitation/create request to the client[\[310\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Creating%20Elicitation%20Requests).

* **Request:** Contains a user-facing message and a JSON Schema for the data being requested[\[311\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=To%20request%20information%20from%20a,request). For example:

**Simple text request example:**[\[312\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Simple%20Text%20Request)

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "method": "elicitation/create",  
  "params": {  
    "message": "Please provide your GitHub username",  
    "requestedSchema": {  
      "type": "object",  
      "properties": {  
        "name": { "type": "string" }  
      },  
      "required": \["name"\]  
    }  
  }  
}

This asks the client to prompt the user with "Please provide your GitHub username" and expects an object with a string property "name".

**Structured data request example:**[\[313\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Structured%20Data%20Request)[\[314\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=,)

{  
  "jsonrpc": "2.0",  
  "id": 2,  
  "method": "elicitation/create",  
  "params": {  
    "message": "Please provide your contact information",  
    "requestedSchema": {  
      "type": "object",  
      "properties": {  
        "name": {  
          "type": "string",  
          "description": "Your full name"  
        },  
        "email": {  
          "type": "string",  
          "format": "email",  
          "description": "Your email address"  
        },  
        "age": {  
          "type": "number",  
          "minimum": 18,  
          "description": "Your age"  
        }  
      },  
      "required": \["name", "email"\]  
    }  
  }  
}

Here the server asks for contact info with a schema: an object containing name (string), email (string with email format), and age (number, must be \>= 18), with name and email required.

* **Response:** The client (after potentially showing a form to the user) responds with one of three outcomes[\[315\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Response%3A)[\[316\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Reject%20Response%20Example%3A):

* **Accept:** User provided the requested data. The result will have action: "accept" and a content object with the data.

* **Decline:** User explicitly refused. The result has action: "decline" and typically no content.

* **Cancel:** User dismissed the request (did not explicitly answer or decline). Result has action: "cancel".

**Example responses:**

– Accept example[\[317\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Copy) (for the GitHub username request, say the user enters "octocat"):

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "result": {  
    "action": "accept",  
    "content": {  
      "name": "octocat"  
    }  
  }  
}

– Accept example for structured request (user provided all fields)[\[318\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=%7B%20,30):

{  
  "jsonrpc": "2.0",  
  "id": 2,  
  "result": {  
    "action": "accept",  
    "content": {  
      "name": "Monalisa Octocat",  
      "email": "\[email protected\]",  
      "age": 30  
    }  
  }  
}

– Decline example[\[316\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Reject%20Response%20Example%3A):

{  
  "jsonrpc": "2.0",  
  "id": 2,  
  "result": {  
    "action": "decline"  
  }  
}

– Cancel example[\[319\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Cancel%20Response%20Example%3A):

{  
  "jsonrpc": "2.0",  
  "id": 2,  
  "result": {  
    "action": "cancel"  
  }  
}

The server should handle each case appropriately (if accept, use the data; if decline or cancel, perhaps abort or try an alternative path).

*(Notably: The content is only present for action "accept".)*

#### *Message Flow*

The typical flow: 1\. Server sends elicitation/create with message & schema. 2\. Client shows user prompt (like a form or input dialog). 3\. User submits (or declines/cancels). 4\. Client returns result as above. 5\. Server receives the result and continues accordingly (if accept, uses provided info; if decline/cancel, maybe halts or goes with default behavior).

#### *Request Schema*

The requestedSchema field in the request is a restricted JSON Schema that defines the expected structure of the user’s response[\[320\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Request%20Schema). To simplify client implementation, the schema is limited to **flat objects with primitive properties** only (no nested objects/arrays)[\[321\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=The%20,objects%20with%20primitive%20properties%20only).

Example snippet from requestedSchema format[\[322\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Copy):

"requestedSchema": {  
  "type": "object",  
  "properties": {  
    "propertyName": {  
      "type": "string",  
      "title": "Display Name",  
      "description": "Description of the property"  
    },  
    "anotherProperty": {  
      "type": "number",  
      "minimum": 0,  
      "maximum": 100  
    }  
  },  
  "required": \["propertyName"\]  
}

Only certain JSON Schema features are allowed:

##### Supported Schema Types

The schema can only contain **primitive types** (string, number/integer, boolean) and simple enums, with basic constraints. Specifically[\[323\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=The%20schema%20is%20restricted%20to,these%20primitive%20types)[\[324\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=,time%22)[\[325\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=3)[\[326\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=4):

1. **String Schema:** may include minLength, maxLength, and a limited set of format values (supported: "email", "uri", "date", "date-time")[\[327\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=1). Example[\[328\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Copy):

* {  
    "type": "string",  
    "title": "Display Name",  
    "description": "Description text",  
    "minLength": 3,  
    "maxLength": 50,  
    "format": "email"  
  }

* (This would prompt for an email with certain length limits.)

2. **Number Schema:** can have minimum/maximum and indicate "number" or "integer"[\[329\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=2). Example[\[330\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Copy):

* {  
    "type": "number",  
    "title": "Display Name",  
    "description": "Description text",  
    "minimum": 0,  
    "maximum": 100  
  }

3. **Boolean Schema:** optionally a default value (true/false)[\[325\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=3). Example:

* {  
    "type": "boolean",  
    "title": "Display Name",  
    "description": "Description text",  
    "default": false  
  }

4. **Enum Schema:** a special case of string with an enum array and optional enumNames for display labels[\[326\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=4). Example:

* {  
    "type": "string",  
    "title": "Display Name",  
    "description": "Description text",  
    "enum": \["option1", "option2", "option3"\],  
    "enumNames": \["Option 1", "Option 2", "Option 3"\]  
  }

No nested objects or arrays are allowed inside properties. This keeps the client’s job simpler (just generate a simple form).

Clients can use this schema to[\[331\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Clients%20can%20use%20this%20schema,to):  
\- Auto-generate input forms (fields for each property).  
\- Validate the user’s input against the schema before sending (type checks, required fields, formats, etc.).  
\- Provide guidance to users (e.g. use description as help text, title as field label).

Complex structures or deeply nested schemas are intentionally not supported to avoid overly complicating clients[\[332\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Note%20that%20complex%20nested%20structures%2C,supported%20to%20simplify%20client%20implementation).

#### *Response Actions*

As mentioned, there are three possible user actions: *accept*, *decline*, *cancel*. The client’s response uses an action field to clearly indicate which occurred[\[333\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Response%20Actions)[\[334\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=The%20three%20response%20actions%20are%3A), and optionally includes content for accept.

Recap of actions[\[334\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=The%20three%20response%20actions%20are%3A)[\[335\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=1.%20Accept%20%28%60action%3A%20,without%20making%20an%20explicit%20choice):

* **Accept ("accept"):** User provided the requested data and confirmed.

* The content field contains an object matching the requested schema (the user’s input)[\[336\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=1.%20Accept%20%28%60action%3A%20,dismissed%20without%20making%20an%20explicit).

* Example user action: clicked “Submit” or “OK” with data filled.

* **Decline ("decline"):** User explicitly refused to provide the info.

* content is typically omitted[\[337\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=,clicked%20outside%2C%20pressed%20Escape%2C%20etc).

* Example: clicked “No” or “Don’t allow.”

* **Cancel ("cancel"):** User dismissed the prompt without making a choice.

* content is omitted[\[337\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=,clicked%20outside%2C%20pressed%20Escape%2C%20etc).

* Example: closed dialog, clicked outside, pressed Escape.

Servers should handle these as:  
\- *Accept:* proceed with the operation using the provided content data.  
\- *Decline:* treat it as a negative response – maybe inform the user that the operation cannot continue without the data, or use a fallback behavior.  
\- *Cancel:* similar to decline – the user essentially aborted the request, so the server should halt or take a default path.

#### *Security Considerations*

1. Servers **MUST NOT** use elicitation to ask for highly sensitive information (passwords, private keys, etc.)[\[338\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Security%20Considerations). Clients should ideally prevent such requests or at least warn users.

2. Clients **SHOULD** ensure the user approves any data before it’s sent. (No auto-send of potentially sensitive info without user confirmation.)

3. Both parties **SHOULD** validate that the user’s input conforms to the schema – clients do this before sending (already covered), and servers should validate on receipt (never assume the client enforced everything).

4. Clients **SHOULD** make it very clear which server is asking for info, to avoid phishing. For instance, label the prompt like “Server X requests: Please provide Y.”[\[339\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=1,way%20that%20makes%20it%20clear)

5. Clients **SHOULD** allow users to decline or cancel at any time and ensure that a “cancel” truly stops any waiting server operation (the server will get an action indicating cancellation).

6. Clients **SHOULD** implement rate limiting or other controls if a server spams elicitation requests (to avoid annoyance or social engineering attempts).

7. Clients **SHOULD** design the elicitation prompt UI to be obviously distinct from any normal system prompt, so users realize it’s coming from an external server and not from the app itself if that matters.

*(The goal is to ensure elicitation is used safely and transparently, with user in control of what is shared.)*

## Server Features

**Servers** provide the fundamental building blocks for adding context to language models via MCP[\[340\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=Servers%20provide%20the%20fundamental%20building,clients%2C%20servers%2C%20and%20language%20models). These **primitives** enable rich interactions between clients, servers, and language models:

* **Prompts:** Pre-defined templates or instructions that guide language model interactions[\[341\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=%2A%20Prompts%3A%20Pre,perform%20actions%20or%20retrieve%20information). (User-triggered messages or workflows, often interactive.)

* **Resources:** Structured data or content that provides additional context to the model[\[342\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=interactions%20,perform%20actions%20or%20retrieve%20information). (E.g. files, documents, context data attached by the application.)

* **Tools:** Executable functions that allow models to perform actions or retrieve information[\[343\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=,perform%20actions%20or%20retrieve%20information). (The model "calls" these to affect the outside world or get info.)

Each primitive falls into a general *control hierarchy* in terms of who triggers or controls it[\[344\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=Primitive%20Control%20Description%20Example%20Prompts,API%20POST%20requests%2C%20file%20writing):

| Primitive | Control | Description | Example Uses |
| :---- | :---- | :---- | :---- |
| **Prompts** | **User-controlled** | Interactive templates invoked by explicit user choice[\[345\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=Primitive%20Control%20Description%20Example%20Prompts,API%20POST%20requests%2C%20file%20writing) | Slash commands, menu options initiated by user |
| **Resources** | **Application-controlled** | Contextual data attached and managed by the client application[\[346\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=commands%2C%20menu%20options%20Resources%20Application,API%20POST%20requests%2C%20file%20writing) | File contents, git history automatically provided |
| **Tools** | **Model-controlled** | Functions that the *LLM model* decides to invoke as needed[\[347\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=client%20File%20contents%2C%20git%20history,API%20POST%20requests%2C%20file%20writing) | API requests, performing computations, file writes |

*(Prompts occur when the user selects them, resources are provided by the app, and tools are invoked by the AI itself during generation.)*

Below, each of these key primitives is detailed.

### Prompts

**Protocol Revision:** 2025-06-18[\[348\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Protocol%20Revision%3A%202025)

Prompts in MCP are **predefined message templates or instructions** that servers can expose to clients[\[349\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=The%20Model%20Context%20Protocol%20,provide%20arguments%20to%20customize%20them). They allow servers to provide structured interactions or guidance for the language model. Clients can discover what prompts a server offers, retrieve their content, and supply any required arguments to customize them[\[349\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=The%20Model%20Context%20Protocol%20,provide%20arguments%20to%20customize%20them).

#### *User Interaction Model*

Prompts are designed to be **user-controlled**[\[350\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=User%20Interaction%20Model). That means the user explicitly chooses to invoke a prompt provided by the server. In practice, a client might present prompts as slash commands in a chat interface, or as menu items, buttons, etc., that the user can select[\[351\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Prompts%20are%20designed%20to%20be,For%20example%2C%20as%20slash%20commands). For example, a server might offer a "/code\_review" prompt; the user typing "/code\_review" could trigger that prompt. *(See image: an example prompt exposed as a slash command in a UI.)*

*(Image: Example of prompt exposed as a slash command – the user types a slash and sees "Request Code Review" as an option.)*

However, implementors are free to present prompts however fits their app; MCP doesn’t mandate the UI[\[352\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=discover%20and%20invoke%20available%20prompts,any%20specific%20user%20interaction%20model).

#### *Capabilities*

Servers that support prompts **MUST** declare the prompts capability during initialization[\[353\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Capabilities). For example:

{  
  "capabilities": {  
    "prompts": {  
      "listChanged": true  
    }  
  }  
}

Here, listChanged: true indicates the server will send a notification if the list of available prompts changes (e.g. new prompt added on the fly)[\[354\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=%7B%20,true%20%7D%20%7D).

#### *Protocol Messages*

**Listing Prompts:** The client fetches the list of available prompts by sending a prompts/list request[\[355\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Listing%20Prompts). This supports pagination if there are many prompts[\[356\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=To%20retrieve%20available%20prompts%2C%20clients,Request).

* **Request:** {"jsonrpc":"2.0","id":X,"method":"prompts/list","params":{ "cursor": "\<optional-cursor\>" }}[\[356\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=To%20retrieve%20available%20prompts%2C%20clients,Request)

* **Response:** The server returns a list of prompt definitions (and possibly a nextCursor if not all were sent). Example[\[357\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=%7B%20,value%22%20%7D)[\[358\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Copy):

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "result": {  
    "prompts": \[  
      {  
        "name": "code\_review",  
        "title": "Request Code Review",  
        "description": "Asks the LLM to analyze code quality and suggest improvements",  
        "arguments": \[  
          { "name": "code", "description": "The code to review", "required": true }  
        \]  
      }  
    \],  
    "nextCursor": "next-page-cursor"  
  }  
}

In this example, the server has one prompt named "code\_review" with a title and description, and it expects one argument "code" (the code to be reviewed) which is required[\[359\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=,%5B).

**Getting a Prompt:** To retrieve the full content of a specific prompt (and possibly auto-fill its arguments), the client sends a prompts/get request with the prompt name and any arguments the user supplied[\[360\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Getting%20a%20Prompt)[\[361\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=,%7D%20%7D).

* **Request:** e.g. {"jsonrpc":"2.0","id":2,"method":"prompts/get","params":{ "name":"code\_review", "arguments": { "code": "...code snippet..." } }}[\[360\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Getting%20a%20Prompt)[\[361\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=,%7D%20%7D). The arguments object includes values for each required argument.

* **Response:** The server returns the prompt content. Example[\[362\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Response%3A)[\[363\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=,text):

{  
  "jsonrpc": "2.0",  
  "id": 2,  
  "result": {  
    "description": "Code review prompt",  
    "messages": \[  
      {  
        "role": "user",  
        "content": {  
          "type": "text",  
          "text": "Please review this Python code:\\ndef hello():\\n    print('world')"  
        }  
      }  
    \]  
  }  
}

Here, the prompt’s description and actual messages are returned. In this case, the prompt is a user message saying "Please review this Python code: ..." followed by the code provided in the argument[\[363\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=,text). (Prompts can contain multiple messages forming a conversation template; e.g. perhaps an assistant's expected response, etc., but here just one user message.)

*(The client would then presumably present that to the user or directly to the model as appropriate. If arguments were incomplete, the server might auto-complete them if possible via the completion API, see below.)*

**List Changed Notification:** If the server’s available prompts list changes (and it declared listChanged), it **SHOULD** send a notifications/prompts/list\_changed notification to the client[\[364\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=List%20Changed%20Notification):

{  
  "jsonrpc": "2.0",  
  "method": "notifications/prompts/list\_changed"  
}

This tells the client that it should call prompts/list again to get the updated list. (This could happen if, say, the server loaded a new prompt pack, or prompts depend on context that changed.)

#### *Message Flow*

The typical prompt usage flow is:

sequenceDiagram  
    participant Client  
    participant Server  
    Note over Client,Server: Discovery  
    Client-\>\>Server: prompts/list  
    Server--\>\>Client: List of prompts  
    Note over Client,Server: Usage  
    Client-\>\>Server: prompts/get (with args)  
    Server--\>\>Client: Prompt content  
    opt listChanged  
        Note over Client,Server: Changes  
        Server--)Client: prompts/list\_changed  
        Client-\>\>Server: prompts/list  
        Server--\>\>Client: Updated prompts  
    end

In this diagram: first the client discovers prompts via prompts/list. Later, when user wants to use one, client calls prompts/get (Usage). If the server’s prompts change on its own, it notifies and client fetches updated list (Changes).

#### *Data Types*

**Prompt:** A prompt definition includes:

* name: Unique identifier for the prompt (used in code, not shown to user if a title exists).

* title: Optional human-readable name for display in UI.

* description: Optional description of what the prompt does.

* arguments: Optional list of arguments that can customize the prompt (each argument may have name, description, whether required, etc.).

**PromptMessage:** A prompt may consist of one or more messages (like a conversation snippet). Each has:

* role: "user" or "assistant" (who the message is from in the template).

* content: a content block (text, image, audio, or even an embedded resource reference).

*(E.g. a prompt could define a multi-turn conversation where the user says X and the assistant should respond with Y – useful for scenario setups.)*

All content types in prompt messages support optional **annotations** (metadata like audience or priority), which are defined in the Resources section (not detailed here, but essentially tags about the content).

**PromptArgument:** Defines an argument for a prompt. Fields:

* name: identifier of the argument (for programmatic use and possibly fallback display).

* title: optional human-readable label for UI.

* description: optional description for the argument (guidance to user).

* required: boolean, whether this argument must be provided to use the prompt.

*(In the earlier example, the prompt "code\_review" had one argument "code" that was required and described as "The code to review".)*

#### *Error Handling*

Servers **SHOULD** return standard JSON-RPC errors for issues using prompts[\[365\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Error%20Handling):

* If an unknown prompt name is requested: error code \-32602 (Invalid params) – meaning "prompt not found".

* If required arguments are missing: also \-32602 (Invalid params).

* For internal server errors when processing a prompt: \-32603.

Example: If client requests a prompt that doesn’t exist or misses args, server might respond:

{  
  "jsonrpc": "2.0",  
  "id": X,  
  "error": {  
    "code": \-32602,  
    "message": "Invalid prompt name or missing arguments"  
  }  
}

#### *Implementation Considerations*

1. Servers **SHOULD** validate any prompt arguments they receive (e.g. if expecting code text, ensure it’s not too large or malformed) before processing[\[366\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Implementation%20Considerations).

2. Clients **SHOULD** handle pagination of prompt lists – e.g. if server provides nextCursor, call prompts/list again to get more, until all prompts are fetched[\[367\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=1,parties%20SHOULD%20respect%20capability%20negotiation).

3. Both clients and servers **SHOULD** respect capability negotiation – e.g. client shouldn’t call prompt methods if server didn’t advertise prompts, and server shouldn’t assume client will use prompts if it didn’t advertise support[\[367\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=1,parties%20SHOULD%20respect%20capability%20negotiation).

#### *Security*

Implementations **MUST** carefully validate all inputs to and outputs from prompts to prevent injection attacks or unauthorized data access[\[368\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Security). For example, if a prompt inserts user-provided code into a template, ensure it’s properly sanitized (to avoid malicious content in a prompt that could trick the LLM in unintended ways). Also, ensure that prompts themselves don’t inadvertently reveal sensitive info (since they might include static text authored by the server).

*(In summary: treat prompt content as potentially sensitive; validate and sanitize as appropriate.)*

### Resources

**Protocol Revision:** 2025-06-18[\[369\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Protocol%20Revision%3A%202025)

Resources provide a standardized way for servers to share data (context) with clients[\[370\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=The%20Model%20Context%20Protocol%20,uniquely%20identified%20by%20a%20URI). A **resource** could be anything from a file, to a dataset, to any contextual information that the server wants the LLM to have access to. Each resource is uniquely identified by a URI[\[371\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=context%20to%20language%20models%2C%20such,uniquely%20identified%20by%20a%20URI).

For example, a server could expose a documentation file or a database schema as a resource that the client can fetch and provide to the LLM when needed.

#### *User Interaction Model*

Resources in MCP are generally **application-driven** (controlled by the host client application)[\[372\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Resources%20in%20MCP%20are%20designed,For%20example%2C%20applications%20could). The host decides how and when to incorporate resource data. For instance, possible UI/UX patterns:

* A UI listing resources (files, docs) that the user can explicitly choose to attach to a question or allow the LLM to read[\[373\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=applications%20could%3A).

* A search interface for resources where user searches and selects relevant items.

* Automatic inclusion: the app might automatically attach certain resources based on context (like the file currently open in an IDE for context, etc.)[\[374\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,or%20the%20AI%20model%E2%80%99s%20selection).

*(An example UI might be a "resource picker" dialog showing available documents. See image for an example resource context picker.)*

*(Image: Example of resource context picker – shows a user interface where the user can select which files or data sources to share with the AI.)*

But again, MCP doesn’t dictate the UI; it only provides the protocol for listing, reading, and subscribing to resource changes[\[375\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Image%3A%20Example%20of%20resource%20context,any%20specific%20user%20interaction%20model).

#### *Capabilities*

Servers that offer resources **MUST** declare the resources capability[\[376\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Capabilities). It can include two optional flags:

{  
  "capabilities": {  
    "resources": {  
      "subscribe": true,  
      "listChanged": true  
    }  
  }  
}

* subscribe: whether the server supports clients subscribing to changes in specific resources[\[377\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=The%20capability%20supports%20two%20optional,features) (i.e., the server will send notifications when a resource is updated).

* listChanged: whether the server will send a notification if the overall list of resources changes (resource added/removed)[\[378\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,list%20of%20available%20resources%20changes).

Both are optional; a server might support none, one, or both[\[379\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Both%20,support%20neither%2C%20either%2C%20or%20both). Some examples:

* If neither is supported: {"resources": { }} (empty object)[\[380\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Copy).

* If only subscriptions are supported: {"resources": { "subscribe": true }}[\[381\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Copy).

* If only list-change notifications are supported: {"resources": { "listChanged": true }}[\[382\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=).

#### *Protocol Messages*

**Listing Resources:** The client requests the list of available resources via resources/list[\[383\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Listing%20Resources). This supports pagination (cursor-based) because there might be many resources.

* **Request:** {"jsonrpc":"2.0","id":X,"method":"resources/list","params":{ "cursor": "\<optional-cursor\>" }}[\[383\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Listing%20Resources).

* **Response:** The server returns a list of resources and possibly a nextCursor. Example[\[384\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=To%20discover%20available%20resources%2C%20clients,Request)[\[385\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Response%3A):

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "result": {  
    "resources": \[  
      {  
        "uri": "file:///project/src/main.rs",  
        "name": "main.rs",  
        "title": "Rust Software Application Main File",  
        "description": "Primary application entry point",  
        "mimeType": "text/x-rust"  
      }  
    \],  
    "nextCursor": "next-page-cursor"  
  }  
}

Here one resource is listed: a file main.rs with a URI, a human title and description, and a MIME type indicating it's Rust source code[\[386\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,rust).

*(The presence of nextCursor indicates more resources on subsequent pages.)*

**Reading Resources:** To get the actual content of a resource, the client sends resources/read with the resource’s URI[\[387\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Reading%20Resources).

* **Request:** e.g. {"jsonrpc":"2.0","id":2,"method":"resources/read","params":{ "uri": "file:///project/src/main.rs" }}[\[388\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=To%20retrieve%20resource%20contents%2C%20clients,request%3A%20Request).

* **Response:** The server returns the content(s). Example[\[389\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Response%3A):

{  
  "jsonrpc": "2.0",  
  "id": 2,  
  "result": {  
    "contents": \[  
      {  
        "uri": "file:///project/src/main.rs",  
        "mimeType": "text/x-rust",  
        "text": "fn main() {\\n    println\!(\\"Hello world\!\\");\\n}"  
      }  
    \]  
  }  
}

In this case, the resource was text (Rust code) so the server returns a text field with the content[\[390\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,%7D%20%5D%20%7D). It could also have returned binary data in a blob field if it were binary (discussed later). The contents is an array because conceivably reading one resource might yield multiple pieces (like a base resource and sub-resources? but typically one item).

**Resource Templates:** Servers might have *parameterized* resources – e.g., a template URI that can generate many resources. For example, a server might allow reading any file via a template file:///{path}. To support discovery of these, resources/templates/list can be used[\[391\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Resource%20Templates).

* **Request:** {"jsonrpc":"2.0","id":3,"method":"resources/templates/list"} (no params needed)[\[392\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Copy).

* **Response:** Returns a list of resource templates. Example[\[393\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Response%3A)[\[394\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=%7B%20,Project%20Files):

{  
  "jsonrpc": "2.0",  
  "id": 3,  
  "result": {  
    "resourceTemplates": \[  
      {  
        "uriTemplate": "file:///{path}",  
        "name": "Project Files",  
        "title": "Project Files",  
        "description": "Access files in the project directory",  
        "mimeType": "application/octet-stream"  
      }  
    \]  
  }  
}

This indicates the server supports reading files via a template URI file:///{path}, described as "Project Files". (Clients might use this to present an open file dialog or similar.)

*(Also note: the mimeType in a template might be generic like application/octet-stream if files can be of any type.)*

**List Changed Notification:** If the list of resources changes and the server declared listChanged, it **SHOULD** send notifications/resources/list\_changed[\[395\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=List%20Changed%20Notification):

{  
  "jsonrpc": "2.0",  
  "method": "notifications/resources/list\_changed"  
}

This signals the client to refresh the resource list.

**Subscriptions:** If subscribe is supported, the client can subscribe to updates on a specific resource using resources/subscribe[\[396\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Subscriptions).

* **Subscribe Request:** {"jsonrpc":"2.0","id":4,"method":"resources/subscribe","params":{ "uri": "\<resource URI\>" }}[\[397\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=%7B%20,%7D).

* The server will then send an **Update Notification** whenever that resource changes: notifications/resources/updated[\[398\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Update%20Notification%3A).

**Update Notification example:**

{  
  "jsonrpc": "2.0",  
  "method": "notifications/resources/updated",  
  "params": {  
    "uri": "file:///project/src/main.rs"  
  }  
}

This tells the client that the resource with that URI was updated (modified, new content available). The client can then call resources/read again if it wants the new content.

*(Unsubscribe is covered later, but essentially there's a resources/unsubscribe to cancel a subscription.)*

#### *Message Flow*

Typical flows might be:

* **Resource listing:** Client does resources/list (possibly multiple times if paginated) to get all available resources or ones of interest.

* **Resource usage:** When an LLM query is being formed, the client might attach certain resources (by reading them from server) to give to the model.

* **Dynamic update:** If a resource is large or frequently updated, the client might subscribe to it. The server then pushes updated notifications, and the client re-fetches content as needed, possibly updating context given to the model.

*(There's no explicit sequence diagram given in the text, but one can imagine: client asks for list, gets URIs; later client reads specific URIs; if server notifies changes, client re-reads if needed.)*

#### *Data Types*

**Resource:** A resource definition (as seen in list results) includes[\[399\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceContents%20,mimeType%3F%3A%20string%3B%20uri%3A%20string%3B)[\[400\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceLink%20,number%3B%20title%3F%3A%20string%3B%20type%3A%20%E2%80%9Cresource_link%E2%80%9D):

* uri: Unique identifier (likely a URI scheme like file://, https://, etc.)[\[399\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceContents%20,mimeType%3F%3A%20string%3B%20uri%3A%20string%3B)[\[400\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceLink%20,number%3B%20title%3F%3A%20string%3B%20type%3A%20%E2%80%9Cresource_link%E2%80%9D).

* name: Name of the resource (for programmatic use; often a filename or key)[\[401\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=annotations%3F%3A%20Annotations%3B%20description%3F%3A%20string%3B%20mimeType%3F%3A,type%3A%20%E2%80%9Cresource_link%E2%80%9D%3B%20uri%3A%20string%3B).

* title: Optional human-readable title for display[\[402\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=annotations%3F%3A%20Annotations%3B%20description%3F%3A%20string%3B%20mimeType%3F%3A,title%3F%3A%20string%3B%20uriTemplate%3A%20string%3B).

* description: Optional description of what the resource is[\[402\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=annotations%3F%3A%20Annotations%3B%20description%3F%3A%20string%3B%20mimeType%3F%3A,title%3F%3A%20string%3B%20uriTemplate%3A%20string%3B).

* mimeType: Optional MIME type of the resource content (if known)[\[403\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=annotations%3F%3A%20Annotations%3B%20description%3F%3A%20string%3B%20mimeType%3F%3A,string%3B%20type%3A%20%E2%80%9Cresource_link%E2%80%9D%3B%20uri%3A%20string).

* size: Optional size in bytes (if known)[\[404\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=mimeType%3F%3A%20string%3B%20name%3A%20string%3B%20size%3F%3A,type%3A%20%E2%80%9Cresource_link%E2%80%9D%3B%20uri%3A%20string%3B).

*(In the example above, name "main.rs", title "Rust ... Main File", description given, mimeType text/x-rust, etc.)*

**ResourceContents:** Represents the contents of a resource or sub-resource[\[405\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=):

* uri: The URI of this content piece (could be same as resource or a sub-part)[\[405\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* mimeType: MIME type of this content (if known)[\[405\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* \_meta: optional metadata object (for future/extensibility)[\[399\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceContents%20,mimeType%3F%3A%20string%3B%20uri%3A%20string%3B).

This is an interface that has two concrete forms: \- **TextResourceContents** – when content is textual, it will have a text field containing the text[\[406\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=)[\[407\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=text). \- **BlobResourceContents** – when content is binary, it will have a blob field with base64 data[\[408\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=)[\[409\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Inherited%20from%20ResourceContents.).

**ResourceLink:** A special content type used in tools and prompts, covered later, but basically a reference to a resource that can be included in a message or tool result. It includes similar fields to Resource (URI, name, etc.) plus type: "resource\_link"[\[400\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceLink%20,number%3B%20title%3F%3A%20string%3B%20type%3A%20%E2%80%9Cresource_link%E2%80%9D).

**ResourceTemplate:** Describes a parameterized resource source[\[410\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Fields: \- uriTemplate: The URI template (RFC 6570 syntax likely) with placeholders[\[411\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceTemplate%20,title%3F%3A%20string%3B%20uriTemplate%3A%20string%3B).  
\- name: Identifier for the template (like an ID)[\[412\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=mimeType%3F%3A%20string%3B%20name%3A%20string%3B%20title%3F%3A,string%3B%20uriTemplate%3A%20string%3B).  
\- title: Display title[\[413\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).  
\- description: Description of what kind of resources this template accesses[\[414\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).  
\- mimeType: The MIME type of resources from this template, if uniform[\[415\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

*(Example given was file:///{path} template.)*

**ResourceTemplateReference:** If needed, identifies either a resource or a template. It has type: "ref/resource" and a uri which could be a template URI or concrete resource URI[\[416\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). (Used in the completion API to hint completions for resources.)

#### *Annotations*

Resources (and content blocks) may have **annotations** as metadata hints[\[417\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Annotations). For resources, annotations can indicate:

* audience: who the resource is meant for – "user", "assistant", or both[\[418\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,12T15%3A00%3A58Z). For example, a resource with audience \["assistant"\] might be meant only for the AI’s eyes (like hidden context), whereas \["user"\] might be something to show to the user but not directly to the model.

* priority: a number 0.0 to 1.0 indicating importance[\[418\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,12T15%3A00%3A58Z). Higher means more important (should definitely include), lower means optional.

* lastModified: timestamp (ISO 8601 string) of when the resource was last updated[\[419\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=resource,12T15%3A00%3A58Z).

Example resource with annotations[\[420\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Copy):

{  
  "uri": "file:///project/README.md",  
  "name": "README.md",  
  "title": "Project Documentation",  
  "mimeType": "text/markdown",  
  "annotations": {  
    "audience": \["user"\],  
    "priority": 0.8,  
    "lastModified": "2025-01-12T15:00:58Z"  
  }  
}

This might indicate the README is primarily for the user to see, is fairly important (0.8), and was last modified Jan 12, 2025\.

Clients can use annotations to[\[421\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Clients%20can%20use%20these%20annotations,to):

* Filter resources by audience (only show user-relevant ones to user, etc.).

* Prioritize which resources to include in context (maybe only include top priority ones if context length limited).

* Display last modified times or sort by recency.

#### *Common URI Schemes*

MCP defines some standard URI schemes for resources. This list is not exhaustive (custom schemes can be used too)[\[422\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Common%20URI%20Schemes)[\[423\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Custom%20URI%20Schemes):

* **https://** – Used for resources available on the web via HTTPS[\[424\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=https%3A%2F%2F). Note: If the client can fetch the URL directly, the server should use https://. If the server itself needs to provide it, use a different scheme or custom scheme. Essentially, https:// here implies "the client can independently retrieve this resource from the internet if allowed"[\[425\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Used%20to%20represent%20a%20resource,resource%20contents%20over%20the%20internet).

* **file://** – Used for resources that behave like filesystems[\[426\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=file%3A%2F%2F). Doesn’t necessarily map to actual local files (the server might be remote but exposing its files via this scheme). The server may tag directories with a MIME type like inode/directory (an XDG MIME type) to denote directories versus files[\[427\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Used%20to%20identify%20resources%20that,have%20a%20standard%20MIME%20type).

* **git://** – Could represent git repository content (though not fully detailed here)[\[428\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=git%3A%2F%2F). Possibly to identify resources tied to version control.

* **Custom schemes:** Allowed as long as they conform to URI format (RFC 3986\)[\[429\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Custom%20URI%20Schemes). e.g. myapp://data/123 if an application defines its own way to reference things. Namespaces starting with mcp: or similar might be reserved as earlier sections indicated.

#### *Error Handling*

Servers **SHOULD** return standard errors for common issues[\[430\]](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/pagination#:~:text=Error%20Handling):

* If a requested resource (by URI) is not found or accessible: they can use a custom error code, e.g. \-32002 for "Resource not found"[\[431\]](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/pagination#:~:text=Error%20Handling). (The code \-32000 to \-32099 are reserved for implementation-defined errors in JSON-RPC.)

* Internal errors (e.g. file I/O issue): \-32603 (Internal error).

Example error response for missing resource[\[432\]](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/pagination#:~:text=Invalid%20cursors%20SHOULD%20result%20in,32602%20%28Invalid%20params):

{  
  "jsonrpc": "2.0",  
  "id": 5,  
  "error": {  
    "code": \-32002,  
    "message": "Resource not found",  
    "data": {  
      "uri": "file:///nonexistent.txt"  
    }  
  }  
}

#### *Security Considerations*

1. Servers **MUST** validate all resource URIs they receive (to avoid path traversal or invalid references)[\[433\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Security%20Considerations). For instance, ensure a file:/// URI actually falls under allowed directories, etc.

2. Servers should implement access controls on resources – e.g. ensure the user has permission to access that resource before including it.

3. Binary data must be properly encoded (the spec already requires base64 for binary in JSON)[\[434\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=1,SHOULD%20be%20checked%20before%20operations).

4. Both server and client should be mindful of resource sizes – e.g. not sending extremely large contexts without user consent.

5. The client should not expose resources to the model unless the user allowed it (basically tie in with user consent flows possibly).

6. The client should monitor which resources are in use and manage accordingly (e.g. if a resource is sensitive, maybe confirm before sending to LLM).

*(Overall: treat resources as potentially sensitive data. Only share and use them with proper user awareness and according to access rules.)*

### Tools

**Protocol Revision:** 2025-06-18[\[435\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Protocol%20Revision%3A%202025)

Tools allow servers to expose functions that can be invoked by the language model (via the client)[\[436\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=The%20Model%20Context%20Protocol%20,includes%20metadata%20describing%20its%20schema). They enable LLMs to interact with external systems – e.g. querying a database, retrieving live information, performing calculations. Each tool has a name and a schema describing its input (and optionally output)[\[437\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=invoked%20by%20language%20models,includes%20metadata%20describing%20its%20schema).

#### *User Interaction Model*

Tools in MCP are intended to be **model-controlled**[\[438\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=User%20Interaction%20Model). That means the language model can decide to call a tool when it determines it's needed, without direct user action at that moment (though the user had to permit the tool in general). However, implementations may still involve the user in approving tool use for safety.

For trust & safety, it’s recommended that a human be in the loop for any tool that can have side effects[\[439\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=itself%20does%20not%20mandate%20any,specific%20user%20interaction%20model). Applications **SHOULD**[\[440\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=For%20trust%20%26%20safety%20and,Applications%20SHOULD):

* Clearly indicate which tools are available to the AI (so the user knows what the AI can do).

* Show a visual indicator when a tool is invoked (so the user sees that "the AI is using tool X now").

* Possibly present a confirmation prompt to the user before certain sensitive tools execute, ensuring user oversight (especially for destructive actions).

*(This ensures that even though the model "chooses" to use a tool, the user isn’t completely blindsided.)*

#### *Capabilities*

Servers that provide tools **MUST** declare the tools capability[\[441\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Capabilities):

{  
  "capabilities": {  
    "tools": {  
      "listChanged": true  
    }  
  }  
}

listChanged: true indicates the server will notify if the list of tools changes (like prompts, resources, etc.)[\[442\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,).

*(No “subscribe” for tools because tools don’t have streaming updates in the same way, aside from their outputs which come as part of call results.)*

#### *Protocol Messages*

**Listing Tools:** Client requests tool list via tools/list[\[443\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Listing%20Tools). (Supports pagination similar to prompts/resources.)

* **Request:** {"jsonrpc":"2.0","id":X,"method":"tools/list","params":{ "cursor": "\<optional\>" }}[\[444\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=To%20discover%20available%20tools%2C%20clients,Request).

* **Response:** Server returns list of tool definitions (and nextCursor if more). Example[\[445\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Response%3A)[\[446\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,City%20name%20or%20zip%20code):

{  
  "jsonrpc": "2.0",  
  "id": 1,  
  "result": {  
    "tools": \[  
      {  
        "name": "get\_weather",  
        "title": "Weather Information Provider",  
        "description": "Get current weather information for a location",  
        "inputSchema": {  
          "type": "object",  
          "properties": {  
            "location": {  
              "type": "string",  
              "description": "City name or zip code"  
            }  
          },  
          "required": \["location"\]  
        }  
      }  
    \],  
    "nextCursor": "next-page-cursor"  
  }  
}

This defines a tool named "get\_weather" which, given a location string, provides weather info[\[447\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,). It has a title and description, and an inputSchema (JSON Schema for the expected arguments). No outputSchema here, meaning output is presumably unstructured (will just be returned as content).

**Calling Tools:** When the model (via the client) decides to invoke a tool, the client sends tools/call to the server[\[448\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Calling%20Tools).

* **Request:** includes the tool name and an arguments object with the inputs. Example[\[449\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Calling%20Tools)[\[450\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,%7D%20%7D):

{  
  "jsonrpc": "2.0",  
  "id": 2,  
  "method": "tools/call",  
  "params": {  
    "name": "get\_weather",  
    "arguments": {  
      "location": "New York"  
    }  
  }  
}

This asks the server to execute get\_weather with the location "New York".

* **Response:** The server executes the tool and returns a result or error. Example successful result[\[451\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=)[\[452\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,false):

{  
  "jsonrpc": "2.0",  
  "id": 2,  
  "result": {  
    "content": \[  
      {  
        "type": "text",  
        "text": "Current weather in New York:\\nTemperature: 72°F\\nConditions: Partly cloudy"  
      }  
    \],  
    "isError": false  
  }  
}

Here content is an array of content blocks (in this case just a text block with the weather info), and isError: false indicates the tool executed successfully[\[453\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=%7B%20,false).

If the tool had a structured output schema and returned structured content, the result might also include a structuredContent field (discussed later).

*(Note: content is an array because a tool might return multiple pieces, e.g. text plus an image, etc. In many cases, it’s one item.)*

**List Changed Notification:** If listChanged is declared for tools, the server notifies the client of any additions/removals with notifications/tools/list\_changed[\[454\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

{  
  "jsonrpc": "2.0",  
  "method": "notifications/tools/list\_changed"  
}

Client should then refresh the list via tools/list.

#### *Message Flow*

General flow: \- The client fetches the tool list at startup (after initialization) so it knows what tools are available and can present them to the model or user as needed. \- During an LLM conversation, if the model output indicates a tool invocation (according to whatever agent paradigm is used), the client calls tools/call on behalf of the model. \- The server executes the action and returns results; the client feeds those results back into the model’s context (e.g. as the assistant’s reply or as data for further reasoning). \- If new tools become available or removed (perhaps server loaded a new plugin), server sends list\_changed and client updates its knowledge of available tools.

*(This is the typical “ReAct” or tool-using agent loop, though the spec does not prescribe exactly how the model decides to call a tool – that’s up to the client’s prompting mechanism or chain-of-thought logic.)*

#### *Data Types*

**Tool:** A tool definition includes[\[455\]\[456\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=):

* name: unique name (identifier) for the tool (used by model to reference it)[\[457\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=name).

* title: optional human-friendly title[\[458\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* description: what the tool does, human-readable[\[459\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Optional%20additional%20tool%20information).

* inputSchema: JSON Schema (object type) defining expected input parameters[\[460\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=input%20Schema).

* outputSchema: (optional) JSON Schema defining structure of the tool’s structured output (if any)[\[461\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* annotations: optional ToolAnnotations object with extra hints about the tool (see below)[\[462\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* \_meta: optional metadata (reserved)[\[463\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

The **inputSchema** is an object schema requiring whatever fields (like the “location” string in get\_weather). The **outputSchema** if present is also an object schema describing the structure of the result (for example, if get\_weather had an output schema, it might specify fields like temperature, conditions, etc.). If outputSchema is provided, the server promises to return structuredContent conforming to it, and clients should validate it[\[461\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=)[\[464\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=outputSchema%3F%3A%20,type%3A%20%E2%80%9Cobject%E2%80%9D%3B).

**ToolAnnotations:** Additional hints about a tool’s behavior and properties[\[465\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ToolAnnotations%20,readOnlyHint%3F%3A%20boolean%3B%20title%3F%3A%20string%3B). Fields:

* destructiveHint: boolean hint if the tool may perform destructive actions (true means it can delete/modify data; false means it's read-only)[\[466\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Only meaningful if readOnlyHint is false (because if readOnly is true, destructiveHint is irrelevant). Default true (assume it could be destructive unless said otherwise)[\[466\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* idempotentHint: boolean hint if calling the tool with the same input multiple times has no additional effect beyond the first (true \= idempotent)[\[467\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Only meaningful if readOnly is false. Default false (assume not idempotent)[\[467\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* openWorldHint: boolean hint if the tool interacts with an "open world" (external/unbounded environment) or a closed domain[\[468\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). For example, a web search tool is open-world, a memory lookup tool is closed-world. Default true (assume it can access broad external data unless indicated)[\[468\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* readOnlyHint: boolean hint if the tool does not modify anything (true \= purely read operations)[\[469\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Default false (assume it might modify unless declared read-only)[\[469\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* title: optional short title for the tool (like a label)[\[470\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

These are hints – not guaranteed accurate (especially for untrusted servers). Clients should *not* rely solely on them for security decisions without trust, but they can use them to, for example, warn the user if a tool is potentially destructive or requires caution[\[471\]\[471\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=NOTE%3A%20all%20properties%20in%20ToolAnnotations,title). The spec explicitly notes these are not guaranteed and should be treated as untrusted if from untrusted sources[\[465\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ToolAnnotations%20,readOnlyHint%3F%3A%20boolean%3B%20title%3F%3A%20string%3B)[\[471\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=NOTE%3A%20all%20properties%20in%20ToolAnnotations,title).

*(In other words, a malicious server could lie in ToolAnnotations. So a client shouldn't automatically trust a tool that claims readOnlyHint true – it should still sandbox or confirm.)*

#### *Example Tools and Annotations*

In our "get\_weather" example: \- It's likely read-only (just fetching data) so readOnlyHint \= true, destructiveHint \= (not applicable), idempotent \= probably true (same query yields same result around same time), openWorld \= true (calls external API).

If a server defined a "delete\_file" tool, it might mark: destructiveHint \= true, readOnlyHint \= false, idempotent maybe true (deleting same file twice has no extra effect if first succeeded), openWorld perhaps false if it's confined to its environment.

#### *Tool Execution & Output*

When a tool is invoked: \- The server executes it and returns a result in CallToolResult[\[472\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=)[\[473\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=model).

**CallToolResult** contains[\[472\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=)[\[473\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=model): \- content: an array of ContentBlocks representing the tool's *unstructured* output (e.g. a textual message or image to show the user/LLM)[\[474\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CreateMessageResult%20,key%3A%20string%5D%3A%20unknown%3B)[\[473\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=model).  
\- structuredContent: optional object with structured output (if outputSchema was defined)[\[472\]\[475\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).  
\- isError: optional boolean indicating if the tool encountered an execution error (business logic error)[\[476\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). If false or missing, means success. If true, the content likely contains an error message.  
\- \_meta: optional metadata (like others)[\[477\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

The idea is: \- If a tool execution fails *internally* (e.g. API call failed), the server should still return 200 OK at protocol level but set isError: true and perhaps output an error message in content[\[476\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=)[\[478\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Any%20errors%20that%20originate%20from,correct). This way the LLM knows the tool failed and can handle it. Only if a tool cannot be found or input was invalid should the server return a JSON-RPC error (which the LLM might not see directly)[\[479\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Any%20errors%20that%20originate%20from,correct). The spec recommends using isError for tool-level errors so that the AI is aware of the failure rather than shielding it with a protocol error[\[480\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=isError%3F%3A%20boolean)[\[479\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Any%20errors%20that%20originate%20from,correct). \- If outputSchema exists, the server should provide the parsed result in structuredContent and also likely include a serialized version in content for the LLM to read (for backward compatibility)[\[481\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,tool%20behavior)[\[482\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=%7B%20,). The client might validate structuredContent against outputSchema if desired.

For example, if "get\_weather" had an outputSchema with fields temperature, conditions, humidity, then the server could return:

"result": {  
  "content": \[  
    { "type": "text", "text": "{\\"temperature\\":22.5, \\"conditions\\":\\"Partly cloudy\\", \\"humidity\\":65}" }  
  \],  
  "structuredContent": {  
    "temperature": 22.5,  
    "conditions": "Partly cloudy",  
    "humidity": 65  
  }  
}

So the LLM sees the JSON as text, but also if the client/LLM is smart, it could parse structuredContent directly. The spec says if an outputSchema is provided, clients and LLMs can use it for strict validation and parsing[\[483\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=)[\[484\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Image%20Content).

#### *Error Handling*

There are two layers of errors for tools[\[485\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Tools%20use%20two%20error%20reporting,mechanisms): 1\. *Protocol-level errors:* JSON-RPC errors if the tool name is unknown, or invalid input, or server totally fails (like exceptions)[\[486\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=1.%20Protocol%20Errors%3A%20Standard%20JSON,Business%20logic%20errors). These follow normal JSON-RPC error flows (so the tools/call would return an "error" object). The model might not directly see these, depending on client implementation. 2\. *Tool execution errors:* If the tool runs but results in an application error (like "City not found" or an API limit exceeded), the server should return a normal result with isError: true and details in content/structuredContent[\[486\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=1.%20Protocol%20Errors%3A%20Standard%20JSON,Business%20logic%20errors). This way the LLM can handle it.

The spec gives examples: \- *Protocol error example:* If the client calls a tool that doesn’t exist: json { "jsonrpc": "2.0", "id": 3, "error": { "code": \-32602, "message": "Unknown tool: invalid\_tool\_name" } }[\[487\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=%7B%20,%7D) \- *Tool execution error example:* Suppose get\_weather’s API fails: json { "jsonrpc": "2.0", "id": 4, "result": { "content": \[ { "type": "text", "text": "Failed to fetch weather data: API rate limit exceeded" } \], "isError": true } }[\[488\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Copy)

In this second case, the assistant (LLM) would receive the error message and could decide to apologize to user or try again later, etc. The isError flag tells the client/LLM that the tool didn't accomplish its intended task.

#### *Security Considerations*

Tools can be powerful (some might execute code, access external APIs, modify data), so:

* Servers **MUST** validate all tool inputs before executing (don’t run dangerous operations on bad input)[\[489\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Security%20Considerations).

* Servers **MUST** implement proper access controls for tools. Only expose tools that are safe for the given user/context. If a tool performs sensitive actions, maybe require additional user authorization beyond normal.

* Servers **MUST** rate limit tool invocations to prevent abuse (especially if they call external services or can cost money)[\[490\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=1.%20Servers%20MUST%3A%20,Rate%20limit%20tool%20invocations).

* Servers **MUST** sanitize any outputs (e.g. if a tool returns a string that came from an untrusted source, ensure it doesn’t contain malicious content that could prompt the model maliciously – though this is a complex topic).

* Clients **SHOULD** prompt users for confirmation on sensitive tool actions (especially if a tool has destructiveHint true or openWorld true, etc.)[\[491\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=2.%20Clients%20SHOULD%3A%20,tool%20usage%20for%20audit%20purposes).

* Clients **SHOULD** show the tool’s inputs to the user before sending to server, if there's concern of data exfiltration (i.e. if model tries to send some user data to a tool, user should know)[\[491\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=2.%20Clients%20SHOULD%3A%20,tool%20usage%20for%20audit%20purposes).

* Clients **SHOULD** implement timeouts for tool calls (so a hung tool doesn’t stall everything)[\[492\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,tool%20usage%20for%20audit%20purposes).

* Clients **SHOULD** log tool usage for audit (so you can trace what the AI did)[\[492\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,tool%20usage%20for%20audit%20purposes).

*(Essentially: treat tools as highly privileged operations. The user should be aware of what the AI is doing with them, and the system should guard against misuse.)*

---

## Schema Reference

*(Below is the full normative TypeScript interface schema for MCP, describing every message and data structure. This serves as the authoritative specification of message formats.)*

### Common Types

#### *Annotations*

interface Annotations {    
  audience?: Role\[\];    
  lastModified?: string;    
  priority?: number;    
}

Optional annotations for various objects. These provide hints for how clients can use or display data[\[493\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Optional%20annotations%20for%20the%20client,objects%20are%20used%20or%20displayed).

* **audience?** (Role\[\]) – Intended audience(s) for the object[\[494\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=). Possible values: "user", "assistant" (one or both). If an object is useful for both user and assistant, include both.

* **lastModified?** (string) – ISO 8601 timestamp of when the object was last modified[\[495\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=). E.g. "2025-01-12T15:00:58Z". Useful for showing recency.

* **priority?** (number) – Importance of the object (0.0 to 1.0)[\[496\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=priority%3F%3A%20number). 1 \= most important (essential), 0 \= least important (optional).

#### *AudioContent*

interface AudioContent {    
  \_meta?: { \[key: string\]: unknown };    
  annotations?: Annotations;    
  data: string;    
  mimeType: string;    
  type: "audio";    
}

Represents an audio clip provided to or from an LLM[\[497\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Audio%20provided%20to%20or%20from,an%20LLM).

* **\_meta?** – optional metadata (object)[\[498\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=%60Optional%60). (Reserved for future/protocol use; should ignore if unknown keys.)

* **annotations?** – optional Annotations for the audio (e.g. audience might specify if the audio is meant for user vs assistant)[\[499\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=).

* **data** (string) – Base64-encoded audio data[\[500\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=data).

* **mimeType** (string) – MIME type of the audio (e.g. "audio/wav", "audio/mpeg")[\[501\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=mime%20Type).

* **type** – literal "audio" (discriminator)[\[502\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=interface%20AudioContent%20%5C,).

#### *BlobResourceContents*

interface BlobResourceContents {    
  \_meta?: { \[key: string\]: unknown };    
  blob: string;    
  mimeType?: string;    
  uri: string;    
}

The contents of a resource when the content is binary (a "blob")[\[408\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=).

* **\_meta?** – optional metadata[\[503\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=%60Optional%60). (See \_meta usage notes.)

* **blob** (string) – Base64-encoded binary data of the resource[\[504\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=blob).

* **mimeType?** (string) – MIME type if known (optional)[\[505\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=). If not provided, client may infer or treat as application/octet-stream.

* **uri** (string) – The URI of this resource content[\[506\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=uri). (It should match the resource’s URI or a sub-resource identifier.)

*(This interface extends the base ResourceContents concept with a blob.)*

#### *BooleanSchema*

interface BooleanSchema {    
  default?: boolean;    
  description?: string;    
  title?: string;    
  type: "boolean";    
}

Schema definition for a boolean type (used in elicitation requestedSchema, etc.). It may have:

* **default?** (boolean) – default value if not provided by user.

* **description?** (string) – a human-readable description of what this boolean means.

* **title?** (string) – a short title/label.

* **type** – literal "boolean".

#### *ClientCapabilities*

interface ClientCapabilities {    
  elicitation?: object;    
  experimental?: { \[key: string\]: object };    
  roots?: { listChanged?: boolean };    
  sampling?: object;    
}

Capabilities a client can support[\[507\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=). Fields (all optional):

* **elicitation?** (object) – Present if client supports server-initiated elicitation requests[\[508\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=). (The object is empty or can contain future sub-capabilities; currently just presence/absence is used.)

* **experimental?** ({ \[key: string\]: object }) – A map of any client-specific experimental capabilities the client supports[\[509\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Present%20if%20the%20client%20supports,elicitation%20from%20the%20server). (Keys can be any custom capability names, values are objects possibly detailing support.)

* **roots?** ({ listChanged?: boolean }) – Present if client supports roots feature[\[510\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Experimental%2C%20non,client%20supports). If present, listChanged indicates support for notifications when roots list changes.

* **sampling?** (object) – Present if client supports server-initiated sampling[\[511\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Whether%20the%20client%20supports%20notifications,changes%20to%20the%20roots%20list) (again, object likely empty as a flag).

*(This interface is extensible; servers should ignore keys they don’t recognize, and any unknown properties in known keys, etc.)*

#### *ContentBlock*

type ContentBlock \=   
    | TextContent   
    | ImageContent   
    | AudioContent   
    | ResourceLink   
    | EmbeddedResource;

A union of all content types. A content block can be: \- Text content \- Image content \- Audio content \- Resource link (a reference to a resource) \- Embedded resource (actual resource content included inline)

#### *Cursor*

type Cursor \= string;

An opaque token used for pagination[\[512\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=). (The client should not interpret this string, just pass it back to continue listing.)

#### *EmbeddedResource*

interface EmbeddedResource {    
  \_meta?: { \[key: string\]: unknown };    
  annotations?: Annotations;    
  resource: TextResourceContents | BlobResourceContents;    
  type: "resource";    
}

Represents an embedded resource content included directly in a message or tool result[\[513\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=). This is essentially a full resource’s data inlined.

* **\_meta?** – optional metadata[\[514\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=%60Optional%60).

* **annotations?** – optional Annotations for this resource content (e.g. audience, priority)[\[515\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=See%20General%20fields%3A%20,meta%60%20usage).

* **resource** – either a TextResourceContents or BlobResourceContents object containing the data[\[516\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=%5C_meta%3F%3A%20%5C,).

* **type** – literal "resource" (discriminator)[\[517\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=annotations%3F%3A%20Annotations%3B%20resource%3A%20TextResourceContents%20,).

*(The client can render or use this embedded content as if it fetched the resource. It’s up to the client how to present it to the LLM or user, e.g. "Here is file X content...")*

#### *EmptyResult*

type EmptyResult \= Result;

Represents a response that indicates success but carries no data. Essentially, an empty JSON-RPC result object (maybe just \_meta). It aliases Result (described later) for semantic clarity.

*(Used for e.g. notifications acknowledgments or something possibly.)*

#### *EnumSchema*

interface EnumSchema {    
  description?: string;    
  enum: string\[\];    
  enumNames?: string\[\];    
  title?: string;    
  type: "string";    
}

Schema for an enumeration of strings (used in elicitation). Fields:

* **description?** – description of the field that uses this schema.

* **enum** (string\[\]) – the set of allowed string values[\[518\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=).

* **enumNames?** (string\[\]) – optional human-friendly names corresponding to each value in enum (same length as enum array)[\[519\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=%7B%20,). If provided, use these for display instead of raw values.

* **title?** – a title/label for the field.

* **type** – "string" (since enumerations are represented as string type).

*(So essentially, an enum is a string schema with a constrained set of values.)*

#### *ImageContent*

interface ImageContent {    
  \_meta?: { \[key: string\]: unknown };    
  annotations?: Annotations;    
  data: string;    
  mimeType: string;    
  type: "image";    
}

Represents an image provided to or from an LLM[\[520\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Image%20Content).

* **\_meta?** – optional metadata.

* **annotations?** – optional Annotations (perhaps indicating e.g. an image might only be for user or model, etc.).

* **data** – Base64-encoded image data[\[521\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Image%20content%20allows%20including%20visual,information%20in%20messages).

* **mimeType** – MIME type of the image (e.g. "image/png", "image/jpeg")[\[522\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Copy).

* **type** – literal "image".

*(Large images should be handled carefully to not blow up token limits; but that’s up to client to maybe convert to text (like an OCR or description) if needed, since LLMs can’t literally "see" images unless there's a multimodal model. Or maybe the LLM could use an image recognition tool if available. Anyway, this just passes image data if needed.))*

#### *Implementation*

interface Implementation {    
  name: string;    
  title?: string;    
  version: string;    
}

Describes the name and version of a software implementation (client or server)[\[523\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ModelHint%20,)[\[524\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Used in e.g. clientInfo and serverInfo fields during initialization.

* **name** (string) – Programmatic name of the implementation. Should be something like a package or product name, used internally or for logging. In past specs it was sometimes used as display if title not given.

* **title?** (string) – Optional human-readable name for UI display. If not provided, the name can be used as fallback for display.

* **version** (string) – Version of the implementation (e.g. "1.0.0").

*(These fields allow both sides to know what software the other is running, which can help compatibility and debugging. E.g. name "ExampleClient", title "Example Client Display Name", version "1.0.0".)*

#### *JSONRPCError*

interface JSONRPCError {    
  error: { code: number; data?: unknown; message: string };    
  id: RequestId;    
  jsonrpc: "2.0";    
}

A JSON-RPC error response object (per JSON-RPC 2.0 spec). Fields:

* **error** – object containing:

* code (number) – the error code (e.g. \-32602).

* message (string) – short description of the error.

* data? (unknown) – optional additional data about the error[\[525\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Additional%20information%20about%20the%20error,error%20information%2C%20nested%20errors%20etc) (could be any JSON value). For MCP, often used to convey details like supported versions, etc., in errors.

* **id** – the ID of the request that this is a response to.

* **jsonrpc** – the string "2.0".

*(This corresponds to the JSON-RPC 2.0 error object. The client or server uses this for error replies. Example earlier of an error for unsupported version fits here.)*

#### *JSONRPCNotification*

interface JSONRPCNotification {    
  jsonrpc: "2.0";    
  method: string;    
  params?: { \_meta?: { \[key: string\]: unknown }; \[key: string\]: unknown };    
}

Represents a JSON-RPC **notification** (no id, no response expected)[\[526\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **jsonrpc** – "2.0"

* **method** – the method name (e.g. "notifications/progress")[\[526\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **params?** – optional parameters object[\[527\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=method%3A%20string%3B%20params%3F%3A%20,). In MCP, we allow an object that may contain \_meta and other fields depending on the notification type. If none, this could be omitted.

*(Notifications in MCP often have no params (just signal something happened), but some have, like updated has uri param, progress has progress details, etc.)*

**Note on params**: The interface defines it as possibly containing \_meta and any other keys. MCP reserves \_meta in notifications for future use or additional info (like progress tokens on cancellations, etc.)[\[528\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

#### *JSONRPCRequest*

interface JSONRPCRequest {    
  id: RequestId;    
  jsonrpc: "2.0";    
  method: string;    
  params?: {    
    \_meta?: { progressToken?: ProgressToken; \[key: string\]: unknown };    
    \[key: string\]: unknown;    
  };    
}

Represents a JSON-RPC **request** (expects a response)[\[529\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **id** – the unique request ID (string or number)[\[530\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20JSONRPCRequest%20,).

* **jsonrpc** – "2.0".

* **method** – the method name (e.g. "initialize", "prompts/list", etc.)[\[530\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20JSONRPCRequest%20,).

* **params?** – parameters for the request, if any[\[531\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=jsonrpc%3A%20%E2%80%9C2,). In MCP, this is usually an object. The schema allows:

* An optional \_meta field within params, which itself can include an optional progressToken and other unknown keys[\[532\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). This is how the progressToken for tracking progress is attached (if the caller wants progress updates).

* Other fields as required by the specific method.

**ProgressToken usage:** If present in \_meta, it signals the sender wants progress updates for this request. The progressToken is an opaque value (string or number) chosen by the sender that's unique for active requests[\[533\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=,key%3A%20string%5D%3A%20unknown). The server would then use this in notifications/progress messages to identify which request is making progress.

#### *JSONRPCResponse*

interface JSONRPCResponse {    
  id: RequestId;    
  jsonrpc: "2.0";    
  result: Result;    
}

A JSON-RPC **response** indicating success (with a result)[\[534\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **id** – matches the request’s ID[\[535\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20JSONRPCResponse%20,0%E2%80%9D%3B%20result%3A%20Result%3B).

* **jsonrpc** – "2.0".

* **result** – a Result object (see below) containing the outcome.

*(If an error had occurred, JSONRPCError would be used instead with an error field; JSONRPCResponse is specifically the successful case structure.)*

#### *LoggingLevel*

type LoggingLevel \=   
    | "debug"   
    | "info"   
    | "notice"   
    | "warning"   
    | "error"   
    | "critical"   
    | "alert"   
    | "emergency";

The severity level for a log message[\[536\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). This follows standard syslog levels from RFC 5424[\[537\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20severity%20of%20a%20log,message):

* "debug" (most fine-grained)

* "info"

* "notice"

* "warning"

* "error"

* "critical"

* "alert"

* "emergency" (most severe)

*(These are used in logging notifications and setLevel requests.)*

#### *ModelHint*

interface ModelHint {    
  name?: string;    
}

A hint for model selection[\[538\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Currently only one property:

* **name?** (string) – A model name hint[\[539\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). The client should interpret this as a substring to match or an identifier for a class of models. (Multiple ModelHints can be given in order of preference.)

If unspecified fields in ModelHint, they are ignored (e.g. future attributes might appear). Today, essentially it's just an optional name string.

Model hints are used in ModelPreferences to suggest particular models or families to the client[\[540\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20client%20SHOULD%20treat%20this,a%20model%20name%3B%20for%20example).

#### *ModelPreferences*

interface ModelPreferences {    
  costPriority?: number;    
  hints?: ModelHint\[\];    
  intelligencePriority?: number;    
  speedPriority?: number;    
}

Preferences for model selection, provided by the server[\[524\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) (as described in Sampling):

* **costPriority?** (number) – Importance of minimizing cost. 0 \= not important, 1 \= most important[\[541\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **hints?** (ModelHint\[\]) – Optional list of model hints (preferred model names or families, in order)[\[542\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). The client evaluates these in given order.

* **intelligencePriority?** (number) – Importance of model capability/quality. 0 \= not important, 1 \= extremely important[\[543\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **speedPriority?** (number) – Importance of latency/speed. 0 \= not important, 1 \= extremely important[\[544\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

These values guide the client in picking an LLM. They are advisory; the client is free to balance them as it sees fit (for example, might use them to compute a weighted score for candidate models, etc.)[\[545\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=dimensions%20to%20help%20clients%20make,selection%20for%20their%20use%20case).

No field is strictly required – if a priority is omitted, the client can assume a default (maybe 0 or 0.5). Hints if provided might override numeric priorities in importance as per spec (client should prioritize hints slightly over numbers)[\[546\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=that%20the%20first%20match%20is,taken).

#### *NumberSchema*

interface NumberSchema {    
  description?: string;    
  maximum?: number;    
  minimum?: number;    
  title?: string;    
  type: "number" | "integer";    
}

Schema for numeric types in elicitation. Fields:

* **description?** – description of the number field.

* **maximum?** (number) – maximum allowed value (inclusive presumably).

* **minimum?** (number) – minimum allowed value.

* **title?** – label for UI.

* **type** – either "number" (which can be float) or "integer" (no fractional part)[\[547\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=minimum%3F%3A%20number%3B%20title%3F%3A%20string%3B%20type%3A,%E2%80%9Cinteger%E2%80%9D%3B).

*(If the type is integer, the values user enters should be integers. The ranges apply accordingly.)*

#### *PrimitiveSchemaDefinition*

type PrimitiveSchemaDefinition \=   
    | StringSchema   
    | NumberSchema   
    | BooleanSchema   
    | EnumSchema;

A union of allowed primitive schema types for elicitation data: string, number/integer, boolean, or an enum of strings[\[548\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). This excludes complex types (no nested objects or arrays allowed in requestedSchema beyond the top object’s properties of these types).

#### *ProgressToken*

type ProgressToken \= string | number;

A progress token can be a string or number[\[549\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). It’s an opaque identifier chosen by the request sender to track progress notifications for that request. Must be unique per active request.

*(E.g. client could use an incrementing number or a GUID string as progressToken when making a request. The server just echoes it in progress notifications.)*

#### *Prompt*

interface Prompt {    
  \_meta?: { \[key: string\]: unknown };    
  arguments?: PromptArgument\[\];    
  description?: string;    
  name: string;    
  title?: string;    
}

Definition of a prompt template offered by the server[\[550\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata (reserved)[\[551\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **arguments?** (PromptArgument\[\]) – list of expected arguments for the prompt, if any[\[552\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=See%20General%20fields%3A%20_meta%20for,usage). Each argument defines a placeholder in the prompt that can be filled by the user or client.

* **description?** – a description of what this prompt does/provides[\[553\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=A%20list%20of%20arguments%20to,use%20for%20templating%20the%20prompt). Could be shown to user to help them decide when to use it.

* **name** (string) – unique identifier for the prompt[\[554\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=name) (for programmatic use).

* **title?** – optional display name for UI listing[\[555\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Inherited%20from%20BaseMetadata). If not given, name might be shown.

*(The actual content of the prompt is not in this structure because it’s retrieved via prompts/get. This is more like prompt metadata.)*

#### *PromptArgument*

interface PromptArgument {    
  description?: string;    
  name: string;    
  required?: boolean;    
  title?: string;    
}

Describes one argument of a prompt[\[556\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **description?** – human-readable explanation of the argument’s purpose[\[557\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). e.g. "The code to review" in our example.

* **name** – the name of the argument (used in the prompt template placeholders and in the API)[\[558\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=name). Should be unique within a prompt.

* **required?** (boolean) – whether this argument must be provided for the prompt to function[\[559\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). If true and user doesn't provide it, the client should ask or the server will error on get.

* **title?** – optional display label for the argument (short)[\[560\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). If not present, the client could use name as label.

*(This helps clients generate UI for filling prompt arguments, with proper labeling and help text.)*

#### *PromptMessage*

interface PromptMessage {    
  content: ContentBlock;    
  role: Role;    
}

Represents a single message in a prompt’s content[\[561\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **content** – the message content (text, image, audio, resource link, etc.)[\[562\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20PromptMessage%20,role%3A%20Role%3B).

* **role** – "user" or "assistant" indicating who is the speaker of this message in the prompt template[\[563\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

A prompt’s messages (as returned by prompts/get) will be an array of PromptMessage objects forming a conversation snippet. The roles alternate or as defined by the prompt scenario.

#### *PromptReference*

interface PromptReference {    
  name: string;    
  title?: string;    
  type: "ref/prompt";    
}

Identifies a prompt (used in completion references, etc.)[\[564\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **name** – the prompt’s name (identifier)[\[565\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=name).

* **title?** – optional title (again for display, if needed)[\[566\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **type** – "ref/prompt" indicating this reference type.

*(The completion/complete request uses a ref which could be a PromptReference or ResourceTemplateReference to specify what it's completing. E.g. ref: { type:"ref/prompt", name:"code\_review" } tells the server we want completions for a prompt argument of that name.)*

#### *RequestId*

type RequestId \= string | number;

ID of a JSON-RPC request. It can be string or number (but not null)[\[567\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

#### *Resource*

interface Resource {    
  \_meta?: { \[key: string\]: unknown };    
  annotations?: Annotations;    
  description?: string;    
  mimeType?: string;    
  name: string;    
  size?: number;    
  title?: string;    
  uri: string;    
}

Describes a resource available on the server[\[568\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata[\[569\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Inherited%20from%20BaseMetadata).

* **annotations?** – optional Annotations for this resource (audience, priority, lastModified)[\[570\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri).

* **description?** – a description of the resource[\[571\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri%3A%20string). For example "Primary application entry point" for main.rs. This is like a hint to help the LLM understand or to display to user.

* **mimeType?** – MIME type of the resource, if known[\[572\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20URI%20of%20this%20resource) (e.g. text/markdown, application/json, etc.).

* **name** – a name/identifier for the resource. Might be a filename or key. Not necessarily unique globally if multiple resources share names, but likely unique within context. (Used for programmatic reference or display if title missing.)

* **size?** (number) – size in bytes, if known. Useful for showing file size or estimating context usage.

* **title?** – human-readable title for UI. If not provided, name can be shown. For tools, if both prompt and name have titles, maybe prefer title.

* **uri** – the URI identifying this resource[\[570\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri).

*(Essentially, this is what we saw in resources/list responses.)*

**Note:** The text mentions "It can be thought of like a 'hint' to the model" for description, implying that the client might include the description of a resource when providing it to the model as context, to help the model understand why the resource is relevant.

#### *ResourceContents*

interface ResourceContents {    
  \_meta?: { \[key: string\]: unknown };    
  mimeType?: string;    
  uri: string;    
}

Base interface for content of a resource or sub-resource[\[405\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata[\[573\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **mimeType?** – MIME type if known[\[574\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **uri** – URI of this content piece[\[575\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=mimeType%3F%3A%20string).

TextResourceContents and BlobResourceContents extend this with a text or blob field respectively.

#### *ResourceLink*

interface ResourceLink {    
  \_meta?: { \[key: string\]: unknown };    
  annotations?: Annotations;    
  description?: string;    
  mimeType?: string;    
  name: string;    
  size?: number;    
  title?: string;    
  type: "resource\_link";    
  uri: string;    
}

A reference (link) to a resource, used within messages or tool outputs[\[576\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

This has basically the same fields as Resource (it’s like an inlined resource reference) plus: \- **type** – "resource\_link" to distinguish it as a content block type[\[577\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=type%3A%20%E2%80%9Cresource_link%E2%80%9D%3B%20uri%3A%20string%3B%20).

So ResourceLink includes: \- \_meta, annotations, description, mimeType, name, size, title, uri, all as defined in Resource above[\[400\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceLink%20,number%3B%20title%3F%3A%20string%3B%20type%3A%20%E2%80%9Cresource_link%E2%80%9D)[\[578\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

*(ResourceLink is used e.g. in tool outputs where a tool might say "here's a reference to a file you might want to read" instead of embedding whole file content. The model can then decide to ask to read it, etc.)*

#### *ResourceTemplate*

interface ResourceTemplate {    
  \_meta?: { \[key: string\]: unknown };    
  annotations?: Annotations;    
  description?: string;    
  mimeType?: string;    
  name: string;    
  title?: string;    
  uriTemplate: string;    
}

Describes a resource template (parameterized resource) on the server[\[410\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata[\[579\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **annotations?** – optional Annotations (could indicate, say, all resources from this template have certain audience/importance)[\[580\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **description?** – description of what this template is for[\[414\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Eg: "Access files in the project directory".

* **mimeType?** – If all resources produced by this template share a MIME type, specify it[\[581\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). If not, omit. (e.g. file:///{path} might omit because files can be many types, or specify octet-stream as generic).

* **name** – an identifier for the template[\[412\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=mimeType%3F%3A%20string%3B%20name%3A%20string%3B%20title%3F%3A,string%3B%20uriTemplate%3A%20string%3B).

* **title?** – display title for UI listing of templates[\[582\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **uriTemplate** (string) – The URI template string (RFC 6570 style) with placeholders for parameters[\[583\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri%20Template).

*(Clients could use uriTemplate to present an interface to fill in variables. E.g. if uriTemplate is file:///{path}, the client might allow user to enter a path or browse filesystem to pick a path, then construct the actual resource URI.)*

#### *ResourceTemplateReference*

interface ResourceTemplateReference {    
  type: "ref/resource";    
  uri: string;    
}

A reference used for completions that refers to a resource or a resource template by URI[\[416\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **type** – "ref/resource" (distinguishing it from "ref/prompt")[\[584\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceTemplateReference%20,uri%3A%20string%3B).

* **uri** – If it matches an existing resource’s URI, or if it matches a resource template’s uriTemplate format (with variables perhaps), the server will know what to complete.

*(In completion/complete, you can provide a ref with type "ref/resource" and a uri that might be a template like file:///{path} to get path completions, as seen in earlier changes list item about context arguments in completions.)*

#### *Result*

interface Result {    
  \_meta?: { \[key: string\]: unknown };    
  \[key: string\]: unknown;    
}

A generic result object for JSON-RPC responses[\[585\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). It’s basically an open object where \_meta can hold protocol metadata, and it can have any other fields.

* **\_meta?** – reserved field for protocol metadata in results[\[586\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). (Similar to how \_meta is used in requests.)

* Beyond that, any key can appear with any JSON value, as needed by the specific method’s result.

*(Every concrete response extends this or is defined in terms of this. For instance, ListPromptsResult adds prompts and nextCursor fields to this structure.)*

#### *Role*

type Role \= "user" | "assistant";

Role of a message or participant in a conversation. Either "user" or "assistant".

*(This is used in content messages to mark who is speaking. Could potentially be extended in future if needed (like system), but currently just those two for simplicity, as far as schema is concerned.)*

#### *Root*

interface Root {    
  \_meta?: { \[key: string\]: unknown };    
  name?: string;    
  uri: string;    
}

Represents a filesystem root (directory or file) that the client offers to server[\[587\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata[\[588\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **name?** – optional name for the root (for display)[\[589\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). (E.g. could be the folder name or a user-provided label like "Project A Directory".)

* **uri** – the URI of the root (likely file:// scheme)[\[590\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri). Must currently start with file:// (since as spec notes, only file URIs are allowed as roots for now)[\[591\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri%3A%20string).

*(This is what the client sends in roots/list results. E.g. name "My Project", uri "file:///home/user/myproject".)*

#### *SamplingMessage*

interface SamplingMessage {    
  content: TextContent | ImageContent | AudioContent;    
  role: Role;    
}

A message in a sampling (LLM call) conversation[\[592\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Similar to PromptMessage but only text, image, or audio content (no resource links embedded here, since we wouldn't embed actual resources in a model prompt, we'd use references or prior context injection instead).

* **content** – either text, image, or audio content block that will be sent to/received from LLM[\[593\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20SamplingMessage%20,AudioContent%3B%20role%3A%20Role%3B). (Resource content is not included because if a resource is needed, the idea is the client should embed it as text or as an image with OCR or some approach; or use the techniques outside of direct content. But anyway, the schema restricts to those three types here for clarity.)

* **role** – "user" or "assistant", denoting who said this message in the context of the sampling conversation[\[593\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20SamplingMessage%20,AudioContent%3B%20role%3A%20Role%3B).

*(This structure is used in the messages array within a CreateMessageRequest in sampling, and also to represent the model's reply in CreateMessageResult.)*

#### *ServerCapabilities*

interface ServerCapabilities {    
  completions?: object;    
  experimental?: { \[key: string\]: object };    
  logging?: object;    
  prompts?: { listChanged?: boolean };    
  resources?: { listChanged?: boolean; subscribe?: boolean };    
  tools?: { listChanged?: boolean };    
}

Capabilities that a server may support[\[594\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). This is analogous to ClientCapabilities.

Fields (all optional):

* **completions?** (object) – Present if server supports the argument autocompletion feature (Completion API)[\[595\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **experimental?** ({ \[key: string\]: object }) – Map of any experimental features the server supports (non-standard)[\[596\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **logging?** (object) – Present if server supports sending log messages via notifications/message and adjusting log level[\[597\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Experimental%2C%20non,server%20supports).

* **prompts?** ({ listChanged?: boolean }) – Present if server offers prompts. listChanged true if it will send prompt list change notifications[\[598\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **resources?** ({ listChanged?: boolean; subscribe?: boolean }) – Present if server offers resources. listChanged for resource list changes, subscribe for resource update subscriptions[\[599\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **tools?** ({ listChanged?: boolean }) – Present if server offers tools. listChanged if it notifies on tool list changes[\[600\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

*(This object is sent in the InitializeResult from server to client so the client knows what it can do with the server. For example, if logging is present, the client knows it can set log level and expect logs. If tools present, it can orchestrate tool usage, etc.)*

#### *StringSchema*

interface StringSchema {    
  description?: string;    
  format?: "uri" | "email" | "date" | "date-time";    
  maxLength?: number;    
  minLength?: number;    
  title?: string;    
  type: "string";    
}

Schema for a string type (for elicitation inputs, etc.)[\[601\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **description?** – e.g. "Your full name".

* **format?** – can be one of "uri", "email", "date", "date-time" if applicable[\[602\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20StringSchema%20,title%3F%3A%20string%3B%20type%3A%20%E2%80%9Cstring%E2%80%9D%3B). This hints the expected format; clients might validate or provide special input fields.

* **maxLength?** – maximum length of the string.

* **minLength?** – minimum length.

* **title?** – label/title for the field.

* **type** – "string".

#### *TextContent*

interface TextContent {    
  \_meta?: { \[key: string\]: unknown };    
  annotations?: Annotations;    
  text: string;    
  type: "text";    
}

Represents plain text content in a message[\[603\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata[\[604\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **annotations?** – optional Annotations (not usually needed for plain text, but perhaps could be used if text has an audience or priority)[\[605\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **text** (string) – the textual content[\[606\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=text).

* **type** – "text".

*(This is the most common content type for chat.)*

#### *TextResourceContents*

interface TextResourceContents {    
  \_meta?: { \[key: string\]: unknown };    
  mimeType?: string;    
  text: string;    
  uri: string;    
}

The contents of a resource when it’s text data[\[406\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata[\[607\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **mimeType?** – MIME type, if known (should match a text type, e.g. text/plain or text/markdown, etc.)[\[608\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Inherited%20from%20ResourceContents).

* **text** (string) – the text content of the resource[\[407\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=text).

* **uri** (string) – the URI of this content (the resource’s URI)[\[609\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri).

*(This corresponds to what we saw in resources/read result for main.rs where it returned a text field with the file content.)*

---

Now, after these type definitions, the spec lists the specific JSON-RPC methods and their request/response structures, tying together the types above:

### completion/complete

*(The method to get autocompletion suggestions for prompt/resource arguments.)*

#### *CompleteRequest*

interface CompleteRequest {    
  method: "completion/complete";    
  params: {    
    argument: { name: string; value: string };    
    context?: { arguments?: { \[key: string\]: string } };    
    ref: PromptReference | ResourceTemplateReference;    
  };    
}

Represents a client’s request to the server for completion suggestions[\[610\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **method** – "completion/complete"[\[611\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CompleteRequest%20,).

* **params**:

* **argument** – an object with:

  * name: the name of the argument being completed[\[612\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=,value%3A%20string).

  * value: the current input (prefix) that the user has typed for this argument[\[613\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20argument%E2%80%99s%20information).

* **context?** – optional context info:

  * arguments?: a map of already-resolved arguments[\[614\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=,). If this completion is for an argument in a prompt or template that has multiple fields, you provide those already known. E.g. if completing a framework field after a language field was chosen in a prompt, pass context.arguments \= { language: "python" } to guide suggestions[\[615\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Additional%2C%20optional%20context%20for%20completions).

* **ref** – a reference to what is being completed:

  * If completing a prompt argument, a PromptReference with the prompt name[\[616\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Previously,template%20or%20prompt).

  * If completing a resource path, a ResourceTemplateReference with the template URI.

*(Essentially, the client says: "the user is trying to fill argument X of prompt Y (or path param of resource Z), they've typed 'py', give me suggestions to complete it", possibly with context that they've already filled other related fields.)*

#### *CompleteResult*

interface CompleteResult {    
  \_meta?: { \[key: string\]: unknown };    
  completion: { hasMore?: boolean; total?: number; values: string\[\] };    
  \[key: string\]: unknown;    
}

The server’s response to a completion request[\[617\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata (e.g. might not be used here but reserved).

* **completion** – an object with:

* values (string\[\]): array of suggestion strings[\[618\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Type%20declaration) (maximum 100 suggestions as per spec, and ideally sorted by relevance).

* total? (number): optional total number of matches available[\[619\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Might be more than values.length if only returning a subset.

* hasMore? (boolean): if true, indicates there are additional suggestions beyond these values[\[618\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Type%20declaration) (even if exact total unknown). This is a cue that user might refine or ask for more.

The presence of total and hasMore is optional. They provide additional info: e.g. total: 50, values: \[first 10\], hasMore: true means there are 50 suggestions total and only 10 returned now.

*(Clients can use this to show "showing 10 of 50, type more to narrow down" etc.)*

### elicitation/create

*(Method for server to request info from user.)*

#### *ElicitRequest*

interface ElicitRequest {    
  method: "elicitation/create";    
  params: {    
    message: string;    
    requestedSchema: {    
      properties: { \[key: string\]: PrimitiveSchemaDefinition };    
      required?: string\[\];    
      type: "object";    
    };    
  };    
}

A server’s request to elicit information from the user[\[620\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **method** – "elicitation/create"[\[621\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ElicitRequest%20,type%3A%20%E2%80%9Cobject%E2%80%9D).

* **params**:

* **message** (string) – the prompt message to show the user (asking for something)[\[622\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,).

* **requestedSchema** – a JSON Schema (object type) defining the structure of the expected user input[\[622\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,). It contains:

  * properties: an object defining each field and its schema (each schema is one of StringSchema, NumberSchema, etc.)[\[623\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=message%3A%20string%3B%20requestedSchema%3A%20,).

  * required?: an array of property names that are required[\[624\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

  * type: fixed "object"[\[625\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=requestedSchema%3A%20,).

*(This maps to our earlier examples; e.g. properties might have "name": {type:"string"} etc., required: \["name"\].)*

#### *ElicitResult*

interface ElicitResult {    
  \_meta?: { \[key: string\]: unknown };    
  action: "accept" | "decline" | "cancel";    
  content?: { \[key: string\]: string | number | boolean };    
  \[key: string\]: unknown;    
}

The client’s response to an elicitation request[\[626\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata.

* **action** – one of "accept", "decline", "cancel"[\[627\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **content?** – if action is "accept", this contains an object with keys corresponding to the schema’s properties and values of types string/number/boolean fulfilling the request[\[628\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). If action is decline or cancel, this is typically omitted (or could be empty).

* Additional keys could be present if needed, but likely none.

*(This is what we saw in examples: for accept, content had "name": "...", etc., for decline/cancel content was not present.)*

### initialize

*(The initial handshake request from client to server.)*

#### *InitializeRequest*

interface InitializeRequest {    
  method: "initialize";    
  params: {    
    capabilities: ClientCapabilities;    
    clientInfo: Implementation;    
    protocolVersion: string;    
  };    
}

Sent by the client to begin initialization[\[629\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20InitializeRequest%20,).

* **method** – "initialize"[\[630\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,).

* **params**:

* **capabilities** – the ClientCapabilities object advertising what the client supports[\[631\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params).

* **clientInfo** – an Implementation object with the client’s name/version (and optional title)[\[632\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,Implementation%3B%20protocolVersion%3A%20string%3B). This allows server to identify the client.

* **protocolVersion** – a string indicating the latest MCP protocol version the client supports (format YYYY-MM-DD)[\[633\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=clientInfo%3A%20Implementation%3B%20protocolVersion%3A%20string%3B%20). In this case likely "2025-06-18".

*(If client supports older versions too, it still sends the latest it wants to use and expects server to negotiate down if needed.)*

#### *InitializeResult*

interface InitializeResult {    
  \_meta?: { \[key: string\]: unknown };    
  capabilities: ServerCapabilities;    
  instructions?: string;    
  protocolVersion: string;    
  serverInfo: Implementation;    
  \[key: string\]: unknown;    
}

The server’s response to initialize[\[634\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata (none defined currently for init result)[\[635\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **capabilities** – the ServerCapabilities object listing what the server supports[\[636\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20InitializeResult%20,key%3A%20string%5D%3A%20unknown%3B).

* **instructions?** (string) – optional human-readable instructions or guidelines for the client/user on how to use the server[\[637\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Servers can use this to convey usage info (e.g. "This server provides tools X, Y. Be sure to ..."). The client might display this to the user or incorporate into system prompt for the model. It's like server’s help message.

* **protocolVersion** (string) – the protocol version the server has agreed to use for this session[\[638\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=protocol%20Version). Could be the same as requested or a lower one if negotiated.

* **serverInfo** – Implementation info for the server (name and version, etc.)[\[639\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=capabilities%3A%20ServerCapabilities%3B%20instructions%3F%3A%20string%3B%20protocolVersion%3A,key%3A%20string%5D%3A%20unknown%3B).

* Additional fields can appear (some implementations might extend handshake with custom data in \_meta or beyond, though not standard).

*(If the server can’t support the requested version, it would likely not send an InitializeResult at all but an error prompting the client to try a different version. But if it does support, it might still adjust to an older version here. In either case, this is the authoritative version used henceforth, and the client should also send it in MCP-Protocol-Version header for HTTP.)*

### logging/setLevel

*(Client adjusting server log verbosity.)*

#### *SetLevelRequest*

interface SetLevelRequest {    
  method: "logging/setLevel";    
  params: { level: LoggingLevel };    
}

Client requests server to set minimum log level[\[640\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **method** – "logging/setLevel"[\[641\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20SetLevelRequest%20,).

* **params**:

* **level** – a LoggingLevel string, e.g. "info", "error"[\[642\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params).

If successful, server will presumably start sending notifications/message with logs at \>= that level. There’s no separate result object defined (could be EmptyResult indicating success).

*(No explicit SetLevelResult type is given; presumably an empty result or perhaps server returns the level it set (could just echo). But likely just an acknowledgement or no content response needed if using HTTP 202 for a notification, but since it's a request, probably it returns {} or something with \_meta maybe.)*

### notifications/cancelled

*(Notification to cancel a request.)*

#### *CancelledNotification*

interface CancelledNotification {    
  method: "notifications/cancelled";    
  params: { reason?: string; requestId: RequestId };    
}

Indicates cancellation of a previous request[\[643\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). This can be sent by client or server.

* **method** – "notifications/cancelled"[\[644\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **params**:

* **reason?** (string) – optional human-readable reason for cancellation[\[645\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Type%20declaration). May be logged or shown to user. E.g. "User aborted operation".

* **requestId** – the ID of the request being canceled[\[646\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). This must match a request that was previously sent and is still pending.

Important: One side should not attempt to cancel the initialize request (client MUST NOT cancel initialize)[\[647\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=A%20client%20MUST%20NOT%20attempt,request).

*(When the other side receives this, it should stop processing that request and not send a response except to acknowledge maybe. Any response that arrives after cancellation should be ignored by the canceler as well.)*

### notifications/initialized

*(Notification from client after it has finished initialization.)*

#### *InitializedNotification*

interface InitializedNotification {    
  method: "notifications/initialized";    
  params?: { \_meta?: { \[key: string\]: unknown }; \[key: string\]: unknown };    
}

Sent by client to server after it has completed initialization on its end[\[648\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **method** – "notifications/initialized"[\[649\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20InitializedNotification%20,).

* **params?** – optional object, currently not used (could include \_meta if needed)[\[650\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

*(This essentially signals "I'm ready, you can start sending requests (like server-\>client requests for roots, etc.) now". No response expected.)*

### notifications/message

*(Server-\>client log message.)*

#### *LoggingMessageNotification*

interface LoggingMessageNotification {    
  method: "notifications/message";    
  params: { data: unknown; level: LoggingLevel; logger?: string };    
}

A structured log message from server to client[\[651\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **method** – "notifications/message"[\[652\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20LoggingMessageNotification%20,).

* **params**:

* **data** (unknown) – the log content. Could be a string message or any JSON-serializable data (object, array, etc.)[\[653\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=method%3A%20%E2%80%9Cnotifications%2Fmessage%E2%80%9D%3B%20params%3A%20,)[\[654\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **level** (LoggingLevel) – severity of this log message[\[655\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). E.g. "error", "info".

* **logger?** (string) – optional name of the logger/source of this message[\[656\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). For instance, "database" or "auth" to categorize logs.

*(The client might display logs in a console UI, filter by level or component, etc. If the client never sent logging/setLevel, the server might default to sending certain logs or none at all. If it did, server sends \>= that level. The server can also decide to automatically send certain important messages even without an explicit setLevel request as per spec remark.)*

### notifications/progress

*(Progress update notifications.)*

#### *ProgressNotification*

interface ProgressNotification {    
  method: "notifications/progress";    
  params: {    
    message?: string;    
    progress: number;    
    progressToken: ProgressToken;    
    total?: number;    
  };    
}

An out-of-band progress update about a long-running request[\[657\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **method** – "notifications/progress"[\[658\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ProgressNotification%20,).

* **params**:

* **message?** (string) – optional human-readable message about current progress[\[659\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Type%20declaration), e.g. "Reticulating splines..." or "50% done".

* **progress** (number) – the current progress value[\[660\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=message%3F%3A%20string%3B%20progress%3A%20number%3B%20progressToken%3A,ProgressToken%3B%20total%3F%3A%20number%3B). This should monotonically increase; can be out of 100 if total is 100, or an absolute count of items processed, etc.

* **progressToken** (ProgressToken) – the token originally provided in the request’s \_meta to link this notification to that request[\[661\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **total?** (number) – optional total value if known[\[662\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). If known, progress/total gives a percentage. If unknown, omit or set progress as relative without known endpoint.

**Interpretation**: \- If total is known, progress value likely goes from 0 up to total. If total unknown, progress might be an incremental count or e.g. seconds of runtime. The spec says even if total unknown, progress should still increase (never reset or go backwards)[\[663\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=An%20optional%20message%20describing%20the,current%20progress). \- hasMore concept is not directly here; instead if progress \< total (when known) or always treat until an end condition outside this mechanism.

*(The client can use these to display a progress bar or percentage to the user. If progress surpasses or equals total (or no more progress notifications), the operation likely finished either with a result or cancellation.)*

### notifications/prompts/list\_changed

*(Server informs client prompt list changed.)*

#### *PromptListChangedNotification*

interface PromptListChangedNotification {    
  method: "notifications/prompts/list\_changed";    
  params?: { \_meta?: { \[key: string\]: unknown }; \[key: string\]: unknown };    
}

Server-\>client notification that available prompts have changed[\[664\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

No specific params needed (just a signal). It's optional to include a params object but nothing defined except maybe a \_meta if needed. The client should respond by calling prompts/list again to get new state.

### notifications/resources/list\_changed

*(Server informs client resource list changed.)*

#### *ResourceListChangedNotification*

interface ResourceListChangedNotification {    
  method: "notifications/resources/list\_changed";    
  params?: { \_meta?: { \[key: string\]: unknown }; \[key: string\]: unknown };    
}

Same pattern as above but for resources[\[665\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). No specific params; client should refresh via resources/list.

### notifications/resources/updated

*(Server informs client a specific resource was updated.)*

#### *ResourceUpdatedNotification*

interface ResourceUpdatedNotification {    
  method: "notifications/resources/updated";    
  params: { uri: string };    
}

Notification of an update to a subscribed resource[\[666\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **params**:

* **uri** (string) – the URI of the resource that changed[\[667\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params).

If a client had subscribed (resources/subscribe) to that URI or its containing resource, it knows to refresh it. If the resource updated is a sub-resource (like part of a larger resource), it's indicated that that part changed (the spec mentions it could be a sub-resource of what was subscribed)[\[668\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=A%20notification%20from%20the%20server,previously%20sent%20a%20resources%2Fsubscribe%20request).

### notifications/roots/list\_changed

*(Client informs server the roots list changed.)*

#### *RootsListChangedNotification*

interface RootsListChangedNotification {    
  method: "notifications/roots/list\_changed";    
  params?: { \_meta?: { \[key: string\]: unknown }; \[key: string\]: unknown };    
}

Client-\>server notification that the list of roots the client exposes has changed[\[669\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

Server should call roots/list again to get new roots. No specific params.

### notifications/tools/list\_changed

*(Server informs client tool list changed.)*

#### *ToolListChangedNotification*

interface ToolListChangedNotification {    
  method: "notifications/tools/list\_changed";    
  params?: { \_meta?: { \[key: string\]: unknown }; \[key: string\]: unknown };    
}

Server-\>client notification that available tools changed[\[670\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

Client should refresh via tools/list. No params.

### ping

*(Ping request either direction to check liveness.)*

#### *PingRequest*

interface PingRequest {    
  method: "ping";    
  params?: {    
    \_meta?: { progressToken?: ProgressToken; \[key: string\]: unknown };    
    \[key: string\]: unknown;    
  };    
}

A ping request (client or server can send) to verify the other side is responsive[\[671\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* It’s just "ping" with no required params. The optional params is only there to allow a progressToken in \_meta if someone wanted to track a ping (not usually needed).

The receiver should promptly respond with an empty result (just {}), indicating alive.

*(If no response in a timely manner, the sender might assume connection is stale and disconnect.)*

### prompts/get

*(Client retrieving a prompt’s content.)*

#### *GetPromptRequest*

interface GetPromptRequest {    
  method: "prompts/get";    
  params: { arguments?: { \[key: string\]: string }; name: string };    
}

Sent by client to server to fetch a prompt template[\[672\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **params**:

* **name** (string) – the prompt’s name to fetch[\[673\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params).

* **arguments?** ({ \[key: string\]: string }) – optional map of argument values to fill into the prompt template[\[673\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params). Only include if the prompt has arguments (matching those defined in prompt’s arguments list). If not provided, server may return a prompt with placeholders or possibly auto-complete using defaults if any.

*(E.g. name: "code\_review", arguments: { "code": "\<user's code\>" } as earlier example.)*

#### *GetPromptResult*

interface GetPromptResult {    
  \_meta?: { \[key: string\]: unknown };    
  description?: string;    
  messages: PromptMessage\[\];    
  \[key: string\]: unknown;    
}

Server’s response to prompts/get[\[674\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata.

* **description?** – description of the prompt (same as in Prompt definition, possibly)[\[675\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListPromptsResult%20,key%3A%20string%5D%3A%20unknown%3B). Might be included to give context. In example, "Code review prompt".

* **messages** (PromptMessage\[\]) – the sequence of messages that form the prompt template content[\[676\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=_meta%3F%3A%20,key%3A%20string%5D%3A%20unknown%3B).

*(There could be additional fields if needed, but usually just these. The messages is the main thing, containing user/assistant roles and content. The client will integrate these into the conversation – e.g. insert them as system or assistant messages, depending on how it's done. But likely the client will present the user messages to the model and treat assistant ones as context or expected answer structure.)*

### prompts/list

*(Client listing available prompts.)*

#### *ListPromptsRequest*

interface ListPromptsRequest {    
  method: "prompts/list";    
  params?: { cursor?: string };    
}

Request from client for prompt list[\[677\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **params?**:

* **cursor?** – if continuing a previous paginated list, include the last nextCursor you got to get next page[\[678\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Otherwise omitted or null.

#### *ListPromptsResult*

interface ListPromptsResult {    
  \_meta?: { \[key: string\]: unknown };    
  nextCursor?: string;    
  prompts: Prompt\[\];    
  \[key: string\]: unknown;    
}

Response from server with prompt list[\[679\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **\_meta?** – optional metadata.

* **nextCursor?** – if present, there are more prompts to fetch. Provide this value in a subsequent ListPromptsRequest to get the next page[\[680\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). If not present, this is the last page.

* **prompts** (Prompt\[\]) – array of Prompt definitions for the prompts available (on this page)[\[681\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=_meta%3F%3A%20,key%3A%20string%5D%3A%20unknown%3B).

*(As in example, one prompt with name, title, desc, args, etc.)*

### resources/list

*(Client listing resources.)*

#### *ListResourcesRequest*

interface ListResourcesRequest {    
  method: "resources/list";    
  params?: { cursor?: string };    
}

Client \-\> server request for resource list[\[682\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). Same pattern as others: optional cursor for pagination.

#### *ListResourcesResult*

interface ListResourcesResult {    
  \_meta?: { \[key: string\]: unknown };    
  nextCursor?: string;    
  resources: Resource\[\];    
  \[key: string\]: unknown;    
}

Server response with resources list[\[683\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **nextCursor?** – if more pages[\[684\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **resources** (Resource\[\]) – list of Resource descriptors on this page[\[685\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListResourcesResult%20,key%3A%20string%5D%3A%20unknown%3B).

### resources/read

*(Client reading a resource’s content.)*

#### *ReadResourceRequest*

interface ReadResourceRequest {    
  method: "resources/read";    
  params: { uri: string };    
}

Client request to server to read a resource’s contents[\[686\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **params**:

* **uri** – the resource’s URI to read[\[687\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params).

#### *ReadResourceResult*

interface ReadResourceResult {    
  \_meta?: { \[key: string\]: unknown };    
  contents: (TextResourceContents | BlobResourceContents)\[\];    
  \[key: string\]: unknown;    
}

Server’s response with resource content[\[688\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **contents** – an array of TextResourceContents or BlobResourceContents objects[\[689\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ReadResourceResult%20,key%3A%20string%5D%3A%20unknown%3B). Usually this will be one item (the file content), but it could include multiple pieces (perhaps if the resource is a composite or has multiple parts; the spec hints at sub-resources but not many details). For a plain file, it’s one TextResourceContents if text, or one BlobResourceContents if binary.

*(We saw example with one text content for main.rs. If a directory was read, maybe the server could return content listings as sub-resources? But then it wouldn't be text or blob, it would be resources listing—likely they'd not overload this, they'd have a different method if needed. So typically one content item in the array except maybe in specialized cases like reading multiple files at once if they allowed that, but the current API is one URI at a time. Possibly a resource could represent a multi-part file, like a HTML with images? But more likely not. So treat as array for future-proofing, but expect single element.)*

### resources/subscribe

*(Client subscribing to changes on a resource.)*

#### *SubscribeRequest*

interface SubscribeRequest {    
  method: "resources/subscribe";    
  params: { uri: string };    
}

Client asks server to send resources/updated notifications for a given resource URI[\[690\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

#### *(No explicit result type given, presumably an EmptyResult on success to acknowledge subscription, or maybe it returns some confirmation.)*

*(Likely, server could respond with a confirmation or some initial state. But given the design, probably it just returns an empty object result if subscription is set up, or an error if failed or not supported.)*

### resources/templates/list

*(Client listing resource templates.)*

#### *ListResourceTemplatesRequest*

interface ListResourceTemplatesRequest {    
  method: "resources/templates/list";    
  params?: { cursor?: string };    
}

Client request to list resource templates offered by the server[\[691\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). (Rare case, but supported.)

#### *ListResourceTemplatesResult*

interface ListResourceTemplatesResult {    
  \_meta?: { \[key: string\]: unknown };    
  nextCursor?: string;    
  resourceTemplates: ResourceTemplate\[\];    
  \[key: string\]: unknown;    
}

Server response with list of resource templates[\[692\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **resourceTemplates** – array of ResourceTemplate objects[\[693\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListResourceTemplatesResult%20,key%3A%20string%5D%3A%20unknown%3B).

* **nextCursor?** – for pagination if many templates (not likely many, but included)[\[694\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

### resources/unsubscribe

*(Client unsubscribing from resource updates.)*

#### *UnsubscribeRequest*

interface UnsubscribeRequest {    
  method: "resources/unsubscribe";    
  params: { uri: string };    
}

Client request to stop receiving updates for a resource it subscribed to[\[695\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

*(Likely an EmptyResult on success as acknowledgment.)*

### roots/list

*(Server listing client’s roots.)*

#### *ListRootsRequest*

interface ListRootsRequest {    
  method: "roots/list";    
  params?: {    
    \_meta?: { progressToken?: ProgressToken; \[key: string\]: unknown };    
    \[key: string\]: unknown;    
  };    
}

Server request for the list of roots from the client[\[696\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

It optionally could include a progressToken in \_meta (though listing roots likely quick, not needed).

*(No cursor for roots; presumably number of roots is small, so no pagination implemented. They didn't include a cursor field here. If a client had numerous roots, well, they might not design for that scenario heavily.)*

#### *ListRootsResult*

interface ListRootsResult {    
  \_meta?: { \[key: string\]: unknown };    
  roots: Root\[\];    
  \[key: string\]: unknown;    
}

Client’s response with the list of roots it provides[\[697\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **roots** – array of Root objects (each with uri and optional name)[\[698\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListRootsResult%20,key%3A%20string%5D%3A%20unknown%3B).

*(No pagination; presumably all roots sent in one go.)*

### sampling/createMessage

*(Server requesting an LLM message creation via client’s LLM connection.)*

#### *CreateMessageRequest*

interface CreateMessageRequest {    
  method: "sampling/createMessage";    
  params: {    
    includeContext?: "none" | "thisServer" | "allServers";    
    maxTokens: number;    
    messages: SamplingMessage\[\];    
    metadata?: object;    
    modelPreferences?: ModelPreferences;    
    stopSequences?: string\[\];    
    systemPrompt?: string;    
    temperature?: number;    
  };    
}

Server’s request to have the client’s LLM generate a message[\[699\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **includeContext?** – optional, how much context from other servers to include[\[700\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Type%20declaration). Can be:

* "none" – do not include any conversation history or other server data beyond the provided messages.

* "thisServer" – include context from this server only (maybe e.g. this server knows it provided certain info earlier).

* "allServers" – include context from all servers (full conversation).

This is a mechanism to allow server to ask for additional context. However, the spec notes the client *may ignore* this request[\[701\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=,%E2%80%9CallServers%E2%80%9D). It's just a hint: a server might say "allServers" if it thinks full conversation is needed, but the client might anyway restrict what the server gets to see (for privacy or security).

* **maxTokens** (number) – maximum tokens to generate[\[702\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,systemPrompt%3F%3A%20string%3B%20temperature%3F%3A%20number) (to prevent runaway generation). The client may choose to generate fewer (this is an upper bound)[\[703\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **messages** (SamplingMessage\[\]) – the conversation context messages provided by the server to seed the generation[\[704\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,systemPrompt%3F%3A%20string%3B%20temperature%3F%3A%20number). Typically includes one or more user or assistant turns that the server wants continued. For example, server might provide a user question in messages, or an entire conversation snippet, and expect the assistant to continue.

* **metadata?** (object) – optional model/provider-specific metadata to pass through to the LLM API[\[705\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). This could contain anything not standardized by MCP, like particular provider parameters, etc. The format is provider-specific. The client may ignore or use it if it understands.

* **modelPreferences?** (ModelPreferences) – server’s preferences for model selection (as defined above)[\[706\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=metadata%20is%20provider).

* **stopSequences?** (string\[\]) – optional list of strings that if encountered, should cause generation to stop[\[707\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20server%E2%80%99s%20preferences%20for%20which,client%20MAY%20ignore%20these%20preferences). Typically things like special tokens or end-of-message delineators. If included, client passes them to the LLM API.

* **systemPrompt?** (string) – an optional system prompt that the server suggests to use for this generation[\[708\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=A%20request%20from%20the%20server,decide%20whether%20to%20approve%20it)[\[709\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). The client *may modify or omit* this prompt[\[710\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). It's essentially allowing the server to insert instructions to the LLM. But the client might choose to merge it with its own system instructions or ignore it for safety reasons. If used, it might be appended to the conversation's beginning.

* **temperature?** (number) – optional sampling temperature for the LLM (0 \= deterministic, higher \= more random)[\[711\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). If omitted, the client will use its default or the model’s default.

*(Essentially, this is an API for server to ask the client: "Please have the AI generate a response given these messages and preferences." The client will presumably consult user if needed and then call the LLM. The design keeps client in control: for example, the client might present the messages to user for approval or might autopilot if user allowed, etc. But protocol-wise, server just asks.)*

#### *CreateMessageResult*

interface CreateMessageResult {    
  \_meta?: { \[key: string\]: unknown };    
  content: TextContent | ImageContent | AudioContent;    
  model: string;    
  role: Role;    
  stopReason?: string;    
  \[key: string\]: unknown;    
}

Client’s response to the server with the generated message[\[472\]\[472\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **content** – the generated content from the model (text, image, or audio)[\[474\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CreateMessageResult%20,key%3A%20string%5D%3A%20unknown%3B). Currently only one content block is returned (which is an assistant's reply typically). If the model can produce multimodal (e.g. text and image?), they'd need multiple content blocks, but the schema here only allows one. Possibly they'd have to encode multiple in one content (like an image as base64 inside text?), or this might be extended in future if needed. But likely one piece of content is expected.

* **model** (string) – the name of the model that was used to generate this message[\[712\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=model). E.g. "claude-3-sonnet-20240307" or "gpt-4". This lets the server know what model produced the content (maybe for attribution or further logic).

* **role** (Role) – the role of the generated message, likely "assistant" (since this is typically the AI's answer)[\[713\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=content%3A%20TextContent%20,key%3A%20string%5D%3A%20unknown%3B). Possibly if the server somehow requested user content generation (rare), it could be "user". But normally it's the assistant's output.

* **stopReason?** (string) – optional reason why generation stopped, if provided by the LLM API[\[714\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20name%20of%20the%20model,that%20generated%20the%20message). e.g. "endTurn", "maxTokens", "stopSequence", etc. This gives server a hint if the generation was cut off or naturally ended.

* There could be additional fields (like if model provided some usage info, tokens used, etc., the client might include in \_meta or additional keys, but not standardized in spec).

*(This is basically the assistant’s answer that the server was looking for. The client might also have shown it to user for approval (depending on settings) before sending it. But by the time server receives CreateMessageResult, presumably it's final content that can be shared with the server freely.)*

### tools/call

*(Client calling a tool on behalf of model.)*

#### *CallToolRequest*

interface CallToolRequest {    
  method: "tools/call";    
  params: { arguments?: { \[key: string\]: unknown }; name: string };    
}

Client’s request to server to invoke a tool[\[715\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **params**:

* **name** (string) – the name of the tool to execute[\[716\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CallToolRequest%20,).

* **arguments?** ({ \[key: string\]: unknown }) – an object with input arguments for the tool[\[717\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CallToolRequest%20,). The keys should match the tool’s inputSchema properties. If no arguments needed, this can be omitted or empty.

*(We saw e.g. name: "get\_weather", arguments: { location: "New York" }.)*

#### *CallToolResult*

interface CallToolResult {    
  \_meta?: { \[key: string\]: unknown };    
  content: ContentBlock\[\];    
  isError?: boolean;    
  structuredContent?: { \[key: string\]: unknown };    
  \[key: string\]: unknown;    
}

Server’s response to a tool call[\[718\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **content** (ContentBlock\[\]) – list of content blocks representing the tool’s unstructured output[\[719\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CallToolResult%20,key%3A%20string%5D%3A%20unknown). Could be text, images, etc., multiple items if needed. E.g. in get\_weather result, it was a single TextContent with weather info. If a tool returns both text and an image (conceivably), they'd both be in this array.

* **isError?** (boolean) – whether the tool execution indicates an error condition[\[476\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). If true, then the output is an error message or partial result, and the client/LLM should treat it accordingly (not a normal success).

* **structuredContent?** ({ \[key: string\]: unknown }) – optional structured output of the tool if an outputSchema was defined[\[475\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). This will be an object that should conform to that schema. The client/LLM can parse it for precise data extraction. The spec suggests that if outputSchema is provided, the server includes both structuredContent and a JSON string of it in the content array for backward compatibility[\[484\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Image%20Content).

* Other fields might include things like execution time or logs, but none are defined here.

*(We've explained earlier how isError is used to convey tool internal errors without using JSON-RPC error. If isError is not set or false, it's a normal successful result and presumably content contains the intended output. If structuredContent is present, the LLM could better parse it if it’s aware of the schema from the initial capability negotiation or documentation. In practice, the schema is available in the tool definition that the client had, so the client could even validate structuredContent before feeding to model or use it directly if needed.)*

### tools/list

*(Client listing available tools.)*

#### *ListToolsRequest*

interface ListToolsRequest {    
  method: "tools/list";    
  params?: { cursor?: string };    
}

Client’s request to get the list of tools from server[\[720\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=). With optional cursor for pagination.

#### *ListToolsResult*

interface ListToolsResult {    
  \_meta?: { \[key: string\]: unknown };    
  nextCursor?: string;    
  tools: Tool\[\];    
  \[key: string\]: unknown;    
}

Server’s response with tool list[\[721\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=).

* **tools** (Tool\[\]) – array of Tool definitions[\[722\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListToolsResult%20,key%3A%20string%5D%3A%20unknown%3B).

* **nextCursor?** – for pagination if needed[\[723\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Inherited%20from%20PaginatedResult).

*(Matches earlier example. Typically number of tools is modest, but the structure allows for larger sets if needed.)*

---

Finally, after enumerating all these, the spec is complete. It then has the "Was this page helpful?" UI and references to Pagination and such, which we don't need to replicate beyond including any citations we already did.

We have thus converted the entire MCP 2025-06-18 spec into an offline Markdown document, preserving all sections, headings, and including tables, code blocks, and images descriptions where needed. The output is comprehensive and organized for easy reading and reference offline.

---

[\[1\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Model%20Context%20Protocol%20,%E2%80%9CSHOULD%20NOT%E2%80%9D%2C%20%E2%80%9CRECOMMENDED%E2%80%9D%2C%20%E2%80%9CNOT%20RECOMMENDED%E2%80%9D) [\[2\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=protocol%20requirements%2C%20based%20on%20the,all%20capitals%2C%20as%20shown%20here) [\[3\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=schema,all%20capitals%2C%20as%20shown%20here) [\[4\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=MCP%20provides%20a%20standardized%20way,for%20applications%20to) [\[5\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=The%20protocol%20uses%20JSON,messages%20to%20establish%20communication%20between) [\[6\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=MCP%20takes%20some%20inspiration%20from,the%20ecosystem%20of%20AI%20applications) [\[7\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Base%20Protocol) [\[8\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=%2A%20JSON,Server%20and%20client%20capability%20negotiation) [\[9\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Servers%20offer%20any%20of%20the,following%20features%20to%20clients) [\[10\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Clients%20may%20offer%20the%20following,features%20to%20servers) [\[12\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=The%20Model%20Context%20Protocol%20enables,all%20implementors%20must%20carefully%20address) [\[13\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=1,before%20exposing%20user%20data%20to) [\[14\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=2.%20Data%20Privacy%20,Tool%20Safety) [\[15\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=3.%20Tool%20Safety%20,LLM%20Sampling%20Controls) [\[16\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=4.%20LLM%20Sampling%20Controls%20,limits%20server%20visibility%20into%20prompts) [\[17\]](https://modelcontextprotocol.io/specification/2025-06-18#:~:text=Implementation%20Guidelines) Specification \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)

[\[11\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=All%20implementations%20MUST%20support%20the,exactly%20the%20features%20they%20need) [\[48\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Protocol%20Revision%3A%202025) [\[49\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=The%20Model%20Context%20Protocol%20consists,key%20components%20that%20work%20together) [\[50\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=All%20messages%20between%20MCP%20clients,defines%20these%20types%20of%20messages) [\[51\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Copy) [\[52\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,requestor%20within%20the%20same%20session) [\[53\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Responses) [\[54\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,Error%20codes%20MUST%20be%20integers) [\[55\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=errors.%20Either%20a%20,Error%20codes%20MUST%20be%20integers) [\[56\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,Error%20codes%20MUST%20be%20integers) [\[57\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Notifications) [\[58\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=) [\[59\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Auth) [\[60\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=MCP%20provides%20an%20Authorization%20framework,the%20future%20of%20the%20protocol) [\[61\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=implementations%20using%20STDIO%20transport%20SHOULD,the%20future%20of%20the%20protocol) [\[62\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=The%20full%20specification%20of%20the,use%20with%20various%20automated%20tooling) [\[63\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=) [\[64\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=The%20,Prefix) [\[65\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=names%20have%20two%20segments%3A%20an,Prefix) [\[66\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,are%20all%20reserved) [\[67\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=,are%20all%20reserved) [\[68\]](https://modelcontextprotocol.io/specification/2025-06-18/basic#:~:text=Name%3A) Overview \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/basic](https://modelcontextprotocol.io/specification/2025-06-18/basic)

[\[18\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=This%20document%20lists%20changes%20made,26) [\[19\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=Major%20changes) [\[20\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=1.%20Remove%20support%20for%20JSON,371) [\[21\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=2,in%20a%20new%20%2013) [\[22\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=4,603) [\[23\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=access%20tokens.%20%28PR%20,enabling%20servers%20to%20request%20additional) [\[24\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=authorization%20spec%20and%20in%20a,%28PR) [\[25\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=information%20from%20users%20during%20interactions,Protocol) [\[26\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=,548) [\[27\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=Version,to%20MUST%20in%20Lifecycle%20Operation) [\[28\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=Other%20schema%20changes) [\[29\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=1.%20Add%20,resolved%20variables%20%28PR%20%23598) [\[30\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=2.%20Add%20,663) [\[31\]](https://modelcontextprotocol.io/specification/2025-06-18/changelog#:~:text=Full%20changelog) Key Changes \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/changelog](https://modelcontextprotocol.io/specification/2025-06-18/changelog)

[\[32\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=The%20Model%20Context%20Protocol%20,coordination%20between%20clients%20and%20servers) [\[33\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=The%20host%20process%20acts%20as,the%20container%20and%20coordinator) [\[34\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=Clients) [\[35\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,Maintains%20security%20boundaries%20between%20servers) [\[36\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=Servers) [\[37\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=MCP%20is%20built%20on%20several,inform%20its%20architecture%20and%20implementation) [\[38\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,are%20controlled%20by%20the%20host) [\[39\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=1,Shared%20protocol%20enables%20interoperability) [\[40\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,receive%20only%20necessary%20contextual%20information) [\[41\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,Host%20process%20enforces%20security%20boundaries) [\[42\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,Backwards%20compatibility%20is%20maintained) [\[43\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=Capability%20Negotiation) [\[44\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=Each%20capability%20unlocks%20specific%20protocol,For%20example) [\[45\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,declare%20support%20in%20its%20capabilities) [\[47\]](https://modelcontextprotocol.io/specification/2025-06-18/architecture#:~:text=,through%20extensions%20to%20the%20protocol) Architecture \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)

[\[46\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Category%20Capability%20Description%20Client%20,standard%20experimental%20features) [\[69\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Protocol%20Revision%3A%202025) [\[70\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=The%20Model%20Context%20Protocol%20,capability%20negotiation%20and%20state%20management) [\[71\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=1,Graceful%20termination%20of%20the%20connection) [\[72\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Initialization) [\[73\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=The%20client%20MUST%20initiate%20this,request%20containing) [\[74\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=The%20server%20MUST%20respond%20with,its%20own%20capabilities%20and%20information) [\[75\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=) [\[76\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=,notification) [\[77\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=,notification) [\[78\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Version%20Negotiation) [\[79\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=In%20the%20,server%E2%80%99s%20response%2C%20it%20SHOULD%20disconnect) [\[80\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=server%20supports%20the%20requested%20protocol,server%E2%80%99s%20response%2C%20it%20SHOULD%20disconnect) [\[81\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=If%20using%20HTTP%2C%20the%20client,Version%20Header%20section%20in%20Transports) [\[82\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Capability%20Negotiation) [\[83\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Category%20Capability%20Description%20Client%20,for%20LLM%20%2015%20requests) [\[84\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Category%20Capability%20Description%20Client%20,Support%20for%20server%20elicitation%20requests) [\[85\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Client%20,standard%20experimental%20features) [\[86\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Client%20,standard%20experimental%20features) [\[87\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,Exposes%20callable%20tools) [\[88\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,Emits%20structured%20%2023) [\[89\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,Emits%20structured%20%2023) [\[90\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,Supports%20argument%20%2025) [\[91\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,standard%20experimental%20features) [\[92\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Server%20,standard%20experimental%20features) [\[93\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Capability%20objects%20can%20describe%20sub,like) [\[94\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Operation) [\[95\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Shutdown) [\[96\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=During%20the%20shutdown%20phase%2C%20one,used%20to%20signal%20connection%20termination) [\[97\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=stdio) [\[98\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=For%20the%20stdio%20transport%2C%20the,client%20SHOULD%20initiate%20shutdown%20by) [\[99\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=after%20) [\[100\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=HTTP) [\[101\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Timeouts) [\[102\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Implementations%20SHOULD%20establish%20timeouts%20for,progress%20notifications%2C%20to%20limit%20the) [\[103\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=SDKs%20and%20other%20middleware%20SHOULD,a%20misbehaving%20client%20or%20server) [\[104\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=Error%20Handling) [\[105\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#:~:text=) Lifecycle \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)

[\[106\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Protocol%20Revision%3A%202025) [\[107\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=MCP%20uses%20JSON,server%20communication) [\[108\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,Streamable%20HTTP) [\[109\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=stdio) [\[110\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=sends%20messages%20to%20its%20standard,MUST%20NOT%20contain%20embedded%20newlines) [\[111\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,is%20not%20a%20valid%20MCP) [\[112\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,not%20a%20valid%20MCP%20message) [\[113\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,not%20a%20valid%20MCP%20message) [\[114\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=This%20replaces%20the%20HTTP%2BSSE%20transport,the%20backwards%20compatibility%20guide%20below) [\[115\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=In%20the%20Streamable%20HTTP%20transport%2C,https%3A%2F%2Fexample.com%2Fmcp) [\[116\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=that%20can%20handle%20multiple%20client,https%3A%2F%2Fexample.com%2Fmcp) [\[117\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Events%20en,https%3A%2F%2Fexample.com%2Fmcp) [\[118\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Security%20Warning) [\[119\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,proper%20authentication%20for%20all%20connections) [\[120\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Sending%20Messages%20to%20the%20Server) [\[121\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Every%20JSON,request%20to%20the%20MCP%20endpoint) [\[122\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,202%20Accepted%20with%20no%20body) [\[123\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=2,body%20MAY%20comprise%20a%20JSON) [\[124\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=4,client%20MUST%20support%20both%20these) [\[125\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=status%20code%20%28e,MUST%20support%20both%20these%20cases) [\[126\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=cases,request%2C%20unless%20the%20session%20expires) [\[127\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,the%20server%20SHOULD%20close%20the) [\[128\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=request.%20,SHOULD%20close%20the%20SSE%20stream) [\[129\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=SSE%20stream.%20,CancelledNotification) [\[130\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Therefore%3A%20,the%20server%20MAY%20make%20the) [\[131\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,server%20initiates%20an%20SSE%20stream) [\[132\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,Method%20Not%20Allowed%2C%20indicating%20that) [\[133\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=the%20client%20first%20sending%20data,RPC) [\[134\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=4,SSE%20stream%20at%20any%20time) [\[135\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,with%20a%20previous%20client%20request) [\[136\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,SSE%20stream%20at%20any%20time) [\[137\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Multiple%20Connections) [\[138\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,by%20making%20the%20stream%20resumable) [\[139\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Resumability%20and%20Redelivery) [\[140\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,messages%20that%20would%20have%20been) [\[141\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=2,delivered%20on%20a%20different%20stream) [\[142\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=an%20HTTP%20GET%20to%20the,delivered%20on%20a%20different%20stream) [\[143\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,delivered%20on%20a%20different%20stream) [\[144\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=different%20stream) [\[145\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Session%20Management) [\[146\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,Session) [\[147\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=initialization%20time%2C%20by%20including%20it,of%20their%20subsequent%20HTTP%20requests) [\[148\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=0x21%20to%200x7E%29,with%20HTTP%20404%20Not%20Found) [\[149\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=clients%20using%20the%20Streamable%20HTTP,time%2C%20after%20which%20it%20MUST) [\[150\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,DELETE%20to%20the%20MCP%20endpoint) [\[151\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=respond%20to%20requests%20containing%20that,HTTP%20405%20Method%20Not%20Allowed) [\[152\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,allow%20clients%20to%20terminate%20sessions) [\[153\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=leaving%20the%20client%20application,allow%20clients%20to%20terminate%20sessions) [\[154\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Protocol%20Version%20Header) [\[155\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=If%20using%20HTTP%2C%20the%20client,server%20SHOULD%20assume%20protocol%20version) [\[156\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=MCP%20server%20to%20respond%20based,400%20Bad%20Request) [\[157\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=the%20one%20negotiated%20during%20initialization,400%20Bad%20Request) [\[158\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Clients%20and%20servers%20can%20maintain,to%20support%20older%20clients%20should) [\[159\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=HTTP%2BSSE%20transport%20,to%20support%20older%20clients%20should) [\[160\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Clients%20wanting%20to%20support%20older,servers%20should) [\[161\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=1,event%20as%20the%20first%20event) [\[162\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=,transport%20for%20all%20subsequent%20communication) [\[163\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Custom%20Transports) [\[164\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#:~:text=Clients%20and%20servers%20MAY%20implement,exchange%20patterns%20to%20aid%20interoperability) Transports \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/basic/transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)

[\[165\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Protocol%20Revision%3A%202025) [\[166\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=The%20Model%20Context%20Protocol%20provides,based%20transports) [\[167\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Authorization%20is%20OPTIONAL%20for%20MCP,When%20supported) [\[168\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Standards%20Compliance) [\[169\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=interoperability%20while%20maintaining%20simplicity%3A) [\[170\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,RFC7591) [\[171\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,RFC7591) [\[172\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,0%20Protected%20Resource%20Metadata%20%28RFC9728) [\[173\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Roles) [\[174\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=A%20protected%20MCP%20server%20acts,It%20may%20be) [\[175\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=server%20is%20responsible%20for%20interacting,authorization%20server%20to%20a%20client) [\[176\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Overview) [\[177\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=1,0) [\[178\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=2,0%20Authorization%20Server%20Metadata) [\[179\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=3,0%20Authorization%20Server%20Metadata) [\[180\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Authorization%20Server%20Location) [\[181\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20servers%20MUST%20implement%20the,lies%20with%20the%20MCP%20client) [\[182\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Resource%20Metadata%20,MUST%20be%20able%20to%20parse) [\[183\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=following%20the%20guidelines%20specified%20in,responses%20from%20the%20MCP%20server) [\[184\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Server%20Metadata%20Discovery) [\[185\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Dynamic%20Client%20Registration) [\[186\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,implement%20their%20own%20registration%20policies) [\[187\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Any%20authorization%20servers%20that%20do,clients%20will%20have%20to%20either) [\[188\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=to%20provide%20alternative%20ways%20to,clients%20will%20have%20to%20either) [\[189\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=The%20complete%20Authorization%20flow%20proceeds,as%20follows) [\[190\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Resource%20Parameter%20Implementation) [\[191\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=which%20the%20token%20is%20being,parameter) [\[192\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=1,in%20RFC%208707%20Section%202) [\[193\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=For%20the%20purposes%20of%20this,Examples%20of%20valid%20canonical) [\[194\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=defined%20as%20the%20resource%20identifier,Examples%20of%20valid%20canonical%20URIs) [\[195\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=,significant%20for%20the%20specific%20resource) [\[196\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=in%20RFC%208707,Examples%20of%20valid%20canonical%20URIs) [\[197\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Examples%20of%20invalid%20canonical%20URIs%3A) [\[198\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=%2A%20%60https%3A%2F%2Fmcp.example.com) [\[199\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=For%20example%2C%20if%20accessing%20an,the%20authorization%20request%20would%20include) [\[200\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20clients%20MUST%20send%20this,whether%20authorization%20servers%20support%20it) [\[201\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Token%20Requirements) [\[202\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=1,1) [\[203\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Authorization%3A%20Bearer%20%3Caccess) [\[204\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Note%20that%20authorization%20MUST%20be,of%20the%20same%20logical%20session) [\[205\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Example%20request%3A) [\[206\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20servers%2C%20acting%20in%20their,MUST%20NOT%20accept%20or%20transit) [\[207\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=access%20tokens%20as%20described%20in,MUST%20NOT%20accept%20or%20transit) [\[208\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=as%20the%20intended%20audience%2C%20according,MUST%20NOT%20accept%20or%20transit) [\[209\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=as%20the%20intended%20audience%2C%20according,or%20transit%20any%20other%20tokens) [\[210\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Error%20Handling) [\[211\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Security%20Considerations) [\[212\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=RFC%208707%20Resource%20Indicators%20provide,enable%20current%20and%20future%20adoption) [\[213\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=issued%20for%20their%20use) [\[214\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Attackers%20who%20obtain%20tokens%20stored,1%20%E2%80%9CToken%20Endpoint%20Extension%E2%80%9D) [\[215\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=to%20resource%20servers,1%20%E2%80%9CToken%20Endpoint%20Extension%E2%80%9D) [\[216\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=follow%20OAuth%20best%20practices%2C%20as,1%20%E2%80%9CToken%20Endpoint%20Extension%E2%80%9D) [\[217\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Communication%20Security) [\[218\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Implementations%20MUST%20follow%20OAuth%202,Specifically) [\[219\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Authorization%20Code%20Protection) [\[220\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=token%20or%20otherwise%20make%20use,requestor%20can%20exchange%20an%20authorization) [\[221\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Open%20Redirection) [\[222\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=An%20attacker%20may%20craft%20malicious,Authorization%20servers%20SHOULD%20only%20automatically) [\[223\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=parameters%20in%20the%20authorization%20code,to%20make%20the%20correct%20decision) [\[227\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=Access%20Token%20Privilege%20Restriction) [\[228\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20servers%20MUST%20validate%20access,Practices%20Token%20Passthrough%20section%20for) [\[229\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=two%20critical%20dimensions%3A) [\[230\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=2,Practices%20guide%20for%20additional%20details) [\[231\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=MCP%20servers%20MUST%20validate%20access,it%20may%20act%20as%20an) [\[232\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=server%20MUST%20follow%20the%20guidelines,MCP%20clients%20MUST%20implement) [\[233\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=token,This%20requirement%20aligns%20with) [\[234\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#:~:text=OAuth%20client%20to%20them,be%20misused%20across%20different%20services) Authorization \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)

[\[224\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Confused%20Deputy%20Problem) [\[225\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Attack%20Description) [\[226\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=MCP%20proxy%20servers%20using%20static,which%20may%20require%20additional%20consent) [\[235\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=This%20document%20provides%20security%20considerations,0%20security%20best%20practices) [\[236\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=When%20an%20MCP%20proxy%20server,the%20following%20attack%20becomes%20possible) [\[237\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=dynamically%20registered%20client%20ID%204,without%20the%20user%E2%80%99s%20explicit%20approval) [\[238\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=,API%20as%20the%20compromised%20user) [\[239\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=MCP%20proxy%20servers%20using%20static,which%20may%20require%20additional%20consent) [\[240\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Token%20Passthrough) [\[241\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Risks) [\[242\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=,Accountability%20and%20Audit%20Trail%20Issues) [\[243\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=service%2C%20they%20bypass%20these%20controls,is%20actually%20forwarding%20the%20tokens) [\[244\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=service%2C%20they%20bypass%20these%20controls,investigation%2C%20controls%2C%20and%20auditing%20more) [\[245\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=server%20that%20is%20actually%20forwarding,Trust%20Boundary%20Issues) [\[246\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=,it%20might%20need%20to%20add) [\[247\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=,to%20evolve%20the%20security%20model) [\[248\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Mitigation) [\[249\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Session%20Hijacking) [\[250\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=When%20you%20have%20multiple%20stateful,possible%3A%20Session%20Hijack%20Prompt%20Injection) [\[251\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=affect%20the%20tools%20that%20are,malicious%20payload%2C%20leading%20to%20potential) [\[252\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Session%20Hijack%20Impersonation) [\[253\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Mitigation) [\[254\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=verify%20all%20inbound%20requests,ensures%20that%20even%20if%20an) [\[255\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=Generated%20session%20IDs%20%28e,ensures%20that%20even%20if%20an) [\[256\]](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices#:~:text=attacker,optionally%20leverage%20additional%20unique%20identifiers) Security Best Practices \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/basic/security\_best\_practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)

[\[257\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Protocol%20Revision%3A%202025) [\[258\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=The%20Model%20Context%20Protocol%20,notifications%20when%20that%20list%20changes) [\[259\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=User%20Interaction%20Model) [\[260\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Roots%20in%20MCP%20are%20typically,any%20specific%20user%20interaction%20model) [\[261\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Capabilities) [\[262\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=) [\[263\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Listing%20Roots) [\[264\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=To%20retrieve%20roots%2C%20servers%20send,request%3A%20Request) [\[265\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Response%3A) [\[266\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Root%20List%20Changes) [\[267\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Root) [\[268\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=A%20root%20definition%20includes%3A) [\[269\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=A%20root%20definition%20includes%3A) [\[270\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Project%20Directory) [\[271\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Multiple%20Repositories) [\[272\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Error%20Handling) [\[273\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Clients%20SHOULD%20return%20standard%20JSON,errors%20for%20common%20failure%20cases) [\[274\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=,32603) [\[275\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=Security%20Considerations) [\[276\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=,all%20paths%20against%20provided%20roots) [\[277\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=1.%20Clients%20SHOULD%3A%20,Respect%20root%20boundaries%20in%20operations) [\[278\]](https://modelcontextprotocol.io/specification/2025-06-18/client/roots#:~:text=1.%20Clients%20SHOULD%3A%20,Handle%20root%20list%20changes%20gracefully) Roots \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/client/roots](https://modelcontextprotocol.io/specification/2025-06-18/client/roots)

[\[279\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Protocol%20Revision%3A%202025) [\[280\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=The%20Model%20Context%20Protocol%20,MCP%20servers%20in%20their%20prompts) [\[281\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=User%20Interaction%20Model) [\[282\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=For%20trust%20%26%20safety%20and,Applications%20SHOULD) [\[283\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Capabilities) [\[284\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Creating%20Messages) [\[285\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=,) [\[286\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=%5D%2C%20,0.5) [\[287\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Response%3A) [\[288\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=,20240307%22%2C%20%22stopReason%22%3A%20%22endTurn%22%20%7D) [\[289\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=,20240307%22%2C%20%22stopReason%22%3A%20%22endTurn%22) [\[290\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Messages) [\[291\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=%7B%20,to%20any%20Claude%20model) [\[292\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=) [\[293\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Image%20Content) [\[294\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Audio%20Content) [\[295\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Model%20Preferences) [\[296\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Capability%20Priorities) [\[297\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Model%20Hints) [\[298\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=While%20priorities%20help%20select%20models,specific%20models%20or%20model%20families) [\[299\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=,advisory%E2%80%94clients%20make%20final%20model%20selection) [\[300\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=Copy) [\[301\]](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling#:~:text=The%20client%20processes%20these%20preferences,pro%60%20based%20on%20similar%20capabilities) Sampling \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/client/sampling](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling)

[\[302\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Protocol%20Revision%3A%202025) [\[303\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Elicitation%20is%20newly%20introduced%20in,evolve%20in%20future%20protocol%20versions) [\[304\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=The%20Model%20Context%20Protocol%20,JSON%20schemas%20to%20validate%20responses) [\[305\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=User%20Interaction%20Model) [\[306\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Elicitation%20in%20MCP%20allows%20servers,any%20specific%20user%20interaction%20model) [\[307\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=For%20trust%20%26%20safety%20and,security) [\[308\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=,elicitation%20to%20request%20sensitive%20information) [\[309\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Capabilities) [\[310\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Creating%20Elicitation%20Requests) [\[311\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=To%20request%20information%20from%20a,request) [\[312\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Simple%20Text%20Request) [\[313\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Structured%20Data%20Request) [\[314\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=,) [\[315\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Response%3A) [\[316\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Reject%20Response%20Example%3A) [\[317\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Copy) [\[318\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=%7B%20,30) [\[319\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Cancel%20Response%20Example%3A) [\[320\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Request%20Schema) [\[321\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=The%20,objects%20with%20primitive%20properties%20only) [\[322\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Copy) [\[323\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=The%20schema%20is%20restricted%20to,these%20primitive%20types) [\[324\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=,time%22) [\[325\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=3) [\[326\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=4) [\[327\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=1) [\[328\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Copy) [\[329\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=2) [\[330\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Copy) [\[331\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Clients%20can%20use%20this%20schema,to) [\[332\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Note%20that%20complex%20nested%20structures%2C,supported%20to%20simplify%20client%20implementation) [\[333\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Response%20Actions) [\[334\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=The%20three%20response%20actions%20are%3A) [\[335\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=1.%20Accept%20%28%60action%3A%20,without%20making%20an%20explicit%20choice) [\[336\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=1.%20Accept%20%28%60action%3A%20,dismissed%20without%20making%20an%20explicit) [\[337\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=,clicked%20outside%2C%20pressed%20Escape%2C%20etc) [\[338\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=Security%20Considerations) [\[339\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=1,way%20that%20makes%20it%20clear) [\[519\]](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation#:~:text=%7B%20,) Elicitation \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation)

[\[340\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=Servers%20provide%20the%20fundamental%20building,clients%2C%20servers%2C%20and%20language%20models) [\[341\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=%2A%20Prompts%3A%20Pre,perform%20actions%20or%20retrieve%20information) [\[342\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=interactions%20,perform%20actions%20or%20retrieve%20information) [\[343\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=,perform%20actions%20or%20retrieve%20information) [\[344\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=Primitive%20Control%20Description%20Example%20Prompts,API%20POST%20requests%2C%20file%20writing) [\[345\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=Primitive%20Control%20Description%20Example%20Prompts,API%20POST%20requests%2C%20file%20writing) [\[346\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=commands%2C%20menu%20options%20Resources%20Application,API%20POST%20requests%2C%20file%20writing) [\[347\]](https://modelcontextprotocol.io/specification/2025-06-18/server#:~:text=client%20File%20contents%2C%20git%20history,API%20POST%20requests%2C%20file%20writing) Overview \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/server](https://modelcontextprotocol.io/specification/2025-06-18/server)

[\[348\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Protocol%20Revision%3A%202025) [\[349\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=The%20Model%20Context%20Protocol%20,provide%20arguments%20to%20customize%20them) [\[350\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=User%20Interaction%20Model) [\[351\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Prompts%20are%20designed%20to%20be,For%20example%2C%20as%20slash%20commands) [\[352\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=discover%20and%20invoke%20available%20prompts,any%20specific%20user%20interaction%20model) [\[353\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Capabilities) [\[354\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=%7B%20,true%20%7D%20%7D) [\[355\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Listing%20Prompts) [\[356\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=To%20retrieve%20available%20prompts%2C%20clients,Request) [\[357\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=%7B%20,value%22%20%7D) [\[358\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Copy) [\[359\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=,%5B) [\[360\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Getting%20a%20Prompt) [\[361\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=,%7D%20%7D) [\[362\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Response%3A) [\[363\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=,text) [\[364\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=List%20Changed%20Notification) [\[365\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Error%20Handling) [\[366\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Implementation%20Considerations) [\[367\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=1,parties%20SHOULD%20respect%20capability%20negotiation) [\[368\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Security) [\[518\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=) [\[520\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Image%20Content) [\[521\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Image%20content%20allows%20including%20visual,information%20in%20messages) [\[522\]](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts#:~:text=Copy) Prompts \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/server/prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)

[\[369\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Protocol%20Revision%3A%202025) [\[370\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=The%20Model%20Context%20Protocol%20,uniquely%20identified%20by%20a%20URI) [\[371\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=context%20to%20language%20models%2C%20such,uniquely%20identified%20by%20a%20URI) [\[372\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Resources%20in%20MCP%20are%20designed,For%20example%2C%20applications%20could) [\[373\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=applications%20could%3A) [\[374\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,or%20the%20AI%20model%E2%80%99s%20selection) [\[375\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Image%3A%20Example%20of%20resource%20context,any%20specific%20user%20interaction%20model) [\[376\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Capabilities) [\[377\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=The%20capability%20supports%20two%20optional,features) [\[378\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,list%20of%20available%20resources%20changes) [\[379\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Both%20,support%20neither%2C%20either%2C%20or%20both) [\[380\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Copy) [\[381\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Copy) [\[382\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=) [\[383\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Listing%20Resources) [\[384\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=To%20discover%20available%20resources%2C%20clients,Request) [\[385\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Response%3A) [\[386\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,rust) [\[387\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Reading%20Resources) [\[388\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=To%20retrieve%20resource%20contents%2C%20clients,request%3A%20Request) [\[389\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Response%3A) [\[390\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,%7D%20%5D%20%7D) [\[391\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Resource%20Templates) [\[392\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Copy) [\[393\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Response%3A) [\[394\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=%7B%20,Project%20Files) [\[395\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=List%20Changed%20Notification) [\[396\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Subscriptions) [\[397\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=%7B%20,%7D) [\[398\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Update%20Notification%3A) [\[417\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Annotations) [\[418\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=,12T15%3A00%3A58Z) [\[419\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=resource,12T15%3A00%3A58Z) [\[420\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Copy) [\[421\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Clients%20can%20use%20these%20annotations,to) [\[422\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Common%20URI%20Schemes) [\[423\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Custom%20URI%20Schemes) [\[424\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=https%3A%2F%2F) [\[425\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Used%20to%20represent%20a%20resource,resource%20contents%20over%20the%20internet) [\[426\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=file%3A%2F%2F) [\[427\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Used%20to%20identify%20resources%20that,have%20a%20standard%20MIME%20type) [\[428\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=git%3A%2F%2F) [\[429\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Custom%20URI%20Schemes) [\[433\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=Security%20Considerations) [\[434\]](https://modelcontextprotocol.io/specification/2025-06-18/server/resources#:~:text=1,SHOULD%20be%20checked%20before%20operations) Resources \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/server/resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources)

[\[399\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceContents%20,mimeType%3F%3A%20string%3B%20uri%3A%20string%3B) [\[400\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceLink%20,number%3B%20title%3F%3A%20string%3B%20type%3A%20%E2%80%9Cresource_link%E2%80%9D) [\[401\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=annotations%3F%3A%20Annotations%3B%20description%3F%3A%20string%3B%20mimeType%3F%3A,type%3A%20%E2%80%9Cresource_link%E2%80%9D%3B%20uri%3A%20string%3B) [\[402\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=annotations%3F%3A%20Annotations%3B%20description%3F%3A%20string%3B%20mimeType%3F%3A,title%3F%3A%20string%3B%20uriTemplate%3A%20string%3B) [\[403\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=annotations%3F%3A%20Annotations%3B%20description%3F%3A%20string%3B%20mimeType%3F%3A,string%3B%20type%3A%20%E2%80%9Cresource_link%E2%80%9D%3B%20uri%3A%20string) [\[404\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=mimeType%3F%3A%20string%3B%20name%3A%20string%3B%20size%3F%3A,type%3A%20%E2%80%9Cresource_link%E2%80%9D%3B%20uri%3A%20string%3B) [\[405\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[406\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[407\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=text) [\[410\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[411\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceTemplate%20,title%3F%3A%20string%3B%20uriTemplate%3A%20string%3B) [\[412\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=mimeType%3F%3A%20string%3B%20name%3A%20string%3B%20title%3F%3A,string%3B%20uriTemplate%3A%20string%3B) [\[413\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[414\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[415\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[416\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[454\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[455\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[456\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[457\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=name) [\[458\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[459\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Optional%20additional%20tool%20information) [\[460\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=input%20Schema) [\[461\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[462\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[463\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[464\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=outputSchema%3F%3A%20,type%3A%20%E2%80%9Cobject%E2%80%9D%3B) [\[465\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ToolAnnotations%20,readOnlyHint%3F%3A%20boolean%3B%20title%3F%3A%20string%3B) [\[466\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[467\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[468\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[469\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[470\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[471\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=NOTE%3A%20all%20properties%20in%20ToolAnnotations,title) [\[472\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[473\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=model) [\[474\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CreateMessageResult%20,key%3A%20string%5D%3A%20unknown%3B) [\[475\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[476\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[477\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[478\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Any%20errors%20that%20originate%20from,correct) [\[479\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Any%20errors%20that%20originate%20from,correct) [\[480\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=isError%3F%3A%20boolean) [\[523\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ModelHint%20,) [\[524\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[525\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Additional%20information%20about%20the%20error,error%20information%2C%20nested%20errors%20etc) [\[526\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[527\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=method%3A%20string%3B%20params%3F%3A%20,) [\[528\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[529\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[530\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20JSONRPCRequest%20,) [\[531\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=jsonrpc%3A%20%E2%80%9C2,) [\[532\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[533\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=,key%3A%20string%5D%3A%20unknown) [\[534\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[535\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20JSONRPCResponse%20,0%E2%80%9D%3B%20result%3A%20Result%3B) [\[536\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[537\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20severity%20of%20a%20log,message) [\[538\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[539\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[540\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20client%20SHOULD%20treat%20this,a%20model%20name%3B%20for%20example) [\[541\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[542\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[543\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[544\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[545\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=dimensions%20to%20help%20clients%20make,selection%20for%20their%20use%20case) [\[546\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=that%20the%20first%20match%20is,taken) [\[547\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=minimum%3F%3A%20number%3B%20title%3F%3A%20string%3B%20type%3A,%E2%80%9Cinteger%E2%80%9D%3B) [\[548\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[549\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[550\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[551\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[552\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=See%20General%20fields%3A%20_meta%20for,usage) [\[553\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=A%20list%20of%20arguments%20to,use%20for%20templating%20the%20prompt) [\[554\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=name) [\[555\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Inherited%20from%20BaseMetadata) [\[556\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[557\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[558\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=name) [\[559\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[560\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[561\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[562\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20PromptMessage%20,role%3A%20Role%3B) [\[563\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[564\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[565\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=name) [\[566\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[567\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[568\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[569\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Inherited%20from%20BaseMetadata) [\[570\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri) [\[571\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri%3A%20string) [\[572\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20URI%20of%20this%20resource) [\[573\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[574\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[575\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=mimeType%3F%3A%20string) [\[576\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[577\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=type%3A%20%E2%80%9Cresource_link%E2%80%9D%3B%20uri%3A%20string%3B%20) [\[578\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[579\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[580\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[581\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[582\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[583\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri%20Template) [\[584\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ResourceTemplateReference%20,uri%3A%20string%3B) [\[585\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[586\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[587\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[588\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[589\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[590\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri) [\[591\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri%3A%20string) [\[592\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[593\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20SamplingMessage%20,AudioContent%3B%20role%3A%20Role%3B) [\[594\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[595\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[596\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[597\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Experimental%2C%20non,server%20supports) [\[598\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[599\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[600\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[601\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[602\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20StringSchema%20,title%3F%3A%20string%3B%20type%3A%20%E2%80%9Cstring%E2%80%9D%3B) [\[603\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[604\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[605\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[606\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=text) [\[607\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[608\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Inherited%20from%20ResourceContents) [\[609\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=uri) [\[610\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[611\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CompleteRequest%20,) [\[612\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=,value%3A%20string) [\[613\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20argument%E2%80%99s%20information) [\[614\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=,) [\[615\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Additional%2C%20optional%20context%20for%20completions) [\[616\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Previously,template%20or%20prompt) [\[617\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[618\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Type%20declaration) [\[619\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[620\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[621\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ElicitRequest%20,type%3A%20%E2%80%9Cobject%E2%80%9D) [\[622\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,) [\[623\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=message%3A%20string%3B%20requestedSchema%3A%20,) [\[624\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[625\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=requestedSchema%3A%20,) [\[626\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[627\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[628\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[629\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20InitializeRequest%20,) [\[630\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,) [\[631\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params) [\[632\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,Implementation%3B%20protocolVersion%3A%20string%3B) [\[633\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=clientInfo%3A%20Implementation%3B%20protocolVersion%3A%20string%3B%20) [\[634\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[635\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[636\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20InitializeResult%20,key%3A%20string%5D%3A%20unknown%3B) [\[637\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[638\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=protocol%20Version) [\[639\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=capabilities%3A%20ServerCapabilities%3B%20instructions%3F%3A%20string%3B%20protocolVersion%3A,key%3A%20string%5D%3A%20unknown%3B) [\[640\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[641\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20SetLevelRequest%20,) [\[642\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params) [\[643\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[644\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[645\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Type%20declaration) [\[646\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[647\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=A%20client%20MUST%20NOT%20attempt,request) [\[648\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[649\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20InitializedNotification%20,) [\[650\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[651\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[652\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20LoggingMessageNotification%20,) [\[653\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=method%3A%20%E2%80%9Cnotifications%2Fmessage%E2%80%9D%3B%20params%3A%20,) [\[654\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[655\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[656\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[657\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[658\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ProgressNotification%20,) [\[659\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Type%20declaration) [\[660\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=message%3F%3A%20string%3B%20progress%3A%20number%3B%20progressToken%3A,ProgressToken%3B%20total%3F%3A%20number%3B) [\[661\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[662\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[663\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=An%20optional%20message%20describing%20the,current%20progress) [\[664\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[665\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[666\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[667\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params) [\[668\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=A%20notification%20from%20the%20server,previously%20sent%20a%20resources%2Fsubscribe%20request) [\[669\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[670\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[671\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[672\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[673\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params) [\[674\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[675\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListPromptsResult%20,key%3A%20string%5D%3A%20unknown%3B) [\[676\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=_meta%3F%3A%20,key%3A%20string%5D%3A%20unknown%3B) [\[677\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[678\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[679\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[680\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[681\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=_meta%3F%3A%20,key%3A%20string%5D%3A%20unknown%3B) [\[682\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[683\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[684\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[685\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListResourcesResult%20,key%3A%20string%5D%3A%20unknown%3B) [\[686\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[687\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params) [\[688\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[689\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ReadResourceResult%20,key%3A%20string%5D%3A%20unknown%3B) [\[690\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[691\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[692\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[693\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListResourceTemplatesResult%20,key%3A%20string%5D%3A%20unknown%3B) [\[694\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[695\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[696\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[697\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[698\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListRootsResult%20,key%3A%20string%5D%3A%20unknown%3B) [\[699\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[700\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Type%20declaration) [\[701\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=,%E2%80%9CallServers%E2%80%9D) [\[702\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,systemPrompt%3F%3A%20string%3B%20temperature%3F%3A%20number) [\[703\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[704\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=params%3A%20,systemPrompt%3F%3A%20string%3B%20temperature%3F%3A%20number) [\[705\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[706\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=metadata%20is%20provider) [\[707\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20server%E2%80%99s%20preferences%20for%20which,client%20MAY%20ignore%20these%20preferences) [\[708\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=A%20request%20from%20the%20server,decide%20whether%20to%20approve%20it) [\[709\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[710\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[711\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[712\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=model) [\[713\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=content%3A%20TextContent%20,key%3A%20string%5D%3A%20unknown%3B) [\[714\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=The%20name%20of%20the%20model,that%20generated%20the%20message) [\[715\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[716\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CallToolRequest%20,) [\[717\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CallToolRequest%20,) [\[718\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[719\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20CallToolResult%20,key%3A%20string%5D%3A%20unknown) [\[720\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[721\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=) [\[722\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=interface%20ListToolsResult%20,key%3A%20string%5D%3A%20unknown%3B) [\[723\]](https://modelcontextprotocol.io/specification/2025-06-18/schema#:~:text=Inherited%20from%20PaginatedResult) Schema Reference \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/schema](https://modelcontextprotocol.io/specification/2025-06-18/schema)

[\[408\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=) [\[409\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Inherited%20from%20ResourceContents.) [\[493\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Optional%20annotations%20for%20the%20client,objects%20are%20used%20or%20displayed) [\[494\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=) [\[495\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=) [\[496\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=priority%3F%3A%20number) [\[497\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Audio%20provided%20to%20or%20from,an%20LLM) [\[498\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=%60Optional%60) [\[499\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=) [\[500\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=data) [\[501\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=mime%20Type) [\[502\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=interface%20AudioContent%20%5C,) [\[503\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=%60Optional%60) [\[504\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=blob) [\[505\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=) [\[506\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=uri) [\[507\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=) [\[508\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=) [\[509\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Present%20if%20the%20client%20supports,elicitation%20from%20the%20server) [\[510\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Experimental%2C%20non,client%20supports) [\[511\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=Whether%20the%20client%20supports%20notifications,changes%20to%20the%20roots%20list) [\[512\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=) [\[513\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=) [\[514\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=%60Optional%60) [\[515\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=See%20General%20fields%3A%20,meta%60%20usage) [\[516\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=%5C_meta%3F%3A%20%5C,) [\[517\]](https://modelcontextprotocol.io/llms-full.txt#:~:text=annotations%3F%3A%20Annotations%3B%20resource%3A%20TextResourceContents%20,) modelcontextprotocol.io

[https://modelcontextprotocol.io/llms-full.txt](https://modelcontextprotocol.io/llms-full.txt)

[\[430\]](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/pagination#:~:text=Error%20Handling) [\[431\]](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/pagination#:~:text=Error%20Handling) [\[432\]](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/pagination#:~:text=Invalid%20cursors%20SHOULD%20result%20in,32602%20%28Invalid%20params) Pagination \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/pagination](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/pagination)

[\[435\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Protocol%20Revision%3A%202025) [\[436\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=The%20Model%20Context%20Protocol%20,includes%20metadata%20describing%20its%20schema) [\[437\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=invoked%20by%20language%20models,includes%20metadata%20describing%20its%20schema) [\[438\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=User%20Interaction%20Model) [\[439\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=itself%20does%20not%20mandate%20any,specific%20user%20interaction%20model) [\[440\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=For%20trust%20%26%20safety%20and,Applications%20SHOULD) [\[441\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Capabilities) [\[442\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,) [\[443\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Listing%20Tools) [\[444\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=To%20discover%20available%20tools%2C%20clients,Request) [\[445\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Response%3A) [\[446\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,City%20name%20or%20zip%20code) [\[447\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,) [\[448\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Calling%20Tools) [\[449\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Calling%20Tools) [\[450\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,%7D%20%7D) [\[451\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=) [\[452\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,false) [\[453\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=%7B%20,false) [\[481\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,tool%20behavior) [\[482\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=%7B%20,) [\[483\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=) [\[484\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Image%20Content) [\[485\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Tools%20use%20two%20error%20reporting,mechanisms) [\[486\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=1.%20Protocol%20Errors%3A%20Standard%20JSON,Business%20logic%20errors) [\[487\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=%7B%20,%7D) [\[488\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Copy) [\[489\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=Security%20Considerations) [\[490\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=1.%20Servers%20MUST%3A%20,Rate%20limit%20tool%20invocations) [\[491\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=2.%20Clients%20SHOULD%3A%20,tool%20usage%20for%20audit%20purposes) [\[492\]](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#:~:text=,tool%20usage%20for%20audit%20purposes) Tools \- Model Context Protocol

[https://modelcontextprotocol.io/specification/2025-06-18/server/tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)