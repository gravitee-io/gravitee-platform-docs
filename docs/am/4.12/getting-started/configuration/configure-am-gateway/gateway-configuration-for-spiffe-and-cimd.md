# Gateway Configuration for SPIFFE and CIMD

## Gateway Configuration

### CIMD Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.oidc.cimdSettings.enabled` | Enables CIMD (Client Identity Metadata Document) flows | `true` |
| `gravitee.oidc.cimdSettings.allowedDomains` | Permitted domains for CIMD document URLs | `["example.com", "trusted.org"]` |
| `gravitee.oidc.cimdSettings.allowPrivateIpAddress` | Permits CIMD URLs resolving to private IP addresses | `false` |
| `gravitee.oidc.cimdSettings.allowUnsecuredHttpUri` | Permits HTTP CIMD URLs | `false` |

### SPIFFE Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.oidc.spiffeSettings.enabled` | Enables SPIFFE workload identity authentication at domain level | `true` |
| `gravitee.oidc.spiffeSettings.allowPrivateIpAddress` | Permits JWKS URLs resolving to private IP addresses | `false` |
| `gravitee.oidc.spiffeSettings.allowUnsecuredHttpUri` | Permits HTTP (non-TLS) JWKS URLs | `false` |
| `gravitee.oidc.spiffeSettings.cacheMaxEntries` | Maximum JWKS cache entries | `100` |
| `gravitee.oidc.spiffeSettings.cacheTtlSeconds` | JWKS cache TTL in seconds | `3600` |
| `gravitee.oidc.spiffeSettings.clockSkewSeconds` | Allowed clock skew for JWT validation | `30` |
| `gravitee.oidc.spiffeSettings.defaultAllowedAlgorithms` | Default signing algorithms for trust domains | `["RS256", "ES256"]` |
| `gravitee.oidc.spiffeSettings.fetchTimeoutMs` | HTTP timeout for JWKS fetch | `5000` |
| `gravitee.oidc.spiffeSettings.maxJwtLifetimeSeconds` | Maximum JWT lifetime | `300` |
| `gravitee.oidc.spiffeSettings.maxResponseSizeKb` | Maximum JWKS response size | `512` |
