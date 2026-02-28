### Overview

The AI Semantic Caching policy reduces LLM API costs and latency by reusing responses for semantically similar requests. Instead of exact string matching, the policy uses vector embeddings to identify similar prompts and return cached responses without invoking the backend LLM. This Enterprise Edition feature integrates with Redis or AWS S3 vector stores and supports multiple embedding model providers.

### Key concepts

#### Semantic similarity matching

The policy generates vector embeddings from request prompts and queries a vector store for similar cached responses. When a match exceeds the configured similarity threshold, the cached response is returned without invoking the backend LLM. Similarity is measured using configurable metrics (cosine or euclidean) against stored embedding vectors.

#### Metadata filtering

Each cached response stores metadata parameters alongside its embedding vector. These parameters enable multi-tenant caching by filtering results based on context (e.g., API key, user ID, organization). Parameters can be encoded using MurmurHash3 to index sensitive values securely.

#### Cache eviction

Vector stores support automatic eviction when `allowEviction` is enabled. The policy calculates an `expireAt` timestamp (current time + configured eviction time) and stores it in vector metadata. Redis handles automatic expiration based on this timestamp.

### Prerequisites

- Gravitee APIM Enterprise Edition
- Deployed AI embedding model resource (ONNX BERT, OpenAI, or custom HTTP endpoint)
- Deployed vector store resource (Redis or AWS S3)
- Redis 8.4.0+ or AWS S3 bucket with appropriate access credentials
- LLM proxy API configured to track token usage via `llmproxy.usage.sent.token` and `llmproxy.usage.received.token` attributes

### Gateway configuration

#### AI Semantic Caching policy

Configure the policy in your API flow using these properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `modelName` | Name of the AI embedding model resource (required) | `openai-embeddings` |
| `vectorStoreName` | Name of the vector store resource (required) | `redis-vectors` |
| `promptExpression` | EL expression to extract content for embedding | `{#request.content}` |
| `cacheCondition` | EL expression determining if response is cacheable | `{#response.status >= 200 && #response.status < 300}` |
| `parameters` | Array of metadata key-value pairs | See Parameter configuration below |

#### Parameter configuration

Each parameter defines metadata stored with cached vectors:

| Property | Description | Example |
|:---------|:------------|:--------|
| `key` | Metadata field name | `retrieval_context_key` |
| `value` | EL expression to extract value | `{#request.headers['X-API-Key']}` |
| `encode` | Hash value using MurmurHash3 (boolean) | `true` |

#### Redis vector store resource

| Property | Description | Example |
|:---------|:------------|:--------|
| `embeddingSize` | Dimension of embedding vectors (required) | `384` |
| `maxResults` | Maximum similar vectors to return (required) | `5` |
| `similarity` | Similarity metric (COSINE, EUCLIDEAN) | `COSINE` |
| `threshold` | Minimum similarity score (required) | `0.85` |
| `indexType` | Vector index type | `HNSW` |
| `readOnly` | Prevent writes to store | `false` |
| `allowEviction` | Enable automatic cache eviction | `true` |
| `evictTime` | Time before eviction (required if eviction enabled) | `3600` |
| `evictTimeUnit` | Unit for eviction time (required if eviction enabled) | `SECONDS` |

#### Redis connection

| Property | Description | Example |
|:---------|:------------|:--------|
| `url` | Redis connection URL (required) | `redis://localhost:6379` |
| `username` | Redis username | `admin` |
| `index` | Redis index name | `semantic-cache` |
| `prefix` | Key prefix for stored vectors | `llm:` |
| `query` | Redis query template for vector search | `*` |
| `scoreField` | Field name for similarity scores | `score` |
| `maxPoolSize` | Maximum connection pool size | `10` |

#### Text embedding model resource

**ONNX BERT models:**

| Property | Description | Example |
|:---------|:------------|:--------|
| `model.type` | Pre-configured model | `XENOVA_ALL_MINILM_L6_V2` |
| `poolingMode` | Pooling strategy | `MEAN` |
| `padding` | Enable sequence padding | `true` |

**OpenAI models:**

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | OpenAI API endpoint (required) | `https://api.openai.com/v1/embeddings` |
| `apiKey` | API authentication key (required) | `sk-...` |
| `organizationId` | Optional organization ID | `org-...` |
| `projectId` | Optional project ID | `proj_...` |
| `modelName` | Model identifier | `text-embedding-3-small` |
| `dimensions` | Optional embedding dimensions (non-negative) | `384` |
| `encodingFormat` | FLOAT or BASE64 | `FLOAT` |

