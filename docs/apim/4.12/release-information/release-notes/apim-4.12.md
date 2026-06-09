---
hidden: true
noIndex: true
---

# APIM 4.12

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:APIM-13752 -->
#### **Hazelcast Rate Limit Repository**

* The Hazelcast rate limit repository is now available as an alternative to Redis for distributed rate limiting across gateway instances.
* Supports both standalone deployments (TCP-IP discovery) and Kubernetes environments (automatic service discovery via the Helm chart).
* Configure by setting `ratelimit.type=hazelcast` in `gravitee.yml` and providing a `hazelcast-ratelimit.xml` configuration file (sample included in the distribution).
* Kubernetes deployments using the Helm chart automatically provision the required Service, RBAC permissions, and discovery configuration when `apim.managedServiceAccount=true`.
* When RBAC is disabled, each gateway pod operates as a single-member cluster, which multiplies rate limit budgets by the replica count.
<!-- /PIPELINE:APIM-13752 -->

<!-- PIPELINE:APIM-13822 -->
#### **JWT Policy Nested Claim Extraction**

* The JWT policy now supports dot-notation syntax (e.g., `realm_access.preferred_username` or `act.repository`) to extract user identities and client IDs from nested JWT claims.
* When a claim path contains a dot, the policy first checks for a top-level claim with that exact literal name, then traverses nested Map values if no flat claim exists, preserving backward compatibility.
* Configure nested claim extraction using the **User Claim** and **Client ID Claim** fields in the JWT policy settings—existing flat claim configurations continue to work unchanged.
<!-- /PIPELINE:APIM-13822 -->



<!-- PIPELINE:APIM-13472 -->
#### **OpenTelemetry Tracing for Kafka Native APIs**

* Provides OpenTelemetry tracing for Kafka protocol operations, capturing connection lifecycle, authentication, and per-request spans with protocol-specific attributes (topics, batch counts, consumer groups, error codes).
* Requires enablement at both gateway level (`services.opentelemetry.enabled=true`) and per-API level (`analytics.tracing.enabled=true`), allowing platform administrators to control tracing infrastructure globally while API owners decide which APIs to instrument.
* Supports optional verbose mode (`services.opentelemetry.verbose=true` and `analytics.tracing.verbose=true`) that adds per-phase, per-flow, and per-policy spans for deep debugging—use only when needed as it significantly increases trace volume on high-throughput APIs.
* Includes API key filtering (`services.opentelemetry.kafka.tracedApiKeys`) to restrict tracing to specific Kafka protocol types (e.g., `PRODUCE`, `FETCH`), reducing noise from housekeeping requests.
* Spans include OpenTelemetry semantic conventions for messaging systems and Gravitee-specific attributes for error classification, authentication details, and API identification.
<!-- /PIPELINE:APIM-13472 -->


<!-- PIPELINE:APIM-13461 -->
#### **API Product Membership and Ownership Management**

* Add individual users as direct members of an API Product and assign them specific roles that determine their permissions (read, manage, deploy, etc.).
* Attach or detach groups to API Products, allowing group members to inherit API Product roles automatically without individual assignment.
* Transfer primary ownership of an API Product to another user or group, with the previous owner demoted to a regular role of your choice.
* Configure API Product Primary Owner mode at the environment level to control whether new API Products are owned by a user, a group, or either (hybrid mode).
* Review all API Products a user has access to (directly or through groups) from the Organization page's user details view.
<!-- /PIPELINE:APIM-13461 -->


<!-- PIPELINE:APIM-12132 -->
#### **Import and Update v4 APIs from OpenAPI and Gravitee Definitions**

