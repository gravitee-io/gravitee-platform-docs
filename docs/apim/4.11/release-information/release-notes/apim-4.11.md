# APIM 4.11

## Highlights

* LLM Dashboard and MCP Dashboard provide real-time analytics for LLM token usage, costs, and MCP request latency in the APIM Console.
* AI-Powered PII Filtering policy detects and redacts personally identifiable information in API payloads using on-device AI models.
* AI Semantic Caching reduces LLM token consumption by returning cached responses for semantically similar prompts.
* A2A Proxy API type enables direct agent-to-agent communication through a dedicated V4 reactor with HTTP selectors.
* API Products bundle multiple V4 HTTP Proxy APIs into a single subscribable package with unified plans and subscriptions.
* JMS Endpoint Connector integrates Gravitee with JMS-compliant brokers (ActiveMQ, IBM MQ, Solace) for queue and topic messaging.
* Entrypoint Connect phase enables policy execution at TCP connection time for Native Kafka and A2A APIs, before authentication.
* mTLS plan support for Kafka Native APIs authenticates clients via X.509 certificates with dynamic trust store updates.
* Kafka Governance Rules policies enforce compliance standards on Produce, Fetch, CreateTopics, and AlterConfigs requests.
* Kafka message encryption and decryption policy protects Kafka payloads at the gateway level using AES-GCM with JWE or DEK modes.
* Native IP filtering policy for Kafka APIs controls client access using whitelist/blacklist rules with IPv4, IPv6, and CIDR support.
* Multi-tenant endpoint support routes Kafka traffic to different backend clusters based on gateway tenant configuration.
* Subscription forms let API publishers define custom forms that consumers complete when subscribing to plans.
* Context-aware logging infrastructure automatically enriches gateway logs with API, organization, environment, and plan metadata.

## Breaking Changes and deprecations&#x20;

#### **End of support for V1 APIs**

V1 APIs have been deprecated since version 4.0.0 of API Management (APIM). From 4.12.0 of APIM, V1 APIs are no longer supported. To prepare for the end of support, you must migrate your V1 APIs to at least V2 before upgrading to 4.12.0.

#### **A2A proxy APIs**

The A2A proxy architecture introduces the `A2A_PROXY` API type. With this change, you must create your A2A Proxy APIs again to avoid any issues and to align with the new architecture.

Existing A2A proxy APIs continue to work but they are no longer supported.

## New Features

#### **LLM Dashboard**

* Users can view analytics for their LLMs in the observability section of their APIM Console.
* The LLM dashboard provides you with clear visibility into the LLMs' performance and traffic patterns.
* The dashboard shows the following key metrics:
  * **Total tokens.** The combined total of prompt tokens and completion tokens processed.
  * **Average tokens per request.** The average token consumption for each LLM call.
  * **Total token count over time.** The cost trend of tokens for prompts and completion.
  * **Token cost over time.** The trend of prompt, completion, and total tokens consumed.
  * **Total cost.** The total cost of the LLM usage.
  * **Average cost per request.** The average spend for each LLM call.
  * **Response status repartition.** The breakdown of HTTP outcomes for each LLM call.
  * **Total token per model.** The breakdown of consumption across LLM models.
  * **Total requests.** All HTTP calls processed by the Gateway.
  * **LLM requests.** Total call volume targeting LLM providers.

#### **MCP dashboard**

* Users can view analytics for their MCPs in the observability section of their APIM Console.
* The MCP dashboard provides you with clear visibility into the MCPs' performance and traffic patterns.
* The dashboard shows the following key metrics:
  * **MCP requests.** The total number of requests targeting MCP APIs.
  * **Average latency.** The average Gateway latency for MCP requests.
  * **Max latency.** The maximum Gateway latency observed for MCP requests.
  * **P90 latency.** The 90th percentile Gateway latency for MCP requests.
  * **P99 latency.** The 99th percentile Gateway latency for MCP requests.
  * **Method usage.** The distribution of MCP proxy methods by request count.
  * **Method usage over time.** The evolution of the method usage over time.
  * **Most used resources.** The top five used MCP resources by request count.
  * **Response status repartition.** The distribution of HTTP response status codes for MCP requests.
  * **Most used tools.** The top 5 MCP tools by request count.
  * **Most used prompts.** The top 5 most used request prompts by request count.
  * **Average response time.** Average Gateway response time for MCP requests over time.

