
### Prerequisites

Before configuring a fallback certificate for a domain, ensure the following:

* Security domain exists
* Fallback certificate (if specified) exists and belongs to the same domain
* User has `DOMAIN_SETTINGS[UPDATE]` permission

### Gateway Configuration

#### Enable HMAC signature
To enable HMAC signature in your `gravitee.yaml` file, navigate to the `applications` section, and then add the following configuration: 
```yaml
applications:
  signing:
    fallback-to-hmac-signature: true|false
```


## Create Domain Ceritifcate Settings
You can create Domain Certicate Settings with either of the following methods:
* [Create Domain Certificate Settings using the Access Management UI](#create-domain-certificate-settings-using-the-access-management-ui)
* [Create Domain Certificate Settings using the Management API](#create-domain-certificate-settings-using-the-management-api)

### Create Domain Cerificate Settings using the Access Management UI
### Create Domain Certificate Settings using the Management API

To configure a fallback certificate for a domai using the Management API, complete the following steps:

1. Send a PUT request to `/organizations/{organizationId}/environments/{environmentId}/domains/{domain}/certificate-settings` with a JSON body containing the `fallbackCertificate` property set to the desired certificate ID.
2. The system validates that the certificate exists and belongs to the domain.
3. If validation passes, the certificate settings are stored and a `DOMAIN_CERTIFICATE_SETTINGS.UPDATE` event is published to notify gateway nodes.
4. Gateway nodes update their certificate resolution logic without requiring a full domain restart.

**Example request body:**

```json
{
  "fallbackCertificate": "fallback-cert-123"
}
```

### Restrictions

* Fallback certificate must belong to the same domain (master domains can access certificates from all domains)
* Certificates configured as domain fallback cannot be deleted (returns `CertificateIsFallbackException` with HTTP 400)
* Certificates in use by applications, identity providers, or protected resources cannot be deleted
* Certificate settings validation occurs before persistence
 