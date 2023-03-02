---
description: A description of the various API creation concepts in Gravitee.
---

# Concepts

## Different ways to create APIs in Gravitee

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
  * For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint, as this is how consumers will consume data from your target or source, which is Kafka.
* **API endpoints:** the target or source (often a backend system, but _not always_) that the Gateway will route a request to, or, in the case of asynchronous API use cases, establish a persistent connection with and field messages from.
  * For example, if you wanted to make a Kafka topic consumable over Websockets, you would choose the Websockets entrypoint and "Kafka" as your endpoint, as the Gateway will establish a persistent connection with your Kafka topic and then stream messages in real-time via a Websocket connection to the consumer.
* **Security:** how you regulate access to your API by configuring plans and access controls. The Security section will allow you to define:
  * **Plan information:** basic plan details, the "Security level" or authentication type, subscription validation (either automatic or manual), and terms of service.
  * **Configuration**: where you can define your [Gravitee Access Management](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/hbYbONLnkQLHGL1EpwKa/) Configuration, or external IdP/IAM configuration.
  * **Limitations:** where you can easily define initial API consumption limitations, such as rate limits and quotas, path authorizations, and exceptions. What you define will be dependent on what you choose during the Plan information and Configuration modules. For example, if you were to choose OAuth2 as your security level, you would be able to define:
    * **Rate limit:** configures the number of requests allowed over either seconds or minutes
      * **Quota:** configures the number of requests allowed over either hours, days, weeks, or months
      * **Path authorizations:** define IP addresses that you will allow or deny.&#x20;
      * Exceptions: define certain consumer profiles or characteristics that will be treated as "exceptions" as they relate to your security settings.
* **Documentation:**&#x20;
{% endtab %}
{% endtabs %}

### Import API

