### Certificate fallback hierarchy

When a client certificate is requested, AM follows this fallback chain:

1. The client's configured certificate
2. The domain's fallback certificate (if configured)
3. The domain's default HMAC certificate (only if `fallbackToHmacSignature = true`)
4. `TemporarilyUnavailableException` if all options are exhausted

This hierarchy provides graceful degradation and prevents immediate failures during certificate issues.

### Master domain privilege

Master domains can access certificates from any domain for cross-domain introspection scenarios. Regular domains can only access certificates belonging to their own domain. This distinction is enforced by the `belongsToCurrentDomain()` validation rule.

### Event-driven updates

Certificate settings updates use a dedicated event type (`DOMAIN_CERTIFICATE_SETTINGS`) and listener, allowing real-time updates without requiring a full domain reload. The system uses `AtomicReference<CertificateSettings>` for thread-safe state management.

### Prerequisites

Before configuring certificate fallback:

- Obtain valid certificate IDs for both primary and fallback certificates
- Verify `DOMAIN_SETTINGS[UPDATE]` permission on domain, environment, or organization level
- Confirm the fallback certificate is loaded and available in the domain

### Configure certificate fallback

To configure a fallback certificate:

1. Send a PUT request to the certificate settings endpoint:

    ```http
    PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
    ```

2. Include the fallback certificate ID in the request body:

    ```json
    {
      "fallbackCertificate": "backup-cert-id"
    }
    ```

3. The system updates only certificate settings without triggering a full domain reload.
4. The response returns the updated domain object with certificate settings.

### Automatic fallback behavior

When a client application is configured with a certificate, AM automatically applies the fallback logic during JWT signing and certificate provider resolution:

1. If the primary certificate fails, AM logs a warning:

    ```
    Certificate: {clientCert} not loaded, using: {fallbackId} as fallback
    ```

2. AM attempts to use the fallback certificate.
3. If the fallback also fails and `fallbackToHmacSignature = true`, AM falls back to the default HMAC certificate with another warning log.
4. If all attempts fail, AM throws a `TemporarilyUnavailableException`.

### Restrictions

- Fallback certificate must belong to the same domain (except for master domains, which can access certificates from any domain)
- Certificate settings updates require `DOMAIN_SETTINGS[UPDATE]` permission
- System certificates are now selectable as fallback certificates in the UI (previously filtered out)
- If `fallbackToHmacSignature = false`, AM throws an exception if both primary and fallback certificates fail
- Certificate loading failures trigger warning logs but don't prevent fallback attempts

### Architecture notes

#### Atomic state management

AM uses `AtomicReference<CertificateSettings>` to ensure thread-safe updates to certificate settings. When the domain repository fetches an updated domain, the certificate settings reference is updated atomically without requiring a domain restart.

#### JWT signing fallback

The `JWTServiceImpl` implements fallback logic for JWT encoding. When signing fails with the primary certificate, the service attempts to use the fallback certificate (if different from the original). If the fallback also fails or is the same as the original, the error is propagated. A warning is logged whenever the fallback is used.

### Related changes

The Management API now includes a dedicated endpoint for updating certificate settings independently of full domain updates. The UI certificate selection filter was updated to include system certificates, aligning with backend capabilities. New permission types were added for protected resource settings (`PROTECTED_RESOURCE_SETTINGS`, `PROTECTED_RESOURCE_OAUTH`, `PROTECTED_RESOURCE_CERTIFICATE`), and existing permission descriptions were updated to use more granular permission names (e.g., `PROTECTED_RESOURCE_MEMBER[READ]` instead of `PROTECTED_RESOURCE[READ]`).

