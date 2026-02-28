### Overview

The certificate fallback mechanism provides resilience for JWT signing operations when primary certificates fail or become unavailable. Administrators can configure a domain-level fallback certificate that the gateway attempts before resorting to the default HMAC certificate or failing the request. This feature improves service availability and provides transparent failover with structured logging for troubleshooting.

### Key concepts

#### Certificate selection hierarchy

The gateway evaluates certificates in priority order when signing JWTs. First, it attempts the client-specific certificate if configured. If unavailable, it tries the domain-level fallback certificate. If that also fails and HMAC fallback is enabled, it uses the default HMAC certificate. If no valid certificate is available after all attempts, the gateway throws a `TemporarilyUnavailableException`.

| Priority | Certificate Source | Condition |
|:---------|:-------------------|:----------|
| 1 | Client-specific certificate | `client.getCertificate()` is set and loaded |
| 2 | Fallback certificate | Configured in domain certificate settings |
| 3 | Default HMAC certificate | `fallbackToHmacSignature = true` |
| 4 | Error | None available → `TemporarilyUnavailableException` |

#### Certificate scope

Certificate access depends on domain type. Master domains can access all certificates across the organization (cross-domain introspection). Regular domains can only access certificates that belong to that specific domain. This scoping ensures proper isolation while allowing master domains to manage certificates centrally.

#### Fallback logging

When the gateway uses a fallback certificate, it emits structured warning logs identifying both the failed primary certificate and the fallback certificate used. This transparency aids operators in diagnosing certificate issues and understanding when failover occurs. Logs appear at the WARN level with certificate IDs clearly identified.

### Prerequisites

- Access Management gateway version supporting certificate settings API
- `DOMAIN_SETTINGS[UPDATE]` permission on the target domain, environment, or organization
- At least one valid certificate uploaded to the domain or organization
- Understanding of JWT signing requirements for your authentication flows

### Gateway configuration

#### Domain certificate settings

Configure the fallback certificate at the domain level using the certificate settings property. This configuration doesn't trigger a full domain reload, making it a lightweight runtime operation.

| Property | Type | Default | Description |
|:---------|:-----|:--------|:------------|
| `fallbackCertificate` | String | null | Certificate ID to use when primary certificate fails or is unavailable |

**Configuration Path:** Domain → Certificate Settings → Fallback Certificate

**Example Value:** `"550e8400-e29b-41d4-a716-446655440000"`

### Configuring certificate fallback

To configure a fallback certificate:

1. Identify the certificate ID from your certificate inventory (available in the Management Console or via the certificates API).

2. Update the domain's certificate settings:

    ```
    PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
    ```

    Request body:

    ```json
    {
      "fallbackCertificate": "your-certificate-id"
    }
    ```

3. The API returns the updated settings in the response. The gateway applies the change immediately without restarting the domain.

4. Verify the configuration by checking the domain's certificate settings or by triggering a JWT signing operation with an unavailable primary certificate and observing the fallback behavior in logs.

### Architecture notes

#### Event-driven configuration updates

Certificate settings changes propagate to gateway nodes via `DomainCertificateSettingsEvent`. This event-driven approach ensures all gateway instances receive configuration updates without requiring manual synchronization or domain reloads. The lightweight update mechanism reduces operational overhead compared to full domain configuration changes.

#### Fallback loop prevention

The gateway prevents infinite loops by filtering out fallback certificates that match the failed primary certificate. When a signing attempt fails, the system retrieves the fallback certificate and compares its ID to the failed certificate's ID. If they match, the fallback is skipped and the original error is returned. This safeguard ensures the system fails fast rather than retrying with the same certificate.

#### JWT signing flow

The JWT signing process attempts the primary certificate first. On failure, it retrieves the fallback certificate provider and filters out any fallback matching the failed certificate. If a valid fallback exists, the gateway logs a warning identifying both certificates and attempts signing with the fallback.
