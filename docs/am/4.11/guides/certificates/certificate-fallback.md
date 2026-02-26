## Certificate fallback mechanism

Certificate fallback provides resilience for JWT signing operations when a client's primary certificate becomes unavailable. When configured, the system automatically uses a domain-level fallback certificate if the primary certificate fails, preventing service disruptions.

### Certificate resolution chain

When a client requests JWT signing, the system follows this deterministic fallback sequence:

1. If the client has no configured certificate, the default certificate is used immediately
2. Otherwise, the system attempts the primary certificate
3. If the primary certificate fails, the system attempts the configured fallback certificate (if set)
4. If the fallback certificate fails, the system attempts the default certificate (only if HMAC fallback is enabled)
5. If all attempts fail, the system throws a `TemporarilyUnavailableException`

This chain ensures maximum availability while maintaining security boundaries.

### Domain-scoped certificate access

Certificate access follows domain-scoping rules:

- Regular domains can only access certificates within their own domain boundary
- Master domains have elevated privileges and can access certificates from any domain, enabling cross-domain introspection scenarios

The system enforces this scoping rule during certificate resolution to prevent unauthorized certificate usage.

### Fallback exclusion logic

The fallback mechanism includes protection against infinite loops. When attempting fallback, the system filters out any fallback certificate whose ID matches the primary certificate ID. This prevents the system from retrying the same failed certificate and ensures genuine fallback behavior.

The mutual exclusion filter compares certificate IDs before attempting fallback:

```java
!Objects.equals(fallback.getCertificateInfo().certificateId(), certificateProvider.getCertificateInfo().certificateId())
```

This ensures fallback only occurs when a genuinely different certificate is available.

## Prerequisites

- Gravitee Access Management instance with domain configured
- At least one valid certificate uploaded to the domain or system
- `DOMAIN_SETTINGS[UPDATE]` permission at domain, environment, or organization level
- Understanding of JWT signing requirements for your clients

## Configure certificate fallback

Configure fallback behavior at the domain level using the certificate settings endpoint. This configuration persists independently of the domain object and doesn't trigger a full domain reload when updated.

### Domain certificate settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `fallbackCertificate` | ID of the certificate to use when primary certificate fails | `"cert-abc-123"` |

**REST Endpoint**: `PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings`

**Request Body**:
```json
{
  "fallbackCertificate": "cert-abc-123"
}
```

### Configure fallback in Management Console

1. Navigate to your domain's certificate settings in the Management Console
2. Select a fallback certificate from the available certificates (system certificates are included in the selection list)
3. Submit the configuration change

The system applies the configuration immediately without restarting the domain. Monitor your logs for fallback usage messages to verify the configuration is working as expected.

### Event-driven configuration updates

Certificate settings changes propagate through the system via `DomainCertificateSettingsEvent`. This event type enables non-disruptive configuration updates. The gateway reacts to certificate settings changes without requiring a full domain reload.

## Create a client with certificate fallback

When creating or updating a client application:

1. Assign a primary certificate through the client configuration
2. If that certificate becomes unavailable (deleted, expired, or corrupted), the system automatically attempts the domain-level fallback certificate
3. The client continues to receive signed JWTs without interruption

Your logs will show which certificate was used for each signing operation.

## Monitor fallback events

The system logs detailed information when fallback occurs, enabling proactive monitoring and troubleshooting.

## TemporarilyUnavailableException on certificate fallback failure

The system throws a `TemporarilyUnavailableException` when all certificate fallback attempts fail during JWT signing operations. This exception occurs under the following conditions:

- The client's primary certificate fails (unavailable, expired, or corrupted)
- No fallback certificate is configured at the domain level, **or** the configured fallback certificate also fails
- HMAC fallback is disabled

When this exception is thrown, the JWT signing operation cannot proceed, and the client request fails. To prevent this scenario, ensure that:

1. A valid fallback certificate is configured in the domain certificate settings
2. The fallback certificate differs from the primary certificate
3. HMAC fallback is enabled (if appropriate for your security requirements)

Monitor your logs for `TemporarilyUnavailableException` events to identify certificate availability issues before they impact production traffic.

{% hint style="warning" %}
If HMAC fallback is disabled and no valid fallback certificate is available, certificate failures result in immediate service disruption for affected clients.
{% endhint %}

## Restrictions

- Fallback certificate must exist within the same domain or be a system certificate accessible to the domain.
- Fallback certificate ID must differ from the primary certificate ID to trigger fallback.
- Master domain privilege for cross-domain certificate access is limited to master domain type only.
- Certificate settings updates require `DOMAIN_SETTINGS[UPDATE]` permission.
- If HMAC fallback is disabled and no fallback certificate is configured, certificate failure results in `TemporarilyUnavailableException`.
- System does not validate certificate expiration or revocation status during fallback selection.

## API and permission changes

The Management Console certificate selection dialog now includes system certificates in the dropdown list. Three new permission types were added:

- `PROTECTED_RESOURCE_SETTINGS`
- `PROTECTED_RESOURCE_OAUTH`
- `PROTECTED_RESOURCE_CERTIFICATE`

The REST API schema was extended with the `CertificateSettings` model and the dedicated certificate settings endpoint. All changes maintain backward compatibility with existing domain configurations.
