### Overview

AI Semantic Caching reduces latency and costs for LLM-based APIs by caching responses based on semantic similarity rather than exact string matching. When a request arrives, the policy embeds the prompt using a configured text embedding model, searches a vector store for similar past prompts, and returns the cached response if a match exceeds the similarity threshold.

### Key Concepts

#### Semantic Similarity Matching

Unlike traditional caching that requires exact key matches, semantic caching compares the meaning of prompts using vector embeddings. A prompt like "What is the capital of France?" will match "Tell me France's capital city" if their embeddings are sufficiently similar. The policy uses configurable similarity metrics (cosine, euclidean, or dot product) and a threshold score to determine cache hits. Results are ranked by similarity score, with only matches above the threshold returned.

#### Vector Stores

Vector stores persist embeddings and their associated cached responses. Gravitee supports Redis and AWS S3 as vector store backends. Each store maintains an index of vectors with metadata (response body, headers, status code, token count) and supports configurable eviction policies. Administrators configure connection details, index names, similarity metrics, and result limits at the resource level.

#### Text Embedding Models

Embedding models transform text prompts into high-dimensional vectors. Gravitee supports three provider types: ONNX BERT (local pre-trained models like `all-MiniLM-L6-v2`), OpenAI (cloud-based models like `text-embedding-3-small`), and Custom HTTP (user-hosted embedding services). Each model resource defines the provider configuration, including API credentials, model names, and output dimensions.

### Prerequisites

Before configuring AI Semantic Caching, complete the following:

* Enable the `apim-ai-policy-semantic-cache` feature flag in Gravitee API Management
* Create a text embedding model resource (ONNX BERT, OpenAI, or HTTP provider)
* Create a vector store resource (Redis or AWS S3)
* For AWS S3: provide valid AWS credentials with S3 bucket access permissions
* For Redis: provide connection details for a Redis instance with vector search capabilities
* For OpenAI: provide a valid API key and organization/project IDs (if applicable)

### Configuration

#### AI Semantic Caching Policy

| Property | Description | Example |
|:---------|:------------|:--------|
| `modelName` | Name of the text embedding model resource | `ai-model-text-embedding-resource` |
| `vectorStoreName` | Name of the vector store resource | `vector-store-redis-resource` |
| `promptExpression` | EL expression to extract content for embedding | `{#jsonPath(#request.content, '$.messages[-1:].content')}` |
| `cacheCondition` | EL expression determining if response should be cached | `{#response.status >= 200 && #response.status < 300}` |
| `parameters` | Array of metadata key-value pairs (supports EL and encoding) | See Parameter Object table |

#### Parameter Object

| Property | Description | Example |
|:---------|:------------|:--------|
| `key` | Metadata field name for indexing | `retrieval_context_key` |
| `value` | EL expression to extract value | `{#context.attributes['api']}_{#context.attributes['user-id']}` |
| `encode` | Hash value using MurmurHash3 (for sensitive data) | `true` |

#### AWS S3 Vector Store Resource

| Property | Description | Example |
|:---------|:------------|:--------|
| `vectorBucketName` | S3 bucket name for vector storage | `my-vector-cache-bucket` |
| `vectorIndexName` | Vector index name | `llm-cache-index` |
| `awsAccessKeyId` | AWS access key ID | `AKIAIOSFODNN7EXAMPLE` |
| `awsSecretAccessKey` | AWS secret access key | `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY` |
| `awsSessionToken` | AWS session token (for temporary credentials) | `FwoGZXIvYXdzEBYaD...` |
| `region` | AWS region | `us-east-1` |
| `encryptionType` | Encryption type: `SSE_S3`, `SSE_KMS`, or `NONE` | `SSE_KMS` |
| `kmsKeyId` | KMS key ID (required when using `SSE_KMS`) | `arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012` |

#### Redis Vector Store Resource

| Property | Description | Example |
|:---------|:------------|:--------|
| `url` | Redis connection URL | `redis://localhost:6379` |
| `username` | Redis username | `default` |
| `index` | Redis index name | `llm-cache-index` |
| `prefix` | Key prefix for stored vectors | `cache:` |
| `maxPoolSize` | Maximum connection pool size | `6` |
| `embeddingSize` | Dimension of embedding vectors | `384` |
| `maxResults` | Maximum number of results to return | `5` |
| `similarity` | Similarity metric: `COSINE`, `EUCLIDEAN`, or `DOT_PRODUCT` | `COSINE` |
| `threshold` | Minimum similarity score threshold | `0.85` |
| `indexType` | Vector index type | `HNSW` |
| `readOnly` | Whether the store is read-only | `false` |
| `allowEviction` | Enable automatic eviction | `true` |
| `evictTime` | Time before eviction (when enabled) | `3600` |
| `evictTimeUnit` | Time unit: `SECONDS`, `MINUTES`, `HOURS`, etc. | `SECONDS` |

#### Text Embedding Model (ONNX BERT)

| Property | Description | Example |
|:---------|:------------|:--------|
| `model.type` | Pre-trained model: `XENOVA_ALL_MINILM_L6_V2`, `XENOVA_BGE_SMALL_EN_V1_5`, `XENOVA_MULTILINGUAL_E5_SMALL` | `XENOVA_ALL_MINILM_L6_V2` |
| `poolingMode` | Pooling strategy: `MEAN`, `CLS`, `MAX` | `MEAN` |
| `padding` | Whether to pad input sequences | `false` |

