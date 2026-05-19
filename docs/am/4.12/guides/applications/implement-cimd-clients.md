# Implement CIMD Clients

## Using CIMD Clients

Clients present a URL as their `client_id` in OAuth authorization and token requests. On first authorization request, the gateway fetches the metadata document from the `client_id` URL or uses a cached copy if available. The gateway validates the metadata, synthesizes a client configuration by merging metadata with the template application, and proceeds with the OAuth flow.

### Authorization Code Flow

1. The client sends `GET /oauth/authorize?client_id=http://example.com/my-app&redirect_uri=...&response_type=code`
2. The gateway fetches and validates metadata from `http://example.com/my-app`
3. The user authenticates and consents
4. The gateway redirects to `redirect_uri` with an authorization code

### Token Exchange

The client sends `POST /oauth/token` with:
- `grant_type=authorization_code`
- `code` (authorization code from previous step)
- `redirect_uri`
- `client_id=http://example.com/my-app`

The gateway issues `access_token`, `id_token`, and (if `grant_types` includes `refresh_token`) `refresh_token`.

### Refresh Token Flow

The client sends `POST /oauth/token` with:
- `grant_type=refresh_token`
- `refresh_token`
- `client_id`

The gateway validates the `client_id` matches the refresh token's client and issues a new `access_token`.

### Token Revocation

The client sends `POST /oauth/revoke` with:
- `token`
- `token_type_hint` (optional)
- `client_id`

The gateway revokes the token.

### Token Introspection

The caller sends `POST /oauth/introspect` with:
- `token`
- Basic auth credentials

The gateway returns `{"active": true, "client_id": "http://example.com/my-app", ...}` for valid tokens or `{"active": false}` for revoked or invalid tokens.

## End-User Configuration

### CIMD Metadata Document Schema

CIMD clients provide metadata at a URL-shaped `client_id`. The gateway fetches and validates the following fields:

| Field | Description | Example |
|:------|:------------|:--------|
| `client_id` | Must match the request URL (canonicalized: lowercase scheme/host, normalized path) | `"http://example.com/my-app"` |
| `client_name` | Human-readable client name | `"My Application"` |
| `redirect_uris` | Non-empty array of redirect URIs (required) | `["https://app.example.com/callback"]` |
| `token_endpoint_auth_method` | Authentication method (default: `"none"`; secret-based methods forbidden) | `"none"`, `"private_key_jwt"` |
| `grant_types` | Supported grant types (default: `["authorization_code"]`) | `["authorization_code", "refresh_token"]` |
| `response_types` | Supported response types (default: `["code"]`) | `["code"]` |
| `scope` | Space-separated list of scopes | `"openid profile email"` |
| `logo_uri` | URL to client logo (max 256 KB) | `"https://example.com/logo.png"` |
| `jwks_uri` | URL to JWKS document (required for `private_key_jwt`) | `"https://example.com/jwks"` |
| `jwks` | Inline JWKS document (alternative to `jwks_uri`) | `{"keys": [...]}` |
| `application_type` | Application type | `"web"` |
| `subject_type` | Subject identifier type | `"public"` |
| `id_token_signed_response_alg` | ID token signing algorithm | `"RS256"` |
| `request_object_signing_alg` | Request object signing algorithm | `"RS256"` |
| `backchannel_token_delivery_mode` | CIBA token delivery mode | `"poll"` |
| `backchannel_authentication_request_signing_alg` | CIBA request signing algorithm | `"RS256"` |
| `require_pushed_authorization_requests` | Require PAR | `true` |
| `post_logout_redirect_uris` | Post-logout redirect URIs | `["https://app.example.com/logout"]` |
| `contacts` | Contact email addresses | `["admin@example.com"]` |

The fields `client_secret` and `client_secret_expires_at` must not be present in CIMD metadata. If `token_endpoint_auth_method` is `private_key_jwt`, metadata must include `jwks` or `jwks_uri`. If `jwks_uri` is present, it must be a valid HTTPS URL (unless **Allow Unsecured HTTP URIs** is enabled) and must not resolve to a private IP (unless **Allow Private/Loopback IP Addresses** is enabled).

## Restrictions

- CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`)
- CIMD clients always enforce exact `redirect_uri` matching, regardless of domain-level **Redirect URI Strict Matching** setting
- Logo fetching is limited to 256 KB per logo
- Metadata documents are limited to **Max Response Size (KB)** (default: 20 KB)
- `jwks_uri` and `logo_uri` must be HTTPS unless **Allow Unsecured HTTP URIs** is enabled
- `jwks_uri` and `logo_uri` must not resolve to private IP addresses unless **Allow Private/Loopback IP Addresses** is enabled
- Template applications cannot be deleted or un-templated while they are referenced as the CIMD template (see [Enable CIMD](enable-cimd.md))
- CIMD metadata changes are detected by SHA-256 hash comparison; hash collisions (extremely unlikely) could prevent revocation on document change
- Pre-registered applications with a `client_id` matching a CIMD URL take precedence over remote CIMD metadata
- Changes to template application settings do not trigger automatic token revocation, even when **Revoke Tokens and Consents When Client Metadata Changes** is enabled

## Related Changes

The OIDC discovery document now advertises `client_id_metadata_document_supported` when CIMD is enabled. A new CIMD settings page is available at `/domains/:domainId/settings/cimd` with form fields for enabling CIMD, selecting a template application, configuring SSRF protection, specifying allowed domains, and setting cache parameters. Template applications display a "Template Application" badge in the application list and general settings. If an application is the CIMD template, it displays "CIMD Template Application (cannot be deleted or un-templated)" and delete/un-template actions are disabled. Audit logs for CIMD client authentication and token events include `metadataDocumentHash` in actor attributes; actor links for CIMD clients do not navigate to the application detail page. The property `oidc.cimdSettings.softwareId` has been renamed to `oidc.cimdSettings.templateId`; update domain configuration accordingly. New event types `CIMD_METADATA.DEPLOY`, `CIMD_METADATA.UPDATE`, and `CIMD_METADATA.UNDEPLOY` track metadata document lifecycle. A new database table `cimd_client_state` stores metadata document hashes for revocation-on-change detection, with columns `id`, `domain_id`, `client_id`, `metadata_hash`, `created_at`, and `updated_at`, and a unique index on `(domain_id, client_id)`.
