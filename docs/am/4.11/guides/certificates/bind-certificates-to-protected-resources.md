### Binding Certificates to Protected Resources

Set the `certificate` field on the Protected Resource to the ID of an existing certificate in the domain. The system validates that the certificate exists during create and update operations, returning `"Certificate not found"` if the ID is invalid.

Once bound, the certificate can be used for mTLS authentication methods (`tls_client_auth`, `self_signed_tls_client_auth`).

Attempting to delete a certificate referenced by any Protected Resource fails with error `"You can't delete a certificate with existing protected resources."`

To remove the binding, update the Protected Resource with `certificate` set to null.

### Searching Protected Resources

Send a GET request to `/organizations/{orgId}/environments/{envId}/domains/{domainId}/protected-resources` with query parameters:

* `q`: Search query string. Supports wildcards (`*`). Searches against `name` and `clientId` fields.
* `type`: Resource type filter
* `page`: Page number (default: 0)
* `size`: Page size (default: 50)

Example:

```
GET /organizations/{orgId}/environments/{envId}/domains/{domainId}/protected-resources?q=mcp*&type=MCP_SERVER&page=0&size=10
```

All searches are case-insensitive. Exact matches return resources where `clientId` or `name` match the query exactly. Wildcard queries (e.g., `q=client*`) perform case-insensitive prefix matching on `clientId` or `name`.
