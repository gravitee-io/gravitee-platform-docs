---
description: >-
  This article explores the additional features that you get from the Gravitee
  Enterprise API Management solution.
---

# Open Source vs Enterprise Edition

## Introduction

Gravitee offers both an open source (OSS) and an enterprise version of its API Management (APIM) platform. In this article, we'll discuss the additional features, capabilities, hosting options, and support options that come with the Gravitee Enterprise edition of API Management.

{% hint style="info" %}
**Other Gravitee Products**

Gravitee's platform extends beyond just API Management. For information on enterprise versions of other products, please refer to our [platform overview documentation.](https://documentation.gravitee.io/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee)
{% endhint %}

## Gravitee Community Edition API Management vs Gravitee Enterprise Edition API Management

Please see the following features and capabilities that you get with the enterprise version of Gravitee API Management. Please be aware that the enterprise version of Gravitee is broken up into three different packaging structures, each with access to different amount of the below enterprise capabilities. For more information on each package, please refer to our [pricing page](https://www.gravitee.io/pricing).

### Enterprise features

The below features are included in the default enterprise API Management distribution and will not require the addition of any enterprise plugins:

* Enterprise OpenID Connect SSO: use OpenId connect for SSO for your API Management platform
* [Debug Mode](../../guides/policy-design/v2-api-policy-design-studio.md#debug-mode): easily test and debug your policy execution and enforcement.
* [Audit trail](../../guides/api-measurement-tracking-and-analytics/#the-audit-trail): audit API consumption and activity, per event and type for your Gravitee APIs. You can use the Audit trail for monitoring the behavior of your API and platform over time.
* [DCR Registration](../../guides/api-exposure-plans-applications-and-subscriptions/plans-1.md#dynamic-client-registration-provider): Dynamic client registration (DCR) is a protocol that allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint
* [Custom Roles](../../guides/administration/user-management-and-permissions.md#roles): create custom user roles to fit your needs. A role is a functional group of permissions, and can be defined at the Organization, Environment, API, and/or Application levels.
* [Sharding Tags](../../getting-started/configuration/configure-sharding-tags-for-your-gravitee-api-gateways.md): specify which "shard" of the Gateway an API should be deployed to. By tagging Gateways with specific keywords, you can select the tag in the API's Deployments proxy settings to determine the Gateway where the API will be deployed.
* Bridge Gateway: By default, an API Gateway needs to connect to a repository (mongoDB, Postgres) to retrieve the list of APIs to deploy, plans, API keys, and subscriptions. When deployed in a more complex environment (network zones, different data centers, ...), many teams prefer to avoid opening a connection between the database and something from outside its network. The solution is to deploy a Bridge Gateway, which is a kind of proxy in regards to the repository. The sync will be done over HTTP instead of the database protocol. API GW > Bridge > Database.

### Enterprise Policy pack

The Enterprise policy pack includes policies that are typically necessary for enterprise-grade, production API Management deployments:

* **Data logging masking**: if you enable logging on APIs, you can use the data-logging-masking policy to configure rules to conceal sensitive data.
* **Assign metrics**: you can use the assign-metrics policy to push extra metrics in addition to the natively provided request metrics. These metrics can then be used for monetization invoices, analytics dashboards to create custom widgets, and, optionally, apply aggregations based on their value.
* **GeoIP Filtering policy: y**ou can use the geoip-filtering policy to control access to your API by filtering IP addresses. You can allow IPs by country or distance.
* **GeoIP service:** load the geoip databases in memory. It’s required to use the geoip-filtering policy in APIM and for [Adaptive Multi-Factor Authentication in AM](https://documentation.gravitee.io/am).

### Legacy upgrade pack

The Legacy upgrade pack is comprised of the following plugins and capabilities that enable organizations to better migrate from and/or service legacy systems:

* **XSLT policy plugin**: you can use the xslt policy to apply an XSL transformation to an incoming XML request body or to the response body if your backend is exposing XML content.
* WebSocket security authentication:&#x20;

### Observability pack

The Observability Pack includes capabilities that help you better implement enterprise-grade API Monitoring and Observability:

* **Datadog reporter**: push API metrics to your Datadog instance and dashboards
* **TCP reporter**: report Gateway events to a TCP listening server

### Event-native pack

The Event-native pack includes capabilities that enable you to use Gravitee to expose, secure, and govern asynchronous APIs and event brokers:

* **v4 message API entrypoints**:
  * **HTTP GET:** enable consumers to access the Gateway and/or consume various message-based backend resources via HTTP GET
  * **HTTP POST**: enable consumers to access the Gateway and/or consume various message-based backend resources via HTTP POST
  * **WebSocket**: enable consumers to access the Gateway and/or consume various message-based backend resources via WebSocket protocol
  * **Webhooks**: enable consumers to access the Gateway and/or consume various message-based backend resources via a Webhooks subscription
  * Server-sent Events (SSE): enable consumers to access the Gateway and/or consume various message-based backend resources via Server-sent Events protocol
* **v4 message API endpoints**:
  * **Kafka/Confluent**: allows the Gateway to open up a persistent connection and/or call a backend Kafka broker via a Kafka client set up by the Gravitee Gateway
  * **MQTT**: allows the Gateway to open up a persistent connection and/or call a backend MQTT broker, as long as that broker is running on MQTT 5.x, via an MQTT client set up by the Gravitee Gateway
  * **RabbitMQ**: allows the Gateway to open up a persistent connection and/or call a backend RabbitMQ broker, as long as that broker is running on AMQP 0-9-1
  * **Solace**: allows the Gateway to expose Solace resources and event APIs via your chosen Gravitee Entrypoint(s)
* **CloudEvents policy**: transform ingoing and outgoing data using the CloudEvents spec
* **Message Filtering policy**: filter messages streamed to clients/subscribers based on certain API publisher and/or client criterion
* **Avro <> JSON policy**: transform information from Avro format into JSON format
* **Gateway message reactor plugin**: enable the Gravitee Gateway to intercept and introspect messages when publishing and subscribing to/from message-based systems
* **Confluent Schema Registry resource**: define Confluent Schema Registry as a resource for serialization and deserialization policies

## Advanced API Monitoring

While not technically a part of the API Management product, Gravitee does offer a standalone API Monitoring solution called Gravitee Alert Engine. Gravitee Alert Engine (AE) is Gravitee's enterprise grade API Monitoring solution. Alert Engine (AE) provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configuration and notifications sent through their preferred channels, such as email, Slack and Webhooks.&#x20;

Alert Engine integrates with Gravitee API Management to enable advanced alerting, new dashboards, and more. For more information, please refer to [the Alert Engine documentation](https://documentation.gravitee.io/ae/overview/introduction-to-gravitee-alert-engine).

## Advanced environment management

Gravitee EE APIM enables you to register multiple APIM environments and installations using [Gravitee Cloud.](https://documentation.gravitee.io/gravitee-cloud) This enables you to manage environment hierarchies and promote APIs across higher and lower environments.&#x20;

## Hosting options

An investment in Gravitee EE is an investment in deployment flexibility, and, optionally, the ability to offload costs associated with maintaining self-hosted API Management installations. Gravitee Enterprise supports:

* **Self-hosted deployments**: install and host APIM within your own private cloud/environment
* **Gravitee-managed deployments**: Gravitee hosts and manages all APIM components within its own cloud environments
* **Hybrid deployment**: Gravitee hosts and manages some APIM components in its own cloud environment while you manage some components in your own private cloud/environment

For more information on each, please refer to our [APIM Architecture documentation](apim-architecture.md).

### Support options

Gravitee offers enterprise-grade support for enterprise customers. Gravitee offers three different support packages: Gold, Platinum, and Diamond. Each has different SLAs, benefits, etc. For more information on each support option, please [refer to our pricing page](https://www.gravitee.io/pricing).

## Wrapping up

Our open source products are the foundation of everything we do—and they are powerful. The enterprise platform is an investment in the security and business continuity benefits of open-source paired with the power of event-native API Management, Security, Monitoring, and Design capabilities—all made available in a single platform.

In addition to the vast amount of feature and functionality that are included with the enterprise platform, the enterprise solution comes with industry-leading support, customer success services, and direct access to Gravitee leadership.

We hope that this document makes it easier to decide between Gravitee open source products and the Gravitee enterprise platform. As your trusted API Management advisor, we will always strive to help you choose the option that best fits your use case and desire to scale. If you have any questions about which solution is best for you, we recommend that you [contact us](https://www.gravitee.io/contact-us) and/or book[ a demo](https://www.gravitee.io/demo) to see Gravitee in action and talk to one of our API Management experts.
