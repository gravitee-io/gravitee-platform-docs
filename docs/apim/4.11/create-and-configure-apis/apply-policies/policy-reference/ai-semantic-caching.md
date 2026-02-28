### Overview

AI Semantic Caching reduces LLM API costs and latency by recognizing semantically similar requests and serving cached responses instead of making redundant backend calls. The feature uses vector embeddings to match user prompts, enabling intelligent cache hits even when request text differs slightly. This is an Enterprise Edition capability available for LLM Proxy APIs.

### Key concepts

#### Semantic similarity matching

The policy converts user prompts into vector embeddings using a configured text embedding model (ONNX BERT, OpenAI, or custom HTTP endpoint). When a new request arrives, the system searches the vector store for embeddings that exceed a configured similarity threshold. If a match is found, the cached response is returned without calling the LLM backend. Similarity is measured using configurable metrics (e.g., COSINE distance).

#### Vector storage backends

Gravitee supports two vector storage options: Redis and AWS S3 Vectors. Redis provides low-latency in-memory storage with configurable indexing (HNSW). AWS S3 Vectors offers scalable cloud storage with automatic encryption (SSE-S3 or SSE-KMS) and optional TTL-based eviction. Both backends store embeddings alongside response metadata and support similarity search operations.

#### Cache key scoping

Cache entries can be scoped using optional metadata parameters extracted via EL expressions. This allows cache isolation per API, user, or custom dimension. For example, `parameters: [{name: "apiId", value: "{#request.headers['X-API-ID']}"}]` ensures cache hits only occur within the same API context.

### Prerequisites

- Gravitee APIM 4.x with LLM Proxy support
- Enterprise Edition license
- One of the following text embedding resources deployed:
  - ONNX BERT (local inference)
  - OpenAI embedding model (requires API key)
  - Custom HTTP embedding endpoint
- One of the following vector store resources deployed:
  - Redis (with vector search capability)
  - AWS S3 Vectors (requires AWS credentials or IAM role)
- Hazelcast cache plugin 8.0.0-alpha.3 or later
- Hazelcast cluster plugin 8.0.0-alpha.3 or later

### Gateway configuration

#### Hazelcast plugin versions

| Property | Description | Example |
|:---------|:------------|:--------|
| `cluster.plugins[0]` | Hazelcast cache plugin download URL | `https://download.gravitee.io/pre-releases/plugins/node-cache/gravitee-node-cache-plugin-hazelcast/gravitee-node-cache-plugin-hazelcast-8.0.0-alpha.3.zip` |
| `cluster.plugins[1]` | Hazelcast cluster plugin download URL | `https://download.gravitee.io/pre-releases/plugins/node-cluster/gravitee-node-cluster-plugin-hazelcast/gravitee-node-cluster-plugin-hazelcast-8.0.0-alpha.3.zip` |

#### AI resource versions

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee-resource-ai-vector-store-redis.version` | Redis vector store resource version | `1.0.0-alpha.2` |
| `gravitee-resource-ai-vector-store-aws-s3.version` | AWS S3 vector store resource version | `1.0.0-alpha.1` |
| `gravitee-resource-ai-model-text-embedding.version` | Text embedding model resource version | `1.0.0-alpha.4` |
| `gravitee-policy-ai-semantic-caching.version` | Semantic caching policy version | `1.0.0-alpha.3` |

#### Text embedding model configuration

**ONNX BERT configuration**

| Property | Description | Example |
|:---------|:------------|:--------|
| `model.type` | Pre-trained model selection | `XENOVA_ALL_MINILM_L6_V2`, `XENOVA_BGE_SMALL_EN_V1_5`, `XENOVA_MULTILINGUAL_E5_SMALL` |
| `poolingMode` | Pooling strategy for embeddings | `MEAN` |
| `padding` | Enable input padding | `true` |

**OpenAI configuration**

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | OpenAI API endpoint | `https://api.openai.com/v1` |
| `apiKey` | OpenAI API key (required) | `sk-...` |
| `organizationId` | OpenAI organization ID | `org-...` |
| `projectId` | OpenAI project ID | `proj_...` |
| `modelName` | Model identifier (required) | `text-embedding-3-small` |
| `dimensions` | Embedding dimensions (must be non-negative) | `1536` |
| `encodingFormat` | Output format | `FLOAT`, `BASE64` |

