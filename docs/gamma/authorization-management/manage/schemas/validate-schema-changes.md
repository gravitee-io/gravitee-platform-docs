---
hidden: false
noIndex: true
---

# Validate schema changes

Understand how the console validates schema changes before saving and what errors to expect.

{% hint style="warning" %}
This feature is under active development and may not be available in all environments at this time.
<!-- GAP: Schema validation backend endpoint behavior and specific error codes need SME confirmation. Current documentation covers the client-side validation UX from SchemaPage.tsx and useSchemaValidation.ts. -->
{% endhint %}

## Validation pipeline

Schema validation happens at two stages:

### 1. Client-side validation (real-time)

While you edit the schema in the Monaco editor, the console sends the draft text to the backend's schema validation endpoint. Results appear immediately:

| Result | UI behavior |
|--------|-------------|
| **Valid** | No alerts shown; **Save** button is enabled |
| **Parse errors** | A destructive alert lists each error. **Save** button is disabled |
| **Validation unavailable** | An informational alert: "Could not reach the schema validator, so this draft has not been checked." **Save** button remains enabled |

### 2. Server-side validation (on save)

The backend validates the schema again when you click **Save**. If validation fails server-side, the save is rejected and an error alert appears: "Could not save schema."

## Common validation errors

| Error type | Cause |
|-----------|-------|
| **Unknown entity type** | Referencing a type in `appliesTo` that is not declared in `entityTypes` |
| **Circular membership** | A type declaring `memberOfTypes` that creates a cycle |
| **Duplicate type name** | Two entity types with the same name in the same namespace |
| **Invalid attribute type** | Using an unsupported attribute type |

## Schema validation response

The backend returns a `SchemaValidation` response:

```json
{
  "valid": false,
  "errors": [
    "Entity type 'UnknownType' referenced in action 'invoke' appliesTo.resourceTypes is not defined"
  ]
}
```

## Next steps

* [Edit your schema](edit-your-schema.md) — Modify an existing schema
* [Schema generation](schema-generation.md) — Schema structure reference
