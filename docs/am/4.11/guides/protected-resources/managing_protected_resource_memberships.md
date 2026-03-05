### Searching Protected Resources

Query Protected Resources using the search endpoint: `GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/protected-resources?q={query}`.

The `q` parameter supports wildcard matching with `*`. For example, `q=api-*` matches resources with names or client IDs starting with "api-". Searches are case-insensitive and match against both `name` and `clientId` fields. Omit `q` to retrieve all resources filtered by type.

**Response:** `Page<ProtectedResourcePrimaryData>` (paginated, ordered by `updated_at` descending)
