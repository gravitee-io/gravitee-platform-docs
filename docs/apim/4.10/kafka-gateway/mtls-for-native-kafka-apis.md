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

### Connection behavior

When the client connects:

1. The client initiates a TLS connection and presents its client certificate
2. The Gateway validates the certificate against known subscription certificates
3. On match, the connection is authorized and the context is populated with plan, application, and subscription information
4. Metrics and analytics reflect the resolved subscription

If the client certificate doesn't match a valid subscription, the Gateway rejects the connection.

Before implementing this configuration, review the following constraints and requirements.


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
- The Gateway does not verify the client identity.

**TLS + mTLS**

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

### Benefits

- **Strong authentication**: Kafka clients are authenticated using certificates.
- **Subscription resolution**: Metrics and analytics correctly attribute traffic to the application, plan, and subscription.
- **Alignment with existing APIM mechanisms**: mTLS for native Kafka APIs uses the same subscription and certificate management as HTTP/Message APIs.

### Plan Restrictions

Kafka APIs cannot have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together. You cannot expose simultaneously:

- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)


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