## Overview
This guide explains how to configure a fallback certificate for your domain using the Access Management (AM) or the Management API.


## Configure a domain certificate fallback

To configure the domain certificate fallback, complete the following stpes:
1. [Enable HMAC signature](#enable-hmac-signature)
2. [Configure the Domain Ceritifcate Settings](#configure-the-domain-ceritifcate-settings)

### Enable HMAC signature
To enable HMAC signature in your `gravitee.yaml` file, navigate to the `applications` section, and then add the following configuration: 
```yaml
applications:
  signing:
    fallback-to-hmac-signature: true|false
```

## Configure the Domain Ceritifcate Settings
You can create Domain Certicate Settings with either of the following methods:
* [Create Domain Certificate Settings using the Access Management UI](#create-domain-certificate-settings-using-the-access-management-ui)
* [Create Domain Certificate Settings using the Management API](#create-domain-certificate-settings-using-the-management-api)

### Create the Domain Cerificate Settings using the Access Management UI
1. Create a certificate. For more information about creating a certificate, see [Certificates](/docs/am/4.11/guides/certificates/README.md).
2. From the Access Management (AM) dashboard, click **Settings**.
  <figure><img src="/.gitbook/assets/Fallback_certificate_dashboard.jpg" alt="Access Management dashboard"><figcaption></figcaption></figure>
3. In the **Settings menu**, navigate to the **Security** section, and then click **Certificates**.
  <figure><img src="/.gitbook/assets/Fallback_certificate_settings_menu.jpg" alt="Access Management setting's menu"><figcaption></figcaption></figure>
4. In the **Certificates** screen, click **Settings**. The **Certificate Settings** pop-up window appears.
  <figure><img src="/.gitbook/assets/Fallback_certificate_certificates_screen.jpg" alt=" Access Management certficiates screen"><figcaption></figcaption></figure>
5. From the **Fallback Certificate** dropdown menu, select the certificate you want to use. 
  <figure><img src="/.gitbook/assets/Fallback_certificate_certificates_settings_popup_menu.jpg" alt=" Access Management certficiates screen"><figcaption></figcaption></figure>

#### Verification
The certificate appears in the **Cerificates** screen of the Access Management UI.
<figure><img src="/.gitbook/assets/Fallback_certificate_certificates_screen_verification.jpg" alt=" Access Management certficiates screen"><figcaption></figcaption></figure>

### Create the Domain Certificate Settings using the Management API

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