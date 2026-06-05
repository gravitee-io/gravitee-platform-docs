# Gateway Configuration for SPIRE Testing

## Gateway Configuration

### SPIRE Local Stack (Development/Testing)

Use the provided `docker-compose.spire.yml` overlay to run a SPIRE server, agent, and OIDC discovery provider for local testing.

| Service | Port Mapping | Description |
|:--------|:-------------|:------------|
| `spire-server` | `18081:8081` | SPIRE server with trust domain `am.local` |
| `spire-oidc` | `18443:8443` | OIDC discovery provider serving JWKS at `http://localhost:18443/keys` |
| `spire-agent` | — | SPIRE agent with unix workload attestor |

**SPIRE Server Configuration:**

| Property | Value | Description |
|:---------|:------|:------------|
| `trust_domain` | `am.local` | SPIFFE trust domain |
| `jwt_issuer` | `http://spire-oidc:8443` | JWT-SVID issuer URL |
| `default_jwt_svid_ttl` | `5m` | Default JWT-SVID lifetime |
| `ca_ttl` | `24h` | CA certificate lifetime |

**Example Workload Entries:**

| SPIFFE ID | Selector | Description |
|:----------|:---------|:------------|
| `spiffe://am.local/agent/billing` | `unix:uid:0` | Exact workload entry |
| `spiffe://am.local/agent/test/sample` | `unix:uid:0` | Pattern workload entry (single segment) |

### CIMD Trust Policies

Configure CIMD trust policies at the domain level under `oidc.cimdSettings`:

<figure><img src="../.gitbook/assets/am-cimd-ssrf-protection.png" alt="CIMD SSRF protection settings"><figcaption></figcaption></figure>


<figure><img src="../.gitbook/assets/am-cimd-cache-settings.png" alt="CIMD cache configuration settings"><figcaption></figcaption></figure>

| Property | Description | Example |
|:---------|:------------|:--------|
| `enabled` | Enable CIMD application creation | `true` |
| `allowUnsecuredHttpUri` | Allow HTTP (non-HTTPS) CIMD URLs | `false` |
| `allowedDomains` | Whitelist of allowed CIMD URL hosts (empty = all allowed) | `["agents.example.com"]` |
| `allowPrivateIpAddress` | Allow CIMD URLs resolving to private/reserved IP addresses | `false` |

### Test Environment Variables

| Variable | Value | Description |
|:---------|:------|:------------|
| `RUN_SPIRE_TESTS` | `true` | Enable SPIRE-dependent gateway tests in CI |
| `MONGO_VERSION` | `4.4` | MongoDB version for local-stack |
| `JEST_JUNIT_OUTPUT_NAME` | `junit-management.xml` / `junit-gateway.xml` | JUnit report filename for test results |
