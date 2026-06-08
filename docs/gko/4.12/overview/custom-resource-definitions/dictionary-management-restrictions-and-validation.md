# Dictionary management restrictions and validation

## Restrictions

Dictionary management enforces the following constraints and validation rules.

### HRID and naming constraints

- An HRID matches the pattern `^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$` with a maximum length of 256 characters.
- HRIDs are unique within an environment. The same HRID in a different environment is treated as a separate dictionary, so cross-environment collisions aren't prevented.

### Type-specific constraints

The following rules apply per dictionary type.

**Manual dictionaries:**
- Include at least one property in `manual.properties`.
- Don't define `dynamic.provider` or `dynamic.trigger`.

**Dynamic dictionaries:**
- Define both `dynamic.provider` and `dynamic.trigger`.
- Don't include `manual.properties`.

### Validation limitations

Dry-run validation checks the structure of the specification. It doesn't test provider connectivity for dynamic dictionaries.

### Permission-based behavior

A caller that doesn't hold the `CREATE`, `UPDATE`, or `DELETE` action on `ENVIRONMENT_DICTIONARY` can't view the `dynamic` configuration in `GET` responses.

### Kubernetes resource dependencies

When a dynamic dictionary references a Kubernetes Secret or ConfigMap, create that Secret or ConfigMap before you create the dictionary. The operator reads the referenced value during reconciliation, and reconciliation fails if the value isn't found. Each template expression uses `[[ ]]` delimiters and takes a single `<resource-name>/<key>` argument:

```yaml
dynamic:
  provider:
    type: HTTP
    url: "[[ secret `my-secret/url` ]]"
    headers:
      - name: Authorization
        value: "[[ secret `my-secret/token` ]]"
```
