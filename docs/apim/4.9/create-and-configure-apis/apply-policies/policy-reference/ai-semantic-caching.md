---
description: Working JSON configuration examples for common AI Semantic Caching policy use cases.
---

# AI Semantic Caching policy examples

## Overview

This guide provides working JSON configuration examples for common AI Semantic Caching policy use cases. Each example includes a complete API definition and explains what the configuration demonstrates.

## Example 1: LLM Proxy with JSONPath extraction

This example demonstrates how to cache OpenAI-compatible chat completions by extracting the last message content using JSONPath.

### What this example demonstrates

* Using JSONPath to extract specific content from structured payloads
* Caching only successful responses with status code validation
* Scoping cache entries per API using encoded metadata

### Configuration

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

### Configuration variations

You can modify the following parameters to customize the behavior:

* **promptExpression**: Change the JSONPath expression to extract different parts of the request payload
* **cacheCondition**: Adjust the status code range or add additional conditions
* **parameters**: Add more metadata filters to scope cache entries by plan, user, or other attributes

## Example 2: Custom cache condition

This example demonstrates how to cache only successful responses with a custom status code check.

### What this example demonstrates

* Using a strict status code check for cache eligibility
* Caching the entire request body without extraction
* Minimal metadata configuration

### Configuration

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

### Configuration variations

You can modify the following parameters to customize the behavior:

* **cacheCondition**: Change the status code or add additional response validation logic
* **promptExpression**: Add JSONPath extraction if you need to cache only specific parts of the request
* **parameters**: Add metadata filters to scope cache entries by context attributes