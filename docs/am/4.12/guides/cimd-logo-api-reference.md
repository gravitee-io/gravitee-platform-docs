# CIMD Logo API Reference

### CIMD Logo API

**Endpoint:** `GET /{domain}/cimd/logo?clientId={url-encoded-client-id}`

**Purpose:** Retrieve the logo for a CIMD client from the in-memory cache.

**Behavior:**
- Returns `200 OK` with `Content-Type` and `Cache-Control` headers if logo is cached.
- Fetches logo synchronously and caches it if not cached but metadata is valid and `logo_uri` is set.
- Returns `404 Not Found` if no logo is available.

**Example Request:**
```http
GET /my-domain/cimd/logo?clientId=http%3A%2F%2Fexample.com%2Fmy-app HTTP/1.1
```

**Example Response:**
```http
HTTP/1.1 200 OK
Content-Type: image/png
Cache-Control: max-age=3600

<binary image data>
```

## Restrictions

- CIMD clients cannot be pre-registered — they are synthesized on-demand from metadata documents and do not persist in the `applications` table.
- CIMD clients always require exact `redirect_uri` matching, even if domain-level `redirectUriStrictMatching` is `false`.
- CIMD metadata cache is in-memory only and is lost on gateway restart. First request after restart fetches metadata remotely.
- Logo fetch is synchronous on cache miss, which may introduce latency if the logo is not cached and metadata is valid.
- `allowedDomains` supports wildcard only for first-level subdomains (e.g., `*.example.com` matches `sub.example.com` but not `deep.sub.example.com`).
- JWKS URIs must be HTTPS unless `allowUnsecuredHttpUri = true`.
- Template application cannot be deleted or un-templated while referenced as `cimdSettings.templateId`. Attempting either operation returns `400 Bad Request` with error message: `"Application is referenced as a CIMD template and cannot be modified"`.
- Token revocation on metadata change is opt-in via `revokeOnDocumentChange = true`. When enabled, stored hashes persist indefinitely and are deleted only when the policy is disabled.
- CIMD clients do not appear in the application list or have detail pages in the console.
- CIMD clients cannot use secret-based authentication methods (`client_secret_basic`, `client_secret_post`, `client_secret_jwt`). Only `none` and `private_key_jwt` are allowed.
- `grant_types`, `response_types`, and `scope` in CIMD metadata are intersected with the template application's allowed values. Metadata cannot request grants, response types, or scopes not allowed by the template.
