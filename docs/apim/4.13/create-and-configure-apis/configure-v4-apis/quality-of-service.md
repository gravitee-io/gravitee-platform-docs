---
description: An overview about quality of service.
metaLinks:
  alternates:
    - quality-of-service.md
---

# Quality of Service

## Overview

Quality of Service (QoS) defines the guaranteed level of message delivery of an asynchronous APIs or event broker. While higher Quality of Service corresponds to more reliable message delivery, this could lead to lower system performance. Different QoS are available for every entrypoint/endpoint combination. This article describes how to configure Quality of Service for Gravitee v4 APIs.

## QoS levels

The different levels of QoS are defined below:

<table><thead><tr><th width="213">Level</th><th>Description</th></tr></thead><tbody><tr><td>None</td><td><ul><li>A given message might be delivered zero, one, or many times.</li><li>Allows high throughput and good performance but without guaranteed delivery.</li><li>After failure or disconnection, the client will only receive messages sent after reconnection.</li></ul></td></tr><tr><td>Auto (0 or N)</td><td><ul><li>A given message might be delivered zero, one, or many times.</li><li>Allows a trade-off between performance and delivery guarantee.</li><li>Delivery is highly dependent on the capabilities supported by the endpoint connector.</li><li>In case of failure or disconnection, the client can resume from a previously saved state after reconnection, but duplication of messages is possible.</li></ul></td></tr><tr><td>At-Most-Once (0 or 1)</td><td><ul><li>A given message might be delivered zero times or once without any duplication.</li><li>Depending on the capabilities of the entrypoint connector, performance could be degraded.</li></ul></td></tr><tr><td>At-Least-Once (1 or N)</td><td><ul><li>A given message is delivered once or many times.</li><li>Offers good balance between guaranteed delivery and performance when compared to At-Most-Once, especially when the entrypoint connector is not able to resume message streams after failure.</li></ul></td></tr></tbody></table>

## Entrypoint/endpoint compatibility

Quality of Service is set on the entrypoints. A given QoS may or may not be supported by a given endpoint. Support also depends on the protocol used for the entrypoint. The following table outlines QoS compatibility:

<table><thead><tr><th width="131"></th><th>MQTT5</th><th>Kafka</th><th>Solace</th><th>RabbitMQ</th></tr></thead><tbody><tr><td>HTTP POST</td><td>None<br>Auto</td><td>None<br>Auto</td><td>None<br>Auto</td><td>None<br>Auto</td></tr><tr><td>HTTP GET</td><td>Auto</td><td>Auto<br>At-Least-Once<br>At-Most-Once</td><td>Auto</td><td>Auto<br>At-Least-Once<br>At-Most-Once</td></tr><tr><td>SSE</td><td>None<br>Auto</td><td>None<br>Auto<br>At-Least-Once<br>At-Most-Once</td><td>None<br>Auto</td><td>None<br>Auto<br>At-Least-Once<br>At-Most-Once</td></tr><tr><td>WebSocket</td><td>None<br>Auto</td><td>None<br>Auto</td><td>None<br>Auto</td><td>None<br>Auto</td></tr><tr><td>Webhook</td><td>None<br>Auto<br>At-Least-Once<br>At-Most-Once</td><td>None<br>Auto<br>At-Least-Once<br>At-Most-Once</td><td>None<br>Auto<br>At-Least-Once<br>At-Most-Once</td><td>None<br>Auto<br>At-Least-Once<br>At-Most-Once</td></tr></tbody></table>

## Setting QoS for Gravitee v4 APIs

You can set QoS levels with the `qos` object of the `entrypoints` object, as shown in the following example. See the Management API `openapi.json` for a list of possible `qos` values.

```json
"entrypoints": [
                {
                    "type": "sse",
                    "qos": "none",
                    "configuration": {
                        "heartbeatIntervalInMs": 5000,
                        "metadataAsComment": false,
                        "headersAsComment": false
                    }
                }
            ]
```
