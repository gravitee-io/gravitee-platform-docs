# CIMD Gateway Configuration Reference

## Gateway Configuration

### CIMD Settings

Configure CIMD at the gateway level using `gravitee.yml` or environment variables. All properties are prefixed with `oidc.cimdSettings`.

| Property | Description | Example |
|:---------|:------------|:--------|
| `enabled` | Enable CIMD support | `false` |
| `templateId` | Application ID of the template used for CIMD clients (required when enabled) | `"app-template-123"` |
| `allowPrivateIpAddress` | Allow metadata document requests to private IP addresses | `false` |
| `allowUnsecuredHttpUri` | Allow metadata document requests to plain HTTP URIs | `false` |
| `fetchTimeoutMs` | Timeout in milliseconds for fetching client metadata documents | `3000` |
| `maxResponseSizeKb` | Maximum allowed size of a metadata response in kilobytes | `20` |
| `allowedDomains` | Restrict metadata document to these domains (supports wildcard `*.example.com`). Empty list allows all domains | `["*.example.com", "trusted.org"]` |
| `cacheTtlSeconds` | Time-to-live for cached metadata responses in seconds | `3600` |
| `cacheMaxEntries` | Maximum number of entries to store in the metadata cache | `500` |
| `revokeOnDocumentChange` | Revoke all tokens and consents when CIMD metadata document changes | `false` |

### SSRF Protection

SSRF protection applies to both metadata document and logo URI requests.

When `allowPrivateIpAddress` is `false`, requests to private, loopback, link-local, or any-local IP addresses are rejected.

When `allowUnsecuredHttpUri` is `false`, only `https://` URIs are allowed.

The `allowedDomains` list restricts requests to matching hosts. Wildcard patterns (`*.example.com`) match first-level subdomains only. For example, `*.example.com` matches `app.example.com` but not `sub.app.example.com`.