* Import or update v4 HTTP Proxy, Message, and Native APIs using Gravitee v4 API definitions or OpenAPI Specifications (JSON/YAML) from local files or remote URLs.
* Imported definitions fully overwrite existing API configurations, including endpoints, flows, plans, pages, and metadata, while preserving API ID and deployment state.
* OpenAPI imports automatically generate flows and endpoints, with optional documentation page creation and OAS Validation policy attachment.
* Requires `API_DEFINITION[UPDATE]` permission and is unavailable for Kubernetes-managed APIs or v2 APIs (which use the legacy import dialog).
<!-- /PIPELINE:APIM-12132 -->
<!-- PIPELINE:APIM-13463 -->
#### **OpenTelemetry Logs Integration for Log-to-Trace Correlation**

* Injects active trace IDs and span IDs into runtime log records captured during request processing, enabling direct navigation from logs in Loki to corresponding traces in Tempo via Grafana.
* Captures request and response payloads at four lifecycle points (entrypoint request/response, endpoint request/response) and exports them asynchronously to Loki via OTLP/HTTP to avoid adding latency.
* Requires the `gravitee-reporter-otel` plugin installed as a `.zip` file in the gateway's `plugins/` directory and OpenTelemetry tracing enabled on the API.
* Controlled by a per-API OTel Logs toggle in the Console UI under Runtime Logs settings, subject to the configured tracing sampling strategy.
* The `service.name` must match between tracer and logger (default: `gio_apim_gateway`) for Grafana correlation to function correctly.
<!-- /PIPELINE:APIM-13463 -->


<!-- PIPELINE:APIM-14123 -->
#### **Portal Navigation Templating with FreeMarker Expressions**

* Developer Portal pages now support FreeMarker template expressions (`${...}`) to embed dynamic, context-aware content based on API metadata, lifecycle state, ownership, and environment properties.
* API-scoped pages expose an `api` root variable containing the full API model object (V2, V4 HTTP/Async, V4 Native, or Federated), while environment-scoped pages expose a `metadata` root variable with environment-level key/value pairs.
* Templates are evaluated at render time (when the page is requested), not when saved, ensuring real-time data accuracy.
* Enhanced error handling surfaces specific backend validation messages instead of generic client-side notifications when template expressions fail.
* The `api` variable provides access to common fields (ID, name, version, state, lifecycle state, visibility, tags, categories, primary owner) and type-specific fields (proxy configuration for V2, listeners/endpoint groups for V4, failover for V4 HTTP).
<!-- /PIPELINE:APIM-14123 -->
<!-- PIPELINE:APIM-13459 -->
#### **Portal Analytics Dashboards**

* API consumers and administrators can now view pre-configured analytics dashboards in the New Developer Portal, displaying API traffic, performance, and usage metrics through customizable widgets (stats, charts, time-series).
* Dashboards aggregate data from HTTP requests, response times, and status codes, with filtering by API, application, or HTTP status. Users can pin up to 4 dashboards for quick access.
* Access is controlled by user role and API/application visibility. Environment administrators see all APIs but no application data; authenticated users see authorized APIs and their own applications.
* Requires the `portal.next.analytics.enabled` environment parameter set to `true`, which enables both the analytics endpoints and the New Developer Portal analytics UI.
* Dashboards are environment-scoped and isolated. Cross-environment access returns a `404` error.
<!-- /PIPELINE:APIM-13459 -->
<!-- PIPELINE:APIM-12146 -->
#### **Remote URL Import for API Definitions**

* Import v4 APIs directly from remote HTTP(S) endpoints hosting Gravitee API definitions or OpenAPI specifications, when creating a new API or updating an existing one.
* Optional security controls let administrators restrict imports to an approved list of URLs and block imports from private or internal network addresses.
* Available only for v4 APIs. Creating an API requires permission to create APIs in the environment; updating an API requires permission to update the API definition.
<!-- /PIPELINE:APIM-12146 -->
<!-- PIPELINE:APIM-14014 -->
#### **Native API Connection Logs**

