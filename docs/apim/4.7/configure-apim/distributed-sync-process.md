# Distributed Sync Process

## Overview

This article covers the distributed sync process for the Gravitee Gateway, including the motivation for its creation, an overview of how it works, and what it means for APIM developers.&#x20;

{% hint style="warning" %}
The distributed sync process requires Redis to be used as the Gateway cache, with the [RediSearch module](https://github.com/RediSearch/RediSearch) enabled.
{% endhint %}

## Background

Gravitee’s Gateway runs a synchronization (sync) process to obtain the state of APIs, API keys, subscriptions, dictionaries, and organization data from the central [repository](repositories/) backing the management API (e.g., MongoDB, Postgres). The sync process then maintains the state in the Gateway’s memory, to ensure that the Gateway is resilient and performant even if the repository is down or inaccessible.

The sync process in older versions of the Gravitee Gateway would:

* Obtain the full initial state at startup, including all APIs, dictionaries, API keys, and subscriptions.
* Incrementally obtain the delta for what has been deployed to the Gateway on a configurable cadence (5 seconds by default).

This process had notable drawbacks, in that it required each Gateway to consume a large amount of resources just to launch, and also that the state repository had to share the same data to each Gateway. This would not scale well when there were many Gateways deployed as a cluster for the same Management API.

## Overview

The distributed sync process solves these problems by introducing a zone concept along with a dedicated Redis state repository to be used by that zone.

In the distributed sync process:

* Each Gateway is assigned a zone, and one Gateway from the zone is elected as the zone leader, or “primary node.”&#x20;
* The primary Gateway obtains the state from the management repository and writes it to the distributed sync repository.
* Each zone's secondary Gateway obtains the state from the distributed sync repository for that zone.

In the event that the primary Gateway goes offline, another Gateway takes on the role of primary node.

<figure><img src="../.gitbook/assets/Management Repository.png" alt=""><figcaption></figcaption></figure>

## Configuring the distributed sync process

{% hint style="warning" %}
Ensure that Redis conforms to the requirements mentioned above, namely that the RediSearch module is enabled.
{% endhint %}

1. Enable the service by setting `services.sync.distributed.enabled` to `true` in `gravitee.yml`.
2. Enable the `distributed-sync` section of the `gravitee.yml` file for each Gateway.

A full example of the configuration in [gravitee.yml](https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml) is:

```yaml
distributed-sync:
 type: redis
 redis:
   # Redis Standalone settings
   host: localhost
   port: 6379
   password:
   # Redis Sentinel settings
   sentinel:
     master: redis-master
     nodes:
       - host: sentinel1
         port: 26379
       - host: sentinel2
         port: 26379
   # SSL settings
   ssl: false
   trustAll: true # default value is true to keep backward compatibility but you should set it to false and configure a truststore for security concerns
   tlsProtocols: # List of TLS protocols to allow comma separated i.e: TLSv1.2, TLSv1.3
   tlsCiphers: # List of TLS ciphers to allow comma separated i.e: TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
   alpn: false
   openssl: false # Used to rely on OpenSSL Engine instead of default JDK SSL Engine
   # Keystore for redis mTLS (client certificate)
   keystore:
     type: pem # Supports jks, pem, pkcs12
     path: ${gravitee.home}/security/redis-keystore.jks # A path is required if certificate's type is jks or pkcs12
     password: secret
     keyPassword:
     alias:
     certificates: # Certificates are required if keystore's type is pem
       - cert: ${gravitee.home}/security/redis-mycompany.org.pem
     key: ${gravitee.home}/security/redis-mycompany.org.key
       - cert: ${gravitee.home}/security/redis-mycompany.com.pem
     key: ${gravitee.home}/security/redis-mycompany.com.key
   truststore:
     type: pem # Supports jks, pem, pkcs12
     path: ${gravitee.home}/security/redis-truststore.jks
     password: secret
     alias:
```
