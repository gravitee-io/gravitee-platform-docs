# Dictionary Management Restrictions and Validation

## Restrictions

Dictionary management enforces the following constraints and validation rules:

### HRID and Naming Constraints

- HRIDs must match the pattern `^[a-zA-Z0-9][a-zA-Z0-9_-]+[a-zA-Z0-9]$` with a maximum length of 256 characters.
- Dictionary names must be at least 3 characters long.
- HRIDs are unique within an environment. Cross-environment collisions are not prevented.

### Type-Specific Constraints

**Manual dictionaries:**
- Must include at least one property in `manual.properties`.
- Must not define `dynamic.provider` or `dynamic.trigger`.

**Dynamic dictionaries:**
- Must define both `dynamic.provider` and `dynamic.trigger`.
- Must not include `manual.properties`.

### Validation Limitations

- Dry-run validation does not test provider connectivity for dynamic dictionaries.
- APIs with only `SubscriptionListener` skip HTTP validation. Dictionaries are not validated in this context.

### Permission-Based Behavior

Users without `CREATE`, `UPDATE`, or `DELETE` permissions on `ENVIRONMENT_DICTIONARY` cannot view `dynamic` configuration in GET responses.

### Kubernetes Resource Dependencies

Kubernetes Secrets and ConfigMaps must exist before dictionary creation. No automatic retry occurs on secret creation. Example:

```yaml
dynamic:
  provider:
    type: HTTP
    url: "{{ secret `my-secret` `url` }}"
    headers:
      - name: Authorization
        value: "{{ secret `my-secret` `token` }}"
```
