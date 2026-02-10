---
description: >-
  Learn how to configure mutual TLS (mTLS) authentication for Kafka Gateway to
  secure client-server communication
---

# Configure mTLS


## Overview

Mutual TLS (mTLS) authentication provides bidirectional certificate-based authentication between the Kafka Gateway and Kafka clients. Unlike standard TLS where only the server is authenticated, mTLS requires both parties to present valid certificates, ensuring strong identity verification for both the Gateway and connecting clients.


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

This is a complete duplication. The AFTER section should be removed entirely as it is identical to the NEW CONTENT being inserted.


## Configuration

[Rest of existing configuration content would go here]


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

- **keystore**: Contains the Gateway's private key and certificate
    - `type`: Keystore format (`jks`, `pkcs12`, or `pem`)
    - `path`: File path to the keystore
    - `password`: Keystore password

- **truststore**: Contains the certificate authorities (CAs) that signed client certificates
    - `type`: Truststore format (`jks`, `pkcs12`, or `pem`)
    - `path`: File path to the truststore
    - `password`: Truststore password

- **clientAuth**: Client authentication mode
    - `required`: Enforces mTLS (Gateway rejects connections without valid client certificates)
    - `request`: Requests but doesn't require client certificates
    - `none`: Disables client authentication

{% hint style="warning" %}
Set `clientAuth` to `required` to enforce mTLS. The Gateway will reject any client connection without a valid certificate.
{% endhint %}
