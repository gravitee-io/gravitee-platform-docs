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


<!-- PIPELINE:APIM-12308 -->
#### **Node Logging Infrastructure with MDC Context**

* Enriches application logs with contextual metadata (node ID, API ID, application ID, plan ID) for improved traceability and debugging in production environments.
* Configure MDC filtering and log patterns directly in `gravitee.yml` without manually editing `logback.xml`, using the `node.logging.mdc.include` property and `%mdcList` conversion word.
* Supports runtime pattern override for console and file appenders, automatically wrapping file appenders in async mode when enabled via `node.logging.pattern.overrideLogbackXml`.
* Provides context-aware logging for reactive code paths using `ctx.withLogger(log)` pattern to ensure execution context metadata appears in asynchronous request logs.
* Available from APIM 4.11; requires `gravitee-node` 8.0.0-alpha.2+ for plugin development and Helm chart version supporting `logback.override` configuration for Kubernetes deployments.
<!-- /PIPELINE:APIM-12308 -->

## Improvements

## Bug Fixes
