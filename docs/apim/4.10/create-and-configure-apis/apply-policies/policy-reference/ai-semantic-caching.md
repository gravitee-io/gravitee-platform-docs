## Overview

The AI Semantic Caching policy enables semantic caching of responses based on the similarity of request content. It uses an embedding model to transform incoming requests into vector representations, then compares them against previously cached vectors in a vector store. If a similar context is found, the cached response can be reused, reducing LLM token consumption and latency.

The policy integrates with Gravitee AI resources such as text embedding models and vector stores, providing flexible caching decisions through Gravitee Expression Language (EL).

## How it works

The policy operates in two phases:

### Request phase

When a request arrives, the policy:

1. Extracts content using the `promptExpression` (default: entire request body)
2. Generates a vector embedding using the configured embedding model
3. Searches the vector store for similar cached vectors using metadata filters
4. If a similar vector is found (based on similarity threshold), returns the cached response
5. If no match, forwards the request to the backend

### Response phase

After receiving the backend response:

1. Evaluates the `cacheCondition` to determine if the response should be cached
2. If cacheable, stores the response (status, headers, body) with the vector and metadata in the vector store

## Prerequisites

Before using this policy, you must configure the following Gravitee resources:

* **AI Text Embedding Model Resource**: Provides vector embeddings (e.g., `gravitee-resource-ai-model-text-embedding`)
* **Vector Store Resource**: Stores and retrieves vectors (e.g., `gravitee-resource-ai-vector-store-redis`)

These resources must be configured at the API or platform level before adding the policy to your flow.

## Metadata and filtering

The `parameters` configuration allows you to attach metadata to each cached vector. This metadata is used for:

* **Filtering queries**: Ensure caching is scoped appropriately (e.g., per API, per user, per plan)
* **Privacy**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

Example use cases:

* Scope cache per API: `{#context.attributes['api']}`
* Scope cache per user: `{#context.attributes['user-id']}`
* Scope cache per plan: `{#context.attributes['plan']}`

## Best practices

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

4. **Consider vector store similarity thresholds**: Configure your vector store resource with appropriate similarity thresholds to balance cache hit rate vs accuracy.

## Limitations

* The quality of semantic matching depends on the embedding model and vector store configuration
* Not suitable for APIs with highly dynamic or personalized responses

## Phases

The `ai-semantic-caching` policy can be applied to the following API types and flow phases.

### Compatible API types

* `LLM PROXY`

### Supported flow phases

* Request

## Compatibility matrix

| Plugin version | APIM | Java version |
| --- | --- | --- |
| 1.x | 4.11.x and above | 21+ |

## Configuration

You can configure the policy with the following options:

| Name <br>`json name` | Type <br>`constraint` | Mandatory | Default | Description |
|:---------------------|:----------------------|:---------:|:--------|:------------|
| Cache condition<br>`cacheCondition` | string | | `{#response.status >= 200 && #response.status < 300}` | Expression to determine if response should be cached |
| Embedding model resource<br>`modelName` | string | ✅ | | Name of the AI Text Embedding Model resource |
| Parameters<br>`parameters` | array | | `[{"encode": true, "key": "retrieval_context_key", "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}"}]` | Parameters to provide as metadata (using EL)<br/>See "Parameters" section |
| Prompt expression<br>`promptExpression` | string | | `{#request.content}` | Expression to extract content for vectorization |
| Vector store resource<br>`vectorStoreName` | string | ✅ | | Name of the Vector Store resource |

### Parameters (Array)

| Name <br>`json name` | Type <br>`constraint` | Mandatory | Default | Description |
|:---------------------|:----------------------|:---------:|:--------|:------------|
| Encode value<br>`encode` | boolean | | | Encode the value to use as index (in case of sensitive information) |
| Parameter name<br>`key` | string | | | Name of the parameter |
| parameterValue<br>`value` | string | | | Value of the parameter (using EL) |

## Examples

### LLM Proxy with JSONPath extraction

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

### Custom cache condition

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

* adjust vector-store api changes + bump gravitee deps ([4a51f4f](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/4a51f4f80eb0d1905b70a91bb557b98285491256))
* tests ([bcadf21](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/bcadf211aae346d090aa00e83ccd58903b4134a8))

#### Features

* adapt vector store api ([2188076](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/218807623d47acb26b1cff6e7eea608f111b7816))
* enable policy for LLM proxy ([9ac20b7](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/9ac20b7a0de8028d0bef165f9d09d28fa2838511))
* first import ([5547a51](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/5547a51a9e1a24429386ebf8bea70456751a2f51))
* prepare policy for EE ([800d037](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/800d0378f7d9a04faa5e9ee5846ab563e0a0e51d))
* update inference service version ([#2](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/issues/2)) ([8595387](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/8595387dc9a82b17caffed9bce1985d224885f2d))