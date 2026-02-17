## Overview

The AI Semantic Caching policy enables semantic caching of responses based on the similarity of request content. Unlike traditional caching mechanisms that rely on exact text matching, this policy uses vector embeddings to identify semantically equivalent requests, even when phrased differently.

When a request arrives, the policy transforms the request content into a vector representation using an embedding model, then searches a vector store for similar cached vectors. If a semantically similar request is found, the cached response is returned immediately, reducing latency and LLM token consumption. If no match is found, the request is forwarded to the backend, and the response is cached for future use.

## How it works

The policy operates in two phases:

**Request phase:**
1. Extracts content from the incoming request using the `promptExpression` (defaults to the entire request body)
2. Generates a vector embedding using the configured AI Text Embedding Model Resource
3. Searches the vector store for similar cached vectors using metadata filters
4. If a similar vector is found based on the similarity threshold, returns the cached response
5. If no match is found, forwards the request to the backend

**Response phase:**
1. Evaluates the `cacheCondition` expression to determine if the response should be cached
2. If the condition is met, stores the response (status, headers, body) with the vector and metadata in the vector store

## Prerequisites

Before using this policy, configure the following Gravitee resources at the API or platform level:

- **AI Text Embedding Model Resource**: Provides vector embeddings for request content (e.g., `gravitee-resource-ai-model-text-embedding`)
- **Vector Store Resource**: Stores and retrieves vectors with associated cached responses (e.g., `gravitee-resource-ai-vector-store-redis`)

## Configuration

### Embedding model resource
**Required**  
`modelName` (string)

The name of the AI Text Embedding Model Resource to use for generating vector embeddings.

### Vector store resource
**Required**  
`vectorStoreName` (string)

The name of the Vector Store Resource to use for storing and retrieving cached vectors and responses.

### Prompt expression
**Optional**  
`promptExpression` (string)  
Default: `{#request.content}`

An expression that extracts the content to be used for semantic comparison. Use Gravitee Expression Language (EL) to specify which part of the request should be cached. For complex payloads, use JSONPath to extract specific fields.

Example for LLM chat completions:
```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

### Cache condition
**Optional**  
`cacheCondition` (string)  
Default: `{#response.status >= 200 && #response.status < 300}`

An expression that determines whether a response should be cached. Use Gravitee Expression Language (EL) to define the caching criteria based on response attributes.

Example to cache only successful responses:
```
{#response.status == 200}
```

### Parameters
**Optional**  
`parameters` (array)  
Default: 
```json
[
  {
    "key": "retrieval_context_key",
    "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
    "encode": true
  }
]
```

Metadata parameters attached to each cached vector. These parameters are used to filter cache queries and scope caching appropriately.

Each parameter object contains:
- **Parameter name** (`key`, string): The metadata key
- **Parameter value** (`value`, string): The metadata value, specified using Gravitee Expression Language (EL)
- **Encode value** (`encode`, boolean): When `true`, hashes the value using MurmurHash3 (Base64 encoded) to protect sensitive information

## Metadata filtering use cases

The `parameters` array enables fine-grained cache scoping:

- **Scope per API**: `{#context.attributes['api']}`
- **Scope per user**: `{#context.attributes['user-id']}`
- **Scope per plan**: `{#context.attributes['plan']}`
- **Combined scoping**: `{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}`

Use `encode: true` when including personally identifiable information (PII) or other sensitive data in metadata filters.

## Best practices

**Use JSONPath for complex payloads**  
When working with structured data like LLM chat completions, extract only the relevant content:
```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

**Set appropriate cache conditions**  
Avoid caching errors or non-deterministic responses:
```
{#response.status >= 200 && #response.status < 300}
```

**Use encoded parameters for sensitive data**  
When using user IDs or other PII as metadata filters:
```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

**Configure appropriate similarity thresholds**  
Configure your vector store resource with appropriate similarity thresholds to balance cache hit rate versus accuracy.

## Limitations

- The quality of semantic matching depends on the embedding model and vector store configuration
- Not suitable for APIs with highly dynamic or personalized responses
- Cache effectiveness depends on the similarity threshold configured in the vector store resource

## Examples

{% tabs %}
{% tab title="LLM Proxy with JSONPath extraction" %}
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
{% endtab %}

{% tab title="Custom cache condition" %}
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
{% endtab %}
{% endtabs %}

## Changelog

### 1.0.0-alpha.1 (2026-01-23)

**Bug Fixes**
- Adjusted vector store API changes and bumped Gravitee dependencies ([4a51f4f](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/4a51f4f80eb0d1905b70a91bb557b98285491256))
- Fixed tests ([bcadf21](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/bcadf211aae346d090aa00e83ccd58903b4134a8))

**Features**
- Adapted vector store API ([2188076](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/218807623d47acb26b1cff6e7eea608f111b7816))
- Enabled policy for LLM proxy ([9ac20b7](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/9ac20b7a0de8028d0bef165f9d09d28fa2838511))
- First import ([5547a51](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/5547a51a9e1a24429386ebf8bea70456751a2f51))
- Prepared policy for Enterprise Edition ([800d037](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/800d0378f7d9a04faa5e9ee5846ab563e0a0e51d))
- Updated inference service version ([#2](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/issues/2)) ([8595387](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/8595387dc9a82b17caffed9bce1985d224885f2d))
