---
description: An overview about mtls.
---

# mTLS

## Overview

The mTLS authentication type enforces the use of a client certificate to connect to an API. The client certificate is added to an application, and then a subscription is created for that application. At runtime, the gateway checks that an incoming request contains a client certificate matching one associated with an application that has an active subscription.

You can use the mTLS with or without TLS enabled between the client and the gateway. The gateway server can require client authentication, which uses the truststore at the server level to determine which clients to trust. The mTLS plan checks the client certificate with the gateway-level TLS. The client certificate is either found in either of the following locations:

* The TLS session between the client and the gateway
* In a pre-specified header in plaintext, base64-encoded.

This can be done if a load balancer is placed in front of the gateway that terminates TLS. For more information about the configuration, See configuration.

## Limitations

Currently, mTLS plans have the following limitations:

* You can apply mTLS plans to only v4 APIs.
* You cannot use mTLS plans in Gravitee Cloud with SaaS-based Gateways.
* Only one client certificate can be added per application. This means that to rotate certificates for an application, you need to pause the application’s subscriptions or schedule a maintenance window to avoid traffic for that API.
* Applications do not provide a warning that certificates are going to expire.

## How to add a client certificate

To subscribe to an mTLS plan, the client must add a certificate to their application. To add a certification to an application, complete the following steps:

1. In the console, navigate to **Applications**, and then click a specific application.
2. For that application, click the setting the Tls Configuration. The client certificate is pasted in base64-encoded format.

<figure><img src="https://lh7-qw.googleusercontent.com/docsz/AD_4nXc_4L_O2a7U3HCPit9I74v_II5gn7pS-l6uyix2fScJPMusOebtUTmmvHnjL5pVZwOIcKmiRxNOi8uZeumcZTNQzk7VzHhW7tdWZnWNMghyROnJlpbRfXfTkUypSZGmJ2iSejROejRLglgdC-feoXpL5C3G?key=PrMp2J0zWBtqrsqO75zcMw" alt="Screenshot showing Tls configuration"><figcaption><p>Screenshot showing Tls configuration</p></figcaption></figure>

{% hint style="warning" %}
Multiple applications in the same APIM instance must **not** share client certificates. You cannot save an application’s configuration if the added client certificate is already present for another application.
{% endhint %}

When you add a client certificate to an application, the gateway adds this application to its truststore. At runtime, the gateway checks whether the truststore has a certificate that matches an application with a valid subscription for the API.

## How to call an API

To call an API with mTLS, you must have the client certificate and the private key, and your client trusts the certificate sent by the gateway.

Use the following command, replacing `<client.cer>` and `<client.key>` with the name of the files where you have stored your client certificate and the file where you have stored the client key.

```bash
$ curl –-cert  <client.cer> --key <client.key> https://my-gateway.com/mtls-api
```

## How to terminate TLS

{% hint style="danger" %}
From Gravitee APIM 4.5 onwards, when the certificates have been processed by NGINX, API Management only supports extracting client certificates from headers in plaintext.
{% endhint %}

To run a load balancer in front of the gateway like NGINX, and then terminate TLS at the load balancer. The load balancer forwards traffic to the gateway in plaintext. To use the mTLS plan in this situation, you can set a gateway configuration. For example:

```bash
http:
  # ...
  ssl:
    clientAuthHeader:
      name: X-Gravitee-Client-Cert
```

When executing an mTLS plan, the gateway checks if TLS is enabled. If it is enabled, the gateway uses the certificate from the TLS handshake , which occurs before plan selection. If TLS is not enabled, it checks for the certificate in the header. If the header contains a valid base64-encoded plaintext certificate matching a certificate for a subscribed application, the request will succeed.

Ensure that when you use this option that only trusted parties can set this header. If using a load balancer, it must be solely responsible for setting this header. In this setup, the gateway should only be directly accessible through the load balancer.
