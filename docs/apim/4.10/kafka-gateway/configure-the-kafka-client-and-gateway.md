## Technical Prerequisites

For mTLS to work correctly, both the Kafka Gateway and Kafka clients must be configured with specific SSL components.

### Gateway Requirements

The Kafka Gateway must be configured with:

- **Keystore**: Contains the Gateway private key and certificate
- **Truststore**: Contains the Certificate Authorities (CAs) that signed client certificates
- **Client authentication**: Must be enabled

### Client Requirements

The Kafka client must be configured with:

- **Keystore**: Contains the client private key and certificate
- **Truststore**: Contains the CA that signed the Gateway certificate

### Required SSL Files

<!-- GAP: The source mentions "Required SSL Files" as a section heading but provides no content under it. Clarification needed on what specific files or file formats should be documented here. -->

## Configure Gateway for mTLS

To enable mTLS for native Kafka APIs, configure the Gateway's SSL settings in `gravitee.yml`. This configuration defines the keystore, truststore, and client authentication mode.

### Gateway SSL configuration

Add the following configuration to the `kafka.ssl` section of `gravitee.yml`:

```yaml
kafka:
  ssl:
    # Gateway keystore
    # Contains the Gateway private key and certificate
    keystore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.keystore.jks
      password: gravitee

    # Gateway truststore
    # Contains the CAs that signed client certificates
    truststore:
      type: jks                      # jks | pkcs12 | pem
      path: /path/to/server.truststore.jks
      password: gravitee

    # Client authentication mode
    clientAuth: required             # required | request | none
```

#### Configuration parameters

- **keystore**: Contains the Gateway's private key and certificate. Supported types: `jks`, `pkcs12`, `pem`.
- **truststore**: Contains the certificate authorities (CAs) that signed client certificates. Supported types: `jks`, `pkcs12`, `pem`.
- **clientAuth**: Defines the client authentication mode. Set to `required` to enforce mTLS. The Gateway will reject any client connection without a valid certificate.

### Kafka client configuration

Configure Kafka clients to use SSL with a client keystore. The client must present a valid certificate during the TLS handshake.

```properties

security.protocol=SSL



ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS



ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```

The client keystore must contain the certificate that matches the subscription created in APIM. The Gateway uses this certificate to identify the application and resolve the subscription.

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