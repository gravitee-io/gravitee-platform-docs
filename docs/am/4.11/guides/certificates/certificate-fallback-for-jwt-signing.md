## Overview

The certificate fallback feature provides a resilience mechanism for JWT signing operations in Gravitee Access Management. When a client's primary certificate fails to load or sign a JWT, the system can attempt signing with a domain-level fallback certificate before falling back to the default HMAC certificate or failing completely. This feature is designed for API platform administrators managing multi-tenant environments where certificate availability is critical.

## Key concepts

### Certificate selection hierarchy

AM evaluates certificates in a three-tier priority order:

1. **Client-specific certificate**: The system first attempts to use the client-specific certificate configured in the client settings.
2. **Domain fallback certificate**: If the client certificate is unavailable or signing fails, the system checks for a domain-level fallback certificate.
3. **Default HMAC certificate**: If no fallback is configured or available, the system uses the default HMAC certificate (if `fallbackToHmacSignature` is enabled) or throws a `TemporarilyUnavailableException`.

The system automatically skips the fallback certificate if its ID matches the primary certificate ID. This prevents infinite loops and ensures correct progression through the certificate hierarchy.

### Domain isolation

Certificate access follows domain isolation rules:

- Non-master domains can only access certificates belonging to their own domain ID.
- Master domains have cross-domain access for introspection purposes.
- The fallback certificate must belong to the same domain unless the domain is configured as a master domain.

### Logging and observability

All fallback operations are logged at WARN level with explicit certificate IDs:

- When falling back from primary to fallback certificate:
  `"Failed to sign JWT with certificate: {primary}, attempting fallback using: {fallback}"`
- When falling back to HMAC default:
  `"Certificate: {primary} not loaded, using default certificate as fallback"`

This provides operational visibility into certificate failures and fallback usage patterns, enabling administrators to identify and resolve certificate availability issues proactively.

## Prerequisites

Before configuring certificate fallback, ensure you have:

- A valid certificate deployed in the domain's certificate repository
- `DOMAIN_SETTINGS[UPDATE]` permission on the domain, environment, or organization
- Access Management version supporting the certificate settings API

## Configure fallback certificate

Configure the fallback certificate at the domain level using the certificate settings property.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `fallbackCertificate` | String | null | ID of the certificate to use as fallback when primary certificate fails |

### Configure certificate settings via Management API

Use the Management API to configure certificate settings without triggering a full domain reload.

1. Send a PUT request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`.
2. Include a JSON body with the `fallbackCertificate` property set to a valid certificate ID:

    ```json
    {
      "fallbackCertificate": "<certificate-id>"
    }
    ```

3. The endpoint returns the updated certificate settings object.

**Validation rules:**

- The fallback certificate must exist in the domain's certificate repository
- The fallback certificate must belong to the same domain (unless the domain is a master domain)
- The fallback certificate ID cannot match the primary certificate ID
- Requires `DOMAIN_SETTINGS[UPDATE]` permission

Certificate settings updates use an event-driven mechanism (`DomainCertificateSettingsEvent.UPDATE`) that allows runtime configuration changes without requiring a full domain reload. This improves operational efficiency for dynamic fallback certificate management.

## JWT signing fallback sequence

When signing a JWT, the system follows this process:

1. The system first attempts to use the client's configured certificate.
2. If signing fails, it retrieves the fallback certificate from the domain settings.
3. The system verifies that the fallback certificate ID differs from the primary certificate ID.
4. The system logs a warning message: `"Failed to sign JWT with certificate: {primary}, attempting fallback using: {fallback}"`.
5. The system attempts signing with the fallback certificate.
6. If the fallback certificate is unavailable:
    - When `fallbackToHmacSignature` is enabled, the system uses the default HMAC certificate and logs: `"Certificate: {primary} not loaded, using default certificate as fallback"`.
    - Otherwise, it throws a `TemporarilyUnavailableException`.

### Interaction with fallbackToHmacSignature

The `fallbackToHmacSignature` setting determines system behavior when both the primary and fallback certificates are unavailable:

- **Enabled**: The system uses the default HMAC certificate as a final fallback
- **Disabled**: Authentication fails with `TemporarilyUnavailableException`

## Restrictions

- Fallback certificate must exist in the domain's certificate repository
- Fallback certificate must belong to the same domain (unless domain is master)
- Fallback certificate ID can't match the primary certificate ID
- Requires `DOMAIN_SETTINGS[UPDATE]` permission to modify certificate settings
- If `fallbackToHmacSignature` is disabled and no fallback certificate is available, authentication fails with `TemporarilyUnavailableException`

## Related changes

The Management API now includes a dedicated PUT endpoint for certificate settings at `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`.

The UI certificate settings dialog has been updated to include system certificates in the selection list, which were previously filtered out.

The feature introduces three new permission types for finer-grained access control:

- `PROTECTED_RESOURCE_SETTINGS`
- `PROTECTED_RESOURCE_OAUTH`
- `PROTECTED_RESOURCE_CERTIFICATE`

These replace the generic `PROTECTED_RESOURCE[ACTION]` permissions and enable more precise authorization policies for protected resource management.

