## Overview

Cache policies enable you to cache upstream responses (content or headers) to eliminate the need for subsequent requests to the backend. Cache policies can be applied at the API or plan level.

{% hint style="info" %}
Cache policies are compatible with all Gravitee API types.
{% endhint %}

## Supported cache policies

Gravitee supports the following cache policies:

| Policy | v2 API | v4 proxy API | v4 message API |
| --- | --- | --- | --- |
| [Cache](cache.md) | ✅ | ✅ | ✅ |
| [Cache Redis](policy-reference/cache-redis.md) | ✅ | ✅ | ✅ |
| [AI Semantic Caching](../../../../4.11/create-and-configure-apis/apply-policies/policy-reference/ai-semantic-caching.md) | ❌ | ✅ (LLM Proxy only) | ❌ |

## Cache policy comparison

### Traditional cache policies

Traditional cache policies (Cache and Cache Redis) match requests using exact keys derived from request attributes such as URL, headers, or body hash. A cached response is returned only when the incoming request produces an identical cache key. Any variation in wording, parameter order, or formatting results in a cache miss, triggering a new backend call.

**Use cases:**
- General-purpose caching for REST APIs
- Scenarios where request structure is predictable and consistent
- Applications requiring deterministic cache key matching

### AI Semantic Caching

AI Semantic Caching is a specialized caching strategy designed for LLM proxy APIs. Instead of exact key matching, it uses vector embeddings to identify semantically equivalent queries. Requests that convey the same meaning—even when phrased differently—return the same cached response.

**How it differs from traditional caching:**
- **Traditional cache policies**: Match requests using exact keys (e.g., URL, headers, body hash). A slight variation in wording results in a cache miss.
- **AI Semantic Caching**: Converts request content into vector embeddings and compares them using similarity scoring. Semantically equivalent queries return the same cached response, regardless of phrasing.

**Key benefits:**
- **Reduce LLM costs**: Avoid redundant API calls for semantically identical queries (e.g., "What's the weather in Paris?" vs. "Tell me Paris weather").
- **Improve response times**: Serve cached responses instantly when similar queries have been processed before.
- **Optimize non-personalized, deterministic responses**: Best suited for queries where the answer doesn't vary by user context or session state.

**Compatible API types:**

The AI Semantic Caching policy is compatible with the following API type:

- **LLM_PROXY**: Cache OpenAI-compatible chat completions by extracting the last message content using JSONPath. Example configuration:
  ```
  promptExpression: {#jsonPath(#request.content, '$.messages[-1:].content')}
  ```

For full configuration details, see [AI Semantic Caching policy reference](../../../../4.11/create-and-configure-apis/apply-policies/policy-reference/ai-semantic-caching.md).

## Prerequisites for AI Semantic Caching

Before using the AI Semantic Caching policy, you must configure the following Gravitee resources:

- **AI Text Embedding Model Resource**: Provides vector embeddings (e.g., `gravitee-resource-ai-model-text-embedding`)
- **Vector Store Resource**: Stores and retrieves vectors (e.g., `gravitee-resource-ai-vector-store-redis`)

These resources must be configured at the API or platform level before adding the policy to your flow.

{% hint style="info" %}
**Java 21+ Required**: The AI Semantic Caching policy (version 1.x) requires Java 21 or higher.
{% endhint %}

## Best practices for semantic caching

When implementing semantic caching for LLM workloads, follow these guidelines to optimize performance and accuracy:

1. **Use JSONPath for complex payloads**: Extract only relevant content from structured data (e.g., `{#jsonPath(#request.content, '$.messages[-1:].content')}` for chat completions).
2. **Set appropriate cache conditions**: Avoid caching errors or non-deterministic responses (e.g., `{#response.status >= 200 && #response.status < 300}`).
3. **Use encoded parameters for sensitive data**: Protect PII such as user IDs by setting `encode: true` in metadata filters.
4. **Configure vector store similarity thresholds**: Balance cache hit rate vs accuracy by adjusting similarity thresholds in your vector store resource.

