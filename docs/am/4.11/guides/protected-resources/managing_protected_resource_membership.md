### Searching Protected Resources

Query Protected Resources by name, client ID, or type using the search endpoint.

Send a GET request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources?q={query}&type={type}&page={page}&size={size}`.

**Query parameters:**

- `q`: Search query string. Supports exact matches (case-insensitive) or wildcard patterns (e.g., `my*` matches `myResource`, `MyApp`). Multiple wildcards collapse to a single `.*` regex pattern.
- `type`: Resource type filter (e.g., `MCP_SERVER`)
- `page`: Page number (default: 0)
- `size`: Page size (default: 50)

**Search behavior:**

| Query Type | Behavior | Example |
|:-----------|:---------|:--------|
| Exact match | Case-insensitive equality on `name` or `clientId` | `"myResource"` |
| Wildcard | Regex pattern match (case-insensitive) | `"my*"` matches `"myResource"`, `"MyApp"` |
| Multiple wildcards | Collapsed to single `.*` | `"my***res"` → `"my.*res"` |
