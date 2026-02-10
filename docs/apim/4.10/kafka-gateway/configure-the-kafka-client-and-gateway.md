---
description: Configure Kafka clients and Gateway settings for secure communication
---

# Configure the Kafka Client and Gateway

## Configure Kafka Client for mTLS

To connect to a Kafka Gateway with mTLS enabled, configure your Kafka client with the required SSL properties.

### Client Configuration Properties

Add the following properties to your Kafka client configuration:

```properties
# Security protocol
security.protocol=SSL

# Client truststore
# Contains the CA that signed the Gateway certificate
ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS

# Client keystore
# Contains the client private key and certificate
ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```

### Configuration Details

- **`security.protocol`**: Must be set to `SSL` to enable TLS/mTLS.
- **`ssl.truststore.location`**: Path to the truststore containing the CA that signed the Gateway certificate.
- **`ssl.truststore.password`**: Password for the client truststore.
- **`ssl.truststore.type`**: Truststore format (JKS, PKCS12, or PEM).
- **`ssl.keystore.location`**: Path to the keystore containing the client private key and certificate.
- **`ssl.keystore.password`**: Password for the client keystore.
- **`ssl.keystore.type`**: Keystore format (JKS, PKCS12, or PEM).

The client certificate in the keystore must match the certificate associated with your application's subscription to the mTLS plan.

<!-- GAP: No information provided about how to obtain or generate the client keystore/truststore files, or how to verify the certificate matches the subscription -->