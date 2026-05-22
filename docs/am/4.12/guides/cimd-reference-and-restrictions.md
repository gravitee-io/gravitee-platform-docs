# CIMD Reference and Restrictions

## CIMD Settings Reference

| Field | Description | Example |
|:------|:------------|:--------|
| **Client ID Metadata Document (CIMD) support** | Enable support for Client ID Metadata Document | Enabled |
| **Template Application** | The template application used in CIMD requests | `app-template-001` |
| **Allow private/loopback IP addresses** | Allow metadata document requests to private IP addresses | Disabled |
| **Allow unsecured HTTP URIs** | Allow metadata document requests to plain HTTP URIs | Disabled |
| **Fetch Timeout (ms)** | Timeout in milliseconds for fetching client metadata documents | `3000` |
| **Max Response Size (KB)** | Maximum allowed size of a metadata response in kilobytes | `20` |
| **Allowed Domains** | List of allowed domains for metadata document (supports `*.example.com`) | `*.example.com, trusted.org` |
| **Cache TTL (seconds)** | Time-to-live for cached metadata responses in seconds | `3600` |
| **Cache Max Entries** | Maximum number of entries to store in the metadata cache | `500` |
| **Revoke on Document Change** | Revoke all tokens and consents when metadata document changes | Disabled |

### CIMD Logo Endpoint

**Endpoint:** `GET /{domain}/cimd/logo?clientId={url-encoded-client-id}`

Retrieves the logo image for a CIMD client. The gateway fetches the `logo_uri` from cached metadata (or fetches metadata on cache miss), validates the URI against SSRF rules, and retrieves the logo with a 256 KB size limit. Logos are cached in-memory with TTL equal to the remaining metadata TTL.

**Responses:**
- `200 OK` with `Content-Type: image/*` and `Cache-Control: max-age={ttl}` when successful
- `404 Not Found` when no logo is available or metadata is missing

## Restrictions

- CIMD clients are ephemeral and not persisted in the `applications` table; they exist only in cache and are synthesized on-demand
- CIMD metadata documents must be publicly accessible or within `allowedDomains` if configured
- Logo URIs are fetched synchronously on cache miss, which may introduce latency on first request
- Maximum logo size is 256 KB (hardcoded)
- CIMD clients always use exact redirect URI matching, ignoring the domain's `redirectUriStrictMatching` setting
- CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`)
- CIMD metadata cache is in-memory only and not shared across gateway instances; database persistence is for consistency, not primary storage
- CIMD metadata changes are detected via SHA-256 hash comparison; hash collisions (though astronomically unlikely) would prevent revocation
- CIMD clients do not appear in the Management Console's application list
- CIMD template applications cannot be deleted or un-templated while referenced in `oidc.cimdSettings.templateId`
- Wildcard in `allowedDomains` supports only first-level subdomain (e.g., `*.example.com` matches `app.example.com` but not `api.app.example.com`)
- `token_endpoint_auth_method` defaults to `none` when omitted in metadata, overriding the template application's value
- `grant_types`, `response_types`, and `scope` are intersected with template application values; metadata cannot expand beyond template restrictions
- Changes to template application settings do not trigger token revocation, even when "Revoke on Document Change" is enabled
- CIMD metadata must not contain `client_secret` or `client_secret_expires_at` fields
- `jwks` or `jwks_uri` is required when `token_endpoint_auth_method` is `private_key_jwt`
- `jwks_uri` must pass SSRF validation (same rules as `client_id`)
- `fetchTimeoutMs`, `maxResponseSizeKb`, `cacheTtlSeconds`, and `cacheMaxEntries` must all be greater than zero
- `allowedDomains` entries must be valid domain patterns; wildcard is only allowed for first-level subdomain
- Pre-registered applications with URL-shaped `client_id` values take precedence over CIMD metadata

## Related Changes

When CIMD is enabled, the OIDC discovery document (`/.well-known/openid-configuration`) includes `"client_id_metadata_document_supported": true`. Applications marked as templates display a "Template" badge in the Management Console, and applications referenced as CIMD `templateId` display a "CIMD Template" badge. CIMD template applications cannot be deleted or un-templated via the UI (controls are disabled). Audit logs for CIMD clients include a `metadataDocumentHash` attribute (SHA-256 hash of metadata JSON) and do not link to application detail pages. The property `oidc.cimdSettings.softwareId` was renamed to `oidc.cimdSettings.templateId` in version 4.6; existing configurations must be updated to use the new property name.
