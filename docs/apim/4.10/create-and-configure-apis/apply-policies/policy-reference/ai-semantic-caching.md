The AI Semantic Caching policy supports the following configuration options:

| Name<br>`json name` | Type<br>`constraint` | Mandatory | Default | Description |
|:--------------------|:---------------------|:---------:|:--------|:------------|
| Cache condition<br>`cacheCondition` | string | | `{#response.status >= 200 && #response.status < 300}` | Gravitee Expression Language condition determining whether a response should be cached |
| Embedding model resource<br>`modelName` | string | ✅ | | Name of the configured AI Text Embedding Model Resource |
| Parameters<br>`parameters` | array | | `[{"encode": true, "key": "retrieval_context_key", "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}"}]` | Metadata parameters to attach to cached vectors (using Gravitee Expression Language). See Parameters array schema table below. |
| Prompt expression<br>`promptExpression` | string | | `{#request.content}` | Gravitee Expression Language expression to extract content from the request |
| Vector store resource<br>`vectorStoreName` | string | ✅ | | Name of the configured Vector Store Resource |

**Parameters array schema:**

| Name<br>`json name` | Type<br>`constraint` | Mandatory | Default | Description |
|:--------------------|:---------------------|:---------:|:--------|:------------|
| Encode value<br>`encode` | boolean | | | Encode the value using MurmurHash3 (Base64 encoded) for sensitive information |
| Parameter name<br>`key` | string | | | Name of the metadata parameter |
| Parameter value<br>`value` | string | | | Value of the parameter (using Gravitee Expression Language) |

The following configuration fields support Gravitee Expression Language (EL):

* `promptExpression`: Extracts content from the request. Default: `{#request.content}`
* `cacheCondition`: Determines whether a response should be cached. Default: `{#response.status >= 200 && #response.status < 300}`
* `parameters[].value`: Defines metadata values for cache scoping and filtering

The `parameters` configuration attaches metadata to each cached vector. This metadata enables:

* **Scoped caching**: Ensure cache entries are scoped appropriately (e.g., per API, per user, per plan)
* **Privacy protection**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

<!-- GAP: No detailed explanation of MurmurHash3 encoding algorithm or Base64 encoding format is provided. Source only states 'hash sensitive values using MurmurHash3 (Base64 encoded)'. -->

Common metadata use cases:

* Scope cache per API: `{#context.attributes['api']}`
* Scope cache per user: `{#context.attributes['user-id']}`
* Scope cache per plan: `{#context.attributes['plan']}`

The default `parameters` configuration includes:

```json
[
  {
    "key": "retrieval_context_key",
    "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
    "encode": true
  }
]
```

This default configuration scopes the cache per API, plan, and user, with encoded values to protect sensitive identifiers.

When working with structured data like LLM chat completions, extract only the relevant content using JSONPath:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This approach reduces noise in the vector embedding and improves semantic matching accuracy.

Avoid caching errors or non-deterministic responses by configuring the `cacheCondition` to cache only successful responses:

```
{#response.status >= 200 && #response.status < 300}
```

This ensures only valid responses are stored in the cache.

When using user IDs or other personally identifiable information as metadata filters, enable encoding to protect sensitive values:

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

The `encode: true` setting hashes the value using MurmurHash3 (Base64 encoded) before storing it in the vector store.

Configure your vector store resource with appropriate similarity thresholds to balance cache hit rate versus accuracy. Higher thresholds require closer semantic matches, reducing false positives but potentially lowering cache hit rates. Lower thresholds increase cache hits but may return less relevant cached responses.

<!-- GAP: No specific similarity threshold recommendations or cache hit rate benchmarks are provided -->

**Limitations:**

* The quality of semantic matching depends on the embedding model and vector store configuration
* Not suitable for APIs with highly dynamic or personalized responses where each request requires a unique response


This example demonstrates caching OpenAI-compatible chat completions by extracting the last message content. The cache is scoped per API using encoded metadata to protect sensitive identifiers.

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


This example caches only responses with HTTP status code 200. No metadata parameters are used, allowing cache sharing across all requests.

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


**Bug fixes:**

* Adjust vector-store API changes and bump Gravitee dependencies ([4a51f4f](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/4a51f4f80eb0d1905b70a91bb557b98285491256))
* Fix tests ([bcadf21](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/bcadf211aae346d090aa00e83ccd58903b4134a8))

**Features:**

* Adapt vector store API ([2188076](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/218807623d47acb26b1cff6e7eea608f111b7816))
* Enable policy for LLM Proxy ([9ac20b7](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/9ac20b7a0de8028d0bef165f9d09d28fa2838511))
* First import ([5547a51](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/5547a51a9e1a24429386ebf8bea70456751a2f51))
* Prepare policy for EE ([800d037](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/800d0378f7d9a04faa5e9ee5846ab563e0a0e51d))
* Update inference service version ([#2](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/issues/2)) ([8595387](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/8595387dc9a82b17caffed9bce1985d224885f2d))