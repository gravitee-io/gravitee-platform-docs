---
description: This article covers the new features released in Gravitee API Management 4.2
---

# APIM 4.2

{% hint style="danger" %}
**Make sure you upgrade your license file**

If you are an existing Gravitee Enterprise customer upgrading to 4.x, please make sure that you upgrade your Gravitee license file. Reach out to your Customer Success Manager or Support team in order to receive a new 4.x license.
{% endhint %}

## Introduction

Gravitee 4.2 was released on December 21st, 2023, and introduced secret provider plugins, API documentation, enhanced API-level logging capabilities, multi-tenancy, TCP proxy APIs, GKO support for v4 APIs, entrypoint/endpoint enhancements, and policy improvements. For a pared-down version of what was released, please see the [changelog for Gravitee APIM 4.2](../changelog/apim-4.2.x.md).

## Secret providers

Gravitee 4.2 offers a set of `secret-provider` plugins that enable Secret Managers to configure Gravitee API Management and Access Management. Secret providers are generic, configurable, and autonomous clients used to:

* Extend the operable range Secret Managers to resolve and watch secrets
* Retrieve sensitive information (passwords, x509 pairs, etc.) from Secret Managers to ensure this information does not appear in clear text
* Manage connections, retries, and credentials renewal when connecting to Secret Managers.&#x20;

Two `secret-provider` plugins are available for Gravitee Gateway, Management API, and Access Management:

* `kubernetes`: A Community Edition plugin that fetches secret and TLS pairs from Kubernetes.io
* `vault`: An Enterprise Edition plugin that uses the Key/Value engine of HashiCorp Vault

For more information, refer to [Secret Providers](../../getting-started/configuration/secret-providers.md).

## API Documentation

The Management Console now includes the [API Documentation](../../guides/api-configuration/v4-api-configuration/documentation.md) capability to introduce consumers to an API and provide instructions for how to use it.&#x20;

Folders can be added to organize the documentation structure, and pages of Markdown content can be created in any directory. You can choose the visibility of each folder and page:

* **Public** entries are visible by anyone browsing the Developer Portal
* **Private** entries are only visible to authenticated users

The Documentation feature includes **Actions** associated with each folder or page entry to edit, delete, publish/unpublish, or reorder content.

<figure><img src="../../.gitbook/assets/docs_editing.png" alt=""><figcaption></figcaption></figure>

When published, documentation is accessible via the Developer Portal.

<figure><img src="../../.gitbook/assets/docs_dev portal docs (1).png" alt=""><figcaption></figcaption></figure>

## Logging

[API-level logging](broken-reference) is now supported for both v4 proxy APIs and v4 message APIs. Logging options can be configured in the Management Console and include the ability to record data based on content and whether information is associated with an entrypoint, endpoint, request, and/or response.&#x20;

Message-level logging also offers message sampling, which can be configured either in the Console or via `gravitee.yaml`. The `gravitee.yaml` file's `messageSampling` configuration option determines, for each message sampling method, whether it can be used, its default value, and its max value.&#x20;

By configuring the API logging methods, a Gravitee administrator can restrict the type of message sampling in use and control the pressure it puts on the Gateway, and Gravitee can restrict the type and scale of sampling used in cloud environments.

## Multi-tenancy

Gravitee 4.2 upgrades to APIM and Cockpit implement support for [multi-tenancy](../../getting-started/install-and-upgrade-guides/multi-tenancy.md). In Gravitee, a multi-tenant configuration is defined as a single APIM installation connected to multiple Cockpit Organizations and Environments, where features and data are isolated between tenants and dedicated URLs are used to access the APIM components and APIs deployed on Gravitee Gateways.&#x20;

<figure><img src="https://slabstatic.com/prod/uploads/6lql0jy7/posts/images/mNhfcqTUgEOXngJNcAcdIf1o.png" alt=""><figcaption><p>Typical multitenant setup</p></figcaption></figure>

