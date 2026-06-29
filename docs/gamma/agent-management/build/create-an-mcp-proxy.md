---
hidden: false
noIndex: true
---

# Create an MCP proxy
<!-- GAP-STRUCTURAL: Missing procedural content source -->

An MCP Proxy sits in front of an upstream MCP server and applies governance — authentication, fine-grained authorization, observability, and rate limiting — to every tool invocation. The proxy speaks protocol-native MCP (JSON-RPC 2.0), operates on typed MCP objects (tool name, arguments, resource URI), and supports OAuth authorization discovery.

{% hint style="info" %}
For a quickstart with minimal configuration, see [Create your first MCP server](../get-started/create-your-first-mcp-server.md).
{% endhint %}

## Two modes

The MCP Proxy operates in two modes:

{% tabs %}
{% tab title="Proxy mode" %}
A transparent intermediary in front of an existing upstream MCP server. Proxy mode adds governance without changing the server — like a classic API proxy for MCP traffic.

**Use case:** You have an upstream MCP server (HubSpot, GitHub, Salesforce) and want to add authentication, authorization, and observability without modifying the server.
{% endtab %}

{% tab title="Studio mode" %}
An authoring environment for Composite MCP Servers. In Studio mode, you compose tools, resources, prompts, and skills from multiple sources into a new MCP server that didn't exist as a single unit upstream.

For Studio mode, see [Create an MCP Studio](create-an-mcp-studio.md).
{% endtab %}
{% endtabs %}

## Step 1: Open the MCP Proxy wizard

1. From the Gamma console sidebar, select **Agent Management**.
2. Navigate to **Build**.
3. Select **Create MCP Proxy**.

## Step 2: Define your proxy

1. Choose **Proxy mode** to act as a transparent intermediary for an existing MCP server.
2. Provide a **Name** and an optional **Description**.
3. Enter the **Context path** (the URL path prefix clients will use to reach this proxy).

## Step 3: Configure consumer security

Choose how clients authenticate to the proxy entrypoint:

| Security method                     | Description                                                                                             |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Gravitee as Authorization Server**| Uses Gravitee Identity & Access Management to secure access, handling OAuth token issuance. (Recommended)|
| **External Authorization Server**   | Use an external identity provider (Auth0, Keycloak, PingFederate, etc.) as your authorization server.   |
| **API Key**                         | Use a shared key for server access when user-level identity is not available.                           |
| **Passthrough**                     | Gravitee passes all requests through without enforcing any authentication.                              |

## Step 4: Configure upstream authentication

Configure how the proxy authenticates with the upstream MCP server:

| Method                 | Description                                                                 |
| ---------------------- | --------------------------------------------------------------------------- |
| **Static credential**  | Inject a static credential (API key, Bearer token, Basic auth, or Custom secret) into a request header on every call. |
| **No upstream auth**   | Call the upstream without injecting credentials (passthrough).              |

## Step 5: Review and create

Review the MCP Proxy configuration — including security and upstream authentication — then select **Create**.

The MCP Proxy is created and registered in the AI Gateway. Every tool invocation through this proxy is now subject to the configured authentication, policies, and observability.

## After creation

Once the MCP Proxy is created, you can:

* **Add authorization policies** — Control which consumers can invoke specific tools. See [Add policies to your MCP server](configure-your-mcp/add-policies-to-mcp-server.md).
* **Configure mediation** — Set up token exchange and credential management for upstream OAuth. See [Configure your MCP proxy](configure-your-mcp/README.md).
* **View in the Catalog** — The MCP Proxy appears in the API Management console alongside API proxies.

## Next steps

* [Configure your MCP proxy](configure-your-mcp/README.md) — Set up mediation and advanced configuration.
* [Add policies to your MCP server](configure-your-mcp/add-policies-to-mcp-server.md) — Apply fine-grained authorization.
* [Create an MCP Studio](create-an-mcp-studio.md) — Compose tools from this server with tools from other sources.
