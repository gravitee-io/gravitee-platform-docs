---
description: Documentation about apim 4.10 in the context of APIs.
---

# APIM 4.10

## Release Date:

## Highlights

* Redis-backed distributed synchronization improves Gateway resilience with cluster-wide state sharing, Management DB–independent bootstrap, and automatic master failover.
* New LLM proxy provides an OpenAI-compatible API surface across providers, plus routing controls, token tracking/rate limiting, and prompt guard rails.
* New runtime and webhook logging improves observability for v4 APIs with configurable payload capture, delivery metrics, filtering, and OpenTelemetry tracing.
* Elasticsearch compatibility now includes version 9.2.x alongside existing supported versions.

## Breaking Changes

## New Features

* **Distributed sync with Redis**\
  APIM Gateways can use Redis to synchronize in-memory and deployed state across a cluster (for example APIs, API keys, subscriptions, dictionaries, organizations, and licenses). It introduces deploy/undeploy event-based synchronization with master election and failover, without requiring a full resync. Gateways can bootstrap and serve traffic without direct Management DB access when Redis sync is enabled, and Bridge-based deployments can continue synchronizing even if the Bridge becomes unavailable.

* **LLM proxy (OpenAI-compatible routing across providers)**\
  The LLM proxy supports OpenAI-compatible endpoints for chat completions, responses, and embeddings, with a provider compatibility matrix and documented transformation/constraint behavior (for example role mapping and token-usage reporting). It supports OpenAI SDK configuration via the proxy base URL and API key header, and documents unsupported OpenAI features and related error behavior. Token tracking during streaming can be disabled (with accuracy tradeoffs), and a Token Rate Limit policy can enforce token-based limits over time. It also supports prompt guard rails via text-classification resources to block prompts matching specified content labels (for example toxic or obscene), and can be created using the AI Gateway architecture with provider/model identifiers and model listing support.

* **Runtime and webhook logs for v4 APIs**\
  Gravitee can collect and display runtime logs for v4 Proxy APIs and v4 Message APIs, plus webhook logs for v4 Message APIs that use a webhook entrypoint. Logging is configurable at the Gateway level for modes and captured content (including optional payload capture with a maximum size cap). Runtime logs support filtering (for example by time period, entrypoint, HTTP method, and plan) and OpenTelemetry tracing with optional verbose span detail. Webhook logs include delivery metrics (for example callback URL, response duration, payload size, attempts, and error details), and connection failures can surface as HTTP status 0.

## Updated features

* **Elasticsearch support**\
  APIM's tested compatibility for Elasticsearch now includes version 9.2.x in addition to 7.17.x and 8.16.x.
