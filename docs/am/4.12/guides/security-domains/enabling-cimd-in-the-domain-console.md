# Enabling CIMD in the Domain Console

## End-User Configuration

Navigate to **Settings → CIMD** in the domain console to configure Client ID Metadata Document support.

1. Toggle **Enable CIMD** to enable Client ID Metadata Document support.

    <figure><img src="../../.gitbook/assets/am-cimd-settings-overview.png" alt="CIMD settings page showing Enable CIMD toggle and Template Application selector"><figcaption></figcaption></figure>

2. Select a **Template Application** from the autocomplete dropdown (filtered to applications with `template: true`).
3. Toggle **Allow Private/Loopback IP Addresses** to allow metadata document requests to private, loopback, link-local, or any-local IP addresses.

    <figure><img src="../../.gitbook/assets/am-cimd-ssrf-protection.png" alt="CIMD SSRF protection settings showing Allow Private/Loopback IP Addresses and Allow Unsecured HTTP URIs toggles"><figcaption></figcaption></figure>

4. Toggle **Allow Unsecured HTTP URIs** to allow metadata document requests to plain HTTP (non-HTTPS) URIs.
5. Enter a value in the **Fetch Timeout (ms)** field to set the timeout for metadata fetch operations (must be greater than 0).

    <figure><img src="../../.gitbook/assets/am-cimd-fetch-settings.png" alt="CIMD fetch settings showing Fetch Timeout and Max Response Size fields"><figcaption></figcaption></figure>

6. Enter a value in the **Max Response Size (KB)** field to set the maximum allowed size of a metadata response (must be greater than 0).
7. Add domains to the **Allowed Domains** chip list to restrict metadata document requests to specific domains (supports `*.example.com` for first-level subdomain wildcards; empty list allows all domains).

    <figure><img src="../../.gitbook/assets/am-cimd-allowed-domains.png" alt="CIMD Allowed Domains chip list for restricting metadata document requests"><figcaption></figcaption></figure>

8. Enter a value in the **Cache TTL (seconds)** field to set the time-to-live for cached metadata responses (must be greater than 0).
9. Enter a value in the **Cache Max Entries** field to set the maximum number of entries to store in the metadata cache (must be greater than 0).
10. Toggle **Revoke Tokens and Consents When Client Metadata Changes** to automatically revoke all tokens and consents when the metadata document hash changes.

**CIMD Settings Reference**

| Field | Description | Validation |
|:------|:------------|:-----------|
| **Enable CIMD** | Enable Client ID Metadata Document support | — |
| **Template Application** | Template application for CIMD clients | Required when CIMD is enabled |
| **Allow Private/Loopback IP Addresses** | Allow metadata requests to private IP addresses | — |
| **Allow Unsecured HTTP URIs** | Allow metadata requests to plain HTTP URIs | — |
| **Fetch Timeout (ms)** | Timeout for metadata fetch | Must be > 0 |
| **Max Response Size (KB)** | Maximum metadata document size | Must be > 0 |
| **Allowed Domains** | Restrict metadata to these domains | Valid hostnames; wildcard only for first-level subdomain |
| **Cache TTL (seconds)** | Metadata cache time-to-live | Must be > 0 |
| **Cache Max Entries** | Maximum cache entries | Must be > 0 |
| **Revoke Tokens and Consents When Client Metadata Changes** | Revoke tokens when metadata changes | — |

### CIMD Logo Endpoint

The gateway provides an on-demand logo fetch endpoint for CIMD clients at `GET /{domain}/cimd/logo?clientId={url-encoded-client-id}`. The `clientId` query parameter must be the canonical metadata URL of the CIMD client. The endpoint returns `200 OK` with `Content-Type: image/*` and logo bytes if the logo is cached, or `404 Not Found` if the logo is not cached or the metadata does not include a `logo_uri`. On cache miss, the endpoint fetches the logo synchronously if non-expired metadata exists and `logo_uri` is set. The same SSRF protection rules apply to logo fetches as to metadata fetches. Logo size is limited to 256 KB.

## Restrictions

- CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`)
- CIMD clients always require exact redirect URI matching (no prefix matching)
- Metadata document size is limited to `maxResponseSizeKb` (default 20 KB)
- Logo size is limited to 256 KB
- Cache eviction is LRU-based; no manual cache invalidation API
- `jwks_uri` must be accessible from the gateway and is subject to the same SSRF protection as the metadata URL
- Template application cannot be deleted or un-templated while referenced as the CIMD template
- Metadata fetch retries up to 3 times with 100ms delay between attempts
- CIMD clients inherit template's identity providers, factors, and other settings not overridden by metadata
- Pre-registered clients take precedence over CIMD clients when the same `client_id` is used
- Token revocation on metadata change detects changes in remote CIMD metadata only; changes to template application settings do not trigger revocation
- Hash data for token revocation policy persists indefinitely while the policy is enabled and is deleted when disabled
