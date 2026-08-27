---
hidden: false
noIndex: false
description: Agent Management governs LLM, MCP, and agent-to-agent traffic from one control plane. Learn what it provides and how it fits the Gamma platform.
---

# Agent Management overview

Agent Management is Gravitee's product line for governing AI agent traffic. It provides a unified Control Plane and runtime for every protocol in the agentic stack: LLM calls, MCP tool invocations, and agent-to-agent (A2A) delegations. It adds end-to-end observability, fine-grained authorization, and identity for every agent that touches your enterprise infrastructure.

## Why Agent Management exists

Enterprise AI adoption introduces the following classes of traffic that existing API gateways and identity systems weren't designed for:

* **LLM traffic.** Engineering teams use Claude Code, Cursor, and ChatGPT Enterprise with no central visibility into cost, model usage, or data exposure.
* **MCP traffic.** Agents call tools on upstream MCP servers such as HubSpot, GitHub, Salesforce, and Jira using shared API keys or unaudited credentials.
* **A2A traffic.** Multi-agent systems delegate work across trust boundaries with no authorization, lineage, or cost attribution per delegation.

Agent Management extends the gateway infrastructure that already governs API and event traffic to cover these three protocol types, using the same Catalog, the same authorization engine, and the same enforcement architecture.

## Core components

### AI Gateway

The AI Gateway is the unified runtime that processes LLM, MCP, and A2A traffic. It consists of three proxies that share an authentication chain, a policy chain, an observability chain, and an Authorization Management integration point:

| Proxy         | What it governs                                                         | Key capabilities                                                                                                                                                                                 |
| ------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **LLM Proxy** | Traffic to LLM providers (OpenAI, Anthropic, Gemini, Bedrock, Vertex AI) | Guardrails, PII filtering, token-based rate limiting, structured output |
| **MCP Proxy** | Tool invocations on upstream MCP servers                                | Two modes: **Proxy mode** (transparent governance) and **Studio mode** (composition of Composite MCP Servers). Protocol-native JSON-RPC 2.0, OAuth authorization discovery, credential mediation |
| **A2A Proxy** | Agent-to-agent delegations                                              | Skill discovery via `/.well-known/agent-card.json`, per-skill authorization, agent identity verification                                                                                              |

### Catalog

The Catalog is the authoritative registry of every asset an agent can use. Policy is authored against cataloged entities, which is why it's intentionally rich. It holds the following entity types:

| Entity type          | Sources                                                                                                                                                                     |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI Models**        | Synced from a built-in provider template (OpenAI, Anthropic, Google Gemini, Mistral AI, DeepSeek, Groq, xAI, Together AI, Fireworks AI), synced from Azure AI Foundry, or registered manually |
| **MCP Servers**      | Gravitee MCP Server Registry, third-party registries (GitHub, Smithery), or manual. Type: **Native** (upstream) or **Composite** (authored in MCP Studio)                    |
| **Prompts**          | Reusable, parameterized templates with declared arguments, discovered from connected MCP servers                                                                             |
| **MCP Resources**    | Auto-discovered from registered MCP servers: the files, databases, and APIs each server exposes                                                                              |
| **Tools**            | **MCP Tools** from connected MCP servers, **API Tools** built from REST APIs in API Management, and **Workflow Tools** composed from a sequence of operations                |
| **Knowledge & Data** | Document sources registered for grounding, such as repository bundles and file collections                                                                                  |
| **Skills**           | Uploaded as `.zip` skill packages, exposed to agents as MCP resources using the FastMCP Skills-as-Resources pattern                                                          |
| **Agents**           | A2A agents, hyperscaler-federated agents, Studio-authored agents                                                                                                             |

The Catalog participates bidirectionally in the MCP ecosystem: it **consumes** from external MCP Registries and **operates** as an MCP Registry that other systems can discover and read from.

### Agent Identity

Agent Identity registers agents as OAuth clients in Gravitee Access Management so the AI Gateway and authorization policies can authenticate, attribute, and audit every agent that touches your infrastructure.

Every agent is registered as one of three **personas**, each determining the underlying OAuth client type:

| Persona                        | OAuth client                                            | Use it for                                                 |
| ------------------------------ | ------------------------------------------------------- | ---------------------------------------------------------- |
| **Desktop Productivity Agent** | Native, public client (PKCE enforced)                   | An agent that runs on the user's device                    |
| **Hosted Agent**               | Web, confidential client                                | An agent that runs on your server, acting per user session |
| **Workload Agent**             | Service client (`client_credentials` or token exchange) | An unattended service worker with no interactive user      |

Identity standards such as **Client ID Metadata Documents (CIMD)** and **SPIFFE** are available as credential options within the registration wizard. They're orthogonal to the persona choice, not determined by it. See [Create an agent identity](../build/create-an-agent-identity.md) for the full wizard walkthrough.

### Edge Management

Edge Management provides visibility and control over AI traffic on employee devices. A lightweight agent, the **Edge Daemon**, is installed using an MDM tool such as Kandji, Jamf, or Intune. It observes outgoing connections to AI providers, reports shadow AI usage, and enforces local policies before traffic leaves the device.

### Observability

End-to-end observability across every hop: agent to tool, agent to LLM, and agent to agent. Every interaction emits an OpenTelemetry span with agent identity, tool name, inputs, outputs, latency, policy decision, cost, and timestamp. The lineage view stitches spans into a navigable trace of the full request graph.

## How Agent Management connects to the platform

Agent Management shares three things with API Management and Event Stream Management:

1. **A common Catalog.** REST APIs from API Management become API Tools, so existing enterprise infrastructure becomes agent-accessible without redevelopment.
2. **A common authorization engine.** Authorization Management defines fine-grained, catalog-aware policies that the AI Gateway, API Gateway, and Event Gateway all enforce at the wire level.
3. **Common enforcement architecture.** The same policy engine, the Policy Decision Point (PDP), runs inside every gateway. It's evaluated at microsecond latency with no network hop.

A typical enterprise AI request might traverse multiple protocols in a single logical request:

1. An agent invocation arrives at the A2A Proxy.
2. The LLM Proxy handles the model call.
3. The MCP Proxy governs the tool call and reaches a Composite MCP Server, which calls its upstream MCP servers.
4. The API Gateway serves the underlying API.
5. The Event Gateway handles the published event.

You need one place to define policy, one place to see the trace, and one place to attribute cost. That's the AI Gateway backed by the Catalog and Authorization Management.

## Next steps

* [Create your first MCP server](../get-started/create-your-first-mcp-server.md). Configure an MCP proxy in front of an upstream MCP server, and then verify tool invocations.
* [Create your LLM Proxy](../get-started/create-your-llm-proxy.md). Configure an LLM Proxy, connect it to an upstream model provider, and then send a test prompt.