Multi-tenancy is an enterprise capability that requires an APIM installation in multi-tenant mode to be connected to an [enterprise-enabled Gravitee Cockpit account](https://documentation.gravitee.io/platform-overview/gravitee-essentials/gravitee-offerings-ce-vs-ee#enterprise-version-of-gravitee-cockpit). In addition, the Access Points feature must be enabled for tenants to use dedicated URLs to access the resources of a shared installation.

Although multi-tenancy support necessitated changes to both APIM and Cockpit, customer deployments may continue to function as standalone (not multi-tenant) APIM installations. Please note that once a multi-tenant APIM is connected to Cockpit, it is not possible to disable multi-tenancy mode in APIM.

## TCP proxy support

Gravitee now supports TCP proxy APIs to provide the lowest latency access to raw backend data. Gravitee can proxy messages from any REST endpoint or event system with an available IP address that accepts TCP socket clients. This enables the Gateway to transmit formats not commonly available to the standard API consumer (video streams, HL7, IoT protocols, etc.) as TCP packets. Gravitee does not perform protocol mediation, and the client is responsible for decoding and serializing data into the desired format.

To learn more about TCP proxy support and how to create TCP proxy APIs, refer to [this page](../../guides/create-apis/tcp-proxy-apis.md).

## Entrypoints

### HTTP POST

The HTTP POST entrypoint now supports initiating an empty message flow that gives policies full access to the context (i.e., to construct messages with metadata, headers, etc.) whenever the POST request is made to the entrypoint.&#x20;

For more information, see [HTTP POST in Entrypoint Configuration](../../guides/api-configuration/v4-api-configuration/entrypoints/#http-post).

## Endpoints

### RabbitMQ

Gravitee now allows a RabbitMQ endpoint to be configured with a Virtual Host so that messages can be produced and consumed from a specific vhost.

In addition, a RabbitMQ endpoint can now be configured using TLS/mTLS to securely produce and consume messages. Gravitee supports creating APIs with a RabbitMQ endpoint and any of the following:

* JKS Truststore file
* JKS Truststore base64 content
* PKCS12 Truststore file
* PKCS12 Truststore base64 content
* PEM certificate file
* PEM certificate content
* JKS Keystore file
* JKS Keystore base64 content
* PKCS12 Keystore file
* PKCS12 Keystore base64 content
* PEM certificate and key file
* PEM certificate and key content

For more information, see [RabbitMQ in Endpoint Configuration](../../guides/api-configuration/v4-api-configuration/endpoints/#rabbitmq).

### Kafka

#### Topics

In addition to explicitly specifying a list of consumed Kafka topics that can be set in the API, the user can now set a wildcard for the consumed topics on the Kafka endpoint. The Kafka consumer automatically detects, adds, and removes topics that match the provided pattern.&#x20;

When creating or configuring a v4 message API with a Kafka endpoint, the user can select either **Specify List of Topics** or **Specify Topic Expression**, then enter the information appropriate to the selection:

* **Specify List of Topics:** The topic(s) from which your Gravitee Gateway client will consume messages.
* **Specify Topic Expression:** A single Java regular expression.  to consume only messages from Kafka topics that match the expression.

For more information, see [Kafka in Endpoint Configuration](../../guides/api-configuration/v4-api-configuration/endpoints/#kafka).

#### SASL OAUTHBEARER

To facilitate support for SASL OAUTHBEARER, the Kafka endpoint plugin includes a [login callback handler for token retrieval](https://docs.confluent.io/platform/current/kafka/authentication\_sasl/authentication\_sasl\_oauth.html#login-callback-handler-for-token-retrieval). This handler is configured using the following JAAS configuration:

```
"org.apache.kafka.common.security.oauthbearer.OAuthBearerLoginModule required access_token=\"<ACCESS_TOKEN>\";"
```

## Policy enhancements

### Assign Metrics

A user can now assign custom metrics at the message level. A condition can be defined on the metric added to an API that evaluates and becomes part of the metrics, which can then be obtained via the Management API. See [this page](../../reference/policy-reference/assign-metrics.md) for more information.

### Groovy

The `groovy` policy has been enhanced to support message-level definitions. This implementation of custom Groovy scripts is designed for nonstandard or specific use cases that are not sufficiently addressed by other Gravitee policies. The `groovy` policy can be applied to an API to override message content via the `message.content` property. See [this page](../../reference/policy-reference/groovy.md) for more information.

## Datadog

(Enterprise-only) Datadog reporter support now extends to v4 APIs. v4 API metrics and monitoring data can be exported to a Datadog instance to ensure a comprehensive observability strategy. To learn more about reporters, check out [this section](../../getting-started/configuration/reporters/).
