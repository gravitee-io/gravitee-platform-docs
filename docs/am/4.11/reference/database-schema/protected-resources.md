### Database Schema Changes

The `protected_resources` table includes a new `certificate` column to store certificate identifiers for JWT signature verification. This column is nullable and uses the `nvarchar(64)` data type.

### Secret Lifecycle Events

Protected Resource secret operations emit `PROTECTED_RESOURCE_SECRET` events for audit and notification purposes. The following actions trigger events:

| Action | Description |
|:-------|:------------|
| `CREATE` | Secret creation |
| `RENEW` | Secret renewal |
| `DELETE` | Secret deletion |

### Certificate Deletion Validation

Certificate deletion validation now checks for Protected Resource associations. If a certificate is used by one or more Protected Resources, the deletion operation fails with a `CertificateWithProtectedResourceException` error. This validation applies in addition to existing checks for Applications and Identity Providers.

### MCP Server Configuration Restrictions

MCP Server resources support a limited set of token endpoint authentication methods:

* `client_secret_basic`
* `client_secret_post`
* `client_secret_jwt`

The Refresh Token and PKCE configuration sections are not available for MCP Server resources.

### Secret Value Masking

Secret values are masked in list operations. Plaintext values are returned only when a secret is created or renewed.

### Resource Identifier Uniqueness

Resource identifiers must be unique across all Protected Resources in a domain. During updates, the current resource is excluded from uniqueness validation.

### Multi-Audience Token Validation

Tokens with multiple audiences always use RFC 8707 validation. This bypasses Application and Protected Resource client ID matching.

### Legacy RFC 8707 Mode

When legacy RFC 8707 mode is enabled, the caller client ID must match the audience for resource identifier validation to succeed.

### Search Query Support

The search API supports wildcard queries with case-insensitive pattern matching. Multiple consecutive wildcards are collapsed to a single pattern.
