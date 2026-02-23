## Overview

The AI Semantic Caching policy reduces latency and cost for LLM Proxy APIs by caching responses to semantically similar prompts. Unlike traditional HTTP caching, which requires exact request matches, AI Semantic Caching uses vector embeddings to recognize semantic similarity. For example, "What is the capital of France?" and "Capital of France?" are treated as semantically equivalent, allowing the policy to return a cached response without invoking the backend LLM.

The policy converts user prompts into high-dimensional vectors using AI embedding models. Semantically similar prompts produce similar vectors, enabling the system to match requests based on meaning rather than exact text. When a request arrives, the policy queries the vector store for cached embeddings above a configured similarity threshold. If a match is found, the cached response is returned immediately without invoking the backend LLM. If no match exists, the request proceeds to the backend and the response is cached for future use.

The policy supports metadata parameters that enable context-specific caching. For example, you can cache responses per API, per tenant, or per user by attaching metadata to each cached entry. Sensitive metadata values can be hashed using MurmurHash3 (128-bit) and Base64 URL-safe encoding before storage.

## Prerequisites

- APIM Enterprise Edition
- Deployed AI text embedding model resource (ONNX BERT, OpenAI, or HTTP custom)
- Deployed vector store resource (Redis or AWS S3)
- Redis infrastructure (if using Redis vector store) with support for vector indexing (HNSW algorithm)
- AWS S3 bucket (if using AWS S3 vector store)
- LLM Proxy API configured with chat completion endpoint

## Policy configuration

Configure the AI Semantic Caching policy using the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `modelName` | Name of the AI embedding model resource | `ai-model-text-embedding-resource` |
| `vectorStoreName` | Name of the vector store resource | `vector-store-redis-resource` |
| `promptExpression` | EL expression to extract content to embed | `{#jsonPath(#request.content, '$.messages[-1:].content')}` |
| `cacheCondition` | EL expression determining if response is cacheable | `{#response.status >= 200 && #response.status < 300}` |
| `parameters` | List of key-value metadata pairs (supports EL expressions) | See Parameter configuration below |

For chat completion APIs, set `promptExpression` to `{#jsonPath(#request.content, '$.messages[-1:].content')}` to extract the last message content.

Configure `cacheCondition` to control when responses are cached. The default caches all 2xx responses.

### Parameter configuration

Add metadata parameters to enable context-aware caching:

| Property | Description | Example |
|:---------|:------------|:--------|
| `key` | Metadata field name | `retrieval_context_key` |
| `value` | EL expression to extract value | `{#context.attributes['api']}` |
| `encode` | Whether to hash the value using secure encoding | `true` |

To enable context-aware caching, add parameters to attach metadata to cached entries. For example, to cache responses per API, set `key` to `"api_id"`, `value` to `"{#context.attributes['api']}"`, and `encode` to `true` to hash the value before storage.

To prevent metadata leakage, set `encode: true` to hash the value using MurmurHash3 (128-bit) and Base64 URL-safe encoding. The policy evaluates EL expressions at runtime and stores the resulting metadata alongside the cached response and embedding vector.

## Resource configuration

### OpenAI embedding model resource

Configure the OpenAI embedding model resource with the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | OpenAI API endpoint | `https://api.openai.com/v1/embeddings` |
| `apiKey` | API authentication key | `sk-proj-...` |
| `organizationId` | Optional organization ID | `org-...` |
| `projectId` | Optional project ID | `proj_...` |
| `modelName` | Model identifier | `text-embedding-3-small` |
| `dimensions` | Embedding dimensions (must be non-negative) | `384` |
| `encodingFormat` | `FLOAT` or `BASE64` | `FLOAT` |

### HTTP custom embedding model resource

Configure the HTTP custom embedding model resource with the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `uri` | HTTP endpoint URI | `https://custom-model.example.com/embed` |
| `method` | HTTP method | `POST` |
| `headers` | Request headers | `[{"name": "Authorization", "value": "Bearer token"}]` |
| `requestBodyTemplate` | Template for request body | `{"input": "{input}"}` |
| `inputLocation` | JSONPath to input field | `$.input` |
| `outputEmbeddingLocation` | JSONPath to embedding output | `$.data[0].embedding` |

### ONNX BERT embedding model resource

