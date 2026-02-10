---
description: Learn how to configure and use the AI Semantic Caching policy to cache AI responses based on semantic similarity
---

# AI Semantic Caching

## Overview

{% hint style="info" %}
**Plugin version**: 1.0.0  
**APIM version**: 4.10+
{% endhint %}

The AI Semantic Caching policy reduces latency and costs for AI-powered APIs by caching responses based on semantic similarity rather than exact string matching. When a request is semantically similar to a previously cached request, the policy returns the cached response instead of forwarding the request to the backend.

This policy uses vector embeddings to represent request content and performs similarity searches against a vector store. It is designed for AI workloads where multiple requests may express the same intent using different wording.

## Compatibility matrix

| Plugin version | APIM version |
|----------------|--------------|
| 1.x            | 4.10+        |

## How it works

The AI Semantic Caching policy operates in two phases:

### Request phase
1. Extracts content from the request using the configured prompt expression
2. Generates a vector embedding using the configured AI Text Embedding Model resource
3. Queries the vector store for semantically similar cached vectors
4. If a match is found above the similarity threshold, returns the cached response and skips backend execution
5. If no match is found, forwards the request to the backend

### Response phase
1. Evaluates the cache condition expression
2. If the condition is true, generates a vector embedding for the request content
3. Stores the vector and response in the vector store with configured metadata parameters
4. Returns the response to the client

## Configuration

The AI Semantic Caching policy requires configuration of resource references and optional parameters to control caching behavior.

### Configuration parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| Embedding model resource | string | Yes | — | Name of the configured AI Text Embedding Model resource used to generate vector embeddings from request content. |
| Vector store resource | string | Yes | — | Name of the configured Vector Store resource used to store and retrieve cached vectors. |
| Prompt expression | string | No | `{#request.content}` | Gravitee EL expression that extracts the content to be vectorized. Use JSONPath for structured payloads (e.g., `{#jsonPath(#request.content, '$.messages[-1:].content')}`). |
| Cache condition | string | No | `{#response.status >= 200 && #response.status < 300}` | Gravitee EL expression evaluated during the response phase. If true, the response is cached. Use this to exclude errors or non-deterministic responses. |
| Parameters | array | No | `[{"key": "retrieval_context_key", "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}", "encode": true}]` | Metadata attached to each cached vector. Used for filtering queries and scoping cache entries. See Parameters table below. |

### Parameters array

Each entry in the `parameters` array defines metadata attached to cached vectors.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| Parameter name | string | No | — | Key name for the metadata field. |
| Parameter value | string | No | — | Gravitee EL expression that resolves to the metadata value (e.g., `{#context.attributes['api']}`). |
| Encode value | boolean | No | `false` | If true, the parameter value is hashed using MurmurHash3 (Base64 encoded) before storage. Use this for sensitive information like user IDs. |

### Configuration examples

#### Cache OpenAI-compatible chat completions

Extract the last message content using JSONPath and scope cache per API:

```json
{
  "modelName": "ai-model-text-embedding-resource",
  "vectorStoreName": "vector-store-redis-resource",
  "promptExpression": "{#jsonPath(#request.content, '$.messages[-1:].content')}",
  "cacheCondition": "{#response.status >= 200 && #response.status < 300}",
  "parameters": [
    {
      "key": "retrieval_context_key",
      "value": "{#context.attributes['api']}",
      "encode": true
    }
  ]
}
```

#### Cache only HTTP 200 responses

Restrict caching to successful responses with a custom status code check:

```json
{
  "modelName": "ai-model-text-embedding-resource",
  "vectorStoreName": "vector-store-redis-resource",
  "promptExpression": "{#request.content}",
  "cacheCondition": "{#response.status == 200}",
  "parameters": []
}
```

#### Scope cache per user with encoded metadata

Use encoded user IDs to filter cached vectors while protecting PII:

```json
{
  "modelName": "ai-model-text-embedding-resource",
  "vectorStoreName": "vector-store-redis-resource",
  "promptExpression": "{#request.content}",
  "cacheCondition": "{#response.status >= 200 && #response.status < 300}",
  "parameters": [
    {
      "key": "user_context",
      "value": "{#context.attributes['user-id']}",
      "encode": true
    }
  ]
}
```

## Prerequisites

Before using this policy, you must configure:

1. **AI Text Embedding Model resource**: Defines the embedding model endpoint and authentication
2. **Vector Store resource**: Defines the vector database connection and similarity threshold

Refer to the [AI Resources](../../configure-ai-resources/) documentation for configuration instructions.

## Use cases

### Reduce AI API costs
Cache responses for semantically similar requests to reduce the number of calls to expensive AI backends.

### Improve response latency
Return cached responses instantly instead of waiting for AI model inference.

### Scope caching by context
Use metadata parameters to isolate cache entries per API, plan, user, or tenant.

## Limitations

- The policy does not support streaming responses
- Cache effectiveness depends on the quality of the embedding model and similarity threshold configuration
- Cached responses may become stale if the AI model behavior changes over time

## Error handling

If the embedding model or vector store is unavailable during the request phase, the policy forwards the request to the backend without caching. If the resources are unavailable during the response phase, the response is returned without caching.

## Related resources

- [AI Resources Configuration](../../configure-ai-resources/)
- [Gravitee Expression Language](../../../gravitee-expression-language/)
- [Vector Store Resources](../../configure-ai-resources/vector-store-resources/)