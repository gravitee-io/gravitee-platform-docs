### Overview

AI Semantic Caching reduces LLM token consumption and API latency by caching responses based on semantic meaning rather than exact text matching. When a user submits a query that is semantically equivalent to a previously processed prompt—even if phrased differently—the policy serves the cached result without invoking the LLM backend. This policy is available exclusively on LLM Proxy APIs and requires an embedding model resource and a vector store resource.

{% hint style="info" %}
AI Semantic Caching is available in Gravitee Enterprise Edition and requires Agent Mesh deployment.
{% endhint %}

### Key Concepts

#### Semantic Matching

Traditional caching relies on exact text matching, resulting in cache misses when users rephrase queries. Semantic caching converts prompts into vector embeddings using an AI text embedding model, then searches a vector store for semantically similar queries. If a match exceeds the configured similarity threshold, the cached response is returned immediately. Similarity is measured using configurable metrics (cosine, euclidean, or dot product).

#### Cache Lifecycle

The policy operates in two phases:

**Request Phase:**
1. The policy extracts the prompt using an EL expression (default: `{#request.content}`).
2. The prompt is converted into a vector embedding via the configured embedding model resource.
3. The vector store is queried for semantically similar cached vectors.
4. On a cache hit, the backend is bypassed and the cached response is returned.
5. On a cache miss, the request proceeds to the LLM backend.

**Response Phase:**
1. If the cache condition evaluates to true (default: 2xx status codes), the response is stored in the vector store.
2. The stored entry includes the embedding, response body, headers, status code, token usage, and user-defined metadata.
3. If `allowEviction` is enabled, an `expireAt` timestamp is calculated and stored.

#### Metadata and Partitioning

Each cached vector includes metadata such as response headers, status code, token usage, and user-defined parameters. Parameters are key-value pairs extracted via EL expressions and can be encoded (hashed using MurmurHash3) to partition the cache by sensitive attributes like API, plan, or user ID. This ensures that semantically identical prompts from different contexts (e.g., "Give me my balance" from different users) retrieve context-appropriate cached results.

### Prerequisites

- LLM Proxy API (semantic caching is not available on standard v4 APIs)
- Agent Mesh deployment
- AI text embedding model resource configured (ONNX BERT, OpenAI, or HTTP provider)
- Vector store resource configured (Redis or AWS S3)
- Embedding model and vector store must use compatible embedding dimensions

### Gateway Configuration

#### Policy Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `modelName` | Name of the AI text embedding model resource | `"ai-model-text-embedding-resource"` |
| `vectorStoreName` | Name of the vector store resource | `"vector-store-redis-resource"` |
| `promptExpression` | EL expression to extract the content to embed (default: `{#request.content}`) | `"{#jsonPath(#request.content, '$.messages[-1:].content')}"` |
| `cacheCondition` | EL expression determining whether the response is cacheable (default: `{#response.status >= 200 && #response.status < 300}`) | `"{#response.status >= 200}"` |
| `parameters` | Array of metadata parameters to store with the vector | See Parameter Configuration below |

#### Parameter Configuration

| Property | Description | Example |
|:---------|:------------|:--------|
| `key` | Name of the metadata field | `"retrieval_context_key"` |
| `value` | EL expression to extract the value from the context | `"{#context.attributes['api']}_{#context.attributes['user-id']}"` |
| `encode` | Whether to hash the value using MurmurHash3 (for indexing sensitive data) | `true` |

**Default parameter:**
```json
{
 "key": "retrieval_context_key",
 "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
 "encode": true
}
```

### Creating a Semantic Caching Flow

Configure the policy in the request phase of an LLM Proxy API flow:

1. Create or select an AI text embedding model resource and a vector store resource.
2. Add the AI Semantic Caching policy to the request phase.
3. Set `modelName` to the embedding model resource name and `vectorStoreName` to the vector store resource name.
4. (Optional) Customize `promptExpression` to extract the relevant prompt content (e.g., using JSONPath for chat message arrays).
5. (Optional) Configure `parameters` to partition the cache by API, plan, user, or other context attributes.
6. Deploy the API.

On the first request, the policy will generate an embedding, find no match, invoke the backend, and cache the response. Subsequent semantically similar requests will return the cached result.

### Embedding Model Configuration

For detailed configuration of embedding model resources, see the AI text embedding model resource documentation.

#### ONNX BERT Provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `model.type` | Embedding model type | `XENOVA_ALL_MINILM_L6_V2`, `XENOVA_BGE_SMALL_EN_V1_5`, or `XENOVA_MULTILINGUAL_E5_SMALL` |
| `poolingMode` | Pooling mode for embeddings | `MEAN` |
| `padding` | Whether to apply padding | `true` |

All ONNX BERT models support a maximum sequence length of 512 tokens.

#### OpenAI Provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | OpenAI API endpoint URI | `"https://api.openai.com/v1/embeddings"` |
| `apiKey` | OpenAI API key | `"sk-..."` |
| `organizationId` | Optional organization ID | `"org-..."` |
| `projectId` | Optional project ID | `"proj_..."` |
| `modelName` | Name of the embedding model | `"text-embedding-ada-002"` |
| `dimensions` | Optional embedding dimensions (must be non-negative) | `1536` |
| `encodingFormat` | Encoding format | `FLOAT` or `BASE64` |

