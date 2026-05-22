# Configuring CIMD Gateway Settings

## Prerequisites

Before configuring CIMD gateway settings, ensure the following:

* At least one application is marked as a template (`template: true`).
* The template application defines allowed grant types, response types, and scopes.
* The template application configures identity providers, MFA, and other non-OAuth settings.
* The domain has `domain_openid_read` and `domain_openid_update` permissions for CIMD settings management.

## Gateway Configuration

### CIMD settings

Configure CIMD support using the following `oidc.cimdSettings.*` properties in `gravitee.yml`:

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `oidc.cimdSettings.enabled` | Boolean | `false` | Enable Client ID Metadata Document support. |
| `oidc.cimdSettings.templateId` | String | (required when enabled) | Application ID of the template used for CIMD clients. Required when `enabled` is `true`. |
| `oidc.cimdSettings.allowPrivateIpAddress` | Boolean | `false` | Allow metadata document requests to private IP addresses. |
| `oidc.cimdSettings.allowUnsecuredHttpUri` | Boolean | `false` | Allow metadata document requests to plain HTTP (non-HTTPS) URIs. |
| `oidc.cimdSettings.fetchTimeoutMs` | Integer | `3000` | Timeout in milliseconds for fetching client metadata documents. Must be greater than 0. |
| `oidc.cimdSettings.maxResponseSizeKb` | Integer | `20` | Maximum allowed size of a metadata response in kilobytes. Must be greater than 0. |
| `oidc.cimdSettings.allowedDomains` | List<String> | `[]` | Restrict metadata document to these domains. Supports wildcard for first-level subdomain (e.g., `*.example.com`). Empty list allows all domains. |
| `oidc.cimdSettings.cacheTtlSeconds` | Integer | `3600` | Time-to-live for cached metadata responses in seconds. Must be greater than 0. |
| `oidc.cimdSettings.cacheMaxEntries` | Integer | `500` | Maximum number of entries to store in the metadata cache. Must be greater than 0. |
| `oidc.cimdSettings.revokeOnDocumentChange` | Boolean | `false` | Revoke all tokens and consents when CIMD metadata document changes. |

**Validation Rules:**

* `templateId` is required when `enabled` is `true`.
* `fetchTimeoutMs` must be greater than 0.
* `maxResponseSizeKb` must be greater than 0.
* `cacheTtlSeconds` must be greater than 0.
* `cacheMaxEntries` must be greater than 0.
* `allowedDomains` entries must be valid hostnames. Wildcard (`*`) is supported only for first-level subdomains (e.g., `*.example.com`).

## Creating a CIMD-Enabled Domain

To enable CIMD support, configure the domain's OIDC settings with a template application and SSRF protection rules:

1. Ensure at least one application is marked as a template (`template: true`).
2. Set `oidc.cimdSettings.enabled` to `true`.
3. Specify the `templateId` of the template application.
4. Configure SSRF protection by setting `allowPrivateIpAddress`, `allowUnsecuredHttpUri`, and `allowedDomains` according to your security requirements.
5. Adjust `fetchTimeoutMs` and `maxResponseSizeKb` to control metadata fetch behavior.
6. Configure caching with `cacheTtlSeconds` and `cacheMaxEntries` to balance performance and freshness.
7. (Optional) Enable `revokeOnDocumentChange` to automatically revoke tokens when metadata changes.

## Authenticating CIMD Clients

CIMD clients authenticate by presenting their metadata URL as the `client_id` in OAuth flows:

1. **Authorization Request:** The gateway checks if the `client_id` is URL-shaped (matches `^https?://`). If yes, the gateway fetches the metadata document from the `client_id` URL, validates it, and caches the result. Template application settings are merged with metadata to synthesize the client configuration. The client proceeds through the authorization flow using the synthesized configuration.
2. **Token Exchange:** The client sends the `client_id` in the token request. The gateway resolves the client from cache or re-fetches metadata if expired. The issued token includes an `aud` claim set to the `client_id` URL.
3. **Refresh Token:** The client sends the `client_id` in the refresh request (body or Basic auth). The gateway resolves the client from cache to issue a new access token.
4. **Token Revocation:** The client sends the `client_id` in the revocation request. The gateway resolves the client from cache to revoke the token.
