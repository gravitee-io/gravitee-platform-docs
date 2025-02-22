# Other ways Gravitee supports Kafka

## Overview

Gravitee supports connecting to Kafka either via **protocol mediation**, where clients talk over HTTP and the Gateway talks to the backend using the Kafka client, or via **federation**, where data about topics are passed to the Developer Portal but the client never connects to the Gravitee Gateway. This page describes the different approaches.

## Kafka APIs vs other Gravitee APIs

The following sections describe the similarities and differences between Kafka APIs and other Gravitee API types that support Kafka communication: v4 Kafka message APIs, TCP proxy APIs, and Federated Kafka APIs. These comparisons highlight the appropriate use cases for Kafka APIs.

### Message APIs & TCP proxy APIs

Gravitee message APIs perform protocol mediation to transform the Kafka protocol consumed by the Gravitee Gateway into an HTTP response or request, and vice versa. TCP proxy APIs proxy the low-level TCP protocol without layering additional metadata. While TCP proxy APIs could in theory interact with Kafka brokers, the additional work required by the user is prohibitively technical and challenging.

In contrast, the Kafka Gateway implements the Kafka protocol, where clients to the Gateway can be Kafka consumers and producers that interact with the Gateway as if it were a regular Kafka broker.

### Federated Kafka APIs

Gravitee Federation is a capability that enables the creation of API catalogs that span across multiple API management platforms such as Apigee, Azure, and AWS, and event brokers like Kafka and Solace. Unified catalogs improve API governance by:

* Centralizing assets and tooling&#x20;
* Providing API consumers with one location to discover and access APIs

Subscription management and the functionality within the Developer Portal are very similar between federated Kafka APIs and Kafka-native proxy APIs, and both API types can expose Kafka topics in the portal. However, APIs running on the Kafka Gateway can also apply policies and add extra features.

Federated Kafka APIs do not run on the Gravitee Gateway. As with other federated APIs, the federation component is limited to publishing documentation and managed access to resources in Kafka.
