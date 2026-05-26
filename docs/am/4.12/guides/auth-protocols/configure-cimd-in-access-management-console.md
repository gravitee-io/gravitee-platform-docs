
# Configure CIMD in the Access Management Console


## Creating a CIMD-Enabled Domain

To enable CIMD support, first create or designate an existing application as the template by setting its `template` flag to `true`. Navigate to the domain's OIDC settings and enable CIMD, then select the template application from the autocomplete field. Configure SSRF protection settings: toggle **Allow Private/Loopback IP Addresses** and **Allow Unsecured HTTP URIs** as needed, and add allowed domains to the **Allowed Domains** chip list (use `*.example.com` for wildcard subdomains). Set **Fetch Timeout (ms)** (default 3000), **Max Response Size (KB)** (default 20), **Cache TTL (seconds)** (default 3600), and **Cache Max Entries** (default 500). Optionally enable **Revoke Tokens and Consents When Client Metadata Changes** to automatically revoke tokens when metadata hashes change. Save the configuration. The OIDC discovery document (`/.well-known/openid-configuration`) will now advertise `"client_id_metadata_document_supported": true`.

## Authenticating CIMD Clients

CIMD clients initiate OAuth authorization by presenting a URL-shaped `client_id` (e.g., `http://example.com/my-app`). The gateway detects the URL pattern, checks the in-memory metadata cache, and fetches the metadata document from the `client_id` URL on cache miss. The fetch is subject to SSRF protection: the gateway validates that the URL does not resolve to private IPs (unless allowed), enforces HTTPS (unless HTTP is allowed), checks the domain against the allowed domains list, and enforces the fetch timeout and maximum response size. The gateway validates the metadata document, ensuring `client_id` matches the request URL exactly, `redirect_uris` is present and non-empty, and no secret-based `token_endpoint_auth_method` is used. The gateway synthesizes a client by merging metadata with the template application, caches the metadata with the configured TTL, and proceeds with the OAuth flow. During token exchange, the gateway validates `token_endpoint_auth_method`: `"none"` requires no credentials, while `"private_key_jwt"` validates the JWT signature using `jwks` or `jwks_uri` from the metadata. Tokens are issued with the `aud` claim set to the CIMD `client_id` URL.

## End-User Configuration

1. Navigate to **Settings → OAuth 2.0 → CIMD** in the domain console.

    <figure><img src="../../.gitbook/assets/am-cimd-settings-overview.png" alt="CIMD settings page showing Enable CIMD toggle and Template Application selector"><figcaption></figcaption></figure>

2. Toggle **Enable CIMD** to enable Client ID Metadata Document support.
3. Select a **Template Application** from the autocomplete dropdown (required when CIMD is enabled; filters applications where `template=true`).
4. Toggle **Allow Private/Loopback IP Addresses** to permit metadata requests to private IP addresses (SSRF protection setting).

    <figure><img src="../../.gitbook/assets/am-cimd-ssrf-protection.png" alt="CIMD SSRF protection settings including private IP and HTTP URI toggles"><figcaption></figcaption></figure>

5. Toggle **Allow Unsecured HTTP URIs** to permit metadata requests to plain HTTP URIs (SSRF protection setting).
6. Enter a value in the **Fetch Timeout (ms)** field (default 3000; must be greater than 0).

    <figure><img src="../../.gitbook/assets/am-cimd-fetch-settings.png" alt="CIMD fetch timeout and max response size configuration fields"><figcaption></figcaption></figure>

7. Enter a value in the **Max Response Size (KB)** field (default 20; must be greater than 0).
8. Add domains to the **Allowed Domains** chip list to restrict metadata fetching to specific domains (supports `*.example.com` wildcard for first-level subdomains; empty list allows all domains).

    <figure><img src="../../.gitbook/assets/am-cimd-allowed-domains.png" alt="CIMD allowed domains chip list for domain restriction"><figcaption></figcaption></figure>

9. Enter a value in the **Cache TTL (seconds)** field (default 3600; must be greater than 0).
10. Enter a value in the **Cache Max Entries** field (default 500; must be greater than 0).
11. Toggle **Revoke Tokens and Consents When Client Metadata Changes** to automatically revoke all tokens and scope approvals when the metadata document hash changes.

### CIMD Settings Reference

| Field | Description | Default |
|:------|:------------|:--------|
| **Enable CIMD** | Enable/disable Client ID Metadata Document support | Disabled |
| **Template Application** | Template application for CIMD clients (required when enabled) | None |
| **Allow Private/Loopback IP Addresses** | SSRF protection: allow metadata requests to private IPs | Disabled |
| **Allow Unsecured HTTP URIs** | SSRF protection: allow metadata requests to HTTP URIs | Disabled |
| **Fetch Timeout (ms)** | Timeout for metadata fetch | 3000 |
| **Max Response Size (KB)** | Maximum metadata response size | 20 |
| **Allowed Domains** | Restrict metadata to these domains (supports `*.example.com`) | Empty (allow all) |
| **Cache TTL (seconds)** | Metadata cache time-to-live | 3600 |
| **Cache Max Entries** | Maximum cache entries | 500 |
| **Revoke Tokens and Consents When Client Metadata Changes** | Revoke tokens when metadata hash changes | Disabled |
