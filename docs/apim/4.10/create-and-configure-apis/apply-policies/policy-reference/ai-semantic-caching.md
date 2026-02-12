The AI Semantic Caching policy enables semantic caching of responses based on the similarity of request content. Unlike traditional caching mechanisms that rely on exact text matching, this policy uses vector embeddings to identify semantically equivalent requests, even when phrased differently.

When a request arrives, the policy converts the request content into a vector representation using an embedding model, then searches a vector store for similar cached vectors. If a match is found, the cached response is returned immediately, reducing LLM token consumption and latency. If no match exists, the request is forwarded to the backend, and the response is cached for future use.


The AI Semantic Caching policy operates in two phases:

**Request phase:**

1. Extract content from the incoming request using the `promptExpression` (defaults to the entire request body)
2. Generate a vector embedding using the configured embedding model
3. Search the vector store for similar cached vectors using metadata filters
4. If a similar vector is found based on the vector store's similarity threshold, return the cached response
5. If no match is found, forward the request to the backend

**Response phase:**

1. Evaluate the `cacheCondition` to determine if the response should be cached
2. If cacheable, store the response (status, headers, body) with the vector and metadata in the vector store


Before using this policy, configure the following Gravitee resources at the API or platform level:

* **AI Text Embedding Model Resource**: Converts text into vector embeddings (e.g., `gravitee-resource-ai-model-text-embedding`)
* **Vector Store Resource**: Stores and retrieves vectors (e.g., `gravitee-resource-ai-vector-store-redis`)


The AI Semantic Caching policy can be applied to the following API types:

* LLM Proxy


The AI Semantic Caching policy can be applied in the following flow phase:

* Request


The following table lists plugin version compatibility with APIM and Java.

| Plugin version | APIM version | Java version |
|:---------------|:-------------|:-------------|
| 1.x            | 4.11.x+      | 21+          |


| Name<br>`json name` | Type<br>`constraint` | Mandatory | Default | Description |
|:--------------------|:---------------------|:---------:|:--------|:------------|
| Cache condition<br>`cacheCondition` | string | | `{#response.status >= 200 && #response.status < 300}` | Expression Language condition determining whether a response should be cached |
| Embedding model resource<br>`modelName` | string | ✅ | | Name of the configured AI Text Embedding Model Resource |
| Parameters<br>`parameters` | array | | `[{"encode": true, "key": "retrieval_context_key", "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}"}]` | Metadata parameters to attach to cached vectors (using Expression Language) |
| Prompt expression<br>`promptExpression` | string | | `{#request.content}` | Expression Language expression to extract content from the request |
| Vector store resource<br>`vectorStoreName` | string | ✅ | | Name of the configured Vector Store Resource |


| Name<br>`json name` | Type<br>`constraint` | Mandatory | Default | Description |
|:--------------------|:---------------------|:---------:|:--------|:------------|
| Encode value<br>`encode` | boolean | | | Encode the value using MurmurHash3 (for sensitive information) |
| Parameter name<br>`key` | string | | | Name of the metadata parameter |
| Parameter value<br>`value` | string | | | Value of the parameter (using Expression Language) |


The `parameters` configuration attaches metadata to each cached vector. This metadata enables:

* **Scoped caching**: Ensure cache entries are scoped appropriately (e.g., per API, per user, per plan)
* **Privacy protection**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

Common metadata use cases:

* Scope cache per API: `{#context.attributes['api']}`
* Scope cache per user: `{#context.attributes['user-id']}`
* Scope cache per plan: `{#context.attributes['plan']}`


When working with structured data like LLM chat completions, extract only the relevant content:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```


Avoid caching errors or non-deterministic responses:

```
{#response.status >= 200 && #response.status < 300}
```


When using user IDs or other personally identifiable information as metadata filters:

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```


Configure your vector store resource with appropriate similarity thresholds to balance cache hit rate versus accuracy.

<!-- GAP: No specific similarity threshold values are provided in the source. The draft mentions 'appropriate similarity thresholds' but gives no numeric guidance. -->


* The quality of semantic matching depends on the embedding model and vector store configuration
* Not suitable for APIs with highly dynamic or personalized responses


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


* Adjust vector-store API changes and bump Gravitee dependencies ([4a51f4f](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/4a51f4f80eb0d1905b70a91bb557b98285491256))
* Fix tests ([bcadf21](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/bcadf211aae346d090aa00e83ccd58903b4134a8))


* Adapt vector store API ([2188076](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/218807623d47acb26b1cff6e7eea608f111b7816))
* Enable policy for LLM Proxy ([9ac20b7](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/9ac20b7a0de8028d0bef165f9d09d28fa2838511))
* First import ([5547a51](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/5547a51a9e1a24429386ebf8bea70456751a2f51))
* Prepare policy for EE ([800d037](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/800d0378f7d9a04faa5e9ee5846ab563e0a0e51d))
* Update inference service version ([#2](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/issues/2)) ([8595387](https://github.com/gravitee-io/gravitee-policy-ai-semantic-caching/commit/8595387dc9a82b17caffed9bce1985d224885f2d))

<!-- GAP: No guidance on how to test or validate the policy configuration. -->