#### Text Embedding Model (OpenAI)

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | OpenAI API endpoint URL | `https://api.openai.com/v1/embeddings` |
| `apiKey` | OpenAI API key | `sk-proj-...` |
| `organizationId` | OpenAI organization ID (optional) | `org-...` |
| `projectId` | OpenAI project ID (optional) | `proj_...` |
| `modelName` | Model name | `text-embedding-3-small` |
| `dimensions` | Output embedding dimensions (optional, must be non-negative) | `512` |
| `encodingFormat` | Encoding format: `FLOAT` or `BASE64` | `FLOAT` |

#### Text Embedding Model (Custom HTTP)

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | HTTP endpoint URL | `https://my-embedding-service.example.com/embed` |
| `method` | HTTP method: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`, `TRACE` | `POST` |
| `headers` | List of HTTP headers (name/value pairs) | `[{"name": "Authorization", "value": "Bearer token"}]` |
| `requestBodyTemplate` | Template for request body | `{"input": "{{input}}"}` |
| `inputLocation` | JSONPath to input field in request | `$.input` |
| `outputEmbeddingLocation` | JSONPath to embedding field in response | `$.data[0].embedding` |

### Creating an LLM API with Semantic Caching

Configure the semantic caching policy in the request phase of your LLM proxy API flow:

1. Create or select a text embedding model resource (ONNX BERT for local processing, OpenAI for cloud-based, or HTTP for custom endpoints).
2. Create or select a vector store resource (Redis for low-latency in-memory caching or AWS S3 for persistent storage).
3. Add the AI Semantic Caching policy to the request flow, referencing the model and vector store by name.
4. Configure the `promptExpression` to extract the relevant content from the request (e.g., `{#jsonPath(#request.content, '$.messages[-1:].content')}` for OpenAI-style chat completions).
5. Set the `cacheCondition` to define when responses should be cached (default: successful 2xx responses).
6. (Optional) Add metadata parameters with EL expressions to partition the cache by API, plan, or user (enable `encode: true` for sensitive values like user IDs).

### Configuring Cache Eviction

Enable automatic eviction in the vector store resource to prevent stale responses from persisting indefinitely. For AWS S3, set `allowEviction: true` and specify `evictTime` and `evictTimeUnit` (e.g., `evictTime: 3600, evictTimeUnit: SECONDS` for one-hour expiration). The policy stores an `expireAt` timestamp in the vector metadata, calculated as the current time plus the eviction duration. For Redis, configure eviction using the `allowEviction`, `evictTime`, and `evictTimeUnit` properties in the resource configuration. Eviction is checked when vectors are added; expired entries are not automatically removed but will not be returned in search results.

### Encoding Sensitive Metadata

Use the `encode: true` parameter option to hash sensitive metadata values before storing them in the vector index. When enabled, the policy applies MurmurHash3 (128-bit) and Base64-encodes the result (URL-safe, no padding). This allows partitioning the cache by user ID, API key, or other sensitive identifiers without storing plaintext values. For example, set `key: "retrieval_context_key"`, `value: "{#context.attributes['user-id']}"`, and `encode: true` to create a unique cache partition per user without exposing user IDs in the vector store.

### Restrictions

* Requires the `apim-ai-policy-semantic-cache` feature flag to be enabled
* Policy must be placed in the REQUEST phase of the flow
* Embedding model and vector store resources must be created before configuring the policy
* AWS S3 vector store requires valid credentials with S3 bucket read/write permissions
* When using `SSE_KMS` encryption, `kmsKeyId` must be provided
* OpenAI provider requires a valid API key; `dimensions` (if specified) must be non-negative
* HTTP provider requires `uri`, `method`, `inputLocation`, and `outputEmbeddingLocation` to be configured
* ONNX BERT models have a maximum sequence length of 512 tokens
* Cache hits bypass the backend entirely; ensure `cacheCondition` accurately identifies cacheable responses
* If embedding generation fails, the policy logs a warning and proceeds without caching (request is not failed)
* If cache write fails, the policy logs a warning and returns the backend response (request is not failed)
* Metadata parameter values are evaluated using Gravitee EL; invalid expressions will cause policy execution errors
* Vector similarity threshold and maxResults are configured at the vector store resource level, not per-policy

### Related Changes

The AI semantic caching policy and vector store resources are distributed as part of Gravitee API Management Enterprise Edition. The policy is categorized under `ai` and appears in the policy catalog when the feature flag is enabled. The distribution includes four new artifacts: `gravitee-policy-ai-semantic-caching` (1.0.0-alpha.3), `gravitee-resource-ai-vector-store-redis` (1.0.0-alpha.2), `gravitee-resource-ai-vector-store-aws-s3` (1.0.0-alpha.1), and `gravitee-resource-ai-model-text-embedding` (1.0.0-alpha.4). Hazelcast cluster and cache plugins have been updated to version 8.0.0-alpha.3 to support distributed caching scenarios. The policy emits metrics for cache hits, misses, and errors, including similarity scores and token savings, which are visible in the API analytics dashboard. Validation errors for missing or invalid configuration properties are surfaced in the API deployment logs with descriptive messages (e.g., "URI is required", "Model name is required").
