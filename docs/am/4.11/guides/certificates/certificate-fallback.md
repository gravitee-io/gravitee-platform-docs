## Certificate fallback for JWT signing

Access Manager supports automatic failover to a backup certificate when the primary certificate fails during JWT signing operations. Configure a domain-level fallback certificate to improve service resilience without manual intervention.

### How certificate fallback works

When signing a JWT, AM follows this sequence:

1. Attempts to use the client's configured certificate
2. On failure, retrieves the domain's fallback certificate
3. Filters out the fallback if its ID matches the primary certificate
4. Logs a warning with both certificate IDs
5. Attempts to sign with the fallback certificate
6. If no fallback exists or the fallback fails, attempts the default certificate when `fallbackToHmacSignature=true`
7. If all certificates fail, throws `TemporarilyUnavailableException` with message "The certificate cannot be loaded"

This flow is implemented in `JWTServiceImpl.encodeJwtWithFallback()`.

Master domains can access certificates from any domain in the system. Regular domains are restricted to certificates within their own domain scope. This access control is enforced in `CertificateManagerImpl.belongsToCurrentDomain()`.

{% hint style="info" %}
**Master Domain Certificate Access**

Master domains have special privileges that allow them to access certificates from any domain for fallback purposes. This enables cross-domain introspection scenarios and centralized certificate management across the entire system.
{% endhint %}

### Prerequisites

* Domain administrator access with `DOMAIN_SETTINGS[UPDATE]` permission
* At least one valid certificate configured in the domain (or accessible from master domain)
* Gateway version supporting certificate settings management

### Configure certificate fallback

Update the domain's certificate settings using the Management API:

```http
PUT /organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings
```

**Request body:**

```json
{
  "fallbackCertificate": "backup-cert-id"
}
```

**Required permission:**

`DOMAIN_SETTINGS[UPDATE]` at domain, environment, or organization level

**Response:**

The endpoint returns the updated domain object on success (200 OK). Changes take effect immediately without reloading the domain.

**Example:**

```bash
curl -X PUT \
  https://am-gateway.example.com/management/organizations/org-123/environments/env-456/domains/my-domain/certificate-settings \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"fallbackCertificate": "backup-cert-2024"}'
```

{% hint style="info" %}
Certificate settings updates trigger a `DomainCertificateSettingsEvent` rather than a full domain reload, allowing configuration changes to propagate to all gateway nodes without service disruption.
{% endhint %}

### Certificate settings properties

| Property | Description | Example |
|:---------|:------------|:--------|
| `certificateSettings.fallbackCertificate` | ID of the certificate to use when the primary certificate fails | `"backup-cert-2024"` |

The fallback certificate must exist in the certificate manager and belong to the current domain (unless the domain is a master domain).

### Configuration requirements

The fallback certificate must meet these requirements:

* **Certificate existence**: The certificate must exist in the certificate manager before configuration
* **Domain scope**: The certificate must belong to the same domain (master domains can access certificates from any domain)
* **Unique ID**: The fallback certificate can't have the same ID as the primary certificate (system skips fallback if IDs match)
* **Permission requirements**: Certificate settings updates require `DOMAIN_SETTINGS[UPDATE]` permission at domain, environment, or organization level

### Logging

All fallback attempts generate warning-level log entries containing both certificate IDs:

* `Certificate: {clientCertId} not loaded, using: {fallbackCertId} as fallback` — when the primary certificate fails to load
* `Failed to sign JWT with certificate: {primaryCertId}, attempting fallback using: {fallbackCertId}` — when JWT signing fails

These logs provide audit trails for troubleshooting certificate issues.

### Troubleshooting certificate fallback

When diagnosing certificate issues in JWT signing operations, monitor gateway logs for the following patterns:

#### Primary certificate load failure

```
Certificate: {clientCertId} not loaded, using: {fallbackCertId} as fallback
```

This warning indicates the primary certificate failed to load from the certificate manager. The system automatically attempts to use the configured fallback certificate.

#### JWT signing failure with fallback attempt

```
Failed to sign JWT with certificate: {primaryCertId}, attempting fallback using: {fallbackCertId}
```

This warning indicates the primary certificate loaded successfully but failed during the JWT signing operation. The system attempts to sign with the fallback certificate.

#### Complete certificate failure

If all certificates fail (primary, fallback, and default), the system throws a `TemporarilyUnavailableException` with the message:

```
The certificate cannot be loaded
```

This error indicates no valid certificates are available for JWT signing. Verify that:

* The primary certificate exists in the certificate manager
* The fallback certificate is configured and accessible
* Certificate files are readable and not corrupted
* The domain has appropriate access permissions to the certificates

### Related API and permission changes

The Management API includes a dedicated endpoint for updating certificate settings without triggering full domain reloads. Permission scopes for protected resource operations have been refined:

* **Secret management**: Operations now require `PROTECTED_RESOURCE_OAUTH[*]` permissions instead of generic `PROTECTED_RESOURCE[*]` permissions
* **Member listing**: Requires `PROTECTED_RESOURCE_MEMBER[READ]` permission

Three new permission types were added to support granular access control:

* `PROTECTED_RESOURCE_SETTINGS`
* `PROTECTED_RESOURCE_OAUTH`
* `PROTECTED_RESOURCE_CERTIFICATE`

The UI certificate settings dialog now includes system certificates in the fallback selection list.

