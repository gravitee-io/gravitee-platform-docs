# AI Semantic Caching

## Overview

The AI Semantic Caching policy uses vector embeddings to cache AI responses based on semantic similarity rather than exact string matching. This enables intelligent cache hits for semantically equivalent requests, even when the exact wording differs.

## Configuration

The AI Semantic Caching policy supports the following configuration options:

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `modelName` | string | Yes | — | Name of the AI text embedding model resource configured at the API or platform level. |
| `vectorStoreName` | string | Yes | — | Name of the vector store resource configured at the API or platform level. |
| `promptExpression` | string | No | `{#request.content}` | Gravitee EL expression used to extract content from the request for vector embedding generation. |
| `cacheCondition` | string | No | `{#response.status >= 200 && #response.status < 300}` | Gravitee EL expression evaluated during the response phase to determine if the response should be cached. |
| `parameters` | array | No | See below | Metadata parameters attached to cached vectors for filtering and scoping. |

### Parameters

The `parameters` array allows you to attach metadata to each cached vector. Each parameter object supports the following properties:

| Property | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `key` | string | No | — | Name of the metadata parameter. |
| `value` | string | No | — | Value of the metadata parameter. Supports Gravitee EL expressions. |
| `encode` | boolean | No | `false` | When `true`, hashes the value using MurmurHash3 (Base64 encoded) to protect sensitive information. |

**Default parameters value:**

```json
[
  {
    "key": "retrieval_context_key",
    "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
    "encode": true
  }
]
```

### Configuration examples

#### Extract last message from chat completion

Use JSONPath to extract only the last message content from an OpenAI-compatible chat completion request:

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

#### Cache only successful responses

Restrict caching to responses with a `200` status code:

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

Use encoded user IDs to scope cache entries while protecting sensitive information:

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