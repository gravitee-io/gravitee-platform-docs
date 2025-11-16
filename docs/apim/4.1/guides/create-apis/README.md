---
description: This article covers critical Gravitee API creation concepts
---

# Create APIs

## Introduction

Gravitee enables teams to create Gateway APIs. Gateway APIs are what your API consumers will call or subscribe to in order to retrieve data, functionality, etc. from your backend APIs. Your backend APIs are essentially the data source or functionality that you want to expose to your consumers.

Gravitee currently supports two kinds of Gateway APIs:

* v4 API definition Gateway APIs: Gateway APIs that use the Gravitee v4 API definition
* (Legacy) v2 API definition Gateway APIs: Gateway APIs that use the Gravitee v2 API definition

We plan to focus our future efforts and innovation on the v4 API definition, as it enables teams to use Gravitee to manage both synchronous and asynchronous APIs. However, while the v2 API definition is still supported, we include documentation for v2 API definition-specific functionality. Please keep reading to learn more about v4 and v2 API concepts.

Keep reading this article to learn more about these different concepts. If you want to see step-by-step API creation documentation, please skip ahead to:

* [The API creation wizard documentation:](how-to/README.md) covers how to use the API creation wizard in the UI
* [The Import APIs documentation](import-apis/README.md): covers how to import APIs in Gravitee

## v4 API creation concepts

The important v4 API creation concepts are:

* Entrypoints
* Endpoints
* Backend exposure methods

### Entrypoints and endpoints

When creating v4 APIs, you will need to define your Gateway entrypoints and endpoints. These are:

* **Gateway entrypoints:** define the protocol and configuration by which the API consumer accesses the Gateway API. This essentially defines how the backend API is exposed through the gateway.
* **Gateway endpoints:** define the protocol and configuration by which the Gateway API will fetch data from, or post data to, the backend API.

For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint and Kafka endpoint. If you wanted to expose a backend REST API as a Gateway REST API (i.e. a "pure" RESt API use case), your entrypoint would be your context path (the URL location of your Gateway API) and the endpoint would be your target url (the url for the backend resource that you want to expose).

### Backend exposure methods

When creating Gateway APIs in Gravitee, you will have to define the "type" or method of exposing your backend resources. You will have two options:

* Proxy upstream protocol
* Introspect messages from event-driven backend

Depending on the the architecture that you choose, you will be limited to certain kinds of entrypoints and endpoints. Please see the tables below for more information:

#### Proxy upstream protocol

| Entrypoints                                                                                                                                                                                      | Endpoints        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------- |
| Context path that will support REST, GraphQL, gRPC, and WebSocket Gateway APIs (you will not be able to apply policies at the level of WebSocket messages if using this backend exposure method) | REST             |
|                                                                                                                                                                                                  | SOAP             |
|                                                                                                                                                                                                  | WebSocket Server |
|                                                                                                                                                                                                  | gRPC             |
|                                                                                                                                                                                                  | GraphQL          |

#### Introspect messages from event-driven backend

