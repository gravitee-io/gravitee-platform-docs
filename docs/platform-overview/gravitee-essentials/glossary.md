---
description: Gravitee defined
---

# Gravitee Glossary

All core Gravitee and related web API terminology defined. Use the search function to quickly look up a definition.

### Gravitee products

* **Gravitee API Management (APIM):** event-native API management platform that helps you design, deploy, manage, and secure synchronous and asynchronous APIs throughout the entire lifecycle
* **Gravitee Access Management (AM):** apply identity and access management (multi-factor authentication, biometric, etc.) at the API and application levels
* **Gravitee Alert Engine (AE):** monitor API consumption and configure alerts based on anomalous traffic, reliability incidents, etc.
* **Gravitee API Designer (APID):** design, document, and publish API data models; the community version is limited to one data model
* **Gravitee Cloud (GC):** centrally manage Gravitee environments and installations and promote APIs across various environments; the community version is limited to one managed environment

### Gravitee product components

#### APIM

* **Management UI:** a console UI that teams can use to configure their Gateway, design and create APIs, design policies, and publish documentation. Every action in the API management console is tied to a REST API that can be accessed outside the console
* **Management API:** REST API that can be used to configure and manage APIs and various Gravitee resources
* **API Gateway:** reverse proxy layer that brokers, secures, and hardens access to APIs and data streams; natively supports both synchronous and asynchronous APIs
* **API developer portal:** build an API catalog and marketplace for API consumers fit with documentation, API analytics, and more

#### AM

*

#### AE

*

#### APID

*

#### GC

*

### Gravitee terminology

* ****[**Community Edition:**](gravitee-offerings-ce-vs-ee.md) **** comprised of Gravitee’s open source offerings, plus Gravitee’s free-to-use versions of Gravitee-managed enterprise products
* ****[**Enterprise Edition:**](gravitee-offerings-ce-vs-ee.md) **** built on top of our open-source foundations, the enterprise event-native API Management platform enables commercial end-users to fully manage, secure, monitor, and govern their entire API ecosystem
* **Gravitee API definition:** a JSON representation of everything that the Gravitee Gateway needs to know in order for it to proxy, apply policies to, create plans for, etc. your APIs and their traffic — a gateway specification
* **Gateway API:** an API that is deployed on the gateway by an API publisher to expose and proxy a backend API. All gateway APIs have a unique context-path, at least one entrypoint, and an endpoint.
* **Context-path:** unique route to target a specific gateway API. The context path does not include the domain.
  * Example: If the fully qualified domain name is `https://apim-gateway:8082/my-context-path`, then `/my-context-path` is the context path.
* **Gateway entrypoint:** defines the protocol and configuration by which the API consumer accesses the gateway. This essentially defines how the backend API is exposed through the gateway.
* **Gateway endpoint:** defines protocol and configuration by which gateway will fetch data from, or post data to, the backend API
* **Backend APIs:** source or target API that is proxied by the gateway
* **API publisher:** the creator, designer, and/or manager of a gateway API
* **API consumer:** the user accessing the gateway API
* **Plan:** access layer around APIs that provide the API producer a method to secure, monitor, and transparently communicate details around access
  * **Staging** - Generally, this is the first state of a plan. View it as a draft mode. You can configure your plan but it won’t be accessible to users.
  * **Published** - Once your plan is ready, you can publish it to let API consumers view and subscribe on the APIM Portal and consume the API through it. A published plan can still be edited.
  * **Deprecated** - You can deprecate a plan so it won’t be available on the APIM portal and API Consumers won’t be able to subscribe to it. Existing subscriptions remains so it doesn’t impact your existing API consumers.
  * **Closed** - Once a plan is closed, all associated subscriptions are closed too. This can not be undone. API consumers subscribed to this plan won’t be able to use your API.
* **Application:** allows an API consumer to register and agree to a plan
* **Subscription:** a contract between an API plan and application
* **Plugin:** components that additional functionality by _plugging into_ the Gravitee ecosystem
* **Policy:** rules or logic that can be executed by the API gateway during the request or the response of an API call. The functionality of the plugin is enabled through plugins
* **API design studio:** UI that helps you create a gateway API
* **Flow:** method to enact policies on the request or response of an API call
* **Sharding tags:** a tag that can be assigned to gateway APIs and Gravitee gateways to provide a method to deploy a gateway API to a subset of gateways. Sharding tags are mapped to a gateway’s fully qualified domain name which allows the developer portal to intelligently display different gateway entrypoints depending on the API’s sharding tags
* **Tenants:** a tag that can be assigned to gateways and and gateway endpoints to allow the same API to target different backend APIs based on the gateway receiving the request
* **Expression language (EL):** language used by API publishers to configure various aspects and services of an API that supports querying and manipulating an object graph and is based on the [SpEL](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/expressions.html) (Spring Expression Language)
* **Execution context:** data available during the request/response flow of an API call

