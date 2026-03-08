### Database Schema

The `protected_resources` table includes a new column for certificate references:

| Property | Type | Nullable | Description |
|:---------|:-----|:---------|:------------|
| `certificate` | nvarchar(64) | Yes | Certificate ID for JWT signature verification |

When a Protected Resource has a certificate configured, the system uses it for JWT signature verification. Otherwise, HMAC validation is assumed.
