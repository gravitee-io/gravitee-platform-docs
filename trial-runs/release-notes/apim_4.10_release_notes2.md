---
description: Documentation about apim 4.10 in the context of APIs.
---

# APIM 4.10

## Release Date: 

## Highlights

* Distributed Sync With Redis enables resilient Gateway state synchronization with master failover support.
* Expanded runtime and webhook logging adds filtering, sampling, and payload controls for v4 APIs.
* New LLM Proxy capabilities introduce OpenAI-compatible routing, SDK support, and governance controls.
* Updated Elasticsearch compatibility adds support for version 9.2.x.

## Breaking Changes

## New Features

* **Distributed Sync With Redis**\
  APIM Gateways can use Redis for distributed synchronization of deployments, dictionaries, organizations, and licenses across a cluster. Distributed sync introduces state tracking, bootstrap support for new Gateways, master election with failover, and continued API serving during Bridge outages without requiring a full resynchronization.

* **Runtime And Webhook Logging Enhancements**\
  v4 Proxy and v4 Message APIs support expanded runtime and webhook logging with configurable logging modes, phases, and content capture. Enhancements include filtering by time period, HTTP method, and plan, windowed sampling to manage bursts of messages, separate webhook logging for callbacks, delivery metrics with payload capture, and limits on maximum logged payload size.

* **LLM Proxy Capabilities**\
  Gravitee introduces an LLM Proxy with OpenAI-compatible routing between consumers and providers, configurable endpoints, and a defined compatibility matrix. The feature set includes SDK support with API key headers, model listing, token-based rate limiting, prompt guard rails for text classification, and documented unsupported features and error behaviors.

## Updated features

* **Elasticsearch Compatibility**\
  APIM’s tested Elasticsearch compatibility now includes version 9.2.x in addition to 7.17.x and 8.16.x.
