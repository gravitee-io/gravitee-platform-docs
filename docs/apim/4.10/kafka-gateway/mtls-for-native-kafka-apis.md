# Configure Kafka Client for mTLS

## mTLS for Native Kafka APIs Overview

mTLS (mutual TLS) for native Kafka APIs strengthens security by adding mutual authentication on top of the TLS already required for Kafka traffic. With mTLS enabled, both the Kafka client and the Gateway must present valid certificates to establish a connection.

### How mTLS differs from TLS-only authentication

**TLS only (before mTLS)**  
The Kafka client verifies the Gateway's identity using the Gateway's certificate.

**TLS + mTLS (after mTLS)**  
Both the client and the Gateway must present valid certificates. The Gateway verifies the Kafka client's identity using a client certificate.

mTLS is an additional security layer on top of TLS. It allows the Gateway to authenticate Kafka clients by certificate and resolve subscription, application, and plan dimensions for metrics and analytics.

### Why mTLS is required for native Kafka APIs

Without mTLS, native Kafka APIs configured as Keyless cannot resolve subscriptions at runtime. This results in:
- Metrics showing `ANONYMOUS` instead of the correct application/plan/subscription
- No subscription attribution in analytics
- Inability to combine Keyless plans with other security types

mTLS plans solve this by associating client certificates with subscriptions, enabling the Gateway to identify clients and populate metrics correctly.

### mTLS behavior for native Kafka APIs

mTLS for native Kafka APIs works the same way as for HTTP/Message APIs:

1. An application subscribes to an mTLS plan on a Kafka API
2. The application provides a PEM client certificate
3. The certificate is associated with the subscription
4. At runtime, the client initiates a TLS connection with the client certificate
5. The Gateway validates the certificate against known subscription certificates
6. On match, the connection is authorized and the context is populated with plan, application, and subscription data
7. Metrics and analytics reflect the resolved subscription

### Plan restrictions

Kafka APIs cannot have Keyless, mTLS, and authentication plans (OAuth2, JWT, API Key) published together. You cannot expose simultaneously:
- A Keyless plan
- An mTLS plan
- An authentication plan (OAuth2, JWT, API Key)

## Client configuration

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

### Authentication flow

When the client connects:

1. The client initiates a TLS connection and presents its client certificate
2. The Gateway validates the certificate against known subscription certificates
3. On match, the connection is authorized and the context is populated with plan, application, and subscription information
4. Metrics and analytics reflect the resolved subscription