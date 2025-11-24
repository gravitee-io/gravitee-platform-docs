---
description: An overview about mtls plans overview.
---

# mTLS plans overview

The mTLS authentication type enforces the use of a client certificate to connect to an API. The client certificate is added to an application, and then a subscription is created for that application. At runtime, the gateway checks that an incoming request contains a client certificate matching one associated with an application that has an active subscription.

You can use the mTLS with or without TLS enabled between the client and the gateway. The gateway server can require client authentication, which uses the truststore at the server level to determine which clients to trust. The mTLS plan checks the client certificate with the gateway-level TLS. The client certificate is either found in either of the following locations:

* The TLS session between the client and the gateway
* In a pre-specified header in plaintext, base64-encoded.

This can be done if a load balancer is placed in front of the gateway that terminates TLS. For more information about the configuration, See configuration.

## Limitations

mTLS plans have the following limitations:

* You can apply mTLS plans to only v4 APIs.
* You cannot use mTLS plans in Gravitee Cloud.
* Only one client certificate can be added per application. This means that to rotate certificates for an application, you need to pause the application’s subscriptions or schedule a maintenance window to avoid traffic for that API.
* Applications do not provide a warning that certificates are going to expire.

\\