#### **AI-Powered PII Filtering Policy**

* Automatically detects and redacts Personally Identifiable Information (PII) in API request and response payloads using AI token classification models
* Supports configurable redaction rules based on AI confidence thresholds (0.0–1.0) and PII categories (PERSON, LOCATION, EMAIL, etc.)
* Requires Enterprise license with `agent-mesh` pack, write permissions to `$GRAVITEE_HOME/models` directory for automatic model downloads, and sufficient heap memory for model loading
* Includes streaming detection safeguards that reject streaming requests when response filtering is enabled to prevent incomplete redaction

#### **Entrypoint Connect Phase for Native APIs**

* Policies can now execute during the Entrypoint Connect phase, which runs immediately after a client establishes a TCP connection but before authentication and message processing.
* This phase enables connection-level controls such as IP filtering and TLS certificate validation, with the ability to interrupt connections before authentication occurs.
* Context attributes set during Entrypoint Connect are automatically propagated to all subsequent phases (authentication, interact, publish/subscribe).
* Available for Native Kafka APIs (reactor 6.0.0-alpha.1+) and agent-to-agent APIs (connectors 2.0.0-alpha.1+) in APIM 4.11.0 or later.
* The deprecated `CONNECT` mode is replaced by this new phase, which provides a dedicated execution point in the policy chain.

#### **A2A Proxy API Type**

* Introduces a dedicated V4 API type for agent-to-agent communication, enabling direct integration between AI agents through the Gravitee platform.
* Uses a standalone reactor architecture with HTTP selectors for flow routing and supports REQUEST and RESPONSE flow phases for policy execution.
* Requires Enterprise Edition with the AI Agent Management pack and APIM 4.11 or later.
* Configure the endpoint with a target URL pointing to the agent service and apply compatible policies such as rate limit, IP filtering, transform headers, and AI prompt guard rails.

#### **AI Semantic Caching for LLM Proxy APIs**

* Reduces LLM token consumption and API latency by caching responses based on semantic meaning rather than exact text matching.
* Uses AI text embedding models and vector stores to identify semantically similar prompts, even when phrased differently, and returns cached results when similarity exceeds the configured threshold.
* Supports cache partitioning via metadata parameters (for example, API, plan, user ID) to ensure context-appropriate responses for identical queries from different users.
* Requires an AI text embedding model resource (ONNX BERT, OpenAI, or HTTP provider) and a vector store resource (Redis or AWS S3) with compatible embedding dimensions.
* Available exclusively on LLM Proxy APIs deployed with Agent Mesh.

#### **API Products**

* Bundle multiple V4 HTTP Proxy APIs into a single subscribable package with unified access control and API Product-level plans (API Key, JWT, or mTLS).
* Manage subscriptions at the API Product level instead of individual APIs, enabling API Product managers to package and monetize APIs at scale.
* APIs must have the `allowedInApiProducts` flag enabled to be included in API Products; APIs can belong to multiple API Products while maintaining their own direct subscription plans.
* Requires Enterprise Universe tier license and environment-level permissions for API Product management.
* Plans and subscriptions now support a reference model with `referenceType` (API or API\_PRODUCT) and `referenceId` fields; the legacy `api` field is deprecated as of 4.11.0.

#### **JMS Endpoint Connector for Message Broker Integration**

