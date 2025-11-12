---
description: >-
  This article explores the additional features included in the enterprise
  Gravitee API Management solution.
---

# Gravitee APIM Enterprise Edition

## Introduction

Gravitee offers open source and enterprise versions of its API Management (APIM) distribution package. The Gravitee APIM Enterprise Edition is available as three different packages, each offering a different level of access to enterprise features and capabilities. For more information, please refer to our [pricing page](https://www.gravitee.io/pricing).

Refer to the sections below to learn about what's included in the Gravitee APIM Enterprise Edition:

* [Enterprise features](./#enterprise-features)
* [Enterprise plugins](./#enterprise-plugins)
* [Advanced API monitoring](./#advanced-api-monitoring)
* [Advanced environment management](./#advanced-environment-management)
* [Hosting options](./#hosting-options)

{% hint style="info" %}
Gravitee's platform extends beyond API Management. For information on enterprise versions of other products, please refer to the [platform overview](https://documentation.gravitee.io/platform-overview/gravitee-platform/gravitee-offerings-ce-vs-ee).
{% endhint %}

## Enterprise features

{% hint style="warning" %}
The features below are included in the default enterprise APIM distribution.
{% endhint %}

<table><thead><tr><th width="214">Feature</th><th>Description</th></tr></thead><tbody><tr><td><a href="../../guides/api-measurement-tracking-and-analytics/audit-trail.md"><strong>Audit Trail</strong></a></td><td>Audit the consumption and activity of your Gravitee APIs per event and type to monitor the behavior of your APIs and platform</td></tr><tr><td><a href="../../getting-started/install-and-upgrade-guides/hybrid-deployment/#bridge-gateways"><strong>Bridge Gateway</strong></a></td><td>Deploy a Bridge Gateway, which is a proxy for a repository, to avoid opening a connection between a database and something outside its network. The sync occurs over HTTP instead of the database protocol.</td></tr><tr><td><a href="../../guides/administration/user-management-and-permissions.md#roles"><strong>Custom roles</strong></a></td><td>Create custom user roles to fit your needs. A role is a functional group of permissions and can be defined at the organization, environment, API, and/or application level.</td></tr><tr><td><a href="../../guides/api-exposure-plans-applications-and-subscriptions/applications.md#dynamic-client-registration-provider"><strong>DCR</strong></a></td><td>The dynamic client registration (DCR) protocol allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint</td></tr><tr><td><a href="../../guides/policy-studio/v2-api-policy-studio.md#debug-mode"><strong>Debug mode</strong></a></td><td>Easily test and debug your policy execution and enforcement</td></tr><tr><td><strong>Enterprise OpenID Connect SSO</strong></td><td>Use OpenId Connect SSO with your API Management platform</td></tr><tr><td><a href="../../getting-started/configuration/apim-gateway/sharding-tags.md"><strong>Sharding tags</strong></a></td><td>Specify which "shard" of the Gateway an API should be deployed to. By tagging Gateways with specific keywords, you can select a tag in the API's proxy settings to control where the API will be deployed.</td></tr></tbody></table>

## Enterprise plugins

The following packs consist of Gravitee Enterprise Edition plugins. These are not included in the default distribution and must be manually downloaded [here](https://download.gravitee.io/).&#x20;

EE plugins are installed from their respective repositories in GitHub. Gravitee’s EE plugin repositories are private and their names are prefixed as:&#x20;

`gravitee-io/gravitee-policy-<plugin-name>`

For example, the Data Logging Masking policy repository is at `https://github.com/gravitee-io/gravitee-policy-data-logging-masking`.&#x20;

If you have not been granted access to private EE plugin repositories as part of your EE license request process, email [contact@graviteesource.com](mailto:contact@graviteesource.com). Information on plugin deployment can be found [here](../plugins.md#deployment). Packs are described in more detail below.

<details>

<summary>Enterprise Policy pack</summary>

The Enterprise Policy pack includes policies that are typically necessary for enterprise-grade, production API Management deployments:

* [**Data logging masking**](../../reference/policy-reference/data-logging-masking.md)**:** If you enable logging on APIs, you can use this policy to configure rules to conceal sensitive data.
* [**Assign metrics**](../../reference/policy-reference/assign-metrics.md)**:** Push metrics in addition to the natively provided request metrics. These metrics can be used for analytics dashboards to create custom widgets, monetization invoices, and, optionally, to apply aggregations based on their value.
* [**GeoIP filtering policy**](../../reference/policy-reference/geoip-filtering.md)**:** Control access to your API by filtering IP addresses. You can allow IPs by country or distance.
* **GeoIP service:** Load GeoIP databases in memory. The GeoIP service is required to use the GeoIP filtering policy in APIM and for [Adaptive Multi-Factor Authentication in AM](https://documentation.gravitee.io/am).

</details>

<details>

<summary>Event-native pack</summary>

The Event-native pack includes capabilities that enable Gravitee to expose, secure, and govern asynchronous APIs and event brokers:

* [**v4 message API entrypoints**](../../guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md#step-2-entrypoints)**:** Access the Gateway and/or consume various message-based backend resources via **HTTP GET**, **HTTP POST**, **Server-sent Events**, **Webhook**, and/or **WebSocket**
* [**v4 message API endpoints**](../../guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md#introspect-messages-from-event-driven-backend-endpoints)&#x20;
  * Allow the Gateway to open up a persistent connection and/or call a backend:
    * **Kafka** broker via a Kafka client
    * **MQTT** broker running on MQTT 5.x, via an MQTT client&#x20;
    * **RabbitMQ** broker running on AMQP 0-9-1
  * Allow the Gateway to expose **Solace** resources and event APIs via your Gravitee entrypoint(s)
* **CloudEvents policy**: Transform ingoing and outgoing data using the CloudEvents spec.
* [**Message Filtering policy**](../../reference/policy-reference/message-filtering.md)**:** Filter messages streamed to clients/subscribers based on API publisher and/or client criteria.
* [**Avro to JSON policy**](../../reference/policy-reference/avro-to-json.md)**:** Transform information from Avro format to JSON format.
* **Gateway message reactor plugin:** Enable the Gravitee Gateway to intercept and introspect messages when publishing and subscribing to/from message-based systems.
* [**Confluent Schema Registry resource**](../../guides/api-configuration/resources.md#confluent-schema-registry)**:** Define Confluent Schema Registry as a resource for serialization and deserialization policies.

</details>

<details>

<summary>Legacy Upgrade pack</summary>

The Legacy Upgrade pack comprises the following plugins and capabilities to enable organizations to better migrate from and/or service legacy systems:

* [**XSLT policy**](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/ZOkrVhrgwaygGUoFNHRF/\~/changes/1120/reference/policy-reference/template-policy-rework-structure-35)**:** Apply an XSL transformation to an incoming XML request body, or to the response body if your backend is exposing XML content.
* [**WebService Security Authentication policy**](../../reference/policy-reference/ws-security-authentication.md)**:** Enables the client to send a SOAP envelope with WSS details, where the policy validates credentials (currently supports username and password).

</details>

<details>

<summary>Observability pack</summary>

The Observability pack includes capabilities to better implement enterprise-grade API monitoring and observability:

* [**Datadog reporter**](../../getting-started/configuration/reporters/#datadog-reporter): Push API metrics to your Datadog instance and dashboards.
* [**TCP reporter**](../../getting-started/configuration/reporters/#tcp-reporter): Report Gateway events to a TCP listening server.

</details>

<details>

<summary>Secret Manager pack</summary>

The Secret Manager pack includes generic, configurable, and autonomous clients that manage connections, retries, and credentials renewal when connecting to Secret Managers:

* **HashiCorp Vault**: Use the Key/Value engine of HC Vault to to avoid exposing plain text passwords and secrets keys.

</details>

## Advanced API monitoring

Not technically a part of the Access Management product, Gravitee offers a standalone, enterprise-grade API monitoring solution called Gravitee Alert Engine (AE). AE provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configurations and notifications sent through preferred channels such as email, Slack and Webhooks. Alert Engine integrates with Gravitee APIM and AM to enable advanced alerting, new dashboards, etc. For more information, please refer to [the Alert Engine documentation](https://documentation.gravitee.io/alert-engine).

## Advanced environment management

Gravitee APIM EE includes [Gravitee Cockpit](https://documentation.gravitee.io/gravitee-cloud), used to register multiple APIM environments and installations. This allows you to manage environment hierarchies and promote APIs across higher and lower environments.

## Hosting options

Gravitee EE is an investment in deployment flexibility, and, optionally, the ability to offload costs associated with maintaining self-hosted APIM installations. Gravitee EE supports:

* **Self-hosted deployments**: Install and host APIM within your own private cloud/environment.
* **Gravitee-managed deployments**: Gravitee hosts and manages all APIM components within its own cloud environment.
* **Hybrid deployment**: Gravitee hosts and manages some APIM components within its cloud environment while you manage others within your private cloud/environment.

For more information on each, please refer to our [APIM Architecture documentation](../apim-architecture/).
