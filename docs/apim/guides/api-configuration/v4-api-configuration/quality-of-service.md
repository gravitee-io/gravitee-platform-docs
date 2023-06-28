---
description: >-
  This article walks through how to configure Quality of Service for Gravitee v4
  APIs
---

# Quality of Service

## Introduction

When working with asynchronous APIs and/or event brokers, quality of service is important. Quality of service defines the guaranteed level of message delivery. For example, a quality of service of "none" means that a given message might be delivered zero, one, or several times. A quality of service of "at-most-once" means that a given message will be delivered zero or one times, with no duplication.

A higher quality of service could lead to lower system performance depending on the endpoint chosen. Please see the following table that describes the different levels of QoS:

| Level                  | Description                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| None                   | A given message might be delivered zero, one, or many times. This level allows high throughput and good performance but without guaranteed delivery. After failure or disconnection, the client will only receive messages sent after reconnection.                                                                                                                                                                |
| Auto (0 or N)          | A given message might be delivered zero, one, or many times. This level allows a trade-off between performance and delivery guarantee. Delivery is highly dependent on the capabilities supported by the endpoint connector. In case of failure or disconnection, after reconnection the client will resume, if possible, from a previously saved state, although duplication of messages could potentially exist. |
| At-Most-Once (0 or 1)  | A given message might be delivered zero times or once without any duplication. Depending on the capabilities of the entrypoint connector, performance could be degraded.                                                                                                                                                                                                                                           |
| At-Least-Once (1 or N) | A given message is delivered once or many times. This level gives a good balance between guaranteed delivery and performance when compared to At-Most-Once, especially when the entrypoint connector is not able to resume message streams after failure.                                                                                                                                                          |

The quality of service is set on the entrypoints. A given quality of service may or may not be supported by a given endpoint. Support also depends on the protocol used for the entrypoint. Please see the following table that outlines QoS compatibility:

| Entrypoint       | MQTT endpoint               | MQTT Advanced endpoint      | Kafka endpoint | Kafka Advanced endpoint                 |
| ---------------- | --------------------------- | --------------------------- | -------------- | --------------------------------------- |
| HTTP POST        | None, Auto                  | None, Auto                  | None, Auto     | None, Auto                              |
| HTTP GET         | Auto                        | Auto                        | Auto           | Auto, At-Least-Once, At-Most-Once       |
| SSE              | None, Auto                  | None, Auto                  | None, Auto     | None, Auto                              |
| SSE Advanced     | None, Auto                  | None, Auto                  | None, Auto     | None, Auto, At-Least-Once, At-Most-Once |
| WebSocket        | None, Auto                  | None, Auto                  | None, Auto     | None, Auto                              |
| Webhook          | At-Least-Once, At-Most-Once | At-Least-Once, At-Most-Once | None, Auto     | None, Auto, At-Least-Once, At-Most-Once |
| Webhook Advanced | At-Least-Once, At-Most-Once | At-Least-Once, At-Most-Once | None, Auto     | None, Auto, At-Least-Once, At-Most-Once |

## Setting quality of service for Gravitee v4 APIs

You can set quality of service levels with the `qos` object in the `entrypoints` object, as shown in the following example. See the [`swagger.json`](https://docs.gravitee.io/apim/3.x/management-api/3.20/swagger.json) definition of the Management API for a list of possible `qos` values you can specify.

```
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
