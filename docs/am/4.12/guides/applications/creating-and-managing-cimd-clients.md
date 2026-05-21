# Creating and Managing CIMD Clients

## Creating a CIMD Client

To authenticate a CIMD client, host a JSON metadata document at a publicly accessible URL (e.g., `https://client.example.com/metadata`). The metadata document must contain at minimum:

```json
{
  "client_id": "https://client.example.com/metadata",
  "redirect_uris": ["https://client.example.com/callback"]
}
```

The `client_id` field must match the URL hosting the metadata document, and `redirect_uris` must be a non-empty array.

Initiate an OAuth 2.0 authorization code flow using the metadata document URL as the `client_id` parameter. The Authorization Server fetches the metadata document, validates it against the template application and trust rules, synthesizes an ephemeral client configuration, and caches the result. The client proceeds through the standard authorization flow, receiving tokens with the `aud` claim set to the canonical `client_id` URL.

Redirect URIs are matched exactly (no prefix matching), regardless of the domain's `redirectUriStrictMatching` setting.

## Managing CIMD Clients

CIMD clients are ephemeral and exist only in the in-memory cache. They are not listed in the Applications UI.

To revoke a CIMD client's tokens, enable **Revoke Tokens and Consents When Client Metadata Changes** in Domain Settings → OAuth 2.0 → CIMD. When the metadata document changes (detected by SHA-256 hash comparison), all access tokens, refresh tokens, and scope approvals for the client are revoked automatically.

To manually revoke tokens, use the token revocation endpoint (`POST /{domain}/oauth/revoke`) with the `client_id` and `token` parameters. For refresh token revocation, include `token_type_hint=refresh_token`.

Audit logs for CIMD clients include the `metadataDocumentHash` in `actor.attributes` but do not link to application detail pages.

### Logo Fetching

CIMD clients can specify a `logo_uri` in their metadata document. The Authorization Server fetches the logo on-demand and caches it.

To retrieve a cached logo, call `GET /{domain}/cimd/logo?clientId={url-encoded-client-id}`. The endpoint returns `200 OK` with `Content-Type: image/*` and `Cache-Control: max-age={seconds}` on success, or `404 Not Found` if the logo is not cached or the metadata lacks a `logo_uri`. Remote `logo_uri` values are never served directly; the gateway fetches them using the same trust rules as metadata documents.

## End-User Configuration

### CIMD Settings Page

Navigate to Domain Settings → OAuth 2.0 → CIMD to configure CIMD support.

<figure><img src="../../.gitbook/assets/am-cimd-revocation-setting.png" alt="CIMD revoke tokens and consents on metadata change toggle"><figcaption></figcaption></figure>


<figure><img src="../../.gitbook/assets/am-cimd-cache-settings.png" alt="CIMD cache TTL and max entries configuration fields"><figcaption></figcaption></figure>


<figure><img src="../../.gitbook/assets/am-cimd-allowed-domains.png" alt="CIMD allowed domains configuration field with wildcard support"><figcaption></figcaption></figure>


<figure><img src="../../.gitbook/assets/am-cimd-fetch-settings.png" alt="CIMD fetch timeout and max response size configuration fields"><figcaption></figcaption></figure>


<figure><img src="../../.gitbook/assets/am-cimd-ssrf-protection.png" alt="CIMD SSRF protection settings including private IP and unsecured HTTP toggles"><figcaption></figcaption></figure>


<figure><img src="../../.gitbook/assets/am-cimd-settings-overview.png" alt="CIMD settings page showing enable toggle and template application selector"><figcaption></figcaption></figure>

| Field | Description | Example |
|:------|:------------|:--------|
| **Enable CIMD** | Toggle to enable Client ID Metadata Document support | Enabled |
| **Template Application** | Select an application configured as a template (required when CIMD is enabled) | `My Template App` |
| **Allow Private/Loopback IP Addresses** | Allow metadata document requests to private, loopback, link-local, or any-local IP addresses | Disabled |
| **Allow Unsecured HTTP URIs** | Allow metadata document requests to plain HTTP (non-HTTPS) URIs | Disabled |
| **Fetch Timeout (ms)** | Timeout in milliseconds for fetching client metadata documents (must be > 0) | `3000` |
| **Max Response Size (KB)** | Maximum allowed size of a metadata response in kilobytes (must be > 0) | `20` |
| **Allowed Domains** | Restrict metadata document to these domains (supports wildcard for first-level subdomain). Empty list allows all domains | `example.com`, `*.trusted.com` |
| **Cache TTL (seconds)** | Time-to-live for cached metadata responses in seconds (must be > 0) | `3600` |
| **Cache Max Entries** | Maximum number of entries to store in the metadata cache (must be > 0) | `500` |
| **Revoke Tokens and Consents When Client Metadata Changes** | Revoke all tokens and consents when CIMD metadata document changes | Disabled |

### Token Introspection and Revocation

CIMD clients support token introspection and revocation.

To introspect a token, authenticate with a registered (non-CIMD) client and call `POST /{domain}/oauth/introspect` with the `token` parameter. The response includes `client_id` and `aud` fields.

To revoke a token, call `POST /{domain}/oauth/revoke` with the `client_id` and `token` parameters. For refresh token revocation, include `token_type_hint=refresh_token`. Revocation succeeds if the `client_id` matches the token's audience.

## Restrictions

- CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`)
- CIMD clients cannot specify `client_secret` or `client_secret_expires_at` in metadata
- HTTP redirects are not followed when fetching metadata documents
- Logo URIs are fetched synchronously on cache miss, which may introduce latency
- Metadata cache is in-memory only and not persisted across gateway restarts
- **Revoke Tokens and Consents When Client Metadata Changes** requires database queries on every metadata re-fetch
- Template applications cannot be deleted or un-templated while referenced as the CIMD template
- CIMD clients are not listed in the Applications UI (ephemeral, cache-only)
- Audit logs for CIMD clients do not link to application detail pages
- CIMD clients always use exact redirect URI matching (no prefix matching)
- Changes to template application settings do not trigger token revocation, even when **Revoke Tokens and Consents When Client Metadata Changes** is enabled
- Pre-registered applications with a `client_id` matching a CIMD URL take precedence over remote metadata
