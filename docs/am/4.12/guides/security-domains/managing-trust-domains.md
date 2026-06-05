# Managing Trust Domains

Navigate to **Domain Settings > Workload Identity** to list, create, and edit trust domains. Each trust domain represents a SPIFFE trust boundary and holds the JWKS bundle used to verify JWT-SVIDs.

## Creating a Trust Domain

1. Click **Add Trust Domain**.
2. Enter a **Name** for the trust domain (e.g., `am.local`).
3. (Optional) Enter a **Description** in the text area.
4. Select a **Bundle Source** from the dropdown: **JWKS URL** or **Static JWKS**.
5. If **JWKS URL** is selected, enter the **JWKS URL** in the text field (e.g., `https://spire-oidc:8443/keys`).
6. If **Static JWKS** is selected, paste the inline JWKS JSON in the text area.
7. Enter **Allowed Algorithms** as a comma-separated list (e.g., `RS256, ES256`).
8. Enter a **Refresh Interval Seconds** value (how often to refresh the JWKS bundle from the URL).
9. Click **Create** to save the trust domain.

**Trust Domain Reference:**

| Field | Description | Constraints |
|:------|:------------|:------------|
| **Name** | Trust domain name (e.g., `am.local`) | Required; unique per domain |
| **Description** | Human-readable description | Optional |
| **Bundle Source** | JWKS source: JWKS URL or Static JWKS | Required |
| **JWKS URL** | HTTPS endpoint serving the trust bundle | Required when Bundle Source is JWKS URL; must not resolve to private/reserved IP unless `allowPrivateIpAddress=true` |
| **Static JWKS** | Inline JWKS JSON | Required when Bundle Source is Static JWKS |
| **Allowed Algorithms** | Permitted JWS signature algorithms (e.g., `RS256`, `ES256`) | Required |
| **Refresh Interval Seconds** | JWKS bundle refresh interval | Required when Bundle Source is JWKS URL |

{% hint style="info" %}
AM caches trust bundles and serves the last known good bundle on transient fetch errors.
{% endhint %}

## Configuring SPIFFE Settings on an Application

1. Navigate to the agent application's settings.
2. Under **Workload Identity Settings**, select a **Trust Domain** from the dropdown.
3. Enter the **Subject** (expected SPIFFE ID, e.g., `spiffe://am.local/hotel-agent/`).
4. Select a **Subject Match Mode** from the dropdown: **Exact Match** or **Prefix Match**.
5. Click **Save**.

**Workload Identity Settings Reference:**

| Field | Description | Constraints |
|:------|:------------|:------------|
| **Trust Domain** | Name of the trust domain this application authenticates against | Required when token endpoint auth method is `spiffe_jwt` |
| **Subject** | Expected SPIFFE ID in SVID `sub` claim | Required when token endpoint auth method is `spiffe_jwt`; must start with `spiffe://{trustDomain}/` |
| **Subject Match Mode** | EXACT (sub must equal subject) or PREFIX (sub must start with subject) | Defaults to EXACT; PREFIX requires subject to end with `/` and is only allowed for HOSTED_DELEGATED or AUTONOMOUS agents |
