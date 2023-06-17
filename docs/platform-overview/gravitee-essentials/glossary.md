---
description: Gravitee's cheat sheet
---

# Gravitee Glossary

This page is divided into four sections to define: [Gravitee products](glossary.md#gravitee-products), [Gravitee product components](glossary.md#gravitee-product-components), [Gravitee terminology](glossary.md#gravitee-terminology), and [general API terminology](glossary.md#general-api-terminology). General concepts with Gravitee-specific meanings or usages are included to prevent misconceptions. Use the search function to quickly find a definition.

## Gravitee products

* **Gravitee API Management (APIM):** An event-native API management platform used throughout the entire lifecycle to design, deploy, manage, and secure synchronous and asynchronous APIs.
* **Gravitee Access Management (AM):** Used to apply identity and access management (multi-factor authentication, biometrics, etc.) at the API and application levels.
* **Gravitee Alert Engine (AE):** Monitors API consumption and configures alerts based on anomalous traffic, reliability incidents, etc.
* **Gravitee API Designer (APID):** Used to design, document, and publish API data models. The community version is limited to one data model.
* **Gravitee Cloud (GC):** Enables centralized management of Gravitee installations and promotes APIs across various environments. The community version is limited to one managed environment.

## Gravitee product components

### APIM

* **Management UI:** A graphical user interface to configure gateways, create APIs, design policies, and publish documentation. Every action in the API management UI is tied to a REST API that can be accessed outside of the interface.
* **Management API:** A REST API used to configure and manage APIs and various Gravitee resources.
* **API Gateway:** A reverse proxy layer that brokers and secures access to APIs and data streams. It natively supports both synchronous and asynchronous APIs.
* **API Developer Portal:** Used to build an API catalog and marketplace for API consumers. Feature-rich with with documentation generation, API analytics, etc.

### AM

*

### AE

*

### APID

*

### GC

*

## Gravitee terminology

* [**Community Edition:**](gravitee-offerings-ce-vs-ee/) An event-native API management platform comprising Gravitee’s open-source offerings and the free versions of Gravitee-managed enterprise products.
* [**Enterprise Edition:**](gravitee-offerings-ce-vs-ee/) The enhanced version of Gravitee's open-source event-native API management platform. Feature sets targeting commercial end users include the Alert Engine, the no-code API Designer with unlimited data models, monetization capabilities, and advanced protocol mediation options.
* **Gravitee API Definition:** A human and machine-readable JSON representation of the information required by the Gravitee Gateway to proxy, apply policies to, create plans for, and otherwise manage or configure gateway APIs and traffic. The Gravitee API Definition of a gateway API is analogous to the OpenAPI or AsyncAPI specification of a backend API.&#x20;
* **Gravitee Gateway API:** An API deployed on the gateway by an API publisher to expose and proxy a backend API. All gateway APIs require at least one entrypoint and an endpoint.
* **Gravitee Gateway API Architecture:** _still not finalized_
  * **Proxy:** _still not finalized_
  * **Message:** _still not finalized_
* **Gravitee Context Path:** A unique route targeting a specific gateway API. The context path does not include the root URL, i.e., the context path of the fully qualified domain name `https://apim-gateway:8082/my-context-path` is `/my-context-path`. NOTE: _not finalized but some APIs do not have a context-path_
* **Gravitee Gateway Entrypoint:** Defines the protocol and configuration settings by which the API consumer accesses the gateway API. The gateway entrypoint dictates how the backend API is exposed through the gateway.
* **Gravitee Gateway Endpoint:** Defines the protocol and configuration settings by which the gateway API will fetch data from, or post data to, the backend API.
* **Gravitee Backend API:** The source or target API that is proxied by the gateway.
* **Gravitee API Publisher:** The creator, designer, and/or manager of a gateway API.
* **Gravitee API Consumer:** The user or application accessing the gateway API.
* **Gravitee Plan:** The API access layer that provides the API producer with a method to secure, monitor, and transparently communicate access details. Valid plan states are:
  * **Staging:** The first state of a plan, akin to a draft. The plan can be configured but won’t be accessible to users.
  * **Published:** The state of a finalized plan made available to all users. API consumers can use the APIM Portal to view, subscribe to, and consume the API. A published plan may still be edited.
  * **Deprecated:** The state of a plan that is no longer available on the APIM portal and API Consumers won’t be able to subscribe to it. Existing subscriptions remain so it doesn’t impact your existing API consumers.
  * **Closed:** once a plan is closed, all associated subscriptions are closed too. This can not be undone. API consumers subscribed to this plan won’t be able to use your API.
* **Plan modes:** _still not finalized_
  * `Standard` with the policy security required
  * `Push` with no security required
* **Application:** allows an API consumer to register and agree to a plan with authentication enabled. This allows the API producer more granular control over access to their secured API.
* **Subscription:** a contract between an API consumer and API publisher that requires the gateway API to have a plan and the consumer to have at least one application
* **Resource:** a way to define reusable sets of configuration
* **Plugin:** components that provide additional functionality by _plugging into_ the Gravitee ecosystem
* **Policy:** rules or logic that can be executed by the API gateway during an API transaction. The functionality of the policy is enabled through plugins
* **API design studio:** a component of APIM's management UI that allows you to interactively create a gateway API
* **Flow:** method to control where, and under what conditions, policies act on an API transaction
* **Sharding tags:** a tag that can be assigned to gateway and gateway APIs to provide a method to deploy a gateway API to a subset of gateways. Sharding tags can be mapped to a gateway’s fully qualified domain name which allows the developer portal to intelligently display different access URLs depending on the API’s sharding tags.
* **Tenants:** a tag that can be assigned to gateways and gateway endpoints to allow the same API to target different backend APIs based on the gateway receiving the request
* **Gravitee expression language (EL):** a superset of the [SpEL](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/expressions.html) (Spring Expression Language) used by API publishers to dynamically configure various aspects and policies of an API by referencing object properties from the current API transaction
* **Execution context:** the runtime environment in which APIs are deployed and executed. It includes various components and settings that are used during the processing of API transactions.

## General API terminology

* **Application programming interface (API):** a set of _publicly_ exposed interface conventions for the _application programmer_ to interact with
  * **Web API:** the interacting parties run on separate machines and communicate over a network
  * **Local API:** both interacting parties run on the same machine

{% hint style="info" %}
In Gravitee's documentation, you can assume web APIs and APIs are synonymous terms; otherwise, we will explicitly refer to them as **local** APIs.
{% endhint %}

* **API transaction:** a single interaction between a client application and a server through an API. For synchronous APIs, it typically involves a request sent by a client application to a server using an API endpoint, and the subsequent response returned by the server to the client. For asynchronous APIs, an API transaction refers to a single transmission of a message payload between a client and a message broker
* **HTTP API resource:** an object with a type, associated data, relationships to other resources, and a set of methods that operate on it
* **HTTP API route:** part of the URL used to access a resource. It does not include parts of the URL like fragments.
  * Example: `http://foo.com/api/user/1`
* **HTTP API endpoint:** one end of a communication channel. It is the URL combined with an HTTP method used to perform an action on a resource
  * Example: `GET http://foo.com/api/user/1`
* **Resource:** an entity or object that is made available for interaction through the API. It represents a specific piece of data or functionality that can be accessed, modified, or manipulated by clients.
  * **Example:** `{id: 42, type: employee, company: 5}`
* **HTTP API entry point:** a special type of resource — it’s a singleton resource that exists outside of any other collection and houses all other collections of resources. There is exactly one entry point per API.
  * Example: `http://foo.com/api`
* **Path parameters:** a way of passing variable values within the route of an API request
  * Example: `http://foo.com/api/user/{id}` where {id} is a path parameter
* **Query parameters:** a way to include additional information or parameters in the URL to customize or filter the results of the request. Query parameters are appended to the endpoint URL using a question mark ("?") followed by key-value pairs separated by ampersands ("&"). Each key-value pair represents a specific parameter and its corresponding value.
  * Example: `http://foo.com/api/user/{id}/?height=tall` where "height" is a query parameter with a value of "tall"
* **Synchronous APIs:** APIs that require linear, sequential communication between a tightly-coupled client and server. Clients initiate all communication.&#x20;
  * Example: A user authentication API that verifies a user's credentials and returns a token for accessing protected resources. A client application sends a request to the API with the user's username and password, and the API returns a response containing a token or an error message.&#x20;
* **Asynchronous APIs**: APIs that break up the linear, sequential communication between information producers and information consumers. Events (i.e., changes in state) initiate all communication beyond the initial subscription from the information consumer.
  * Example: A stock trading API that sends real-time updates on the prices of stocks. A client application subscribes to the API for updates on specific stocks. The API sends updates to the client application as soon as the prices change, without waiting for a request from the client application.&#x20;
* **API specification:** provides a broad understanding of how an API behaves and how the API links with other APIs. It explains how the API functions and the results to expect when using the API.
  * **OpenAPI specification:** defines a standard, language-agnostic interface to HTTP APIs that allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection
  * **AsyncAPI specification**: a specification for building and documenting asynchronous APIs that defines a standard format for describing the messages, events, and channels of an API, making it easier for developers to understand and use the API.&#x20;
  * **CloudEvents:** specification for describing event data in a common way. It defines an envelope for your API’s actual data as opposed to the structure of the overall API.
    * Example: Let's draw a quick metaphor to the postal service. You can think of the AsyncAPI specification as being responsible for defining what constitutes a complete address and the means of routing the actual mail. Meanwhile, CloudEvents would be focused on defining the envelope specifications such as your envelope can be a maximum of 11-1/2" long x 6-1/8" high. However, the letter you actually send, or the payload, does not fall under the jurisdiction of either specification.
* **API definition:** an instance of an API specification. API specification and definition are often used synonymously.
* **API design-first:** the API definition is written first and then the code follows. The advantages are that the code already has a skeleton upon which to build and that some tools can provide boilerplate code automatically. Additionally, this ensures that the API in code can be adequately described by the chosen specification for complete documentation of the API.
* **API lifecycle:** process of overseeing an API from its creation to retirement including aspects such as API design, development, testing, deployment, troubleshooting, monitoring, and security
* **System architectures and design patterns:** a general, reusable description or template to a commonly occurring problem within a given context in software design
  * **Monolithic architecture:** the traditional model of a software program, which is built as a unified and tightly coupled unit that is self-contained and independent from other applications
  * **Microservices architecture:** software development model where software is composed of small independent services that communicate over well-defined APIs
  * **Event-driven architecture (EDA):** uses events, or changes in state, to trigger asynchronous communication between decoupled services&#x20;
* **Network communication model:** a design or architecture to accomplish communication between different systems
  * **Request-response:** tightly-coupled, synchronous communication model where the _client_ computer initiates communication by making a request directly to the _server_ computer which responds by serving data or a service. The basis for synchronous APIs.
  * **Event/message-driven:** loosely-coupled, asynchronous communication model where a change in state initiates communication. The basis for asynchronous APIs.

{% hint style="info" %}
**Events vs Messages**

Although often used synonymously, you can draw a distinction between an event and a message. Sometimes people will say a message is the directed carrier of the event, while the event is the actual change in state to be observed. However, these terms have a deeper, technical distinction which is outlined well by the [Reactive Manifesto](https://www.reactivemanifesto.org/glossary#Message-Driven):

> "A message is an item of data that is sent to a specific destination. An event is a signal emitted by a component upon reaching a given state. In a message-driven system addressable recipients await the arrival of messages and react to them, otherwise lying dormant. In an event-driven system notification listeners are attached to the sources of events such that they are invoked when the event is emitted. This means that an event-driven system focuses on addressable event sources while a message-driven system concentrates on addressable recipients. A message can contain an encoded event as its payload."
{% endhint %}

* **Internet:** the [physically interconnected](https://theconversation.com/in-our-wi-fi-world-the-internet-still-depends-on-undersea-cables-49936) network of computers linked around the world and is the physical means by which information travels
* **World wide web (web):** information system on the internet which allows documents to be connected to other documents in the form of hypermedia (e.g., web pages)
* **Network protocol:** standard for communication
  * **Layered networking model:** the different layers of protocols that let a computer talk at different distances and different layers of abstraction. Typically defined by different abstractions such as the Open Systems Interconnection (OSI) conceptual model.
  * **Transport layer:** a conceptual layer responsible for establishing protocols that collect packet-based messages from applications, and transmit them into the network
  * **Application layer:** a conceptual layer responsible for establishing protocols that detail what should be done with the data transferred over the network
* **API architectural style:** guidelines and/or constraints around API design
  * **Representational state transfer (REST)**: an architectural style where a client makes a request to the server, the server makes any modifications requested by the client, and the server responds to the client with a _representation of the state_ of the requested resource. REST APIs have [rigid architectural constraints](https://www.ibm.com/topics/rest-apis) and employ resource-centric URLs where a different HTTP verb on the same URL provides different functionality.
    * Example: `GET http://foo/user/1` vs `POST http://foo/user/1`
  * **Remote procedure call (RPC):** a less rigid architectural style that employs action-centric URLs. These URLs represent remote functions and RPC APIs communicate over the network to invoke them. The HTTP verb employed has no real bearing on functionality as every action will have a unique URL.
    * Example: `GET http://foo/getUser` vs `POST http://foo/addUser`
  * **Publish-subscribe pattern (pub/sub):** an architectural style where a computer known as the event _broker_ allows information producers, or _publishers_, to publish messages to the broker and information consumers, or _subscribers_, to subscribe to receive messages from the broker

{% hint style="info" %}
**Pub/sub confusion**

The pub/sub [design pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe\_pattern) is different and broader from Google's implementation of the pub/sub design pattern in the Pub/Sub [messaging service](https://cloud.google.com/pubsub/docs/overview).
{% endhint %}

* **GraphQL:** an architectural style, a [query language](https://www.techopedia.com/definition/3948/query-language) for APIs, and a runtime for fulfilling those queries
* **Event-native:** event-driven architecture implemented with reactive programming to natively handle asynchronous, event-driven APIs
* **Synchronous programming:** a linear, sequential execution of tasks
* **Asynchronous programming:** concurrent execution of tasks
* **Parallelism vs Concurrency:** the key concept is that concurrency is about _dealing with_ lots of things at once. Parallelism is about _doing_ lots of things at once.&#x20;

{% hint style="info" %}
**Concurrency vs parallelism**

These are two really tricky concepts to disambiguate, largely due to how similar they are and all the terminology (e.g., processes, threads, tasks, etc.) that can have slightly different meanings in different contexts. If you’re interested in developing a more intuitive understanding, our recommendation is to take a deep dive until you find an explanation that really clicks. This [stack overflow thread](https://stackoverflow.com/questions/1050222/what-is-the-difference-between-concurrency-and-parallelism) is a great starting place.
{% endhint %}

* **JSON Web Key (JWK):** a JSON object that represents a cryptographic key. The members of the object represent properties of the key, including its value.
* **JSON Web Key Set (JWKS):**  a JSON object that represents a set of JWKs. The JSON object MUST have a `keys` member, which is an array of JWKs.
* **Stateful web APIs:** the server stores information about the client making the request. In other words, the session is stored on the server where the session is an encapsulation of a particular client and server interaction
* **Stateless web APIs:** the server does not store any information about the client making the request. In other words, the session is stored on the client where the session is an encapsulation of a particular client and server interaction
* **Reactive programming:** making _asynchronous data streams the spine_ of your application. Events are now the main orchestrators of your application’s flow. The reactive programmer manages the logic around manipulating and performing operations on the data streams.
* **Queue:** a transient, linear data structure that uses the first in first out (FIFO) approach to accessing elements. Generally, each application has its own queue as messages are lost when consumed.
  * Example: RabbitMQ, ActiveMQ, MSMQ, AWS SQS, and JMQ are all queue-based
* **Log:** an immutable, append-only data structure. Multiple consumers can read from the same log due to their persistent nature.
  * Example: Apache Kakfa, Apache Pulsar, AWS Kinesis, and Azure Event Hubs are all log-based
* **Batch processing:** processing and analysis on a large (large in comparison to stream processing) set of data that has already been stored for a period of time
* **Stream processing:** applying complex logic to an array of input streams as they flow through the system that can be joined, aggregated, filtered, etc.
* **Data-interchange format:** text or binary serialized formats for storing and transferring data
* **Serialization:** the process of converting an object in memory to a stream of bytes for storage or transport
* **Deserialization:** the inverse process of serialization that converts a stream of bytes back into a complex object
* **Domain name:** part of a network address that identifies a realm of administrative autonomy, authority or control
* **Fully qualified domain name (FQDN):** a domain name that specifies its exact location in the tree hierarchy of the Domain Name System





