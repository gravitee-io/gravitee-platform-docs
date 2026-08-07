---
hidden: false
noIndex: false
description: Create an MCP Proxy that governs an upstream MCP server with authentication, authorization, and observability. Follow the steps in the wizard.
---

# Create an MCP proxy

An MCP Proxy sits in front of an upstream MCP server and applies governance—authentication, fine-grained authorization, observability, and rate limiting—to every tool invocation. The proxy speaks protocol-native MCP, JSON-RPC 2.0. It operates on typed MCP objects—tool name, arguments, and resource URI—and supports OAuth authorization discovery.

{% hint style="info" %}
For a quickstart with minimal configuration, see [Create your first MCP server](../get-started/create-your-first-mcp-server.md).
{% endhint %}

## Two modes

The MCP Proxy operates in two modes:

{% tabs %}
{% tab title="Proxy mode" %}
A transparent intermediary in front of an existing upstream MCP server. Proxy mode adds governance without changing the server—like a classic API proxy for MCP traffic.

**Use case:** You have an upstream MCP server, such as HubSpot, GitHub, or Salesforce, and want to add authentication, authorization, and observability without modifying the server.
{% endtab %}

{% tab title="Studio mode" %}
An authoring environment that assembles catalog tools into a unified MCP entrypoint. In Studio mode, you select tools from the catalog to expose through a new MCP server that didn't exist as a single unit upstream.

For Studio mode, see [Create an MCP Studio](create-an-mcp-studio.md).
{% endtab %}
{% endtabs %}

## Create the MCP proxy

To create an MCP proxy, complete the following steps:

1. [Open the MCP Proxy wizard](#open-the-mcp-proxy-wizard)
2. [Define your proxy](#define-your-proxy)
3. [Configure consumer security](#configure-consumer-security)
4. [Connect to the upstream MCP server](#connect-to-the-upstream-mcp-server)
5. [Review and create](#review-and-create)

### Open the MCP Proxy wizard

1. From the Gamma console sidebar, select **Agent Management**.
2. Under **Secure**, select **MCP Proxies**.
3. Select **+ Create MCP proxy**.

### Define your proxy

1. Choose **Proxy mode** to act as a transparent intermediary for an existing MCP server.
2. Provide a **Name** and an optional **Description**.
3. Enter the **Context path**, the URL path prefix clients use to reach this proxy.

### Configure consumer security

Choose how clients authenticate to the proxy entrypoint. The wizard offers the following methods:

| Security method                      | Description                                                                                                 |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| **Gravitee as Authorization Server** | Uses Gravitee Identity & Access Management to secure access, handling OAuth token issuance. Recommended.     |
| **External Authorization Server**    | Use an external identity provider, such as Auth0, Keycloak, or PingFederate, as your authorization server.   |
| **API Key**                          | Use a shared key for server access when user-level identity is not available.                               |
| **Passthrough**                      | Gravitee passes all requests through without enforcing any authentication.                                  |

### Connect to the upstream MCP server

Enter the **Server URL** of the upstream MCP endpoint, and then choose how the Gateway authenticates to that server at runtime. The wizard offers the following methods:

| Method                | Description                                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------------------- |
| **Static credential** | Inject a static credential—API key, Bearer token, Basic auth, or Custom secret—into a request header on every call. |
| **No upstream auth**  | Call the upstream without injecting credentials.                                                         |

### Review and create

Review the MCP Proxy configuration, including security and upstream authentication. Then select **Create only** to register the proxy without deploying it, or **Create & deploy** to register and deploy it in one step.

**Create only** leaves the proxy stopped and out of sync. Select **Deploy** on the proxy overview to push it to the AI Gateway. Once the proxy is deployed, every tool invocation through it is subject to the configured authentication, policies, and observability.

## After creation

Once the MCP Proxy is created, you can do the following:

* **Add authorization policies**. Control which consumers can invoke specific tools. See [Add policies to your MCP server](configure-your-mcp/add-policies-to-mcp-server.md).
* **Configure upstream authentication**. Manage the credentials the Gateway injects when it calls the upstream server. See [Configure your MCP proxy](configure-your-mcp/README.md).
* **Backing API**. Gravitee backs each MCP Proxy with an API in API Management. Deleting the MCP Proxy also deletes that API.

## Next steps

* [Configure your MCP proxy](configure-your-mcp/README.md). Configure upstream authentication and other advanced settings.
* [Add policies to your MCP server](configure-your-mcp/add-policies-to-mcp-server.md). Apply fine-grained authorization.
* [Create an MCP Studio](create-an-mcp-studio.md). Compose tools from this server with tools from other sources.
