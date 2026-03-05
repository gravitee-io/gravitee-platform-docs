### Searching Protected Resources

Use the search API to locate Protected Resources by name or client ID. The search endpoint supports wildcard patterns and case-insensitive matching.

#### Endpoint

```
GET /protected-resources?q={query}
```

#### Query Parameter

| Parameter | Type | Required | Description |
|:----------|:-----|:---------|:------------|
| `q` | string | No | Search query. Supports wildcard (`*`) pattern matching. Searches the `name` and `clientId` fields (case-insensitive). If omitted, returns all resources filtered by type. |

#### Pagination

The search endpoint supports pagination using `PageSortRequest` parameters:

| Parameter | Type | Description |
|:----------|:-----|:------------|
| `page` | integer | Page number (zero-indexed) |
| `size` | integer | Number of results per page |

#### Response Format

The endpoint returns a `Page<ProtectedResourcePrimaryData>` object containing:

* **content**: Array of Protected Resource objects matching the query
* **totalElements**: Total number of matching resources
* **totalPages**: Total number of pages
* **size**: Number of results per page
* **number**: Current page number

#### Search Behavior

* **With query parameter**: Performs case-insensitive search on `name` and `clientId` fields. Use `*` for wildcard matching (e.g., `q=prod*` matches "production-api" and "prod-service").
* **Without query parameter**: Returns all Protected Resources filtered by type.

#### Required Permission

`PROTECTED_RESOURCE[LIST]`

The system checks permissions in this hierarchy:
1. Resource-level
2. Domain-level
3. Environment-level
4. Organization-level
