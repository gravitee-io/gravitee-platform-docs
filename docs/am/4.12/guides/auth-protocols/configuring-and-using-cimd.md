# Configuring and Using CIMD

## Creating a CIMD-Enabled Domain

1. Navigate to **Domain Settings → OAuth 2.0 → CIMD**.
2. Toggle **Client ID Metadata Document (CIMD) support** to enable the feature.
3. Select a **Template Application** from the autocomplete field (only applications marked as "Template" appear in the list).
4. Configure SSRF protection settings:
   * Toggle **Allow private/loopback IP addresses** to permit metadata requests to private IP addresses (RFC 1918, loopback, link-local, any-local).
   * Toggle **Allow unsecured HTTP URIs** to permit metadata requests to plain HTTP URIs.
5. Add domains to the **Allowed domains** chip list to restrict metadata requests to specific hosts (supports `*.example.com` for first-level subdomain wildcard; leave empty to allow all domains).
6. Set numeric values for **Fetch Timeout (ms)**, **Max Response Size (KB)**, **Cache TTL (seconds)**, and **Cache Max Entries** (all must be greater than zero).
7. Toggle **Revoke on Document Change** to enable automatic token revocation when metadata changes.
8. Save the settings to apply the configuration.

## Authenticating CIMD Clients

CIMD clients initiate the OAuth authorization code flow by sending a request to `/oauth/authorize` with a URL-shaped `client_id` (e.g., `client_id=https://client.example.com/metadata`). The gateway detects the URL pattern, fetches metadata from the `client_id` URL, and validates the document against SSRF rules and schema requirements. Metadata must include `client_id` (matching the request), `redirect_uris` (non-empty array), and must not contain `client_secret` or `client_secret_expires_at`. The `token_endpoint_auth_method` defaults to `none` when omitted; secret-based methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are forbidden. The gateway synthesizes an ephemeral client by merging metadata with template application settings, caches the metadata (in-memory and database), and proceeds with standard user authentication. After the user authenticates, the gateway issues an authorization code and redirects to the `redirect_uri`. The client exchanges the code for tokens via `POST /oauth/token`, and the gateway validates the `client_id` (re-fetching metadata if cache miss) before issuing `access_token` and `refresh_token` (if `grant_types` includes `refresh_token`). For refresh token flows, the client sends `POST /oauth/token` with `grant_type=refresh_token`, and the gateway fetches CIMD metadata (from cache or origin) before issuing new tokens.
