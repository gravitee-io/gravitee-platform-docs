---
description: Secure the HubSpot MCP server in Gravitee Gamma with an MCP Proxy. Follow the steps to authenticate, scope, and audit agent access.
---

# Secure the HubSpot MCP server

## Overview

* **Outcome.** A Gravitee MCP Proxy in front of HubSpot's MCP server, enforcing authentication, per-tool authorization, rate limiting, and PII filtering on every call.
* **Use this when.** Multiple agents need access to HubSpot CRM and conversation data and you need one place to authenticate callers, scope which tools each caller can invoke, and audit what happened, rather than distributing a HubSpot MCP Auth App credential to every agent.
* **Not covered here.** Composing tools from HubSpot alongside other sources into one server. See [Create an MCP Studio](create-an-mcp-studio.md "mention"). Concepts behind Agent Management as a whole. See [Agent Management overview](../get-started/ai-management-overview.md "mention").

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Gravitee Gamma, Agent Management enabled. MCP Proxy is available from Gamma 4.12 onward.
* A HubSpot account with an MCP Auth App already created, giving you a Client ID, a Client secret, and a Redirect URL. See HubSpot's own documentation for creating an MCP Auth App.
* The permission to create and deploy an MCP Proxy, and the permission to author Authorization Management policies if you're adding tool-level authorization.
* If you're syncing consumer identities from an external IdP, a SCIM-compatible tenant, such as Okta, already connected.

{% hint style="warning" %}
<!-- TODO: confirm whether any part of this flow requires an Enterprise Edition pack, per the plugin.properties feature= check — not verified against source for this draft. -->
{% endhint %}

## Create the MCP proxy

To create the MCP proxy, complete the following steps:

1. From the Gamma console sidebar, select **Agent Management**.
2. In the **Secure** section, select **MCP Proxies**.
3. Select **Create MCP proxy**.
4. Select **Proxy mode**.
5. Enter a **Name**, for example `hubspot-mcp`, and an optional **Description**.
6. Enter the **Context path** your agents will use to reach this proxy, for example `/mcp/hubspot`.
7. Under **Configure consumer security**, select how callers authenticate to the proxy entrypoint:

    | Method | Description |
    | --- | --- |
    | **Gravitee as Authorization Server** | Gravitee Identity & Access Management issues and validates OAuth tokens for callers. |
    | **External Authorization Server** | Use an external IdP, such as Auth0, Keycloak, or PingFederate, as the authorization server. |
    | **API Key** | A shared key for server access when per-caller identity isn't available. |
    | **Passthrough** | No authentication enforced. |

    Select **Gravitee as Authorization Server** or **External Authorization Server** if your tool-level authorization policies need to know which caller is making each request.

8. Enter the **Server URL**: `https://mcp.hubspot.com`.
9. Under **Connect to the upstream MCP server**, select how the Gateway authenticates to HubSpot:

    | Method | Description |
    | --- | --- |
    | **Static credential** | Inject an API key, Bearer token, Basic auth, or Custom secret into a request header on every call to HubSpot. |
    | **No upstream auth** | Call HubSpot without injecting credentials. |

    <!-- TODO: HubSpot's MCP server requires the OAuth 2.1 Authorization Code flow with PKCE for every client — this is documented by HubSpot as mandatory, not optional, and there is no plain-API-key alternative on HubSpot's side. Static credential injects one fixed value per call; PKCE requires a per-session code_verifier/code_challenge pair and an interactive authorization step, so a static Bearer token doesn't satisfy it. No upstream auth doesn't apply either, since HubSpot requires authentication. Whether the MCP Proxy can complete a full OAuth 2.1+PKCE handshake as an upstream client — the same "oauth-elicitation" capability described to this writer directly by Agent Management's product owner as available, with token refresh not yet automatic and upstream token storage being hardened — needs confirming from source or an updated upstream-authentication doc page before this section can responsibly recommend a specific path. Until then, treat upstream auth to HubSpot specifically as an open question, not a solved step. -->

10. Select **Create & deploy** to register and deploy the proxy in one step, or **Create only** to register it without deploying.

## Add tool-level authorization

To control which callers can invoke which HubSpot tools, complete the following steps:

1. From the Gamma console sidebar, select **Authorization**.
2. In the Authorization sidebar, select **MCPs**.
3. Select **+ Create policy**.
4. Enter a **Policy name** and optional **Description**.
5. In the Visual editor, set the **effect** to **permit** or **forbid**.
6. Select the **principals** the policy applies to. Choose from users, groups, agents, or agent identities.
7. Select an **action**. Choose `invoke`, `list`, or `read`.
8. Select a **resource**. Choose the whole `MCPServer`, or a specific `MCPTool` such as `search_crm_objects`, `get_crm_objects`, `manage_crm_objects`, or `search_conversations`.
9. Optionally add a **condition**, for example a business-hours restriction (`context.time.hour >= 9 && context.time.hour < 17`) or a corporate IP range (`context.source.ip.in_cidr("10.0.0.0/8")`).
10. Select **Create and Deploy policy**.

The Gateway picks up a newly deployed policy within 30 seconds, without a restart. For example, permit `search_crm_objects` and `get_crm_objects` broadly for a support-agent group, and then forbid `manage_crm_objects` for that same group, so support agents can look up records without being able to create or update them.

## Rate limit or filter individual tools

To apply a policy to one HubSpot tool rather than the whole proxy, complete the following steps:

1. Open your HubSpot MCP proxy.
2. In the sidebar, select **Policy Studio**.
3. Under **MCP Method Flows**, select **Add MCP method flow**.
4. Enter a **Flow name**, and then select the **`tools/call`** method.
5. Add a **Condition** matching the tool name, for example `{#context.attributes['mcp_tool_name'] == 'search_crm_objects'}`.
6. In the flow's **Request** or **Response** phase, open the **Add Policy** catalog, and then select the policy to apply. Choose a rate limit for `search_crm_objects`, since it's the primary lookup tool and the most likely to see high call volume. Choose PII Filtering for `search_conversations` or `get_crm_objects`, since HubSpot's own documentation lists conversation and CRM record data as including customer emails, phone numbers, and message content.

    {% hint style="warning" %}
    PII Filtering rejects streaming responses with a 400 error unless `skipResponsePayloadFiltering` is set to `true`.
    {% endhint %}

7. Select **Save**.

## Verification

To confirm the proxy is enforcing what you configured, complete the following steps:

1. Call a permitted tool as a principal your policy allows. Confirm the call reaches HubSpot and returns a result.
2. Call the same tool as a principal your policy denies, or call `manage_crm_objects` as a principal scoped to read-only tools. Confirm the Gateway rejects the call before it reaches HubSpot.
3. Open the agent log for the call in step 1 and confirm it shows the caller's identity, the tool invoked, and the policy decision.

## Next steps

* [Create an agent identity](../create-an-agent-identity.md "mention") so policies can reference the calling agent, not just the end user, as a principal.
* [Monitor your MCP servers](../../observe/monitor-your-mcp-servers.md "mention") for tool-level call volume, errors, and latency.
