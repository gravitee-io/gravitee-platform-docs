### Searching Protected Resources

Query Protected Resources using the `GET /protected-resources` endpoint with the optional `q` parameter. The `q` parameter supports wildcard matching using the asterisk (`*`) character for prefix matching. For example, `q=api-*` matches resources with names or client IDs starting with "api-".

Searches are case-insensitive and match against both the `name` and `clientId` fields. When the `q` parameter is omitted, the endpoint retrieves all resources filtered by type.

Results are paginated and ordered by `updated_at` in descending order.

{% hint style="info" %}
Wildcard queries use prefix matching only. The search pattern follows the `^query.*` format, where the asterisk matches any characters after the specified prefix.
{% endhint %}

#### Search Query Examples

**Exact Match:**

**Wildcard Match:**

**Retrieve All Resources:**
