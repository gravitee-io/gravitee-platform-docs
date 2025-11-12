---
description: This article explains how to configure a Redis repository
---

# Redis

## Overview

The Redis repository plugin enables you to connect to Redis databases to use the Rate Limit feature. The Redis plugin is part of the default distribution of APIM.

## Supported databases

| Database | Version tested |
| -------- | -------------- |
| Redis    | 6.2.x / 7.0.x  |

## Configure the Rate Limit repository plugin

The following tables show the configuration options for different Redis implementations. All specific configurations are located under the `ratelimit.redis` attribute.

{% tabs %}
{% tab title="Standalone" %}
Redis Standalone options:

<table><thead><tr><th width="168">Parameter</th><th width="140">Default</th><th>Description</th></tr></thead><tbody><tr><td>host</td><td>localhost</td><td></td></tr><tr><td>port</td><td>6379</td><td></td></tr><tr><td>password</td><td></td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="Sentinel" %}
Redis Sentinel options:

<table><thead><tr><th width="168.66666666666666">Parameter</th><th width="90">Default</th><th>Description</th></tr></thead><tbody><tr><td>sentinel.nodes</td><td></td><td>List of sentinels with host and port</td></tr><tr><td>sentinel.master</td><td></td><td>Mandatory when using Sentinel</td></tr><tr><td>password</td><td></td><td></td></tr></tbody></table>
{% endtab %}

{% tab title="SSL" %}
Redis SSL options:

<table><thead><tr><th width="140.66666666666666">Parameter</th><th width="146">Default</th><th>Description</th></tr></thead><tbody><tr><td>ssl</td><td>false</td><td></td></tr><tr><td>trustAll</td><td>true</td><td>Default value is true for backward compatibility but keep in mind that this is not a good practice and you should set to false and configure a truststore</td></tr><tr><td>tlsProtocols</td><td>See <a href="https://vertx.io/docs/vertx-core/java/#_configuring_tls_protocol_versions">Vert.x doc</a></td><td>List of TLS protocols to allow comma separated</td></tr><tr><td>tlsCiphers</td><td>See <a href="https://vertx.io/docs/vertx-core/java/#_configuring_tls_protocol_versions">Vert.x doc</a></td><td>List of TLS ciphers to allow comma separated</td></tr><tr><td>alpn</td><td>false</td><td></td></tr><tr><td>openssl</td><td>false</td><td>Used to rely on OpenSSL Engine instead of default JDK SSL Engine</td></tr><tr><td>keystore</td><td></td><td>Configuration for Mutual TLS. The keystore is used to select the client certificate to send to the backend server when connecting. See <a href="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-repository/gravitee-apim-repository-redis/README.adoc#keystore-table">Redis SSL keystore options (client certificate, Mutual TLS)</a></td></tr><tr><td>truststore</td><td></td><td>Configuration for the truststore. The truststore is used to validate the server’s certificate. See <a href="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-repository/gravitee-apim-repository-redis/README.adoc#truststore-table">Redis SSL truststore options</a></td></tr></tbody></table>
{% endtab %}

{% tab title="SSL keystore" %}
Redis SSL keystore options (client certificate, Mutual TLS):

<table><thead><tr><th width="168.66666666666666">Parameter</th><th width="90">Default</th><th>Description</th></tr></thead><tbody><tr><td>type</td><td></td><td>Supports <code>jks</code>, <code>pem</code>, <code>pkcs12</code></td></tr><tr><td>path</td><td></td><td>A path is required if certificate’s type is <code>jks</code> or <code>pkcs12</code></td></tr><tr><td>password</td><td></td><td></td></tr><tr><td>alias</td><td></td><td></td></tr><tr><td>certificates</td><td></td><td>List of certificates with cert and key. Certificates are required if keystore’s type is <code>pem</code></td></tr></tbody></table>
{% endtab %}

{% tab title="SSL truststore" %}
Redis SSL truststore options:

<table><thead><tr><th width="168.66666666666666">Parameter</th><th width="90">Default</th><th>Description</th></tr></thead><tbody><tr><td>type</td><td></td><td>Supports <code>jks</code>, <code>pem</code>, <code>pkcs12</code></td></tr><tr><td>path</td><td></td><td></td></tr><tr><td>password</td><td></td><td></td></tr><tr><td>alias</td><td></td><td></td></tr></tbody></table>
{% endtab %}
{% endtabs %}

Below is the minimum configuration needed to get started with a Redis database.

```yaml
# ===================================================================
# MINIMUM REDIS REPOSITORY PROPERTIES
#
# This is a minimal sample file declared connection to Redis
# ===================================================================
ratelimit:
  type: redis               # repository type
  redis:                    # redis repository
    host:                   # redis host (default localhost)
    port:                   # redis port (default 6379)
    password:               # redis password (default null)
    timeout:                # redis timeout (default -1)

    # Following properties are REQUIRED ONLY when running Redis in sentinel mode
    sentinel:
      master:               # redis sentinel master host
      password:             # redis sentinel master password
      nodes: [              # redis sentinel node(s) list
        {
          host : localhost, # redis sentinel node host
          port : 26379      # redis sentinel node port
        },
        {
          host : localhost,
          port : 26380
        },
        {
          host : localhost,
          port : 26381
        }
      ]

    # Following SSL settings are REQUIRED ONLY for Redis client SSL
    ssl: true                # redis ssl mode (default false)
    trustAll: false
    tlsProtocols: TLSv1.2, TLSv1.3
    tlsCiphers: TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
    alpn: false
    openssl: false
    # Keystore for redis mTLS (client certificate)
    keystore:
      type: jks
      path: ${gravitee.home}/security/redis-keystore.jks
      password: secret
    keyPassword:
    alias:
    certificates: # Certificates are required if keystore's type is pem
    #      - cert: ${gravitee.home}/security/redis-mycompany.org.pem
    #        key: ${gravitee.home}/security/redis-mycompany.org.key
    #      - cert: ${gravitee.home}/security/redis-myothercompany.com.pem
    #        key: ${gravitee.home}/security/redis-myothercompany.com.key
    truststore:
      type: pem
      path: ${gravitee.home}/security/redis-truststore.jks
      password: secret
      alias:
```

{% hint style="info" %}
If Redis Rate Limit repository is not accessible, the API call will fail. Do not forget to monitor your probe health-check to verify that Redis repository is healthy. See the [Internal API documentation](../apim-management-api/general-configuration.md) for health endpoints.
{% endhint %}
