---
description: Learn how to configure and use the AI Vector Cache policy in Gravitee APIM 4.10
---

# AI Vector Cache

## Metadata and Filtering

The `parameters` configuration allows you to attach metadata to each cached vector. This metadata is used to filter queries and ensure caching is scoped appropriately.

### Use Cases

Metadata filtering enables:

- **API-scoped caching**: Cache responses separately per API
- **User-scoped caching**: Cache responses separately per user
- **Plan-scoped caching**: Cache responses separately per subscription plan
- **Privacy protection**: Hash sensitive values to prevent exposure

### Configuration

Each parameter consists of:

- **key**: The metadata field name
- **value**: A Gravitee EL expression that resolves to the metadata value
- **encode**: (optional) When `true`, hashes the value using MurmurHash3 (Base64 encoded)

### Examples

**Scope cache per API:**

```json
{
  "key": "api_context",
  "value": "{#context.attributes['api']}",
  "encode": false
}
```

**Scope cache per user (with encoding):**

```json
{
  "key": "user_context",
  "value": "{#context.attributes['user-id']}",
  "encode": true
}
```

**Scope cache per plan:**

```json
{
  "key": "plan_context",
  "value": "{#context.attributes['plan']}",
  "encode": false
}
```

**Combined scoping:**

```json
{
  "key": "retrieval_context_key",
  "value": "{#context.attributes['api']}_{#context.attributes['plan']}_{#context.attributes['user-id']}",
  "encode": true
}
```

### Privacy Considerations

Use `encode: true` when the metadata value contains:

- User IDs
- Email addresses
- Session tokens
- Any other personally identifiable information (PII)

Encoding prevents sensitive values from being stored in plaintext in the vector store while maintaining filtering functionality.