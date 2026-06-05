# Manage Trust Domains

## Managing Trust Domains

Navigate to **Workload Identity** under domain settings to manage Trust Domains.

### Creating a Trust Domain

1. Click **Add Trust Domain**.
2. Enter a **Name** (SPIFFE trust domain identifier, e.g., `prod.example.org`).
3. Enter an optional **Description**.
4. Select a **Bundle Source**:
   * **JWKS URL**: Fetch keys from a URL (e.g., `https://spire-oidc:8443/keys`).
   * **Static JWKS**: Paste a JSON Web Key Set directly.
5. Configure **Allowed Algorithms** (e.g., `RS256`, `ES256`).
6. Set a **Refresh Interval** (seconds) for JWKS URL sources.
7. Save the Trust Domain.

| Field | Description |
|:------|:------------|
| **Name** | SPIFFE trust domain identifier |
| **Description** | Optional description of the trust domain |
| **Bundle Source** | JWKS URL or Static JWKS |
| **JWKS URL** | URL to fetch trust bundle keys (for JWKS URL source) |
| **Static JWKS** | Embedded JSON Web Key Set (for Static JWKS source) |
| **Allowed Algorithms** | Signing algorithms accepted for SVID verification |
| **Refresh Interval** | How often to fetch updated trust bundles (seconds) |
