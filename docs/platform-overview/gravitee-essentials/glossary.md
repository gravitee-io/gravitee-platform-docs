---
description: Gravitee defined
---

# Gravitee Glossary

All core Gravitee and related web API terminology defined. Use the search function to quickly look up a definition.

### Products

* **Gravitee API Management (APIM):**&#x20;
* **Gravitee Access Management (AM):** apply identity and access management (multi-factor authentication, biometric, etc.) at the API and application levels
* **Gravitee Alert Engine (AE):** monitor API consumption and configure alerts based on anomalous traffic, reliability incidents, etc.
* **Gravitee API Designer (APID):** design, document, and publish API data models; the community version is limited to one data model
* **Gravitee Cloud (GC):** centrally manage Gravitee environments and installations and promote APIs across various environments; the community version is limited to one managed environment

### Product components

#### APIM

* **management UI:** a console UI that teams can use to configure their Gateway, design and create APIs, design policies, and publish documentation. Every action in the API management console is tied to a REST API that can be accessed outside the console
* **management API:** REST API that can be used to configure and manage APIs and various Gravitee resources
* **gateway:** reverse proxy layer that brokers, secures, and hardens access to APIs and data streams; natively supports both synchronous and asynchronous APIs
* **developer portal:** build an API catalog and marketplace for API consumers fit with documentation, API analytics, and more

#### AM

* developer portal
* gateway
* management API
* management UI

#### AE

* management UI
* management API

#### APID

* gateway
* developer portal

#### GC

* gateway
* developer portal

### Gravitee Terminology

* **Enterprise Edition:** Built on top of our open-source foundations, the enterprise event-native API Management platform enables organizations to fully manage, secure, monitor, and govern their entire API ecosystem. Learn more [here](gravitee-offerings-ce-vs-ee.md).
* **Community Edition:** comprised of Gravitee’s open source offerings, plus Gravitee’s free-to-use versions of Gravitee-managed enterprise products. Learn more [here](gravitee-offerings-ce-vs-ee.md).
* **API definition:** a JSON representation of everything that the Gravitee Gateway needs to know in order for it to proxy, apply policies to, create plans for, etc. your APIs and their traffic -- a gateway specification
* **gateway entrypoint:** how the consumer “calls” or “subscribes” to the gateway. This essentially defines how a consumer will end up consuming data from a producer/provider
* **gateway endpoint:** the datasource from/to which the gateway will fetch/post data for/from the consumer that calls or subscribes to the gateway
* **API publisher**
* **API consumer**
* **plugin:** components that additional functionality by _plugging into_ the Gravitee ecosystem
* **policy:** rules or logic that can be executed by the API gateway during the request or the response of an API call. The functionality of the plugin is enabled through plugins
*

### General API terminology

* **API:** an application programming interface
  * **web API:** the interacting parties run on separate machines and communicate over a network
  * **local API:** both interacting parties run on the same machine
  * **synchronous APIs**: A synchronous API is an application programming interface (API) that processes a request and requires a response.&#x20;
    * Example: A user authentication API that verifies a user's credentials and returns a token for accessing protected resources. A client application sends a request to the API with the user's username and password, and the API returns a response containing a token or an error message.&#x20;
  * **asynchronous APIs**: An asynchronous API allows for an application (consumer) to subscribe to a feed of data. All that app has to do is ask for updates once, and then updates are sent when an event occurs, regardless of whether there are any future requests. In other words, the consumers’ requests do not dictate the sending of data or messages after that initial subscription. Events (updates or changes in state) are what dictate the sending of data.
    * Example: A stock trading API that sends real-time updates on the prices of stocks. A client application subscribes to the API for updates on specific stocks. The API sends updates to the client application as soon as the prices change, without waiting for a request from the client application.&#x20;
  * API design-first
  * API lifecycle
* **event-native**
* **API specification**
  * **OpenAPI specification**
  * **AsyncAPI specification**: AsyncAPI is a specification for building and documenting asynchronous APIs. It defines a standard format for describing the messages, events, and channels of an API, making it easier for developers to understand and use the API. It is similar to OpenAPI specification (formerly Swagger) but is specifically designed for messaging and event-driven APIs.

