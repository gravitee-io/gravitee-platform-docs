# Gravitee API Definitions

## Overview

API consumers call or subscribe to Gateway APIs to the retrieve data, functionality, etc., exposed by backend APIs. Gravitee supports two types of Gateway API definitions: v2 APIs and v4 APIs. Gravitee v2 APIs are based on the v2 API definition and Gravitee v4 APIs are based on the v4 API definition which support both HTTP and message-based protocols.

A Gravitee API definition is a JSON representation of everything that the APIM Gateway needs to know for it to proxy, apply policies to, and to create plans for your APIs and their transactions. The v2 and v4 API definitions used to create Gravitee APIs are explored in more detail below.

## Gravitee v2 APIs

The v2 API definition hinges on the following:

* Endpoints refer to the final backend target or data source of a request&#x20;
* There is no concept of entrypoints

Because there is no decoupling of entrypoints and endpoints, v2 APIs do not support protocol mediation between event brokers and messaging services. When creating v2 APIs, you are limited to proxying backend APIs that communicate over HTTP by exposing Gateway APIs that communicate over HTTP. Policy enforcement at the request/response levels is fully supported, but there is no support for message-level policies.

## Gravitee v4 APIs

The concepts critical to the v4 API definition are entrypoints, endpoints, and backend exposure methods.

### Entrypoints and endpoints

When creating v4 APIs, you will need to select your Gateway entrypoints and endpoints.

* **Gateway entrypoint:** The Gateway entrypoint defines the protocol and configuration settings the API consumer uses to access the Gateway API. This defines how the backend API is exposed through the Gateway.
* **Gateway endpoint:** The Gateway endpoint defines the protocol and configuration settings the Gateway API uses to fetch data from, or post data to, the backend API.

Gravitee Gateway entrypoints and endpoints are decoupled.

### Protocol mediation

Decoupled entrypoints and endpoints allow you to use different protocols for the entrypoint and endpoint of a single API. Gravitee uses this as the basis for protocol mediation. Protocol mediation is the ability to mediate between the two different protocols used by the consumer and a backend service.

An example of protocol mediation is a Kafka topic that is consumable over HTTP GET/POST and WebSockets. In this case, you would choose the HTTP GET, HTTP POST, and WebSockets entrypoints,  and the Kafka endpoint.&#x20;

### Backend exposure methods

