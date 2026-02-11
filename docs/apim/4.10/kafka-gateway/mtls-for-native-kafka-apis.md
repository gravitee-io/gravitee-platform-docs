---
description: >-
  Learn how to configure Kafka clients to connect to Kafka APIs secured with
  mTLS plans in Gravitee APIM
---

# Configure Kafka Client for mTLS
## Configure Kafka Client for mTLS

To connect to a Kafka API with an mTLS plan, configure the Kafka client to use SSL with a client keystore and truststore.

### Client configuration properties

Add the following properties to your Kafka client configuration:

```properties
security.protocol=SSL

ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS

ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```

### Required files

The Kafka client requires:

- **Client keystore**: Contains the client private key and certificate used to authenticate with the Gateway
- **Client truststore**: Contains the CA that signed the Gateway certificate

The client certificate in the keystore must match the certificate associated with your application subscription in APIM.

<!-- GAP: No explicit mention of certificate format requirements (e.g., PEM vs DER) or whether self-signed certificates are supported -->
<!-- GAP: No explicit mention of supported keystore/truststore types beyond JKS (e.g., PKCS12, PEM) for client configuration -->

### Connection behavior

When the client connects:

1. The client initiates a TLS connection and presents its client certificate.
2. The Gateway validates the certificate against known subscription certificates.
3. On match, the connection is authorized and the context is populated with plan, application, and subscription information.
4. Metrics and analytics reflect the resolved subscription.

If the client certificate doesn't match a valid subscription, the Gateway rejects the connection.
## mTLS for Native Kafka APIs Overview

mTLS (mutual TLS) for native Kafka APIs strengthens security by adding mutual authentication on top of the TLS already required for native Kafka APIs. With mTLS enabled, both the Kafka client and the Gateway must present valid certificates to establish a connection.

### TLS vs. mTLS

**TLS only (default for native Kafka APIs)**

- The client verifies the Gateway identity.
- The Gateway does not verify the client identity.

**TLS + mTLS**

- Both the client and the Gateway must present valid certificates.
- The Kafka client must prove its identity using a client certificate.
- The Gateway validates the client certificate against known subscription certificates.

mTLS is an additional security layer on top of TLS. It allows the Gateway to identify Kafka clients by certificate and capture metrics with correct subscription, application, and plan dimensions.

### How mTLS Works for Native Kafka APIs

The mTLS behavior for native Kafka APIs works the same way as for HTTP and Message APIs.

**Subscription flow**

1. An application subscribes to an mTLS plan on a Kafka API.
2. The application provides a PEM client certificate.
3. The certificate is associated with the subscription.

**Runtime flow**

1. The client initiates a TLS connection with a client certificate.
2. The Gateway validates the certificate against known subscription certificates.
3. On match, the connection is authorized and the context is populated with plan, application, and subscription information.
4. Metrics and analytics reflect the resolved subscription.

### Plan Restrictions

Kafka APIs can't have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together.

You can't expose simultaneously:

- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)
## Overview

mTLS (mutual TLS) for native Kafka APIs adds an additional security layer on top of the TLS already required for native Kafka APIs. With mTLS enabled, both the Gateway and the Kafka client must present valid certificates during the connection handshake.

### TLS vs. mTLS

**TLS only (default)**:
- The client verifies the Gateway identity.
- The Gateway does not verify the client identity.

**TLS + mTLS**:
- Both the client and the Gateway must present valid certificates.
- The Kafka client must prove its identity using a client certificate.
- The Gateway validates the client certificate against known subscription certificates.

### Why mTLS for Kafka APIs

mTLS plans allow the Gateway to:
- Identify Kafka clients by certificate
- Resolve subscriptions based on client certificates
- Capture metrics with correct subscription, application, and plan dimensions

Without mTLS, Kafka APIs configured as Keyless cannot resolve subscriptions. This results in metrics showing `ANONYMOUS` instead of the actual application and plan details.

### Subscription Resolution

When a Kafka client connects with a valid certificate:
1. The Gateway validates the certificate against known subscription certificates.
2. On match, the connection is authorized and the context is populated with plan, application, and subscription details.
3. Metrics and analytics reflect the resolved subscription.

This behavior is identical to mTLS plans for HTTP and Message APIs.

### Plan Restrictions

Kafka APIs cannot have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together. You cannot expose simultaneously:
- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)
## Overview

mTLS (mutual TLS) for native Kafka APIs adds an additional security layer on top of the TLS already required for native Kafka APIs. With mTLS enabled, both the Kafka client and the Gateway must present valid certificates during the connection handshake.

### TLS vs. mTLS

**TLS only (default)**

- The client verifies the Gateway identity.
- The Gateway doesn't verify the client identity.

**TLS + mTLS**

- Both the client and the Gateway must present valid certificates.
- The Kafka client must prove its identity using a client certificate.
- The Gateway validates the client certificate against known subscription certificates.

### Why mTLS for Kafka APIs

mTLS plans allow the Gateway to:

- Identify Kafka clients by certificate
- Resolve subscriptions based on client certificates
- Capture metrics with correct subscription, application, and plan dimensions

Without mTLS, Kafka APIs configured as Keyless can't resolve subscriptions. This results in metrics showing `ANONYMOUS` instead of the actual application and plan details.

