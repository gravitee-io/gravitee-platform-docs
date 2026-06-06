# SPIFFE Workload Identity & Agent Applications: Managing Trust Domains

## Managing Trust Domains

Navigate to **Settings > Workload Identity** in the domain sidebar to manage trust domains.

### Creating a Trust Domain

1. Navigate to **Settings > Workload Identity** and click **Add Trust Domain**.
2. Enter a **Name** (e.g., `production.acme.com`).
3. Optionally enter a **Description**.
4. Select a **Bundle Source**: JWKS URL or Static JWKS.
5. If JWKS URL, enter the **JWKS URL** (e.g., `https://spire.acme.com/keys`) and a **Refresh Interval (seconds)**.
6. If Static JWKS, paste the JWKS JSON in the **Static JWKS** field.
7. Select **Allowed Algorithms** (e.g., RS256, ES256).
8. Click **Create**.

**Reference Table:**

| Field | Description | Required |
|:------|:------------|:---------|
| Name | Trust domain identifier | Yes |
| Description | Optional description | No |
| Bundle Source | JWKS URL or Static JWKS | Yes |
| JWKS URL | Remote JWKS endpoint | Conditional (JWKS URL) |
| Refresh Interval (seconds) | JWKS fetch interval | Conditional (JWKS URL) |
| Static JWKS | Inline JWKS JSON | Conditional (Static JWKS) |
| Allowed Algorithms | Permitted JWT signing algorithms | Yes |

### Updating a Trust Domain

Select a trust domain from the list, modify the desired fields, and click **Save**. Changes to the JWKS URL or refresh interval take effect on the next scheduled fetch. Changes to allowed algorithms apply immediately to new authentication requests.

### Deleting a Trust Domain

Select a trust domain and click **Delete**. Deletion is blocked if any application references the trust domain in its Workload Identity Settings.
