---
description: Best practices for configuring AI Semantic Caching in Gravitee APIM
---

# AI Semantic Caching Best Practices

## Best Practices and Examples

### Extracting Relevant Content

Use JSONPath expressions to extract only the relevant content from complex payloads. For LLM chat completions, extract the last message content instead of caching the entire request:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This approach improves cache hit rates by focusing on semantic similarity of the actual prompt rather than metadata or conversation history.

### Setting Cache Conditions

Configure the `cacheCondition` to avoid caching errors or non-deterministic responses. Cache only successful responses:

```
{#response.status >= 200 && #response.status < 300}
```

For stricter control, cache only specific status codes:

```
{#response.status == 200}
```

### Scoping Cache with Metadata

Use the `parameters` configuration to scope cached vectors appropriately:

**Scope per API:**

```json
{
  "key": "api_context",
  "value": "{#context.attributes['api']}",
  "encode": false
}
```

**Scope per user:**

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

**Scope per plan:**

```json
{
  "key": "plan_context",
  "value": "{#context.attributes['plan']}",
  "encode": false
}
```

**Combined scoping:**

```json
{
  "key": "retrieval_context_key",
  "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
  "encode": true
}
```

### Protecting Sensitive Data

Set `encode: true` when using PII or sensitive values as metadata filters. The policy hashes values using MurmurHash3 (Base64 encoded):

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

### Configuring Similarity Thresholds

Configure your vector store resource with appropriate similarity thresholds to balance cache hit rate and accuracy. Lower thresholds increase cache hits but may return less relevant responses. Higher thresholds improve accuracy but reduce cache effectiveness.

<!-- GAP: Specific threshold values or ranges are not provided in source material -->

### Example: LLM Proxy with JSONPath Extraction

Cache OpenAI-compatible chat completions by extracting the last message content:

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

### Example: Custom Cache Condition

Cache only successful responses with a specific status code:

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
    "parameters": []
  }
}
```