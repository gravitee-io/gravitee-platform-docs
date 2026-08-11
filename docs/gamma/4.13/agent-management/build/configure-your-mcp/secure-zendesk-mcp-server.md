---
description: Secure the Zendesk MCP server in Gravitee Gamma with an MCP Proxy. Follow the steps to authenticate, scope, and audit agent access.
---

# Secure the Zendesk MCP server

## Overview

* **Outcome.** A Gravitee MCP Proxy in front of Zendesk's MCP server, enforcing authentication, per-tool authorization, rate limiting, and PII filtering on every call.
* **Use this when.** Multiple agents need access to Zendesk support-ticket tools and you need one place to authenticate callers, scope which tools each caller can invoke, and audit what happened, rather than distributing a Zendesk credential to every agent.
* **Not covered here.** Composing tools from Zendesk alongside other sources into one server. See [Create an MCP Studio](create-an-mcp-studio.md "mention"). Concepts behind Agent Management as a whole. See [Agent Management overview](../get-started/ai-management-overview.md "mention").

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Gravitee Gamma, Agent Management enabled. MCP Proxy is available from Gamma 4.12 onward.
* A Zendesk instance with its MCP server enabled, and a credential Gravitee can use to authenticate to it. See Zendesk's own documentation for enabling MCP access.
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
5. Enter a **Name**, for example `zendesk-mcp`, and an optional **Description**.
6. Enter the **Context path** your agents will use to reach this proxy, for example `/mcp/zendesk`.
7. Under **Configure consumer security**, select how callers authenticate to the proxy entrypoint:

    | Method | Description |
    | --- | --- |
    | **Gravitee as Authorization Server** | Gravitee Identity & Access Management issues and validates OAuth tokens for callers. |
    | **External Authorization Server** | Use an external IdP, such as Auth0, Keycloak, or PingFederate, as the authorization server. |
    | **API Key** | A shared key for server access when per-caller identity isn't available. |
    | **Passthrough** | No authentication enforced. |

    Select **Gravitee as Authorization Server** or **External Authorization Server** if your tool-level authorization policies need to know which caller is making each request.

8. Enter the **Server URL** of Zendesk's MCP endpoint.
9. Under **Connect to the upstream MCP server**, select how the Gateway authenticates to Zendesk:

    | Method | Description |
    | --- | --- |
    | **Static credential** | Inject an API key, Bearer token, Basic auth, or Custom secret into a request header on every call to Zendesk. |
    | **No upstream auth** | Call Zendesk without injecting credentials. |

    Use **Static credential** with a Zendesk API token as a Bearer token. This credential is shared across every call, not scoped to the calling user or agent.

    <!-- TODO: a per-caller OAuth delegation option is described to this writer directly by Agent Management's product owner as available. One MCP Proxy endpoint maps to one upstream OAuth client, with the delegated user's identity carried through to Zendesk. It isn't described on this page as verified from source. This page's own "Configure mediation" cross-reference points to the upstream-authentication doc for "token exchange and credential management for upstream OAuth", but that page currently only documents Static credential and No upstream auth. Two limitations were named alongside the confirmation. Token refresh isn't automatic yet, so a caller re-authenticates when their delegated token expires. The storage of delegated tokens on the gateway is being hardened. Confirm the exact console steps from source, or from an updated version of the upstream-authentication page, before adding this as a numbered walkthrough. -->

10. Select **Create & deploy** to register and deploy the proxy in one step, or **Create only** to register it without deploying.

## Add tool-level authorization

To control which callers can invoke which Zendesk tools, complete the following steps:

1. From the Gamma console sidebar, select **Authorization**.
2. In the Authorization sidebar, select **MCPs**.
3. Select **+ Create policy**.
4. Enter a **Policy name** and optional **Description**.
5. In the Visual editor, set the **effect** to **permit** or **forbid**.
6. Select the **principals** the policy applies to. Choose from users, groups, agents, or agent identities.
7. Select an **action**. Choose `invoke`, `list`, or `read`.
8. Select a **resource**. Choose the whole `MCPServer`, a specific `MCPTool` such as `search_tickets`, an `MCPPrompt`, or an `MCPResource`.
9. Optionally add a **condition**, for example a business-hours restriction (`context.time.hour >= 9 && context.time.hour < 17`) or a corporate IP range (`context.source.ip.in_cidr("10.0.0.0/8")`).
10. Select **Create and Deploy policy**.

The Gateway picks up a newly deployed policy within 30 seconds, without a restart.

## Rate limit or filter individual tools

To apply a policy to one Zendesk tool rather than the whole proxy, complete the following steps:

1. Open your Zendesk MCP proxy.
2. In the sidebar, select **Policy Studio**.
3. Under **MCP Method Flows**, select **Add MCP method flow**.
4. Enter a **Flow name**, and then select the **`tools/call`** method.
5. Add a **Condition** matching the tool name, for example `{#context.attributes['mcp_tool_name'] == 'search_tickets'}`.
6. In the flow's **Request** or **Response** phase, open the **Add Policy** catalog, and then select the policy to apply. Choose a rate limit for a high-volume tool, or PII Filtering for a tool that returns ticket content.

    {% hint style="warning" %}
    PII Filtering rejects streaming responses with a 400 error unless `skipResponsePayloadFiltering` is set to `true`.
    {% endhint %}

7. Select **Save**.

## Verification

To confirm the proxy is enforcing what you configured, complete the following steps:

1. Call a permitted tool as a principal your policy allows. Confirm the call reaches Zendesk and returns a result.
2. Call the same tool as a principal your policy denies, or call a `forbid`-scoped tool such as `delete_ticket`. Confirm the Gateway rejects the call before it reaches Zendesk.
3. Open the agent log for the call in step 1 and confirm it shows the caller's identity, the tool invoked, and the policy decision.

## Next steps

* [Create an agent identity](../create-an-agent-identity.md "mention") so policies can reference the calling agent, not just the end user, as a principal.
* [Monitor your MCP servers](../../observe/monitor-your-mcp-servers.md "mention") for tool-level call volume, errors, and latency.