### Subscription Resolution

When a Kafka client connects with a valid certificate:

1. The client initiates a TLS connection with a client certificate.
2. The Gateway validates the certificate against known subscription certificates.
3. On match, the connection is authorized and the context is populated with plan, application, and subscription details.
4. Metrics and analytics reflect the resolved subscription.

This behavior is identical to mTLS plans for HTTP and Message APIs.

### Benefits

- **Strong authentication**: Kafka clients are authenticated using certificates.
- **Subscription resolution**: Metrics and analytics correctly attribute traffic to the application, plan, and subscription.
- **Alignment with existing APIM mechanisms**: mTLS for native Kafka APIs uses the same subscription and certificate management as HTTP and Message APIs.

### Plan Restrictions

Kafka APIs can't have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together. You can't expose simultaneously:

- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)
## Technical Prerequisites

Before configuring mTLS for native Kafka APIs, ensure the following requirements are met:

### Gateway Requirements

The Kafka Gateway must be configured with:

- **Keystore**: Contains the Gateway private key and certificate
- **Truststore**: Contains the CAs that signed client certificates
- **Client authentication**: `clientAuth` must be set to `required`

These settings are defined in the `kafka.ssl` section of `gravitee.yml`.

### Client Requirements

The Kafka client must be configured with:

- **Keystore**: Contains the client private key and certificate
- **Truststore**: Contains the CA that signed the Gateway certificate

The client certificate in the keystore must match the certificate associated with your application subscription in APIM.

### SSL Configuration Files

Both the Gateway and the Kafka client require properly configured SSL files:

- **Gateway keystore**: JKS, PKCS12, or PEM format
- **Gateway truststore**: JKS, PKCS12, or PEM format
- **Client keystore**: JKS, PKCS12, or PEM format
- **Client truststore**: JKS, PKCS12, or PEM format

<!-- GAP: No explicit mention of certificate format requirements (e.g., PEM vs DER) or whether self-signed certificates are supported -->
## Client configuration properties

To connect to a Kafka API with an mTLS plan, configure the Kafka client to use SSL with a client keystore and truststore.

Add the following properties to your Kafka client configuration:

```properties
security.protocol=SSL

ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS

ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```
## Required files

The Kafka client requires:

- **Client keystore**: Contains the client private key and certificate used to authenticate with the Gateway
- **Client truststore**: Contains the CA that signed the Gateway certificate

The client certificate in the keystore must match the certificate associated with your application subscription in APIM.
## Connection behavior

When the client connects:

1. The client initiates a TLS connection and presents its client certificate
2. The Gateway validates the certificate against known subscription certificates
3. On match, the connection is authorized and the context is populated with plan, application, and subscription information
4. Metrics and analytics reflect the resolved subscription

If the client certificate doesn't match a valid subscription, the Gateway rejects the connection.
## Impacts and Benefits

### Impacts

Enabling mTLS for native Kafka APIs introduces the following operational changes:

- **Stricter SSL configuration**: Both the Gateway and Kafka clients must be configured with keystores and truststores.
- **Mandatory client certificate management**: Applications must provide client certificates during subscription creation.
- **Limited plan combination options**: Kafka APIs can't have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together.

### Benefits

mTLS for native Kafka APIs provides:

- **Strong authentication**: Kafka clients are authenticated using certificates, preventing unauthorized access.
- **Subscription resolution**: The Gateway resolves subscriptions based on client certificates, ensuring metrics and analytics correctly attribute traffic to the application, plan, and subscription. This eliminates the `ANONYMOUS` metrics issue that occurs with Keyless plans.
- **Alignment with existing APIM mechanisms**: mTLS for native Kafka APIs uses the same subscription and certificate management as HTTP and Message APIs.
## Configure mTLS Plans and Subscriptions

mTLS plans for native Kafka APIs allow the Gateway to identify clients by certificate and resolve subscriptions. This enables accurate metrics attribution to the correct application, plan, and subscription.

### Create an mTLS Plan

To create an mTLS plan for a Kafka API:

1. Add an mTLS plan to the Kafka API (same process as for HTTP or Message APIs).
2. Publish the plan.

#### Plan Restrictions

Kafka APIs can't have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together. You can't expose simultaneously:

- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)

### Create a Subscription

After publishing the mTLS plan:

1. Create an application that contains a client certificate.
2. Create a subscription to the Kafka API using the mTLS plan.

The client certificate is used by APIM to identify the application during the Kafka connection. The behavior is identical to mTLS plans for HTTP and Message APIs.

### Subscription Resolution

When a Kafka client connects with a valid certificate:

1. The client initiates a TLS connection and presents its client certificate.
2. The Gateway validates the certificate against known subscription certificates.
3. On match, the connection is authorized and the context is populated with plan, application, and subscription information.
4. Metrics and analytics reflect the resolved subscription.

If the client certificate doesn't match a valid subscription, the Gateway rejects the connection.

<!-- GAP: Detailed UI steps for creating an application with a client certificate are not specified in source materials. -->
<!-- GAP: Detailed UI steps for creating a subscription to a Kafka API using an mTLS plan are not specified in source materials. -->