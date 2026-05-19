# CIMD Logo Endpoint and Discovery Metadata

## End-User Configuration

### CIMD Logo Endpoint

**Endpoint:** `GET /{domain}/cimd/logo?clientId={url-encoded-client-id}`

Serves pre-fetched or on-demand client logos for CIMD clients. Returns cached logo if available. On cache miss, fetches logo from `logo_uri` if metadata is cached and valid. Returns `404` if no logo is available. Applies the same SSRF protection as metadata fetch.

**Response Headers:**
- `Content-Type`: MIME type from original `logo_uri` response
- `Cache-Control`: `max-age={remaining-ttl-seconds}`

### OIDC Discovery Metadata

When CIMD is enabled, the OIDC discovery document (`/.well-known/openid-configuration`) includes `"client_id_metadata_document_supported": true`.

## Restrictions

- Logo fetch is limited to 256 KB
