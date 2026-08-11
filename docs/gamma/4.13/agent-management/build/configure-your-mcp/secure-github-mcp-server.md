---
description: Secure the GitHub MCP server in Gravitee Gamma with an MCP Proxy. Follow the steps to authenticate, scope, and audit agent access.
---

# Secure the GitHub MCP server

## Overview

* **Outcome.** A Gravitee MCP Proxy in front of GitHub's MCP server, enforcing authentication, per-tool authorization, rate limiting, and PII filtering on every call.
* **Use this when.** Multiple agents need access to GitHub repositories, issues, and pull requests, and you need one place to authenticate callers, scope which tools each caller invokes, and audit what happened, rather than distributing a GitHub personal access token to every agent.
* **Not covered here.** How the three governance controls interact conceptually. See [Layered governance for MCP tools](govern-mcp-tool-access.md "mention"). Composing tools from GitHub alongside other sources into one server. See [Create an MCP Studio](../create-an-mcp-studio.md "mention"). Concepts behind Agent Management as a whole. See [Agent Management overview](../../get-started/ai-management-overview.md "mention").

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Gravitee Gamma, Agent Management enabled. MCP Proxy is available from Gamma 4.12 onward.
* A GitHub personal access token, scoped to the tools you plan to expose. Most repository, issue, and pull request tools need the `repo` scope. Security-related tools need `security_events`, and organization-level tools need `read:org`. Some tools mirror a paid GitHub or Copilot feature and need the matching plan on the token's account.
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
5. Enter a **Name**, for example `github-mcp`, and an optional **Description**.
6. Enter the **Context path** your agents will use to reach this proxy, for example `/mcp/github`.
7. Under **Configure consumer security**, select how callers authenticate to the proxy entrypoint:

    | Method | Description |
    | --- | --- |
    | **Gravitee as Authorization Server** | Gravitee Identity & Access Management issues and validates OAuth tokens for callers. |
    | **External Authorization Server** | Use an external IdP, such as Auth0, Keycloak, or PingFederate, as the authorization server. |
    | **API Key** | A shared key for server access when per-caller identity isn't available. |
    | **Passthrough** | No authentication enforced. |

    Select **Gravitee as Authorization Server** or **External Authorization Server** if your tool-level authorization policies need to know which caller is making each request.

8. Enter the **Server URL**: `https://api.githubcopilot.com/mcp/`.
9. Under **Connect to the upstream MCP server**, select **Static credential**.
10. Set **Credential type** to **Bearer token**, and then paste the GitHub personal access token from the prerequisites. The Gateway injects it as an `Authorization: Bearer` header on every call to GitHub, so the token is held once, on the Gateway, instead of distributed to every agent.
11. Select **Create & deploy** to register and deploy the proxy in one step, or **Create only** to register it without deploying.

## Add tool-level authorization

To control which callers invoke which GitHub tools, complete the following steps:

1. From the Gamma console sidebar, select **Authorization**.
2. In the Authorization sidebar, select **MCPs**.
3. Select **+ Create policy**.
4. Enter a **Policy name** and optional **Description**.
5. In the Visual editor, set the **effect** to **permit** or **forbid**.
6. Select the **principals** the policy applies to. Choose from users, groups, agents, or agent identities.
7. Select an **action**. Choose `invoke`, `list`, or `read`.
8. Select a **resource**. Choose the whole `MCPServer`, or a specific `MCPTool` such as `github-mcp-server.issue_read`, `github-mcp-server.pull_request_read`, `github-mcp-server.search_code`, or `github-mcp-server.create_or_update_file`.
9. Optionally add a **condition**, for example a business-hours restriction (`context.time.hour >= 9 && context.time.hour < 17`) or a corporate IP range (`context.source.ip.in_cidr("10.0.0.0/8")`).
10. Select **Create and Deploy policy**.

The Gateway picks up a newly deployed policy within 30 seconds, without a restart. For example, permit `issue_read`, `pull_request_read`, `search_code`, and `search_repositories` broadly for a read-only agent group, and then forbid `create_or_update_file`, `merge_pull_request`, and `create_branch` for that same group, so the agents look up code and history without changing the repository.

## Rate limit or filter individual tools

To apply a policy to one GitHub tool rather than the whole proxy, complete the following steps:

1. Open your GitHub MCP proxy.
2. In the sidebar, select **Policy Studio**.
3. Under **MCP Method Flows**, select **Add MCP method flow**.
4. Enter a **Flow name**, and then select the **`tools/call`** method.
5. Add a **Condition** matching the tool name, for example `{#context.attributes['mcp_tool_name'] == 'search_code'}`.
6. In the flow's **Request** or **Response** phase, open the **Add Policy** catalog, and then select the policy to apply. Choose a rate limit for `search_code` and `search_repositories`, since they're the tools most likely to see high call volume from an agent iterating over results. Choose PII Filtering for `get_file_contents`, `issue_read`, and `pull_request_read`, since file contents, issue bodies, and pull request descriptions carry names, email addresses, and other personal data committed into the repository.

    {% hint style="warning" %}
    PII Filtering rejects streaming responses with a 400 error unless `skipResponsePayloadFiltering` is set to `true`.
    {% endhint %}

7. Select **Save**.

## Verification

To confirm the proxy is enforcing what you configured, complete the following steps:

1. Call a permitted tool, such as `issue_read`, as a principal your policy allows. Confirm the call reaches GitHub and returns a result.
2. Call `merge_pull_request` as a principal scoped to the read-only group. Confirm the Gateway rejects the call before it reaches GitHub.
3. Open the agent log for the call in step 1 and confirm it shows the caller's identity, the tool invoked, and the policy decision.

## Next steps

* [Layered governance for MCP tools](govern-mcp-tool-access.md "mention") for how authorization, rate limits, and redaction combine on a Composite MCP Server.
* [Create an agent identity](../create-an-agent-identity.md "mention") so policies reference the calling agent, not just the end user, as a principal.
* [Monitor your MCP servers](../../observe/monitor-your-mcp-servers.md "mention") for tool-level call volume, errors, and latency.
