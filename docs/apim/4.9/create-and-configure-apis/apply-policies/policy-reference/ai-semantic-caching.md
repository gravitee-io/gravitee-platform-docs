---
description: Cache LLM responses using semantic similarity to reduce costs and improve performance
---

# AI Semantic Caching

## Overview

The AI Semantic Caching policy enables intelligent caching of Large Language Model (LLM) responses based on semantic similarity rather than exact request matching. By leveraging vector embeddings and similarity search, this policy can identify when a new request is semantically similar to a previously cached request and return the cached response, significantly reducing API costs and improving response times.

Unlike traditional caching mechanisms that require exact matches, semantic caching understands the meaning and context of requests. For example, "What's the weather like today?" and "How's the weather right now?" would be recognized as semantically similar and could share a cached response.

## Functional and implementation information

The AI Semantic Caching policy operates through the following workflow:

1. **Request processing**: When a request arrives, the policy extracts the relevant content using the configured `requestContent` expression (typically using JSONPath for structured payloads)
2. **Vector embedding generation**: The extracted content is sent to the configured embedding model to generate a vector representation
3. **Similarity search**: The generated vector is compared against cached vectors in the vector store using the configured similarity threshold
4. **Cache hit/miss handling**:
   - **Cache hit**: If a semantically similar cached vector is found, the cached response is returned immediately
   - **Cache miss**: The request proceeds to the backend, and the response is cached along with its vector embedding for future requests
5. **Metadata filtering**: Optional metadata parameters can be used to scope cache lookups (e.g., per user, per API, per plan)

### Key components

- **Embedding model**: Converts text into vector representations that capture semantic meaning
- **Vector store**: Stores and retrieves vector embeddings with similarity search capabilities
- **Metadata filters**: Optional key-value pairs that scope cache lookups to specific contexts

## Configuration

### Phases

The policy can be applied to the following request and response phases:

- `onRequest`
- `onResponse`

### Options

You can configure the AI Semantic Caching policy with the following options:

<table data-full-width="false">
  <thead>
    <tr>
      <th width="150">Property</th>
      <th width="100" data-type="checkbox">Required</th>
      <th width="250">Description</th>
      <th width="150">Type</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>scope</code></td>
      <td>true</td>
      <td>The execution scope (<code>REQUEST</code> or <code>RESPONSE</code>)</td>
      <td>string</td>
      <td><code>REQUEST</code></td>
    </tr>
    <tr>
      <td><code>embeddingModel</code></td>
      <td>true</td>
      <td>The embedding model resource to use for generating vector embeddings</td>
      <td>string</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td><code>vectorStore</code></td>
      <td>true</td>
      <td>The vector store resource to use for storing and retrieving cached vectors</td>
      <td>string</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td><code>requestContent</code></td>
      <td>true</td>
      <td>Expression Language (EL) expression to extract the content from the request that will be used for semantic matching</td>
      <td>string</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td><code>cacheCondition</code></td>
      <td>false</td>
      <td>EL expression that determines whether a response should be cached. Only responses where this expression evaluates to <code>true</code> will be stored</td>
      <td>string</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td><code>parameters</code></td>
      <td>false</td>
      <td>List of metadata key-value pairs used to filter cached vectors. Supports EL expressions for dynamic values</td>
      <td>array</td>
      <td><code>[]</code></td>
    </tr>
    <tr>
      <td><code>parameters[].key</code></td>
      <td>true</td>
      <td>The metadata key name</td>
      <td>string</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td><code>parameters[].value</code></td>
      <td>true</td>
      <td>The metadata value. Supports EL expressions</td>
      <td>string</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td><code>parameters[].encode</code></td>
      <td>false</td>
      <td>Whether to hash the value using MurmurHash3 (Base64 encoded) before storing. Useful for sensitive data like user IDs</td>
      <td>boolean</td>
      <td><code>false</code></td>
    </tr>
  </tbody>
</table>

## Examples

### Basic semantic caching for LLM chat completions

This example demonstrates semantic caching for an OpenAI-compatible chat completion API. The policy extracts the last message content from the request and caches successful responses.

```json
{
  "name": "AI Semantic Caching",
  "description": "Cache LLM responses based on semantic similarity",
  "enabled": true,
  "policy": "ai-semantic-caching",
  "configuration": {
    "scope": "REQUEST_RESPONSE",
    "embeddingModel": "openai-embeddings",
    "vectorStore": "pgvector-store",
    "requestContent": "{#jsonPath(#request.content, '$.messages[-1:].content')}",
    "cacheCondition": "{#response.status == 200}"
  }
}
```

### Scoped caching per user and API

This example adds metadata filters to scope the cache per user and API, ensuring that cached responses are only returned to the appropriate context. User IDs are hashed for privacy.

