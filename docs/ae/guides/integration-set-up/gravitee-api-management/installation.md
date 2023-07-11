---
description: >-
  This article walks through how to integrate Alert Engine with Gravitee API
  Management (APIM).
---

# Installation

{% hint style="info" %}
**Skip installation if...**

If you are performing a new installation of the Gravitee Enterprise platform or running Enterprise Docker images, you can skip the installation section. Also, since APIM version 3.18, you do not need to download and install the AE connector separately - it is shipped as part of the APIM bundle.
{% endhint %}

### Installation

#### Download the connector

{% code overflow="wrap" %}
```
$ curl -L https://download.gravitee.io/graviteeio-ae/plugins/connectors/gravitee-ae-connectors-ws/gravitee-ae-connectors-ws-2.1.2.zip -o gravitee-ae-connectors-ws-2.1.2.zip
```
{% endcode %}

#### Install the connector

In the command below, `${GRAVITEEIO_HOME}` refers to the root directory of both APIM Gateway and APIM API.

```
$ cp gravitee-ae-connectors-ws-2.1.2.zip ${GRAVITEEIO_HOME}/plugins/
```

## Configuration

For both the APIM Gateway and APIM API, you need to configure access to AE through WebSockets, as in the following example:

```
alerts:
  alert-engine:
    enabled: true
    ws:
      discovery: true
      endpoints:
        - http://localhost:8072/
      security:
        username: admin
        password: adminadmin
     # ssl:
     #   keystore:
     #     type: jks # Supports jks, pem, pkcs12
     #     path: /path/to/keystore.jks
     #     password: password
     #     certs:
     #       - /path/to/cert.pem
     #       - /path/to/cert2.pem
     #     keys:
     #       - /path/to/key.pem
     #       - /path/to/key2.pem
     #   truststore:
     #     type: jks # Supports jks, pem, pkcs12
     #     path: /path/to/keystore.jks
     #     password: password
```

### Endpoints

You can have as many endpoints as you need. The node will select one of them using a round-robin method.

### Discovery mode

You can use discovery mode when running an AE cluster to automatically register other nodes in the cluster from a single node reference.

<figure><img src="https://docs.gravitee.io/images/ae/howitworks/discovery.png" alt=""><figcaption><p>Alert Engine, auto-discovery</p></figcaption></figure>

### Event sending mode

Since v1.5.0 of the AE connector, it is possible to configure the connection to send events either over WebSocket (default) or HTTP.

On an environment with high throughput (\~1000 rps), we highly recommend configuring the event sending over http in order to benefit from better load balancing and load repartition.

Enabling this feature comes with some configuration tuning:

```
alerts:
  alert-engine:
    ws:
      sendEventsOnHttp: true # Indicates if events should be sent over http or not.
      connectTimeout: 2000   # Request timeout (useful when relying on http to send events). Default is 2000ms.
      idleTimeout: 120000    # Idle timeout. After this duration, the connection will be released.
      keepAlive: true        # Indicates if connection keep alive is enabled or not.
      pipelining: true       # Indicates if pipelining is enabled or not. When pipelining is enabled, multiple event packets will be sent in a single connection without waiting for the previous responses. Enabling pipeline can increase performances.
      tryCompression: true   # Indicates if compression is enabled when sending events. The compression must also be enabled on alert engine ingester.
      maxPoolSize: 50        # Set the maximum number of connections (useful when relying on http to send events).
      bulkEventsSize: 100    # Events will be sent by packet of 100 events.
      bulkEventsWait: 100    # Set the duration to wait for bulk events to be ready for sending. When set to 100ms with event size of 100, it means that we will wait for 100 events to be ready to be sent during 100ms. After this period of time, events will be sent event if there are less than 100 events to send.
```

As of Gravotee APIM 3.20, events are sent over HTTP as the default behavior. In order to switch back to WebSocket:

```
alerts:
  alert-engine:
    ws:
      sendEventsOnHttp: false
```

### Proxy

As of APIM 3.20, the alert engine connector can use the system proxy to send both triggers and events. In order to activate it

```
alerts:
  alert-engine:
    ws:
      useSystemProxy: false
```

This will use these proxy settings

```
# global configuration of the http client
httpClient:
  proxy:
    type: HTTP #HTTP, SOCK4, SOCK5
    http:
      host: localhost
      port: 3128
      username: user
      password: secret
    https:
      host: localhost
      port: 3128
      username: user
      password: secret
```

\
