---
hidden: false
noIndex: false
description: Create your first MCP Proxy in Gravitee Gamma using Proxy mode with API key security.
---

# Create your first MCP server

This quickstart walks you through creating an MCP Proxy in front of an upstream MCP server. Every tool invocation then passes through the AI Gateway with authentication, policy enforcement, and observability. This quickstart uses the simplest configuration—Proxy mode with API key security—to get a governed MCP server running in under five minutes.

{% hint style="info" %}
For a complete reference on all MCP Proxy options, including Studio mode, see [Create an MCP proxy](../build/create-an-mcp-proxy.md).
{% endhint %}

## Prerequisites

To complete this quickstart, you need the following:

* Access to a running Gamma console instance.
* An upstream MCP server accessible using HTTP, such as `https://mcp.example.com/mcp`.

## Create your first MCP server

To create your first MCP server, complete the following steps:

1. [Open the MCP Proxy wizard](#open-the-mcp-proxy-wizard).
2. [Configure security](#configure-security).
3. [Connect to the upstream server](#connect-to-the-upstream-server).
4. [Review and create](#review-and-create).

### Open the MCP Proxy wizard

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **MCP Proxies**.
3. Select **+ Create MCP proxy**.

The console opens the MCP Proxy creation wizard. Select **Proxy mode**, enter a name like "My First MCP Server" and a context path, and then select **Next**.

### Configure security

The next step defines how consumers authenticate when calling tools through this MCP Proxy. The wizard offers four authentication methods: **Gravitee as Authorization Server**, **External Authorization Server**, **API Key**, and **Passthrough**.

For this quickstart, select **API Key** to get running quickly without configuring an identity provider. The console flags API Key as **Not recommended**, since API keys don't carry user identity and can't be scoped as granularly as OAuth. For production deployments, use **Gravitee as Authorization Server** instead.

Select **Next** to proceed.

### Connect to the upstream server

Provide the connection details for the upstream MCP server:

1. Under **Upstream server**, enter the URL of your MCP endpoint, such as `https://mcp.example.com/mcp`. The Gateway uses Streamable HTTP transport by default.
2. Under **Upstream Authentication**, select **No upstream auth**—a passthrough option—for this quickstart, or enter your static credentials if your server requires them.

Select **Next** to proceed.

### Review and create

Review the MCP Proxy configuration, and then select **Create & deploy** to create the proxy and make it immediately available on the gateway. Select **Create only** instead if you want to create the proxy without deploying it yet.

The console creates the MCP Proxy and registers it in the AI Gateway. The MCP Proxy now sits in front of your upstream MCP server—every tool invocation flows through the AI Gateway, where authentication, policies, and observability are applied.

## Verify tool invocations

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

After creating your MCP Proxy, explore the following:

* **Add policies.** Apply fine-grained authorization to control which consumers can invoke specific tools. See [Add policies to your MCP server](../build/configure-your-mcp/add-policies-to-mcp-server.md).
* **Configure mediation.** Establish token exchange and credential mediation for upstream MCP servers that require their own OAuth. See [Configure your MCP proxy](../build/configure-your-mcp/README.md).
* **Create a Composite MCP Server.** Compose tools from multiple upstream servers, APIs, and events into a single governed MCP server. See [Create an MCP Studio](../build/create-an-mcp-studio.md).
