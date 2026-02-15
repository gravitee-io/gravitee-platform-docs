## Overview

The AI Semantic Caching policy enables semantic caching of responses based on the similarity of request content. Unlike traditional caching mechanisms that rely on exact text matching, this policy uses vector embeddings to identify semantically equivalent requests, even when phrased differently. When a similar request is found, the cached response is returned immediately, reducing LLM token consumption and API latency.

This capability addresses a key limitation of traditional caching mechanisms, which rely on lexical (exact text) matching and result in high cache miss rates when users submit semantically equivalent queries phrased differently.

The policy integrates with Gravitee AI resources to transform requests into vector representations and store them in a vector database for efficient retrieval.

{% hint style="info" %}
AI resources are Enterprise features.
{% endhint %}

## How it works

The AI Semantic Caching policy operates in two phases:

### Request phase

When a request arrives, the policy:

1. Extracts content using the `promptExpression` (default: entire request body)
2. Generates a vector embedding using the configured AI Text Embedding Model Resource
3. Searches the Vector Store Resource for similar cached vectors using metadata filters
4. If a similar vector is found, returns the cached response immediately
5. If no match is found, forwards the request to the backend

### Response phase

After receiving the backend response, the policy:

1. Evaluates the `cacheCondition` to determine if the response should be cached
2. If cacheable, stores the response (status, headers, body) with the vector and metadata in the Vector Store Resource

## Prerequisites

Before using this policy, configure the following Gravitee resources:

- **AI Text Embedding Model Resource**: Converts text into vector embeddings (e.g., `gravitee-resource-ai-model-text-embedding`)
- **Vector Store Resource**: Stores and retrieves vectors (e.g., `gravitee-resource-ai-vector-store-redis`)

These resources must be configured at the API or platform level before adding the policy to your flow.

## Metadata and filtering

The `parameters` configuration attaches metadata to each cached vector. This metadata is used for:

- **Filtering queries**: Scope caching appropriately (e.g., per API, per user, per plan)
- **Privacy**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

Example use cases:

- Scope cache per API: `{#context.attributes['api']}`
- Scope cache per user: `{#context.attributes['user-id']}`
- Scope cache per plan: `{#context.attributes['plan']}`

## Best practices

### Use JSONPath for complex payloads

When working with structured data like LLM chat completions, extract only the relevant content. For LLM Proxy APIs handling OpenAI-compatible chat completion requests, configure the policy to extract only the relevant message content using JSONPath:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This approach ensures that semantically similar conversations are matched even when the exact phrasing differs, dramatically reducing LLM token consumption and API response latency.

### Set appropriate cache conditions

Avoid caching errors or non-deterministic responses:

```
{#response.status >= 200 && #response.status < 300}
```

### Use encoded parameters for sensitive data

When using user IDs or other PII as metadata filters:

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

### Consider similarity thresholds

Configure your Vector Store Resource with appropriate similarity thresholds to balance cache hit rate versus accuracy.

## Limitations

- The quality of semantic matching depends on the embedding model and Vector Store Resource configuration
- Not suitable for APIs with highly dynamic or personalized responses

## Phases

The `ai-semantic-caching` policy can be applied to the following API types and flow phases.

### Compatible API types

- `LLM_PROXY`

### Supported flow phases

- Request

## Compatibility matrix

| Plugin version | APIM | Java version |
| --- | --- | --- |
| 1.x | 4.11.x and above | 21+ |

## Configuration

### Configuration options

| Name<br>`json name` | Type<br>`constraint` | Mandatory | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| Cache condition<br>`cacheCondition` | string |  | `{#response.status >= 200 && #response.status < 300}` | EL expression to determine if the response should be cached |
| Embedding model resource<br>`modelName` | string | ✅ |  | Name of the configured AI Text Embedding Model Resource |
| Parameters<br>`parameters` | array |  | `[{"encode": true, "key": "retrieval_context_key", "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}"}]` | Metadata parameters to attach to cached vectors (using EL) |
| Prompt expression<br>`promptExpression` | string |  | `{#request.content}` | EL expression to extract content for vector generation |
| Vector store resource<br>`vectorStoreName` | string | ✅ |  | Name of the configured Vector Store Resource |

