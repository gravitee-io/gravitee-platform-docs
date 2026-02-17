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
| [AI Semantic Caching](policy-reference/ai-semantic-caching.md) | ❌ | ✅ | ❌ |

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

**Use cases:**
- **Reduce LLM costs**: Avoid redundant API calls for semantically identical queries (e.g., "What's the weather in Paris?" vs. "Tell me Paris weather").
- **Improve response times**: Serve cached responses instantly when similar queries have been processed before.
- **Optimize non-personalized, deterministic responses**: Best suited for queries where the answer doesn't vary by user context or session state.

For full configuration details, see [AI Semantic Caching policy reference](policy-reference/ai-semantic-caching.md).

## Prerequisites for AI Semantic Caching

Before using the AI Semantic Caching policy, you must configure the following Gravitee resources:

- **AI Text Embedding Model Resource**: Provides vector embeddings (e.g., `gravitee-resource-ai-model-text-embedding`)
- **Vector Store Resource**: Stores and retrieves vectors (e.g., `gravitee-resource-ai-vector-store-redis`)

These resources must be configured at the API or platform level before adding the policy to your flow.

{% hint style="info" %}
**Java 21+ Required**: The AI Semantic Caching policy (version 1.x) requires Java 21 or higher.
{% endhint %}

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

> For the full configuration block ({...), see [Ai Semantic Caching](../../../../4.11/create-and-configure-apis/apply-policies/policy-reference/ai-semantic-caching.md).
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
