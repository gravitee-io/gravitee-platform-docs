---
description: >-
  Configuration and usage guide for adding a client certificate to an
  application.
---

# Adding a Client Certificate to an Application

To subscribe to an mTLS plan, the client must add a certificate to their application. To add a certification to an application, complete the following steps:

1. In the console, navigate to **Applications**, and then click a specific application.
2. For that application, click the setting the Tls Configuration. The client certificate is pasted in base64-encoded format.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXc_4L_O2a7U3HCPit9I74v_II5gn7pS-l6uyix2fScJPMusOebtUTmmvHnjL5pVZwOIcKmiRxNOi8uZeumcZTNQzk7VzHhW7tdWZnWNMghyROnJlpbRfXfTkUypSZGmJ2iSejROejRLglgdC-feoXpL5C3G?key=PrMp2J0zWBtqrsqO75zcMw" alt="Screenshot showing Tls configuration"><figcaption><p>Screenshot showing Tls configuration</p></figcaption></figure>

{% hint style="warning" %}
Multiple applications in the same APIM instance must **not** share client certificates. You cannot save an application’s configuration if the added client certificate is already present for another application.
{% endhint %}

When you add a client certificate to an application, the gateway adds this application to its truststore. At runtime, the gateway checks whether the truststore has a certificate that matches an application with a valid subscription for the API.
