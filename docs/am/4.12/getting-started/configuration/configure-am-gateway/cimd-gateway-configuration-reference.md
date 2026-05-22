# CIMD Gateway Configuration Reference

## Prerequisites

Before configuring CIMD for a domain, ensure the following requirements are met:

* Access Management 4.6 or later
* A template application configured with baseline OAuth settings (grant types, response types, scopes, identity providers, MFA policies)
* Domain-level permission `domain_openid_read` to configure CIMD settings
* HTTPS-accessible metadata document endpoint for each CIMD client (or HTTP if `allowUnsecuredHttpUri` is enabled)

## Gateway Configuration

### CIMD Settings

Configure CIMD behavior at the domain level using the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `oidc.cimdSettings.enabled` | Enable or disable CIMD support for the domain. | `true` |
| `oidc.cimdSettings.templateId` | Application ID of the template used for CIMD clients. Required when CIMD is enabled. | `app-template-123` |
| `oidc.cimdSettings.allowPrivateIpAddress` | Allow metadata document requests to private, loopback, link-local, and any-local IP addresses. | `false` |
| `oidc.cimdSettings.allowUnsecuredHttpUri` | Allow metadata document requests to plain HTTP (non-HTTPS) URIs. | `false` |
| `oidc.cimdSettings.fetchTimeoutMs` | Timeout in milliseconds for fetching client metadata documents. Must be greater than 0. | `3000` |
| `oidc.cimdSettings.maxResponseSizeKb` | Maximum allowed size of a metadata response in kilobytes. Must be greater than 0. | `20` |
| `oidc.cimdSettings.allowedDomains` | Restrict metadata document fetching to these domains. Supports wildcard for first-level subdomain (e.g., `*.example.com`). Empty list allows all domains. | `["example.com", "*.trusted.org"]` |
| `oidc.cimdSettings.cacheTtlSeconds` | Time-to-live for cached metadata responses in seconds. Must be greater than 0. | `3600` |
| `oidc.cimdSettings.cacheMaxEntries` | Maximum number of entries to store in the metadata cache. Must be greater than 0. | `500` |
| `oidc.cimdSettings.revokeOnDocumentChange` | Revoke all tokens and consents when the CIMD metadata document changes. | `false` |

**Validation rules:**

* `fetchTimeoutMs`, `maxResponseSizeKb`, `cacheTtlSeconds`, and `cacheMaxEntries` must be greater than 0.
* `allowedDomains` supports wildcard notation (`*.example.com`) for first-level subdomains only. An empty list allows all domains.

### OIDC Discovery

When CIMD is enabled, the OIDC discovery document (`/.well-known/openid-configuration`) advertises support:

```json
{
  "client_id_metadata_document_supported": true
}
```

### CIMD Logo Endpoint

The CIMD logo endpoint returns cached logos for CIMD clients:

| Property | Description | Example |
|:---------|:------------|:--------|
| **Path** | `/{domain}/cimd/logo` | `/my-domain/cimd/logo` |
| **Method** | `GET` | |
| **Query Parameter: clientId** | URL-encoded canonical `client_id` of the CIMD client. | `?clientId=https%3A%2F%2Fclient.example.com` |
| **Response (200 OK)** | Returns cached logo with `Content-Type: image/*` and `Cache-Control: max-age={seconds}`. | |
| **Response (404 Not Found)** | Logo not cached, metadata does not contain `logo_uri`, or metadata is expired. | |

On cache miss, the endpoint fetches the logo from `logo_uri` if metadata is cached and non-expired. Logo fetch applies the same SSRF protection as metadata fetch and is limited to 256 KB.

## Creating a CIMD-Enabled Domain

{% hint style="info" %}
The procedure for configuring CIMD settings in the Console UI is covered in a separate topic.
{% endhint %}