### General API terminology

* **Application programming interface (API):** a set of _publicly_ exposed interface conventions for the **** application programmer to interact with
  * **Web API:** the interacting parties run on separate machines and communicate over a network
  * **Local API:** both interacting parties run on the same machine
  * **HTTP API resource:** an object with a type, associated data, relationships to other resources, and a set of methods that operate on it
  * **HTTP API endpoint:** the URL combined with a HTTP method used to access and operate on a resource
    * Example: `GET http://foo.com/api/user/1`
  * **API entrypoint:** a special type of endpoint — it’s a resource that exists outside of any other collection and houses all other collections of resources
  * **Synchronous APIs**: employ tightly coupled communication between a client's _request_ and a server's _response_. Clients initiate all communication.&#x20;
    * Example: A user authentication API that verifies a user's credentials and returns a token for accessing protected resources. A client application sends a request to the API with the user's username and password, and the API returns a response containing a token or an error message.&#x20;
  * **Asynchronous APIs**: break up the linear, sequential communication by employing an event broker which allows information producers to _publish_ messages to the broker and information consumers to _subscribe_ to receive messages from the broker. Events (i.e., changes in state) initiate all communication.
    * Example: A stock trading API that sends real-time updates on the prices of stocks. A client application subscribes to the API for updates on specific stocks. The API sends updates to the client application as soon as the prices change, without waiting for a request from the client application.&#x20;
  * **API specification**
    * **OpenAPI specification**
    * **AsyncAPI specification**: AsyncAPI is a specification for building and documenting asynchronous APIs. It defines a standard format for describing the messages, events, and channels of an API, making it easier for developers to understand and use the API. It is similar to OpenAPI specification (formerly Swagger) but is specifically designed for messaging and event-driven APIs.
    * **CloudEvents:** specification specification for describing event data in a common way. It defines an envelope for your API’s actual data as opposed to the structure of the overall API.
      * Example: Let's draw a quick metaphor to the postal service. You can think of the AsyncAPI specification as being responsible for defining what constitutes a complete address and the means of routing the actual mail. Meanwhile, CloudEvents would be focused on defining the envelope specifications such as your envelope can be a maximum of 11-1/2" long x 6-1/8" high. However, the letter you actually send, or the payload, does not fall under the jurisdiction of either specification.
  * **API definition:** implementation of an API specification in an API description file
  * **API design-first:** the API definition is written first and then the code follows. The  advantages are that the code already has a skeleton upon which to build, and that some tools can provide boilerplate code automatically. Addtionally, this ensures that the API in code can be adequately described by the chosen specification for complete documentation of the API.
  * **API lifecycle:** process of overseeing an API from its creation to retirement including aspects such as API design, development, testing, deployment, troubleshooting, monitoring, and security
* **Event-native:** event-driven architecture implemented with reactive programming to handle asynchronous, event-driven APIs
* **Internet:** the [physically interconnected](https://theconversation.com/in-our-wi-fi-world-the-internet-still-depends-on-undersea-cables-49936) network of computers linked around the world and is the physical means by which information travels
* **World wide web (web):** information system on the internet which allows documents to be connected to other documents in the form of **hypermedia** (e.g., web pages)
* **Network protocol:** standard for communication
* **Layered networking model:** the different layers of protocols that let a computer talk at different distances and different layers of abstraction. Typically defined by different abstractions such as the Open Systems Interconnection (OSI) conceptual model.
  * **Transport layer:** a conceptual layer responsible for establishing protocols that collect packet-based messages from applications, and transmit them into the network
  * **Application layer:** a layer responsible for establishing protocols that detail what should be done with the data transferred over the network
* Network communication model
  * Request-response
    * Client
    * Server
  * Event/message streaming
    * Event
    * Message
    * Publisher
    * Subscriber
    * Broker
* System architectural style
  * Monolithic architecture: traditional model of a software program, which is built as a unified and tightly coupled unit that is self-contained and independent from other applications
  * Microservices architecture: software development model where software is composed of small independent services that communicate over well-defined APIs
  * Event-driven architecture (EDA): uses events, or changes in state, to trigger asynchrounous communication between decoupled services&#x20;
* API architectural style
  * REST: stateless architectural style where a client makes a request to the server, the server makes any modifications requested by the client, and the server responds to the client with a _**** representation of the state_ of the requested resource&#x20;
  * RPC
  * Pub/sub
  * GraphQL architectural style
* Synchronous programming
* Asynchronous programming
* Synchronous web APIs
* Asynchronous web APIs
* Stateful web APIs
* Stateless web APIs
* Reactive programming
* Queues
* Logs
* Stream processing
* Concurrency
* Parallelism
* Data-interchange format
* Serialization/deserialization
* Fully qualified domain name (fqdn)
* API route
* Domain
* URL
* URI
* URN

