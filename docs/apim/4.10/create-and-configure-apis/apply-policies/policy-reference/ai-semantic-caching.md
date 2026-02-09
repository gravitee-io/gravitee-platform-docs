---
description: Learn how to configure and use the AI Semantic Caching policy to cache LLM responses based on semantic similarity
---

# AI Semantic Caching

## Overview

The AI Semantic Caching policy enables intelligent caching of API responses based on semantic similarity rather than exact string matching. This is particularly useful for LLM (Large Language Model) APIs where different prompts may have similar meanings and can share cached responses.

The policy works by:
1. Extracting the relevant content from incoming requests using configurable expressions
2. Generating vector embeddings using an AI model resource
3. Searching for semantically similar cached responses in a vector store
4. Returning cached responses when similarity thresholds are met
5. Caching new responses with their vector embeddings for future requests

## Compatibility matrix

| Plugin version | APIM version |
| -------------- | ------------ |
| 1.x            | 4.10+        |

## Configuration

The policy requires configuration of an AI model resource for generating embeddings and a vector store resource for caching.

### Policy configuration

| Property | Required | Description | Type | Default |
| -------- | -------- | ----------- | ---- | ------- |
| `modelName` | Yes | Name of the AI model resource to use for generating embeddings | string | - |
| `vectorStoreName` | Yes | Name of the vector store resource to use for caching | string | - |
| `promptExpression` | No | Expression Language (EL) expression to extract the relevant content from the request. If not specified, the entire request body is used. | string | `{#request.content}` |
| `cacheCondition` | No | Expression Language (EL) condition that must evaluate to `true` for the response to be cached. Use this to avoid caching errors or non-deterministic responses. | string | - |
| `parameters` | No | List of metadata parameters to attach to cached vectors. These can be used to scope cache lookups by API, user, plan, or other contextual attributes. | array | - |

#### Parameters configuration

Each parameter in the `parameters` array supports:

| Property | Required | Description | Type | Default |
| -------- | -------- | ----------- | ---- | ------- |
| `key` | Yes | Metadata key name | string | - |
| `value` | Yes | Expression Language (EL) expression to compute the metadata value | string | - |
| `encode` | No | Whether to hash the value using MurmurHash3 (Base64 encoded). Useful for protecting sensitive data like user IDs. | boolean | `false` |

### Resource configuration

This policy requires two types of resources to be configured:

1. **AI Model Resource**: Provides the embedding model for generating vector representations of text
2. **Vector Store Resource**: Stores and retrieves cached vectors with their associated responses

Refer to the AI Model and Vector Store resource documentation for configuration details.

## Best practices

### General

* **Use JSONPath for complex payloads**: When working with structured data like LLM chat completions, extract only the relevant content using the `promptExpression` field. This ensures the embedding model processes only the semantically meaningful portion of the request.
* **Set appropriate cache conditions**: Avoid caching errors or non-deterministic responses by configuring the `cacheCondition` field. Only cache responses that meet your quality criteria.
* **Use encoded parameters for sensitive data**: When using user IDs or other PII as metadata filters, enable the `encode` option to hash values using MurmurHash3 (Base64 encoded). This protects sensitive information while maintaining cache scoping.
* **Configure vector store similarity thresholds**: Work with your vector store resource configuration to set appropriate similarity thresholds. Balance cache hit rate against semantic accuracy based on your use case requirements.
* **Scope cache appropriately**: Use the `parameters` configuration to attach metadata that filters cached vectors by API, user, plan, or other contextual attributes. This prevents cache pollution across different contexts.

### Limitations

* The quality of semantic matching depends on the embedding model and vector store configuration.
* Not suitable for APIs with highly dynamic or personalized responses.

## Examples

### Example 1: Cache OpenAI-compatible chat completions

This example demonstrates caching for an LLM proxy API that forwards requests to an OpenAI-compatible endpoint. The policy extracts the last message content from the chat completion request using JSONPath, generates a vector embedding, and caches successful responses.

**Configuration:**

```json
{
  "name": "AI Semantic Caching",
  "enabled": true,
  "policy": "ai-semantic-caching",
  "configuration": {
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
}
```

**How it works:**

1. The `promptExpression` uses JSONPath to extract the content of the last message in the `messages` array from the request body.
2. The policy generates a vector embedding for this extracted content.
3. The vector store searches for similar cached vectors using the `retrieval_context_key` metadata filter (scoped to the API).
4. If a similar vector is found, the cached response is returned immediately.
5. If no match is found, the request is forwarded to the backend.
6. The `cacheCondition` ensures only successful responses (status 200-299) are cached.

### Example 2: Scope cache per user with encoded metadata

This example demonstrates caching scoped to individual users while protecting user IDs through encoding. This is useful for APIs where responses are user-specific but semantically similar requests should still benefit from caching.

**Configuration:**

```json
{
  "name": "AI Semantic Caching",
  "enabled": true,
  "policy": "ai-semantic-caching",
  "configuration": {
    "modelName": "ai-model-text-embedding-resource",
    "vectorStoreName": "vector-store-redis-resource",
    "promptExpression": "{#request.content}",
    "cacheCondition": "{#response.status == 200}",
    "parameters": [
      {
        "key": "user_context",
        "value": "{#context.attributes['user-id']}",
        "encode": true
      }
    ]
  }
}
```

**How it works:**

1. The `promptExpression` uses the entire request body as the input for vector embedding.
2. The `parameters` configuration attaches a `user_context` metadata field with the user ID from the request context.
3. The `encode: true` option hashes the user ID using MurmurHash3 (Base64 encoded) before storing it as metadata.
4. The vector store searches for similar cached vectors filtered by the encoded user ID.
5. Only responses with status code 200 are cached, as specified by the `cacheCondition`.

### Example 3: Multi-dimensional cache scoping

This example demonstrates caching scoped by multiple dimensions (API, plan, and user) to ensure cache isolation across different contexts.

**Configuration:**

```json
{
  "name": "AI Semantic Caching",
  "enabled": true,
  "policy": "ai-semantic-caching",
  "configuration": {
    "modelName": "ai-model-text-embedding-resource",
    "vectorStoreName": "vector-store-redis-resource",
    "promptExpression": "{#request.content}",
    "cacheCondition": "{#response.status >= 200 && #response.status < 300}",
    "parameters": [
      {
        "key": "retrieval_context_key",
        "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
        "encode": true
      }
    ]
  }
}
```

**How it works:**

1. The `parameters` configuration combines API, plan, and user ID into a single composite metadata key.
2. The `encode: true` option hashes the composite value to protect sensitive information.
3. The vector store searches for similar cached vectors filtered by this composite key.
4. This ensures cache isolation: responses are only reused when the API, plan, and user all match.
5. Successful responses (status 200-299) are cached for future requests with the same context.