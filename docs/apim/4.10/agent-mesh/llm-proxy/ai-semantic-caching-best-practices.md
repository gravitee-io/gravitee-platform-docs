# AI Semantic Caching Best Practices

## Best practices

### Use JSONPath for complex payloads

When working with structured data like LLM chat completions, extract only the relevant content instead of caching the entire request body. This improves cache hit rates by focusing on the semantic meaning of the user's actual prompt.

**Example:**
```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This expression extracts only the last message content from an OpenAI-compatible chat completion request, ignoring system messages, conversation history, and other metadata that may vary between requests.

### Set appropriate cache conditions

Avoid caching errors or non-deterministic responses by using the `cacheCondition` parameter. Only cache responses that meet your quality and reliability requirements.

**Example:**
```
{#response.status >= 200 && #response.status < 300}
```

This condition ensures only successful HTTP responses are cached. You can customize this based on your API's behavior:
- Cache only specific status codes: `{#response.status == 200}`
- Exclude certain error types: `{#response.status >= 200 && #response.status < 300 && #response.status != 204}`

### Use encoded parameters for sensitive data

When using user IDs, API keys, or other personally identifiable information (PII) as metadata filters, enable the `encode` option. This hashes the value using MurmurHash3 (Base64 encoded) before storing it in the vector store.

**Example:**
```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

This approach allows you to scope caching per user without exposing sensitive identifiers in the vector store.

### Configure vector store similarity thresholds

The quality of semantic matching depends on the similarity threshold configured in your vector store resource. Balance cache hit rate against accuracy:
- **Higher thresholds** (e.g., 0.9): More strict matching, fewer false positives, lower cache hit rate
- **Lower thresholds** (e.g., 0.7): More lenient matching, higher cache hit rate, potential for less precise matches

Test different threshold values based on your use case and monitor cache performance metrics.

### Scope cache appropriately with metadata

Use the `parameters` configuration to attach metadata that controls cache scope. This prevents unintended cache sharing across different contexts.

**Common scoping patterns:**
- **Per API**: `{#context.attributes['api']}`
- **Per user**: `{#context.attributes['user-id']}`
- **Per plan**: `{#context.attributes['plan']}`
- **Combined**: `{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}`

Choose the scoping strategy that matches your API's security and performance requirements.