### Searching Protected Resources

Search Protected Resources by name or client ID using the `q` query parameter:

The search is case-insensitive and supports wildcards (`*`). Search queries match against `name` and `clientId` fields only.

**Query behavior:**

* **Exact match**: `q=clientId` returns resources where the name or client ID exactly matches the query
* **Wildcard match**: `q=client*` performs prefix matching on name or client ID

**Filtering by type:**

Combine the `q` parameter with `type` to filter by resource type:

**Pagination:**

Results are paginated using the following parameters:

* `page`: Page number (default: 0)
* `size`: Page size (default: 50)

