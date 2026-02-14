## Overview

Mutual TLS (mTLS) authentication provides bidirectional certificate verification between the Gateway and Kafka clients. The Gateway validates client certificates against a configured truststore, while clients verify the Gateway's certificate.

## Prerequisites

Before configuring mTLS:

- Kafka cluster with SSL/TLS enabled
- Valid SSL certificates for the Gateway (keystore)
- Certificate Authority (CA) certificates that signed client certificates (truststore)
- Client certificates signed by a trusted CA

## Gateway configuration

Configure mTLS in the `kafka.ssl` section of `gravitee.yml`.

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

### Configuration parameters

**Keystore**
- `type`: Keystore format (`jks`, `pkcs12`, or `pem`)
- `path`: File path to the keystore
- `password`: Keystore password

**Truststore**
- `type`: Truststore format (`jks`, `pkcs12`, or `pem`)
- `path`: File path to the truststore
- `password`: Truststore password

**clientAuth**
- `required`: Enforces mTLS. The Gateway rejects any client connection without a valid certificate.
- `request`: Requests but does not require a client certificate
- `none`: Disables client authentication

{% hint style="warning" %}
Set `clientAuth` to `required` to enforce mTLS. The Gateway will reject any client connection without a valid certificate.
{% endhint %}

## Kafka client configuration

Configure the Kafka client to use SSL with a client keystore.

```properties
security.protocol=SSL

ssl.truststore.location=/path/to/client.truststore.jks
ssl.truststore.password=gravitee
ssl.truststore.type=JKS

ssl.keystore.location=/path/to/client.keystore.jks
ssl.keystore.password=gravitee
ssl.keystore.type=JKS
```

<!-- GAP: Draft mentions 'Required SSL Files' section but provides no details on what files are required, how to generate them, or where to obtain them. -->

## APIM configuration

### mTLS plan

After completing the SSL/mTLS configuration:

1. Add an mTLS plan to the Kafka API (same as for a V4 API)
2. Publish the plan

{% hint style="warning" %}
Kafka APIs can't have Keyless, mTLS, and authentication (OAuth2, JWT, API Key) plans published together.
{% endhint %}

### Subscription

After publishing the plan:

1. Create an application that contains a client certificate
2. Create a subscription to the Kafka API using the mTLS plan

The client certificate is used by APIM to identify the application during the Kafka connection.