* Enables Gravitee APIM to produce and consume messages from JMS-compliant brokers (ActiveMQ, IBM MQ, Solace, etc.) using queue or topic messaging patterns.
* Supports multiple connection factory configuration methods: direct broker URL, provider-specific properties (hostname/port/channel), or JNDI lookup with custom properties.
* Configurable for producer mode (send messages with TEXT or BYTES format), consumer mode (receive messages with durable subscription support), or both capabilities simultaneously on the same endpoint.
* Requires `event-native` license pack and JMS provider client library placed in `./plugins/jms/ext/` directory.
* Topic consumers use shared or exclusive connections based on client ID and durability settings; queue consumers always use shared connections.

#### **Native IP filtering policy for Kafka APIs**

* Controls client access to Native Kafka APIs by matching client IP addresses against configurable whitelist and blacklist rules during the entrypoint connection phase (`ENTRYPOINT_CONNECT`).
* Supports IPv4, IPv6, CIDR notation, IP ranges, comma-separated IP lists, and Expression Language for dynamic filtering.
* Automatically normalizes IPv4-mapped IPv6 addresses to their IPv4 equivalents for rule matching.
* Rejects unauthorized connections with the Kafka protocol error `CLUSTER_AUTHORIZATION_FAILED` and the message `"IP not allowed"`.
* Requires Enterprise Edition license with the `apim-native-policy-ip-filtering` feature.

#### **Multi-Tenant Endpoint Support for Kafka APIs**

* Enables a single Kafka API definition to route traffic to different backend clusters based on the gateway's configured tenant identifier, eliminating the need to duplicate API definitions across deployment zones.
* Each endpoint in the first endpoint group can be tagged with one or more tenant identifiers; gateways automatically filter and activate only endpoints matching their configured tenant at startup and during hot-reload.
* Endpoints with no tenant tags are treated as shared and always match any gateway, making them useful during gradual rollout or for legacy gateways without tenant configuration.
* Configure the gateway tenant identifier using the `tenant` property in `gravitee.yml`, environment variable, or system property.
* If all endpoints in the group are tenant-specific and none match the gateway's tenant, the gateway can't route to the API and connections fail. Include at least one shared (untagged) endpoint to ensure the API remains accessible.

#### **Multiple Endpoints for Native Kafka APIs**

* Native Kafka APIs can now define multiple endpoints within an endpoint group, enabling pre-configured cluster alternatives for disaster recovery, migration, and regional routing scenarios.
* The gateway routes new connections to the active endpoint based on tenant configuration or list order—publishers control which endpoint is active by reordering endpoints in the group.
* Endpoint switching is manual and publisher-initiated; the gateway doesn't perform automatic failover or health checks, and Kafka clients must handle reconnection when endpoints change.
* Tenant-aware routing is supported: if the gateway tenant matches an endpoint's tenant tag, that endpoint is selected; otherwise, the first endpoint in the group is used.

#### **mTLS Plan Support for Kafka Native APIs**

* Kafka native APIs now support mTLS plans for client authentication using X.509 certificates, enabling accurate subscription resolution and metrics attribution.
* The gateway extracts the client certificate from the TLS session, computes its MD5 hash, and uses it as a security token to look up the subscription and populate connection context with `planId`, `applicationId`, and `subscriptionId`.
* Kafka native APIs enforce strict plan security mutual exclusion—you can't mix Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) in published state. Publishing a plan of one type automatically closes all published plans of conflicting types.
* Requires Gravitee APIM 4.11 or later, `gravitee-policy-mtls` version 2.0.0-alpha.2 or later, and gateway configuration with `kafka.ssl.clientAuth=required` and appropriate truststore/keystore settings.
* Subscription certificates are loaded dynamically without requiring gateway restarts—when a subscription is created or updated with a new certificate, the gateway's trust store manager refreshes automatically.

#### **Kafka Governance Rules Policies**

