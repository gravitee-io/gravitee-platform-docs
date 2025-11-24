---
description: Configuration and usage guide for terminating tls in front of the gateway.
---

# Terminating TLS in front of the Gateway

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

\
Ensure that when you use this option that only trusted parties can set this header. If using a load balancer, it must be solely responsible for setting this header. In this setup, the gateway should only be directly accessible through the load balancer.
