### System Certificate Visibility

System certificates (built-in certificates provided by the platform) are now visible in certificate selection dialogs, including the fallback certificate selector. This allows administrators to designate system certificates as domain-level fallbacks.

### Prerequisites

Before configuring domain certificate settings, ensure the following:

* Domain must exist and be accessible
* Fallback certificate (if specified) must exist in the certificate repository
* Fallback certificate must belong to the same domain (or be accessible from a master domain)
* User must have `DOMAIN_SETTINGS[UPDATE]` permission to modify certificate settings

### Gateway Configuration

#### Domain Certificate Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `certificateSettings.fallbackCertificate` | The certificate ID to use when no client-specific certificate is configured | `"cert-abc123"` |

### Configure Domain Certificate Settings

To configure a fallback certificate for a domain:

1. Send a PUT request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` with a JSON body:

   ```json
   {
     "fallbackCertificate": "certificate-id"
   }
   ```

2. The system validates that the certificate exists and belongs to the domain before applying the setting.

This operation updates only the certificate settings without triggering a full domain reload, minimizing disruption to active sessions.

#### Remove Fallback Certificate

To remove the fallback certificate, set the `fallbackCertificate` property to `null` or an empty string in the request body. The domain will not use a fallback certificate after this change.

### Certificate Deletion with Fallback Protection

When deleting a certificate, the system checks whether it is configured as a domain's fallback certificate. If the certificate is in use as a fallback, the deletion fails with the error message:

```
You can't delete a certificate that is configured as the domain's fallback certificate.
```

The certificate must first be removed from the domain's certificate settings before it can be deleted. The system also validates that the certificate is not in use by applications, identity providers, or protected resources.

### Restrictions

* Fallback certificate must belong to the same domain as the domain being configured (master domains can access certificates from all domains)
* Certificate settings updates require `DOMAIN_SETTINGS[UPDATE]` permission
* Certificates configured as domain fallbacks cannot be deleted until removed from certificate settings
* Certificate settings validation occurs before the update is persisted
* System certificates are now visible in certificate selection dialogs (previously filtered out)

### Related Changes

The Management API now includes a dedicated endpoint for updating certificate settings (`PUT /certificate-settings`) that avoids full domain reloads. The event system emits `DOMAIN_CERTIFICATE_SETTINGS.UPDATE` events to notify gateway nodes of certificate settings changes without requiring domain synchronization. Certificate deletion validation now includes a check for fallback certificate usage, returning HTTP 400 with `CertificateIsFallbackException` when attempting to delete a certificate configured as a domain fallback.