* Enforce compliance and operational standards on Kafka protocol requests (Produce, Fetch, CreateTopics, AlterConfigs) flowing through the Gateway.
* Validate fields such as acknowledgements, batch size, compression type, replication factor, and topic configurations against administrator-defined rules.
* Configure rule actions to forbid requests, override values, throttle clients, or log violations when governance conditions aren't met.
* Requires Enterprise Edition license with the `apim-native-kafka-policy-rules` feature and a Kafka-enabled API (v4 definition with Kafka entrypoint).

#### **Subscription Forms for API Plans**

* API publishers can now define custom subscription forms that API consumers complete when subscribing to API plans, replacing the legacy comment field from the Classic Portal.
* Forms are authored using Gravitee Markdown (GMD) in the Management Console with a live preview editor, and submitted values are stored as structured metadata with each subscription.
* Forms are scoped per environment and can be toggled visible or hidden for API consumers in the Developer Portal. Subscription forms aren't displayed for Keyless plans.
* Requires `environment-metadata-r` permission to view forms and `environment-metadata-u` permission to create, update, enable, or disable forms.

#### **Kafka message encryption and decryption policy**

* Encrypts and decrypts Kafka message payloads at the gateway level using AES-GCM (128, 192, or 256-bit), ensuring data is protected while stored in Kafka topics without requiring changes to producer or consumer applications.
* Supports three encryption modes: direct encryption with base64 output, direct encryption with JWE format, and DEK-based encryption that generates a unique data encryption key per message.
* Processes entire message payloads or individual JSON fields identified by JSONPath expressions. Optional compression (GZIP, LZ4, BZIP2, Snappy) mitigates the storage overhead of encrypted data.
* Keys are provisioned as base64-encoded values or stored in PKCS12 keystores, with support for Expression Language and the Gravitee secrets mechanism.

#### **AI Model Text Classification Resource**

* Provides eight pre-trained models for detecting toxic content and prompt injection attacks in API traffic, supporting up to 15 languages.
* Includes binary and multi-label toxicity detection models (2–16 labels) and two Llama Prompt Guard variants for identifying LLM prompt manipulation attempts.
* Administrators select models based on accuracy requirements, resource constraints, and language coverage, with configurable classification thresholds per model type.
* Models are sourced from HuggingFace repositories and require sufficient memory and compute resources (model sizes range from 4.39M to 100M+ parameters).


<!-- PIPELINE:APIM-13342 -->
#### **mTLS Certificate Management for Applications**

* Application owners can now upload, rotate, and manage client certificates for mutual TLS authentication directly in the New Developer Portal.
* Certificate rotation supports grace periods, allowing both old and new certificates to remain active simultaneously to prevent authentication downtime during transitions.
* Administrators control feature availability via the `portal.next.mtls.enabled` configuration property, and users require `APPLICATION_DEFINITION[UPDATE]` permission to manage certificates.
* Certificates are organized into Active and History views, with support for lifecycle statuses (Active, Active with End, Scheduled, and Revoked) and metadata display including subject, issuer, and fingerprint.
<!-- /PIPELINE:APIM-13342 -->

## Improvements

#### **Context-aware logging infrastructure**

* Gateway and Management API logs now automatically include request metadata (API ID, organization, environment, application, plan) via MDC (Mapped Diagnostic Context), enabling operators to filter and correlate logs across multi-tenant environments without manual instrumentation.
* Administrators configure which MDC keys appear in log output using `node.logging.mdc.include` and customize formatting with `node.logging.mdc.format` and `node.logging.mdc.separator` properties in `gravitee.yml`.
* Logback appender patterns are overridden at runtime via `node.logging.pattern.console` and `node.logging.pattern.file` properties when `node.logging.pattern.overrideLogbackXml` is set to `true` (default: `false`).
* The custom `%mdcList` Logback converter formats and filters MDC keys in log patterns. Structured encoders (JsonEncoder, EcsEncoder) log the full unfiltered MDC map.
