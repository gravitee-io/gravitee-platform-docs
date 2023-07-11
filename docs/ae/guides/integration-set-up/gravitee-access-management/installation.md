---
description: >-
  This article walks through how to integrate Gravitee Alert Engine with
  Gravitee Access Management (AM)
---

# Installation

{% hint style="info" %}
**Skip installation if...**

If you are performing a new installation of the Gravitee enterprise platform or running Enterprise Docker images, you can skip the installation section.
{% endhint %}

## Installation

{% hint style="info" %}
**Be aware**

Since Gravitee Access Management 3.18, the AE connector comes bundled with Enterprise Access Management, you don’t need to download and install it.
{% endhint %}

#### Download the connector

{% code overflow="wrap" %}
```
$ curl -L https://download.gravitee.io/graviteeio-ae/plugins/connectors/gravitee-ae-connectors-ws/gravitee-ae-connectors-ws-2.1.2.zip -o gravitee-ae-connectors-ws-2.1.2.zip
```
{% endcode %}

#### Install connector

In the command below, ${GRAVITEEIO\_HOME} refers to the root directory of both the AM Gateway and Management API.

```
$ cp gravitee-ae-connectors-ws-2.1.2.zip ${GRAVITEEIO_HOME}/plugins/
```

## Configuration

For both the AM Gateway and the AM API, you need to configure access to Alert Engine through WebSockets. You can do this with the following configuration:

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

You can have as many endpoints as you need. The node will select one of them in round-robin fashion.

### Discovery mode

Discovery mode is very useful when running a cluster of Alert Engine. By using it, you just have to refer to a single AE node and the other nodes from the cluster will be automatically registered.

<figure><img src="https://docs.gravitee.io/images/ae/howitworks/discovery.png" alt=""><figcaption><p>Alert Engine: auto-discovery</p></figcaption></figure>

### Event sending mode

Sicne Alert Engine v1.5.0, it is possible to configure the connection to send events either over WebSocket (default) or HTTP.

On an environment with high throughput (\~1000 rps), we highly recommend configuring the event sending over http in order to benefit from a good load balancing and load repartition.

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

By default, to keep the same behavior of the previous version, events are sent over a websocket connection. The default behavior will switch to HTTP in a future version.\
