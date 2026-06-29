# Gamma Release

Released [date]

## Highlights

- **Unified Observability Dashboard & Endpoints** — Full HTTP Proxy observability and extensive analytics endpoints for end-to-end API monitoring.
- **Store-backed Unified Filter Catalog** — Advanced filtering with translated conditions and store-backed listings for precise log and analytics search.
- **Kafka Multi-Endpoint Groups** — In-place editing and multi-endpoint group support aligning Kafka APIs with standard API management flows.
- **Bundled Kafka Policies** — Default gateway distribution now includes Kafka-compatible policies out-of-the-box.
- **MCP Studio Tools Editor** — New visual Studio page for assembling and editing AI tool compositions for agents.
- **Agent Subscription Management** — Full lifecycle support (approve/reject/close) for agent service subscriptions.
- **Native Edge Ingress** — Native ingress support for the gateway edge reactor, accessible via the new Edge Management console card.
- **Multi-Tenant AuthZEN PDP** — New tenant-isolated Policy Decision Point enhancing authorization gateway synchronization.
- **API Product Sharding Tags** — Granular routing and deployment control for API Products via sharding tags.
- **DataTable UI Migration** — Highly performant data table components for managing large catalogs of API Proxies and API Products.

## Breaking changes and deprecations

*(No breaking changes in this release)*

## New features

### API Management

#### **Unified Observability Dashboard & Endpoints**

- Introduces a comprehensive set of analytics endpoints to the Gamma surface, paired with a full HTTP Proxy observability dashboard for end-to-end API monitoring.
- Exposes dedicated endpoints for log search and single log detail retrieval (`GET /observability/logs/{requestId}`).
- Accessible via the new API Overview and Analytics sections in the console for supported API types.

#### **Store-backed Unified Filter Catalog**

- Adds a new unified filter catalog that allows administrators and API publishers to query analytics and logs using translated, human-readable filter conditions.
- Supports Gamma-only `KEYWORD` filters and exposes store-backed value listings, drastically improving search capability across observability metrics.
- This capability seamlessly integrates into the new logs search UI and analytics dashboards.

#### **API Product Sharding Tags**

- You can now attach sharding tags directly to API Products, granting granular control over which gateway instances deploy specific API Products.
- Simplifies the architecture for multi-region or segregated environments where distinct API Product subscriptions must be routed differently.
- Configurable directly from the API Product settings page in the Console.

### Event Stream Management

#### **Kafka Multi-Endpoint Groups & In-Place Editing**

- Aligns Kafka API creation and editing with the standard API Management flows by introducing multi-endpoint groups for Kafka Native APIs.
- Enables in-place editing of Kafka configurations and allows multiple Kafka API plans to coexist smoothly without overriding routing constraints.
- Configuration is available directly in the API endpoints and plans tabs for Kafka services.

#### **Bundled Kafka-Compatible Policies**

- The default gateway distribution bundle now ships with Kafka-compatible policies out-of-the-box, streamlining deployment for event-driven architectures.
- Reduces friction when applying security, transformation, and rate-limiting policies to Kafka message streams.

#### **ESM Module Integration**

- The Event Stream Management (ESM) module has been fully integrated (`gravitee-gamma-module-esm 1.0.0-alpha.1`), formalizing the foundational source code for event-driven API composition.

### Agent Management

#### **MCP Studio Tools Editor**

- Introduces a new Studio Tools page that allows visual editing of Model Context Protocol (MCP) tool compositions.
- Enables platform engineers to seamlessly assemble, configure, and orchestrate AI tools for agents via a dedicated drag-and-drop interface.
- Available under the AI Management / Agents section of the console.

#### **Subscription Lifecycle Management**

- Adds explicit endpoints and UI capabilities to approve, reject, and close subscriptions for agent services.
- Brings parity between AI Agent subscription lifecycle management and standard API Management workflows.

#### **New Access Management Permissions**

- Introduces two new permission roles: `AM_CONFIGURATION` and `AGENT_IDENTITY`.
- Enables finer-grained access control over Access Management configurations and AI agent identity management within the platform.

### Edge Management

#### **Native Ingress Support for Gateway Edge Reactor**

- Adds native ingress support configuration directly for the gateway edge reactor.
- Optimizes traffic routing for Edge gateways deployed in distributed or resource-constrained environments.
- Can be configured via standard Helm charts for edge deployments.

#### **Edge Management Application Card**

- Adds a dedicated Edge Management application card to the main Gamma console, providing a top-level entry point for managing Edge environments.

### Authorization Management

#### **Multi-Tenant AuthZEN PDP**

- Introduces a multi-tenant AuthZEN Policy Decision Point (PDP) for the Gamma platform.
- Enhances Authorization Gateway Sync capabilities by allowing discrete, tenant-isolated policy evaluations in distributed environments.

### Platform-wide

#### **OpenAPI Viewer Configuration**

- Adds the ability to globally configure the OpenAPI viewer settings across both the management console and Portal Next.
- Ensures a consistent documentation rendering experience for API consumers.
- Configurable under Platform Settings.

#### **Learning Tour Onboarding**

- Introduces a guided learning tour for new members, providing step-by-step contextual onboarding upon first logging into the console.
- Helps accelerate user familiarity with the Gamma platform's UI and key workflows.

#### **Tasks & Approvals Deep-Linking**

- Task and approval notifications now deep-link directly to the corresponding module page (e.g., specific API, subscription, or agent).
- Eliminates the need to manually search for pending requests from the global tasks dashboard.

## Improvements

### API Management

#### **DataTable Component Migration**

- The API Proxies and API Products list views have been migrated to a new, highly performant `DataTable` component. This significantly improves loading times, sorting capabilities, and overall user experience when managing large catalogs.

#### **Logs Search Enhancements**

- Improved the underlying query engine for log search by enforcing strict catalog operators, translating remaining LOGS filter conditions, and propagating `apiType` throughout the logs search context.

#### **Analytics Data Quality Fixes**

- Improved analytics data quality and added support for a new `ENTRYPOINT` filter dimension, allowing you to slice traffic metrics based on the specific entrypoint invoked.

### Event Stream Management

#### **Virtual Cluster Safeguards**

- The Virtual Cluster composition flow now explicitly excludes connections that are already in use, preventing configuration conflicts and overlapping routing paths.

#### **Wizard Enhancements**

- The listener port field has been removed from the Create Kafka Service wizard, and the path for configuring multi-connection SASL/SSL has been clarified, reducing friction during initial setup.

#### **Analytics Warnings**

- The console now displays a clear warning when native Kafka API traffic is actively flowing but analytics have been disabled, helping prevent unintended visibility gaps.

## Bug fixes

### API Management

- **User Permissions UI** — Fixed a minor UI defect on the User Permissions page for API Proxies, ensuring accurate display of assigned roles.
