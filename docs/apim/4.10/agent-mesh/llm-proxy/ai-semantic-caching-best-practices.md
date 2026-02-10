# AI Semantic Caching best practices

## Best practices

### Use JSONPath for complex payloads
When working with structured data like LLM chat completions, extract only the relevant content using JSONPath expressions. This ensures the embedding model processes the most meaningful part of the request:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

### Set appropriate cache conditions
Avoid caching errors or non-deterministic responses by configuring the `cacheCondition` parameter. The default condition caches only successful responses:

```
{#response.status >= 200 && #response.status < 300}
```

You can customize this condition based on your requirements. For example, to cache only HTTP 200 responses:

```
{#response.status == 200}
```

### Use encoded parameters for sensitive data
When using user IDs or other personally identifiable information (PII) as metadata filters, enable the `encode` option to hash values using MurmurHash3 (Base64 encoded):

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

### Configure vector store similarity thresholds
The quality of semantic matching depends on the similarity threshold configured in your vector store resource. Balance cache hit rate against accuracy by adjusting this threshold based on your use case.

## Examples

### Cache OpenAI-compatible chat completions
This example demonstrates caching chat completions by extracting the last message content using JSONPath:

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

### Cache only successful responses
This example demonstrates a custom cache condition that caches only HTTP 200 responses:

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