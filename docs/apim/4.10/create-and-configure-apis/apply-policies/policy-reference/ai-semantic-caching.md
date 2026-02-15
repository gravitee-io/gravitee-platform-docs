## Overview

The AI Semantic Caching policy enables semantic caching of responses based on the similarity of request content. Unlike traditional caching mechanisms that rely on exact text matching, this policy uses vector embeddings to identify semantically equivalent requests, even when phrased differently.

When a request arrives, the policy converts it into a vector representation using an embedding model, then searches a vector store for similar cached vectors. If a match is found above the configured similarity threshold, the cached response is returned immediately. Otherwise, the request is forwarded to the backend, and the response is cached for future use.

This approach reduces LLM token consumption and API response latency by avoiding redundant processing of semantically equivalent queries.

## Prerequisites

Before using this policy, configure the following Gravitee resources:

- **AI Text Embedding Model Resource**: Converts text into vector embeddings (e.g., `gravitee-resource-ai-model-text-embedding`)
- **Vector Store Resource**: Stores and retrieves vectors (e.g., `gravitee-resource-ai-vector-store-redis`)

These resources must be configured at the API or platform level before adding the policy to your flow.

## How it works

The policy operates in two phases:

### Request phase

1. Extracts content from the incoming request using the `promptExpression` (default: entire request body)
2. Generates a vector embedding using the configured embedding model
3. Searches the vector store for similar cached vectors using metadata filters
4. If a similar vector is found (based on the vector store's similarity threshold), returns the cached response immediately
5. If no match is found, forwards the request to the backend

### Response phase

1. Evaluates the `cacheCondition` to determine if the response should be cached
2. If cacheable, stores the response (status, headers, body) with the vector and metadata in the vector store

## Metadata and filtering

The `parameters` configuration attaches metadata to each cached vector. This metadata enables:

- **Scoped caching**: Ensure caching is scoped appropriately (e.g., per API, per user, per plan)
- **Privacy protection**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

Example use cases:
- Scope cache per API: `{#context.attributes['api']}`
- Scope cache per user: `{#context.attributes['user-id']}`
- Scope cache per plan: `{#context.attributes['plan']}`

## Configuration

### Options

<table data-full-width="true"><thead><tr><th width="200">Property</th><th width="100" data-type="checkbox">Required</th><th width="200">Description</th><th width="200">Type</th><th>Default</th></tr></thead><tbody><tr><td>Embedding model resource</td><td>true</td><td>Name of the AI Text Embedding Model Resource</td><td>string</td><td>N/A</td></tr><tr><td>Vector store resource</td><td>true</td><td>Name of the Vector Store Resource</td><td>string</td><td>N/A</td></tr><tr><td>Prompt expression</td><td>false</td><td>Expression to extract content for vectorization (supports EL)</td><td>string</td><td><code>{#request.content}</code></td></tr><tr><td>Cache condition</td><td>false</td><td>Condition to determine if response should be cached (supports EL)</td><td>string</td><td><code>{#response.status >= 200 && #response.status < 300}</code></td></tr><tr><td>Parameters</td><td>false</td><td>Metadata parameters for filtering and scoping</td><td>array</td><td>See below</td></tr></tbody></table>

### Parameters (Array)

<table data-full-width="true"><thead><tr><th width="200">Property</th><th width="100" data-type="checkbox">Required</th><th width="200">Description</th><th width="200">Type</th><th>Default</th></tr></thead><tbody><tr><td>Parameter name</td><td>false</td><td>Name of the metadata parameter</td><td>string</td><td>N/A</td></tr><tr><td>Parameter value</td><td>false</td><td>Value of the parameter (supports EL)</td><td>string</td><td>N/A</td></tr><tr><td>Encode value</td><td>false</td><td>Encode the value using MurmurHash3 for sensitive information</td><td>boolean</td><td><code>false</code></td></tr></tbody></table>

**Default parameters:**
```json
[
  {
    "key": "retrieval_context_key",
    "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
    "encode": true
  }
]
```

## Using Gravitee EL for dynamic configuration

The AI Semantic Caching policy uses Gravitee Expression Language (EL) extensively to configure its behavior dynamically. EL expressions allow you to extract content from requests, define caching conditions, and attach metadata for filtering.

### Prompt expression

The `promptExpression` parameter determines what content is used to generate the semantic vector. The default value is `{#request.content}`, which uses the entire request body.

For structured payloads like LLM chat completions, you can use JSONPath to extract only the relevant content:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This expression extracts the content of the last message in a chat completion request, ensuring that only the user's latest prompt is used for semantic matching.

**Common patterns:**

- Extract specific JSON fields: `{#jsonPath(#request.content, '$.prompt')}`
- Extract array elements: `{#jsonPath(#request.content, '$.messages[0].content')}`
- Extract nested properties: `{#jsonPath(#request.content, '$.data.query.text')}`

### Cache condition

The `cacheCondition` parameter controls whether a response should be cached. The default value is:

```
{#response.status >= 200 && #response.status < 300}
```

This expression caches only successful responses (HTTP 2xx status codes). You can customize this condition to match your requirements:

- Cache only specific status codes: `{#response.status == 200}`
- Cache based on response headers: `{#response.headers['x-cache-control'] == 'cacheable'}`
- Combine multiple conditions: `{#response.status == 200 && #response.headers['content-type'].contains('application/json')}`

### Metadata parameters

The `parameters` configuration allows you to attach metadata to each cached vector using EL expressions. This metadata is used to filter cache lookups, ensuring that cached responses are scoped appropriately.

**Default configuration:**

```json
{
  "key": "retrieval_context_key",
  "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
  "encode": true
}
```

This default configuration creates a composite key that scopes the cache by API, plan, and user ID. The `encode: true` setting hashes the value using MurmurHash3 (Base64 encoded) to protect sensitive information.

**Common metadata patterns:**

- Scope by API: `{#context.attributes['api']}`
- Scope by user: `{#context.attributes['user-id']}`
- Scope by plan: `{#context.attributes['plan']}`
- Scope by application: `{#context.attributes['application']}`
- Combine multiple attributes: `{#context.attributes['api']}_{#context.attributes['environment']}`

**Example with multiple metadata parameters:**

```json
"parameters": [
  {
    "key": "api_context",
    "value": "{#context.attributes['api']}",
    "encode": false
  },
  {
    "key": "user_context",
    "value": "{#context.attributes['user-id']}",
    "encode": true
  },
  {
    "key": "plan_context",
    "value": "{#context.attributes['plan']}",
    "encode": false
  }
]
```

This configuration creates three separate metadata fields, with the user ID encoded for privacy.

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

4. **Configure vector store similarity thresholds**: Set appropriate similarity thresholds at the vector store resource level to balance cache hit rate versus accuracy.

## Limitations

- The quality of semantic matching depends on the embedding model and vector store configuration
- Not suitable for APIs with highly dynamic or personalized responses
- Similarity thresholds are configured at the vector store resource level, not in the policy

## Phases

The `ai-semantic-caching` policy can be applied to the following API types and flow phases.

### Compatible API types

* `LLM_PROXY`

### Supported flow phases

* Request

## Compatibility matrix

| Plugin version | APIM | Java version |
|:---|:---|:---|
| 1.x | 4.11.x and above | 21+ |

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

### LLM chat completion with scoped caching

Cache chat completions with metadata scoped by API, plan, and user ID:

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
        "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
        "encode": true
      }
    ]
  }
}
```

This configuration:
1. Extracts only the last message content from chat completion requests
2. Caches only successful responses (2xx status codes)
3. Scopes the cache by API, plan, and user ID with encoded values for privacy

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