# CIMD Client Authentication Flow and Endpoints

## Authenticating CIMD Clients

When a client presents a URL-shaped `client_id` during OAuth authorization, the Authorization Server canonicalizes the URL (lowercasing the scheme and host, removing default ports) and checks the in-memory cache for the metadata document. On a cache miss, the server validates the URL host against SSRF protection rules (private IP addresses, unsecured HTTP, allowed domains), performs DNS resolution, and fetches the metadata document with the configured timeout and size limit. The server validates the JSON structure, required fields (`client_id`, `redirect_uris`), and forbidden fields (`client_secret`, `client_secret_expires_at`). It computes a SHA-256 hash of the metadata document and synthesizes a client configuration by cloning the template application and applying metadata overrides. The `token_endpoint_auth_method` defaults to `none` if absent in the metadata. The `grant_types`, `response_types`, and `scope` from the metadata are intersected with the template's allowed values. Extended metadata fields (`application_type`, `subject_type`, `client_uri`, `policy_uri`, `tos_uri`, `software_id`, `software_version`, `tls_client_auth_subject_dn`, `backchannel_token_delivery_mode`, `require_pushed_authorization_requests`, `post_logout_redirect_uris`, `contacts`) are applied if present and non-blank. If the metadata includes a `logo_uri`, the server pre-fetches the logo (up to 256 KB) and caches it separately. The synthesized client is stored in the cache with the configured TTL. The Authorization Server proceeds with the standard OAuth 2.0 authorization code flow, enforcing exact `redirect_uri` matching (no prefix matching). Tokens are issued with `aud` set to the CIMD `client_id` URL, and the `metadataDocumentHash` is stored in audit log actor attributes. If token revocation on metadata change is enabled, the server compares the new hash with the stored hash in the `cimd_client_state` table; if the hash differs, all tokens and consents for the client are revoked, and the stored hash is updated.

## End-User Configuration

### CIMD Logo Endpoint

**Endpoint:** `GET /{domain}/cimd/logo?clientId={url-encoded-client-id}`

Serves a pre-fetched or on-demand fetched logo for a CIMD client. Returns the cached logo if available. On a cache miss, fetches the logo from the `logo_uri` in the metadata document if the metadata is cached and not expired. Returns `404` if no logo is available or metadata is not found. Returns `200` with `Content-Type` and `Cache-Control` headers on success.

### OIDC Discovery Metadata

When CIMD is enabled, the OIDC discovery document (`/.well-known/openid-configuration`) includes `"client_id_metadata_document_supported": true`.

## Restrictions

- CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`)
- CIMD clients cannot declare `client_secret` or `client_secret_expires_at` in the metadata document
- CIMD clients always require exact `redirect_uri` matching (no prefix matching), even if the domain allows non-strict matching
- Logo fetching is limited to 256 KB
- Metadata document fetching is limited to the configured `maxResponseSizeKb` (default 20 KB)
- The metadata cache is in-memory only and is not persisted across gateway restarts
- The template application cannot be deleted or un-templated while referenced as the CIMD `templateId`
- Token revocation on metadata change requires database support for the `cimd_client_state` table (JDBC only)
- CIMD clients inherit the template's identity providers, certificate settings, and other non-overridable properties
- `grant_types`, `response_types`, and `scope` in the metadata document are intersected with the template's allowed values (not replaced)
- Pre-registered applications with URL-shaped `client_id` values take precedence over CIMD metadata fetching
- Token revocation on metadata change detects changes in remote CIMD metadata only; changes to the template application do not trigger revocation
- JWKS public keys from CIMD metadata are stored in the in-memory cache alongside keys for pre-registered clients
- Stored metadata hash data persists indefinitely while the revocation policy is enabled and is deleted when the policy is disabled

## Related Changes

Audit logs for CIMD clients include the `metadataDocumentHash` in actor attributes, and the actor link is disabled (no application detail page).


<figure><img src="../.gitbook/assets/am-audit-cimd-client.png" alt="Audit log entry for CIMD client showing metadataDocumentHash"><figcaption></figcaption></figure>
