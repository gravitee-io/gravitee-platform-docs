# Configure SPIFFE and CIMD Gateway Settings

## Gateway Configuration

Configure gateway-level properties to enable and tune SPIFFE workload identity authentication and CIMD features for a domain.

### SPIFFE Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.oidc.spiffe.enabled` | Enables SPIFFE workload identity authentication for a domain | `true` |
| `gravitee.oidc.spiffe.defaultAllowedAlgorithms` | Default signing algorithms allowed for SPIFFE JWT-SVIDs | `["RS256", "ES256"]` |
| `gravitee.oidc.spiffe.clockSkewSeconds` | Clock skew tolerance for SVID validation (seconds) | `30` |
| `gravitee.oidc.spiffe.maxJwtLifetimeSeconds` | Maximum allowed lifetime for SPIFFE JWT-SVIDs (seconds) | `3600` |
| `gravitee.oidc.spiffe.cacheMaxEntries` | Maximum number of entries in the trust bundle cache | `100` |
| `gravitee.oidc.spiffe.cacheTtlSeconds` | Time-to-live for trust bundle cache entries (seconds) | `300` |

### CIMD Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.oidc.cimd.enabled` | Enables CIMD feature for a domain | `true` |
| `gravitee.oidc.cimd.allowedDomains` | Whitelist of allowed domains for CIMD URLs | `["example.com", "agents.acme.org"]` |
| `gravitee.oidc.cimd.allowPrivateIpAddress` | Whether CIMD URLs may resolve to private IP addresses | `false` |
| `gravitee.oidc.cimd.allowUnsecuredHttpUri` | Whether unsecured HTTP CIMD URLs are permitted | `false` |
| `gravitee.oidc.cimd.fetchTimeoutMs` | HTTP fetch timeout for CIMD documents (milliseconds) | `5000` |
| `gravitee.oidc.cimd.maxResponseSizeKb` | Maximum allowed size for CIMD document responses (kilobytes) | `512` |
