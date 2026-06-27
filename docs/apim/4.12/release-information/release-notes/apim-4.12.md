# APIM 4.12

## New Features

#### **Hazelcast Rate Limit Repository**

* The Hazelcast rate limit repository is now available as an alternative to Redis for distributed rate limiting across gateway instances.
* Supports both standalone deployments (TCP-IP discovery) and Kubernetes environments (automatic service discovery via the Helm chart).
* Configure by setting `ratelimit.type=hazelcast` in `gravitee.yml` and providing a `hazelcast-ratelimit.xml` configuration file (sample included in the distribution).
* Kubernetes deployments using the Helm chart automatically provision the required Service, RBAC permissions, and discovery configuration when `apim.managedServiceAccount=true`.
* When RBAC is disabled, each gateway pod operates as a single-member cluster, which multiplies rate limit budgets by the replica count.

#### **JWT Policy Nested Claim Extraction**

* The JWT policy now supports dot-notation syntax (e.g., `realm_access.preferred_username` or `act.repository`) to extract user identities and client IDs from nested JWT claims.
* When a claim path contains a dot, the policy first checks for a top-level claim with that exact literal name, then traverses nested Map values if no flat claim exists, preserving backward compatibility.
* Configure nested claim extraction using the **User Claim** and **Client ID Claim** fields in the JWT policy settings—existing flat claim configurations continue to work unchanged.

#### **OpenTelemetry Tracing for Kafka Native APIs**

* Provides OpenTelemetry tracing for Kafka protocol operations, capturing connection lifecycle, authentication, and per-request spans with protocol-specific attributes (topics, batch counts, consumer groups, error codes).
* Requires enablement at both gateway level (`services.opentelemetry.enabled=true`) and per-API level (`analytics.tracing.enabled=true`), allowing platform administrators to control tracing infrastructure globally while API owners decide which APIs to instrument.
* Supports optional verbose mode (`services.opentelemetry.verbose=true` and `analytics.tracing.verbose=true`) that adds per-phase, per-flow, and per-policy spans for deep debugging—use only when needed as it significantly increases trace volume on high-throughput APIs.
* Includes API key filtering (`services.opentelemetry.kafka.tracedApiKeys`) to restrict tracing to specific Kafka protocol types (e.g., `PRODUCE`, `FETCH`), reducing noise from housekeeping requests.
* Spans include OpenTelemetry semantic conventions for messaging systems and Gravitee-specific attributes for error classification, authentication details, and API identification.

#### **API Product Membership and Ownership Management**

* Add individual users as direct members of an API Product and assign them specific roles that determine their permissions (read, manage, deploy, etc.).
* Attach or detach groups to API Products, allowing group members to inherit API Product roles automatically without individual assignment.
* Transfer primary ownership of an API Product to another user or group, with the previous owner demoted to a regular role of your choice.
* Configure API Product Primary Owner mode at the environment level to control whether new API Products are owned by a user, a group, or either (hybrid mode).
* Review all API Products a user has access to (directly or through groups) from the Organization page's user details view.

#### **Cron Schedule Frequency Limits**

* Platform administrators can now enforce minimum intervals for cron-based services (documentation auto-fetch, dynamic properties, health-check) and dictionary polling to prevent performance degradation in shared or SaaS environments.
* Frequency limits are configured in `gravitee.yml` using standard 6-field cron expressions (e.g., `0 */5 * * * *` for 5-minute minimum) or millisecond delays for dictionaries.
* The Management API validates new or updated schedules against configured limits and rejects requests that exceed them with a validation error.
* Existing configurations that exceed newly applied limits continue to function but are silently enforced at runtime using the slower schedule without requiring manual updates.

#### **Import and Update v4 APIs from OpenAPI and Gravitee Definitions**

* Import or update v4 HTTP Proxy, Message, and Native APIs using Gravitee v4 API definitions or OpenAPI Specifications (JSON/YAML) from local files or remote URLs.
* Imported definitions fully overwrite existing API configurations, including endpoints, flows, plans, pages, and metadata, while preserving API ID and deployment state.
* OpenAPI imports automatically generate flows and endpoints, with optional documentation page creation and OAS Validation policy attachment.
* Requires `API_DEFINITION[UPDATE]` permission and is unavailable for Kubernetes-managed APIs or v2 APIs (which use the legacy import dialog).

#### **OpenTelemetry Logs Integration for Log-to-Trace Correlation**

