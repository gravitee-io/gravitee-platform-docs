---
description: What the Gamma 4.13 release adds across API Management, Event Stream Management, and the other modules. Browse the new features and changes.
---

# Gamma Release Notes

## 4.13 new features

The 4.13 release adds the following capabilities.

### Agent Management

Agent Management adds a configuration audit trail, event notifications, and API resource configuration to each proxy detail view. It also brings deployment configuration and deployment history to LLM, MCP, and A2A Proxies, and lets you record the price you negotiated with a provider on a cataloged AI model.

#### API Resources for LLM, MCP, and A2A Proxies

* Each LLM Proxy, MCP Proxy, and A2A Proxy detail view adds a **Resources** page that manages the resources the proxy's policies reference by name at runtime, such as caches, OAuth providers, and guardrail detectors.
* Add a resource by selecting one of the resource plugins installed on your platform and completing its schema-generated configuration form. Edit, enable or disable, remove, and search existing resources from the same page.
* A resource change applies to the gateway when you deploy the proxy from the out-of-sync banner.
* See [Configure resources for your proxies](../agent-management/build/configure-resources-for-your-proxies.md).

#### Audit Logs for LLM, MCP, and A2A Proxies

* Each LLM Proxy, MCP Proxy, and A2A Proxy detail view adds an **Audit Logs** page under **Monitoring** that lists the audit events recorded for the proxy.
* Each entry shows the date, the actor, the event type, and the target of the change. Entries that carry a JSON Patch open the exact change in a side panel.
* Filter the trail by event type and date range, and page through entries 10, 25, 50, or 100 at a time.
* See [Review audit logs](../agent-management/observe/review-audit-logs.md).

#### Notifications for LLM, MCP, and A2A Proxies

* Each LLM Proxy, MCP Proxy, and A2A Proxy detail view adds a **Notifications** page that pairs a notifier with the set of API events that trigger it. The table lists each notification's **Name**, **Notifier**, **Subscribed events**, and **Groups**.
* Every proxy starts with a **Portal notification**. Add further notifications on any notifier configured for your organization, such as **Default Email Notifier** or a webhook notifier, and address them to an email list or a webhook URL. Target fields support Expression Language, and webhook notifications can route through the gateway's system proxy.
* Subscribe each notification to the API events that matter, grouped by category such as **API KEY** and **SUBSCRIPTION**, and optionally scope it to selected groups. Leaving groups empty applies the notification to all groups.
* Creating, editing, and deleting notifications is gated by the `api-notification-c`, `api-notification-u`, and `api-notification-d` permissions. The **Portal notification** can be edited but not deleted, and the channel of an existing notification can't be changed.
* See [Configure LLM Proxy notifications](../agent-management/build/configure-llm-proxy-notifications.md), [Configure MCP Proxy notifications](../agent-management/build/configure-mcp-proxy-notifications.md), and [Configure A2A Proxy notifications](../agent-management/build/configure-a2a-proxy-notifications.md).
#### Deployment configuration for LLM, MCP, and A2A Proxies

* Each LLM Proxy, MCP Proxy, and A2A Proxy detail view adds a **Deployment** section under **Operations**, with a **Configuration** page that controls where the proxy is deployed on the gateway mesh.
* Assign the sharding tags defined for your organization from the **Sharding tags** card. Only gateway instances advertising a matching tag load the proxy's API definition. Each selected tag appears as a chip, and an assigned tag that no longer exists at the organization level is preserved on save.
* Changing tags requires the **API\_DEFINITION** permission with the **UPDATE** access level. Proxies managed by the Gravitee Kubernetes Operator (GKO) are read-only here, and their tags are changed from the source definition.
* See [Configure LLM Proxy deployment](../agent-management/build/configure-llm-proxy-deployment.md), [Configure MCP Proxy deployment](../agent-management/build/configure-mcp-proxy-deployment.md), and [Configure A2A Proxy deployment](../agent-management/build/configure-a2a-proxy-deployment.md).

