# APIM Enterprise Edition

## Overview

Gravitee offers both an open source (OSS) and Enterprise Edition (EE) version of its API Management (APIM) distribution package. The Gravitee APIM Enterprise Edition requires a [license](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing). It is available as three different packages, each offering a different level of access to enterprise features and capabilities. For more information, please refer to our [pricing page](https://www.gravitee.io/pricing).

{% hint style="info" %}
Gravitee's platform extends beyond API Management. For information on enterprise versions of other products, please refer to the [platform overview](https://documentation.gravitee.io/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee).
{% endhint %}

## Enterprise features

{% hint style="warning" %}
The features below are included in the default enterprise APIM distribution.
{% endhint %}

<table><thead><tr><th width="214">Feature</th><th>Description</th></tr></thead><tbody><tr><td><strong>Audit Trail</strong></td><td>Audit the consumption and activity of your Gravitee APIs per event and type to monitor the behavior of your APIs and platform</td></tr><tr><td><strong>Bridge Gateway</strong></td><td>Deploy a Bridge Gateway, which is a proxy for a repository, to avoid opening a connection between a database and something outside its network. The sync occurs over HTTP instead of the database protocol.</td></tr><tr><td><strong>Custom roles</strong></td><td>Create custom user roles to fit your needs. A role is a functional group of permissions and can be defined at the organization, environment, API, and/or application level.</td></tr><tr><td><strong>DCR</strong></td><td>The dynamic client registration (DCR) protocol allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint</td></tr><tr><td><strong>Debug mode</strong></td><td>Easily test and debug your policy execution and enforcement</td></tr><tr><td><strong>Enterprise OpenID Connect SSO</strong></td><td>Use OpenId Connect SSO with your API Management platform</td></tr><tr><td><strong>Sharding tags</strong></td><td>Specify which "shard" of the Gateway an API should be deployed to. By tagging Gateways with specific keywords, you can select a tag in the API's proxy settings to control where the API will be deployed.</td></tr></tbody></table>

## Enterprise plugins

Gravitee Enterprise Edition plugins are not included in the default EE APIM distribution. They are available à la carte and can be downloaded from [https://download.gravitee.io/#graviteeio-ee/apim/plugins/](https://download.gravitee.io/#graviteeio-ee/apim/plugins/).&#x20;

Gravitee offers several different types of plugins. Here are the EE plugins available for download, organized by type:

### Endpoints

* [Agent to Agent](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-agent-to-agent/)
* [AI Agent](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-ai-agent/)
* [Azure Service Bus](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-azure-service-bus/)
* [Kafka](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-kafka/)
* [MQTT5 Advanced](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-mqtt5-advanced/)
* [MQTT5](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-mqtt5/)
* [Native Kafka](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-native-kafka/)
* [RabbitMQ](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-rabbitmq/)
* [Solace](https://download.gravitee.io/#graviteeio-ee/apim/plugins/endpoints/gravitee-endpoint-solace/)

### Entrypoints

* [Agent to Agent](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-agent-to-agent/)
* [HTTP GET](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-http-get/)
* [HTTP POST](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-http-post/)
* [Native Kafka](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-native-kafka/)
* [SSE Advanced](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-sse-advanced/)
* [SSE](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-sse/)
* [Webhook Advanced](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-webhook-advanced/)
* [Webhook](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-webhook/)
* [WebSocket](https://download.gravitee.io/#graviteeio-ee/apim/plugins/entrypoints/gravitee-entrypoint-websocket/)

### Policies

* [Assign Metrics](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-assign-metrics/)
* [Cloud Events](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-cloud-events/)
* [Data Cache](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-data-cache/)
* [Data Logging Masking](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-data-logging-masking/)
* [GeoIP Filtering](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-geoip-filtering/)
* [InterOps A IdP](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-interops-a-idp/)
* [InterOps A SP](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-interops-a-sp/)
* [InterOps R IdP](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-interops-r-idp/)
* [InterOps R SP](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-interops-r-sp/)
* [Kafka ACL](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-acl/)
* [Kafka Message Filtering](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-message-filtering/)
* [Kafka Offloading](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-offloading/)
* [Kafka Quota](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-quota/)
* [Kafka Topic Mapping](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-topic-mapping/)
* [Kafka Transform Key](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-kafka-transform-key/)
* [Transform AVRO to JSON](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-transform-avro-json/)
* [Transform AVRO to Protobuf](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-transform-avro-protobuf/)
* [Transform Protobuf to JSON](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-transform-protobuf-json/)
* [WS Security Authentication](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-wssecurity-authentication/)
* [XSLT](https://download.gravitee.io/#graviteeio-ee/apim/plugins/policies/gravitee-policy-xslt/)

### Reactors

* [Message](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reactors/gravitee-reactor-message/)
* [Native Kafka](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reactors/gravitee-reactor-native-kafka/)

### Reporters

* [Cloud](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-cloud/)
* [Datadog](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-datadog/)
* [TCP](https://download.gravitee.io/#graviteeio-ee/apim/plugins/reporters/gravitee-reporter-tcp/)

### Repositories

* [Bridge HTTP Client](https://download.gravitee.io/#graviteeio-ee/apim/plugins/repositories/gravitee-apim-repository-bridge-http-client/)
* [Bridge HTTP Server](https://download.gravitee.io/#graviteeio-ee/apim/plugins/repositories/gravitee-apim-repository-bridge-http-server/)

### Resources

* [Schema Registry Confluent](https://download.gravitee.io/#graviteeio-ee/apim/plugins/resources/gravitee-resource-schema-registry-confluent/)

For more information on plugins and how to deploy them, see [plugins](../plugins/ "mention"). Enterprise plugin packs are described in detail below.

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
    * **MQTT** broker running on MQTT 5.x, via an MQTT client&#x20;
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

* [**Datadog reporter**](../analyze-and-monitor-apis/reporters/#datadog-reporter): Push API metrics to your Datadog instance and dashboards.
* [**TCP reporter**](../analyze-and-monitor-apis/reporters/#tcp-reporter): Report Gateway events to a TCP listening server.

</details>

<details>

<summary>Secret Manager pack</summary>

The Secret Manager pack includes generic, configurable, and autonomous clients that manage connections, retries, and credentials renewal when connecting to Secret Managers:

* **HashiCorp Vault**: Use the Key/Value engine of HC Vault to to avoid exposing plain text passwords and secrets keys.

</details>

## Gravitee Alert Engine

Gravitee offers a standalone, enterprise-grade API monitoring solution called Alert Engine (AE). AE provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configurations and notifications sent through preferred channels such as email, Slack and Webhooks. Alert Engine integrates with Gravitee APIM and AM to enable advanced alerting, new dashboards, etc. For more information, please refer to [the Alert Engine documentation](https://documentation.gravitee.io/ae/overview/introduction-to-gravitee-alert-engine).

## Gravitee Cloud

Gravitee APIM EE includes [Gravitee C](https://documentation.gravitee.io/gravitee-cloud)[loud](https://documentation.gravitee.io/gravitee-cloud). Gravitee Cloud lets you register multiple APIM environments and installations, manage environment hierarchies, and promote APIs across higher and lower environments.

## Hosting options

Gravitee EE gives you deployment flexibility. Optionally, you can offload costs associated with maintaining self-hosted APIM installations. Gravitee EE supports the following types of deployments:

* **Self-hosted deployments**: Install and host APIM within your own private cloud/environment.
* **Gravitee-managed deployments**: Gravitee hosts and manages all APIM components within its own cloud environment.
* **Hybrid deployments**: Gravitee hosts and manages some APIM components within its cloud environment while you manage others within your private cloud/environment.