#### HTTP Provider

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | HTTP endpoint URI | `"https://custom-embedding-service.example.com/embed"` |
| `method` | HTTP method | `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`, or `TRACE` |
| `headers` | HTTP headers to include | `[]` |
| `requestBodyTemplate` | Template for request body | `null` |
| `inputLocation` | JSONPath or location for input in request | |
| `outputEmbeddingLocation` | JSONPath or location for embedding in response | |

### Vector Store Configuration

For detailed configuration of vector store resources, see the vector store resource documentation.

#### AWS S3 Vector Store

| Property | Description | Example |
|:---------|:------------|:--------|
| `awsS3VectorsConfiguration.region` | AWS region | `"us-east-1"` |
| `awsS3VectorsConfiguration.awsAccessKeyId` | AWS access key ID | |
| `awsS3VectorsConfiguration.awsSecretAccessKey` | AWS secret access key | |
| `awsS3VectorsConfiguration.sessionToken` | Optional AWS session token | `null` |
| `awsS3VectorsConfiguration.vectorBucketName` | S3 bucket name for vectors | |
| `awsS3VectorsConfiguration.vectorIndexName` | Index name for vector search | |
| `awsS3VectorsConfiguration.encryptionType` | Encryption type | `SSE_S3`, `SSE_KMS`, or `DSSE_KMS` |
| `awsS3VectorsConfiguration.kmsKeyId` | KMS key ID (required if encryption is `SSE_KMS` or `DSSE_KMS`) | `null` |
| `properties.embeddingSize` | Size of embedding vectors | |
| `properties.maxResults` | Maximum number of results to return | |
| `properties.similarity` | Similarity metric | `COSINE`, `EUCLIDEAN`, or `DOT_PRODUCT` |
| `properties.threshold` | Minimum similarity threshold | |
| `properties.readOnly` | Whether the store is read-only | `false` |
| `properties.allowEviction` | Whether to allow automatic eviction | `false` |
| `properties.evictTime` | Time before eviction | `0` |
| `properties.evictTimeUnit` | Time unit for eviction | `SECONDS` |

#### Redis Vector Store

| Property | Description | Example |
|:---------|:------------|:--------|
| `redisConfig.url` | Redis connection URL | |
| `redisConfig.username` | Redis username | `"default"` |
| `redisConfig.index` | Redis index name | |
| `redisConfig.prefix` | Key prefix for vectors | |
| `redisConfig.query` | Redis query template | |
| `redisConfig.scoreField` | Field name for similarity score | |
| `redisConfig.maxPoolSize` | Maximum connection pool size | `6` |
| `redisConfig.vectorStoreConfig.vectorType` | Vector data type | `"BFLOAT16"` |
| `redisConfig.vectorStoreConfig.M` | HNSW M parameter | `10` |
| `redisConfig.vectorStoreConfig.efConstruction` | HNSW ef_construction parameter | `200` |
| `redisConfig.vectorStoreConfig.efRuntime` | HNSW ef_runtime parameter | `10` |
| `redisConfig.vectorStoreConfig.epsilon` | HNSW epsilon parameter | `0.01` |
| `redisConfig.vectorStoreConfig.initialCapacity` | Initial capacity | `5` |
| `redisConfig.vectorStoreConfig.blockSize` | Block size | `10` |

### Metrics

The policy emits the following metrics:

| Metric Name | Type | Description |
|:------------|:-----|:------------|
| `cache-hit` | long | Set to `1` when cache hit occurs |
| `cache-hit-score` | double | Similarity score of cache hit |
| `cache-hit-tokens-saved` | long | Number of tokens saved by cache hit |
| `cache-miss` | long | Set to `1` when cache miss occurs |
| `cache-error` | long | Set to `1` when error occurs during caching |

### Restrictions

- **LLM Proxy API only**: Semantic caching is not available on standard v4 APIs.
- **Agent Mesh required**: The policy requires Agent Mesh deployment.
- **Compatible embedding dimensions**: The embedding model and vector store must use compatible embedding dimensions.
- **Read-only mode behavior**: When the vector store is configured in read-only mode, the policy will not write new cache entries but will continue to serve existing cached results.
- **Eviction requirements**: Automatic eviction requires `allowEviction` to be set to `true` and a valid `expireAt` timestamp calculated from `evictTime` and `evictTimeUnit`.
- **Parameter encoding**: When `encode` is set to `true`, parameter values are hashed using MurmurHash3 (128-bit) and Base64 URL-encoded without padding.
- **Cache condition**: The `cacheCondition` expression must evaluate to a boolean value.
- **Prompt expression**: The `promptExpression` must return a non-null string.
- **AWS S3 KMS encryption**: If encryption type is `SSE_KMS` or `DSSE_KMS`, `kmsKeyId` is required.
- **OpenAI dimensions**: If specified, `dimensions` must be non-negative.
- **HTTP provider**: `inputLocation` and `outputEmbeddingLocation` must be valid JSONPath expressions.
