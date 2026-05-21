# Integrate with CIMD Clients

## Authenticating CIMD Clients

When a user navigates to `/oauth/authorize?client_id=http://example.com/my-app&redirect_uri=...`, the gateway checks if the `client_id` is URL-shaped and CIMD is enabled. If both conditions are met, the gateway fetches the metadata document from the `client_id` URL, validates it against the template and SSRF rules, and synthesizes an ephemeral client configuration. The metadata is cached for the configured TTL. The user proceeds through the standard OAuth flow (authentication, consent). At token exchange (`/oauth/token`), the client provides the `client_id` in the request body or Basic auth header (URL-encoded). For `token_endpoint_auth_method=none`, no client secret is required. Clients can refresh tokens using `grant_type=refresh_token` by providing the `client_id`; metadata is re-fetched if the cache has expired. CIMD clients enforce exact redirect URI matching (no prefix matching).

## End-User Configuration

### CIMD Metadata Document

CIMD clients provide metadata at their `client_id` URL. The document must be valid JSON and include the following required fields:

| Field | Description | Example |
|:------|:------------|:--------|
| `client_id` | Must match the request URL | `"http://example.com/my-app"` |
| `redirect_uris` | Non-empty array of redirect URIs | `["https://app.example.com/callback"]` |

Optional fields include `client_name`, `logo_uri`, `jwks`, `jwks_uri`, `grant_types`, `response_types`, `scope`, `token_endpoint_auth_method`, `application_type`, `subject_type`, `id_token_signed_response_alg`, `request_object_signing_alg`, `require_pushed_authorization_requests`, `backchannel_token_delivery_mode`, `backchannel_authentication_request_signing_alg`, `post_logout_redirect_uris`, and `contacts`. The metadata must not include `client_secret` or `client_secret_expires_at`.

### Supported Authentication Methods

| Method | Allowed for CIMD | Requirements |
|:-------|:-----------------|:-------------|
| `none` | ✅ Yes (default) | None |
| `private_key_jwt` | ✅ Yes | Requires `jwks` or `jwks_uri` in metadata |
| `tls_client_auth` | ✅ Yes | None |
| `self_signed_tls_client_auth` | ✅ Yes | None |
| `client_secret_basic` | ❌ No | Secret-based methods not allowed |
| `client_secret_post` | ❌ No | Secret-based methods not allowed |
| `client_secret_jwt` | ❌ No | Secret-based methods not allowed |

### Logo Serving

CIMD metadata may include a `logo_uri`. The gateway fetches the logo during metadata resolution (subject to SSRF protection) and caches it with the same TTL as the metadata. Logos are capped at 256 KB. Access the logo at `/cimd/logo?clientId=http://example.com/my-app`. The endpoint returns the cached logo if present, fetches it synchronously on cache miss if metadata is still valid, or returns `404` if unavailable.

## Restrictions

- CIMD clients are ephemeral and not persisted in the applications table; metadata is fetched on-demand and cached
- Metadata cache uses LRU eviction; no manual cache invalidation API is provided
- Wildcard domain matching supports only first-level subdomain wildcards (e.g., `*.example.com` matches `app.example.com` but not `sub.app.example.com`)
- Token revocation on metadata change requires `revokeOnDocumentChange=true` and is not retroactive (applies only to new fetches)
- `jwks_uri` is validated for SSRF but not fetched during metadata resolution (fetched lazily during token validation)
- Refresh token grant requires `client_id` in request body or Basic auth header per OAuth 2.0 specification
- CIMD clients are identified by **Template Id** in SSO sessions; if the template application is deleted, SSO sessions break
- Metadata document hash is stored in `actor.attributes` (JSON column) in audit logs and is not indexed
- Storage impact may be relevant for environments managing a large volume of CIMD clients when token revocation on metadata change is enabled
