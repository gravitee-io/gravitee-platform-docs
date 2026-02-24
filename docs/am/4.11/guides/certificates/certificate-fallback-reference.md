## Overview

Access Management 4.11 introduces a certificate fallback mechanism for JWT signing operations. When the primary certificate configured for a client fails to load, the gateway automatically attempts to use a domain-level fallback certificate. This feature improves resilience during certificate rotation, expiration, or misconfiguration scenarios.

The fallback mechanism operates transparently—clients continue to receive signed JWTs without interruption, and fallback usage is logged for operational visibility. If both primary and fallback certificates fail and HMAC fallback is disabled, the client receives a `temporarily_unavailable` OAuth error.

## Prerequisites

Before configuring certificate fallback:

- You must have `DOMAIN_SETTINGS[UPDATE]` permission at domain, environment, or organization level
- The fallback certificate must exist in the same domain as the client (unless the domain is a master domain)
- The fallback certificate must be different from the primary certificate

## Configuration

### Configuring the Fallback Certificate

Configure the domain-level fallback certificate through the Management API:

{% code overflow="wrap" %}
```bash
curl -X PUT https://am-management-api/management/organizations/{orgId}/environments/{envId}/domains/{domainId}/certificate-settings \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "fallbackCertificate": "{certificateId}"
  }'
```
{% endcode %}

The certificate settings endpoint updates domain configuration without triggering full domain reloads. Changes propagate to all gateway nodes via the event system.

To disable fallback after configuration, send the certificate settings update request with `"fallbackCertificate": null`.

### Creating a Client with Fallback Protection

When creating or updating a client that requires JWT signing, configure the primary certificate through the client configuration. The fallback mechanism activates automatically when the primary certificate fails to load—no client-side configuration is required. The client continues to receive signed JWTs transparently, with fallback usage logged on the gateway for operational visibility.

## Architecture

### Event-Driven Configuration Updates

Certificate settings changes propagate through the `DomainCertificateSettingsEvent` system, which uses an event manager subscription model. Each gateway node maintains an `AtomicReference<CertificateSettings>` that updates atomically when events arrive, ensuring thread-safe configuration changes without locks or domain restarts. This architecture supports high-availability deployments where configuration changes must propagate instantly across multiple gateway instances.

### JWT Signing Fallback Flow

The JWT signing process uses reactive error handling to attempt fallback only when the primary signing operation fails (not when the certificate loads successfully but signing fails for other reasons). The system filters out fallback attempts where the fallback certificate ID matches the primary ID, logs the fallback usage with both certificate IDs for troubleshooting, and propagates the original error if no valid fallback exists. This design ensures that transient signing errors don't mask underlying certificate configuration problems.

### Gateway Logging

Gateway logs emit structured warnings with certificate IDs when fallback activation occurs:

```
Certificate: {id} not loaded, using: {fallbackId} as fallback
```

This log format improves operational observability during certificate failures.

## Restrictions

The certificate fallback feature has the following restrictions:

- **Domain scope**: Fallback certificate must belong to the same domain as the client (unless the domain is a master domain)
- **Mutual exclusion**: Fallback certificate can't be the same as the primary certificate
- **Permissions**: Certificate settings updates require `DOMAIN_SETTINGS[UPDATE]` permission at domain, environment, or organization level
- **Trigger conditions**: Fallback only triggers on certificate load failure, not on JWT signing errors with a successfully loaded certificate
- **HMAC fallback**: Default HMAC fallback requires `fallbackToHmacSignature = true` in domain configuration

## Related Changes

The certificate fallback feature introduces several system-wide changes:

### Management API Changes

- **Dedicated certificate settings endpoint**: Updates domain configuration without triggering full domain reloads
- **Configuration propagation**: Changes propagate to all gateway nodes via the event system

### Permission Model Changes

Three new permission types were added to support fine-grained access control for protected resource management:

- `PROTECTED_RESOURCE_SETTINGS`
- `PROTECTED_RESOURCE_OAUTH`
- `PROTECTED_RESOURCE_CERTIFICATE`

### UI Changes

The certificate selector now displays system certificates alongside user-created certificates to support fallback configuration (previously filtered out).