#### Deployment history for LLM, MCP, and A2A Proxies

* The **Deployment** section adds a **History** page that lists every deployment of the proxy, newest first, with the **Version**, **Date**, **User**, and **Label** of each and a **live** badge on the most recent. Page through entries 10, 25, 50, or 100 at a time.
* Inspect the API definition a deployment shipped with **View definition**, or compare two versions in a **Side-by-side** or **Line-by-line** diff. **Compare with live** opens an earlier version against the live one in a single step.
* Roll back to an earlier version from the diff view. The rollback restores the proxy's API definition and its plans, and leaves the proxy with undeployed changes until you deploy it. Rollback requires the **API\_DEFINITION** permission with the **UPDATE** access level.
* See [Review LLM Proxy deployment history](../agent-management/build/review-llm-proxy-deployment-history.md), [Review MCP Proxy deployment history](../agent-management/build/review-mcp-proxy-deployment-history.md), and [Review A2A Proxy deployment history](../agent-management/build/review-a2a-proxy-deployment-history.md).

#### Negotiated pricing for AI models

* Record the price you negotiated with the provider on a cataloged model, in the **Input price ({currency} per 1M tokens)** and **Output price ({currency} per 1M tokens)** fields of the model edit form. The negotiated price replaces the suggested price wherever the price is shown and wherever cost is computed.
* Set both prices, or clear both, and enter a price of `0` or more. Entering `0` in both fields is valid, because a free model is still a priced model. `{currency}` is the currency of the suggested price and defaults to `USD` when the provider doesn't suggest one.
* A model with a negotiated price shows a `Custom` badge next to its price, together with the suggested rate and the date and author of the last change. The negotiated price appears in the **Price / 1M** column of the AI Models list, on the model detail page, and on the models page of an LLM Proxy, and it feeds the cost estimates in the AI workspace detail view.
* Refreshing the catalog updates the provider-derived fields and keeps your negotiated price. Republish any LLM Proxy that consumes a repriced model so cost tracking picks up the negotiated rate.
* See [Add an AI model](../agent-management/import/add-an-ai-model.md).

### API Management

API Management gains a file-based path for building and updating API proxies and a redesigned out-of-sync banner in the API detail workspace.

#### Import an API proxy

* Create an API proxy from a Gravitee v4 API definition, an OpenAPI specification, or a WSDL document. The three formats are available from the **Import API** card on the **Create API Proxy** page.
* Replace the configuration of an existing API proxy from the same three formats, using **Import** on the **General** page of the API proxy.
* Supply each format as a local file or as a remote `http` or `https` URL that the Management API fetches server-side.
* For OpenAPI and WSDL imports, choose whether to create a documentation page from the specification and whether to add an OpenAPI Specification Validation policy. WSDL imports also offer the REST to SOAP Transformer policy.
* See [Import an API proxy](../api-management/build/import-an-api-proxy.md).

#### Out-of-sync banner in the API detail workspace

* The **This API is out of sync** banner replaces the **This API has undeployed changes.** banner in the API detail workspace.
* The new banner carries an explanation: **Your latest changes are not live yet. Deploy to push them to the gateway.**
* The **Deploy API** button on the banner and the **Out of sync** state badge in the sidebar header are unchanged.
* See [Configure your API proxy](../api-management/build/configure-your-api-proxy/README.md).

### Event Stream Management

Event Stream Management adds a duplication path for Kafka Services.

#### Duplicate a Kafka service

* Create a copy of an existing Kafka Service with **Duplicate** on the service's **General** page. The copy reuses the source service's listener and endpoint configuration.
* Provide a name, a version, and a new listener host prefix for the copy. The host prefix is unique per environment, and the source service's prefix counts as already in use.
* The new service is created in a stopped state and without plans, so you control when it starts accepting connections.
* See [Duplicate a Kafka service](../event-stream-management/build/duplicate-a-kafka-service.md).

