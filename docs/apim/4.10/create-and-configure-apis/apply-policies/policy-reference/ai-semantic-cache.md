## Metadata and Filtering

The `parameters` configuration allows you to attach metadata to each cached vector. This metadata serves two primary purposes:

- **Filtering queries**: Ensures caching is scoped appropriately (e.g., per API, per user, per plan)
- **Privacy**: Use `encode: true` to hash sensitive values using MurmurHash3 (Base64 encoded)

### Common Use Cases

Scope cache per API:
```json
{
  "key": "api_context",
  "value": "{#context.attributes['api']}",
  "encode": false
}
```

Scope cache per user:
```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

Scope cache per plan:
```json
{
  "key": "plan_context",
  "value": "{#context.attributes['plan']}",
  "encode": false
}
```

Combine multiple filters:
```json
{
  "parameters": [
    {
      "key": "retrieval_context_key",
      "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
      "encode": true
    }
  ]
}
```

### Privacy Considerations

When using user IDs or other personally identifiable information (PII) as metadata filters, enable encoding to protect sensitive data:

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

The `encode` parameter applies MurmurHash3 hashing with Base64 encoding to the value before storing it in the vector store. This ensures sensitive information is not stored in plain text while maintaining the ability to filter cached results by user context.