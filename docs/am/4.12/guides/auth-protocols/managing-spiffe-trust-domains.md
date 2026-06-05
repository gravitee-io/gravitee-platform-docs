# Managing SPIFFE Trust Domains

## Managing Trust Domains

Trust domains are scoped to an Access Management domain and managed via **Domain Settings > Workload Identity**.

### Creating Trust Domains

Navigate to **Domain Settings > Workload Identity** and select **Add Trust Domain**:

1. Enter a **Name** for the trust domain (e.g., `example.org`).
2. Enter a **Description** (optional).
3. Select a **Bundle Source**: JWKS URL or Static JWKS.
4. Enter the **JWKS URL** (when source is JWKS URL).
5. Enter the **Refresh Interval Seconds** (when source is JWKS URL).
6. Select **Allowed Algorithms** from the dropdown (e.g., `RS256`, `ES256`).

| Field | Description |
|:------|:------------|
| **Name** | Trust domain identifier (must match SPIFFE trust domain) |
| **Description** | Human-readable description |
| **Bundle Source** | JWKS URL (fetch from endpoint) or Static JWKS (inline JSON) |
| **JWKS URL** | HTTP(S) endpoint serving the trust bundle |
| **Refresh Interval Seconds** | Seconds between JWKS refetches |
| **Allowed Algorithms** | Permitted JWT signing algorithms |

### Management API

**List Trust Domains:**
```
GET /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains
```

**Create Trust Domain:**
```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains
```

**Update Trust Domain:**
```
PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}
```

**Delete Trust Domain:**
```
DELETE /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/trust-domains/{trustDomainId}
```

### CIMD API

**Validate CIMD Document:**
```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/validate
```

**Create Application from CIMD:**
```
POST /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/cimd/applications
```
