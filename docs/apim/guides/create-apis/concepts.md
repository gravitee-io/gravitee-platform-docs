---
description: A description of the various API creation concepts in Gravitee.
---

# Concepts

## Different ways to create APIs in Gravitee

Gravitee offers three methods for getting started with API creation:

* Create an API from scratch using the Gravitee API creation wizard
* Import an API definition using one of the three supported import methods (more in the ["Import API" section](concepts.md#import-api) below)
* Start by designing an API data model with Gravitee API Designer

{% hint style="info" %}
While not for everybody, we recommend Gravitee API Designer for those that are interested in taking a design-first approach to their API initiatives. If you want to learn more about the benefits of API Design first, you can do so here.&#x20;
{% endhint %}

### The API creation wizard

Gravitee's API creation wizard is an easy-to-use UI. To learn more about the various API creation wizard components and concepts, please feel free to use our interactive UI exploration tool, or, use the text descriptions.

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

## Creating synchronous, asynchronous, event-based, and streaming APIs in Gravitee

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

Another important feature of decoupling entrypoints and endpoints is the ability for Gravitee to mediate between different protocols, API styles, and communication patterns. Gravitee is able to mediate between any entrypoint and endpoint that we currently support.

{% hint style="info" %}
For example, you could make a Kafka topic (via Kafka endpoint) consumable over WebSocket, Webhook, REST API, or SSE (all of these are supported entrypoints).
{% endhint %}

Supported entrypoints and endpoints:

| Entrypoints |   |   |
| ----------- | - | - |
| HTTP        |   |   |
|             |   |   |
|             |   |   |
{% endtab %}
{% endtabs %}

[^1]: Remember, Gravitee entrypoints are how API consumers will "access" the Gravitee Gateway and ultimately consume data from a target or source.



    **For example**, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint, as this is how consumers will consume data from your target or source, which is Kafka.
