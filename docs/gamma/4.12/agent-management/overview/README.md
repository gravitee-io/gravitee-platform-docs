---
hidden: false
noIndex: false
description: Agent Management governs LLM, MCP, and agent-to-agent traffic from one control plane. Find the use case you need and the guide that covers it.
---

# Agent Management overview

Agent Management is Gravitee's product line for governing AI agent traffic. It provides a unified control plane and runtime for every protocol in the agentic stack: LLM calls, MCP tool invocations, and agent-to-agent (A2A) delegations. It adds end-to-end observability, fine-grained authorization, and identity for every agent that touches your enterprise infrastructure.

<figure><img src="../../.gitbook/assets/gamma-aim-ai-gateway-reference-architecture.png" alt="AI Gateway reference architecture, showing the control plane, the three proxies inside the AI Gateway, the identity and observability components, and the upstream targets"><figcaption><p>The AI Gateway reference architecture. Consumers and the Edge Daemon reach the AI Gateway, which routes LLM, MCP, and A2A traffic to upstream targets under a shared authentication, policy, and observability chain.</p></figcaption></figure>

## Why Agent Management exists

Enterprise AI adoption introduces three classes of traffic that existing API gateways and identity systems weren't designed for:

* **LLM traffic.** Engineering teams use Claude Code, Cursor, and ChatGPT Enterprise with no central visibility into cost, model usage, or data exposure.
* **MCP traffic.** Agents call tools on upstream MCP servers such as HubSpot, GitHub, Salesforce, and Jira using shared API keys or unaudited credentials.
* **A2A traffic.** Multi-agent systems delegate work across trust boundaries with no authorization, lineage, or cost attribution per delegation.

Agent Management extends the gateway infrastructure that already governs API and event traffic to cover these three protocol types, using the same Catalog, the same authorization engine, and the same enforcement architecture.

## Get started

| Start here | What you do |
| --- | --- |
| [**Create your first MCP server**](../get-started/create-your-first-mcp-server.md) | Configure an MCP Proxy in front of an upstream MCP server, and then verify tool invocations through the AI Gateway. |
| [**Create your first LLM Proxy**](../get-started/create-your-llm-proxy.md) | Configure an LLM Proxy, connect it to a model provider, and then send a test prompt. |
| [**Expose your agent with the A2A Proxy**](../build/expose-agent-with-a2a-proxy.md) | Make an upstream agent's skills discoverable and callable through the gateway. |
| [**Roles and permissions**](../get-started/roles-and-permissions.md) | Check which environment-scoped permissions govern the resources you need to create. |

## The three proxy types

The AI Gateway is the unified runtime that processes LLM, MCP, and A2A traffic. It consists of three proxies that share an authentication chain, a policy chain, an observability chain, and an Authorization Management integration point:

| Proxy | What it governs | Key capabilities |
| --- | --- | --- |
| **[LLM Proxy](../build/llm-proxies/README.md)** | Traffic to LLM providers (OpenAI, Anthropic, Gemini, Bedrock, Vertex AI) | Guardrails, PII filtering, token-based rate limiting, structured output, per-token cost attribution |
| **[MCP Proxy](../build/mcp-proxies/README.md)** | Tool invocations on upstream MCP servers | Two modes: **Proxy mode** (transparent governance) and **Studio mode** (composition of Composite MCP Servers). Protocol-native JSON-RPC 2.0, OAuth authorization discovery, credential mediation |
| **[A2A Proxy](../build/a2a-proxies/README.md)** | Agent-to-agent delegations | Skill discovery via `/.well-known/agent-card.json`, per-plan client authentication, wire-level policy enforcement |

## Use cases for Agent Management

### Give every team governed access to models