* Injects active trace IDs and span IDs into runtime log records captured during request processing, enabling direct navigation from logs in Loki to corresponding traces in Tempo via Grafana.
* Captures request and response payloads at four lifecycle points (entrypoint request/response, endpoint request/response) and exports them asynchronously to Loki via OTLP/HTTP to avoid adding latency.
* Requires the `gravitee-reporter-otel` plugin installed as a `.zip` file in the gateway's `plugins/` directory and OpenTelemetry tracing enabled on the API.
* Controlled by a per-API OTel Logs toggle in the Console UI under Runtime Logs settings, subject to the configured tracing sampling strategy.
* The `service.name` must match between tracer and logger (default: `gio_apim_gateway`) for Grafana correlation to function correctly.

#### **API Product Analytics and Logging**

* Track and filter API requests by API Product association across analytics dashboards, environment logs, and reporter outputs.
* When an API is accessed through an API Product subscription, the request is associated with that product for product-level observability across logs, metrics, and analytics.
* Filter analytics and environment logs by API Product to view metrics for specific API Products.
* The Elasticsearch, File, TCP, and Datadog reporters capture the API Product ID in their output when requests use an API Product subscription. The File and TCP reporters emit it in whichever output format you configure — as `apiProductId` in JSON, `api-product-id` in Elasticsearch format, or a trailing value in CSV — and the Datadog reporter adds it as an `ApiProductId` metric tag.
* Available for v4 request/response APIs only. The Elasticsearch reporter applies the required `api-product-id` keyword mapping automatically on upgrade; self-managed Elasticsearch installations must add the mapping themselves.

#### **Kafka Port-Based Routing for Native APIs**

* Enables the gateway to route native Kafka API traffic using dedicated TCP ports instead of SNI-based host routing, allowing multiple Kafka APIs to coexist on the same gateway instance without requiring distinct hostnames.
* Each plan receives a unique bootstrap port (1024–65535) and broker port range, with automatic conflict detection preventing overlapping port allocations across plans in the same environment.
* Requires gateway version 4.12.0 or later with `kafka.routingMode=port` configured and console version 4.12.0 or later with `console.kafka.portRouting.enabled=true`.
* Applies only to native Kafka API types; proxy and message APIs continue to use host-based routing.

#### **Portal Navigation Templating with FreeMarker Expressions**

* Developer Portal pages now support FreeMarker template expressions (`${...}`) to embed dynamic, context-aware content based on API metadata, lifecycle state, ownership, and environment properties.
* API-scoped pages expose an `api` root variable containing the full API model object (V2, V4 HTTP/Async, V4 Native, or Federated), while environment-scoped pages expose a `metadata` root variable with environment-level key/value pairs.
* Templates are evaluated at render time (when the page is requested), not when saved, ensuring real-time data accuracy.
* Enhanced error handling surfaces specific backend validation messages instead of generic client-side notifications when template expressions fail.
* The `api` variable provides access to common fields (ID, name, version, state, lifecycle state, visibility, tags, categories, primary owner) and type-specific fields (proxy configuration for V2, listeners/endpoint groups for V4, failover for V4 HTTP).

#### **Portal Analytics Dashboards**

* API consumers and administrators can now view pre-configured analytics dashboards in the New Developer Portal, displaying API traffic, performance, and usage metrics through customizable widgets (stats, charts, time-series).
* Dashboards aggregate data from HTTP requests, response times, and status codes, with filtering by API, application, or HTTP status. Users can pin up to 4 dashboards for quick access.
* Access is controlled by user role and API/application visibility. Environment administrators see all APIs but no application data; authenticated users see authorized APIs and their own applications.
* Requires the `portal.next.analytics.enabled` environment parameter set to `true`, which enables both the analytics endpoints and the New Developer Portal analytics UI.
* Dashboards are environment-scoped and isolated. Cross-environment access returns a `404` error.

#### **Remote URL Import for API Definitions**

* Import v4 APIs directly from remote HTTP(S) endpoints hosting Gravitee API definitions or OpenAPI specifications, when creating a new API or updating an existing one.
* Optional security controls let administrators restrict imports to an approved list of URLs and block imports from private or internal network addresses.
* Available only for v4 APIs. Creating an API requires permission to create APIs in the environment; updating an API requires permission to update the API definition.

#### **Native API Connection Logs**

