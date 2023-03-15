---
description: Learn more about creating Gateway APIs in Gravitee
---

# Create APIs

### Introduction

Gravitee enables teams to create Gateway APIs. Gateway APIs are what your API consumers will call or subscribe to in order to retrieve data, functionality, etc. from your backend APIs. Your backend APIs are essentially the data source or functionality that you want to expose to your consumers.&#x20;

### Supported API styles, event brokers, and communication patterns

Gravitee offers support for a variety of API styles, event brokers, and communication patterns. Please see the table below that captures Gravitee's extensive support:

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

* Synchronous and asynchronous APIs
  * Gravitee supports REST, SOAP, gRPC (limited to simple proxy for now), GraphQL (limited to simple proxy for now), Websockets, Webhooks, and Server-sent events (SSE) as API types
* Event brokers as backend data sources
  * Gravitee currently supports Kafka, Confluent, Solace, MQTT, and MQTT brokers

{% hint style="info" %}
**MQTT support**

As of today, Gravitee only supports MQTT 5 and brokers that support MQTT 5
{% endhint %}

### Entrypoints and endpoints

Before diving in to how to create Gateway APIs, there are two important concepts that you must be familiar with in order to understand the Gravitee API creation process:

* Entrypoints and endpoints: during the API creation process, you will need to define your Gateway entrypoints and endpoints. Entrypoints define the protocol and configuration by which the API consumer accesses the gateway API. This essentially defines how the backend API is exposed through the gateway. Endpoints define the protocol and configuration by which the gateway API will fetch data from, or post data to, the backend API.
  * For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint and Kafka endpoint.
* API exposure style: during the API creation p
  *



Gravitee offers three methods for getting started with API creation:

