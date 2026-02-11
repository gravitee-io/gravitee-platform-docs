## Best Practices

### Use JSONPath for Complex Payloads

When working with structured data like LLM chat completions, extract only the relevant content instead of caching the entire request body. This improves cache hit rates by focusing on the semantic meaning of the user's actual query.

**Example**: For OpenAI-compatible chat completions, extract the last message content:

```
{#jsonPath(#request.content, '$.messages[-1:].content')}
```

This approach:
- Reduces noise in the vector representation
- Increases the likelihood of semantic matches
- Focuses caching on user intent rather than API structure

### Set Appropriate Cache Conditions

Avoid caching errors or non-deterministic responses by using the `cacheCondition` parameter. Only cache responses that represent valid, reusable results.

**Recommended condition**:

```
{#response.status >= 200 && #response.status < 300}
```

**Alternative for strict success-only caching**:

```
{#response.status == 200}
```

This prevents:
- Caching error responses that shouldn't be reused
- Storing partial or failed LLM outputs
- Serving stale error states to subsequent requests

### Use Encoded Parameters for Sensitive Data

When using user IDs or other personally identifiable information (PII) as metadata filters, enable the `encode` option. This hashes sensitive values using MurmurHash3 (Base64 encoded) before storing them in the vector store.

**Example configuration**:

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

This approach:
- Protects user privacy in the vector store
- Maintains filtering functionality without exposing raw PII
- Complies with data protection requirements

### Scope Cache Appropriately with Metadata

Use the `parameters` configuration to attach metadata that defines cache scope. This ensures cached responses are served only to the appropriate context.

**Common scoping patterns**:

- **Per API**: `{#context.attributes['api']}`
- **Per user**: `{#context.attributes['user-id']}`
- **Per plan**: `{#context.attributes['plan']}`
- **Combined scope**: `{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}`

Proper scoping prevents:
- Serving cached responses across different APIs or plans
- Privacy violations from cross-user cache hits
- Incorrect responses due to context mismatch

### Configure Vector Store Similarity Thresholds

The quality of semantic matching depends on the similarity threshold configured in your vector store resource. Balance cache hit rate against accuracy by adjusting this threshold.

**Considerations**:
- **Lower thresholds** (e.g., 0.7): Higher cache hit rate, but may return less precise matches
- **Higher thresholds** (e.g., 0.9): More precise matches, but lower cache hit rate
- **Recommended starting point**: 0.8 for most use cases

Test and adjust the threshold based on your specific LLM use case and acceptable trade-offs between token savings and response accuracy.

### Understand Policy Limitations

The AI Semantic Caching policy is not suitable for all scenarios. Avoid using it when:

- **Highly dynamic responses are required**: The policy caches based on semantic similarity, which assumes similar queries should receive similar responses
- **Personalized content is critical**: Even with user-scoped metadata, responses may not capture fine-grained personalization
- **Real-time data is essential**: Cached responses may not reflect the latest information

The quality of semantic matching depends on:
- The embedding model configuration
- The vector store implementation and similarity algorithm
- The prompt extraction strategy (JSONPath, summarization, etc.)

<!-- GAP: No source material specifies recommended embedding models, vector store configuration details, or performance benchmarks for different threshold values -->