---
description: >-
  This article explores the additional features included in the enterprise
  Gravitee API Management solution.
---

# Enterprise Edition

## Introduction

Gravitee offers open source and enterprise versions of its API Management (APIM) distribution package. The Gravitee APIM Enterprise Edition requires a [license](../../../platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee/enterprise-edition-licensing.md). It is available as three different packages, each offering a different level of access to enterprise features and capabilities. For more information, please refer to our [pricing page](https://www.gravitee.io/pricing).

Refer to the sections below to learn about what's included in the Gravitee APIM Enterprise Edition:

* [Enterprise features](enterprise-edition.md#enterprise-features)
* [Enterprise plugins](enterprise-edition.md#enterprise-plugins)
* [Advanced API monitoring](enterprise-edition.md#advanced-api-monitoring)
* [Advanced environment management](enterprise-edition.md#advanced-environment-management)
* [Hosting options](enterprise-edition.md#hosting-options)

{% hint style="info" %}
Gravitee's platform extends beyond API Management. For information on enterprise versions of other products, please refer to the [platform overview](/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee).
{% endhint %}

## Enterprise features

{% hint style="warning" %}
The features below are included in the default enterprise APIM distribution.
{% endhint %}

<table><thead><tr><th width="214">Feature</th><th>Description</th></tr></thead><tbody><tr><td><strong>Audit Trail</strong></td><td>Audit the consumption and activity of your Gravitee APIs per event and type to monitor the behavior of your APIs and platform</td></tr><tr><td><strong>Bridge Gateway</strong></td><td>Deploy a Bridge Gateway, which is a proxy for a repository, to avoid opening a connection between a database and something outside its network. The sync occurs over HTTP instead of the database protocol.</td></tr><tr><td><strong>Custom roles</strong></td><td>Create custom user roles to fit your needs. A role is a functional group of permissions and can be defined at the organization, environment, API, and/or application level.</td></tr><tr><td><strong>DCR</strong></td><td>The dynamic client registration (DCR) protocol allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint</td></tr><tr><td><strong>Debug mode</strong></td><td>Easily test and debug your policy execution and enforcement</td></tr><tr><td><strong>Enterprise OpenID Connect SSO</strong></td><td>Use OpenId Connect SSO with your API Management platform</td></tr><tr><td><strong>Sharding tags</strong></td><td>Specify which "shard" of the Gateway an API should be deployed to. By tagging Gateways with specific keywords, you can select a tag in the API's proxy settings to control where the API will be deployed.</td></tr></tbody></table>

## Enterprise plugins

The following packs consist of Gravitee Enterprise Edition plugins. These are not included in the default distribution and must be manually downloaded [here](https://download.gravitee.io/).&#x20;

EE plugins are installed from their respective repositories in GitHub. Gravitee’s EE plugin repositories are private and their names are prefixed as:&#x20;

`gravitee-io/gravitee-policy-<plugin-name>`

For example, the Data Logging Masking policy repository is at `https://github.com/gravitee-io/gravitee-policy-data-logging-masking`.&#x20;

If you have not been granted access to private EE plugin repositories as part of your EE license request process, email [contact@graviteesource.com](mailto:contact@graviteesource.com). Information on plugin deployment can be found [here](../getting-started/plugins/deployment.md#deployment). Packs are described in more detail below.

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

* [**v4 message API entrypoints**](../create-apis/v4-api-creation-wizard.md#step-2-entrypoints)**:** Access the Gateway and/or consume various message-based backend resources via **HTTP GET**, **HTTP POST**, **Server-sent Events**, **Webhook**, and/or **WebSocket**
* [**v4 message API endpoints**](../create-apis/v4-api-creation-wizard.md#introspect-messages-from-event-driven-backend-endpoints)**:**
  * Allow the Gateway to open up a persistent connection and/or call a backend:
    * **Kafka** broker via a Kafka client
    * **MQTT** broker running on MQTT 5.x, via an MQTT client&#x20;
    * **RabbitMQ** broker running on AMQP 0-9-1
  * Allow the Gateway to expose **Solace** resources and event APIs via your Gravitee entrypoint(s)
* **CloudEvents policy**: Transform ingoing and outgoing data using the CloudEvents spec.
* **Message Filtering policy:** Filter messages streamed to clients/subscribers based on API publisher and/or client criteria.
* **AVRO to JSON policy:** Transform information from Avro format to JSON format.
* **Gateway message reactor plugin:** Enable the Gravitee Gateway to intercept and introspect messages when publishing and subscribing to/from message-based systems.
* [**Confluent Schema Registry resource**](../policies/resources.md#confluent-schema-registry)**:** Define Confluent Schema Registry as a resource for serialization and deserialization policies.

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

* [**Datadog reporter**](../gravitee-gateway/reporters/datadog-reporter.md#datadog-reporter): Push API metrics to your Datadog instance and dashboards.
* [**TCP reporter**](../gravitee-gateway/reporters/tcp-reporter.md#tcp-reporter): Report Gateway events to a TCP listening server.

</details>

<details>

<summary>Secret Manager pack</summary>

The Secret Manager pack includes generic, configurable, and autonomous clients that manage connections, retries, and credentials renewal when connecting to Secret Managers:

* **HashiCorp Vault**: Use the Key/Value engine of HC Vault to to avoid exposing plain text passwords and secrets keys.

</details>

## Advanced API monitoring

Not technically a part of the Access Management product, Gravitee offers a standalone, enterprise-grade API monitoring solution called Gravitee Alert Engine (AE). AE provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configurations and notifications sent through preferred channels such as email, Slack and Webhooks. Alert Engine integrates with Gravitee APIM and AM to enable advanced alerting, new dashboards, etc. For more information, please refer to [the Alert Engine documentation](/ae/overview/introduction-to-gravitee-alert-engine).

## Advanced environment management

Gravitee APIM EE includes [Gravitee C](../../../gravitee-cloud/README.md)[loud](../../../gravitee-cloud/README.md), used to register multiple APIM environments and installations. This allows you to manage environment hierarchies and promote APIs across higher and lower environments.

## Hosting options

Gravitee EE is an investment in deployment flexibility, and, optionally, the ability to offload costs associated with maintaining self-hosted APIM installations. Gravitee EE supports:

* **Self-hosted deployments**: Install and host APIM within your own private cloud/environment.
* **Gravitee-managed deployments**: Gravitee hosts and manages all APIM components within its own cloud environment.
* **Hybrid deployment**: Gravitee hosts and manages some APIM components within its cloud environment while you manage others within your private cloud/environment.

For more information on each, please refer to our [Architecture](architecture.md) documentation.
