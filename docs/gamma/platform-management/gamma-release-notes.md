# Gravitee Gamma Release

Released June 26, 2026

## Highlights

- **Agent Management** — Unified AI Gateway governing LLM, MCP, and A2A protocols with cost attribution, PII filtering, and end-to-end OpenTelemetry tracing across every agent hop.
- **API Management** — Create and govern REST, GraphQL, and gRPC API proxies with security plans, policy enforcement, and observability — and bridge existing APIs as AI tools in Agent Management.
- **Authorization Management** — Fine-grained, catalog-aware access control via GAPL policies enforced at microsecond latency inline in every gateway, across all Gamma traffic types.
- **Edge Management** — Lightweight device daemon that detects shadow AI usage and enforces pre-egress policies before AI traffic leaves employee devices.
- **Event Stream Management** — Register and govern Kafka clusters with virtual clusters for multi-tenant isolation, and bridge event streams as Kafka API tools in Agent Management.
- **Platform Management** — Shared platform foundations covering application management, reusable resources, Access Management integration, and OpenAPI viewer configuration.

## New features

### Agent Management

#### AI Gateway

- Provides a unified runtime for LLM, MCP, and A2A traffic — all three proxy types share a common authentication chain, policy chain, observability chain, and Authorization Management integration point.
- **LLM Proxy** — Routes model traffic to Anthropic, OpenAI, Bedrock, Vertex AI, and Azure with routing strategies (cost, latency, random), guardrails, PII filtering, token-based rate limiting, and structured output enforcement.
- **MCP Proxy** — Governs tool invocations on upstream MCP servers (HubSpot, GitHub, Salesforce, Jira) with authentication, fine-grained policies, and protocol-native JSON-RPC 2.0. Supports both transparent proxy mode and Studio mode.
- **MCP Studio** — Compose tools, resources, prompts, and skills from multiple sources into a Composite MCP Server without writing code.
- **A2A Proxy** — Secures agent-to-agent delegations with skill discovery via `/.well-known/agent.json`, per-skill authorization, and agent identity verification across trust boundaries.

#### Catalog

- Authoritative registry of AI models, MCP servers, tools, prompts, agents, skills, and resources that policies are authored against.
- Syncs AI models from AWS Bedrock, Azure AI Foundry, and Vertex AI, or accepts manual registration.
- Consumes from external MCP registries (GitHub, Smithery, and third-party) and operates as an MCP Registry itself, so other systems can discover and read from it.
- REST, GraphQL, and gRPC APIs from API Management become **API Tools**; Kafka topics from Event Stream Management become **Kafka API Tools** — making existing enterprise infrastructure agent-accessible without redevelopment.

#### Agent Identity

- Registers agents as OAuth clients in Gravitee Access Management so gateways and authorization policies can authenticate, attribute, and audit every agent.
- Three personas: **User-embedded** (public PKCE client), **Hosted delegated** (confidential web client), and **Autonomous** (service client with `client_credentials` or token exchange).
- Supports CIMD (Client ID Metadata Documents) and SPIFFE as credential options within the registration wizard.

#### Observability

- End-to-end OpenTelemetry tracing across every agent hop: agent → tool, agent → LLM, agent → agent.
- Every span carries agent identity, tool name, inputs, outputs, latency, policy decision, cost, and timestamp.
- A lineage view stitches spans into a navigable trace of the full request graph.

### API Management

#### API Proxy Creation

- Define an API proxy with a context path, upstream target URL, and security plan via a step-by-step wizard or template-based flow.
- Templates preconfigure common patterns, reducing setup time for standard API topologies.

#### Security Plans

- Attach one or more plans to control who can call an API and how they authenticate.
- Supported plan types: Keyless, API Key, JWT, OAuth2, and mTLS.

#### Policy Enforcement

- Apply fine-grained policies at the request and response level: rate limiting, content transformation, and authorization checks powered by Authorization Management.
- Shared policy groups allow reusable policy sets to be applied across multiple API proxies.

#### Consumer Access

- Manage consumer applications, subscriptions, and API keys through controlled channels.
- API Products bundle proxies into a consumer-facing offering with its own subscription lifecycle.