**Custom HTTP models:**

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | Custom endpoint URL (required) | `https://embeddings.example.com/v1` |
| `method` | HTTP method | `POST` |
| `headers` | Custom HTTP headers | `[{"key": "Authorization", "value": "Bearer ..."}]` |
| `requestBodyTemplate` | Request body template | `{"input": "{input}"}` |
| `inputLocation` | JSONPath to input field (required) | `$.input` |
| `outputEmbeddingLocation` | JSONPath to embedding output (required) | `$.data[0].embedding` |

### Creating a semantic cache

Configure semantic caching by:

1. Deploy an AI embedding model resource with your chosen provider (ONNX BERT for local inference, OpenAI for cloud-based embeddings, or custom HTTP for proprietary models).
2. Deploy a vector store resource pointing to your Redis or AWS S3 infrastructure.
3. Add the AI Semantic Caching policy to your LLM proxy API flow.
4. Set `modelName` and `vectorStoreName` to match your deployed resources.
5. Configure `promptExpression` to extract the prompt content from requests (defaults to `{#request.content}`).
6. Optionally add metadata parameters with encoded context keys for multi-tenant filtering.
7. Adjust the similarity threshold in your vector store configuration to balance cache hit rate against response accuracy.

### Creating a subscription with metadata filtering

Enable multi-tenant caching by:

1. Add a parameter to the policy configuration with `key` set to `retrieval_context_key`.
2. Set `value` to an EL expression extracting the tenant identifier (e.g., `{#request.headers['X-API-Key']}`).
3. Enable `encode: true` to hash the value using MurmurHash3.
4. Ensure the vector store query includes this metadata field as a filter.

When a request arrives, the policy generates an embedding, attaches the encoded context key as metadata, and queries only vectors matching that key. This prevents cache pollution across tenants while maintaining semantic similarity matching within each tenant's scope.

### Architecture notes

#### Request processing flow

When a request enters the policy, the system extracts prompt content using the configured EL expression, generates an embedding vector via the text embedding model resource, attaches metadata parameters (with optional encoding), and queries the vector store for similar vectors above the threshold. If a match is found, the policy wraps the invoker in cache-hit mode and returns the cached response (status, headers, body) without calling the backend. If no match is found, the policy wraps the invoker in cache-miss mode, invokes the backend, evaluates the `cacheCondition` on the response, and stores the response in the vector store if the condition is true.

#### Metadata storage schema

Each cached vector stores metadata including HTTP response headers (as a map), response body content (as a string), HTTP status code (as an integer), total tokens (sent + received, as a long), optional expiration timestamp (ISO-8601 string if eviction is enabled), original prompt text, and any custom parameters defined in the policy configuration. The `retrieval_context_key` field enables tenant-specific filtering when encoded parameters are configured.

#### Token tracking and metrics

The policy calculates tokens from LLM proxy attributes (`llmproxy.usage.sent.token` and `llmproxy.usage.received.token`) and stores the total in vector metadata. Metrics track cache hits (`long_semantic-caching_cache-hit`), cache hit similarity scores (`double_semantic-caching_cache-hit-score`), tokens saved by cache hits (`long_semantic-caching_cache-hit-tokens-saved`), cache misses (`long_semantic-caching_cache-miss`), and caching errors (`long_semantic-caching_cache-error`).

### Restrictions

- Requires Gravitee APIM Enterprise Edition
- `modelName` and `vectorStoreName` must reference deployed resources
- `dimensions` (OpenAI) must be non-negative if specified
- `VectorEntity.id` must not be null/blank when adding to vector store
- `evictTime` and `evictTimeUnit` are required when `allowEviction` is enabled
- Redis version must be 8.4.0 or higher for vector store support
- AWS S3 vector store requires AWS SDK 2.41.10+ and appropriate IAM permissions
- Maximum vector dimensions supported depends on vector store implementation
- Cache eviction uses Redis automatic expiration (no separate TTL configuration)

### Related changes

The feature introduces four new plugin artifacts (`gravitee-policy-ai-semantic-caching` 1.0.0-alpha.3, `gravitee-resource-ai-vector-store-redis` 1.0.0-alpha.2, `gravitee-resource-ai-vector-store-aws-s3` 1.0.0-alpha.1, `gravitee-resource-ai-model-text-embedding` 1.0.0-alpha.4) and depends on core APIs (`gravitee-resource-ai-vector-store-api` 1.0.0-alpha.3, `gravitee-resource-ai-model-api` 2.2.1, `gravitee-inference-service` 1.4.0). Integration tests use Testcontainers with Redis 8.4.0 and enable append-only file persistence. The policy validates required configuration fields (model name, vector store name, URIs, API keys, JSONPath locations) and throws `IllegalArgumentException` for missing or invalid values.
