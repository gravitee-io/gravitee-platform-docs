---
description: Learn how to configure and use the AI Semantic Cache policy to optimize LLM API calls by caching semantically similar requests using vector embeddings.
---

# AI Semantic Cache

## Prerequisites

Before using this policy, configure the following Gravitee resources:

- **AI Text Embedding Model Resource**: Provides vector embeddings for request content (e.g., `gravitee-resource-ai-model-text-embedding`)
- **Vector Store Resource**: Stores and retrieves vectors with metadata (e.g., `gravitee-resource-ai-vector-store-redis`)

These resources must be configured at the API or platform level before adding the policy to your flow.

## Metadata and filtering

The `parameters` configuration attaches metadata to each cached vector. This metadata is used for:

- **Filtering queries**: Scope caching appropriately (e.g., per API, per user, per plan)
- **Privacy**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

Example use cases:

- Scope cache per API: `{#context.attributes['api']}`
- Scope cache per user: `{#context.attributes['user-id']}`
- Scope cache per plan: `{#context.attributes['plan']}`

## Best practices

1. **Use JSONPath for complex payloads**: When working with structured data like LLM chat completions, extract only the relevant content:
    
    ```
    {#jsonPath(#request.content, '$.messages[-1:].content')}
    ```

2. **Set appropriate cache conditions**: Avoid caching errors or non-deterministic responses:
    
    ```
    {#response.status >= 200 && #response.status < 300}
    ```

3. **Use encoded parameters for sensitive data**: When using user IDs or other PII as metadata filters:
    
    ```json
    {
      "key": "user_context",
      "value": "{#context.attributes['user-id']}",
      "encode": true
    }
    ```

4. **Consider vector store similarity thresholds**: Configure your vector store resource with appropriate similarity thresholds to balance cache hit rate vs accuracy.