* View and analyze client connection lifecycle events for Kafka-protocol APIs through a dedicated Logs page with summary metrics and filterable connection records.
* Each connection log captures lifecycle status (Connected, Disconnected, Failed, Unknown), client identifiers, server metadata, and error details when applicable.
* Control connection metrics reporting via a toggle in Reporter Settings—when disabled, no new logs are written and the Logs page displays a banner indicating reporting is off.
* Access requires `api-native_log-r` permission for list view and summary, plus `api-native_analytics-r` permission to inspect individual connection details.
* Requires Elasticsearch or OpenSearch reporter configuration to store and retrieve connection log data.

#### **Span Attribute Redaction for OpenTelemetry Tracing**

* Masks sensitive metadata in OpenTelemetry traces before export to external collectors, preventing exposure of authorization headers, API keys, consumer identifiers, and query parameters.
* Supports pattern-based redaction rules using glob patterns, short names, or regular expressions with FULL (complete replacement) or PARTIAL (prefix/suffix preservation) masking strategies.
* Configure global redaction rules in `gravitee.yml` or API-specific rules in the Console for v4 HTTP/Proxy and TCP APIs with tracing enabled.
* Rules are evaluated in order (global first, then API-specific) with first-match-wins behavior and case-insensitive key matching.

#### **API Overview Page Templates for Developer Portal**

* When APIs are added to the New Developer Portal navigation, Gravitee automatically creates unpublished Overview pages using pre-configured Gravitee Markdown templates.
* Two templates are available: a standard template with API metadata and subscription guidance, and an MCP proxy template for Model Context Protocol servers with one-click client configuration.
* The MCP template includes an embedded `<gmd-install-mcp>` component that generates configuration for AI clients (Cursor, VS Code, Claude Desktop) using the gateway endpoint and MCP path.
* API publishers can customize the generated overview pages to add quick start guides, use case descriptions, and links to external documentation.

#### **WSDL Import for v4 APIs**

* Create or update v4 HTTP Proxy APIs directly from WSDL 1.1 documents via file upload or remote URL.
* Automatically converts WSDL to OpenAPI 3 specification, mapping SOAP operations to REST paths and XSD schemas to JSON request bodies.
* Optionally applies REST to SOAP Transformer policy to enable REST/JSON-to-SOAP/XML translation with automatic flow generation.
* Supports OpenAPI Specification Validation policy for request/response validation against the converted spec.
* WSDL 2.0 is not supported; remote URLs must pass SSRF protection rules (private IPs blocked by default).

#### **Dashboard Filtering and Time Range Selection**

* Filter analytics dashboards by API, application, plan, status code, HTTP path, and other fields to focus on specific data subsets.
* Select from predefined relative time periods (last 5 minutes, 1 hour, 1 day, 1 week, 1 month) or specify custom absolute date ranges.

#### **MCP Server Installation Widget for Portal Pages**

* API publishers can embed one-click installer actions and copyable configuration snippets directly into New Developer Portal pages using the `<gmd-install-mcp>` Gravitee Markdown component.
* The widget generates client-specific configuration for Cursor, VS Code, and Claude Desktop, providing deep-link buttons (Cursor, VS Code) or a copyable JSON snippet (Claude Desktop).
* MCP Proxy APIs automatically seed an unpublished Overview page with a pre-configured installation widget when added to the portal navigation. The widget adapts to both remote HTTP/SSE transports and local stdio-based MCP servers.
* Supports eight attributes: `name`, `transport`, `url`, `headers`, `command`, `args`, `env`, and `clients`.

#### Application Membership Management

* You can now add members directly to applications, assign role-based permissions, and transfer application ownership through the Portal Next interface.
* External users can be invited by email to join applications. Invitations include a registration link with a JWT token, allowing recipients to create accounts and automatically become application members.
* Membership features are controlled by feature toggles: `portal.next.applications.membership.enabled` enables the Members tab, `portal.next.applications.membership.invitations.enabled` enables the Invitations tab, and `portal.next.applications.membership.transferOwnership.enabled` enables ownership transfer.
* User search results can include application membership status when you provide the `includes.applicationMembership` parameter, helping you identify existing members.
* You must have `APPLICATION_MEMBER` permissions, including CREATE, READ, UPDATE, and DELETE, and a configured `jwt.secret` for invitation token generation.

#### **API Key Lifecycle Management in Developer Portal**

