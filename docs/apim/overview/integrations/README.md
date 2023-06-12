# Integrations

<mark style="color:yellow;">Need to detail all high-level integrations</mark>

## Event-native support

Part of Gravitee's leading event-native API Management feature set is native support for leading event brokers. These include:

* Kafka
* Confluent
* Solace
* MQTT brokers running MQTT 5
  * HiveMQ
  * Mosquito
  * Etc.

For more information on what this support entails, please read the sections below.

## Gravitee's Kafka support

The Gravitee Gateway is able to establish a persistent connection with a backend Kafka topic. This Kafka topic can be treated as a producer (i.e. Gravitee listens for events/messages from Kafka) and/or a consumer (i.e. Gravitee publishes messages or data to the Kafka topic).&#x20;

Once the persistent connection is established Gravitee users can expose Kafka topics to API consumers as:

* A Gateway REST API
* A Gateway WebSocket API
* A Gateway Webhooks subscription
* A Gateway Server-sent Events API

This is handled via Gravitee's protocol mediation capability, which allows for Gravitee users to mediate between the native Kafka protocol and whatever protocol, API type, or communication style for which Gravitee offers a Gateway entrypoint connector. For more information on this support, please refer to the [API creation section of our documentation](../../guides/create-apis/).

Beyond support for proxying a Kafka topic, Gravitee can also apply policies at the message level for messages coming to and/or from a Kafka topic.

## Gravitee's Confluent support

The Gravitee Gateway is able to establish a persistent connection with a backend Confluent topic. This Confluent topic can be treated as a producer (i.e. Gravitee listens for events/messages from Confluent) and/or a consumer (i.e. Gravitee publishes messages or data to the Confluent topic).&#x20;

Once the persistent connection is established Gravitee users can expose Confluent topics to API consumers as:

* A Gateway REST API
* A Gateway WebSocket API
* A Gateway Webhooks subscription
* A Gateway Server-sent Events API

This is handled via Gravitee's protocol mediation capability, which allows for Gravitee users to mediate between the native Confluent (Kafka) protocol and whatever protocol, API type, or communication style for which Gravitee offers a Gateway entrypoint connector. For more information on this support, please refer to the [API creation section of our documentation](../../guides/create-apis/).

Beyond support for proxying a Confluent topic, Gravitee can also apply policies at the message level for messages coming to and/or from a Confluent topic.

In addition to this, Gravitee supports the Confluent Schema registry, which allows the Gravitee Gateway to utilize schemas in a Confluent schema registry.

## Gravitee's Solace support

The Gravitee Gateway is able to establish a persistent connection with a backend Solace resource. This Solace resource can be treated as a producer (i.e. Gravitee listens for events/messages from Solace) and/or a consumer (i.e. Gravitee publishes messages or data to the Solace resource).&#x20;

Once the persistent connection is established Gravitee users can expose Solace event APIs to Gravitee API consumers as:

* A Gateway REST API
* A Gateway WebSocket API
* A Gateway Webhooks subscription
* A Gateway Server-sent Events API

This is handled via Gravitee's protocol mediation capability, which allows for Gravitee users to mediate between the native Solace protocol and whatever protocol, API type, or communication style for which Gravitee offers a Gateway entrypoint connector. For more information on this support, please refer to the [API creation section of our documentation](../../guides/create-apis/).

Gravitee also supports automatic import of Solace event APIs to the Gravitee Gateway, and can expose Solace event APIs in the Gravitee Developer Portal. Beyond support for proxying a Solace Event API, Gravitee can also apply policies at the message level for messages coming to and/or from a Solace resource. For more information, please refer to our [Gravitee and Solace integration documentation.](broken-reference)

## Gravitee's MQTT support

The Gravitee Gateway is able to establish a persistent connection with a backend MQTT topic. This MQTT topic can be treated as a producer (i.e. Gravitee listens for events/messages from MQTT) and/or a consumer (i.e. Gravitee publishes messages or data to the MQTT topic).&#x20;

Once the persistent connection is established Gravitee users can expose MQTT topics to API consumers as:

* A Gateway REST API
* A Gateway WebSocket API
* A Gateway Webhooks subscription
* A Gateway Server-sent Events API

This is handled via Gravitee's protocol mediation capability, which allows for Gravitee users to mediate between the native MQTT protocol and whatever protocol, API type, or communication style for which Gravitee offers a Gateway entrypoint connector. For more information on this support, please refer to the [API creation section of our documentation](../../guides/create-apis/).

Beyond support for proxying a MQTT topic, Gravitee can also apply policies at the message level for messages coming to and/or from a MQTT topic.
