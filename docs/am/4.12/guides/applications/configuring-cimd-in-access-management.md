# Configuring CIMD in Access Management

## Prerequisites

Before enabling CIMD, ensure the following requirements are met:

* At least one application configured as a template (`template = true`).
* Template application must define allowed grant types, response types, and scopes that CIMD clients will inherit or intersect.
* HTTPS endpoints for CIMD metadata and logo URIs (unless `allowUnsecuredHttpUri` is enabled).
* Network access from the gateway to CIMD metadata and logo URIs (subject to SSRF protection rules).

## Gateway Configuration

### CIMD Settings

Configure CIMD at the domain level under OIDC settings. The following properties control CIMD behavior:

| Property | Description | Example |
|:---------|:------------|:--------|
| `oidc.cimdSettings.enabled` | Enable CIMD support | `true` |
| `oidc.cimdSettings.templateId` | Application ID of the template (required when enabled) | `"app-template-123"` |
| `oidc.cimdSettings.allowPrivateIpAddress` | Allow metadata requests to private IP addresses | `false` |
| `oidc.cimdSettings.allowUnsecuredHttpUri` | Allow plain HTTP URIs (non-HTTPS) | `false` |
| `oidc.cimdSettings.fetchTimeoutMs` | Timeout for fetching metadata in milliseconds (must be > 0) | `3000` |
| `oidc.cimdSettings.maxResponseSizeKb` | Maximum metadata response size in kilobytes (must be > 0) | `20` |
| `oidc.cimdSettings.allowedDomains` | Restrict metadata to these domains (supports `*.example.com`). Empty = allow all. | `["*.example.com", "trusted.org"]` |
| `oidc.cimdSettings.cacheTtlSeconds` | Time-to-live for cached metadata in seconds (must be > 0) | `3600` |
| `oidc.cimdSettings.cacheMaxEntries` | Maximum cache entries (must be > 0) | `500` |
| `oidc.cimdSettings.revokeOnDocumentChange` | Revoke tokens and consents when metadata hash changes | `false` |

{% hint style="info" %}
The configuration property `softwareId` has been renamed to `templateId`. Existing configurations must update this property name.
{% endhint %}

**Validation Rules:**

* `templateId` is required when CIMD is enabled.
* Numeric fields (`fetchTimeoutMs`, `maxResponseSizeKb`, `cacheTtlSeconds`, `cacheMaxEntries`) must be greater than 0.
* `allowedDomains` supports wildcard for first-level subdomains only (e.g., `*.example.com` matches `sub.example.com` but not `deep.sub.example.com`).

### OIDC Discovery

When CIMD is enabled, the OIDC discovery document (`/.well-known/openid-configuration`) includes:

```json
{
  "client_id_metadata_document_supported": true
}
```

## Creating a CIMD-Enabled Domain

To enable CIMD for a domain:

1. Navigate to the domain's OIDC settings.
2. Enable the **Enable CIMD** toggle.
3. Select a **Template Application** from the autocomplete list (filtered to applications with `template = true`).
4. Configure SSRF protection:
   * Set **Allow private/loopback IP addresses** as needed.
   * Set **Allow unsecured HTTP URIs** as needed.
5. Set numeric fields to positive integers:
   * **Fetch Timeout (ms)**
   * **Max Response Size (KB)**
   * **Cache TTL (seconds)**
   * **Cache Max Entries**
6. (Optional) Add **Allowed Domains** to restrict metadata sources (supports wildcard for first-level subdomains).
7. (Optional) Enable **Revoke tokens and consents when client metadata changes** to automatically revoke tokens when metadata hash changes.
8. Save the configuration.

The gateway will now accept CIMD clients and fetch metadata on-demand during OAuth flows.

{% hint style="warning" %}
The template application cannot be deleted or un-templated while referenced as `cimdSettings.templateId`. Attempting either operation returns a `400 Bad Request` error.
{% endhint %}
