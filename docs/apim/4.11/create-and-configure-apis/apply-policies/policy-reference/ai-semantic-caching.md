### Overview

The AI Semantic Caching policy reduces latency and token consumption for LLM proxy APIs by caching responses based on semantic similarity rather than exact string matching. When a request is semantically similar to a previous one (above a configurable threshold), the cached response is returned immediately without invoking the backend LLM.

### How it works

The policy converts incoming prompts into vector embeddings using a configured AI model resource, then queries a vector store to find semantically similar cached entries. If a match exceeds the similarity threshold (default: `0.7` cosine similarity), the cached response is returned. Cache hits save both latency and token usage; the policy records tokens saved via the `cache-hit-tokens-saved` metric.

Administrators can define metadata parameters (e.g., API ID, plan ID, user ID) to partition the cache. Parameters support EL expressions and optional hashing via murmur3_128 with URL-safe Base64 encoding. This ensures cache isolation across tenants or user segments while maintaining privacy for sensitive identifiers.

The `cacheCondition` property (default: `{#response.status >= 200 && #response.status < 300}`) determines whether a backend response is cacheable. Only responses meeting this condition are stored. If embedding creation or vector store writes fail, the policy logs a warning and continues processing without caching.

### Prerequisites

* Gravitee APIM 4.10.1 or later
* Gravitee Node 8.0.0-alpha.3 or later
* An AI model text embedding resource (e.g., OpenAI, ONNX BERT, or custom HTTP endpoint)
* A vector store resource (e.g., Redis or AWS S3)
* LLM proxy API (`type: llm-proxy`, `definitionVersion: 4.0.0`)

### Gateway configuration

#### Cluster plugins

Add Hazelcast plugins to the Helm chart for distributed caching support:

| Property | Value |
|:---------|:------|
| `cluster.plugins[0]` | `https://download.gravitee.io/pre-releases/plugins/node-cache/gravitee-node-cache-plugin-hazelcast/gravitee-node-cache-plugin-hazelcast-8.0.0-alpha.3.zip` |
| `cluster.plugins[1]` | `https://download.gravitee.io/pre-releases/plugins/node-cluster/gravitee-node-cluster-plugin-hazelcast/gravitee-node-cluster-plugin-hazelcast-8.0.0-alpha.3.zip` |

### Vector store resource (Redis)

The following table describes the configuration properties for the Redis vector store resource:

| Property | Description | Example |
|:---------|:------------|:--------|
| `redisConfig.url` | Redis connection URL | `redis://localhost:6379` |
| `redisConfig.username` | Redis username | `default` |
| `redisConfig.index` | Index name for vectors | `semantic-cache-idx` |
| `redisConfig.prefix` | Key prefix for stored vectors | `llm:cache:` |
| `redisConfig.maxPoolSize` | Maximum connection pool size | `6` |
| `properties.embeddingSize` | Dimension of embedding vectors | `1536` |
| `properties.maxResults` | Maximum number of results to return | `1` |
| `properties.similarity` | Similarity metric | `COSINE` |
| `properties.threshold` | Minimum similarity threshold (0.0-1.0) | `0.7` |
| `properties.allowEviction` | Whether to allow cache eviction | `true` |
| `properties.evictTime` | Time before eviction | `10` |
| `properties.evictTimeUnit` | Time unit for eviction | `SECONDS` |

#### AI model text embedding resource

##### OpenAI provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | OpenAI API endpoint | `https://api.openai.com/v1/embeddings` |
| `apiKey` | API authentication key | `sk-...` |
| `organizationId` | Optional organization ID | `org-...` |
| `projectId` | Optional project ID | `proj_...` |
| `modelName` | Model identifier | `text-embedding-3-small` |
| `dimensions` | Embedding dimensions (non-negative) | `1536` |
| `encodingFormat` | Output format: `FLOAT` or `BASE64` | `FLOAT` |

##### Custom HTTP provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | HTTP endpoint URI | `https://custom-model.example.com/embed` |
| `method` | HTTP method | `POST` |
| `headers` | Array of `{name, value}` objects | `[{"name": "Authorization", "value": "Bearer ..."}]` |
| `requestBodyTemplate` | Request body template | `{"input": "{{input}}"}` |
| `inputLocation` | JSONPath to input field | `$.input` |
| `outputEmbeddingLocation` | JSONPath to embedding output | `$.data[0].embedding` |

##### ONNX BERT provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `model.type` | Model type | `XENOVA_ALL_MINILM_L6_V2`, `XENOVA_BGE_SMALL_EN_V1_5`, or `XENOVA_MULTILINGUAL_E5_SMALL` |
| `poolingMode` | Pooling mode for embeddings | (enum value) |
| `padding` | Whether to pad sequences | `true` |

All ONNX models support a maximum sequence length of 512 tokens.

### Creating a semantic caching policy

Add the AI Semantic Caching policy to an LLM proxy API flow:

1. Set `modelName` to the name of your AI model text embedding resource.
2. Set `vectorStoreName` to the name of your vector store resource.
3. Configure `promptExpression` to extract the prompt from the request (default: `{#request.content}`; for OpenAI-style requests, use `{#jsonPath(#request.content, '$.messages[-1:].content')}`).
4. Optionally define `cacheCondition` to control when responses are cached (default: `{#response.status >= 200 && #response.status < 300}`).
5. Add metadata parameters to partition the cache by API, plan, or user (e.g., `{"key": "retrieval_context_key", "value": "{#context.attributes['api']}_{#context.attributes['plan']}", "encode": true}`).

The policy executes on the request phase; cache hits bypass the backend entirely.

### Policy configuration

#### Core properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `modelName` | Name of the AI embedding model resource | `ai-model-text-embedding-resource` |
| `vectorStoreName` | Name of the vector store resource | `vector-store-redis-resource` |
| `promptExpression` | EL expression to extract prompt content | `{#jsonPath(#request.content, '$.messages[-1:].content')}` |
| `cacheCondition` | EL expression to determine if response is cacheable | `{#response.status >= 200}` |

#### Metadata parameters

| Property | Description | Example |
|:---------|:------------|:--------|
| `key` | Parameter name | `retrieval_context_key` |
| `value` | Parameter value (supports EL) | `{#context.attributes['api']}_{#context.attributes['user-id']}` |
| `encode` | Whether to hash the value using murmur3_128 | `true` |

When `encode` is `true`, values are hashed using murmur3_128 and encoded with URL-safe Base64 (without padding).

### Restrictions

* Requires Gravitee APIM 4.10.1 or later and Gravitee Node 8.0.0-alpha.3 or later
* Only available for LLM proxy APIs (`type: llm-proxy`, `definitionVersion: 4.0.0`)
* Policy must be applied in the request phase
* Embedding dimensions must be non-negative
* If embedding creation fails, the policy sets `cache-error` metric to 1 and skips caching
* If vector store writes fail, the policy logs a warning but continues processing
* Cached responses include headers, body, status code, and token count; ensure vector store has sufficient capacity
* Feature flag: `apim-ai-policy-semantic-cache`