### Platform Management

Platform Management adds environment-scoped dictionaries as a reusable asset for API policies, gateway routing configuration for the organization, and organization-wide user administration. It also adds a view of the gateway instances running behind an environment, and an audit trail of configuration changes at both organization and environment scope.

#### Manage dictionaries

* Create, edit, search, and delete the dictionaries of the selected environment from the **Dictionaries** page. Dictionaries hold key-value properties that API policies reference at runtime.
* Manual dictionaries hold properties that you maintain by hand and publish to the gateways with the **Deploy** action.
* Dynamic dictionaries poll an HTTP provider at a configured interval, transform the response with a JOLT specification, and publish the refreshed properties automatically while started.
* See [Manage dictionaries](manage-dictionaries.md).

#### Manage entrypoints and sharding tags

* Configure sharding tags, entrypoint mappings, and each environment's default entrypoint values from the **Entrypoints & Sharding Tags** page.
* Sharding tags route APIs to specific gateway groups. Create a tag with an immutable key, restrict it to selected groups, and add the key to the gateway's configuration file.
* Entrypoint mappings define the entrypoint that the Developer Portal displays for APIs that carry a given tag, as an HTTP URL, a TCP port, or a Kafka bootstrap domain pattern, and apply to all environments or to a selection.
* See [Manage entrypoints and sharding tags](manage-entrypoints-and-sharding-tags.md).

#### Manage users

* Add, review, and delete the users and service accounts of the organization from the **Users** page, and search the list by name, email, or ID.
* Grant organization roles and per-environment roles from the user's detail page, and manage the group memberships that carry the user's API, API Product, application, and integration roles in each environment.
* Accept or reject a pending registration, convert a user to a service account, and send an Active user a password reset email that opens the reset page of the Gamma console.
* Generate and revoke personal access tokens for a user, and review the APIs, API Products, and applications the user is a member of.
* See [Manage users](manage-users.md).

#### Monitor gateway instances

* Review the gateway instances registered with the selected environment from the **Gateways** page, with each instance's version, status, last heartbeat, address, tenant, and sharding tags.
* Open an instance to read what it reported about itself on the **Environment** tab: its information rows, the plugins it loaded, and its JVM system properties.
* Follow the instance's live resource use on the **Monitoring** tab, which refreshes every 5 seconds and reports CPU, heap, memory pools, uptime, file descriptors, threads, and garbage collection.
* See [Monitor gateway instances](monitor-gateway-instances.md).

#### Review organization and environment audit logs

* Trace who changed what, and when, from two **Audit** pages: one in the **Organization** section covering the whole organization, and one in the **Environment** section covering the selected environment.
* Narrow the trail by event type, by the kind of object that changed, by a single environment, application, or API, and by a relative or custom date range.
* Open an event to read its **JSON Patch**, which names each field the change touched and excludes the object's own timestamps.
* Export the filtered trail as CSV or JSON for a compliance archive, up to 10,000 events per export.
* See [Review organization and environment audit logs](review-audit-logs.md).

## Release Date: June 26, 2026

## Highlights

* **Agent Management**: Unified AI Gateway governing LLM, MCP, and A2A protocols with cost attribution, PII filtering, and end-to-end OpenTelemetry tracing across every agent hop.
* **API Management**: Create and govern REST, GraphQL, and gRPC API proxies with security plans, policy enforcement, and observability. Bridge existing APIs as AI tools in Agent Management.
* **Authorization Management**: Fine-grained, catalog-aware access control via GAPL policies enforced at microsecond latency inline in every gateway, across all Gamma traffic types.
* **Edge Management**: Lightweight device daemon that detects shadow AI usage and enforces pre-egress policies before AI traffic leaves employee devices.
* **Event Stream Management**: Register and govern Kafka clusters with virtual clusters for multi-tenant isolation, and bridge event streams as Kafka API tools in Agent Management.
* **Platform Management**: Shared platform foundations covering application management, reusable resources, Access Management integration, and OpenAPI viewer configuration.

