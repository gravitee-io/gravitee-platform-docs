# Creating and Managing Trust Domains

## Creating Trust Domains

Navigate to **Settings** in the left sidebar, then select **SPIFFE Settings** under the OAuth 2.0 section. Trust domains define SPIFFE trust boundaries for workload identity authentication.

<figure><img src="../../../.gitbook/assets/am-trust-domains-list.png" alt="Trust domains list in Workload Identity settings"><figcaption></figcaption></figure>

1. Click the **+** button to add a new trust domain.

    <figure><img src="../../../.gitbook/assets/am-trust-domain-create-form.png" alt="Trust domain creation form"><figcaption></figcaption></figure>

2. Enter a **Name** for the trust domain (e.g., `prod.example`). The name must be a DNS-style label (lowercase letters, digits, `.` or `-`).
3. Provide an optional **Description**.
4. Select a **Bundle Source**: **JWKS URL** or **Static JWKS**.
5. If **JWKS URL** is selected, enter the **JWKS URL** (e.g., `https://spire-oidc:8443/keys`).
6. If **Static JWKS** is selected, paste the JWKS JSON in the **Static JWKS** field.
7. Set the **Refresh Interval (seconds)** for bundle caching (e.g., `300`). This controls how often Access Management polls the JWKS endpoint.
8. Select **Allowed Algorithms** from the dropdown (e.g., `RS256`, `ES256`). Leave empty to inherit the domain default. `none` and HMAC variants are always rejected.
9. Click **Create**.

| Field | Description |
|:------|:------------|
| **Name** | Trust domain identifier (must be unique within the domain) |
| **Description** | Optional description of the trust domain |
| **Bundle Source** | JWKS URL (fetched periodically) or Static JWKS (embedded) |
| **JWKS URL** | URL for fetching the trust bundle (required when Bundle Source is JWKS URL) |
| **Static JWKS** | Embedded JWKS JSON (required when Bundle Source is Static JWKS) |
| **Refresh Interval (seconds)** | Cache TTL for the trust bundle (applies to JWKS URL source) |
| **Allowed Algorithms** | Permitted signing algorithms for JWT-SVID validation |

<figure><img src="../../../.gitbook/assets/am-trust-domains-list.png" alt="Trust domains list in Workload Identity settings"><figcaption></figcaption></figure>

<figure><img src="../../../.gitbook/assets/am-trust-domain-create-form.png" alt="Trust domain creation form"><figcaption></figcaption></figure>
