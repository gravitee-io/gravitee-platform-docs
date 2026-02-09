---
description: Learn how to configure and use the AI Semantic Caching policy for APIM 4.10
---

# AI Semantic Caching

## Overview

{% hint style="warning" %}
**Enterprise Edition only**

This policy is available in Gravitee Enterprise Edition only.
{% endhint %}

The AI Semantic Caching policy enables intelligent caching of LLM responses based on semantic similarity rather than exact query matching. This reduces redundant API calls to LLM providers and improves response times for semantically similar queries.

## Functional and implementation information

The policy uses vector embeddings to determine semantic similarity between queries. When a new query arrives, the policy:

1. Generates an embedding for the incoming query
2. Searches the vector store for semantically similar cached queries
3. Returns the cached response if similarity exceeds the configured threshold
4. Otherwise, forwards the request to the LLM provider and caches the response

## Compatibility matrix

| Plugin Version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.0.x          | 4.10.x                  |

## Configuration

The policy requires configuration of:

- **Vector Store**: The backend storage for embeddings and cached responses
- **Inference Service**: The service used to generate embeddings
- **Similarity Threshold**: The minimum similarity score (0-1) required for a cache hit

## Changelog

### 1.0.0-alpha.1 (2026-01-23)

#### Bug Fixes

* Adjust vector-store API changes and bump Gravitee dependencies ([4a51f4f](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/4a51f4f80eb0d1905b70a91bb557b98285491256))
* Fix tests ([bcadf21](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/bcadf211aae346d090aa00e83ccd58903b4134a8))

#### Features

* Adapt vector store API ([2188076](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/218807623d47acb26b1cff6e7eea608f111b7816))
* Enable policy for LLM Proxy ([9ac20b7](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/9ac20b7a0de8028d0bef165f9d09d28fa2838511))
* First import ([5547a51](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/5547a51a9e1a24429386ebf8bea70456751a2f51))
* Prepare policy for EE ([800d037](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/800d0378f7d9a04faa5e9ee5846ab563e0a0e51d))
* Update inference service version ([#2](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/issues/2)) ([8595387](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/8595387dc9a82b17caffed9bce1985d224885f2d))