## New features

### Agent Management

#### AI Gateway

* Provides a unified runtime for LLM, MCP, and A2A traffic. All three proxy types share a common authentication chain, policy chain, observability chain, and Authorization Management integration point.
* **LLM Proxy**: Routes model traffic to Anthropic, OpenAI, Bedrock, Gemini Enterprise Agent Platform (formerly Vertex AI), and Azure with guardrails, PII filtering, token-based rate limiting, and structured output enforcement.
* **MCP Proxy**: Governs tool invocations on upstream MCP servers (HubSpot, GitHub, Salesforce, Jira) with authentication, fine-grained policies, and protocol-native JSON-RPC 2.0. Supports both transparent proxy mode and Studio mode.
* **MCP Studio**: Compose tools, resources, prompts, and skills from multiple sources into a Composite MCP Server without writing code.
* **A2A Proxy**: Secures agent-to-agent delegations with skill discovery via `/.well-known/agent.json`, per-skill authorization, and agent identity verification across trust boundaries.

#### Catalog

* Authoritative registry of AI models, MCP servers, tools, prompts, agents, skills, and resources that policies are authored against.
* Syncs AI models from AWS Bedrock, Azure AI Foundry, and Gemini Enterprise Agent Platform (formerly Vertex AI), or accepts manual registration.
* Consumes from external MCP registries (GitHub, Smithery, and third-party) and operates as an MCP Registry itself, so other systems can discover and read from it.
* REST, GraphQL, and gRPC APIs from API Management become **API Tools**, and Kafka topics from Event Stream Management become **Kafka API Tools**, making existing enterprise infrastructure agent-accessible without redevelopment.

#### Agent Identity

* Registers agents as OAuth clients in Gravitee Access Management so gateways and authorization policies can authenticate, attribute, and audit every agent.
* Three personas: **Desktop Productivity Agent** (public PKCE client), **Hosted Agent** (confidential web client), and **Workload Agent** (service client with `client_credentials` or token exchange).
* Supports CIMD (Client ID Metadata Documents) and SPIFFE as credential options within the registration wizard.

#### Observability

* End-to-end OpenTelemetry tracing across every agent hop: agent to tool, agent to LLM, and agent to agent.
* Every span carries agent identity, tool name, inputs, outputs, latency, policy decision, cost, and timestamp.
* A lineage view stitches spans into a navigable trace of the full request graph.

### API Management

#### API Proxy Creation

* Define an API proxy with a context path, upstream target URL, and security plan via a step-by-step wizard or template-based flow.
* Templates preconfigure common patterns, reducing setup time for standard API topologies.

#### Security Plans

* Attach one or more plans to control who can call an API and how they authenticate.
* Supported plan types: Keyless, API Key, JWT, OAuth2, and mTLS.

#### Policy Enforcement

* Apply fine-grained policies at the request and response level: rate limiting, content transformation, and authorization checks powered by Authorization Management.
* Shared policy groups allow reusable policy sets to be applied across multiple API proxies.

#### Consumer Access

* Manage consumer applications, subscriptions, and API keys through controlled channels.
* API Products bundle proxies into a consumer-facing offering with its own subscription lifecycle.

#### Observability

* Monitor request volume, latency, error rates, and audit history for every deployed API via per-API dashboards and log search.
* Endpoint health monitoring surfaces backend availability without leaving the console.

#### API detail workspace

* Manage every aspect of an API proxy after creation from a single workspace: general settings, properties, resources, notifications, CORS, entrypoints, endpoints, failover, health checks, logging and tracing, plans, consumers, broadcasts, user permissions, audit logs, and deployment.
* Compare any two deployed versions of an API definition and roll back to an earlier one.
* See [Configure your API proxy](../api-management/build/configure-your-api-proxy/README.md).

