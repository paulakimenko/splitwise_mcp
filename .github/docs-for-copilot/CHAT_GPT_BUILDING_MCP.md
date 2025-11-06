Building MCP servers for ChatGPT and API integrations - OpenAI API

\===============

[](https://platform.openai.com/docs/overview)

[Docs Docs](https://platform.openai.com/docs)[API reference API](https://platform.openai.com/docs/api-reference/introduction)

Log in[Sign up](https://platform.openai.com/signup)

Search K

Get started

[Overview](https://platform.openai.com/docs/overview)

[Quickstart](https://platform.openai.com/docs/quickstart)

[Models](https://platform.openai.com/docs/models)

[Pricing](https://platform.openai.com/docs/pricing)

[Libraries](https://platform.openai.com/docs/libraries)

Core concepts

[Text generation](https://platform.openai.com/docs/guides/text)

[Images and vision](https://platform.openai.com/docs/guides/images-vision)

[Audio and speech](https://platform.openai.com/docs/guides/audio)

[Structured output](https://platform.openai.com/docs/guides/structured-outputs)

[Function calling](https://platform.openai.com/docs/guides/function-calling)

[Using GPT-5](https://platform.openai.com/docs/guides/latest-model)

[Migrate to Responses API](https://platform.openai.com/docs/guides/migrate-to-responses)

Agents

[Overview](https://platform.openai.com/docs/guides/agents)

Build agents

Deploy in your product

Optimize

[Voice agents](https://platform.openai.com/docs/guides/voice-agents)

Tools

[Using tools](https://platform.openai.com/docs/guides/tools)

[Connectors and MCP](https://platform.openai.com/docs/guides/tools-connectors-mcp)

[Web search](https://platform.openai.com/docs/guides/tools-web-search)

[Code interpreter](https://platform.openai.com/docs/guides/tools-code-interpreter)

File search and retrieval

More tools

Run and scale

[Conversation state](https://platform.openai.com/docs/guides/conversation-state)

[Background mode](https://platform.openai.com/docs/guides/background)

[Streaming](https://platform.openai.com/docs/guides/streaming-responses)

[Webhooks](https://platform.openai.com/docs/guides/webhooks)

[File inputs](https://platform.openai.com/docs/guides/pdf-files)

Prompting

Reasoning

Evaluation

[Getting started](https://platform.openai.com/docs/guides/evaluation-getting-started)

[Working with evals](https://platform.openai.com/docs/guides/evals)

[Prompt optimizer](https://platform.openai.com/docs/guides/prompt-optimizer)

[External models](https://platform.openai.com/docs/guides/external-models)

[Best practices](https://platform.openai.com/docs/guides/evaluation-best-practices)

Realtime API

[Overview](https://platform.openai.com/docs/guides/realtime)

Connect

Usage

Model optimization

[Optimization cycle](https://platform.openai.com/docs/guides/model-optimization)

Fine-tuning

[Graders](https://platform.openai.com/docs/guides/graders)

Specialized models

[Image generation](https://platform.openai.com/docs/guides/image-generation)

[Video generation](https://platform.openai.com/docs/guides/video-generation)

[Text to speech](https://platform.openai.com/docs/guides/text-to-speech)

[Speech to text](https://platform.openai.com/docs/guides/speech-to-text)

[Deep research](https://platform.openai.com/docs/guides/deep-research)

[Embeddings](https://platform.openai.com/docs/guides/embeddings)

[Moderation](https://platform.openai.com/docs/guides/moderation)

Coding agents

[Codex cloud](https://developers.openai.com/codex/cloud)

[Agent internet access](https://developers.openai.com/codex/cloud/agent-internet)

[Local shell tool](https://platform.openai.com/docs/guides/tools-local-shell)

[Codex CLI](https://developers.openai.com/codex/cli)

[Codex IDE](https://developers.openai.com/codex/ide)

[Codex changelog](https://developers.openai.com/codex/changelog)

Going live

[Production best practices](https://platform.openai.com/docs/guides/production-best-practices)

Latency optimization

Cost optimization

[Accuracy optimization](https://platform.openai.com/docs/guides/optimizing-llm-accuracy)

Safety

Specialized APIs

Assistants API

Resources

[Terms and policies](https://openai.com/policies)

[Changelog](https://platform.openai.com/docs/changelog)

[Your data](https://platform.openai.com/docs/guides/your-data)

[Rate limits](https://platform.openai.com/docs/guides/rate-limits)

[Deprecations](https://platform.openai.com/docs/deprecations)

[MCP for deep research](https://platform.openai.com/docs/mcp)

[Developer mode](https://platform.openai.com/docs/guides/developer-mode)

ChatGPT Actions

[Cookbook](https://cookbook.openai.com/)[Forum](https://community.openai.com/categories)

# Building MCP servers for ChatGPT and API integrations

Build an MCP server to use with ChatGPT connectors, deep research, or API integrations.

Copy page

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) is an open protocol that's becoming the industry standard for extending AI models with additional tools and knowledge. Remote MCP servers can be used to connect models over the Internet to new data sources and capabilities.

In this guide, we'll cover how to build a remote MCP server that reads data from a private data source (a [vector store](https://platform.openai.com/docs/guides/retrieval)) and makes it available in ChatGPT via connectors in chat and deep research, as well as [via API](https://platform.openai.com/docs/guides/deep-research).

**Note**: You can build and use full MCP connectors with the **developer mode** beta. Pro and Plus users can enable it under **Settings → Connectors → Advanced → Developer mode** to access the complete set of MCP tools. Learn more in the [Developer mode guide](https://platform.openai.com/docs/guides/developer-mode).

## Configure a data source

You can use data from any source to power a remote MCP server, but for simplicity, we will use [vector stores](https://platform.openai.com/docs/guides/retrieval) in the OpenAI API. Begin by uploading a PDF document to a new vector store - [you can use this public domain 19th century book about cats](https://cdn.openai.com/API/docs/cats.pdf) for an example.

You can upload files and create a vector store [in the dashboard here](https://platform.openai.com/storage/vector_stores), or you can create vector stores and upload files via API. [Follow the vector store guide](https://platform.openai.com/docs/guides/retrieval) to set up a vector store and upload a file to it.

Make a note of the vector store's unique ID to use in the example to follow.

![Image 1: vector store configuration](https://cdn.openai.com/API/docs/images/vector_store.png)

## Create an MCP server

Next, let's create a remote MCP server that will do search queries against our vector store, and be able to return document content for files with a given ID.

In this example, we are going to build our MCP server using Python and [FastMCP](https://github.com/jlowin/fastmcp). A full implementation of the server will be provided at the end of this section, along with instructions for running it on [Replit](https://replit.com/).

Note that there are a number of other MCP server frameworks you can use in a variety of programming languages. Whichever framework you use though, the tool definitions in your server will need to conform to the shape described here.

To work with ChatGPT Connectors or deep research (in ChatGPT or via API), your MCP server must implement two tools - `search` and `fetch`.

### `search` tool

The `search` tool is responsible for returning a list of relevant search results from your MCP server's data source, given a user's query.

_Arguments:_

A single query string.

_Returns:_

An object with a single key, `results`, whose value is an array of result objects. Each result object should include:

*   `id` - a unique ID for the document or search result item
*   `title` - human-readable title.
*   `url` - canonical URL for citation.

In MCP, tool results must be returned as [a content array](https://modelcontextprotocol.io/docs/learn/architecture#understanding-the-tool-execution-response) containing one or more "content items." Each content item has a type (such as `text`, `image`, or `resource`) and a payload.

For the `search` tool, you should return **exactly one** content item with:

*   `type: "text"`
*   `text`: a JSON-encoded string matching the results array schema above.

The final tool response should look like:

```json
1
2
3
4
5
6
7
8
{
  "content": [
    {
      "type": "text",
      "text": "{\"results\":[{\"id\":\"doc-1\",\"title\":\"...\",\"url\":\"...\"}]}"
    }
  ]
}
```

### `fetch` tool

The fetch tool is used to retrieve the full contents of a search result document or item.

_Arguments:_

A string which is a unique identifier for the search document.

_Returns:_

A single object with the following properties:

*   `id` - a unique ID for the document or search result item
*   `title` - a string title for the search result item
*   `text` - The full text of the document or item
*   `url` - a URL to the document or search result item. Useful for citing specific resources in research.
*   `metadata` - an optional key/value pairing of data about the result

In MCP, tool results must be returned as [a content array](https://modelcontextprotocol.io/docs/learn/architecture#understanding-the-tool-execution-response) containing one or more "content items." Each content item has a `type` (such as `text`, `image`, or `resource`) and a payload.

In this case, the `fetch` tool must return exactly [one content item with `type: "text"`](https://modelcontextprotocol.io/specification/2025-06-18/server/tools#tool-result). The `text` field should be a JSON-encoded string of the document object following the schema above.

The final tool response should look like:

```json
1
2
3
4
5
6
7
8
{
  "content": [
    {
      "type": "text",
      "text": "{\"id\":\"doc-1\",\"title\":\"...\",\"text\":\"full text...\",\"url\":\"https://example.com/doc\",\"metadata\":{\"source\":\"vector_store\"}}"
    }
  ]
}
```

### Server example

An easy way to try out this example MCP server is using [Replit](https://replit.com/). You can configure this sample application with your own API credentials and vector store information to try it yourself.

[Example MCP server on Replit Remix the server example on Replit to test live.](https://replit.com/@kwhinnery-oai/DeepResearchServer?v=1#README.md) A full implementation of both the `search` and `fetch` tools in FastMCP is below also for convenience.

Full implementation - FastMCP server

```python
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
"""
Sample MCP Server for ChatGPT Integration

This server implements the Model Context Protocol (MCP) with search and fetch
capabilities designed to work with ChatGPT's chat and deep research features.
"""

import logging
import os
from typing import Dict, List, Any

from fastmcp import FastMCP
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
VECTOR_STORE_ID = os.environ.get("VECTOR_STORE_ID", "")

# Initialize OpenAI client
openai_client = OpenAI()

server_instructions = """
This MCP server provides search and document retrieval capabilities
for chat and deep research connectors. Use the search tool to find relevant documents
based on keywords, then use the fetch tool to retrieve complete
document content with citations.
"""

def create_server():
    """Create and configure the MCP server with search and fetch tools."""

    # Initialize the FastMCP server
    mcp = FastMCP(name="Sample MCP Server",
                  instructions=server_instructions)

    @mcp.tool()
    async def search(query: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for documents using OpenAI Vector Store search.

        This tool searches through the vector store to find semantically relevant matches.
        Returns a list of search results with basic information. Use the fetch tool to get
        complete document content.

        Args:
            query: Search query string. Natural language queries work best for semantic search.

        Returns:
            Dictionary with 'results' key containing list of matching documents.
            Each result includes id, title, text snippet, and optional URL.
        """
        if not query or not query.strip():
            return {"results": []}

        if not openai_client:
            logger.error("OpenAI client not initialized - API key missing")
            raise ValueError(
                "OpenAI API key is required for vector store search")

        # Search the vector store using OpenAI API
        logger.info(f"Searching {VECTOR_STORE_ID} for query: '{query}'")

        response = openai_client.vector_stores.search(
            vector_store_id=VECTOR_STORE_ID, query=query)

        results = []

        # Process the vector store search results
        if hasattr(response, 'data') and response.data:
            for i, item in enumerate(response.data):
                # Extract file_id, filename, and content
                item_id = getattr(item, 'file_id', f"vs_{i}")
                item_filename = getattr(item, 'filename', f"Document {i+1}")

                # Extract text content from the content array
                content_list = getattr(item, 'content', [])
                text_content = ""
                if content_list and len(content_list) > 0:
                    # Get text from the first content item
                    first_content = content_list[0]
                    if hasattr(first_content, 'text'):
                        text_content = first_content.text
                    elif isinstance(first_content, dict):
                        text_content = first_content.get('text', '')

                if not text_content:
                    text_content = "No content available"

                # Create a snippet from content
                text_snippet = text_content[:200] + "..." if len(
                    text_content) > 200 else text_content

                result = {
                    "id": item_id,
                    "title": item_filename,
                    "text": text_snippet,
                    "url":
                    f"https://platform.openai.com/storage/files/{item_id}"
                }

                results.append(result)

        logger.info(f"Vector store search returned {len(results)} results")
        return {"results": results}

    @mcp.tool()
    async def fetch(id: str) -> Dict[str, Any]:
        """
        Retrieve complete document content by ID for detailed
        analysis and citation. This tool fetches the full document
        content from OpenAI Vector Store. Use this after finding
        relevant documents with the search tool to get complete
        information for analysis and proper citation.

        Args:
            id: File ID from vector store (file-xxx) or local document ID

        Returns:
            Complete document with id, title, full text content,
            optional URL, and metadata

        Raises:
            ValueError: If the specified ID is not found
        """
        if not id:
            raise ValueError("Document ID is required")

        if not openai_client:
            logger.error("OpenAI client not initialized - API key missing")
            raise ValueError(
                "OpenAI API key is required for vector store file retrieval")

        logger.info(f"Fetching content from vector store for file ID: {id}")

        # Fetch file content from vector store
        content_response = openai_client.vector_stores.files.content(
            vector_store_id=VECTOR_STORE_ID, file_id=id)

        # Get file metadata
        file_info = openai_client.vector_stores.files.retrieve(
            vector_store_id=VECTOR_STORE_ID, file_id=id)

        # Extract content from paginated response
        file_content = ""
        if hasattr(content_response, 'data') and content_response.data:
            # Combine all content chunks from FileContentResponse objects
            content_parts = []
            for content_item in content_response.data:
                if hasattr(content_item, 'text'):
                    content_parts.append(content_item.text)
            file_content = "\n".join(content_parts)
        else:
            file_content = "No content available"

        # Use filename as title and create proper URL for citations
        filename = getattr(file_info, 'filename', f"Document {id}")

        result = {
            "id": id,
            "title": filename,
            "text": file_content,
            "url": f"https://platform.openai.com/storage/files/{id}",
            "metadata": None
        }

        # Add metadata if available from file info
        if hasattr(file_info, 'attributes') and file_info.attributes:
            result["metadata"] = file_info.attributes

        logger.info(f"Fetched vector store file: {id}")
        return result

    return mcp

def main():
    """Main function to start the MCP server."""
    # Verify OpenAI client is initialized
    if not openai_client:
        logger.error(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )
        raise ValueError("OpenAI API key is required")

    logger.info(f"Using vector store: {VECTOR_STORE_ID}")

    # Create the MCP server
    server = create_server()

    # Configure and start the server
    logger.info("Starting MCP server on 0.0.0.0:8000")
    logger.info("Server will be accessible via SSE transport")

    try:
        # Use FastMCP's built-in run method with SSE transport
        server.run(transport="sse", host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    main()
```

Replit setup

On Replit, you will need to configure two environment variables in the "Secrets" UI:

*   `OPENAI_API_KEY` - Your standard OpenAI API key
*   `VECTOR_STORE_ID` - The unique identifier of a vector store that can be used for search - the one you created earlier.

On free Replit accounts, server URLs are active for as long as the editor is active, so while you are testing, you'll need to keep the browser tab open. You can get a URL for your MCP server by clicking on the chainlink icon:

![Image 2: replit configuration](https://cdn.openai.com/API/docs/images/replit.png)

In the long dev URL, ensure it ends with `/sse/`, which is the server-sent events (streaming) interface to the MCP server. This is the URL you will use to import your connector both via API and ChatGPT. An example Replit URL looks like:

```text
https://777xxx.janeway.replit.dev/sse/
```

## Test and connect your MCP server

You can test your MCP server with a deep research model [in the prompts dashboard](https://platform.openai.com/chat). Create a new prompt, or edit an existing one, and add a new MCP tool to the prompt configuration. Remember that MCP servers used via API for deep research have to be configured with no approval required.

![Image 3: prompts configuration](https://cdn.openai.com/API/docs/images/prompts_mcp.png)

Once you have configured your MCP server, you can chat with a model using it via the Prompts UI.

![Image 4: prompts chat](https://cdn.openai.com/API/docs/images/chat_prompts_mcp.png)

You can test the MCP server using the Responses API directly with a request like this one:

```bash
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
curl https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
  "model": "o4-mini-deep-research",
  "input": [
    {
      "role": "developer",
      "content": [
        {
          "type": "input_text",
          "text": "You are a research assistant that searches MCP servers to find answers to your questions."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Are cats attached to their homes? Give a succinct one page overview."
        }
      ]
    }
  ],
  "reasoning": {
    "summary": "auto"
  },
  "tools": [
    {
      "type": "mcp",
      "server_label": "cats",
      "server_url": "https://777ff573-9947-4b9c-8982-658fa40c7d09-00-3le96u7wsymx.janeway.replit.dev/sse/",
      "allowed_tools": [
        "search",
        "fetch"
      ],
      "require_approval": "never"
    }
  ]
}'
```

### Handle authentication

As someone building a custom remote MCP server, authorization and authentication help you protect your data. We recommend using OAuth and [dynamic client registration](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization#2-4-dynamic-client-registration). To learn more about the protocol's authentication, read the [MCP user guide](https://modelcontextprotocol.io/docs/concepts/transports#authentication-and-authorization) or see the [authorization specification](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization).

If you connect your custom remote MCP server in ChatGPT, users in your workspace will get an OAuth flow to your application.

### Connect in ChatGPT

1.  Import your remote MCP servers directly in [ChatGPT settings](https://chatgpt.com/#settings).
2.  Connect your server in the **Connectors** tab. It should now be visible in the composer's "Deep Research" and "Use Connectors" tools. You may have to add the server as a source.
3.  Test your server by running some prompts.

## Risks and safety

Custom MCP servers enable you to connect your ChatGPT workspace to external applications, which allows ChatGPT to access, send and receive data in these applications. Please note that custom MCP servers are not developed or verified by OpenAI, and are third-party services that are subject to their own terms and conditions.

If you come across a malicious MCP server, please report it to [security@openai.com](https://platform.openai.com/docs/mcp).

### Prompt injection-related risks

Prompt injections are a form of attack where an attacker embeds malicious instructions in content that one of our models is likely to encounter–such as a webpage–with the intention that the instructions override ChatGPT’s intended behavior. If the model obeys the injected instructions it may take actions the user and developer never intended—including sending private data to an external destination.

For example, you might ask ChatGPT to find a restaurant for a group dinner by checking your calendar and recent emails. While researching, it might encounter a malicious comment—essentially a harmful piece of content designed to trick the agent into performing unintended actions—directing it to retrieve a password reset code from Gmail and send it to a malicious website.

Below is a table of specific scenarios to consider. We recommend reviewing this table carefully to inform your decision about whether to use custom MCPs.

| Scenario / Risk | Is it safe if I trust the MCP’s developer? | What can I do to reduce risk? |
| --- | --- | --- |
| An attacker may somehow insert a prompt injection attack into data accessible via the MCP. _Examples:_ • For a customer support MCP, an attacker could send you a customer support request with a prompt injection attack. | Trusting a MCP’s developer does not make this safe. For this to be safe you need to trust _all content that can be accessed within the MCP_. | • Do not use a MCP if it could contain malicious or untrusted user input, even if you trust the developer of the MCP. • Configure access to minimize how many people have access to the MCP. |
| A malicious MCP may request excessive parameters to a read or write action. _Example:_ • An employee flight booking MCP could expose a read action to get a flight schedule, but request parameters including `summaryOfConversation`, `userAnnualIncome`, `userHomeAddress`. | Trusting a MCP’s developer does not necessarily make this safe. A MCP’s developer may consider it reasonable to be requesting certain data that you do not consider acceptable to share. | • When sideloading MCPs, carefully review the parameters being requested for each action and ensure there is no privacy overreach. |
| An attacker may use a prompt injection attack to trick ChatGPT into fetching sensitive data from a custom MCP, to then be sent to the attacker. _Example:_ • An attacker may deliver a prompt injection attack to one of the enterprise users via a different MCP (e.g. for email), where the attack attempts to trick ChatGPT into reading sensitive data from some internal tool MCP and then attempt to exfiltrate it. | Trusting a MCP’s developer does not make this safe. Everything within the new MCP could be safe and trusted since the risk is this data being stolen by attacks coming from a different malicious source. | • _ChatGPT is designed to protect users_, but attackers may attempt to steal your data, so be aware of the risk and consider whether taking it makes sense. • Configure access to minimize how many people have access to MCPs with particularly sensitive data. |
| An attacker may use a prompt injection attack to exfiltrate sensitive information through a write action to a custom MCP. _Example:_ • An attacker uses a prompt injection attack (via a different MCP) to trick ChatGPT into fetching sensitive data, and then exfiltrates it by tricking ChatGPT into using a MCP for a customer support system to send it to the attacker. | Trusting a MCP’s developer does not make this safe. Even if you fully trust the MCP, if write actions have any consequences that can be observed by an attacker, they could attempt to take advantage of it. | • Users should review write actions carefully when they happen (to ensure they were intended and do not contain any data that shouldn’t be shared). |
| An attacker may use a prompt injection attack to exfiltrate sensitive information through a read action to a malicious custom MCP (since these can be logged by the MCP). | This attack only works if the MCP is malicious, or if the MCP incorrectly marks write actions as read actions. If you trust a MCP’s developer to correctly only mark read actions as _read_, and trust that developer to not attempt to steal data, then this risk is likely minimal. | • Only use MCPs from developers that you trust (though note this isn’t sufficient to make it safe). |
| An attacker may use a prompt injection attack to trick ChatGPT into taking a harmful or destructive write action via a custom MCP that users did not intend. | Trusting a MCP’s developer does not make this safe. Everything within the new MCP could be safe and trusted, and this risk still exists since the attack comes from a different malicious source. | • Users should carefully review write actions to ensure they are intended and correct. • ChatGPT is designed to protect users, but attackers may attempt to trick ChatGPT into taking unintended write actions. • Configure access to minimize how many people have access to MCPs with particularly sensitive data. |

### Non-prompt injection related risks

There are additional risks of custom MCPs, unrelated to prompt injection attacks:

*   **Write actions can increase both the usefulness and the risks of MCP servers**, because they make it possible for the server to take potentially destructive actions rather than simply providing information back to ChatGPT. ChatGPT currently requires manual confirmation in any conversation before write actions can be taken. The confirmation will flag potentially sensitive data but you should only use write actions in situations where you have carefully considered, and are comfortable with, the possibility that ChatGPT might make a mistake involving such an action. It is possible for write actions to occur even if the MCP server has tagged the action as read only, making it even more important that you trust the custom MCP server before deploying to ChatGPT.
*   **Any MCP server may receive sensitive data as part of querying**. Even when the server is not malicious, it will have access to whatever data ChatGPT supplies during the interaction, potentially including sensitive data the user may earlier have provided to ChatGPT. For instance, such data could be included in queries ChatGPT sends to the MCP server when using deep research or chat connectors.

### Connecting to trusted servers

We recommend that you do not connect to a custom MCP server unless you know and trust the underlying application.

For example, always pick official servers hosted by the service providers themselves (e.g., connect to the Stripe server hosted by Stripe themselves on mcp.stripe.com, instead of an unofficial Stripe MCP server hosted by a third party). Because there aren't many official MCP servers today, you may be tempted to use a MCP server hosted by an organization that doesn't operate that server and simply proxies requests to that service via an API. This is not recommended—and you should only connect to an MCP once you’ve carefully reviewed how they use your data and have verified that you can trust the server. When building and connecting to your own MCP server, double check that it's the correct server. Be very careful with which data you provide in response to requests to your MCP server, and with how you treat the data sent to you as part of OpenAI calling your MCP server.

Your remote MCP server permits others to connect OpenAI to your services and allows OpenAI to access, send and receive data, and take action in these services. Avoid putting any sensitive information in the JSON for your tools, and avoid storing any sensitive information from ChatGPT users accessing your remote MCP server.

As someone building an MCP server, don't put anything malicious in your tool definitions.

*   [Overview Overview](https://platform.openai.com/docs/mcp#page-top)
*   [Configure a data source Configure a data source](https://platform.openai.com/docs/mcp#configure-a-data-source)
*   [Create an MCP server Create an MCP server](https://platform.openai.com/docs/mcp#create-an-mcp-server)
*   [Test and connect your MCP server Test and connect your MCP server](https://platform.openai.com/docs/mcp#test-and-connect-your-mcp-server)
*   [Risks and safety Risks and safety](https://platform.openai.com/docs/mcp#risks-and-safety)