```json
{
  "name": "AI Semantic Caching with User Scoping",
  "description": "Cache LLM responses per user and API",
  "enabled": true,
  "policy": "ai-semantic-caching",
  "configuration": {
    "scope": "REQUEST_RESPONSE",
    "embeddingModel": "openai-embeddings",
    "vectorStore": "pgvector-store",
    "requestContent": "{#jsonPath(#request.content, '$.messages[-1:].content')}",
    "cacheCondition": "{#response.status >= 200 && #response.status < 300}",
    "parameters": [
      {
        "key": "api_id",
        "value": "{#context.attributes['api']}"
      },
      {
        "key": "user_context",
        "value": "{#context.attributes['user-id']}",
        "encode": true
      }
    ]
  }
}
```

### Multi-dimensional cache scoping

This example demonstrates fine-grained cache control by combining API, plan, and user context into a single metadata key.

```json
{
  "name": "AI Semantic Caching with Multi-dimensional Scoping",
  "description": "Cache LLM responses with combined context filtering",
  "enabled": true,
  "policy": "ai-semantic-caching",
  "configuration": {
    "scope": "REQUEST_RESPONSE",
    "embeddingModel": "openai-embeddings",
    "vectorStore": "pgvector-store",
    "requestContent": "{#jsonPath(#request.content, '$.messages[-1:].content')}",
    "cacheCondition": "{#response.status == 200}",
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

## Best practices

### Use JSONPath for complex payloads

When working with structured data like LLM chat completions, extract only the relevant content using JSONPath expressions. This ensures that only the meaningful parts of the request are used for semantic matching.

For example, to extract the last message content from an OpenAI-compatible chat completion request:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This approach improves cache accuracy by focusing on the actual prompt rather than the entire request structure.

### Set appropriate cache conditions

Avoid caching errors or non-deterministic responses by using the `cacheCondition` configuration. Only cache responses that meet specific criteria.

For example, to cache only successful responses:

```
{#response.status >= 200 && #response.status < 300}
```

Or to cache only HTTP 200 responses:

```
{#response.status == 200}
```

This prevents error responses from being stored and returned to subsequent requests.

### Use encoded parameters for sensitive data

When using user IDs, personally identifiable information (PII), or other sensitive data as metadata filters, enable the `encode` option. This hashes the value using MurmurHash3 (Base64 encoded) before storing it in the vector store.

For example, to scope cache per user while protecting user IDs:

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

This ensures that sensitive information is not stored in plain text while still allowing effective cache scoping.

### Scope cache appropriately with metadata

Use the `parameters` configuration to attach metadata that filters cached vectors. This ensures that cached responses are returned only to the appropriate context.

Common scoping patterns:

- **Per API**: Use `{#context.attributes['api']}` to prevent cache sharing across different APIs
- **Per user**: Use `{#context.attributes['user-id']}` to ensure users only receive their own cached responses
- **Per plan**: Use `{#context.attributes['plan']}` to differentiate caching behavior based on subscription plans
- **Combined scoping**: Use multiple parameters together for fine-grained control

For example, to scope cache per API, plan, and user:

```json
{
  "key": "retrieval_context_key",
  "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
  "encode": true
}
```

### Configure vector store similarity thresholds

The similarity threshold determines how closely a new request must match a cached vector to trigger a cache hit. Configure this threshold in your vector store resource to balance cache hit rate and accuracy.

- **Lower thresholds** (e.g., 0.7): More permissive matching, higher cache hit rate, but may return less accurate results
- **Higher thresholds** (e.g., 0.9): Stricter matching, more accurate results, but lower cache hit rate

Adjust the threshold based on your use case and the embedding model's characteristics.

## Limitations

### Embedding model quality

The quality of semantic matching depends on the embedding model used. Different models have varying capabilities for understanding context and semantic similarity. Choose an embedding model that is appropriate for your domain and use case.

### Vector store configuration

The effectiveness of the policy depends on the vector store's similarity search algorithm and configuration. Ensure that your vector store resource is properly configured with appropriate similarity metrics and indexing strategies.

### Dynamic and personalized responses

The AI Semantic Caching policy is not suitable for APIs that return highly dynamic or personalized responses. Caching works best when:

- Responses are deterministic for similar inputs
- Content does not change frequently based on external factors
- Personalization can be captured through metadata filters

For APIs with real-time data, user-specific content that cannot be scoped through metadata, or responses that vary significantly for semantically similar requests, consider alternative caching strategies or disable caching for those endpoints.

### Performance considerations

Generating vector embeddings and performing similarity searches introduce latency. While caching reduces backend load for cache hits, the initial request and cache miss scenarios incur additional processing time. Monitor performance metrics to ensure the policy provides net benefits for your use case.