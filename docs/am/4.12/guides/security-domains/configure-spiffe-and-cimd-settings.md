# Configure SPIFFE and CIMD Settings

## Gateway Configuration

### SPIFFE Settings

Configure SPIFFE JWT-SVID authentication at the domain level:

1. Navigate to **Settings > Security** in the domain sidebar.
2. Scroll to the **SPIFFE Workload Identity** section.
3. Toggle **Enable SPIFFE** to allow clients in this domain to authenticate using the `spiffe_jwt` token-endpoint method.

    <figure><img src="../../.gitbook/assets/am-spiffe-settings-overview.png" alt="SPIFFE Workload Identity settings page with Enable SPIFFE toggle and explanatory text"><figcaption></figcaption></figure>

4. Configure the following properties in your `gravitee.yml` or environment variables:

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.oidc.spiffeSettings.enabled` | Enables SPIFFE JWT-SVID authentication for the domain | `true` |
| `gravitee.oidc.spiffeSettings.allowPrivateIpAddress` | Whether SPIFFE JWKS URLs may resolve to private IP addresses | `false` |
| `gravitee.oidc.spiffeSettings.allowUnsecuredHttpUri` | Whether unsecured HTTP JWKS URLs are permitted | `false` |
| `gravitee.oidc.spiffeSettings.cacheMaxEntries` | Maximum number of cached JWKS entries | `100` |
| `gravitee.oidc.spiffeSettings.cacheTtlSeconds` | TTL for cached JWKS entries | `3600` |
| `gravitee.oidc.spiffeSettings.clockSkewSeconds` | Allowed clock skew for JWT validation | `30` |
| `gravitee.oidc.spiffeSettings.defaultAllowedAlgorithms` | Default signing algorithms accepted for SPIFFE JWTs | `["RS256", "ES256"]` |
| `gravitee.oidc.spiffeSettings.fetchTimeoutMs` | HTTP timeout for fetching JWKS | `10000` |
| `gravitee.oidc.spiffeSettings.maxJwtLifetimeSeconds` | Maximum allowed JWT lifetime | `300` |
| `gravitee.oidc.spiffeSettings.maxResponseSizeKb` | Maximum JWKS response size | `512` |

### CIMD Settings

Configure CIMD application creation at the domain level:

1. Navigate to **Settings > Security** in the domain sidebar.
2. Scroll to the **CIMD** section.
3. Toggle **Client ID Metadata Document (CIMD) support** to enable CIMD for the domain.

    <figure><img src="../../.gitbook/assets/am-cimd-settings-overview.png" alt="CIMD settings page with toggle, template application dropdown, and SSRF protection options"><figcaption></figcaption></figure>

4. Configure the following properties in your `gravitee.yml` or environment variables:

| Property | Description | Example |
|:---------|:------------|:--------|
| `gravitee.oidc.cimdSettings.enabled` | Enables CIMD support for the domain | `true` |
| `gravitee.oidc.cimdSettings.allowedDomains` | Whitelist of allowed domains for CIMD URLs | `["agents.example.com"]` |
| `gravitee.oidc.cimdSettings.allowPrivateIpAddress` | Whether CIMD URLs may resolve to private IP addresses | `false` |
| `gravitee.oidc.cimdSettings.allowUnsecuredHttpUri` | Whether unsecured HTTP CIMD URLs are permitted | `false` |