* View and analyze client connection lifecycle events for Kafka-protocol APIs through a dedicated Logs page with summary metrics and filterable connection records.
* Each connection log captures lifecycle status (Connected, Disconnected, Failed, Unknown), client identifiers, server metadata, and error details when applicable.
* Control connection metrics reporting via a toggle in Reporter Settings—when disabled, no new logs are written and the Logs page displays a banner indicating reporting is off.
* Access requires `api-native_log-r` permission for list view and summary, plus `api-native_analytics-r` permission to inspect individual connection details.
* Requires Elasticsearch or OpenSearch reporter configuration to store and retrieve connection log data.
<!-- /PIPELINE:APIM-14014 -->
<!-- PIPELINE:APIM-13549 -->
#### **Span Attribute Redaction for OpenTelemetry Tracing**

* Masks sensitive metadata in OpenTelemetry traces before export to external collectors, preventing exposure of authorization headers, API keys, consumer identifiers, and query parameters.
* Supports pattern-based redaction rules using glob patterns, short names, or regular expressions with FULL (complete replacement) or PARTIAL (prefix/suffix preservation) masking strategies.
* Configure global redaction rules in `gravitee.yml` or API-specific rules in the Console for v4 HTTP/Proxy and TCP APIs with tracing enabled.
* Rules are evaluated in order (global first, then API-specific) with first-match-wins behavior and case-insensitive key matching.
<!-- /PIPELINE:APIM-13549 -->
<!-- PIPELINE:APIM-14122 -->
#### **API Overview Page Templates for Developer Portal**

* When APIs are added to the New Developer Portal navigation, Gravitee automatically creates unpublished Overview pages using pre-configured Gravitee Markdown templates.
* Two templates are available: a standard template with API metadata and subscription guidance, and an MCP proxy template for Model Context Protocol servers with one-click client configuration.
* The MCP template includes an embedded `<gmd-install-mcp>` component that generates configuration for AI clients (Cursor, VS Code, Claude Desktop) using the gateway endpoint and MCP path.
* API publishers can customize the generated overview pages to add quick start guides, use case descriptions, and links to external documentation.
<!-- /PIPELINE:APIM-14122 -->
<!-- PIPELINE:APIM-12279 -->
#### **WSDL Import for v4 APIs**

* Create or update v4 HTTP Proxy APIs directly from WSDL 1.1 documents via file upload or remote URL.
* Automatically converts WSDL to OpenAPI 3 specification, mapping SOAP operations to REST paths and XSD schemas to JSON request bodies.
* Optionally applies REST to SOAP Transformer policy to enable REST/JSON-to-SOAP/XML translation with automatic flow generation.
* Supports OpenAPI Specification Validation policy for request/response validation against the converted spec.
* WSDL 2.0 is not supported; remote URLs must pass SSRF protection rules (private IPs blocked by default).
<!-- /PIPELINE:APIM-12279 -->

## Improvements


<!-- PIPELINE:APIM-13462 -->
#### **Policy Description Tracing**

* Policy execution spans in OpenTelemetry traces now include a `gravitee.policy.description` attribute when verbose tracing is enabled. This feature improves observability and troubleshooting.
* The description is populated from the Description field configured on each policy step in API flows and Shared Policy Groups.
* The attribute is only emitted when a non-blank description is set and verbose tracing is enabled at both the API and gateway level.
* Applies to v2 APIs, v4 HTTP/Proxy APIs, v4 Message APIs, and Shared Policy Groups.
<!-- /PIPELINE:APIM-13462 -->


<!-- PIPELINE:APIM-13498 -->
#### **Enhanced Certificate Validation for SSL Enforcement Policy**

* The SSL Enforcement policy now validates client certificate attributes beyond distinguished names, including Certificate Policy OIDs and Subject Alternative Name (SAN) patterns.
* OIDs are configured in dotted-decimal format (e.g., `1.3.6.1.4.1.99999.1`); SAN patterns support Ant-style matching (e.g., `*.example.com`, `partner.example.com`).
* All specified OIDs must be present in the certificate's Certificate Policies extension; at least one SAN must match a configured pattern for validation to succeed.
* Both new fields are additive and disabled when their list is empty, so existing policy configurations are unaffected.
<!-- /PIPELINE:APIM-13498 -->

## Bug Fixes
