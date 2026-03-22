# APIM 4.11

## Highlights

## Breaking Changes

## New Features


<!-- PIPELINE:APIM-12439 -->
#### **AI-Powered PII Filtering Policy**

* Automatically detects and redacts Personally Identifiable Information (PII) in API request and response payloads using AI token classification models
* Supports configurable redaction rules based on AI confidence thresholds (0.0–1.0) and PII categories (PERSON, LOCATION, EMAIL, etc.)
* Requires Enterprise license with `agent-mesh` pack, write permissions to `$GRAVITEE_HOME/models` directory for automatic model downloads, and sufficient heap memory for model loading
* Includes streaming detection safeguards that reject streaming requests when response filtering is enabled to prevent incomplete redaction
<!-- /PIPELINE:APIM-12439 -->


<!-- PIPELINE:APIM-12497 -->
#### **Entrypoint Connect Phase for Native APIs**

* Policies can now execute during the Entrypoint Connect phase, which runs immediately after a client establishes a TCP connection but before authentication and message processing.
* This phase enables connection-level controls such as IP filtering and TLS certificate validation, with the ability to interrupt connections before authentication occurs.
* Context attributes set during Entrypoint Connect are automatically propagated to all subsequent phases (authentication, interact, publish/subscribe).
* Available for Native Kafka APIs (reactor 6.0.0-alpha.1+) and agent-to-agent APIs (connectors 2.0.0-alpha.1+) in APIM 4.11.0 or later.
* The deprecated `CONNECT` mode is replaced by this new phase, which provides a dedicated execution point in the policy chain.
<!-- /PIPELINE:APIM-12497 -->

<!-- PIPELINE:APIM-12550 -->
#### **A2A Proxy API Type**

* **Breaking change** — A2A proxy APIs created before APIM 4.11 aren't supported. Delete and recreate any existing A2A proxy APIs.
* Introduces a dedicated V4 API type for agent-to-agent communication, enabling direct integration between AI agents through the Gravitee platform.
* Uses a standalone reactor architecture with HTTP selectors for flow routing and supports REQUEST and RESPONSE flow phases for policy execution.
* Requires Enterprise Edition with the AI Agent Management pack and APIM 4.11 or later.
* Configure the endpoint with a target URL pointing to the agent service and apply compatible policies such as rate limit, IP filtering, transform headers, and AI prompt guard rails.
<!-- /PIPELINE:APIM-12550 -->

<!-- PIPELINE:APIM-12437 -->
#### **AI Semantic Caching for LLM Proxy APIs**

* Reduces LLM token consumption and API latency by caching responses based on semantic meaning rather than exact text matching.
* Uses AI text embedding models and vector stores to identify semantically similar prompts, even when phrased differently, and returns cached results when similarity exceeds the configured threshold.
* Supports cache partitioning via metadata parameters (for example, API, plan, user ID) to ensure context-appropriate responses for identical queries from different users.
* Requires an AI text embedding model resource (ONNX BERT, OpenAI, or HTTP provider) and a vector store resource (Redis or AWS S3) with compatible embedding dimensions.
* Available exclusively on LLM Proxy APIs deployed with Agent Mesh.
<!-- /PIPELINE:APIM-12437 -->

<!-- PIPELINE:APIM-12371 -->
#### **API Products**

* Bundle multiple V4 HTTP Proxy APIs into a single subscribable package with unified access control and product-level plans (API Key, JWT, or mTLS).
* Manage subscriptions at the product level instead of individual APIs, enabling API product managers to package and monetize APIs at scale.
* APIs must have the `allowedInApiProducts` flag enabled to be included in products; APIs can belong to multiple products while maintaining their own direct subscription plans.
* Requires Enterprise Universe tier license and environment-level permissions for API Product management.
* Plans and subscriptions now support a reference model with `referenceType` (API or API_PRODUCT) and `referenceId` fields; the legacy `api` field is deprecated as of 4.11.0.
<!-- /PIPELINE:APIM-12371 -->

<!-- PIPELINE:APIM-13008 -->
#### **JMS Endpoint Connector for Message Broker Integration**

* Enables Gravitee APIM to produce and consume messages from JMS-compliant brokers (ActiveMQ, IBM MQ, Solace, etc.) using queue or topic messaging patterns.
* Supports multiple connection factory configuration methods: direct broker URL, provider-specific properties (hostname/port/channel), or JNDI lookup with custom properties.
* Configurable for producer mode (send messages with TEXT or BYTES format), consumer mode (receive messages with durable subscription support), or both capabilities simultaneously on the same endpoint.
* Requires `event-native` license pack and JMS provider client library placed in `./plugins/jms/ext/` directory.
* Topic consumers use shared or exclusive connections based on client ID and durability settings; queue consumers always use shared connections.
<!-- /PIPELINE:APIM-13008 -->

<!-- PIPELINE:APIM-12999 -->
#### **Native IP filtering policy for Kafka APIs**

* Controls client access to Native Kafka APIs by matching client IP addresses against configurable whitelist and blacklist rules during the entrypoint connection phase (`ENTRYPOINT_CONNECT`).
* Supports IPv4, IPv6, CIDR notation, IP ranges, comma-separated IP lists, and Expression Language for dynamic filtering.
* Automatically normalizes IPv4-mapped IPv6 addresses to their IPv4 equivalents for rule matching.
* Rejects unauthorized connections with the Kafka protocol error `CLUSTER_AUTHORIZATION_FAILED` and the message `"IP not allowed"`.
* Requires Enterprise Edition license with the `apim-native-policy-ip-filtering` feature.
<!-- /PIPELINE:APIM-12999 -->


<!-- PIPELINE:APIM-12170 -->
#### **Subscription Forms for API Metadata Collection**

* API administrators can create custom subscription forms using Gravitee Markdown (GMD) components to collect structured metadata from API consumers during the subscription process.
* Forms support six component types (text input, textarea, select, checkbox, radio, and layout containers) with validation rules and are rendered in the Developer Portal subscription checkout flow.
* Collected metadata is stored with each subscription as key-value pairs and displayed in Console subscription detail views as read-only JSON.
* Forms are configured per environment in Console under **Settings > Subscription Form** and can be enabled or disabled to control visibility to API consumers.
* Requires JDBC repository configuration with the `subscription_forms` table schema (deploy migration script included in this release).
<!-- /PIPELINE:APIM-12170 -->

## Improvements

## Bug Fixes
