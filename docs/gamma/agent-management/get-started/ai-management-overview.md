---
hidden: false
noIndex: false
---

# Agent Management overview
<!-- GAP-STRUCTURAL: Missing procedural content source -->
<!-- GAP: 43 · Investigable · Add a platform architecture diagram showing the AI Gateway, Catalog, Agent Identity, and Edge Management components. Needs: Visual asset -->

Agent Management (AM) is Gravitee's product line for governing AI agent traffic. It provides a unified control plane and runtime for every protocol in the agentic stack — LLM calls, MCP tool invocations, and agent-to-agent (A2A) delegations — with end-to-end observability, fine-grained authorization, and identity for every agent that touches your enterprise infrastructure.

## Why Agent Management exists

Enterprise AI adoption introduces a new class of traffic that existing API gateways and identity systems weren't designed for:

* **LLM traffic** — Engineering teams use Claude Code, Cursor, and ChatGPT Enterprise with no central visibility into cost, model usage, or data exposure.
* **MCP traffic** — Agents call tools on upstream MCP servers (HubSpot, GitHub, Salesforce, Jira) using shared API keys or unaudited credentials.
* **A2A traffic** — Multi-agent systems delegate work across trust boundaries with no authorization, lineage, or cost attribution per delegation.

Agent Management extends the gateway infrastructure that already governs API and event traffic to cover these three protocol types — using the same Catalog, the same authorization engine, and the same enforcement architecture.

## Core components

### AI Gateway

The AI Gateway is the unified runtime that processes LLM, MCP, and A2A traffic. It consists of three proxies that share an authentication chain, a policy chain, an observability chain, and an Authorization Management integration point:

| Proxy         | What it governs                                                         | Key capabilities                                                                                                                                                                                 |
| ------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **LLM Proxy** | Traffic to LLM providers (Anthropic, OpenAI, Bedrock, Vertex AI, Azure) | Routing strategies (`COST`, `LATENCY`, `RANDOM`), guardrails, PII filtering, token-based rate limiting, structured output |
| **MCP Proxy** | Tool invocations on upstream MCP servers                                | Two modes: **Proxy mode** (transparent governance) and **Studio mode** (composition of Composite MCP Servers). Protocol-native JSON-RPC 2.0, OAuth authorization discovery, credential mediation |
| **A2A Proxy** | Agent-to-agent delegations                                              | Skill discovery via `/.well-known/agent.json`, per-skill authorization, agent identity verification                                                                                              |

### Catalog

The Catalog is the authoritative registry of every asset an agent can use. Policy is authored against cataloged entities — which is why the Catalog is intentionally rich.

| Entity type     | Sources                                                                                                                                                   |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI Models**   | Synced from AWS Bedrock, Azure AI Foundry, Vertex AI, or registered manually                                                                              |
| **MCP Servers** | Gravitee MCP Server Registry, third-party registries (GitHub, Smithery), or manual. Type: **Native** (upstream) or **Composite** (authored in MCP Studio) |
| **Tools**       | **MCP Tools** from connected MCP servers, **API Tools** from REST APIs in API Management, **Kafka API Tools** from Kafka APIs in Event Stream Management         |
| **Prompts**     | Uploaded as reusable, parameterized templates with declared arguments                                                                                     |
| **Resources**   | **Server Resources** from MCP servers, or **Repository Resources** (markdown, JSON, structured docs) from Git                                             |
| **Skills**      | Skill folders cataloged from external sources, exposed as MCP Resources via FastMCP                                                                       |
| **Agents**      | A2A agents, hyperscaler-federated agents, Studio-authored agents                                                                                          |

The Catalog participates bidirectionally in the MCP ecosystem: it **consumes** from external MCP Registries and **operates** as an MCP Registry that other systems can discover and read from.

### Agent Identity

Agent Identity registers agents as OAuth clients in Gravitee Access Management (AM) so the AI Gateway and authorization policies can authenticate, attribute, and audit every agent that touches your infrastructure.

Every agent is registered as one of three **personas**, each determining the underlying OAuth client type:

| Persona              | OAuth client                                            | Use it for                                                 |
| -------------------- | ------------------------------------------------------- | ---------------------------------------------------------- |
| **User-embedded**    | Native, public client (PKCE enforced)                   | An agent that runs on the user's device                    |
| **Hosted delegated** | Web, confidential client                                | An agent that runs on your server, acting per user session |
| **Autonomous**       | Service client (`client_credentials` or token exchange) | An unattended service worker with no interactive user      |

Identity standards such as **CIMD** (Client ID Metadata Documents) and **SPIFFE** are available as credential options within the registration wizard — they are orthogonal to the persona choice, not determined by it. See [Create an agent identity](../build/create-an-agent-identity.md) for the full wizard walkthrough.

### Edge Management

Edge Management provides visibility and control over AI traffic on employee devices. A lightweight agent (**Edge Daemon**) installed via MDM (Kandji, Jamf, Intune) observes outgoing connections to AI providers, reports shadow AI usage, and enforces local policies before traffic leaves the device.

### Observability

End-to-end observability across every hop: agent → tool, agent → LLM, agent → agent. Every interaction emits an OpenTelemetry span with agent identity, tool name, inputs, outputs, latency, policy decision, cost, and timestamp. The lineage view stitches spans into a navigable trace of the full request graph.

## How Agent Management connects to the platform

Agent Management shares three things with API Management and Event Stream Management:

1. **A common Catalog** — APIs from APIM become API Tools; Kafka topics from Event Stream Management become Kafka API Tools. Existing enterprise infrastructure becomes agent-accessible without redevelopment.
2. **A common authorization engine** — Authorization Management defines fine-grained, catalog-aware policies that the AI Gateway, API Gateway, and Event Gateway all enforce at the wire level.
3. **Common enforcement architecture** — The same policy engine (PDP) runs inside every gateway, evaluated at microsecond latency with no network hop.

A typical enterprise AI request might traverse multiple protocols in a single logical request:

```
Agent invocation → A2A Proxy → LLM Proxy (model call) → MCP Proxy (tool call)
→ Composite MCP Server → upstream MCP servers → API Gateway (underlying API)
→ Event Gateway (published event)
```

The customer needs one place to define policy, one place to see the trace, and one place to attribute cost — that's the AI Gateway backed by the Catalog and Authorization Management.

## Get started

* [Create your first MCP server](create-your-first-mcp-server.md) — Set up an MCP proxy in front of an upstream MCP server and verify tool invocations
* [Create your LLM Proxy](create-your-llm-proxy.md) — Configure an LLM Proxy, connect to an upstream model provider, and send a test prompt
