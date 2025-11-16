---
description: Gravitee's cheat sheet
---

# Gravitee Glossary

This page is divided into four sections to define: [Gravitee products](glossary.md#gravitee-products), [Gravitee product components](glossary.md#gravitee-product-components), [Gravitee terminology](glossary.md#gravitee-terminology), and [general API terminology](glossary.md#general-api-terminology). General concepts with Gravitee-specific meanings or usages are included to prevent misconceptions. Use the search function to quickly find a definition.

## Gravitee products

**Gravitee API Management (APIM):** An event-native API management platform used throughout the entire lifecycle to design, deploy, manage, and secure synchronous and asynchronous APIs.

**Gravitee Access Management (AM):** Used to apply identity and access management (multi-factor authentication, biometrics, etc.) at the API and application levels.

**Gravitee Alert Engine (AE):** Monitors API consumption and configures alerts based on anomalous traffic, reliability incidents, etc.

**Gravitee API Designer (APID):** Used to design, document, and publish API data models. The community version is limited to one data model.

**Gravitee Cloud (GC):** Enables centralized management of Gravitee installations and promotes APIs across various environments. The community version is limited to one managed environment.

## Gravitee product components

### APIM

**APIM Gateway:** A reverse proxy layer that brokers, secures, and hardens access to APIs and data streams. It natively supports both synchronous and asynchronous APIs.

**APIM Management API (mAPI):** A REST API used to configure and manage APIs and various Gravitee resources.

**APIM Console:** A graphical user interface to configure gateways, create APIs, design policies, and publish documentation. Every action in the APIM Management Console is tied to a REST API that can be accessed outside of the interface.

**APIM Developer Portal:** Used to build an API catalog and marketplace for API consumers. Feature-rich with documentation generation, API analytics, etc.

### AM

**AM Gateway:** AM Gateway is the core component of the AM platform. It acts as a trust broker, connecting supported identity providers with users in a single integration and enabling customized authentication and authorization flows.

**AM Management API (mAPI):** A REST API used to configure and manage the AM platform, users and user sessions, and the authorization flow for OAuth 2.0, OpenID Connect, UMA 2.0, and SCIM 2.0 protocols.

**AM Console:** A web UI that acts as the graphical interface to the AM Management API functionality.

## Gravitee terminology

[**Community Edition:**](../gravitee-platform/gravitee-offerings-ce-vs-ee/README.md) An API management platform comprising Gravitee’s open-source offerings and the free versions of Gravitee-managed enterprise products.

[**Enterprise Edition:**](../gravitee-platform/gravitee-offerings-ce-vs-ee/README.md) The enhanced version of Gravitee's open-source and event-native API management platform. Feature sets targeting commercial end users include Alert Engine, a no-code API Designer with unlimited data models, monetization capabilities, and advanced protocol mediation options.

**Application:** The mechanism by which an API consumer registers and agrees to a Gravitee Plan that uses authentication. This allows the API producer more granular control over access to their secured API.

**Backend service exposure:** The consumption style of your API based on your upstream backend service architecture.

* **Proxy upstream protocol:** A backend exposure method in the Policy Studio that lets you use Gravitee to proxy backend REST APIs, SOAP APIs, WebSocket Server, gRPC, or GraphQL. You will not be able to enforce policies at the message level.
* **Introspect messages from event-driven backend:** A backend exposure method in the Policy Studio that lets you use Gravitee to expose backend event brokers, such as Kafka and MQTT and enforce policies at the message level.

**Context path:** A unique route targeting a specific Gateway API. The context path does not include the root URL, i.e., the context path of the URL `https://apim-gateway:8082/my-context-path` is `/my-context-path`.

**Execution context:** The runtime environment in which APIs are deployed and executed. It encompasses components and settings that are used during API transaction processing.

**Flow:** The method to control where, and under what conditions, policies act on an API transaction.

**Backend API:** The source or target API that is proxied by the Gateway.

**Gateway API:** An API deployed on the Gateway by an API publisher to expose and proxy a backend API. All Gateway APIs require at least one entrypoint and an endpoint.

**Gravitee API definition:** A human and machine-readable JSON representation of the information required by the Gravitee Gateway to proxy, apply policies to, create plans for, and otherwise manage or configure Gateway APIs and traffic. The Gravitee API Definition of a Gateway API is analogous to the OpenAPI or AsyncAPI specification of a backend API.

**Gateway endpoint:** Defines the protocol and configuration settings by which the Gateway API will fetch data from, or post data to, the backend API.

**Gateway entrypoint:** Defines the protocol and configuration settings by which the API consumer accesses the Gateway API. The Gateway entrypoint dictates how the backend API is exposed through the Gateway.

**Gravitee Expression Language (EL):** A [SpEL](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/expressions.html)-based superset that enables API publishers to dynamically configure aspects and policies of an API by referencing object properties of the current API transaction.

**Plan:** The API access layer that provides the API producer with a method to secure, monitor, and transparently communicate access details. Valid plan states are:

* **Staging:** The first state of a plan, akin to a draft. The plan can be configured but won’t be accessible to users.
* **Published:** The state of a finalized plan made available to all users. API consumers can use the APIM Portal to view, subscribe to, and consume the API. A published plan may still be edited.
* **Deprecated:** The state of a plan that is no longer available on the APIM Portal. Existing subscriptions remain in place to avoid impact to current API consumers, but new subscriptions are not permitted.
* **Closed:** The state of a plan that no longer allows subscriptions. API consumers subscribed to this plan will not be able to use the API. Closing a plan is irreversible.

**Plugin:** Components that provide additional functionality to the Gravitee ecosystem.

**Policy:** Logic that is executed by the API Gateway during an API transaction. The functionality of the policy is enabled through plugins.

**Policy Studio:** The interface in the APIM Console UI that is used to visually design flows and apply policies to Gateway APIs.

**Subscription:** A contract between an API consumer and an API publisher that requires the Gateway API to offer a plan and the API consumer to submit at least one application.

**Resource:** The element with which Gravitee defines reusable configurations.

**Sharding tag:** A mechanism to deploy a Gateway API to a subset of Gateways. A sharding tag can be mapped to a Gateway’s fully qualified domain name to prompt the Developer Portal to display the access URL of a similarly tagged API.

**Tenant:** A tag that can be assigned to Gateways and Gateway endpoints to allow the same API to target different backend APIs based on which Gateway receives the request.

## General API terminology

**Application programming interface (API):** A set of publicly exposed interface conventions enabling communication between different computer programs. A web API enables programs running on separate machines to communicate over a network. A local API enables communication between programs running on the same machine.

{% hint style="info" %}
Gravitee's documentation uses the terms "web API" and "API" synonymously. An API used for local communication is explicitly referred to as a local API.
{% endhint %}

**API publisher:** The creator, designer, and/or manager of an API.

**API consumer:** The user or application accessing the API.

**API architectural style:** Guidelines and/or constraints governing API design:

* **Representational state transfer (REST)**: An architectural style where a server receives a client request, executes requested modifications, then responds with a representation of the state of the requested resource. REST APIs respect [rigid architectural constraints](https://www.ibm.com/topics/rest-apis) and employ resource-centric URLs where each HTTP verb on a URL provides unique functionality, e.g., `GET http://foo/user/1` vs `POST http://foo/user/1`.
* **Remote procedure call (RPC):** A semi-rigid architectural style where action-centric URLs represent remote functions that are invoked via network communication. Each action corresponds to a unique URL and the HTTP verb does not determine functionality, e.g., `GET http://foo/getUser` vs `POST http://foo/addUser`.
* **Publish-subscribe pattern (pub/sub):** An architectural style where a computer termed the event broker allows information producers (publishers) to publish messages to the broker and information consumers (subscribers) to subscribe to receive messages from the broker.

{% hint style="info" %}
**Pub/sub confusion**

The pub/sub [design pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe\_pattern) is broader than Google's implementation in the [Pub/Sub](https://cloud.google.com/pubsub/docs/overview) messaging service.
{% endhint %}

**API definition:** An instance of an API specification. "API specification" and "API definition" are often used synonymously.

**API design-first:** The API definition is created before the corresponding code is written. This provides a skeleton for code development and enables the automation of boilerplate code. Deriving the code from the specification ensures that the API documentation is complete.

**API lifecycle:** The processes that govern an API from creation to retirement including design, development, testing, deployment, monitoring, troubleshooting, and security.

**API specification:** Provides an overview of API behavior, interfacing, functionality, and expected output.

* **OpenAPI Specification:** A standardized, language-agnostic, and human and machine-readable HTTP API interface definition that enables discovery and understanding of service capabilities without relying on source code, documentation, or network traffic inspection.
* **AsyncAPI Specification**: A framework to create and document asynchronous APIs that defines a standardized format for message, event, and channel descriptions to facilitate developer understanding and implementation.
* **CloudEvents:** A specification to standardize descriptions of event data that defines an envelope for the API data, not how the API is structured. In a postal service metaphor, the AsyncAPI Specification defines what constitutes a complete address and mail routing mechanisms while CloudEvents defines envelope dimensions. The letter, or payload, does not fall under the jurisdiction of either specification.

{% hint style="info" %}
**Events vs messages**

Although often used synonymously, an event is different from a message. A message is often described as the directed carrier of an event while the event is the observable change in state. However, these terms have a deeper, technical distinction discussed in the [Reactive Manifesto](https://www.reactivemanifesto.org/glossary#Message-Driven):

> "A message is an item of data that is sent to a specific destination. An event is a signal emitted by a component upon reaching a given state. In a message-driven system addressable recipients await the arrival of messages and react to them, otherwise lying dormant. In an event-driven system notification listeners are attached to the sources of events such that they are invoked when the event is emitted. This means that an event-driven system focuses on addressable event sources while a message-driven system concentrates on addressable recipients. A message can contain an encoded event as its payload."
{% endhint %}

**API transaction:** A single interaction between a client application and a server through an API. In a typical synchronous API transaction, a client request is sent to a server via API endpoint and the server response is returned to the client. An asynchronous API transaction refers to a single transmission of a message payload between a client and a message broker.

**Asynchronous APIs**: APIs that do not exhibit linear, sequential communication between information producers and information consumers. Events (i.e., changes in state) initiate all communication following the initial consumer subscription. Example: A stock trading API sends price updates in real-time, a client application subscribes to the API to track specific stocks, and the stock trading API sends price updates to the client application as they occur, without waiting for a request from the client application.

**Asynchronous programming:** The concurrent execution of tasks.

**Batch processing:** Processing and analysis of a large (compared to stream processing) data set that has been stored for a period of time.

**Concurrency vs parallelism:** In essence, concurrency involves handling many things at once while parallelism involves doing many things at once. This [stack overflow thread](https://stackoverflow.com/questions/1050222/what-is-the-difference-between-concurrency-and-parallelism) addresses these concepts, which can be difficult to disambiguate due to contextual terminology.

**Data-interchange format:** Text or binary serialized formats for storing and transferring data.

**Deserialization:** The inverse of serialization to convert a stream of bytes back into a complex object.

**Domain name:** The part of a network address that identifies a realm of administrative autonomy, authority, or control.

**Event-native:** A reactive programming implementation of event-driven architecture to natively handle asynchronous, event-driven APIs.

**Fully qualified domain name (FQDN):** A domain name that specifies its exact location in the tree hierarchy of the Domain Name System (DNS).

**GraphQL:** An architectural style, an API [query language](https://www.techopedia.com/definition/3948/query-language), and a runtime for fulfilling those queries.

**HTTP API endpoint:** One end of a network communication channel, it consists of a URL and an HTTP method to perform an action on a resource, e.g., `GET http://foo.com/api/user/1`.

**HTTP API entry point:** A special type of resource, i.e., a singleton resource that exists outside of any other collection and houses all other collections of resources. There is exactly one entry point per API, e.g., `http://foo.com/api`.

**HTTP API resource:** An object with a type, associated data, relationships to other resources, and a set of methods that operate on it.

**HTTP API route:** The part of a URL used to access a resource and does not include fragments, e.g., `http://foo.com/api/user/1`.

**Internet:** The [physically interconnected](https://theconversation.com/in-our-wi-fi-world-the-internet-still-depends-on-undersea-cables-49936) global network of computers and physical means by which information travels.

**JSON Web Key (JWK):** A JSON object representing a cryptographic key. The members of the object represent the properties of the key, including its value.

**JSON Web Key Set (JWKS):** A JSON object representing a set of JWKs. The JSON object must contain a `keys` member, which is an array of JWKs.

**Log:** An immutable, append-only data structure. Multiple consumers can read from the same log due to their persistent nature. Apache Kafka, Apache Pulsar, AWS Kinesis, and Azure Event Hubs are all log-based.

**Network communication model:** A design or architecture to accomplish communication between different systems.

* **Request-response:** A tightly-coupled, synchronous communication model in which the client initiates communication by making a request directly to the server, which responds by serving data or a service. The basis for synchronous APIs.
* **Event/message-driven:** A loosely-coupled, asynchronous communication model in which a change in state initiates communication. The basis for asynchronous APIs.

**Network protocol:** A standard for network communication.

* **Layered networking model:** A framework of protocol layers to conceptualize the complexity of communication within and between computers. Typically defined through abstractions, e.g., the Open Systems Interconnection (OSI) conceptual model.
* **Transport layer:** A conceptual layer responsible for establishing protocols that collect packet-based messages from applications and transmit them into the network.
* **Application layer:** A conceptual layer responsible for establishing protocols that detail what should be done with the data transferred over the network.

**Path parameters:** A mechanism to pass variable values when routing an API request, e.g., `http://foo.com/api/user/{id}` where {id} is a path parameter.

**Query parameters:** A mechanism to embed additional information or parameters in an endpoint URL to customize or filter the results of the request. Query parameters are appended using a question mark ("?") followed by key-value pairs separated by ampersands ("&"). Each key-value pair represents a specific parameter and its corresponding value, e.g., `http://foo.com/api/user/{id}/?height=tall` where "height" is a query parameter with a value of "tall."

**Queue:** A transient, linear data structure that uses the First In, First Out (FIFO) approach to access elements, where messages are lost when consumed. Each application typically maintains its own queue to ensure all messages are received. RabbitMQ, ActiveMQ, MSMQ, AWS SQS, and JMQ are queue-based.

**Reactive programming:** An application development technique based on asynchronous data streams. Events are the main orchestrators of application flow and scripting manages the logic to manipulate and perform operations on data streams.

**Resource:** An entity or object that is made available through an API and represents specific data or functionality that can be accessed, modified, or manipulated by clients, e.g., `{id: 42, type: employee, company: 5}`.

**Serialization:** The process of converting an object in memory to a stream of bytes for storage or transport.

**Stateful web APIs:** APIs that require the server to store information about the client making the request. The session, an encapsulation of the client-server session, is stored on the server.

**Stateless web APIs:** APIs that require the server to not store any information about the client making the request. The session, an encapsulation of the client-server session, is stored on the client.

**Stream processing:** The application of complex logic to an array of input streams as they flow through a system, including operations to append, aggregate, filter, etc.

**Synchronous APIs:** APIs that require communication to be linear, sequential, between a tightly-coupled client and server, and client-initiated, e.g., a user authentication API where the client application sends a request to the API with the user's credentials and the API returns a response containing either a token to access protected resources or an error message.

**Synchronous programming:** A linear, sequential execution of tasks.

**System architecture / design pattern:** A generalized, reusable description or template to address contextual challenges that are common in software design.

* **Monolithic architecture:** The traditional software development model in which an application is designed as a unified, tightly coupled, and self-contained unit with no dependencies on other applications.
* **Microservices architecture:** A software development model in which software comprises small, independent services that communicate over well-defined APIs.
* **Event-driven architecture (EDA):** A development model that uses events, or changes in state, to trigger asynchronous communication between decoupled services.

**World wide web (web):** An information system that uses the internet to access and connect hypermedia (e.g., web pages).