* View all API keys associated with a subscription—active, revoked, and expired—in a paginated table on the subscription details page.
* Revoke and renew API keys directly from the Developer Portal when you hold Subscription Update permission on the API or application.
* API key status is determined by revocation and expiration dates, with active keys displaying a check-circle icon and inactive keys displaying an X-circle icon.
* The "Calling the API" section is hidden when all API keys are inactive (revoked or expired) for API-Key-secured plans.

#### **SSL Enforcement Policy: Issuer Whitelist for Client Certificates**

* The SSL Enforcement policy now supports issuer Distinguished Name (DN) whitelisting, allowing API administrators to restrict client certificate access to specific Certificate Authorities within the gateway's trusted set.
* Configure allowed issuers using order-insensitive DN matching with Ant-style pattern support (e.g., `CN=My Intermediate CA,O=GraviteeSource*,C=??`) in the policy's **Whitelist Issuers** field.
* Issuer validation requires client authentication to be enabled and validates only the certificate's immediate issuer, not the entire chain or root CA.
* An empty or unset whitelist disables issuer validation entirely, maintaining backward compatibility with existing configurations.

#### **Redis Cluster Support for Rate Limiting and Distributed Synchronization**

* Gravitee APIM 4.12 introduces Redis Cluster support for rate limiting and distributed synchronization repositories, enabling horizontal scaling of Redis infrastructure across sharded deployments.
* The gateway now shares Redis connection pools across resources and repositories that connect to the same endpoint, reducing connection overhead and improving performance under high load.
* Cache policies store response payloads as binary frames instead of JSON envelopes, preserving byte-for-byte fidelity for non-text content and reducing serialization overhead.
* Redis cache resource 2.0.0+ requires Java 21 runtime and APIM 4.12 minimum platform version. Cluster mode is mutually exclusive with Sentinel mode.
* Rate limiting in Cluster mode enforces read policy `NEVER` (masters only) to ensure atomic counter operations and consistent state across sharded nodes.

#### **Cascade Operations for Portal Navigation**

* You can now publish, unpublish, and delete folders and API sections along with all nested content in a single action.
* When you publish or unpublish a folder, the visibility change propagates to all nested documentation pages, sub-folders, and APIs. When you unpublish a folder, all nested items are set to `PRIVATE` visibility.
* When you delete a folder or API section, the container and all descendants are removed recursively. The **Delete** button is now enabled for all items regardless of child count, and sibling items are automatically reordered after deletion.

#### **Token-Bucket Rate Limiting Policy**

* Introduces a new rate-limiting policy that allows controlled bursts of traffic while maintaining a steady average request rate, providing more flexible traffic management than fixed-window rate limits.
* Supports both strict (per-request atomic enforcement) and async (approximate, higher-throughput) modes, with configurable burst capacity, refill rate, and refill period.
* Available for HTTP proxy APIs and V4 message APIs, with optional custom key composition using Expression Language to identify consumers by IP address, user ID, or other attributes.
* Requires a distributed repository (Redis, MongoDB, JDBC, or Hazelcast) for rate-limit state synchronization across gateway nodes.

#### **API Product Deployment with Sharding Tags**

* API Products and their plans can now be assigned organization-level sharding tags to control deployment placement across gateway instances, enabling geographic distribution, environment segmentation, and multi-tenant isolation.
* Product tags define the maximum deployment scope for all plans within that product. Plan tags must be a subset of product tags and refine placement within the product's scope. Plans with no tags inherit the full product deployment scope.
* Member APIs become deployable on a gateway when either their own sharding tags match the gateway or they have at least one published or deprecated product plan indexed on that gateway (where product tags match and plan tags are empty or matching).
* Gateways must declare matching tag keys in their configuration files to index and serve tagged products. Console tag assignment alone is insufficient for deployment.
* Deleting an organization-level tag cascades to all API Products and plans across all environments, automatically removing the tag from affected resources.

#### **Azure Key Vault Secret Provider**

* Retrieve JSON formatted secrets from Azure Key Vault using the `secret://azure-keyvault/` URL scheme in APIM or AM configuration. In API configurations, policies, and authentication flows, use the `{#secrets.get('/azure-keyvault/secret:key')}` Expression Language syntax.
* Supports six authentication methods to accommodate different Azure deployment scenarios: Client Secret, Certificate, Default Azure Credential, Managed Identity, Environment, and Workload Identity. Workload Identity is currently in beta.
* Automatically maps common secret keys—`username`, `password`, `certificate`, and `private_key`—to well-known identifiers for use in authentication and TLS configurations.
* Requires Gravitee APIM or AM 4.11.x or later and appropriate Azure AD credentials based on the selected authentication provider.