Configure the ONNX BERT embedding model resource with the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `model` | Model type and files | `XENOVA_ALL_MINILM_L6_V2` |
| `poolingMode` | Pooling strategy | `MEAN` |
| `padding` | Enable/disable padding | `true` |

Available ONNX models:
- `XENOVA_ALL_MINILM_L6_V2` (512 max sequence length)
- `XENOVA_BGE_SMALL_EN_V1_5` (512 max sequence length)
- `XENOVA_MULTILINGUAL_E5_SMALL` (512 max sequence length)

### Redis vector store resource

Configure the Redis vector store resource with the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `embeddingSize` | Vector dimension size | `384` |
| `maxResults` | Maximum similar vectors to retrieve | `1` |
| `similarity` | Similarity metric | `COSINE` |
| `threshold` | Minimum similarity score | `0.7` |
| `indexType` | Vector index algorithm | `HNSW` |
| `allowEviction` | Enable TTL-based eviction | `true` |
| `evictTime` | Eviction time value | `10` |
| `evictTimeUnit` | Time unit for eviction | `SECONDS` |

Redis vector store requires HNSW index support. The similarity threshold is configured in the vector store resource, not the policy.

<!-- GAP: AWS S3 vector store configuration properties not documented in manifest -->

## Configure AI Semantic Caching

Configure the policy on your LLM Proxy API by specifying the embedding model resource and vector store resource names. Set `promptExpression` to extract the user prompt from the request body. Optionally add metadata parameters to enable context-aware caching, such as API ID or tenant ID. Set `encode: true` for sensitive values to hash them before storage.

## LLM Proxy request format

The policy expects LLM Proxy chat completion requests in this format:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "<user prompt>"
    }
  ],
  "model": "OpenAI:gpt-4o"
}
```

Responses follow the OpenAI chat completion schema with `id`, `object`, `created`, `model`, `choices`, and `usage` fields. The policy caches the entire response body along with HTTP headers and status code.

## Policy execution flow

When a request arrives, the policy extracts the prompt using `promptExpression`, generates an embedding via the AI model resource, and queries the vector store for similar embeddings above the configured threshold. If a match is found, the policy injects the cached response into the execution context and skips backend invocation.

If no match exists, the request proceeds to the backend, and the policy evaluates `cacheCondition` on the response. If true, it stores the response body, headers, status code, and metadata alongside the embedding vector.

### Invoker replacement

The policy replaces the default HTTP invoker with `AiSemanticCachingInvoker`, which intercepts the response phase to conditionally cache responses. This design ensures caching logic executes after the backend call completes and the full response is available.

### Vector metadata schema

Cached entries store a JSON object with `headers` (Map<String, List<String>>), `response` (String), `status` (Integer), and user-defined parameters from the policy configuration. This metadata enables context-aware retrieval and response reconstruction.

## Restrictions

- Requires APIM Enterprise Edition
- Requires deployment of AI text embedding model resource (ONNX BERT, OpenAI, or HTTP custom)
- Requires deployment of vector store resource (Redis or AWS S3)
- Redis vector store requires HNSW index support
- OpenAI `dimensions` must be non-negative if provided
- Vector entity ID must not be null or blank
- Configuration validation throws `IllegalArgumentException` for missing required fields (`uri`, `apiKey`, `modelName`, `inputLocation`, `outputEmbeddingLocation`, `encodingFormat`)
- ONNX BERT models have maximum sequence length of 512 tokens
- Similarity threshold configured in vector store resource, not policy

<!-- GAP: No documentation on error handling for embedding model failures -->
<!-- GAP: No guidance on choosing between Redis vs AWS S3 vector stores -->

## Related changes

The feature introduces new dependencies:
- `gravitee-policy-ai-semantic-caching` (1.0.0-alpha.1)
- `gravitee-resource-ai-vector-store-redis` (1.0.0-alpha.2)
- `gravitee-resource-ai-vector-store-aws-s3` (1.0.0-alpha.1)
- `gravitee-resource-ai-model-text-embedding` (1.0.0-alpha.4)
- `gravitee-inference-service` (1.4.0)

Hazelcast cluster plugins updated to 8.0.0-alpha.3. AWS S3 vector store resource migrated to Enterprise edition.