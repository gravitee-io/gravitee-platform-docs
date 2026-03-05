### Searching Protected Resources

Query Protected Resources by name, client ID, or type using the search endpoint:

#### Query Parameters

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `q` | String | None | Search query string. Supports exact matches (case-insensitive) or wildcard patterns. |
| `type` | String | None | Resource type filter (e.g., `MCP_SERVER`). |
| `page` | Integer | `0` | Page number for pagination. |
| `size` | Integer | `50` | Number of results per page. |

#### Search Query Behavior

The `q` parameter supports two query types:

| Query Type | Behavior | Example |
|:-----------|:---------|:--------|
| Exact match | Case-insensitive equality on `name` or `clientId` | `"myResource"` |
| Wildcard | Regex pattern match (case-insensitive) | `"my*"` matches `"myResource"`, `"MyApp"` |

Multiple wildcards in a query collapse to a single `.*` regex pattern. For example, `"my***res"` becomes `"my.*res"`.

#### Uniqueness Constraint

Resource identifiers must be unique across all Protected Resources in a domain. During updates, the system excludes the current resource from uniqueness validation.