* Create an API from scratch using the Gravitee API creation wizard
* Import an API definition using one of the three supported import methods (more in the ["Import API" section](./#import-api) below)
* Start by designing an API data model with Gravitee API Designer

{% hint style="info" %}
While not for everybody, we recommend Gravitee API Designer for those that are interested in taking a design-first approach to their API initiatives. If you want to learn more about the benefits of API Design first, you can do so here. One of Gravitee's major&#x20;
{% endhint %}

### The API creation wizard

Gravitee's API creation wizard is an easy-to-use UI. To learn how to use the API creation wizard, check out the interactive tutorial below:&#x20;







To learn more about the various API creation wizard components and concepts, please feel free to use our interactive UI exploration tool, or, use the text descriptions.

{% tabs %}
{% tab title="Interactive UI exploration" %}
Insert Arcade once I have access to new UI
{% endtab %}

{% tab title="Text descriptions" %}
The API creation wizard is comprised of the following modules:

* **API basic details/metadata:** basic information such as API name, API version number, and API description.
* **Gateway entrypoints:** how API consumers will "access" the Gravitee Gateway and ultimately consume data from a target or source

{% hint style="info" %}
For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint, as this is how consumers will consume data from your target or source, which is Kafka.
{% endhint %}

* **Gateway endpoints:** the target or source (often a backend system, but _not always_) that the Gateway will route a request to, or, in the case of asynchronous API use cases, establish a persistent connection with and field messages from.

{% hint style="info" %}
For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint and "Kafka" as your endpoint, as the Gateway will establish a persistent connection with your Kafka topic and then stream messages in real-time via a Websocket connection to the consumer.
{% endhint %}

* **Security:** how you regulate access to your API by configuring plans and access controls. The Security section will allow you to define:
  * **Plan information:** basic plan details, the "Security level" or authentication type, subscription validation (either automatic or manual), and terms of service.
  * **Configuration**: where you can define your [Gravitee Access Management](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/hbYbONLnkQLHGL1EpwKa/) Configuration, or external IdP/IAM configuration.
  * **Limitations:** where you can easily define initial API consumption limitations, such as rate limits and quotas, path authorizations, and exceptions.

{% hint style="info" %}
What you define will be dependent on what you choose during the Plan information and Configuration modules. For example, if you were to choose OAuth2 as your security level, you would be able to define:

* **Rate limit:** configures the number of requests allowed over either seconds or minutes
  * **Quota:** configures the number of requests allowed over either hours, days, weeks, or months
  * **Path authorizations:** define IP addresses that you will allow or deny.&#x20;
  * Exceptions: define certain consumer profiles or characteristics that will be treated as "exceptions" as they relate to your security settings.
{% endhint %}

* **Documentation:** this is where you upload your API specification documents. Gravitee supports either markdown or OpenAPI for this step.

{% hint style="warning" %}
While you can skip this step, we highly reccommend creating documentation for every API that you create, as this is best practice.
{% endhint %}

* **Summary:** this is where you can review and change everything that you have configured so far. Once you are satisfied with your API, you have two options:
  * **Create my API:** your API is created, but not yet consumable.&#x20;
  * **Deploy my API:** publishes your API to consumers so that it can be consumed.

{% hint style="info" %}
One thing to keep in mind: Gravitee offers much more in the way of securing APIs, making them more reliable, inducing transformations, etc. using the [Gravitee Policy Designer](../policy-design/). Depending on your needs or use case, you may want to check this out before deploying your API to consumers.
{% endhint %}
{% endtab %}
{% endtabs %}

### Import APIs

In addition to "Creating your API from scratch" with the API creation wizard, Gravitee supports Gravitee API creation via import. You will have four options for API import. To learn more, please feel free to use our interactive UI exploration tool, or, use the text descriptions.

{% tabs %}
{% tab title="Interactive UI exploration" %}
Insert arcade once we have access to new UI
{% endtab %}

{% tab title="Text descriptions" %}
Gravitee allows you to import an API definition via:

* OpenAPI: One of the most powerful features of APIM is its ability to import an OpenAPI specification to create an API. When you import an existing specification you do not have to complete all the fields required when you create a new API.
  * Swagger
  * URL
  * File
* WSDL file: APIM can import a WSDL to create an API. This means you do not have to declare all the routing and policies to interact with your service.
* Existing API as a template: use an already-created Gravitee API as a template and simply edit certain details in the configuration
* Using a model from [Gravitee API Designer](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/3DqdkbBufOGIYC4eu2tC/): import a data model that you created using the Gravitee API Designer to reduce the amount of configuration necessary.&#x20;
{% endtab %}
{% endtabs %}

### Creating synchronous, asynchronous, event-based, and streaming APIs in Gravitee

One of Gravitee's major differentiators is an ability to create, manage, and secure synchronous and asynchronous APIs. This is made possible via a variety of Gravitee features and functionality, but, as it pertains to API creation, it is important to understand the following concepts related to support for synchronous and asynchronous APIs:

{% tabs %}
{% tab title="Selecting your API architecture" %}
If using the API creation wizard, you will be asked to **Select your API architecture. You will have two options:**

1. HTTP proxy: this will be used if you want to proxy Web APIs can **** be accessed via the HTTP protocol. If you choose this option, you will define endpoints and valid request and response formats.

{% hint style="info" %}
If you are hoping to use Gravitee to manage, secure, govern, and expose REST APIs, pure Websocket proxy, SOAP APIs, or pure gRPC proxy, this is typically your best option.&#x20;
{% endhint %}

2. Message: this includes asynchronous/streaming/event-driven API entrypoints[^1]. These are typically used for streaming APIs.

{% hint style="info" %}
Supported asynchronous API entrypoints are WebSocket, Webhook, gRPC, and SSE.
{% endhint %}
{% endtab %}

{% tab title="Entrypoints and endpoints" %}
With our support for asynchronous APIs, we released support for decoupling entrypoints and endpoints. In Gravitee, entrypoints and endpoints are:

* **Gateway Entrypoints**: how API consumers will "access" the Gravitee Gateway and ultimately consume data from a target or source.

{% hint style="info" %}
For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint, as this is how consumers will consume data from your target or source, which is Kafka.
{% endhint %}

* **Gateway endpoints:** the target or source (often a backend system, but _not always_) that the Gateway will route a request to, or, in the case of asynchronous API use cases, establish a persistent connection with and field messages from.

{% hint style="info" %}
For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint and "Kafka" as your endpoint, as the Gateway will establish a persistent connection with your Kafka topic and then stream messages in real-time via a Websocket connection to the consumer.
{% endhint %}
{% endtab %}

{% tab title="Protocol mediation" %}
Another important feature of decoupling entrypoints and endpoints is the ability for Gravitee to mediate between different protocols, API styles, and communication patterns. Gravitee is able to mediate between any entrypoint and endpoint that we currently support.

{% hint style="info" %}
For example, you could make a Kafka topic (via Kafka endpoint) consumable over WebSocket, Webhook, REST API, or SSE (all of these are supported entrypoints). to see an example where Gravitee is mediating between MQTT (supported endpoint) and various supported entrypoints, [check out this tutorial](https://community.gravitee.io/t/gravitee-3-20-release-tutorials-http-post-over-mqtt-websocket-over-mqtt-and-more/1427).&#x20;
{% endhint %}
{% endtab %}
{% endtabs %}

[^1]: Remember, Gravitee entrypoints are how API consumers will "access" the Gravitee Gateway and ultimately consume data from a target or source.



    **For example**, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint, as this is how consumers will consume data from your target or source, which is Kafka.
