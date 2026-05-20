# CIMD Gateway Configuration Reference

## Gateway Configuration

### CIMD Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `oidc.cimdSettings.enabled` | Enable CIMD support | `false` |
| `oidc.cimdSettings.templateId` | Application ID of the template used for CIMD clients | `app-123` |
| `oidc.cimdSettings.fetchTimeoutMs` | Timeout in milliseconds for fetching metadata documents | `3000` |
| `oidc.cimdSettings.maxResponseSizeKb` | Maximum allowed size of a metadata response in kilobytes | `20` |
| `oidc.cimdSettings.cacheTtlSeconds` | Time-to-live for cached metadata responses in seconds | `3600` |
| `oidc.cimdSettings.cacheMaxEntries` | Maximum number of entries to store in the metadata cache | `500` |

{% hint style="info" %}
The configuration property `oidc.cimdSettings.softwareId` has been renamed to `oidc.cimdSettings.templateId` in .
{% endhint %}

### SSRF Protection

| Property | Description | Example |
|:---------|:------------|:--------|
| `oidc.cimdSettings.allowPrivateIpAddress` | Allow metadata document requests to private IP addresses | `false` |
| `oidc.cimdSettings.allowUnsecuredHttpUri` | Allow metadata document requests to plain HTTP (non-HTTPS) URIs | `false` |
| `oidc.cimdSettings.allowedDomains` | Restrict metadata document to these domains (supports wildcard for first-level subdomain). Empty list allows all domains | `["*.example.com", "trusted.org"]` |

### Token Revocation Policy

| Property | Description | Example |
|:---------|:------------|:--------|
| `oidc.cimdSettings.revokeOnDocumentChange` | Revoke all tokens and consents when CIMD metadata document changes | `false` |


For instructions on enabling and configuring CIMD in a domain, see [Enable and Configure CIMD in the Console](../../../guides/enable-and-configure-cimd-in-the-console.md#enable-and-configure-cimd-in-the-console).