**HTTP configuration**

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | Custom model endpoint (required) | `https://custom-embeddings.example.com/embed` |
| `method` | HTTP method (required) | `POST` |
| `headers` | Request headers | `[{name: "Authorization", value: "Bearer ..."}]` |
| `requestBodyTemplate` | Request body template | `{"input": "{#input}"}` |
| `inputLocation` | JSON path for input in request | `$.input` |
| `outputEmbeddingLocation` | JSON path for embedding in response (required) | `$.data[0].embedding` |

#### Vector store configuration

**Redis configuration**

| Property | Description | Example |
|:---------|:------------|:--------|
| `redisConfig.url` | Redis connection URL (required) | `redis://localhost:6379` |
| `redisConfig.username` | Redis username | `default` |
| `redisConfig.index` | Redis index name (required) | `llm-cache-idx` |
| `redisConfig.prefix` | Key prefix for vectors (required) | `llm:cache:` |
| `redisConfig.maxPoolSize` | Maximum connection pool size | `6` |
| `properties.embeddingSize` | Dimension of embedding vectors (required) | `384` |
| `properties.maxResults` | Maximum search results (required) | `10` |
| `properties.similarity` | Similarity metric (required) | `COSINE` |
| `properties.threshold` | Similarity threshold (required) | `0.85` |
| `properties.indexType` | Index type (required) | `HNSW` |

**AWS S3 Vectors configuration**

| Property | Description | Example |
|:---------|:------------|:--------|
| `awsS3VectorsConfiguration.region` | AWS region for S3 Vectors service (required) | `us-east-1` |
| `awsS3VectorsConfiguration.vectorBucketName` | S3 bucket name for vector storage (required) | `gravitee-llm-cache` |
| `awsS3VectorsConfiguration.vectorIndexName` | Index name for vector queries (required) | `llm-cache-index` |
| `awsS3VectorsConfiguration.awsAccessKeyId` | AWS access key ID (optional if using IAM) | `AKIA...` |
| `awsS3VectorsConfiguration.awsSecretAccessKey` | AWS secret access key (optional if using IAM) | `...` |
| `properties.allowEviction` | Enable automatic vector eviction (required) | `true` |
| `properties.evictTime` | Time before eviction (required) | `3600` |
| `properties.evictTimeUnit` | Time unit for eviction (required) | `SECONDS` |

AWS S3 Vectors authentication uses explicit credentials if `awsAccessKeyId` and `awsSecretAccessKey` are provided. Otherwise, it falls back to the default AWS credentials chain (environment variables, IAM role, etc.). Encryption is automatically configured as SSE-S3 (S3-managed keys) or SSE-KMS (KMS-managed keys) based on bucket settings.

#### Semantic caching policy configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `modelName` | Text embedding resource name (required) | `openai-embeddings` |
| `vectorStoreName` | Vector store resource name (required) | `redis-vectors` |
| `promptExpression` | EL expression to extract prompt from request (required) | `{#request.content.messages[0].content}` |
| `cacheCondition` | EL expression for cache eligibility (optional) | `{#response.status == 200}` |
| `parameters` | Metadata parameters for cache key scoping (optional) | `[{name: "apiId", value: "{#api.id}"}]` |

### Creating an LLM Proxy API with semantic caching

Configure an LLM Proxy API with the following structure:

