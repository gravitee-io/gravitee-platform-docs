---
description: >-
  This article explores the additional features included in the enterprise
  Gravitee API Management solution.
---

# Gravitee APIM Enterprise Edition

## Introduction

Gravitee offers open source (OSS) and enterprise versions of its API Management (APIM) distribution package. This article introduces the additional features, capabilities, hosting options, and support options that are included in the Gravitee Enterprise Edition of API Management.​

{% hint style="info" %}
**Other Gravitee Products**

Gravitee's platform extends beyond just API Management. For information on enterprise versions of other products, please refer to our [platform overview documentation.](/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee)
{% endhint %}

## Enterprise APIM

The Gravitee APIM Enterprise Edition is available as three different packages, each offering a different level of access to enterprise features and capabilities. For more information, please refer to our [pricing page](https://www.gravitee.io/pricing).

### Enterprise features

{% hint style="warning" %}
The features below are included in the default enterprise API Management distribution and do not require additional enterprise plugins.
{% endhint %}

* **Enterprise OpenID Connect SSO:** Use OpenId Connect SSO with your API Management platform.
* [**Debug Mode**](docs/apim/4.2/guides/policy-studio/v2-api-policy-studio.md#debug-mode)**:** Easily test and debug your policy execution and enforcement.
* [**Audit trail**](../../guides/api-measurement-tracking-and-analytics/#the-audit-trail)**:** Audit the consumption and activity of your Gravitee APIs per event and type to monitor the behavior of your APIs and platform over time.
* [**DCR Registration**](docs/apim/4.2/guides/api-exposure-plans-applications-and-subscriptions/applications.md#dynamic-client-registration-provider): Dynamic client registration (DCR) is a protocol that allows OAuth client applications to register with an OAuth server through the OpenID Connect (OIDC) client registration endpoint.
* [**Custom Roles**](docs/apim/4.2/guides/administration/user-management-and-permissions.md#roles)**:** Create custom user roles to fit your needs. A role is a functional group of permissions and can be defined at the organization, environment, API, and/or application levels.
* [**Sharding Tags**](docs/apim/4.2/getting-started/configuration/the-gravitee-api-gateway/sharding-tags.md)**:** Specify which "shard" of the Gateway an API should be deployed to. By tagging Gateways with specific keywords, you can select the tag in the API's Deployments proxy settings to determine the Gateway where the API will be deployed.
* [**Bridge Gateway**](../../getting-started/hybrid-deployment/#bridge-gateways)**:** By default, an API Gateway must connect to a repository (mongoDB, Postgres) to retrieve the list of APIs to deploy, plans, API keys, and subscriptions. In the case of complex environments (network zones, different data centers, etc.), many teams prefer to avoid opening a connection between the database and something outside its network. The solution is to deploy a Bridge Gateway, which is a proxy for the repository (API GW > Bridge > Database). The sync will be done over HTTP instead of the database protocol.

## Enterprise plugins

The following packs consist of Gravitee Enterprise Edition plugins. These are not included in the default distribution and must be manually downloaded [here](https://download.gravitee.io/).&#x20;

EE plugins are installed from their respective repositories in GitHub. Gravitee’s EE plugin repositories are private and their names are prefixed as `gravitee-io/gravitee-policy-<plugin-name>`. For example, the Data Logging Masking policy repository is at `https://github.com/gravitee-io/gravitee-policy-data-logging-masking`.&#x20;

If you have not been granted access to private EE plugin repositories as part of your EE license request process, email [contact@graviteesource.com](mailto:contact@graviteesource.com).

Information on plugin deployment can be found [here](docs/apim/4.2/overview/plugins.md#deployment).

### Enterprise policy pack

The Enterprise policy pack includes policies that are typically necessary for enterprise-grade, production API Management deployments:

* [**Data logging masking**](docs/apim/4.2/reference/policy-reference/data-logging-masking.md)**:** If you enable logging on APIs, you can use the data logging masking policy to configure rules to conceal sensitive data.
* [**Assign metrics**](docs/apim/4.2/reference/policy-reference/assign-metrics.md)**:** Use the assign metrics policy to push extra metrics in addition to the natively provided request metrics. These metrics can be used for monetization invoices, analytics dashboards to create custom widgets, and, optionally, to apply aggregations based on their value.
* [**GeoIP filtering policy**](docs/apim/4.2/reference/policy-reference/geoip-filtering.md)**:** Use the GeoIP filtering policy to control access to your API by filtering IP addresses. You can allow IPs by country or distance.
* **GeoIP service:** Use the GeoIP service to load the GeoIP databases in memory. The GeoIP service is required to use the GeoIP filtering policy in APIM and for [Adaptive Multi-Factor Authentication in AM](https://documentation.gravitee.io/am).

### Legacy upgrade pack

The Legacy upgrade pack comprises the following plugins and capabilities that enable organizations to better migrate from and/or service legacy systems:

* [**XSLT policy plugin**](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/ZOkrVhrgwaygGUoFNHRF/\~/changes/1120/reference/policy-reference/template-policy-rework-structure-35): Use the XSLT policy to apply an XSL transformation to an incoming XML request body, or to the response body if your backend is exposing XML content.
* [**WebService security authentication**](docs/apim/4.2/reference/policy-reference/ws-security-authentication.md): Enables the client to send a SOAP envelope with WSS details, where the policy will validate and check the credentials (currently supports username and password).

### Observability pack

The Observability pack includes capabilities to better implement enterprise-grade API monitoring and observability:

* [**Datadog reporter**](../../getting-started/configuration/reporters/#datadog-reporter): Push API metrics to your Datadog instance and dashboards.
* [**TCP reporter**](../../getting-started/configuration/reporters/#tcp-reporter): Report Gateway events to a TCP listening server.

### Event-native pack

The Event-native pack includes capabilities that enable using Gravitee to expose, secure, and govern asynchronous APIs and event brokers:

* [**v4 message API entrypoints**](docs/apim/4.2/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md#step-2-entrypoints) enable consumers to access the Gateway and/or consume various message-based backend resources via
  * **HTTP GET**
  * **HTTP POST**
  * **WebSocket**
  * **Webhooks**
  * **Server-Sent Events (SSE)**
* [**v4 message API endpoints**](docs/apim/4.2/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md#introspect-messages-from-event-driven-backend-endpoints):
  * **Kafka/Confluent**: Allow the Gateway to open up a persistent connection and/or call a backend Kafka broker via a Kafka client set up by the Gravitee Gateway.
  * **MQTT**: Allow the Gateway to open up a persistent connection and/or call a backend MQTT broker, as long as that broker is running on MQTT 5.x, via an MQTT client set up by the Gravitee Gateway.
  * **RabbitMQ**: Allow the Gateway to open up a persistent connection and/or call a backend RabbitMQ broker, as long as that broker is running on AMQP 0-9-1.
  * **Solace**: Allow the Gateway to expose Solace resources and event APIs via your chosen Gravitee entrypoint(s).
* **CloudEvents policy**: Transform ingoing and outgoing data using the CloudEvents spec.
* [**Message filtering policy**:](docs/apim/4.2/reference/policy-reference/message-filtering.md) Filter messages streamed to clients/subscribers based on certain API publisher and/or client criteria.
* [**Avro <> JSON policy**](docs/apim/4.2/reference/policy-reference/avro-to-json.md): Transform information in Avro format into JSON format
* **Gateway message reactor plugin**: Enable the Gravitee Gateway to intercept and introspect messages when publishing and subscribing to/from message-based systems.
* [**Confluent Schema Registry resource**](docs/apim/4.2/guides/api-configuration/resources.md#confluent-schema-registry): Define Confluent Schema Registry as a resource for serialization and deserialization policies.

### Secret Manager pack

The Secret Manager pack includes generic, configurable, and autonomous clients that manage connections, retries, and credentials renewal when connecting to Secret Managers:

* **HashiCorp Vault**: Use the Key/Value engine of HC Vault to to avoid exposing plain text passwords and secrets keys.

## Advanced API monitoring

Not technically a part of the Access Management product, Gravitee offers a standalone, enterprise-grade API monitoring solution called Gravitee Alert Engine (AE). AE provides APIM and AM users with efficient and flexible API platform monitoring, including advanced alerting configurations and notifications sent through preferred channels, such as email, Slack and Webhooks. Alert Engine integrates with Gravitee APIM and AM to enable advanced alerting, new dashboards, etc. For more information, please refer to [the Alert Engine documentation](/ae/overview/introduction-to-gravitee-alert-engine).

## Advanced environment management

Gravitee APIM EE includes [Gravitee Cockpit](https://documentation.gravitee.io/gravitee-cloud), which you can use to register multiple APIM environments and installations. This allows you to manage environment hierarchies and promote APIs across higher and lower environments.

## Hosting options

An investment in Gravitee EE is an investment in deployment flexibility, and, optionally, the ability to offload costs associated with maintaining self-hosted API Management installations. Gravitee Enterprise supports:

* **Self-hosted deployments**: Install and host APIM within your own private cloud/environment.
* **Gravitee-managed deployments**: Gravitee hosts and manages all APIM components within its own cloud environment.
* **Hybrid deployment**: Gravitee hosts and manages some APIM components within its cloud environment while you manage others within your private cloud/environment.

For more information on each, please refer to our [APIM Architecture documentation](../apim-architecture/).

## Support options

Gravitee offers enterprise-grade support for enterprise customers, available in three different packages: Gold, Platinum, and Diamond. Each has different SLAs, benefits, etc. For more information, please [refer to our pricing page](https://www.gravitee.io/pricing).
