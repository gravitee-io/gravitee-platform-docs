### Overview

Domain certificate settings allow administrators to configure a fallback certificate that the Access Management gateway uses when a client-specific certificate is unavailable or fails to load. This feature prevents authentication failures by providing a secondary certificate for JWT signing and client authentication operations.

This feature is intended for API platform administrators managing multi-tenant or high-availability environments.

### Certificate Selection Hierarchy

When resolving a certificate for a client, the gateway follows this fallback chain:

1. Client-specific certificate configured on the application
2. Domain fallback certificate from domain settings
3. Default HMAC certificate (if legacy fallback is enabled)
4. Error if all options are exhausted

The gateway logs warnings when falling back from a configured certificate to the domain fallback or default certificate.

### Domain Isolation

Certificates are scoped to domains:

* **Regular domains** can only access certificates where the certificate's domain ID matches the current domain
* **Master domains** can access certificates from all domains to support cross-domain introspection workflows

Fallback certificate validation enforces domain ownership. A certificate from domain A cannot be configured as the fallback for domain B.

### Event-Driven Updates

Certificate settings updates trigger a `DOMAIN_CERTIFICATE_SETTINGS` event rather than a full domain reload. The certificate manager subscribes to these events and updates its internal reference atomically, allowing configuration changes without service interruption.

### Prerequisites

* Domain must exist in the organization and environment
* Fallback certificate (if configured) must exist in the same domain
* User must have `DOMAIN_SETTINGS[UPDATE]` permission on the domain, environment, or organization

### Gateway Configuration

#### Domain Certificate Settings

Configure fallback certificate behavior at the domain level. These settings are stored in the `domains` table (`certificate_settings` column, CLOB type).

| Property | Description | Example |
|:---------|:------------|:--------|
| `fallbackCertificate` | Certificate ID to use when no specific certificate is configured or when the configured certificate fails to load. Must belong to the same domain. Null or empty value disables fallback. | `"cert-abc-123"` |

### Updating Domain Certificate Settings

Update certificate settings via the REST API without triggering a full domain reload. Send a `PUT` request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` with a JSON body containing `{"fallbackCertificate": "cert-id"}`.

The endpoint validates that the certificate exists and belongs to the domain, returning `400 Invalid Parameter` if validation fails. On success, the gateway publishes a `DOMAIN_CERTIFICATE_SETTINGS` event and returns the updated domain object with a `200 OK` response.

### Restrictions

* Fallback certificate must belong to the same domain as the domain settings (cross-domain certificates are rejected with "Fallback certificate does not belong to this domain")
* Certificates configured as a domain's fallback certificate cannot be deleted (deletion blocked with "You can't delete a certificate that is configured as the domain's fallback certificate")
* If the fallback certificate ID matches the original certificate ID, the gateway skips fallback to prevent infinite loops
* System certificates are now visible in the UI fallback certificate selection dialog

## Overview

Domain certificate settings allow administrators to configure a fallback certificate that the Access Management gateway uses when a client-specific certificate is unavailable or fails to load. This feature prevents authentication failures by providing a secondary certificate for JWT signing and client authentication operations.

{% hint style="info" %}
This feature is intended for API platform administrators managing multi-tenant or high-availability environments.
{% endhint %}