#### **Configurable Documentation Viewers for Portal Pages**

* Portal administrators can now select between Swagger UI and Redoc viewers for OpenAPI documentation pages, with Swagger UI offering interactive Try It Out functionality and Redoc providing a read-focused reference layout.
* AsyncAPI documentation pages render with an interactive viewer and include a starter AsyncAPI 3.0 template for new pages, with YAML validation enforced before saving.
* Viewer configuration is managed through Portal Navigation settings in the Console, with live preview during editing and independent storage of viewer settings from specification content.
* Swagger UI supports full configuration options including base URL override and OAuth with PKCE, while Redoc exposes viewer selection and optional base URL override only.

#### **Typo-Tolerant API Search**

* Enables developers to find APIs in the Developer Portal catalog even when search queries contain minor spelling errors. For example, "paymnt" returns "payment" APIs.
* Applies fuzzy matching based on Levenshtein distance: tokens with four to seven characters tolerate one edit, tokens with eight or more characters tolerate two edits, and tokens shorter than four characters require exact matches.
* Disabled by default and configurable per environment by administrators with the `ENVIRONMENT_SETTINGS` update permission.
* Automatically skips fuzzy matching for queries longer than 512 characters to maintain performance.

#### **Portal and Documentation Management via Automation API**

* Enables CI/CD-driven configuration of next-generation Developer Portal structure, API listings, and documentation through the Automation API.
* Supports declarative portal management using Gravitee Kubernetes Operator (GKO) CRDs or the Terraform provider to define navigation hierarchies, publish APIs, and attach documentation pages.
* Navigation paths use slash-separated strings (`/projects/alpha`) with optional display names and ordering. Portal listings control API placement and sequence within the navigation tree.
* Documentation pages support Gravitee Markdown, OpenAPI, and AsyncAPI formats and can be scoped to either the portal (platform-level) or specific APIs (appearing under each published API instance).
* In 4.12, one portal instance per environment is supported (multi-portal is planned for a future release). All requests must target the HRID `default-portal`. Navigation sync is limited to the top navigation bar area.

## Improvements

#### **Policy Description Tracing**

* Policy execution spans in OpenTelemetry traces now include a `gravitee.policy.description` attribute when verbose tracing is enabled. This feature improves observability and troubleshooting.
* The description is populated from the Description field configured on each policy step in API flows and Shared Policy Groups.
* The attribute is only emitted when a non-blank description is set and verbose tracing is enabled at both the API and gateway level.
* Applies to v2 APIs, v4 HTTP/Proxy APIs, v4 Message APIs, and Shared Policy Groups.

#### **Enhanced Certificate Validation for SSL Enforcement Policy**

* The SSL Enforcement policy now validates client certificate attributes beyond distinguished names, including Certificate Policy OIDs and Subject Alternative Name (SAN) patterns.
* OIDs are configured in dotted-decimal format (e.g., `1.3.6.1.4.1.99999.1`); SAN patterns support Ant-style matching (e.g., `*.example.com`, `partner.example.com`).
* All specified OIDs must be present in the certificate's Certificate Policies extension; at least one SAN must match a configured pattern for validation to succeed.
* Both new fields are additive and disabled when their list is empty, so existing policy configurations are unaffected.

#### **V2 API Analytics Continuity After Migration**

* Migrating an HTTP proxy API from v2 to v4 no longer causes loss of historical analytics data. After migration, the API's pre-migration (v2) and post-migration (v4) data appear together in the per-API analytics dashboard and connection logs. Analytics continuity doesn't extend to environment-level analytics.
* The gateway updates the Elasticsearch or OpenSearch index template automatically on startup. For `gravitee-request-*` indices created before this release, an administrator adds field aliases manually with a one-time mapping update.
* Requires Elasticsearch 7.x, 8.x, or 9.x, or OpenSearch.

#### **Improved Developer Portal display for federated APIs**

* The Developer Portal now adapts API access information for federated APIs based on plan security type. Because federated APIs are hosted by the third-party provider and not proxied through the Gravitee gateway, the portal hides inapplicable connection details.
* For keyless federated APIs, the API access card is hidden entirely since there are no Gravitee-managed endpoints or credentials to display.
* For API key federated APIs, the API access card displays only the provider-provisioned API keys section, hiding the base URL and curl command sections.
