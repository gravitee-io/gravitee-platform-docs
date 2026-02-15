## Overview

The AI Semantic Caching policy (version 1.0.0-alpha.1) is available for LLM proxy APIs in APIM 4.11.x and above. This alpha release enables semantic caching of responses based on the similarity of request content, reducing LLM token usage and latency.

### Key features

- **Semantic matching**: Uses vector embeddings to identify semantically equivalent requests, even when phrased differently
- **Flexible caching logic**: Configurable cache conditions using Gravitee EL expressions
- **Metadata filtering**: Scope caching per API, user, or plan with optional encoding for sensitive data
- **JSONPath support**: Extract specific content from complex payloads for more accurate caching

### Requirements

- APIM 4.11.x or above
- Java 21 or above
- LLM proxy API type
- Agent mesh packaging

## Prerequisites

Before using this policy, configure the following resources at the API or platform level:

- **AI Text Embedding Model Resource**: Converts text into vector representations
- **Vector Store Resource**: Stores and retrieves vectors (Redis recommended for initial deployments)

## How it works

### Request phase

1. Extracts content using the configured `promptExpression` (defaults to full request body)
2. Generates a vector embedding via the embedding model
3. Searches the vector store for similar cached vectors using metadata filters
4. Returns cached response if a match is found above the similarity threshold
5. Forwards request to backend if no match exists

### Response phase

1. Evaluates the `cacheCondition` to determine if the response should be cached
2. Stores the response (status, headers, body) with its vector and metadata in the vector store if cacheable

## Configuration

### Prompt expression

Customize content extraction for semantic matching. The default uses the full request body, but you can extract specific content using Gravitee EL expressions.

Example for chat completions:
```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

### Cache condition

Control what gets cached using Gravitee EL expressions. Default condition:
```
{#response.status >= 200 && #response.status < 300}
```

### Parameters

Attach metadata for filtering and privacy. Parameters support encoding for sensitive values, allowing you to scope caching per API, user, or plan.

## Analytics

Analytics include cache hit information, enabling dashboards to display metrics such as cache hit percentage and token savings.

## Known limitations

- **Alpha release**: Intended for testing and feedback
- **Semantic matching quality**: Depends on embedding model and vector store configuration
- **Response suitability**: Not suitable for highly dynamic or personalized responses