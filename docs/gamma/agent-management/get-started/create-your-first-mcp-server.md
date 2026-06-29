---
hidden: false
noIndex: true
---

# Create your first MCP server
<!-- GAP-STRUCTURAL: Missing procedural content source -->

This quickstart walks you through creating an MCP Proxy in front of an upstream MCP server, so that every tool invocation passes through the AI Gateway with authentication, policy enforcement, and observability. You'll use the simplest configuration — Proxy mode with API key security — to get a governed MCP server running in under five minutes.

{% hint style="info" %}
For a complete reference on all MCP Proxy options, including Studio mode, see [Create an MCP proxy](../build/create-an-mcp-proxy.md).
{% endhint %}

## Prerequisites

* Access to a running Gamma console instance
* An upstream MCP server accessible via HTTP (e.g., `https://mcp.example.com/mcp`)

## Step 1: Open the MCP Proxy wizard

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Build**.
3. Select **Create MCP Proxy**.

The console opens the MCP Proxy creation wizard. Select **Proxy mode**, enter a name like "My First MCP Server" and a context path, then select **Next**.

## Step 2: Configure security

The next step defines how consumers authenticate when calling tools through this MCP Proxy.

For this quickstart, select **API Key**. API key security lets you track and control which consumers invoke tools through your MCP Proxy without setting up an external identity provider.

Select **Next** to proceed.

## Step 3: Connect to the upstream server

Provide the connection details for the upstream MCP server:

1. Under **Upstream server**, enter the URL of your MCP endpoint (e.g., `https://mcp.example.com/mcp`). The Gateway uses Streamable HTTP transport by default.
2. Under **Upstream Authentication**, select **No upstream auth** (passthrough) for this quickstart, or enter your static credentials if your server requires them.

Select **Next** to proceed.

## Step 4: Review and create

Review the MCP Proxy configuration and select **Create**.

The console creates the MCP Proxy and registers it in the AI Gateway. The MCP Proxy now sits in front of your upstream MCP server — every tool invocation flows through the AI Gateway, where authentication, policies, and observability are applied.

## Step 5: Verify tool invocations

Once the MCP Proxy is created, verify that it can receive connections.

1. Note the MCP Proxy URL displayed in the console after creation.
2. Test the connection using `curl` with your API key:

```bash
curl -X POST https://api.your-gateway.com/mcp/my-first-server \
  -H "X-Gravitee-Api-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

3. Confirm the JSON-RPC response matches what the upstream server returns.

## Next steps

* **Add policies** — Apply fine-grained authorization to control which consumers can invoke specific tools. See [Add policies to your MCP server](../build/configure-your-mcp/add-policies-to-mcp-server.md).
* **Configure mediation** — Set up token exchange and credential mediation for upstream MCP servers that require their own OAuth. See [Configure your MCP proxy](../build/configure-your-mcp/README.md).
* **Create a Composite MCP Server** — Compose tools from multiple upstream servers, APIs, and events into a single governed MCP server. See [Create an MCP Studio](../build/create-an-mcp-studio.md).
