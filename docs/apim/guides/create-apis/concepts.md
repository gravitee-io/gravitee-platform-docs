---
description: A description of the various API creation concepts in Gravitee.
---

# Concepts

## Different ways to create APIs in Gravitee

### The API creation wizard

Gravitee's API creation wizard is an easy-to-use UI that allows you to create Gravitee APIs by defining:

* API basic details/metadata: basic information such as API name, API version number, and API description.
* Gateway: entrypoints: how API consumers will "access" the Gravitee Gateway and ultimately consume data from a target or source
  * For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint, as this is how consumers will consume data from your target or source, which is Kafka.
* API endpoints: the target or source (often a backend system, but _not always_) that the Gateway will route a request to, or, in the case of asynchronous API use cases, establish a persistent connection with and field messages from.
  * For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint and "Kafka" as your endpoint, as the Gateway will establish a persistent connection with your Kafka topic and then stream messages in real time via a Websocket connection to the consumer.
* Security: how you regulate access to your API by configuring plans and access controls.&#x20;

#### API configuration

**API type**

**Basic info**

### Import API

