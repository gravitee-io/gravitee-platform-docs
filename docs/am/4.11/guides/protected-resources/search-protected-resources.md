### Searching Protected Resources

Send a GET request to `/organizations/{orgId}/environments/{envId}/domains/{domainId}/protected-resources` with the query parameter `q` to search by name or client ID. The search is case-insensitive and supports wildcards. For example, `q=mcp*` matches all resources whose name or client ID starts with "mcp".

Combine the `q` parameter with `type` to filter by resource type (e.g., `type=MCP_SERVER`). Use `page` and `size` for pagination. The default page is 0 and the default size is 50.

**Example:**

```
GET /protected-resources?q=prod*&type=MCP_SERVER&page=0&size=10
```

This request returns the first 10 MCP Server resources with names or client IDs starting with "prod".

{% hint style="info" %}
Search queries are case-insensitive and support wildcards only. Advanced operators such as regex are not supported.
{% endhint %}
