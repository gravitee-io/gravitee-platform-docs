---
description: Connect Stripe's MCP server to Gravitee, withhold the tool that performs
  every write, and deny refunds per caller. Follow the steps to get started.
---

# Connect and secure the Stripe MCP server

## Overview

* **Outcome.** Stripe's MCP server is reachable through Gravitee as a curated Composite MCP Server. The tool that performs every write in the Stripe API is never exposed, refunds are permitted for one role and denied for another, call volume is capped per caller, and customer data is redacted on the way back.
* **Use this when.** You want an agent to look up customers, charges, and invoices through Gravitee rather than connecting to Stripe's MCP server directly, and you need the ability to move money governed apart from the ability to read.
* **Not covered here.**
  * [What the Stripe MCP server does and which tools it exposes](https://docs.stripe.com/mcp)
  * [How Gravitee governs MCP servers](govern-mcp-tool-access.md "mention")
  * [Building the agent that calls these tools](../create-an-agent-identity.md "mention")

Stripe's MCP server exposes a tool that its own definition describes as writing data through any Stripe API `POST`, `PATCH`, `PUT`, or `DELETE` operation, so creating a customer and canceling a subscription are the same tool. A restricted API key limits what that tool can execute, and it does not change what the agent sees: a restricted key and an unrestricted key return the same tool list, so the model plans against the full write surface regardless of what the key can actually do. The granularity you need does not exist at the key layer or at the tool layer. It exists at the caller layer, which is where Gravitee applies it.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Gravitee Gamma 4.12 or later, with Agent Management enabled.
* Permission to register catalog entities, create and deploy an MCP Proxy, and author Authorization Management policies in the environment you are configuring.
* A Stripe account with MCP access enabled, and a restricted API key scoped to the resources the agent needs. Stripe manages MCP access for sandbox and live mode independently, so enabling it in one and testing against the other produces a confusing failure. For more information about the Stripe MCP server and its API keys, go to [Stripe's documentation](https://docs.stripe.com/mcp).
* An identity provider that is configured in Gravitee and holds the groups that your authorization policies reference. For more information about configuring an identity provider, see [Configure your Access Management instance](../configure-your-access-management-instance.md "mention").
* If you are adding PII redaction on your environment, an AI Model Token Classification resource. For more information about AI resources, see [AI resources](../ai-resources.md "mention").

{% hint style="warning" %}
Agent Management and Authorization Management are licensed as separate packs. Without the `agent-management` and `authorization-management` packs the module renders as a locked upgrade prompt rather than an error, which reads as though the feature is missing from your version. Contact your Gravitee account manager if either is unavailable.

Until you complete the authorization phase, any consumer holding a valid token for the server can invoke every tool you composed into it, including `create_refund`, which returns money to a customer. Complete the authorization and policy phases before you publish the server to consumers.
{% endhint %}

## Connect and secure the Stripe MCP server

To connect and secure the Stripe MCP server, complete the following steps:

1. [Connect the Stripe MCP server](#connect-the-stripe-mcp-server)
2. [Expose the Stripe tools as a Composite MCP Server](#expose-the-stripe-tools-as-a-composite-mcp-server)
3. [Authenticate access to your deployed Stripe MCP server](#authenticate-access-to-your-deployed-stripe-mcp-server)
4. [Restrict Stripe tool access with fine-grained authorization](#restrict-stripe-tool-access-with-fine-grained-authorization)
5. [Apply policies to the Stripe MCP server](#apply-policies-to-the-stripe-mcp-server)
6. [Observe Stripe MCP interactions](#observe-stripe-mcp-interactions)

### Connect the Stripe MCP server

Registering the server adds it to the Catalog with its tools, which is what makes those tools selectable in MCP Studio and available to authorization policies.

To connect the Stripe MCP server, complete the following steps:

1. Sign in to the Gravitee console.
2. From the product navigation menu, select **Agent Management**.
3. Navigate to the **Import** section, and then select **MCP Servers**.
4. Select **+ Add MCP server**. The **Add MCP server** wizard opens.
5. In the **Endpoint URL** field, enter the following Stripe MCP server endpoint:

   ```
   https://mcp.stripe.com
   ```

   The **Transport** is fixed to **Streamable HTTP**.

6. Select **Test connection**.
7. On the **Configure connection** step, select **Static credentials**, set the credential type to **Bearer token**, and then enter the restricted API key. Discovery uses the key to read the server's capabilities. It is stored on the Catalog entry and is not used for runtime traffic. Runtime traffic authenticates with the credential you set on the Composite MCP Server.
8. Select **Test connection** again to re-run discovery, and then on the **Review entry** step select **Save catalog entry**.

{% hint style="info" %}
Grant the restricted key write access only where the agent must genuinely write. Stripe's finest permission grouping combines charges and refunds, so a key able to refund is also able to write charges. That is the limitation this guide works around rather than one it removes.
{% endhint %}

#### Verification

To confirm that the Stripe MCP server is connected, complete the following steps:

1. Navigate to the **Import** section, and then select **MCP Servers**.
2. Confirm that `stripe-mcp` is listed, with the entity ID `mcp-server.stripe-mcp`, the transport `http`, and the endpoint you entered.
3. Select the server to open its detail page, and then confirm the **Overview** card shows the protocol version, an **Auth type** of **Bearer token**, and a **Capabilities** row with a tool count.
4. Confirm that the tools listed under **Tools** match the tools documented for the Stripe MCP server. The set can be smaller than the documentation lists, because some tools are gated on the account.

   ![The MCP Servers catalog listing the registered Stripe server](<../../../.gitbook/assets/gamma-mcp-servers-catalog.png>)

{% hint style="info" %}
Authorization policies reference tools by the server's slug, `stripe-mcp`, and not by the entity ID shown alongside it. A resource written as `MCPTool::"mcp-server.stripe-mcp.create_refund"` carries the entity-ID prefix, matches nothing, and is denied by default.
{% endhint %}

### Expose the Stripe tools as a Composite MCP Server

Rather than proxying Stripe's whole tool surface, use MCP Studio to compose a Composite MCP Server that exposes only the tools a role needs. Curation is the control that precedes all the others, because a tool you never compose is a tool no policy has to defend against, and one an agent's model never sees in `tools/list`.

The following steps build a finance support toolbelt from four Stripe tools: `stripe_api_read`, `get_stripe_account_info`, `search_stripe_documentation`, and `create_refund`.

To expose the Stripe tools as a Composite MCP Server, complete the following steps:

1. From the **Agent Management** menu, navigate to **Secure**, and then select **MCP Proxies**.
2. Select **+ Create MCP proxy**, and then select **Studio mode**.
3. In the **General information** section, enter a **Name**, for example `finance-support-toolbelt`, and a **Context path**, for example `/finance-support-toolbelt`.
4. On the **Secure** page, select **Gravitee as Authorization Server**. To use an external identity provider, select **External Authorization Server** instead.

{% hint style="warning" %}
Fine-grained authorization requires OAuth2 with Gravitee as the authorization server. If Access Management is not configured in this environment, that option is unavailable and the only selectable method is API Key, which does not carry user identity. Every policy in this guide would then evaluate against the same subject. Configure Access Management before you continue.
{% endhint %}
5. In the **Compose** step, select the Stripe MCP server from the palette, and then select only the four tools listed at the start of this section. Leave `stripe_api_write` unselected.
6. In the **Connect** step, select the Stripe MCP server, set the credential type to **Bearer token**, and then enter the restricted API key. The Gateway injects it as an `Authorization` header on every upstream call. The key is held once rather than distributed to each agent.
7. In the **Review** step, confirm the composition, and then select **Create & deploy**.

   ![The Compose step showing all 9 discovered Stripe tools with 4 selected and stripe_api_write left unselected](<../../../.gitbook/assets/gamma-mcp-stripe-compose-tools.png>)

Two choices in that list carry the argument of this guide.

`stripe_api_write` is left out entirely, so the tool that performs every write in the Stripe API never appears in `tools/list` and the model behind the agent never learns that it exists. Curation removes what nobody should reach.

`create_refund` is included so it can be denied per caller in a later section. Authorization then decides who reaches what curation left in place.

{% hint style="info" %}
The credential on the Catalog entry authenticates discovery, and the credential on the Composite MCP Server authenticates traffic at runtime. Keep both current when you rotate the key. Update the Catalog entry, and update the Composite MCP Server on the **Tools** page of the **Design** section by selecting **Edit tools** and replacing the credential on the **Connect** step. Updating one alone produces an upstream failure that looks identical to an authorization failure.
{% endhint %}

#### Verification

To confirm that the Stripe tools are exposed, complete the following steps:

1. Send a `tools/list` request to the Composite MCP Server's endpoint:

   ```sh
   curl -s https://<gateway-host>/finance-support-toolbelt \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json, text/event-stream' \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```

2. Confirm that the response lists only the four tools, and that `stripe_api_write` is absent. The tools you did not compose are absent from this list rather than denied at call time. They never reach the agent, and the model behind it never has them as options.
3. Note that `tools/list` returns each tool under its composed name, for example `create_refund`. Authorization policies reference the same tool under its server-qualified identifier, in the form `stripe-mcp.create_refund`.

### Authenticate access to your deployed Stripe MCP server

{% hint style="info" %}
If you authenticated your Stripe MCP server during the [Expose the Stripe tools as a Composite MCP Server](#expose-the-stripe-tools-as-a-composite-mcp-server) section, you can skip this section and go to [Restrict Stripe tool access with fine-grained authorization](#restrict-stripe-tool-access-with-fine-grained-authorization).
{% endhint %}

Authorization policies can only distinguish callers if the Gateway knows who each caller is. Authenticate the server against an authorization server rather than a shared key, so that each token resolves to a user or an agent identity.

To require authentication for the Stripe MCP server, complete the following steps:

1. On an existing server, open the MCP Server, navigate to the **Consumer access** section, and then select **Plans**.

{% hint style="warning" %}
Do not select **Keyless** or **API Key** on a server you intend to govern per caller. Neither resolves a user identity, so every fine-grained authorization policy evaluates against the same subject.
{% endhint %}

2. Select **+ Create plan**, and then select **OAuth2**.
3. Configure and publish the plan, and then deploy the server.

#### Verification

To confirm that authentication to the Stripe MCP server is enforced, complete the following steps:

1. Call the Stripe MCP server without a token:

   ```sh
   curl -s -i https://<gateway-host>/finance-support-toolbelt \
     -H 'Content-Type: application/json' \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```

2. You receive a response like the following:

   ```
   HTTP/1.1 401 Unauthorized
   WWW-Authenticate: Bearer resource_metadata="https://<gateway-host>/.well-known/oauth-protected-resource/finance-support-toolbelt" scope="openid profile email offline_access stripe_api_read get_stripe_account_info search_stripe_documentation create_refund"

   {"message":"Unauthorized","http_status_code":401}
   ```

3. Confirm that `stripe_api_write` is absent from the advertised scopes, which shows at the protocol level, before any policy runs, that the tool is not merely denied but not present.
4. Repeat the call with a valid access token, and then confirm that the response is `200` and lists the four tools.

{% hint style="info" %}
The plan's required scopes are written from the composition when the server is created, and they stay as set. Update them on the plan whenever you add or remove a tool, otherwise a client is asked to request a scope it cannot use.
{% endhint %}

### Restrict Stripe tool access with fine-grained authorization

All authenticated callers can invoke all four tools, including the one that returns money. Fine-grained authorization narrows that per identity. When you enable fine-grained authorization, the Gateway adds the GAPL Authorization PEP to the server's `tools/call` flow and asks the in-gateway Policy Decision Point for a decision before it forwards anything upstream.

To restrict which tools each caller can use, complete the following steps:

1. Open your Composite MCP Server. On the **Overview** page, turn on **Enable FGA**. A confirmation panel reports that the Authorization PEP has been added to the Policy Studio.
2. From the product selector, open **Authorization Management**, navigate to the **Policy Management** section, and then select **MCPs**.
3. Select **+ Create policy**, enter a **Policy name**, and then switch to the **Code** tab.
4. Enter the policy. The following statement grants a support group the three read tools:

   ```
   permit (
     principal in Group::"<support-group-id>",
     action,
     resource
   ) when {
     resource == MCPTool::"stripe-mcp.stripe_api_read" ||
     resource == MCPTool::"stripe-mcp.get_stripe_account_info" ||
     resource == MCPTool::"stripe-mcp.search_stripe_documentation"
   };
   ```

5. Select **Create and Deploy policy**.
6. Repeat steps 2 to 5 for each remaining statement. The following statement closes refunds for the support group:

   ```
   forbid (
     principal in Group::"<support-group-id>",
     action,
     resource == MCPTool::"stripe-mcp.create_refund"
   );
   ```

   The following statement permits refunds for an approver group only:

   ```
   permit (
     principal in Group::"<approver-group-id>",
     action,
     resource == MCPTool::"stripe-mcp.create_refund"
   );
   ```

The Gateway picks up a deployed policy without a restart, typically within a minute.

![The deployed authorization policies listed in Authorization Management](<../../../.gitbook/assets/gamma-mcp-authorization-policies.png>)

{% hint style="warning" %}
A mistyped resource fails in opposite directions depending on the statement. In a `permit` statement it fails closed, because nothing matches and the call is denied. In a `forbid` statement it fails open, because the statement never matches and any broader `permit` still applies. Confirm every `forbid` statement by making the call and reading the decision in the log, rather than by reading the policy back.
{% endhint %}

{% hint style="info" %}
A tool that no policy permits is denied. Nothing is allowed by omission. A `forbid` statement always beats a `permit`, so a later broad grant cannot reopen `create_refund` for the support group.

Every entity reference is an identifier, not a display name. `principal` takes the group's identifier, and `resource` takes the server-qualified tool identifier taken from the registered Catalog entry. For more information about layered governance for MCP tools, see [Govern MCP tool access](govern-mcp-tool-access.md "mention").
{% endhint %}

#### Verification

To confirm that Stripe tool access is restricted, complete the following steps:

1. As a caller in the support group, call `stripe_api_read`, and then confirm that it returns data from Stripe.
2. As the same caller, call `create_refund`, and then confirm that the response is `403`. The decision runs in the request phase, so the Gateway denies the call before it reaches Stripe.
3. As a caller in the approver group, call `create_refund` with a payment intent that does not exist:

   ```sh
   curl -s https://<gateway-host>/finance-support-toolbelt \
     -H 'Content-Type: application/json' \
     -H 'Accept: application/json, text/event-stream' \
     -H "Authorization: Bearer $APPROVER_TOKEN" \
     -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"create_refund",
          "arguments":{"payment_intent":"pi_missing"}}}'
   ```

4. Confirm that the call is answered with an error from Stripe reporting that no such payment intent exists.

Step 4 is the result worth keeping. The error comes from Stripe, which proves that the call reached it and that the key really can refund. The identical call from the support group never left the Gateway. Using a payment intent that does not exist demonstrates this without creating a refund.

{% hint style="info" %}
Read the tool result as well as the HTTP status. A call that reaches Stripe and is rejected there is still a successful call at the transport level, so the result tells you which layer answered.

Stripe's write tools accept an optional `human_confirmation` argument that asks a person to approve the call. It is the agent that chooses whether to invoke it, so an agent talked into a write is exactly the agent that will not ask first. A Gateway denial does not consult the agent.
{% endhint %}

### Apply policies to the Stripe MCP server

Authorization decides which tools a caller reaches, not how often it calls them or what comes back. An agent looping over reads can exhaust a shared Stripe allowance while staying inside its permissions, and a permitted read returns customer names, email addresses, and phone numbers by construction. Add a rate limit and a redaction policy on the `tools/call` flow to close both.

To apply policies to the Stripe MCP server, complete the following steps:

1. Open your Composite MCP Server, navigate to the **Design** section, and then select **Policy Studio**.
2. Navigate to the **MCP method flows** section, add a flow, enter a **Flow name**, select the **`tools/call`** method, and then select **Create**. If you enabled FGA, this flow already exists, with the Authorization PEP already in the request phase.

   ![The Policy Studio tools/call flow with the Authorization PEP, Rate Limit, and PII Filtering policies](<../../../.gitbook/assets/gamma-mcp-stripe-policy-studio.png>)

3. In the flow's **Request phase**, select **+** to open the policy catalog, and then select **Rate Limit**.
4. Configure the limit:
   * Set **Max requests (static)** to the number of calls allowed, for example `5`.
   * Set **Static time duration** and **Static time unit** to the window, for example `60` and `SECONDS`. The window is two fields rather than one.
   * Set **Key** to `{#context.attributes['user']}` so that each identity draws on its own allowance rather than on a shared plan counter.
   * Enable **Add response headers** so that responses carry `X-Rate-Limit-Limit`, `X-Rate-Limit-Remaining`, and `X-Rate-Limit-Reset`.
   * Set **Error strategy** to block on internal error where the limit is a control rather than a courtesy.
5. Add the **PII Filtering** policy. Select the AI Model Token Classification resource from the prerequisites, and then select the categories to redact, for example person, email, phone, location, financial account, and government ID. Leave **Confidence Threshold** at the default of `0.5`.
6. Select **Save**, and then deploy the server. Saving alone does not update the Gateway. Until you deploy, the console reports that the deployable is out of sync.

{% hint style="info" %}
To limit one tool rather than the whole server, add a **Condition** to the flow that matches the tool name, for example `{#context.attributes['mcp_tool_name'] == 'stripe_api_read'}`. Scoping a tight limit to the tool an iterating agent calls most caps it without constraining the rest. For more information, see [Apply policies to tool invocations](apply-policies-to-tool-invocations.md "mention").
{% endhint %}

{% hint style="warning" %}
PII Filtering fails the call rather than passing the payload through if no AI Model Token Classification resource is selected. Categories are a required setting with no default. A higher confidence threshold redacts less and risks letting data through. A lower threshold redacts more and risks removing the content that made the response useful.

The two policies default in opposite directions on failure. The authorization policy denies when it has no policy snapshot. The rate limit policy accepts requests when its store is unavailable, which is why step 4 sets its error strategy explicitly.
{% endhint %}

{% hint style="info" %}
Policy order decides who pays for denied traffic. With the Authorization PEP ahead of the rate limit, a forbidden caller is rejected before consuming any allowance. Place the rate limit first instead if your goal is to throttle abusive callers rather than to protect the allowance of legitimate ones. Neither order is automatically correct.
{% endhint %}

#### Verification

To confirm that the policies are applied to the Stripe MCP server, complete the following steps:

1. Call `stripe_api_read` six times within 60 seconds as the same caller.
2. Confirm that the sixth call returns `429` and carries the `X-Rate-Limit-Limit`, `X-Rate-Limit-Remaining`, and `X-Rate-Limit-Reset` headers, and that a second caller's first call still succeeds.
3. Read a customer record directly from Stripe, using the upstream credential.
4. Read the same record through the Composite MCP Server.
5. Confirm that `name`, `email`, and `phone` are replaced with `[REDACTED]`, and that fields the classifier does not detect as personal, such as `id` and `description`, are unchanged.

{% hint style="info" %}
Comparing a direct upstream read against a read through the Gateway is the way to confirm redaction. Detection is probabilistic, so treat redaction as a depth control rather than as the only control for a field you already know is sensitive.

Redaction replaces each detected value with a marker, so a redacted field can carry a string where the upstream sent another type. An empty object can return as the string `[REDACTED]`. Test your agent against redacted responses as well as against the upstream shape.
{% endhint %}

### Observe Stripe MCP interactions

A tool call through the Gateway has two legs. The **entrypoint** leg is the agent's call to the Composite MCP Server, and the **endpoint** leg is the Gateway's call to Stripe. Capturing both is what turns a tool call into an auditable event, because each leg answers a different question:

| Leg | What it records | What it answers |
| --- | --- | --- |
| Entrypoint request | The inbound call: headers, the caller's credential, the session, and the timestamp | Which identity called, and when |
| Endpoint request | The outbound JSON-RPC call to `https://mcp.stripe.com`, including the tool name and its arguments | Which tool ran, against which resource, with which arguments |
| Endpoint response | The payload Stripe returned | What the upstream sent back |
| Entrypoint response | The payload the agent received | What reached the model after policies ran |

To observe Stripe MCP interactions, complete the following steps:

1. Open your Composite MCP Server, navigate to the **Gateway** section, and select **Reporter Settings**.
2. In the **Settings** card, turn the reporter on, navigate to **Logging mode**, and then enable both **Entrypoint** (client to gateway) and **Endpoint** (gateway to upstream) to ensure that the inbound and outbound legs are both captured.
3. Enable both the **Request** and **Response** phases, and then enable the **Headers** and **Payload** content data so tool arguments and tool responses are recorded rather than only their metadata.
4. In the **OpenTelemetry** card, enable **Trace enabled** to emit execution spans for each call. Enable **OTel Logs** to emit the request and response payloads as OpenTelemetry log records correlated to the active trace. Enable **Verbose** only while debugging a specific call, because it adds headers, context attributes, and policy execution detail to every span.
5. With **Trace enabled** and **Verbose** both on, a **Span Attribute Redaction** section appears. Add a rule for each attribute that carries a credential or a customer identifier you do not want exported.
6. Select **Save changes**.
7. Navigate to the **Design** section, select **Policy Studio**, open the `tools/call` flow, and then select **Gravitee Authorization PEP (GAPL)**. Confirm that **Log every decision (SLF4J)** is enabled, and then deploy the server. Each evaluated call then writes a line to the Gateway's log output recording the subject, the action, the resource, the decision, and the matched policy. A denial carrying the reason `No applicable policy` means that nothing matched at all, which is default deny rather than your forbid statement.

{% hint style="warning" %}
Stripe's MCP server returns JSON, and on that path response policies run before either leg is recorded, so both logged legs show the same redacted payload and you cannot prove redaction by comparing them. Confirm redaction by reading the record directly from the upstream with its own credential and comparing that against a read through the Composite MCP Server.

A streaming upstream records the endpoint leg differently. The Atlassian MCP server, measured on the same build and the same reporter settings, logged the endpoint leg before response policies ran, so the personal data reached the log store in clear even though the agent received `[REDACTED]`. Two upstreams are not a rule, so confirm which way yours behaves with one permitted call, and treat payload logging as its own decision rather than as a consequence of redaction wherever the payload is sensitive.
{% endhint %}

To review the calls, open your Composite MCP Server and under **Observability** select **Logs**. Each row records the timestamp, the MCP method, the status, the response time, and whether the endpoint was reached. Filter by **MCP methods** to isolate `tools/call`.

For the OpenTelemetry span view, see [Inspect your agent log](../../observe/inspect-your-agent-log.md "mention").

#### Verification

To confirm that Stripe MCP interactions are recorded, complete the following steps:

1. Call `stripe_api_read` as a permitted caller, on a customer record containing an email address.
2. Open the log entry for that call. Navigate to the **Request** page of the **Details** section, and then confirm that the **Consumer** column records the inbound call to your context path and that the **Gateway** column records the outbound call to `https://mcp.stripe.com`, with a body carrying the tool name and its arguments.
3. On the **Response** page of the **Details** section, confirm that both response legs show `[REDACTED]`, which is the JSON-path behaviour described above.
4. Call `create_refund` as a caller that the policy forbids.
5. In the log list, confirm that the denied call is recorded with a `403` status and an empty **Endpoint reached** column, while the permitted call shows a check mark. An unreached endpoint is the evidence that Stripe was never called.
6. Confirm that the decision log records the subject, the resource, and a `FORBID` decision naming the policy that denied it.

{% hint style="info" %}
A `tools/list` or `initialize` call is answered from the composition rather than forwarded upstream, so those entries also show no endpoint reached. An unreached endpoint means the Gateway answered or denied the call itself.
{% endhint %}

A shared upstream key cannot produce any of this on Stripe's side, because Stripe attributes every call to the key rather than to the person or agent behind it. The per-caller record exists only because the Gateway sits between the agent and the tool.

## Verification

To confirm that the Stripe MCP server is connected and secured, complete the following steps:

1. Connect an agent to the Composite MCP Server using a token for an identity in the support group.
2. Prompt the agent to look up a customer and to summarize their recent charges.
3. Confirm that the agent completes the action, and that the customer's personal data is redacted in what the agent received.
4. Prompt the agent to refund one of those charges.
5. Confirm that the agent reports that the action is not permitted, and that no refund appears in the Stripe dashboard.
6. Open the agent log.
7. Confirm that both interactions appear, one allowed and one denied, each attributed to the agent's own identity.

Step 5 is the result worth keeping. The agent held a valid token, the restricted key on the Gateway could issue the refund, and the refund still did not happen, because the identity making the call was not permitted to make it.

## Extend your Stripe MCP setup

Consider the following refinements once your governed Stripe MCP server is working:

* **Reference the agent, not only the user.** Create an agent identity so policies can name the agent making the call as a principal, and grant an autonomous agent less than the person who runs it. For more information about creating an agent identity, see [Create an agent identity](../create-an-agent-identity.md "mention").
* **Add conditions to refund access.** Constrain `create_refund` with a condition, for example a business-hours window or a corporate IP range, so an out-of-hours refund from an unexpected network is denied rather than reviewed after the fact.
* **Compose per role rather than per upstream.** An approver role and a support role are better served by two servers than by one server and a forbid statement, because curation removes `create_refund` from `tools/list` as well as from the permitted set.
* **Add a longer-period allowance.** A per-minute rate limit does not bound a day. Add the Quota policy for allowances measured over longer periods, and Spike Arrest to smooth bursts.
* **Sync principals from your identity provider.** Connect a SCIM-compatible tenant so groups referenced in policies stay current as people join and leave teams.
* **Scope and rotate the upstream key in both places.** The Gateway holds one credential for every caller. Issue a restricted key limited to the resources in scope, and when you rotate it update the Catalog entry and the Composite MCP Server together.

## Next steps

* [Layered governance for MCP tools](govern-mcp-tool-access.md "mention")
* [Add policies to your MCP server](add-policies-to-mcp-server.md "mention")
* [Apply policies to individual tool invocations](apply-policies-to-tool-invocations.md "mention")
* [Inspect your agent log](../../observe/inspect-your-agent-log.md "mention")
* [Monitor your MCP servers](../../observe/monitor-your-mcp-servers.md "mention")
