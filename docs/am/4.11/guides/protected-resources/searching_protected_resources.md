### Searching Protected Resources

Query Protected Resources using `GET /protected-resources?q={query}`. The `q` parameter supports wildcard matching with `*`. For example, `q=api-*` matches resources with names or client IDs starting with "api-". Searches are case-insensitive and match against both `name` and `clientId` fields.

Omit the `q` parameter to retrieve all resources filtered by type. Results are paginated and ordered by `updated_at` descending.

{% hint style="info" %}
Search queries with wildcards are anchored to the start of the string. For example, `*api` does not match `my-api`.
{% endhint %}

Search functionality is available in both JDBC and MongoDB repositories with consistent behavior.