#### Parameters (Array)

| Name<br>`json name` | Type<br>`constraint` | Mandatory | Default | Description |
| :--- | :--- | :---: | :--- | :--- |
| Encode value<br>`encode` | boolean |  |  | Encode the value using MurmurHash3 (Base64) for sensitive information |
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

## Changelog

### 1.0.0-alpha.1 (2026-01-23)

#### Bug Fixes

- adjust vector-store api changes + bump gravitee deps ([4a51f4f](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/4a51f4f80eb0d1905b70a91bb557b98285491256))
- tests ([bcadf21](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/bcadf211aae346d090aa00e83ccd58903b4134a8))

#### Features

- adapt vector store api ([2188076](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/218807623d47acb26b1cff6e7eea608f111b7816))
- enable policy for LLM proxy ([9ac20b7](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/9ac20b7a0de8028d0bef165f9d09d28fa2838511))
- first import ([5547a51](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/5547a51a9e1a24429386ebf8bea70456751a2f51))
- prepare policy for EE ([800d037](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/800d0378f7d9a04faa5e9ee5846ab563e0a0e51d))
- update inference service version ([#2](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/issues/2)) ([8595387](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/8595387dc9a82b17caffed9bce1985d224885f2d))

### Prerequisites

Before using this policy, you must configure the following Gravitee resources:

- **AI Text Embedding Model Resource**: Provides vector embeddings (e.g., `gravitee-resource-ai-model-text-embedding`). This resource must be configured at the API or platform level before adding the policy to your flow.
- **Vector Store Resource**: Stores and retrieves vectors (e.g., `gravitee-resource-ai-vector-store-redis`). This resource must be configured at the API or platform level before adding the policy to your flow.

<!-- GAP: AI Text Embedding Model Resource documentation does not exist. This resource is required for the AI Semantic Caching policy to function. Documentation should cover configuration, supported models, and integration with vector stores. -->

### How it works

1. **Request phase**: When a request arrives, the policy:
   - Extracts content using the `promptExpression` (default: entire request body)
   - Generates a vector embedding using the configured embedding model
   - Searches the vector store for similar cached vectors using metadata filters
   - If a similar vector is found (based on an appropriate similarity threshold), returns the cached response
   - If no match is found, forwards the request to the backend

2. **Response phase**: After receiving the backend response:
   - Evaluates the `cacheCondition` to determine if the response should be cached
   - If cacheable, stores the response (status, headers, body) with the vector and metadata in the vector store

### Metadata and filtering

The `parameters` configuration allows you to attach metadata to each cached vector. This metadata is used for:

- **Filtering queries**: Ensure caching is scoped appropriately (e.g., per API, per user, per plan)
- **Privacy**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

Example use cases:
- Scope cache per API: `{#context.attributes['api']}`
- Scope cache per user: `{#context.attributes['user-id']}`
- Scope cache per plan: `{#context.attributes['plan']}`

### Best practices

1. **Use JSONPath for complex payloads**: When working with structured data like LLM chat completions, extract only the relevant content:
   ```
   {#jsonPath(#request.content, '$.messages[-1:].content')}
   ```

2. **Set appropriate cache conditions**: Avoid caching errors or non-deterministic responses:
   ```
   {#response.status >= 200 && #response.status < 300}
   ```

3. **Use encoded parameters for sensitive data**: When using user IDs or other PII as metadata filters:
   ```json
   {
     "key": "user_context",
     "value": "{#context.attributes['user-id']}",
     "encode": true
   }
   ```

4. **Configure vector store similarity thresholds**: Configure your vector store resource with an appropriate similarity threshold to balance cache hit rate and accuracy.

### Limitations

- The quality of semantic matching depends on the embedding model and vector store configuration
- Not suitable for APIs with highly dynamic or personalized responses

### Overview

The AI Semantic Caching policy enables semantic caching of responses based on the similarity of request content. Unlike traditional HTTP caching policies that rely on exact request matching, this policy uses vector embeddings and similarity thresholds to identify semantically equivalent requests, even when phrased differently.

The policy integrates with Gravitee AI resources (text embedding models and vector stores) to provide intelligent caching decisions through Gravitee EL expressions.

### How it works

#### Request phase

When a request arrives, the policy:

1. Extracts content using the `promptExpression` (default: entire request body)
2. Generates a vector embedding using the configured embedding model
3. Searches the vector store for similar cached vectors using metadata filters
4. If a similar vector is found based on the configured similarity threshold, returns the cached response
5. If no match is found, forwards the request to the backend

#### Response phase

After receiving the backend response, the policy:

1. Evaluates the `cacheCondition` to determine if the response should be cached
2. If cacheable, stores the response (status, headers, body) with the vector and metadata in the vector store

### When to use semantic caching

Use semantic caching when:

- Working with LLM or AI workloads where users submit similar but not identical requests
- Request variations are lexically different but semantically equivalent (e.g., "What's the weather?" vs. "Tell me the current weather conditions")
- Token efficiency and reduced latency are priorities for LLM-backed APIs

Use traditional HTTP caching when:

- Requests must match exactly (same URL, headers, parameters)
- Working with non-AI APIs where semantic similarity isn't relevant
- Deterministic, byte-for-byte request matching is required

### Prerequisites

Before using this policy, configure the following Gravitee resources:

- **AI Text Embedding Model Resource**: Provides vector embeddings for semantic comparison
- **Vector Store Resource**: Stores and retrieves vectors (e.g., Redis with vector capabilities)

These resources must be configured at the API or platform level before adding the policy to your flow.

### Metadata and filtering

The `parameters` configuration allows you to attach metadata to each cached vector. This metadata is used for:

- **Filtering queries**: Ensure caching is scoped appropriately (e.g., per API, per user, per plan)
- **Privacy**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

Example use cases:

- Scope cache per API: `{#context.attributes['api']}`
- Scope cache per user: `{#context.attributes['user-id']}`
- Scope cache per plan: `{#context.attributes['plan']}`

### Best practices

#### Use JSONPath for complex payloads

When working with structured data like LLM chat completions, extract only the relevant content:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

#### Set appropriate cache conditions

Avoid caching errors or non-deterministic responses:

```
{#response.status >= 200 && #response.status < 300}
```

#### Use encoded parameters for sensitive data

When using user IDs or other PII as metadata filters:

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

#### Configure similarity thresholds

Configure your vector store resource with appropriate similarity thresholds to balance cache hit rate vs. accuracy.

### Limitations

- The quality of semantic matching depends on the embedding model and vector store configuration
- Not suitable for APIs with highly dynamic or personalized responses

### Enable semantic caching (optional)

For production deployments, you can enable the AI Semantic Caching policy to reduce costs and latency by reusing cached responses for semantically similar requests.

#### How semantic caching works

The AI Semantic Caching policy uses vector embeddings to identify semantically equivalent requests, even when phrased differently. When enabled:

1. Incoming requests are converted to vector representations using a text embedding model
2. The policy searches a vector store for similar cached vectors
3. If a match is found, the cached response is returned immediately
4. If no match exists, the request is forwarded to the LLM backend and the response is cached for future use

This approach saves computation and reduces latency for production LLM Proxy APIs.

#### Prerequisites

Before enabling semantic caching, configure the following resources at the API or platform level:

- **AI Text Embedding Model Resource**: Converts text to vector representations
- **Vector Store Resource**: Stores and retrieves vectors (e.g., Redis with vector capabilities)

#### Add the policy to your API

1. Navigate to your LLM Proxy API in the APIM Console
2. Go to the **Policies** section
3. Add the **AI Semantic Caching** policy to the request phase
4. Configure the policy:
   - Select your configured embedding model resource
   - Select your configured vector store resource
   - (Optional) Customize the `promptExpression` to extract specific content from requests
   - (Optional) Set a `cacheCondition` to control which responses are cached

#### Example configuration

```json
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
```

{% hint style="info" %}
The quality of semantic matching depends on your embedding model and vector store configuration. Configure your vector store resource with an appropriate similarity threshold to balance cache hit rate and accuracy.
{% endhint %}