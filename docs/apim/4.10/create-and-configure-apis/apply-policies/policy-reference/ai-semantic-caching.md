### Overview

The AI Semantic Caching policy reduces LLM costs and latency by caching responses to semantically similar prompts. When a request arrives, the policy extracts the prompt using an EL expression, generates a vector embedding via a configured AI model resource, and queries a vector store for similar embeddings. If the similarity score exceeds the configured threshold, the cached response is returned immediately without invoking the backend LLM.

### Prerequisites

Before configuring the AI Semantic Caching policy, ensure the following requirements are met:

* Gravitee APIM 4.10.1 or later
* An AI model resource configured for text embedding
* A vector store resource (Redis or AWS S3)
* LLM Proxy API type enabled

### Configuration

Add the AI Semantic Caching policy to the request phase of your LLM Proxy API flow.

#### Policy properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `modelName` | Name of the AI embedding model resource (required) | `ai-model-text-embedding-resource` |
| `vectorStoreName` | Name of the vector store resource (required) | `vector-store-redis-resource` |
| `promptExpression` | EL expression to extract content to embed (optional, default: `{#request.content}`) | `{#jsonPath(#request.content, '$.messages[-1:].content')}` |
| `cacheCondition` | EL expression determining if response is cacheable (optional, default: `{#response.status >= 200 && #response.status < 300}`) | `{#response.status >= 200}` |
| `parameters` | Array of metadata key-value pairs (supports EL expressions) | See Parameter Object table |

#### Parameter object

| Property | Description | Example |
|:---------|:------------|:--------|
| `key` | Metadata field name | `retrieval_context_key` |
| `value` | EL expression to extract value | `{#context.attributes['api']}_{#context.attributes['plan']}` |
| `encode` | Whether to hash the value using murmur3_128 | `true` |

#### Configuration steps

1. Add the AI Semantic Caching policy to the request phase of your LLM Proxy API flow.
2. Configure the `modelName` property with the name of your AI embedding model resource.
3. Configure the `vectorStoreName` property with the name of your vector store resource.
4. Set the `promptExpression` property to extract the prompt content from the request. For example, `{#jsonPath(#request.content, '$.messages[-1:].content')}` extracts the last message content from a JSON request body.
5. (Optional) Configure the `cacheCondition` property to control when responses are cached. The default condition caches responses with status codes between 200 and 299.
6. (Optional) Add metadata parameters to partition the cache by API, plan, or user. For example, set `key` to `retrieval_context_key` and `value` to `{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}` to isolate cache entries by API, plan, and user.

### Metadata filtering

Each cached entry includes metadata parameters extracted via EL expressions. The `retrieval_context_key` parameter enables cache partitioning by API, plan, or user. When present in query metadata, it filters vector search results to ensure cache isolation across tenants or contexts. Metadata values can be hashed using murmur3_128 to reduce storage size by setting the `encode` property to `true`.

### Cache eviction

Vector stores support time-based eviction when `allowEviction` is enabled in the vector store resource configuration. The policy calculates an `expireAt` timestamp by adding `evictTime` (in the specified `evictTimeUnit`) to the current time. Expired entries are removed automatically by the vector store implementation.

### Metrics

The AI Semantic Caching policy emits the following metrics:

| Metric Name | Type | Description |
|:------------|:-----|:------------|
| `long_semantic-caching_cache-hit` | long | Count of cache hits (value: 1) |
| `double_semantic-caching_cache-hit-score` | double | Similarity score of cache hit |
| `long_semantic-caching_cache-hit-tokens-saved` | long | Number of tokens saved by cache hit (sum of sent and received tokens) |
| `long_semantic-caching_cache-miss` | long | Count of cache misses (value: 1) |
| `long_semantic-caching_cache-error` | long | Count of cache errors (value: 1) |

### Restrictions

* Requires Gravitee APIM 4.10.1 or later
* Requires LLM Proxy API type
* Requires an AI model resource configured for text embedding
* Requires a vector store resource (Redis or AWS S3)
* OpenAI embedding dimensions must be non-negative
* AWS S3 bucket and index validation: 404 errors are logged as warnings
* Redis HNSW parameters (`M`, `efConstruction`, `efRuntime`) must be configured in the vector store resource
* Cache eviction requires `allowEviction` to be enabled in the vector store resource configuration
* EL expressions in `promptExpression`, `cacheCondition`, and parameter `value` fields must be valid
* Cache write errors are logged as warnings and do not block the request
* Cache read errors are logged as warnings and the request proceeds to the backend LLM
