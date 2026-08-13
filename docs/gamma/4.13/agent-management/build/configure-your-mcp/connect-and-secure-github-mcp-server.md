---
description: Connect GitHub's MCP server to Gravitee, curate the tools it exposes, and
  secure them with authentication, fine-grained authorization, rate limits, and PII
  redaction. Follow the steps to get started.
---

# Connect and secure the GitHub MCP server

## Overview

* **Outcome.** GitHub's MCP server is reachable through Gravitee as a curated Composite MCP Server. Its tools are protected by authentication and per-tool authorization, its call volume is capped per caller, its responses are redacted, and every invocation is recorded against the identity that made the invocation.
* **Use this when.** You want agents to reach GitHub's tools through Gravitee rather than connecting to `https://api.githubcopilot.com/mcp/` directly. The personal access token stays on the Gateway instead of being copied into every agent's configuration, and every tool call is authorized and audited against the caller's own identity.
* **Not covered here.**
  * [What the GitHub MCP server does and which tools it exposes](https://github.com/github/github-mcp-server)
  * [How Gravitee governs MCP servers](govern-mcp-tool-access.md "mention")
  * [Building the agent that calls these tools](../create-an-agent-identity.md "mention")

GitHub's MCP server authenticates with a personal access token, and that token carries every permission its owner holds. An agent handed the token can read any repository the token can read and write any repository the token can write, and GitHub records the activity as the token's owner rather than as the agent or the person who prompted it. Gravitee closes that gap without changing the upstream server: the token is held once on the Gateway, the tool surface is curated before any policy is written, and each call is authorized, limited, redacted, and logged under the caller's identity.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Gravitee Gamma 4.12 or later, with Agent Management enabled.
* Permission to register catalog entities, create and deploy an MCP Proxy, and author Authorization Management policies in the environment you are configuring.
* A GitHub personal access token scoped to the tools you plan to expose. A fine-grained token scoped to the repositories the agents need is sufficient. On each repository, grant **Contents: read** for `get_file_contents`, **Issues: read** for `list_issues`, **Pull requests: read** for `pull_request_read`, and **Contents: read and write** for `create_or_update_file`. For more information about GitHub personal access tokens, go to [GitHub's documentation](https://docs.github.com/en/authentication/keeping-your-account-secure/managing-your-personal-access-tokens).
* An identity provided that is configured in Gravitee and holds the groups that your authorization policies reference. For more information about configuring an identity provider, see [Configure your Access Management instance](../configure-your-access-management-instance.md "mention").
* If you are adding PII redaction on your environment, an AI Model Token Classification resource. For more information about AI resources, see [AI resources](../ai-resources.md "mention") .

{% hint style="warning" %}
Until you complete the authorization phase, any consumer holding a valid token for the server can invoke every tool you composed into it, including `create_or_update_file`, which commits to a repository. Complete the authorization and policy phases before you publish the server to consumers.
{% endhint %}

## Connect and secure the GitHub MCP server

To connect and secure the GitHub MCP server, complete the following steps:

1. [Connect the GitHub MCP server](#connect-the-github-mcp-server)
2. [Expose the GitHub tools as a Composite MCP Server](#expose-the-github-tools-as-a-composite-mcp-server)
3. [Authenticate access to the GitHub MCP server](#authenticate-access-to-the-github-mcp-server)
4. [Restrict GitHub tool access with fine-grained authorization](#restrict-github-tool-access-with-fine-grained-authorization)
5. [Apply policies to the GitHub MCP server](#apply-policies-to-the-github-mcp-server)
6. [Observe GitHub MCP interactions](#observe-github-mcp-interactions)

### Connect the GitHub MCP server

Registering the server adds it to the Catalog with its tools, which is what makes those tools selectable in MCP Studio and referenceable in authorization policies.

To connect the GitHub MCP server, complete the following steps:

1. Sign in to the Gravitee console.
2. From the product navigation menu, select **Agent Management**.
3. Navigate to the **Import** section, and then select **MCP Servers**.
4. Click **+ Add MCP server**. The **Add MCP server** wizard opens.
5. In the **Endpoint URL** field, enter the following GitHub MCP server endpoint:

   ```
   https://api.githubcopilot.com/mcp/
   ```

   The **Transport** is fixed to **Streamable HTTP**.

   ![The Select server step of the Add MCP server wizard, with GitHub's endpoint entered and Verify URL ready to run](<../../../.gitbook/assets/gamma-mcp-github-add-server.png>)

6. Select **Verify URL**.
7. On the **Configure connection** step, select **Static credential**, set the credential type to **Bearer token**, and then enter the personal access token. Discovery uses the token to read the server's capabilities and does not persist it.
8. Select **Verify URL** again to re-run discovery, and then on the **Review entry** step select **Import MCP Server**.

#### Verification

To confirm that the GitHub MCP server is connected, complete the following steps:

1. Under **Import**, select **MCP Servers**.
2. Confirm that `github-mcp-server` is listed, with the entity ID `mcp-server.github-mcp-server`, the transport `http`, and the endpoint you entered.
3. Select the server to open its detail page, and then confirm the **Overview** card shows the protocol version, an **Auth type** of **Bearer token**, and a **Capabilities** row with a tool count. 
4. Confirm that the tools listed under **Tools** match the tools for GitHub's MCP server. For more information about GitHub's MCP server, go to [GitHub's documentation](https://github.com/github/github-mcp-server).

   ![The github-mcp-server detail page showing 44 tools, 2 prompts, 4 resources, and an auth type of Bearer token](<../../../.gitbook/assets/gamma-mcp-github-server-detail.png>)

{% hint style="info" %}
GitHub's MCP server exposes a large tool surface, and the exact set depends on the token's scopes and the account's plan. Registering the server catalogs everything discovered. The [Expose the GitHub tools as a Composite MCP Server](#expose-the-github-tools-as-a-composite-mcp-server) section narrows that surface to the tools your agents need.
{% endhint %}

### Expose the GitHub tools as a Composite MCP Server

Rather than proxying GitHub's whole tool surface, use MCP Studio to compose a Composite MCP Server that exposes only the tools a role needs. Curation is the control that precedes all the others, because a tool you never compose is a tool no policy has to defend against, and one an agent's model never sees in `tools/list`.

The following steps build an engineering toolbelt from the following five GitHub tools: `list_issues`, `get_file_contents`, `search_code`, `pull_request_read`, and `create_or_update_file`.

To expose the GitHub tools as a Composite MCP Server, complete the following steps:

1. From the **Agent Management** menu, navigate to secure **Secure**, and then select **MCP Proxies**.
2. Select **+ Create MCP proxy**, and then select **Studio mode**.
3. In the **General information** section, enter a **Name**, for example `engineering-toolbelt`, and a **Context path**, for example `/engineering-toolbelt`.
4. On the **Secure** page, select **Gravitee as Authorization Server**. To use an external identity provider, select **External Authorization Server** instead.
4. In the **Compose** step, select the GitHub MCP server from the palette, and then select only the five tools at the start of this section. 
5. In the **Connect** step, select the GitHub MCP server, set the credential type to **Bearer token**, and then enter the personal access token. The Gateway injects it as an `Authorization` header on every upstream call. The token is held once rather than distributed to each agent.
6. In the **Review** step, confirm the composition, and then select **Create & deploy**.

After you deploy the server, the composition is visible on the **Tools** page of the **Design** section, grouped by upstream server. The `github-mcp-server` group shows its upstream auth type and the number of tools composed from it.

![The Tools page of the Composite MCP Server, showing the five composed GitHub tools under the github-mcp-server group](<../../../.gitbook/assets/gamma-mcp-github-compose-tools.png>)

#### Verification

To confirm that the GitHub tools are exposed, complete the following steps:

1. Send a `tools/list` request to the Composite MCP Server's endpoint:

   ```sh
   curl -s https://<gateway-host>/engineering-toolbelt \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json, text/event-stream' \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```

2. You receive a response like the following response, abbreviated to the tool names and descriptions:

   ```json
   {"jsonrpc":"2.0","id":1,"result":{"tools":[
     {"name":"list_issues","description":"List issues in a GitHub repository. For pagination, use the 'endCursor' from the previous response's 'pageInfo' in the 'after' parameter."},
     {"name":"get_file_contents","description":"Get the contents of a file or directory from a GitHub repository"},
     {"name":"search_code","description":"Fast and precise code search across ALL GitHub repositories using GitHub's native search engine."},
     {"name":"pull_request_read","description":"Get information on a specific pull request in GitHub repository."},
     {"name":"create_or_update_file","description":"Create or update a single file in a GitHub repository."}
   ]}}
   ```

3. Confirm that the response lists only the five tools. An agent connected to this server sees only these five, whatever else GitHub exposes upstream.
4. Note that `tools/list` returns each tool under its composed name, for example `list_issues`. Authorization policies reference the same tool under its server-qualified identifier, in the form `github-mcp-server.list_issues`.

{% hint style="info" %}
If you compose tools from more than one upstream server and two tool names collide, assign an alias in the **Compose** step. For more information about assigning an alias, see [Edit MCP Studio composition](../edit-mcp-studio-composition.md "mention").
{% endhint %}

### Authenticate access to your deployed GitHub MCP server 

{% hint style="info" %}
If you authenticated your GitHub MCP Server during the [Expose the GitHub tools as a Composite MCP Server](#expose-the-github-tools-as-a-composite-mcp-server) section, you can skip this section and go to [Restrict GitHub tool access with fine-grained authorization](#restrict-github-tool-access-with-fine-grained-authorization)
{% endhint %}

Authorization policies can only distinguish callers if the Gateway knows who each caller is. Authenticate the server against an authorization server rather than a shared key, so that each token resolves to a user or an agent identity.

To require authentication for the GitHub MCP server, complete the following steps:

1. On an existing server, open the MCP Server, navigate to the **Consumer access** section, and then select **Plans**.

{% hint style="warning" %}
Do not select **Keyless** or **API Key** on a server you intend to govern per caller. Neither resolves a user identity, so every fine-grained authorization policy evaluates against the same subject.
{% endhint %}

2. Select **+ Create plan**, and then select **OAuth2**. The other options are **Keyless**, which enforces no authentication, and **API Key**.
3. Configure and publish the plan, and then deploy the server.

   ![The Plans page of the Composite MCP Server, showing one published plan with OAuth2 security](<../../../.gitbook/assets/gamma-mcp-github-plan-oauth2.png>)

#### Verification

To confirm that authentication to the GitHub MCP server is enforced, complete the following steps:

1. Call the GitHub MCP server without a token:

   ```sh
   curl -s -o /dev/null -w '%{http_code}\n' https://<gateway-host>/engineering-toolbelt \
     -H 'Content-Type: application/json' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```

2. You receive a response like the following response:

   ```
   HTTP/1.1 401 Unauthorized
   WWW-Authenticate: Bearer resource_metadata="https://<gateway-host>/.well-known/oauth-protected-resource/engineering-toolbelt" scope="openid profile email list_issues get_file_contents search_code pull_request_read create_or_update_file"

   {"message":"Unauthorized","http_status_code":401}
   ```

   The `WWW-Authenticate` header points the caller at the server's protected-resource metadata, which is how an MCP client discovers where to get a token.

3. Repeat the call with a valid access token.
4. Confirm that the response is `200` and lists the available tools, as in the previous verification.

### Restrict GitHub tool access with fine-grained authorization

All authenticated callers can invoke all five tools, including the one that commits code. Fine-grained authorization narrows that per identity. When you enable fine-grained authorization, the Gateway adds the GAPL Authorization PEP to the server's `tools/call` flow and asks the in-gateway Policy Decision Point for a decision before it forwards anything upstream.

To restrict which tools each caller can use, complete the following steps:

1. Open your Composite MCP Server. On the **Overview** page, turn on **Enable FGA**. A confirmation panel reports that the Authorization PEP has been added to the Policy Studio.

   ![The Composite MCP Server Overview page with the Enable FGA toggle turned on](<../../../.gitbook/assets/gamma-mcp-github-enable-fga.png>)

2. From the product selector, open **Authorization Management**, navigate to the **Policy Management** ssection, and then select **MCPs**.
3. Select **+ Create policy**, enter a **Policy name**, and then switch to the **Code** tab.
4. Enter the policy. The following statement grants an engineering group every tool on the server:

   ```
   permit (
     principal in Group::"<engineering-group-id>",
     action,
     resource
   ) when { resource is MCPTool };
   ```

5. Select **Create and Deploy policy**.
6. Repeat steps 2 to  5 for each remaining statement. The following statement closes the one tool that writes, for the same group:

   ```
   forbid (
     principal in Group::"<engineering-group-id>",
     action,
     resource == MCPTool::"github-mcp-server.create_or_update_file"
   );
   ```

   The following statement scopes a triage role to two read tools and nothing else:

   ```
   permit (
     principal in Group::"<triage-group-id>",
     action,
     resource
   ) when {
     resource == MCPTool::"github-mcp-server.list_issues" ||
     resource == MCPTool::"github-mcp-server.search_code"
   };
   ```

The Gateway picks up a deployed policy within 30 seconds, with no restart.

Select an existing policy to review it. The **Visual** tab renders each statement as an effect, a principal, an action, and a resource, and resolves the group identifier to its display name. The **Code** tab shows the same statement as GAPL.

![The forbid statement on create_or_update_file in the visual policy editor, showing the Engineering principal, the GitHub tool resource, and a Deployed status](<../../../.gitbook/assets/gamma-mcp-github-forbid-policy.png>)

{% hint style="info" %}
A tool that no policy permits is denied. Nothing is allowed by omission, so the triage role above needs no forbid statement to be closed to the other three tools. A `forbid` statement always beats a `permit`, so a later broad grant cannot reopen `create_or_update_file`.

Every entity reference is an identifier, not a display name. `principal` takes the group's identifier, and `resource` takes the server-qualified tool identifier. Leave `action` unconstrained unless you intend to match one specific tool invocation. A clause that references a name where an identifier is expected matches nothing, and the call is then denied by default rather than reported as a malformed policy. For more information about Layered governance for MCP tools, see [Govern MCP tool access](govern-mcp-tool-access.md "mention").
{% endhint %}

#### Verification

To confirm that GitHub tool access is restricted, complete the following steps:

1. As a caller in the engineering group, call `list_issues`:

   ```sh
   curl -s https://<gateway-host>/engineering-toolbelt \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json, text/event-stream' \
     -H "Authorization: Bearer $ENGINEERING_TOKEN" \
     -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"list_issues",
          "arguments":{"owner":"<owner>","repo":"<repo>","state":"all","perPage":5}}}'
   ```

2. Confirm that the call succeeds and returns issues from the repository.
3. As the same caller, call `create_or_update_file`.
4. Confirm that the response is `403`, and that no commit appears on the repository. The decision runs in the request phase, so the Gateway denies the call before it reaches GitHub.
5. As a caller in the triage group, call `get_file_contents`.
6. Confirm that the response is `403`, because no policy permits that tool for that group.

### Apply policies to the GitHub MCP server

Authorization decides which tools a caller reaches, not how often it calls them or what comes back. An agent that loops over search results can exhaust a shared GitHub rate limit while staying inside its permissions, and a permitted read of a file, an issue, or a pull request can return names and email addresses committed into the repository. Add a rate limit and a redaction policy on the `tools/call` flow to close both.

To apply policies to the GitHub MCP server, complete the following steps:

1. Open your Composite MCP Server, navigate to the **Design** section, and then select **Policy Studio**.
2. Navigate to the **MCP method flows** section, add a flow, enter a **Flow name**, select the **`tools/call`** method, and then select **Create**. Enabling FGA creates this flow for you, with the Authorization PEP already in the request phase.

   ![The Policy Studio tools/call flow, with the Gravitee Authorization PEP, Rate Limit, and PII Filtering policies in the request phase](<../../../.gitbook/assets/gamma-mcp-github-policy-studio.png>)
3. In the flow's **Request phase**, select **+** to open the policy catalog, and then select **Rate Limit**.
4. Configure the limit. Set a **Limit** and a **Period**, for example 10 requests per 60 seconds, and set **Key** to an expression that resolves the caller's identity. This enables each identity draws on its own allowance rather than on a shared plan counter. For more infotmation about layered governance for MCP tools, see, [Govern MCP tool access](govern-mcp-tool-access.md "mention").
5. Add the **PII Filtering** policy. Select the AI Model Token Classification resource from the prerequisites, and then select the categories to redact, for example person, email, phone, location, financial account, and government ID. Leave **Confidence Threshold** at the default of `0.5`.
6. Select **Save**, and then deploy the server.

{% hint style="info" %}
To limit one tool rather than the whole server, add a **Condition** to the flow that matches the tool name, for example `{#context.attributes['mcp_tool_name'] == 'search_code'}`. Scoping a tight limit to `search_code` caps the tool an iterating agent calls most, without constraining the rest. For more information about applying policies to individual tool invocations, see [Apply policies to tool invocations](apply-policies-to-tool-invocations.md "mention").
{% endhint %}

{% hint style="warning" %}
PII Filtering fails the call rather than passing the payload through if no AI Model Token Classification resource is selected. Categories are a required setting with no default. A higher confidence threshold redacts less and risks letting data through. A lower threshold redacts more and risks removing the content that made the response useful.
{% endhint %}

#### Verification

To confirm that the policies are applied to the GitHub MCP server, complete the following steps:

1. Call `search_code` eleven times within 60 seconds as the same caller.
2. Confirm that the eleventh call returns `429`, and that a second caller's first call still succeeds.
3. Call `get_file_contents` on a file that contains an email address or a personal name.
4. Confirm that the response returns the file with each detected span replaced by `[REDACTED]`.

### Observe GitHub MCP interactions

A tool call through the Gateway has two legs. The **entrypoint** leg is the agent's call to the Composite MCP Server, and the **endpoint** leg is the Gateway's call to GitHub. Capturing both is what turns a tool call into an auditable event, because each leg answers a different question:

| Leg | What it records | What it answers |
| --- | --- | --- |
| Entrypoint request | The inbound call: headers, the caller's credential, the session, and the timestamp | Which identity called, and when |
| Endpoint request | The outbound JSON-RPC call to `https://api.githubcopilot.com/mcp/`, including the tool name and its arguments | Which tool ran, against which repository, with which arguments |
| Endpoint response | The payload GitHub returned | What the upstream actually sent back |
| Entrypoint response | The payload the agent received | What reached the model after policies ran |

Comparing the last two rows is the point. The endpoint response is the raw upstream payload, and the entrypoint response is the payload after PII Filtering, so the difference between them is exactly what the Gateway removed before the agent, and the model behind it, ever saw it.

To observe GitHub MCP interactions, complete the following steps:

1. Open your Composite MCP Server, navigate to the **Gateway** section, and select **Reporter Settings**.
2. In the **Settings** card, turn the reporter on, navigate to **Logging mode**, and then enable both **Entrypoint** (client to gateway) and **Endpoint** (gateway to upstream) to ensure that the inbound and outbound legs are both captured.
3. Enable both the **Request** and **Response** phases, and then enable the **Headers** and **Payload** content data so tool arguments and tool responses are recorded rather than only their metadata.
4. In the **OpenTelemetry** card, enable **Trace enabled** to emit execution spans for each call. Enable **OTel Logs** to emit the request and response payloads as OpenTelemetry log records correlated to the active trace, which links logs to traces in Grafana and other OpenTelemetry-compatible backends. Enable **Verbose** only while debugging a specific call, because it adds headers, context attributes, and policy execution detail to every span.
5. With **Trace enabled** and **Verbose** both on, a **Span Attribute Redaction** section appears. Add a rule for each attribute that carries a credential or a repository identifier you don't want exported.
6. Select **Save changes**.

   ![The Reporter Settings page with both logging modes, both phases, headers, and payload enabled, and the OpenTelemetry card below](<../../../.gitbook/assets/gamma-mcp-github-reporter-settings.png>)
7. Navigate to the **Secure** section, confirm that decision logging is enabled on **Fine-Grained Authorization**, and then deploy the server. Each evaluated call then records the subject, the action, the resource, the decision, and the policies that determined it.

{% hint style="warning" %}
Payload logging records the arguments an agent sends and the content a tool returns, which is the data you most want to review and also the data most likely to be sensitive. Enable it deliberately, pair it with span attribute redaction, and keep verbose tracing on only for as long as you are debugging. Detailed logging increases storage and affects Gateway performance.
{% endhint %}

To review the calls, open your Composite MCP Server and under **Observability** select **Logs**. Each row records the timestamp, the MCP method, the status, the response time, and whether the endpoint was reached. Filter by **MCP methods** to isolate `tools/call`.

![The runtime logs for the Composite MCP Server, showing a denied tools/call with no endpoint reached and a permitted tools/call with the endpoint reached](<../../../.gitbook/assets/gamma-mcp-github-runtime-logs.png>)

For the OpenTelemetry span view, which records the agent identity, the inputs and outputs, and the lineage of a single agent request across every tool call it made, see [Inspect your agent log](../../observe/inspect-your-agent-log.md "mention").

#### Verification

To confirm that GitHub MCP interactions are recorded, complete the following steps:

1. Call `get_file_contents` through the GitHub MCP server as a permitted caller, on a file that contains an email address.
2. Open the log entry for that call. Navigate to the **Request** page of the **Details** section, and then confirm that the **Consumer** column records the inbound call to your context path and that the **Gateway** column records the outbound call to `https://api.githubcopilot.com/mcp/`, with a body carrying the tool name and its arguments.

   ![One log entry expanded, with the consumer leg on the left and the gateway leg to api.githubcopilot.com on the right, credentials blurred](<../../../.gitbook/assets/gamma-mcp-github-log-entry-legs.png>)

3. On the **Response** page of the  **Details** section, compare the Gateway response with the consumer response, and then confirm that the email address is present in what GitHub returned and `[REDACTED]` in what the agent received.
4. Call `create_or_update_file` as a caller that the policy forbids.
5. In the log list, confirm that the denied call is recorded with a `403` status and an empty **Endpoint reached** column, while the permitted call shows a check mark. An unreached endpoint is the evidence that GitHub was never called.

{% hint style="info" %}
A `tools/list` or `initialize` call is answered from the composition rather than forwarded upstream, so those entries also show no endpoint reached. An unreached endpoint means the Gateway answered or denied the call itself.
{% endhint %}

A shared upstream token cannot produce any of this on GitHub's side, because GitHub attributes every call to the token's owner. The per-caller record exists only because the Gateway sits between the agent and the tool.

## Verification

To confirm that the GitHub MCP server is connected and secured, complete the following steps:

1. Connect an agent to the Composite MCP Server using a token for an identity in the engineering group.
2. Prompt the agent to summarize the open issues on the repository and read the file the top issue refers to.
3. Confirm that the agent completes the action, and that any personal data in the file or the issue body is redacted in what the agent received.
4. Prompt the agent to commit a fix for that issue to the repository.
5. Confirm that the agent reports that the action is not permitted, and that no commit appears on the repository.
6. Open the agent log.
7. Confirm that both interactions appear, one allowed and one denied, each attributed to the agent's own identity.

Step 5 is the result worth keeping. The agent held a valid token, the upstream credential on the Gateway had write access, and the write still did not happen, because the identity making the call was not permitted to make it. That containment holds whether the agent was asked to write by its operator or by content it read, which matters when the content is an issue body or a pull request description that anyone can open.

## Extend your GitHub MCP setup

Consider the following refinements once your governed GitHub MCP server is working:

* **Reference the agent, not only the user.** Create an agent identity so policies can name the agent making the call as a principal, and grant an autonomous agent less than the person who runs it. For more information about creating an agent identity, see [Create an agent identity](../create-an-agent-identity.md "mention").
* **Add conditions to write access.** Constrain `create_or_update_file` with a condition, for example a business-hours window or a corporate IP range, so an off-hours commit from an unexpected network is denied rather than reviewed after the fact.
* **Compose per role rather than per upstream.** A triage role governed by two forbid statements on a five-tool server is weaker than a triage role given a two-tool server. Curation removes the tool from `tools/list` as well as from the permitted set.
* **Add a longer-period allowance.** A per-minute rate limit does not bound a day. Add the Quota policy for allowances measured over longer periods, and Spike Arrest to smooth bursts.
* **Sync principals from your identity provider.** Connect a SCIM-compatible tenant so groups referenced in policies stay current as people join and leave teams.
* **Scope and rotate the upstream token.** The Gateway holds one credential for every caller, which concentrates the value of that token. Issue a fine-grained token limited to the repositories in scope, and rotate it on the schedule you apply to other shared secrets.

## Next steps

* [Layered governance for MCP tools](govern-mcp-tool-access.md "mention")
* [Add policies to your MCP server](add-policies-to-mcp-server.md "mention")
* [Apply policies to individual tool invocations](apply-policies-to-tool-invocations.md "mention")
* [Inspect your agent log](../../observe/inspect-your-agent-log.md "mention")
* [Monitor your MCP servers](../../observe/monitor-your-mcp-servers.md "mention")
