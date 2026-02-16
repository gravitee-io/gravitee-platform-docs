---
description: An overview about gravitee gateway.
---

# Gravitee Gateway

## Overview

This guide will walk through how to configure your general Gravitee API Management (APIM) Gateway settings using the `gravitee.yaml` file. As described in [APIM Components](services.md), you can override these settings by using system properties or environment variables.

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
**Format sensitive**

YAML (`yml`) format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

## Default `gravitee.yaml` config file

The following is a reference of the default configuration of APIM Gateway in your `gravitee.yml` file:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml" %}

## Kafka SSL/mTLS Configuration

The `kafka.ssl` section configures SSL and mutual TLS (mTLS) authentication for native Kafka APIs. This configuration allows the Gateway to verify Kafka client identities using certificates.

### Configuration Parameters

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

### Parameter Descriptions

| Parameter | Description | Values |
| --- | --- | --- |
| `keystore.type` | Format of the Gateway keystore | `jks`, `pkcs12`, or `pem` |
| `keystore.path` | File path to the Gateway keystore | Absolute path to keystore file |
| `keystore.password` | Password for the Gateway keystore | String |
| `truststore.type` | Format of the Gateway truststore | `jks`, `pkcs12`, or `pem` |
| `truststore.path` | File path to the Gateway truststore containing CAs that signed client certificates | Absolute path to truststore file |
| `truststore.password` | Password for the Gateway truststore | String |
| `clientAuth` | Client authentication mode | `required`, `request`, or `none` |

### Client Authentication Modes

The `clientAuth` parameter controls how the Gateway handles client certificate authentication:

- **`required`**: The Gateway requires a valid client certificate. Connections without a valid certificate are rejected. Use this mode to enforce mTLS.
- **`request`**: The Gateway requests a client certificate but doesn't require it. Connections are allowed even if no certificate is provided.
- **`none`**: The Gateway doesn't request or require client certificates. Only server-side TLS is used.

{% hint style="info" %}
To enforce mTLS for native Kafka APIs, set `clientAuth: required`.
{% endhint %}
