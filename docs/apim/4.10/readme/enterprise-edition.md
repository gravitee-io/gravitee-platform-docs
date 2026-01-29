---
description: An overview about enterprise edition.
metaLinks:
  alternates:
    - enterprise-edition.md
---

# Enterprise Edition

## Overview

Gravitee offers both an open source (OSS) and Enterprise Edition (EE) version of its API Management (APIM) distribution package. The Gravitee APIM Enterprise Edition requires a [license](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing). It is available as three different packages, each offering a different level of access to enterprise features and capabilities. For more information, please refer to our [pricing page](https://www.gravitee.io/pricing).

{% hint style="info" %}
Gravitee's platform extends beyond API Management. For information on enterprise versions of other products, please refer to the [platform overview](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee).
{% endhint %}

## Enterprise features

{% hint style="warning" %}
The features below are included in the default enterprise APIM distribution.
{% endhint %}

<table><thead><tr><th width="214">Feature</th><th>Description</th></tr></thead><tbody><tr><td><strong>Audit Trail</strong></td><td>Audit the consumption and activity of your Gravitee APIs per event and type to monitor the behavior of your APIs and platform</td></tr><tr><td><strong>Bridge Gateway</strong></td><td>Deploy a Bridge Gateway, which is a proxy for a repository, to avoid opening a connection between a database and something outside its network. The sync occurs over HTTP instead of the database protocol.</td></tr><tr><td><strong>Custom roles</strong></td><td>Create custom user roles to fit your needs. A role is a functional group of permissions and can be defined at the organization, environment, API, and/or application level.</td></tr><tr><td><strong>DCR</strong></td><td>The dynamic client registration (DCR) protocol allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint</td></tr><tr><td><strong>Debug mode</strong></td><td>Easily test and debug your policy execution and enforcement</td></tr><tr><td><strong>Enterprise OpenID Connect SSO</strong></td><td>Use OpenId Connect SSO with your API Management platform</td></tr><tr><td><strong>Sharding tags</strong></td><td>Specify which "shard" of the Gateway an API should be deployed to. By tagging Gateways with specific keywords, you can select a tag in the API's proxy settings to control where the API will be deployed.</td></tr></tbody></table>

## Enterprise plugins

Gravitee Enterprise Edition plugins are not included in the default EE APIM distribution. They are available à la carte and can be downloaded from [https://download.gravitee.io/#graviteeio-ee/apim/plugins/](https://download.gravitee.io/#graviteeio-ee/apim/plugins/).

Gravitee offers several different types of plugins. Here are the EE plugins available for download, organized by type:

### Endpoints

* [Agent to Agent](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-agent-to-agent/): Supports Google’s Agent-to-Agent (A2A) protocol. To simplify communication, it uses SSE, HTTP GET, or HTTP POST methods in compliance with evolving A2A specifications.
* [Azure Service Bus](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-azure-service-bus/): Uses HTTP and WebSocket to publish and subscribe to events in Azure Service Bus. The Gateway mediates the protocol between the client and the backend.
* [Kafka](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-kafka/): Uses HTTP and WebSocket to publish and subscribe to events in Kafka. The Gateway mediates the protocol between the client and the backend.
* [MQTT5](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-mqtt5/): Lets you subscribe or publish messages to a MQTT 5.x broker such as HiveMQ or Mosquitto.
* [Native Kafka](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-native-kafka/): Lets you subscribe or publish messages to a Kafka broker using the native Kafka protocol.
* [RabbitMQ](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-rabbitmq/): Communicates with a RabbitMQ resource using the AMQP 0-9-1 protocol.
* [Solace](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-solace/): Lets you subscribe or publish messages to a Solace broker. Only SMF protocol is supported.

### Entrypoints

* [Agent to Agent](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-agent-to-agent/): Supports Google’s Agent-to-Agent (A2A) protocol. To simplify communication, it uses SSE, HTTP GET, or HTTP POST methods in compliance with evolving A2A specifications.
* [HTTP GET](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-http-get/): Fronts a backend or data source with a Gateway REST API that supports the HTTP GET request.
* [HTTP POST](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-http-post/): Fronts a backend or data source with a Gateway REST API that supports the HTTP POST request.
* [Native Kafka](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-native-kafka/): Lets you subscribe or publish messages to a Kafka broker using the native Kafka protocol.
* [SSE](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-sse/): Fronts a backend or data source with a Gateway SSE API for unidirectional communication between server and client.
* [Webhook](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-webhook/): Lets you subscribe to the Gravitee Gateway using Webhook and then retrieve streamed data in real-time over a Webhook callback URL.
* [WebSocket](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-websocket/): Lets you send and retrieve streamed events and messages in real-time using the WebSocket protocol.

### Policies

* [Assign Metrics](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-assign-metrics/): Pushes extra metrics in addition to the natively provided request metrics.
* [Cloud Events](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-cloud-events/): Creates a cloud-events JSON object from messages.
* [Data Cache](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-data-cache/): Lets you get, set, and expire arbitrary key-value pairs in a cache resource.
* [Data Logging Masking](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-data-logging-masking/): Lets you configure rules to conceal sensitive data.
* [GeoIP Filtering](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-geoip-filtering/): Lets you control access to your API by filtering IP addresses. You can allow IPs by country or distance.
* [Kafka ACL](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-acl/): Lets you define [ACLs](https://kafka.apache.org/documentation/#security_authz) on cluster resources that are proxied by the Gateway.
* [Kafka Offloading](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-offloading/): Lets you configure how Kafka message content is offloaded to storage. You have the option to activate message offloading based on the content size of the message.
* [Kafka Quota](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-quota/): Enforces quotas on Kafka messages. It lets you limit the amount of data that can be produced or consumed by a Kafka client.
* [Kafka Topic Mapping](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-topic-mapping/): Lets you map one topic to another so that the Kafka client can use a topic name that is different from the topic name used in the Kafka broker.
* [Kafka Transform Key](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-transform-key/): Adds a custom Kafka message key to your messages so that you can customize partitioning and perform general actions, such as ordering transactions.
* [Transform AVRO to JSON](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-transform-avro-json/): Applies an AVRO to JSON transformation, or mapping, on the request, response, and/or message content.
* [Transform AVRO to Protobuf](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-transform-avro-protobuf/): Applies an AVRO to Protobuf transformation, or mapping, on the request, response, and/or message content.
* [Transform Protobuf to JSON](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-transform-protobuf-json/): Applies a Protobuf to JSON transformation, or mapping, on the request, response, and/or message content.
* [WS Security Authentication](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-wssecurity-authentication/): Lets you manage the security of SOAP API calls.
* [XSLT](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-xslt/): Applies an XSL transformation to an incoming XML request body, or to the response body if your backend is exposing XML content.

### Reactors

* [Message](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reactors/gravitee-reactor-message/): Externalizes all event-native Gateway capabilities related to messages.
* [Native Kafka](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reactors/gravitee-reactor-native-kafka/): Externalizes all Kafka Gateway capabilities to handle APIs dealing with the native Kafka protocol.

### Reporters

* [Cloud](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-cloud/): Exposes a secure endpoint for analytics propagated from either a SaaS or self-hosted Gravitee Gateway to Elastic storage.
* [Datadog](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-datadog/): Sends Gateway reporting data to a Datadog server for analysis and tracking.
* [TCP](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-tcp/): Pushes Gravitee Gateway metrics to a TCP server. You can select from several output formats and filter on or rename fields.

### Repositories

* [Bridge HTTP Client](https://download.gravitee.io/#graviteeio-ee/apim/plugins/repositories/gravitee-apim-repository-bridge-http-client/): Deployed into the API Gateway and used by the sync process to load data. For example, APIs, Subscriptions, and ApiKeys.
* [Bridge HTTP Server](https://download.gravitee.io/#graviteeio-ee/apim/plugins/repositories/gravitee-apim-repository-bridge-http-server/): Exposes the Bridge Rest API and communicates with your database. It should be deployed on the same VPC / network zone as the database.

### Resources

* [Schema Registry Confluent](https://download.gravitee.io/#graviteeio-ee/apim/plugins/resources/gravitee-resource-schema-registry-confluent/): Lets you retrieve serialization/deserialization schema from a Confluent schema registry.

For more information on plugins and how to deploy them, see [plugins](../plugins/ "mention").

### Enterprise plugin packs

Enterprise plugin packs are described in detail below.

<details>

<summary>Enterprise Policy pack</summary>

The Enterprise Policy pack includes policies that are typically necessary for enterprise-grade, production API Management deployments:

* **Data Logging Masking:** If you enable logging on APIs, you can use this policy to configure rules to conceal sensitive data.
* **Assign Metrics:** Push metrics in addition to the natively provided request metrics. These metrics can be used for analytics dashboards to create custom widgets, monetization invoices, and, optionally, to apply aggregations based on their value.
* **GeoIP Filtering:** Control access to your API by filtering IP addresses. You can allow IPs by country or distance.
* **GeoIP service:** Load GeoIP databases in memory. The GeoIP service is required to use the GeoIP Filtering policy in APIM and for [Adaptive Multi-Factor Authentication in AM](https://documentation.gravitee.io/am).

</details>

<details>

<summary>Event-native pack</summary>

The Event-native pack includes capabilities that enable Gravitee to expose, secure, and govern asynchronous APIs and event brokers:

* [**v4 message API entrypoints**](../create-and-configure-apis/create-apis/v4-api-creation-wizard.md#step-2-entrypoints)**:** Access the Gateway and/or consume various message-based backend resources via **HTTP GET**, **HTTP POST**, **Server-sent Events**, **Webhook**, and/or **WebSocket**
* [**v4 message API endpoints**](../create-and-configure-apis/create-apis/v4-api-creation-wizard.md#introspect-messages-from-event-driven-backend-endpoints)**:**
  * Allow the Gateway to open up a persistent connection and/or call a backend:
    * **Kafka** broker via a Kafka client
    * **MQTT** broker running on MQTT 5.x, via an MQTT client
    * **RabbitMQ** broker running on AMQP 0-9-1
  * Allow the Gateway to expose **Solace** resources and event APIs via your Gravitee entrypoint(s)
* **CloudEvents policy**: Transform ingoing and outgoing data using the CloudEvents spec.
* **Message Filtering policy:** Filter messages streamed to clients/subscribers based on API publisher and/or client criteria.
* **AVRO to JSON policy:** Transform information from Avro format to JSON format.
* **Gateway message reactor plugin:** Enable the Gravitee Gateway to intercept and introspect messages when publishing and subscribing to/from message-based systems.
* [**Confluent Schema Registry resource**](../create-and-configure-apis/apply-policies/resources.md#confluent-schema-registry)**:** Define Confluent Schema Registry as a resource for serialization and deserialization policies.

</details>

<details>

<summary>Legacy Upgrade pack</summary>

The Legacy Upgrade pack comprises the following plugins and capabilities to enable organizations to better migrate from and/or service legacy systems:

* **XSLT policy:** Apply an XSL transformation to an incoming XML request body, or to the response body if your backend is exposing XML content.
* **WS Security Authentication policy:** Enables the client to send a SOAP envelope with WSS details, where the policy validates credentials (currently supports username and password).

</details>

<details>

<summary>Observability pack</summary>

The Observability pack includes capabilities to better implement enterprise-grade API monitoring and observability:

* [**Datadog reporter**](../analyze-and-monitor-apis/reporters/datadog-reporter.md#datadog-reporter): Push API metrics to your Datadog instance and dashboards.
* [**TCP reporter**](../analyze-and-monitor-apis/reporters/tcp-reporter.md#tcp-reporter): Report Gateway events to a TCP listening server.

</details>

<details>

<summary>Secret Manager pack</summary>

The Secret Manager pack includes generic, configurable, and autonomous clients that manage connections, retries, and credentials renewal when connecting to Secret Managers:

* **HashiCorp Vault**: Use the Key/Value engine of HC Vault to to avoid exposing plain text passwords and secrets keys.

</details>

## Gravitee Alert Engine

Gravitee offers a standalone, enterprise-grade API monitoring solution called Alert Engine (AE). AE provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configurations and notifications sent through preferred channels such as email, Slack and Webhooks. Alert Engine integrates with Gravitee APIM and AM to enable advanced alerting, new dashboards, etc. For more information, please refer to [the Alert Engine documentation](https://documentation.gravitee.io/alert-engine).

## Gravitee Cloud

Gravitee APIM EE includes [Gravitee Cloud](https://documentation.gravitee.io/gravitee-cloud). Gravitee Cloud lets you register multiple APIM environments and installations, manage environment hierarchies, and promote APIs across higher and lower environments.

## Hosting options

Gravitee EE gives you deployment flexibility. Optionally, you can offload costs associated with maintaining self-hosted APIM installations. Gravitee EE supports the following types of deployments:

* **Self-hosted deployments**: Install and host APIM within your own private cloud/environment.
* **Gravitee-managed deployments**: Gravitee hosts and manages all APIM components within its own cloud environment.
* **Hybrid deployments**: Gravitee hosts and manages some APIM components within its cloud environment while you manage others within your private cloud/environment.
