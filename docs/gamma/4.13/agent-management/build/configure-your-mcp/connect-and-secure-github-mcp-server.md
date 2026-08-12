---
description: Connect GitHub's MCP server to Gravitee, curate the tools it exposes, and
  secure them with authentication, fine-grained authorization, rate limits, and PII
  redaction. Follow the steps to get started.
---

# Connect and secure the GitHub MCP server

## Overview

* **Outcome.** GitHub's MCP server is reachable through Gravitee as a curated Composite MCP Server. Its tools are protected by authentication and per-tool authorization, its call volume is capped per caller, its responses are redacted, and every invocation is recorded against the identity that made it.
* **Use this when.** You want agents to reach GitHub's tools through Gravitee rather than connecting to `https://api.githubcopilot.com/mcp/` directly, so that one personal access token stays on the Gateway instead of being copied into every agent's configuration, and every tool call is authorized and audited against the caller's own identity.
* **Not covered here.**
  * [What the GitHub MCP server does and which tools it exposes](https://github.com/github/github-mcp-server)
  * [How Gravitee governs MCP servers](govern-mcp-tool-access.md "mention")
  * [Building the agent that calls these tools](../create-an-agent-identity.md "mention")

GitHub's MCP server authenticates with a personal access token, and that token carries every permission its owner holds. An agent handed the token can read any repository the token can read and write any repository the token can write, and GitHub records the activity as the token's owner rather than as the agent or the person who prompted it. Gravitee closes that gap without changing the upstream server: the token is held once on the Gateway, the tool surface is curated before any policy is written, and each call is authorized, limited, redacted, and logged under the caller's identity.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Gravitee Gamma 4.12 or later, with Agent Management enabled.
* Permission to register catalog entities, create and deploy an MCP Proxy, and author Authorization Management policies in the environment you are configuring.
* A GitHub personal access token scoped to the tools you plan to expose. A fine-grained token scoped to the repositories the agents need is sufficient. On each repository, grant **Contents: read** for `get_file_contents`, **Issues: read** for `list_issues`, **Pull requests: read** for `pull_request_read`, and **Contents: read and write** for `create_or_update_file`. See [GitHub's documentation](https://docs.github.com/en/authentication/keeping-your-account-secure/managing-your-personal-access-tokens).
* [An identity provider configured in Gravitee](../configure-your-access-management-instance.md "mention"), holding the groups your authorization policies reference.
* An [AI Model Token Classification resource](../ai-resources.md "mention") on the environment, if you are adding PII redaction.

{% hint style="warning" %}
Until you complete the authorization phase, any consumer holding a valid token for the server can invoke every tool you composed into it, including `create_or_update_file`, which commits to a repository. Complete the authorization and policy phases before you publish the server to consumers.
{% endhint %}

## Connect and secure the GitHub MCP server

To connect and secure the GitHub MCP server, complete the following steps:

1. [Connect the GitHub MCP server](#connect-the-github-mcp-server)
2. [Expose the MCP server](#expose-the-mcp-server)
3. [Authenticate access to the MCP server](#authenticate-access-to-the-mcp-server)
4. [Restrict tool access with fine-grained authorization](#restrict-tool-access-with-fine-grained-authorization)
5. [Apply policies to the MCP server](#apply-policies-to-the-mcp-server)
6. [Observe MCP interactions](#observe-mcp-interactions)

### Connect the GitHub MCP server

Registering the server adds it to the Catalog with its tools, which is what makes those tools selectable in MCP Studio and referenceable in authorization policies.

To connect the GitHub MCP server, complete the following steps:

1. Log in to the Gamma console.
2. From the sidebar, select **Agent Management**.
3. Navigate to **Catalog**, and then select **MCP Servers**.
4. Select **Add MCP server**.
5. In the **Server URL** field, enter the GitHub MCP server endpoint:

   ```
   https://api.githubcopilot.com/mcp/
   ```

6. Select **Verify URL**.
7. Under the authentication method, select **Static credential**, set the credential type to **Bearer token**, and then enter the personal access token from the prerequisites. Discovery uses the token to read the server's capabilities and does not persist it.
8. Select **Test connection**, and then select **Import MCP Server**.

#### Verification

To confirm that the MCP server is connected, complete the following steps:

1. Navigate to **Catalog**, and then select **MCP Servers**.
2. Confirm that the GitHub MCP server is listed with the type **Native** and the connection status **Connected**.
3. Confirm that the tools listed match the tools in [GitHub's documentation](https://github.com/github/github-mcp-server), and that the tool count is greater than zero.

{% hint style="info" %}
GitHub's MCP server exposes a large tool surface, and the exact set depends on the token's scopes and the account's plan. Registering the server catalogs everything discovered. The next step narrows that surface to the tools your agents need.
{% endhint %}

### Expose the MCP server

Rather than proxying GitHub's whole tool surface, use MCP Studio to compose a Composite MCP Server that exposes only the tools a role needs. Curation is the control that precedes all the others, because a tool you never compose is a tool no policy has to defend against, and one an agent's model never sees in `tools/list`.

The steps below build an engineering toolbelt from five GitHub tools: `list_issues`, `get_file_contents`, `search_code`, `pull_request_read`, and `create_or_update_file`.

To expose the MCP server, complete the following steps:

1. From the sidebar, select **Agent Management**, and then navigate to **Build**.
2. Select **Create MCP proxy**, and then select **Studio mode**.
3. In the **Define** step, enter a **Name**, for example `engineering-toolbelt`, and a **Context path**, for example `/engineering-toolbelt`.
4. In the **Compose** step, select the GitHub MCP server from the palette, and then select the five tools listed above. Leave every other tool cleared.
5. In the **Connect** step, select the GitHub MCP server, set the credential type to **Bearer token**, and then enter the personal access token. The Gateway injects it as an `Authorization` header on every upstream call, so the token is held once rather than distributed to each agent.
6. In the **Review** step, confirm the composition, and then select **Create & deploy**.

<!-- TODO: Screenshot of the Compose step, with the five selected GitHub tools and the rest of GitHub's tool surface visible but cleared -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-mcp-github-compose-tools.png" alt=""><figcaption><p>The Compose step. Only the selected tools reach the agent, whatever else the upstream server exposes.</p></figcaption></figure>

#### Verification

To confirm that the MCP server is exposed, complete the following steps:

1. Send a `tools/list` request to the Composite MCP Server's endpoint:

   ```sh
   curl -s https://<gateway-host>/engineering-toolbelt \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json, text/event-stream' \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```

2. Confirm that the response lists five tools and no others. An agent connected to this server sees only these five, whatever else GitHub exposes upstream.
3. Note that `tools/list` returns each tool under its composed name, for example `list_issues`. Authorization policies reference the same tool under its server-qualified identifier, in the form `github-mcp-server.list_issues`.

{% hint style="info" %}
If you compose tools from more than one upstream server and two tool names collide, assign an alias in the **Compose** step. See [Edit MCP Studio composition](../edit-mcp-studio-composition.md "mention").
{% endhint %}

### Authenticate access to the MCP server

Authorization policies can only distinguish callers if the Gateway knows who each caller is. Authenticate the server against an authorization server rather than a shared key, so that each token resolves to a user or an agent identity.

To require authentication for the MCP server, complete the following steps:

1. Open your Composite MCP Server, and then navigate to the **Secure** section.
2. In the consumer security list, select **Gravitee as Authorization Server**. To use an external identity provider, select **External Authorization Server** instead.
3. Save the configuration, and then deploy the server.

#### Verification

To confirm that authentication is enforced, complete the following steps:

1. Call the MCP server without a token:

   ```sh
   curl -s -o /dev/null -w '%{http_code}\n' https://<gateway-host>/engineering-toolbelt \
     -H 'Content-Type: application/json' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```

2. Confirm that the response is `401`.
3. Repeat the call with a valid access token.
4. Confirm that the response lists the available tools.

{% hint style="warning" %}
Do not select **API Key** or **Passthrough** on a server you intend to govern per caller. Neither resolves an identity, so every fine-grained authorization policy evaluates against the same subject.
{% endhint %}

### Restrict tool access with fine-grained authorization

At this point every authenticated caller can invoke all five tools, including the one that commits code. Fine-grained authorization narrows that per identity. When it is enabled, the Gateway adds the GAPL Authorization PEP to the server's `tools/call` flow and asks the in-gateway Policy Decision Point for a decision before it forwards anything upstream.

To restrict which tools each caller can use, complete the following steps:

1. Open your Composite MCP Server, navigate to the **Secure** section, and then enable **Fine-Grained Authorization**.
2. From the sidebar, select **Authorization**, select **MCPs**, and then select **+ Create policy**.
3. Enter a **Policy name**, and then switch to the **Code** tab.
4. Enter the policy. The following statement grants an engineering group every tool on the server:

   ```
   permit (
     principal in Group::"<engineering-group-id>",
     action,
     resource
   ) when { resource is MCPTool };
   ```

5. Select **Create and Deploy policy**.
6. Repeat steps 2 through 5 for each remaining statement. The following statement closes the one tool that writes, for the same group:

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

<!-- TODO: Screenshot of the policy Code tab showing the forbid statement on create_or_update_file, with the policy status shown as Deployed -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-mcp-github-forbid-policy.png" alt=""><figcaption><p>The forbid statement that closes the one tool that writes to a repository</p></figcaption></figure>

{% hint style="info" %}
A tool that no policy permits is denied. Nothing is allowed by omission, so the triage role above needs no forbid statement to be closed to the other three tools. A `forbid` statement always beats a `permit`, so a later broad grant cannot reopen `create_or_update_file`.

Every entity reference is an identifier, not a display name. `principal` takes the group's identifier, and `resource` takes the server-qualified tool identifier. Leave `action` unconstrained unless you intend to match one specific tool invocation. A clause that references a name where an identifier is expected matches nothing, and the call is then denied by default rather than reported as a malformed policy. See [Layered governance for MCP tools](govern-mcp-tool-access.md "mention").
{% endhint %}

#### Verification

To confirm that tool access is restricted, complete the following steps:

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

### Apply policies to the MCP server

Authorization decides which tools a caller reaches, not how often it calls them or what comes back. An agent that loops over search results can exhaust a shared GitHub rate limit while staying inside its permissions, and a permitted read of a file, an issue, or a pull request can return names and email addresses committed into the repository. Add a rate limit and a redaction policy on the `tools/call` flow to close both.

To apply policies to the MCP server, complete the following steps:

1. Open your Composite MCP Server, and then in the sidebar select **Policy Studio**.
2. Under **MCP Method Flows**, select **Add MCP method flow**, enter a **Flow name**, select the **`tools/call`** method, and then select **Create**.
3. In the flow's **Request** phase, select **Browse all** to open the **Add Policy** catalog, and then select **Rate Limit**.
4. Configure the limit. Set a **Limit** and a **Period**, for example 10 requests per 60 seconds, and set **Key** to an expression that resolves the caller's identity, so that each identity draws on its own allowance rather than on a shared plan counter. See [Layered governance for MCP tools](govern-mcp-tool-access.md "mention").
5. In the same phase, add the **PII Filtering** policy. Select the AI Model Token Classification resource from the prerequisites, and then select the categories to redact, for example person, email, phone, location, financial account, and government ID. Leave **Confidence Threshold** at its default of `0.5`.
6. Select **Save**, and then deploy the server.

{% hint style="info" %}
To limit one tool rather than the whole server, add a **Condition** to the flow that matches the tool name, for example `{#context.attributes['mcp_tool_name'] == 'search_code'}`. Scoping a tight limit to `search_code` caps the tool an iterating agent calls most, without constraining the rest. See [Apply policies to individual tool invocations](apply-policies-to-tool-invocations.md "mention").
{% endhint %}

{% hint style="warning" %}
PII Filtering fails the call rather than passing the payload through if no AI Model Token Classification resource is selected. Categories are a required setting with no default. A higher confidence threshold redacts less and risks letting data through. A lower threshold redacts more and risks removing the content that made the response useful.
{% endhint %}

#### Verification

To confirm that the policies are applied, complete the following steps:

1. Call `search_code` eleven times within 60 seconds as the same caller.
2. Confirm that the eleventh call returns `429`, and that a second caller's first call still succeeds.
3. Call `get_file_contents` on a file that contains an email address or a personal name.
4. Confirm that the response returns the file with each detected span replaced by `[REDACTED]`.

### Observe MCP interactions

A tool call through the Gateway has two legs. The **entrypoint** leg is the agent's call to the Composite MCP Server, and the **endpoint** leg is the Gateway's call to GitHub. Capturing both is what turns a tool call into an auditable event, because each leg answers a different question:

| Leg | What it records | What it answers |
| --- | --- | --- |
| Entrypoint request | The inbound call: headers, the caller's credential, the session, and the timestamp | Which identity called, and when |
| Endpoint request | The outbound JSON-RPC call to `https://api.githubcopilot.com/mcp/`, including the tool name and its arguments | Which tool ran, against which repository, with which arguments |
| Endpoint response | The payload GitHub returned | What the upstream actually sent back |
| Entrypoint response | The payload the agent received | What reached the model after policies ran |

Comparing the last two rows is the point. The endpoint response is the raw upstream payload, and the entrypoint response is the payload after PII Filtering, so the difference between them is exactly what the Gateway removed before the agent, and the model behind it, ever saw it.

To observe MCP interactions, complete the following steps:

1. Open your Composite MCP Server, and then in the sidebar select **Reporter Settings**.
2. In the **Settings** card, enable analytics, and then enable both the **Entrypoint** and **Endpoint** logging modes so the inbound and outbound legs are both captured.
3. Enable both the **Request** and **Response** phases, and then enable the **Headers** and **Payload** content data so tool arguments and tool responses are recorded rather than only their metadata.
4. In the **OpenTelemetry** card, enable **Trace enabled** to emit execution spans for each call. Enable **OTel Logs** to emit the request and response payloads as OpenTelemetry log records correlated to the active trace, which links logs to traces in Grafana and other OpenTelemetry-compatible backends. Enable **Verbose** only while debugging a specific call, because it adds headers, context attributes, and policy execution detail to every span.
5. Under **Span Attribute Redaction**, add a rule for each attribute that carries a credential or a repository identifier you don't want exported.
6. Select **Save changes**.
7. Navigate to the **Secure** section, confirm that decision logging is enabled on **Fine-Grained Authorization**, and then deploy the server. Each evaluated call then records the subject, the action, the resource, the decision, and the policies that determined it.

<!-- TODO: Screenshot of the MCP proxy's Reporter Settings page, with both logging modes and both phases enabled -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-mcp-github-reporter-settings.png" alt=""><figcaption><p>Both logging modes enabled, so the inbound and the outbound legs of each tool call are captured</p></figcaption></figure>

{% hint style="warning" %}
Payload logging records the arguments an agent sends and the content a tool returns, which is the data you most want to review and also the data most likely to be sensitive. Enable it deliberately, pair it with span attribute redaction, and keep verbose tracing on only for as long as you are debugging. Detailed logging increases storage and affects Gateway performance.
{% endhint %}

To review the calls in the console, select **Agent Management**, navigate to **Observe**, and then open the agent log. Each OpenTelemetry span records the agent identity, the tool invoked, the inputs and outputs, the latency, and the policy decision. The lineage view traces a single agent request through every tool call it made. See [Inspect your agent log](../../observe/inspect-your-agent-log.md "mention").

#### Verification

To confirm that interactions are recorded, complete the following steps:

1. Call `get_file_contents` through the MCP server as a permitted caller, on a file that contains an email address.
2. Open the log entry for that call, and then confirm that the entrypoint request records the caller's identity and that the endpoint request records the outbound call to `https://api.githubcopilot.com/mcp/`, carrying the tool name and its arguments.
3. Compare the endpoint response with the entrypoint response, and then confirm that the email address is present in what GitHub returned and `[REDACTED]` in what the agent received.
4. Call `create_or_update_file` as a caller that the policy forbids.
5. Confirm that the entry records the denial and has no endpoint leg at all. The absence of an outbound call is the evidence that GitHub was never reached.

{% hint style="info" %}
A `tools/list` call is answered from the composition rather than forwarded upstream, so its entry also has no endpoint leg. An absent endpoint leg means the Gateway answered or denied the call itself.
{% endhint %}

A shared upstream token cannot produce any of this on GitHub's side, because GitHub attributes every call to the token's owner. The per-caller record exists only because the Gateway sits between the agent and the tool.

<!-- TODO: Screenshot of a single log entry expanded to show the entrypoint and endpoint legs side by side, with the redacted span visible in the entrypoint response. Blur the token in the Authorization header. -->

<figure><img src="../../../.gitbook/assets/PLACEHOLDER-gamma-mcp-github-log-entry-legs.png" alt=""><figcaption><p>One tool call, both legs. The endpoint response carries the raw payload from GitHub, and the entrypoint response carries what the agent received.</p></figcaption></figure>

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

## Extend this setup

Consider the following refinements once the flow above is working:

* **Reference the agent, not only the user.** Create an agent identity so policies can name the agent making the call as a principal, and grant an autonomous agent less than the person who runs it. See [Create an agent identity](../create-an-agent-identity.md "mention").
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