#### Observability

- Monitor request volume, latency, error rates, and audit history for every deployed API via per-API dashboards and log search.
- Endpoint health monitoring surfaces backend availability without leaving the console.

### Authorization Management

#### GAPL Policy Language

- Policies are written in GAPL (Gravitee Authorization Policy Language), a Cedar-syntax subset optimized for the Gamma visual editor.
- Each policy declares an effect (`permit` or `forbid`), a principal, an action, a resource, and optional `when` conditions.
- Condition support includes time-of-day restrictions, IP range checks, token budgets, cost ceilings, scope checks, PII filter flags, and tenant attribute matching.

#### Policy Categories

- **MCP Policies** — Access to MCP servers, tools, prompts, and resources.
- **AI Model Policies** — Access to AI providers and specific models, with cost and token usage constraints.
- **API Policies** — Access to API proxies, endpoints, and data fields.
- **Custom Policies** — Policies for resources not routed as MCP, API, Agent, LLM, or Event — internal applications, data assets, and bespoke resources.

#### Inline Enforcement

- The Policy Decision Point (PDP) runs inside the AI Gateway, API Gateway, and Event Gateway at microsecond latency with no network hop.
- Principals can be synced from identity providers via SCIM or from Gravitee Access Management, with live sync progress surfaced via toast notifications.

#### Pre-built Condition Snippets

- Each policy category ships with reusable condition snippets for common scenarios: business hours, trusted device, corporate IP range, token budget, cost ceiling, rate limit, and tenant match.

### Edge Management

#### Shadow AI Detection

- Continuously scans device network connections to detect any process communicating with a known AI provider, regardless of whether traffic is routed through the Edge Daemon.
- Surfaces unmanaged AI usage across the device fleet with no per-tool configuration required.

#### Active Traffic Routing

- **Interception mode (default)** — Transparent local DNS resolver redirects configured AI provider domains to the daemon, which terminates TLS locally and forwards to the AI Gateway. No per-tool configuration needed; automatically handles Node.js tools (Claude Code, Cursor) via `NODE_EXTRA_CA_CERTS`.
- **Proxy mode** — Tools can be pointed at the Edge Daemon explicitly via provider base URL environment variables for direct routing.

#### Local Pre-Egress Policy Enforcement

- Blocks sensitive data before it leaves the device: secrets, classified content, large prompt payloads, and disallowed models.
- Policies are evaluated locally so enforcement is not dependent on network connectivity to the gateway.

#### MDM Deployment

- Distributed via Kandji (Jamf and Intune planned) with automatic OS and Node.js trust store setup — no manual certificate steps required.

### Event Stream Management

#### Kafka Cluster Registration

- Import existing Kafka clusters into Gamma so they can be governed, monitored, and composed into higher-level services.
- Registered clusters are available as the backing infrastructure for Kafka Services and Virtual Clusters.

#### Kafka Service Creation

- Define a governed Kafka Service with security plans, policies, and access controls backed by either a Registered Cluster or a Virtual Cluster.
- Analogous to an API proxy in API Management — the same plan types and policy model apply to event streams.

#### Virtual Clusters

- Provision logically isolated Kafka environments on shared infrastructure for multi-tenant workloads (Kafka Mesh).
- Prevents cross-tenant data access while allowing shared underlying broker infrastructure.

#### AI Bridging

- Kafka APIs and event streams can be exposed as **Kafka API Tools** in Agent Management, making existing event infrastructure accessible to AI agents without redevelopment.

### Platform Management

#### Application Management

- Manage consumer applications and their subscriptions to APIs, event streams, and agent services from a single location.

#### Shared Resources

- Define reusable components — OAuth2 token validation endpoints, cache stores, and authentication providers — that API proxies reference at runtime.

#### Access Management Integration

- Configure the connection to Gravitee Access Management, select an environment and domain, and verify OAuth capabilities required by agent identities and security plans.

#### OpenAPI Viewer Configuration

- Configure the OpenAPI viewer globally across both the management console and Portal Next for a consistent API documentation experience.