| Outcome | Feature |
| --- | --- |
| Provider credentials are held once on the AI Gateway instead of being copied into every team's application configuration. | [Create an LLM Proxy](../build/create-an-llm-proxy.md) |
| Each consumer authenticates with its own credential, so usage, rate limits, and cost can be attributed per consumer. | [Manage subscriptions](../publish/manage-subscriptions.md) |
| Existing AI tools route through governance by setting an environment variable, with no code changes. | [Create an LLM Proxy](../build/create-an-llm-proxy.md#zero-code-integration) |
| An OpenAI SDK, an Anthropic SDK, and a Gemini SDK all point at the same proxy and each receives answers in its own format. | [Accepted request formats](../build/accepted-request-formats.md) |
| Traffic moves between models without touching the applications that consume the proxy. | [Override the model at runtime](../build/override-the-model-at-runtime.md) |

### Expose existing enterprise assets as agent tools

| Outcome | Feature |
| --- | --- |
| REST APIs already governed in API Management become agent-callable tools, carrying over their security plans, policies, and backend configuration. | [Create API tools](../import/create-api-tools.md) |
| An agent gets exactly the tools it needs, composed from several upstream servers into one governed endpoint. | [Create an MCP Studio](../build/create-an-mcp-studio.md) |
| Skill packages, prompt templates, repository resources, and knowledge sources are cataloged and composable alongside MCP-native tools. | [Upload skills](../import/upload-skills.md), [Import prompts](../import/import-prompts.md), [Add MCP resources](../import/add-mcp-resources.md), [Add a knowledge source](../import/add-knowledge-source.md) |
| An external agent that publishes an A2A agent card is registered in the Catalog from its endpoint. | [Register an agent](../import/import-an-agent.md) |

### Constrain what an agent can do through a tool

| Outcome | Feature |
| --- | --- |
| A caller reaches only the tools its identity permits, and a call that matches no permit is denied rather than allowed by omission. | [Layered governance for MCP tools](../build/configure-your-mcp/govern-mcp-tool-access.md) |
| A shared upstream token stops conferring its owner's full permission set on every agent that holds it. | [Connect and secure the GitHub MCP server](../build/configure-your-mcp/connect-and-secure-github-mcp-server.md) |
| A permitted caller can't call a permitted tool more often than you intended, with each identity given its own allowance. | [Layered governance for MCP tools](../build/configure-your-mcp/govern-mcp-tool-access.md#rate-limits-decide-how-often) |
| Personal data in a tool response is redacted before it reaches the agent and the model behind it. | [Layered governance for MCP tools](../build/configure-your-mcp/govern-mcp-tool-access.md#redaction-decides-what-comes-back) |
| A limit applies to one high-value tool rather than to the whole server. | [Apply policies to individual tool invocations](../build/configure-your-mcp/apply-policies-to-tool-invocations.md) |

### Screen prompts and responses

| Outcome | Feature |
| --- | --- |
| Prompts carrying toxicity, harmful intent, or jailbreak prompt injections are logged or blocked before they reach the provider. | [Configure text classification](../build/configure-text-classification.md) |
| The classification and embedding models run locally on the AI Gateway rather than calling a third-party screening service. | [AI resources](../build/ai-resources.md) |
| Token spend is capped per consumer over a rolling period, counting the tokens the provider bills you for rather than the number of calls. | [Add the Token Rate Limit policy](../build/add-the-token-rate-limit-policy.md) |
| Response format constraints are enforced on model responses without changing the client. | [Configure an LLM Proxy](../build/configure-an-llm-proxy.md#structured-output) |

### Give every agent a verifiable identity

| Outcome | Feature |
| --- | --- |
| An agent is registered as an OAuth client with a persona that matches how it runs, so the gateway can authenticate, attribute, and audit it. | [Create an agent identity](../build/create-an-agent-identity.md) |
| An unattended workload authenticates with JWKS or a SPIFFE JWT-SVID instead of a shared client secret. | [Create an agent identity](../build/create-an-agent-identity.md#workload-agent) |
| Authorization policies reference the agent itself as a principal. | [Add policies to your MCP server](../build/configure-your-mcp/add-policies-to-mcp-server.md) |
| Users and groups from your enterprise identity provider become principals in your policies. | [Add policies to your MCP server](../build/configure-your-mcp/add-policies-to-mcp-server.md#scim-integration-for-principals) |

### Account for what AI traffic costs

| Outcome | Feature |
| --- | --- |
| Every call records the provider, the model that answered, the tokens in and out, and the cost priced from the model's configured rate. | [Monitor your LLM proxy](../observe/monitor-your-llm-proxy.md) |
| Cost is attributed to the model that actually answered rather than the model the caller asked for. | [Monitor your LLM proxy](../observe/monitor-your-llm-proxy.md#what-the-gateway-records) |
| AI traffic on employee devices that bypasses the governance layer entirely becomes visible. | [Monitor AI Gateway usage from employee systems](../observe/monitor-ai-gateway-from-devices.md) |

<!-- GAP: the two use-case buckets below link to pages that are currently hidden: true / noIndex: true.
     Cut this block in one edit if the page publishes before govern/ and cost-and-value/ are unhidden. -->

### Prove how an agent was overseen

| Outcome | Feature |
| --- | --- |
| Every agent in the catalog is continuously scored against the EU AI Act framework, from declared metadata and from the controls actually installed on its proxy. | [Score agent compliance with the EU AI Act framework](../govern/score-agent-compliance-with-the-eu-ai-act.md) |
| An intended tool call is judged in context and receives a bounded verdict before it executes. | [Guard agent actions with Guardian Agents](../govern/guard-agent-actions-with-guardian-agents.md) |
| A sensitive tool call waits for a human decision, with no client-side integration in the calling agent. | [Require human approval for MCP tool calls](../govern/require-human-approval-for-mcp-tool-calls.md) |
| One record carries the decision chain, the result, and the cost for a single consequential action. | [Audit agent activity logs](../govern/agent-activity-logs.md) |
| Traffic to a single proxy is cut off at the gateway without losing the subscriptions consumers hold. | [Agent kill switch](../build/agent-killswitch.md) |

### Set spend against what it bought

| Outcome | Feature |
| --- | --- |
| Prices live on the catalog items that incur them, and the AI Gateway prices LLM traffic against them as requests flow through. | [Agent FinOps](../cost-and-value/agent-finops.md) |
| The business value an MCP tool delivers is declared by its owner, and each run is classified by whether it achieved its outcome. | [Attribute business value to agent runs](../cost-and-value/attribute-business-value-to-agent-runs.md) |
| A proxy or an agent is evaluated against declared thresholds rather than against an expectation in someone's head. | [Performance targets](../observe/performance-targets.md) |

<!-- END GAP block -->

## Providers and formats

An LLM Proxy accepts inbound requests in the **OpenAI**, **Anthropic Messages**, and **Gemini `generateContent`** formats, and translates them to the native API of the provider you configured.

| Reference | What it covers |
| --- | --- |
| [Accepted request formats](../build/accepted-request-formats.md) | The endpoints and limits for each client format you send requests in. |
| [LLM Proxy provider support](../build/llm-proxy-provider-support.md) | Which OpenAI features each provider supports, how requests map to each native API, and the limits that apply. |

The supported providers are OpenAI, Anthropic, Gemini, Bedrock, and Vertex AI. For the full feature matrix, including finish-reason mapping and embeddings support per provider, see [LLM Proxy provider support](../build/llm-proxy-provider-support.md).

## The Catalog

The Catalog is the authoritative registry of every asset an agent can use. Policy is authored against cataloged entities, which is why it's intentionally rich.

| Entity type | Sources |
| --- | --- |
| **AI Models** | Synced from a connected provider integration, synced from Azure AI Foundry, or registered manually. See [Add an AI model](../import/add-an-ai-model.md). |
| **MCP Servers** | Registered from a Streamable HTTP endpoint, or authored in MCP Studio. Type: **Native** (upstream) or **Composite**. See [Register an MCP server](../import/register-an-mcp-server.md). |
| **Prompts** | Reusable, parameterized templates with declared arguments. See [Import prompts](../import/import-prompts.md). |
| **MCP Resources** | Server resources discovered from registered MCP servers, and repository resources from Git. See [Add MCP resources](../import/add-mcp-resources.md). |
| **Tools** | **MCP Tools** from connected MCP servers, **API Tools** built from REST APIs in API Management, and **Kafka API Tools** from Event Stream Management. See [Create API tools](../import/create-api-tools.md). |
| **Knowledge & Data** | Document sources registered for agent consumption, inline or fetched from a remote URL. See [Add a knowledge source](../import/add-knowledge-source.md). |
| **Skills** | Uploaded as `.zip` skill packages, exposed to agents as MCP resources using the FastMCP Skills-as-Resources pattern. See [Upload skills](../import/upload-skills.md). |
| **Agents** | Registered from the A2A agent card an agent publishes. See [Register an agent](../import/import-an-agent.md). |

For the full set of import operations, see [Import](../import/README.md).

## Scenario recipes

Each recipe connects a real third-party MCP server, curates its tool surface, and then secures it end to end.

* [**Connect and secure the GitHub MCP server**](../build/configure-your-mcp/connect-and-secure-github-mcp-server.md). Hold the personal access token on the gateway instead of copying it into every agent, and authorize each call under the caller's identity.
* [**Connect and secure the Atlassian MCP server**](../build/configure-your-mcp/connect-and-secure-atlassian-mcp-server.md). Reach Jira and Confluence through the gateway, with the API token held once and every call audited per caller.
* [**Connect and secure the Stripe MCP server**](../build/configure-your-mcp/connect-and-secure-stripe-mcp-server.md). Withhold the tool that performs every Stripe write, and permit refunds for one role while denying them for another.

## AI tools and SDKs

* [**Connect Claude Code through an LLM Proxy**](../publish/connect-claude-code-through-an-llm-proxy.md). Govern Claude Code traffic while users keep their own OAuth login, with no shared Anthropic key stored in Gravitee.
* [**Consume your LLM Proxy with LangChain**](../publish/consume-your-llm-proxy-with-langchain.md). Point `ChatOpenAI` at the proxy so the chain never holds a provider credential.
* [**Connect Claude Code to the Edge Daemon**](../../edge-management/connect-claude-code-to-daemon.md). Route LLM traffic through the local daemon for pre-egress policy before it reaches the AI Gateway.

## Observability

| Surface | What it answers |
| --- | --- |
| [**Dashboards**](../observe/dashboards/README.md) | What your AI traffic costs, which models and tools it reaches, and how much of it runs outside the governance layer. |
| [**Logs**](../observe/logs/README.md) | What a single invocation carried and how it was handled. |
| [**Tracing**](../observe/tracing/README.md) | How one request moved through a proxy, as a span timeline or a lineage graph. |
| [**Edge Management**](../observe/monitor-ai-gateway-from-devices.md) | Per-device and per-team AI traffic, shadow AI detection, and fleet health. |

## How Agent Management connects to the platform

Agent Management shares three things with API Management and Event Stream Management:

1. **A common Catalog.** REST APIs from API Management become API Tools, so existing enterprise infrastructure becomes agent-accessible without redevelopment.
2. **A common authorization engine.** [Authorization Management](../../authorization-management/get-started/authorization-management-overview.md) defines fine-grained, catalog-aware policies that the AI Gateway, API Gateway, and Event Gateway all enforce at the wire level.
3. **Common enforcement architecture.** The same policy engine, the Policy Decision Point (PDP), runs inside every gateway. It's evaluated at microsecond latency with no network hop.

A typical enterprise AI request might traverse multiple protocols in a single logical request: an agent invocation arrives at the A2A Proxy, the LLM Proxy handles the model call, the MCP Proxy governs the tool call and reaches a Composite MCP Server, the API Gateway serves the underlying API, and the Event Gateway handles the published event.

You need one place to define policy, one place to see the trace, and one place to attribute cost.

## Frequently asked questions

<details>

<summary>What's the difference between an LLM Proxy, an MCP Proxy, and an A2A Proxy?</summary>

They govern three different protocols. An LLM Proxy routes traffic to upstream model providers. An MCP Proxy sits in front of an upstream MCP server and governs every tool invocation, speaking protocol-native JSON-RPC 2.0. An A2A Proxy exposes an upstream agent so other agents can discover and call it, serving the agent's `/.well-known/agent-card.json` descriptor through the gateway. All three share the same authentication chain, policy chain, and observability chain.

</details>

<details>

<summary>Do I have to change my application code to route through an LLM Proxy?</summary>

No. The LLM Proxy is API-compatible with the Anthropic and OpenAI Messages APIs, so you can route existing AI tool traffic by setting `ANTHROPIC_BASE_URL` or `OPENAI_BASE_URL` to the proxy's context path. See [Create an LLM Proxy](../build/create-an-llm-proxy.md#zero-code-integration).

Note that the OpenAI path carries no `/v1` segment and the Anthropic path does. A request to `<context-path>/v1/chat/completions` returns `404`. See [Publish your LLM Proxy](../publish/publish-your-llm-proxy.md).

</details>

<details>

<summary>Which client API formats does an LLM Proxy accept?</summary>

OpenAI, Anthropic Messages, and Gemini `generateContent`. OpenAI is the proxy's internal format, so OpenAI requests pass through with minimal change; Anthropic and Gemini requests are normalized to OpenAI Chat Completions before the policy chain runs, and the response is converted back to the format the client used. See [Accepted request formats](../build/accepted-request-formats.md).

</details>

<details>

<summary>What's the difference between Proxy mode and Studio mode on an MCP Proxy?</summary>

Proxy mode is a transparent intermediary in front of an existing upstream MCP server, adding governance without changing the server. Studio mode is an authoring environment that assembles tools, resources, prompts, and skills from the Catalog into a **Composite MCP Server** that didn't exist as a single unit upstream. Studio is a mode of the MCP Proxy, not a separate product. See [Create an MCP Studio](../build/create-an-mcp-studio.md).

</details>

<details>

<summary>Where are authorization policies written, and where are they enforced?</summary>

Policies are authored in Authorization Management using the Gravitee Authorization Policy Language (GAPL), a subset of the Cedar policy language, and enforced at the wire level by the AI Gateway with no network hop. A call with no matching permit is denied, and `forbid` beats `permit`. After you deploy a policy to the PDP, the AI Gateway syncs it within 30 seconds with no restart. See [Add policies to your MCP server](../build/configure-your-mcp/add-policies-to-mcp-server.md).

</details>

<details>

<summary>Does the Catalog store the credentials for my upstream MCP servers?</summary>

No. The credentials you supply when registering an MCP server are used strictly to discover and catalog the server's capabilities, and secrets are never persisted. When you create an MCP Proxy in front of that server, you configure upstream authentication separately for runtime invocations. See [Register an MCP server](../import/register-an-mcp-server.md).

</details>

<details>

<summary>Do the guardrail and PII models run on the gateway?</summary>

Yes. The classification and ONNX embedding models run locally on the AI Gateway using the ONNX Runtime. Models aren't bundled with the plugin: on first use the resource downloads the model into `$GRAVITEE_HOME/models`, the first request after a gateway start is slower, and a loaded model is shared across every proxy that selects it.

The ONNX Runtime doesn't run on Alpine Linux, which the default Gravitee Docker images are based on. Use the Debian-based gateway image, `graviteeio/apim-gateway:<version>-debian`. See [AI resources](../build/ai-resources.md).

</details>

<details>

<summary>Why is cost missing for some of my LLM traffic?</summary>

Cost is computed by the gateway, not reported by the provider, and it needs both an input price and an output price set on the model. An absent price means *unknown* and no cost is recorded; a price of `0` is valid and means free. The gateway can also only price a model that is declared on the LLM Proxy endpoint, so a runtime model override to an undeclared model is proxied but not priced. See [Monitor your LLM proxy](../observe/monitor-your-llm-proxy.md#troubleshooting).

</details>

## Guides

* [Get started](../get-started/README.md). The overview, the roles reference, and the MCP and LLM quickstarts.
* [Import](../import/README.md). Populate the Catalog with models, MCP servers, tools, prompts, resources, skills, and agents.
* [Build](../build/README.md). Create and configure the proxies and the agent identities.
* [Observe](../observe/README.md). Monitor AI traffic across proxy types and from employee devices.