**Limitations:**
- Not suitable for APIs with highly dynamic or personalized responses.
- The quality of semantic matching depends on the embedding model and vector store configuration.

## Expression Language (EL) examples

The AI Semantic Caching policy uses Gravitee Expression Language (EL) to configure dynamic behavior. The following examples demonstrate common patterns for `promptExpression`, `cacheCondition`, and `parameters.value`.

### promptExpression

The `promptExpression` extracts content from the request to generate the semantic vector. The default value is `{#request.content}`, which uses the entire request body.

**JSONPath extraction for chat completions:**

When working with structured payloads (e.g., OpenAI-compatible chat completions), use JSONPath to extract only the relevant content:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This expression extracts the content of the last message in the `messages` array, ignoring metadata and previous conversation history.

### cacheCondition

The `cacheCondition` determines whether a response should be cached. The default value is:

```
{#response.status >= 200 && #response.status < 300}
```

This caches only successful responses (HTTP 2xx status codes).

**Custom condition for specific status codes:**

```
{#response.status == 200}
```

### parameters.value

The `parameters` array attaches metadata to cached vectors for filtering and scoping. Use EL to reference context attributes:

**Scope cache per API:**

```json
{
  "key": "api_context",
  "value": "{#context.attributes['api']}",
  "encode": false
}
```

**Scope cache per user (with encoding for privacy):**

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

**Scope cache per plan:**

```json
{
  "key": "plan_context",
  "value": "{#context.attributes['plan']}",
  "encode": false
}
```

**Combined metadata for multi-dimensional scoping:**

```json
{
  "key": "retrieval_context_key",
  "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
  "encode": true
}
```

#### Privacy protection with encoded parameters

The `encode` parameter provides privacy protection for sensitive metadata values. When set to `true`, the policy hashes the parameter value using MurmurHash3 (Base64 encoded) before storing it in the vector store.

**Use case**: Protect personally identifiable information (PII) such as user IDs when using them as metadata filters for cache scoping.

This ensures sensitive values are never stored in plain text while maintaining the ability to filter cached vectors by user context.

## Additional resources

For detailed configuration instructions and examples, refer to the individual policy reference pages linked in the table above.

### Overview

The AI Semantic Caching policy enables semantic caching of responses based on the similarity of request content. Unlike traditional caching mechanisms that rely on exact text matching, this policy uses vector embeddings to identify semantically equivalent queries. When a request arrives, the policy converts it into a vector representation and searches for similar cached vectors. If a match is found, the cached response is returned immediately, reducing Large Language Model (LLM) token consumption and API latency.

The policy integrates with Gravitee AI resources (text embedding models and vector stores) and provides flexible caching decisions through Gravitee Expression Language (EL) expressions.

### How it works

The AI Semantic Caching policy operates in two phases:

#### Request phase

When a request arrives, the policy:

1. Extracts content using the `promptExpression` (default: entire request body)
2. Generates a vector embedding using the configured embedding model
3. Searches the vector store for similar cached vectors using metadata filters
4. If a similar vector is found (based on similarity threshold), returns the cached response
5. If no match is found, forwards the request to the backend

#### Response phase

After receiving the backend response, the policy:

1. Evaluates the `cacheCondition` to determine if the response should be cached
2. If cacheable, stores the response (status, headers, body) with the vector and metadata in the vector store

### Prerequisites

Before using this policy, you must configure the following Gravitee resources:

- **AI Text Embedding Model Resource**: Provides vector embeddings (e.g., `gravitee-resource-ai-model-text-embedding`)
- **Vector Store Resource**: Stores and retrieves vectors (e.g., `gravitee-resource-ai-vector-store-redis`)

These resources must be configured at the API or platform level before adding the policy to your flow.

### Metadata and filtering

The `parameters` configuration allows you to attach metadata to each cached vector. This metadata is used for:

- **Filtering queries**: Ensure caching is scoped appropriately (e.g., per API, per user, per plan)
- **Privacy**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

Example use cases:

- Scope cache per API: `{#context.attributes['api']}`
- Scope cache per user: `{#context.attributes['user-id']}`
- Scope cache per plan: `{#context.attributes['plan']}`

### Phases

The `ai-semantic-caching` policy can be applied to the following API types and flow phases.

#### Compatible API types

* `LLM PROXY`

#### Supported flow phases

* Request

### Compatibility matrix

| Plugin version | APIM | Java version |
| --- | --- | --- |
| 1.x | 4.11.x and above | 21+ |

### Configuration options

| Name<br>`json name` | Type<br>`constraint` | Mandatory | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| Cache condition<br>`cacheCondition` | string |  | `{#response.status >= 200 && #response.status < 300}` | Expression Language (EL) condition to determine if the response should be cached |
| Embedding model resource<br>`modelName` | string | ✅ |  | Name of the AI Text Embedding Model Resource |
| Parameters<br>`parameters` | array |  | `[{"encode": true, "key": "retrieval_context_key", "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}"}]` | Metadata parameters to attach to cached vectors (using EL). See "Parameters" section. |
| Prompt expression<br>`promptExpression` | string |  | `{#request.content}` | Expression Language (EL) expression to extract content from the request |
| Vector store resource<br>`vectorStoreName` | string | ✅ |  | Name of the Vector Store Resource |

#### Parameters (Array)

| Name<br>`json name` | Type<br>`constraint` | Mandatory | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| Encode value<br>`encode` | boolean |  |  | Encode the value using MurmurHash3 (Base64) for privacy protection |
| Parameter name<br>`key` | string |  |  | Name of the metadata parameter |
| Parameter value<br>`value` | string |  |  | Value of the parameter (using EL) |

### Examples

#### LLM Proxy with JSONPath extraction

Cache OpenAI-compatible chat completions by extracting the last message content:

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "LLM_PROXY",
    "name": "AI Semantic Caching example API",
    "flows": [
      {
        "name": "All plans flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "methods": []
          }
        ],
        "request": [
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
        ]
      }
    ]
  }
}
```

#### Custom cache condition

Cache only successful responses with custom status code check:

```json
{
  "api": {
    "definitionVersion": "V4",
    "type": "LLM_PROXY",
    "name": "AI Semantic Caching example API",
    "flows": [
      {
        "name": "All plans flow",
        "enabled": true,
        "selectors": [
          {
            "type": "HTTP",
            "methods": []
          }
        ],
        "request": [
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
        ]
      }
    ]
  }
}
```

### Changelog

#### 1.0.0-alpha.1 (2026-01-23)

##### Bug Fixes

* adjust vector-store api changes + bump gravitee deps ([4a51f4f](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/4a51f4f80eb0d1905b70a91bb557b98285491256))
* tests ([bcadf21](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/bcadf211aae346d090aa00e83ccd58903b4134a8))

##### Features

* adapt vector store api ([2188076](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/218807623d47acb26b1cff6e7eea608f111b7816))
* enable policy for LLM proxy ([9ac20b7](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/9ac20b7a0de8028d0bef165f9d09d28fa2838511))
* first import ([5547a51](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/5547a51a9e1a24429386ebf8bea70456751a2f51))
* prepare policy for EE ([800d037](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/800d0378f7d9a04faa5e9ee5846ab563e0a0e51d))
* update inference service version ([#2](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/issues/2)) ([8595387](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/8595387dc9a82b17caffed9bce1985d224885f2d))

### Policies that use this resource

The AI Text Embedding Model resource is consumed by the following policies:

- [AI Semantic Caching](../../../../4.11/create-and-configure-apis/apply-policies/policy-reference/ai-semantic-caching.md)

For full configuration details, see [AI Semantic Caching policy reference](../../../../4.11/create-and-configure-apis/apply-policies/policy-reference/ai-semantic-caching.md).