1. Add an HTTP listener with an `llm-proxy` entrypoint and a path like `/llm/`.
2. Define an endpoint group with type `llm-proxy` pointing to your LLM provider (e.g., OpenAI at `http://localhost:8080/v1`). Configure authentication (API key in `Authorization` header) and specify models with input/output pricing.
3. Deploy the text embedding resource and vector store resource to your gateway.
4. Apply the AI Semantic Caching policy to the API flow, referencing the deployed resources by name.
5. Configure `promptExpression` to extract the user prompt from the request body (e.g., `{#request.content.messages[0].content}` for OpenAI chat format). Optionally set `cacheCondition` to control when responses are cached (e.g., only successful responses with `{#response.status == 200}`).

### Cache behavior and metrics

When a request arrives, the policy extracts the prompt using `promptExpression` and generates a vector embedding. It searches the vector store for embeddings with similarity scores above the configured threshold. If a match is found (cache hit), the cached response is returned immediately without calling the backend, and metrics are recorded: `cache-hit=1`, `cache-hit-score=<similarity>`, `cache-hit-tokens-saved=<tokens>`. If no match is found (cache miss), the request proceeds to the backend, and `cache-miss=1` is recorded. After a successful backend response, if `cacheCondition` evaluates to true (or is empty), the response is stored in the vector store with the prompt embedding and optional metadata parameters. If the vector store is unavailable or returns an error, the policy logs a warning and records `cache-error=1`, but the request continues normally (non-blocking failure).

### Architecture notes

#### Vector eviction

When `allowEviction` is enabled in AWS S3 Vectors configuration, each stored vector includes an `expireAt` timestamp calculated as `Instant.now() + evictTime`. The S3 Vectors service automatically removes expired entries, preventing unbounded cache growth. Redis eviction is managed through Redis TTL policies configured at the database level.

#### Cache key composition

Cache keys are composed from the prompt embedding plus optional metadata parameters. For example, if `parameters` includes `{name: "apiId", value: "{#api.id}"}`, cache entries are scoped per API, ensuring that identical prompts across different APIs don't share cache entries. This prevents cross-contamination in multi-tenant deployments.

#### Error resilience

Cache failures (vector store unavailable, embedding model timeout, etc.) are logged as warnings but don't interrupt request processing. The policy falls back to normal backend execution, ensuring high availability even when caching infrastructure is degraded. This design prioritizes reliability over cache hit rate.

### Restrictions

- Requires Enterprise Edition license
- Only available for LLM Proxy API type (not HTTP Proxy or Message APIs)
- Minimum Gravitee APIM version: 4.x with LLM Proxy support
- Hazelcast plugins must be version 8.0.0-alpha.3 or later
- AWS S3 Vectors requires valid AWS credentials or IAM role with S3 and S3 Vectors permissions
- Redis vector store requires Redis with vector search capability (RedisStack or Redis Enterprise)
- `promptExpression` must resolve to a non-null string; blank prompts are rejected
- Embedding dimensions must match between text embedding model and vector store configuration
- Similarity threshold must be between 0.0 and 1.0
- If `allowEviction` is enabled, `evictTime` and `evictTimeUnit` are required
- Cache condition expressions must return boolean values
- Metadata parameters are limited to string values extracted via EL expressions

### Related changes

The Console UI now displays AI Semantic Caching as an available policy for LLM Proxy APIs in the policy catalog. Resource configuration screens include validation for required fields (e.g., `uri`, `apiKey`, `modelName` for OpenAI; `region`, `vectorBucketName`, `vectorIndexName` for AWS S3). The policy configuration form provides EL expression editors for `promptExpression`, `cacheCondition`, and metadata parameters. Metrics dashboards include new cache-specific metrics: `cache-hit`, `cache-miss`, `cache-error`, `cache-hit-score`, and `cache-hit-tokens-saved`. Dependency versions have been updated across the distribution: `gravitee-node` to 8.0.0-alpha.3, `gravitee-parent` to 23.5.0, `gravitee-bom` to 8.3.47, `gravitee-common` to 4.8.0, and `gravitee-inference-service` to 1.4.0.
