### Searching Protected Resources

Search for Protected Resources using the endpoint:

```
GET /protected-resources?q={query}
```

**Query Parameter Behavior:**

* **`q` omitted:** Returns all Protected Resources filtered by type.
* **`q` provided:** Performs a case-insensitive search on the `name` and `clientId` fields.

**Wildcard Support:**

The query parameter supports the asterisk (`*`) wildcard character. For example:

* `q=client*` matches resources where `name` or `clientId` starts with "client".
* Multiple consecutive wildcards are collapsed into a single pattern.

**Pagination:**

Results are paginated using the `page` and `size` parameters.

**Example Request:**

```
GET /protected-resources?q=mcp*&page=0&size=10
```

**Related Behavior:**

When token introspection encounters multiple audiences, the system validates via resource identifiers (RFC 8707) rather than client ID lookup. If a single audience does not match an Application client ID, the system attempts to match it against a Protected Resource client ID before falling back to resource identifier validation.

