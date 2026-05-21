# CIMD Operational Reference

## Creating CIMD Clients

CIMD clients are not created manually in the console. When a client presents a `client_id` matching the pattern `^https?://` during authorization, Access Management fetches the metadata document from that URL, validates it against the template application and SSRF rules, and synthesizes an ephemeral client configuration.

The metadata document must include:

| Field | Required | Validation |
|:------|:---------|:-----------|
| `client_id` | Yes | Must exactly match the request URL in canonical form |
| `redirect_uris` | Yes | Must be a non-empty array |
| `token_endpoint_auth_method` | No | Defaults to `none`. Secret-based methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`) are forbidden |
| `grant_types` | No | Defaults to `["authorization_code"]`. Intersected with template's allowed grant types |
| `response_types` | No | Defaults to `["code"]`. Intersected with template's allowed response types |
| `scope` | No | Space-separated string. Intersected with template's scope settings |
| `jwks` or `jwks_uri` | Conditional | Required if `token_endpoint_auth_method` is `private_key_jwt` |

Grant types, response types, and scopes declared in the metadata are intersected with the template application's allowed values. If the intersection is empty, the client is created with no allowed grants, responses, or scopes.

## Managing CIMD Tokens

CIMD clients follow standard OAuth flows with specific constraints.

During token refresh, the `client_id` (the metadata URL) must be provided in the request body or Basic auth header (URL-encoded). Refresh tokens are validated against the CIMD client's metadata hash. If the hash has changed and revocation-on-change is enabled, the refresh token is invalid.

Token revocation requires the `client_id` in the request body and revokes access or refresh tokens for the CIMD client. Introspection responses include the metadata URL as the `client_id`.

Redirect URI validation always requires exact matching, even if the domain's `redirectUriStrictMatching` is `false`.

## End-User Configuration

Navigate to **Settings → OAuth 2.0 → CIMD** in the domain console. Configure the following settings:

1. Toggle **Enable CIMD** to enable or disable CIMD support for the domain.
2. Select a **Template Application** from the autocomplete dropdown (filtered to show only applications with `template = true`).
3. Toggle **Allow private/loopback IP addresses** to permit metadata document requests to private IP addresses (SSRF protection).
4. Toggle **Allow unsecured HTTP URIs** to permit metadata document requests to plain HTTP URIs (SSRF protection).
5. Enter a value in the **Fetch Timeout (ms)** field to set the timeout for metadata fetch requests.
6. Enter a value in the **Max Response Size (KB)** field to set the maximum allowed metadata response size.
7. Add domain patterns to the **Allowed Domains** chip list to restrict metadata document requests to specific domains (supports `*.example.com` wildcard).
8. Enter a value in the **Cache TTL (seconds)** field to set the time-to-live for cached metadata responses.
9. Enter a value in the **Cache Max Entries** field to set the maximum number of entries in the metadata cache.
10. Toggle **Revoke on Document Change** to revoke all tokens and consents when the CIMD metadata document changes.

| Field | Description | Validation |
|:------|:------------|:-----------|
| **Enable CIMD** | Enable/disable CIMD support | — |
| **Template Application** | Template application for CIMD clients | Required when CIMD is enabled; must reference an existing application marked as template |
| **Allow Private/Loopback IP Addresses** | SSRF protection setting | — |
| **Allow Unsecured HTTP URIs** | SSRF protection setting | — |
| **Fetch Timeout (ms)** | Metadata fetch timeout | Must be > 0 |
| **Max Response Size (KB)** | Maximum metadata response size | Must be > 0 |
| **Allowed Domains** | Domain whitelist (supports `*.example.com`) | — |
| **Cache TTL (seconds)** | Metadata cache TTL | Must be > 0 |
| **Cache Max Entries** | Maximum cache entries | Must be > 0 |
| **Revoke on Document Change** | Revoke tokens when metadata changes | — |

### CIMD Logo Endpoint

**Endpoint:** `GET /cimd/logo?clientId={url-encoded-client-id}`

Serves pre-fetched or on-demand client logos for CIMD clients. Returns cached logo if available. On cache miss, fetches logo from `logo_uri` in the metadata document (if metadata is cached and `logo_uri` is set). Applies the same SSRF protection as metadata fetch. Returns `404` if logo not found or metadata unavailable.

**Response Headers:**
- `Content-Type`: MIME type from cached logo (e.g., `image/png`)
- `Cache-Control`: `max-age={seconds}` based on metadata TTL

## Restrictions

- CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`)
- CIMD clients always require exact redirect URI matching (no prefix matching)
- Metadata documents larger than `maxResponseSizeKb` are rejected
- Logo URIs are fetched using the same SSRF protection rules as metadata documents
- Logo cache is in-memory only (not persisted across gateway restarts)
- CIMD clients cannot be pre-registered in the console (they are ephemeral, synthesized from metadata)
- Template application cannot be deleted or un-templated while it is the active CIMD template
- `grant_types`, `response_types`, and `scope` in metadata are intersected with template settings (not replaced)
- Metadata document changes are detected via SHA-256 hash comparison; hash collisions (theoretical) could prevent revocation
- Changes to template application settings do not trigger token revocation for CIMD clients (only remote metadata changes trigger revocation when enabled)
- JWKS public keys from CIMD metadata are stored in the in-memory cache alongside keys for pre-registered clients
- Token revocation policy data (metadata hashes) persists indefinitely while enabled; storage impact may be relevant for environments managing a large volume of CIMD clients

## Related Changes

The OIDC discovery document (`/.well-known/openid-configuration`) now advertises `client_id_metadata_document_supported: true` when CIMD is enabled.

Applications marked as CIMD template display a "CIMD Template" badge in the console and cannot be deleted or un-templated while active.

Audit logs for CIMD clients include a `metadataDocumentHash` actor attribute (SHA-256 hash of the metadata document at time of authentication). Actors with this attribute do not link to application detail pages (ephemeral clients).

The configuration property `oidc.cimdSettings.softwareId` has been renamed to `oidc.cimdSettings.templateId`. Existing `softwareId` values must be migrated.
