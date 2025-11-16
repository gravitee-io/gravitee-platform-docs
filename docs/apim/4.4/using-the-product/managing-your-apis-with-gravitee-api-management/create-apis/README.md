---
description: This article covers critical Gravitee API creation concepts
---

# Create APIs

## Introduction

API consumers call or subscribe to Gateway APIs to the retrieve data, functionality, etc., exposed by backend APIs. Gravitee supports two types of Gateway APIs: v2 and v4. These are based on the Gravitee v2 API definition and Gravitee v4 API definition, respectively.&#x20;

{% hint style="info" %}
Future efforts and innovation will focus on the v4 API definition., but v2 API documentation will be available while the v2 API definition is supported.
{% endhint %}

## v4 API creation concepts

The critical v4 API creation concepts are entrypoints, endpoints, and backend exposure methods.

### Entrypoints and endpoints

When creating v4 APIs, you will need to define your Gateway entrypoints and endpoints. These are:

* **Gateway entrypoints:** The protocol and configuration by which the API consumer accesses the Gateway API. This essentially defines how the backend API is exposed through the Gateway.
* **Gateway endpoints:** The protocol and configuration by which the Gateway API will fetch data from, or post data to, the backend API.

For example, if you wanted to make a Kafka topic consumable over WebSockets, you would choose the WebSockets entrypoint and Kafka endpoint. If you wanted to expose a backend REST API as a Gateway REST API (i.e., a "pure" REST API use case), your entrypoint would be your context path (the URL location of your Gateway API) and the endpoint would be your target URL (the URL for the backend resource that you want to expose).

### Backend exposure methods

When creating Gateway APIs in Gravitee, you need to define the "type" or method of exposing your backend resources: [**Proxy upstream protocol**](README.md#proxy-upstream-protocol) or [**Introspect messages from event-driven backend**](README.md#introspect-messages). The architecture that you choose impacts which entrypoints and endpoints are available:

{% tabs %}
{% tab title="Proxy upstream protocol" %}
* **Entrypoints:** Context path that supports REST, GraphQL, gRPC, and WebSocket Gateway APIs (policies cannot be applied at the WebSocket message-level using this exposure method)
* **Endpoints:** REST, SOAP, WebSocket Server, gRPC, GraphQL
{% endtab %}

{% tab title="Introspect messages" %}
* **Entrypoints:** HTTP GET, HTTP POST, WebSocket, Webhook, Server-sent events
* **Endpoints:** Kafka (including Confluent-managed Kafka), Solace ([contact us](https://www.gravitee.io/contact-us) for the required Solace-specific plugin), MQTT

When choosing the message-based architecture, you can combine any supported entrypoint with any supported endpoint. For example, you could expose a Kafka topic as a REST API using HTTP GET, as a WebSocket API, as an SSE API, etc.
{% endtab %}
{% endtabs %}

### Proxy vs message APIs

In addition to message introspection, Gravitee offers both HTTP and TCP proxy support. The high-level characteristics of these APIs are summarized below:

{% tabs %}
{% tab title="HTTP proxy" %}
* Traditional proxy APIs&#x20;
* Use synchronous HTTP requests&#x20;
* Support transformation to enable traffic shaping, analytics, and the application of policies
{% endtab %}

{% tab title="TCP proxy" %}
* Can proxy any backend protocol that accepts TCP socket connections and can send data over the wire
* Raw TCP packets are transmitted in their native protocol format without transformation or introspection
  * Traffic shaping is unavailable
  * The types of policies and analytics that can be performed in the control plane are limited
{% endtab %}

{% tab title="Message introspection" %}
* Protocol mediation is performed on incoming data streams
* Payloads are reformulated to be consumable by HTTP
* Support transformation and introspection to enable traffic shaping, analytics, and the application of policies
{% endtab %}
{% endtabs %}

### Supported API styles, event brokers, and communication patterns

Gravitee's v4 API definition offers support for a variety of API styles, event brokers, and communication patterns, as detailed below:

<table><thead><tr><th width="204.5">Style/broker/pattern</th><th>What Gravitee can do</th></tr></thead><tbody><tr><td>REST API</td><td><ul><li>Proxy and manage "pure" REST API use cases (your backend API and the Gateway API you are using to expose that backend REST API are both REST APIs)</li><li>Expose Kafka, Confluent, Solace, and MQTT backend data sources as Gateway REST APIs (support is currently limited to HTTP GET and HTTP POST commands)</li></ul></td></tr><tr><td>SOAP API</td><td>Expose backend SOAP web services as Gateway REST APIs</td></tr><tr><td>WebSocket APIs</td><td><ul><li>Apply a simple HTTP proxy to "pure" WebSockets use cases (the Gateway and backend APIs are both Websocket APIs). The simple proxy only allows for transformation at the metadata level.</li><li>Expose Kafka, Confluent, Solace, and MQTT backend data sources as Gateway WebSocket APIs</li></ul></td></tr><tr><td>Webhook</td><td>Gravitee can expose Kafka, Confluent, Solace, and MQTT backend data sources over a Webhook callback URL. This allows your API consumers to subscribe to a Gateway Webhook API and then retrieve events and messages from these backend data sources in real-time via the Webhook subscription.</td></tr><tr><td>Server-sent events (SSE)</td><td>Gravitee can expose Kafka, Confluent, Solace, and MQTT backend data sources over an SSE API. This allows your API consumers to subscribe to a Gateway SSE API and then retrieve events and messages from these backend data sources in real-time via the SSE API.</td></tr><tr><td>Kafka</td><td><p>The Gravitee Gateway can establish a persistent connection with a backend Kafka topic as a data source, allowing the Gateway to expose messages streamed from the Kafka topic to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul></td></tr><tr><td>Confluent</td><td><p>The Gravitee Gateway can establish a persistent connection with a backend Confluent resource as a data source, allowing the Gateway to expose messages streamed from the Confluent resource to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul></td></tr><tr><td>Solace</td><td><p>The Gravitee Gateway can establish a persistent connection with a backend Solace resource as a data source, allowing the Gateway to expose messages streamed from Solace to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands for now)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul></td></tr><tr><td>MQTT</td><td><p>The Gravitee Gateway can establish a persistent connection with a backend MQTT broker (as long as that MQTT broker is running MQTT 5) as a data source, allowing the Gateway to expose messages streamed from the MQTT broker to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands for now)</li><li>WebSocket API</li><li>Webhook</li><li>Sever-sent events API (SSE)</li></ul></td></tr></tbody></table>

{% hint style="warning" %}
**Limitations**

v4 APIs currently do not support Gravitee Debug mode
{% endhint %}

## v2 API creation concepts

The v2 API definition hinges on the following:

* Endpoints refer to the final backend target or data source of a request&#x20;
* There is no concept of entrypoints

Because there is no decoupling of entrypoints and endpoints, v2 APIs do not support protocol mediation between event brokers and messaging services. When creating v2 APIs, you are limited to proxying backend APIs that communicate over HTTP by exposing Gateway APIs that communicate over HTTP. Policy enforcement at the request/response levels is fully supported, but there is no support for message-level policies.