### Authorization Management

#### GAPL Policy Language

* Policies are written in GAPL (Gravitee Authorization Policy Language), a Cedar-syntax subset optimized for the Gamma visual editor.
* Each policy declares an effect (`permit` or `forbid`), a principal, an action, a resource, and optional `when` conditions.
* Condition support includes time-of-day restrictions, IP range checks, token budgets, cost ceilings, scope checks, PII filter flags, and tenant attribute matching.

#### Policy Categories

* **MCP Policies**: Access to MCP servers, tools, prompts, and resources.
* **AI Model Policies**: Access to AI providers and specific models, with cost and token usage constraints.
* **API Policies**: Access to API proxies, endpoints, and data fields.
* **Custom Policies**: Policies for resources not routed as MCP, API, Agent, LLM, or Event (internal applications, data assets, and bespoke resources).

#### Inline Enforcement

* The Policy Decision Point (PDP) runs inside the AI Gateway, API Gateway, and Event Gateway at microsecond latency with no network hop.
* Principals can be synced from identity providers via SCIM or from Gravitee Access Management, with live sync progress surfaced via toast notifications.

#### Pre-built Condition Snippets

* Each policy category ships with reusable condition snippets for common scenarios: business hours, trusted device, corporate IP range, token budget, cost ceiling, rate limit, and tenant match.

### Edge Management

#### Shadow AI Detection

* Continuously scans device network connections to detect any process communicating with a known AI provider, regardless of whether traffic is routed through the Edge Daemon.
* Surfaces unmanaged AI usage across the device fleet with no per-tool configuration required.

#### Active Traffic Routing

* **Interception mode (default)**: Transparent local DNS resolver redirects configured AI provider domains to the daemon, which terminates TLS locally and forwards to the AI Gateway. No per-tool configuration needed. Automatically handles Node.js tools (Claude Code, Cursor) via `NODE_EXTRA_CA_CERTS`.
* **Proxy mode**: Tools can be pointed at the Edge Daemon explicitly via provider base URL environment variables for direct routing.

#### Local Pre-Egress Policy Enforcement

* Blocks sensitive data before it leaves the device: secrets, classified content, large prompt payloads, and disallowed models.
* Policies are evaluated locally so enforcement is not dependent on network connectivity to the gateway.

#### MDM Deployment

* Distributed via Kandji (Jamf and Intune planned) with automatic OS and Node.js trust store setup, with no manual certificate steps required.

### Event Stream Management

#### Kafka Cluster Registration

* Import existing Kafka clusters into Gamma so they can be governed, monitored, and composed into higher-level services.
* Registered clusters are available as the backing infrastructure for Kafka Services and Virtual Clusters.

#### Kafka Service Creation

* Define a governed Kafka Service with security plans, policies, and access controls backed by either a Registered Cluster or a Virtual Cluster.
* Analogous to an API proxy in API Management. The same plan types and policy model apply to event streams.

#### Virtual Clusters

* Provision logically isolated Kafka environments on shared infrastructure for multi-tenant workloads (Kafka Mesh).
* Prevents cross-tenant data access while allowing shared underlying broker infrastructure.

#### AI Bridging

* Kafka APIs and event streams can be exposed as **Kafka API Tools** in Agent Management, making existing event infrastructure accessible to AI agents without redevelopment.

### Platform Management

#### Application Management

* Manage consumer applications and their subscriptions to APIs, event streams, and agent services from a single location.

#### Shared Resources

* Define reusable components (OAuth2 token validation endpoints, cache stores, and authentication providers) that API proxies reference at runtime.

#### Access Management Integration

* Configure the connection to Gravitee Access Management, select an environment and domain, and verify OAuth capabilities required by agent identities and security plans.

#### OpenAPI Viewer Configuration

* Configure the OpenAPI viewer globally across both the management console and Portal Next for a consistent API documentation experience.