When creating Gateway APIs in Gravitee, you need to define the "type" or method of exposing your backend resources: [**Proxy upstream protocol**](./#proxy-upstream-protocol) or [**Introspect messages from event-driven backend**](./#introspect-messages). The architecture that you choose impacts which entrypoints and endpoints are available:

{% tabs %}
{% tab title="Proxy upstream protocol" %}
* **Entrypoints:** Context path that supports REST, GraphQL, gRPC, and WebSocket Gateway APIs (policies cannot be applied at the WebSocket message-level using this exposure method)
* **Endpoints:** REST, SOAP, WebSocket Server, gRPC, GraphQL
{% endtab %}

{% tab title="Protocol mediation" %}
* **Entrypoints:** HTTP GET, HTTP POST, WebSocket, Webhook, Server-sent events
* **Endpoints:** Kafka (including Confluent-managed Kafka), Solace ([contact us](https://www.gravitee.io/contact-us) for the required Solace-specific plugin), MQTT

When choosing the message-based architecture, you can combine any supported entrypoint with any supported endpoint. For example, you could expose a Kafka topic as a REST API using HTTP GET, as a WebSocket API, as an SSE API, etc.
{% endtab %}
{% endtabs %}

### Proxy vs message APIs

In addition to message introspection, Gravitee offers both HTTP and TCP proxy support. The high-level characteristics of these APIs are summarized below:

{% tabs %}
{% tab title="HTTP proxy APIs" %}
* Traditional proxy APIs&#x20;
* Use synchronous HTTP requests&#x20;
* Support transformation to enable traffic shaping, analytics, and the application of policies
{% endtab %}

{% tab title="TCP proxy APIs" %}
* Can proxy any backend protocol that accepts TCP socket connections and can send data over the wire
* Raw TCP packets are transmitted in their native protocol format without transformation or introspection
  * Traffic shaping is unavailable
  * The types of policies and analytics that can be performed in the control plane are limited
{% endtab %}

{% tab title="Message APIs" %}
* Protocol mediation is performed on incoming data streams
* Payloads are reformulated to be consumable by HTTP
* Support transformation and introspection to enable traffic shaping, analytics, and the application of policies
{% endtab %}
{% endtabs %}

### Supported API styles, event brokers, and communication patterns

Gravitee's v4 API definition offers support for a variety of API styles, event brokers, and communication patterns, as detailed below:

<table><thead><tr><th width="204.5">Style/broker/pattern</th><th>What Gravitee can do</th></tr></thead><tbody><tr><td>REST API</td><td><ul><li>Proxy and manage "pure" REST API use cases (your backend API and the Gateway API you are using to expose that backend REST API are both REST APIs)</li><li>Expose Kafka, Confluent, Solace, and MQTT backend data sources as Gateway REST APIs (support is currently limited to HTTP GET and HTTP POST commands)</li></ul></td></tr><tr><td>SOAP API</td><td>Expose backend SOAP web services as both SOAP and REST APIs (with automatic SOAP&#x3C;>REST transformation).</td></tr><tr><td>GraphQL</td><td><p>You can use the Gravitee Gateway to proxy a GraphQL server just like you would with any other backend service or API.</p><p>Additionally, you can enhance security, apply data transformations and GraphQL-specific query-based rate limiting, observability and API exposure.</p></td></tr><tr><td>gRPC</td><td><p>You can use the Gravitee Gateway to proxy a gRPC API's just like you would with any other backend service or API.</p><p>Additionally, you can enhance security, apply data transformations and rate limiting, observability and API exposure.</p></td></tr><tr><td>WebSocket APIs</td><td><ul><li>Apply a simple HTTP proxy to "pure" WebSockets use cases (the Gateway and backend APIs are both WebSocket APIs). The simple proxy only allows for transformation at the metadata level.</li><li>Expose Kafka, Confluent, Solace, and MQTT backend data sources as Gateway WebSocket APIs</li></ul></td></tr><tr><td>Webhook</td><td>Gravitee can expose Kafka, Confluent, Solace, and MQTT backend data sources over a Webhook callback URL. This allows your API consumers to subscribe to a Gateway Webhook API and then retrieve events and messages from these backend data sources in real-time via the Webhook subscription.</td></tr><tr><td>Server-sent events (SSE)</td><td><p>Gravitee can expose Kafka, Confluent, Solace, and MQTT backend data sources over an SSE API. This allows your API consumers to subscribe to a Gateway SSE API and then retrieve events and messages from these backend data sources in real-time via the SSE API.</p><p>SSE is enabled by the client using the <code>Content-Type: text/event-stream</code> header.</p></td></tr><tr><td>Azure Service Bus</td><td><p>The Gravitee Gateway can establish a persistent connection with Azure Service Bus as a data source, allowing the Gateway to expose events via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul></td></tr><tr><td>Kafka</td><td><p>The Gravitee Gateway can establish a persistent connection with a backend Kafka topic as a data source, allowing the Gateway to expose messages streamed from the Kafka topic to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul><p>In addition to Apache Kafka, other Kafka-vendors are supported too, such as:</p><ul><li>Amazon Managed Streaming for Apache Kafka (AWS AMS)</li></ul><ul><li>Aiven</li><li>Azure Event Hubs for Apache Kafka</li><li>Apache Kafka in Azure HDInsight</li></ul><ul><li>Confluent (see below)</li><li>Google Cloud Managed Service for Apache Kafka</li><li>IBM Event Streams</li><li>Oracle Cloud Infrastructure (OCI) Streaming with Apache Kafka</li><li>Redpanda</li><li>and more!</li></ul></td></tr><tr><td>Confluent</td><td><p>The Gravitee Gateway can establish a persistent connection with a backend Confluent (Cloud or Platform) resource as a data source, allowing the Gateway to expose messages streamed from the Confluent resource to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul></td></tr><tr><td>Solace</td><td><p>The Gravitee Gateway can establish a persistent connection with a backend Solace resource as a data source, allowing the Gateway to expose messages streamed from Solace to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands for now)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul></td></tr><tr><td>MQTT</td><td><p>The Gravitee Gateway can establish a persistent connection with a backend MQTT broker (as long as that MQTT broker is running MQTT 5) as a data source, allowing the Gateway to expose messages streamed from the MQTT broker to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands for now)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul></td></tr><tr><td>RabbitMQ</td><td><p>The Gravitee Gateway can establish a persistent connection with RabbitMQ as a backend resource or target, allowing the Gateway to expose queues to publishers and consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands for now)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul><p>This will only work if you are using RabbitMQ and the AMQP 0-9-1 protocol. Because this endpoint supports the AMQP 0-9-1 protocol, it may support other event brokers and message queues that communicate over the AMQP 0-9-1 protocol.</p><div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>Support for AMQP 1.0 protocol is coming!  Reach out to your Customer Success Representative to register your interest.</p></div></td></tr></tbody></table>