| Entrypoints        | Endpoints                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| HTTP GET           | Kafka (this endpoint will support Confluent-managed Kafka as well)                                                        |
| HTTP POST          | Solace (this will require a Solace-specific plugin. For access, please [contact us](https://www.gravitee.io/contact-us).) |
| WebSocket          | MQTT                                                                                                                      |
| Webhooks           |                                                                                                                           |
| Server-sent events |                                                                                                                           |

Please note that you can combine any supported entrypoint with any supported endpoint when choosing the message-based architecture. For example, you could expose a Kafka topic as a REST API using HTTP GET, as WebSocket API, as an SSE API, etc.

### Supported API styles, event brokers, and communication patterns

Gravitee's v4 API definition offers support for a variety of API styles, event brokers, and communication patterns. Please see the table below that captures Gravitee's extensive support:

| Supported API style, communication method, or event broker | How this can be used                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| REST API                                                   | <p>Gravitee can:</p><ul><li>Proxy and manage "pure" REST API use cases, where your backend API is a RESt API and the Gateway API you are using to expose that backend REST API is also a REST API</li><li>Expose Kafka, Confluent, Solace, and MQTT backend data sources as Gateway REST APIs. Please note that this specific support is currently limited to HTTP GET and HTTP POST commands.</li></ul>                       |
| SOAP API                                                   | Gravitee can expose backend SOAP web services as Gateway REST APIs.                                                                                                                                                                                                                                                                                                                                                            |
| WebSocket APIs                                             | <p>Gravitee can:</p><ul><li>Apply a simple HTTP proxy to "pure" WebSockets use cases, where the Gateway API is a Websocket API and the backend API is a Websocket API. The simple proxy only allows for transformation at the metadata level.</li></ul><ul><li>Expose Kafka, Confluent, Solace, and MQTT backend data sources as Gateway WebSocket APIs</li></ul>                                                              |
| Webhooks                                                   | Gravitee can expose Kafka, Confluent, Solace, and MQTT backend data sources over a Webhooks callback URL. This allows your API consumers to subscribe to a Gateway Webhooks API and then retrieve events and messages from these various backend data sources in real-time via this Webhooks subscription.                                                                                                                     |
| Server-sent events (SSE)                                   | Gravitee can expose Kafka, Confluent, Solace, and MQTT backend data sources over an SSE API. This allows your API consumers to subscribe to a Gateway SSE API and then retrieve events and messages from these various backend data sources in real-time via this SSE API.                                                                                                                                                     |
| Kafka                                                      | <p>The Gravitee Gateway can establish a persistent connection with a backend Kafka topic as a data source. From here, the Gateway can be used to expose messages streamed from the Kafka topic to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands for now)</li><li>WebSocket API</li><li>Webhooks</li><li>Sever-sent events API (SSE)</li></ul>                                                 |
| Confluent                                                  | <p>The Gravitee Gateway can establish a persistent connection with a backend Confluent resource as a data source. From here, the Gateway can be used to expose messages streamed from the Confluent resource to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands for now)</li><li>WebSocket API</li><li>Webhooks</li><li>Sever-sent events API (SSE)</li></ul>                                   |
| Solace                                                     | <p>The Gravitee Gateway can establish a persistent connection with a backend Solace resource as a data source. From here, the Gateway can be used to expose messages streamed from Solace to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands for now)</li><li>WebSocket API</li><li>Webhooks</li><li>Sever-sent events API (SSE)</li></ul>                                                      |
| MQTT                                                       | <p>The Gravitee Gateway can establish a persistent connection with a backend MQTT broker (as long as that MQTT broker is running MQTT 5) as a data source. From here, the Gateway can be used to expose messages streamed from the MQTT broker to consumers via:</p><ul><li>REST API (limited to HTTP GET and HTTP POST commands for now)</li><li>WebSocket API</li><li>Webhooks</li><li>Sever-sent events API (SSE)</li></ul> |

{% hint style="info" %}
**Current v4 API limitations**

It's important to know that v4 APIs currently do not support:

* Documentation upload during the API creation process
* Gravitee Debug mode
* Analytics or logs in the API Management Console
* Auditing functionality
* Messages and notifications
{% endhint %}

## v2 API creation concepts

v2 APIs don't bring as many concepts with them. In order to start creating v2 APIs in Gravitee, you mainly to understand that, one, endpoints refer to the ultimate backend target or data source of the request, and, two, that there is no concept of entrypoints.

Because there is no decoupling of entrypoints and endpoints, v2 APIs do not support protocol mediation between event brokers and messaging services. If creating v2 APIs in Gravitee, you will be limited to proxying backend APIs that communicate over HTTP 1 or HTTP 2 by exposing Gateway APIs that communicate over HTTP 1 or HTTP 2, with full support for policy enforcement at the request/response levels, but no support for message-level policies.
