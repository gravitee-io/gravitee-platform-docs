---
description: This article covers the new features released in Gravitee API Management 4.0
---

# APIM 4.0

{% hint style="danger" %}
**Make sure you upgrade your license file**

If you are an existing Gravitee Enterprise customer upgrading to 4.x, please make sure that you upgrade your Gravitee license file. Reach out to your Customer Success Manager or Support team in order to receive a new 4.x license.
{% endhint %}

## Introduction

Gravitee 4.0 was released on July 20th, 2023, and introduced broadened support for asynchronous APIs, event brokers, and protocol mediation, especially as it pertains to what is surfaced in the API Management Console. For a pared-down version of what was released, please see the [changelog for Gravitee APIM 4.x](docs/apim/4.0/releases-and-changelog/changelog/apim-4.0.x.md). Otherwise, keep reading for a more in-depth exploration of everything that was released in APIM 4.0.

## The new v4 API creation wizard

{% @arcade/embed flowid="IoH5bZLjSO6ce8UbgMmc" url="https://app.arcade.software/share/IoH5bZLjSO6ce8UbgMmc" %}

The new v4 API creation wizard enables you to use the Gravitee API Management Console to create Gateway APIs built with the Gravitee v4 API definition.

The v4 API definition allows organizations to use Gravitee to secure, expose, and govern both their synchronous and asynchronous APIs. With the new creation wizard, you can use the Gravitee API Management Console to create APIs that expose Kafka, MQTT, RabbitMQ (if using AMQP 0-9-1 protocol), Solace, and Mock (simulated for testing purposes) backends as either REST, WebSocket, Webhook, or Server-sent events (SSE) APIs.

For more information on how to use the new v4 API Creation wizard, please refer to the [v4 API Creation Wizard documentation.](docs/apim/4.0/guides/create-apis/the-api-creation-wizard/v4-api-creation-wizard.md)

## The new v4 Policy Studio

We've released a brand new Policy Studio that enables you to design policy flows and enforcement mechanisms for v4 APIs. This enables greater API governance, as you can now use a single, centralized tool and approach to ensure synchronous and asynchronous APIs are secured, reliable, transformed, etc.

Policies designed using the new v4 API Policy Studio can be designed and enforced at the request, response, publish, and/or subscribe phases. They can also be enforced at the message level for use cases where message-based APIs and communication are employed.

For more information on how to use the v4 Policy Studio, please refer to the [v4 Policy Studio documentation](docs/apim/4.0/guides/policy-studio/v4-api-policy-studio.md).

### Existing v2 API Gravitee policies that now support v4 message APIs

As a part of the new Policy Studio release, we've made some existing Gravitee policies now work for v4 message APIs. Message APIs are APIs created using the Introspect Messages from Event-driven Backend option. These policies are:

* API key policy
* JWT policy
* Keyless policy
* OAuth2 policy
* JSON to JSON policy
* JSON to XML policy
* XML to JSON policy
* Assign attributes policy
* Latency policy
* Circuit breaker policy
* Retry policy
* Cache policy
* Transform headers policy

{% hint style="info" %}
While these policies can be used for v4 message APIS, not all of these policies support execution at the message level. For more information on the execution phase for each policy, please refer to our [Policy Reference documentation](../../reference/policy-reference/).
{% endhint %}

For more information on policies, please refer to our [policy reference documentation](../../reference/policy-reference/).

### New policies for v4 message APIs

We've also released two brand new policies that will support v4 message APIs:

* [Cloud Events policy](docs/apim/4.0/reference/policy-reference/cloud-events.md): You can use the `cloud-events` policy to create a cloud-events `JSON` object from messages. The `datacontenttype` will be set accordingly to the message `Content-type` if any.
* Serialization and Deserialization policies:
  * [Avro <> JSON](docs/apim/4.0/reference/policy-reference/avro-json.md): transform information between Avro and JSON format

For more information on policies, please refer to our [policy reference documentation](../../reference/policy-reference/).

## Support for Schema registry as a resource

When designing policies and flows, you can now define Confluent Schema Registry as a resource. This allows Gravitee to serialize and deserialize information between Avro and JSON via various serialization and deserialization policies.

Serialization and deserialization will be validated against target schemas stored in specified schema registries. The schema ID can be obtained dynamically through a message header or attribute.

For more information, please refer to our [Resources documentation](docs/apim/4.0/guides/api-configuration/resources.md).

## Webhook subscription configuration in the Developer Portal

We released support for Webhook subscriptions a while ago, but now we've made the consumer experience much better with the ability to define your Webhook subscription in the Gravitee Developer Portal.

When in the Developer Portal, you'll be able to:

* Configure the details of your plan in the portal, including defining a custom Webhook callback URL
* Add basic authentication and an API key as a bearer token

This will all be done while creating an application in the Gravitee Developer Portal. For more information, please refer to the [Webhook subscription management documentation](../../guides/developer-portal/tools-and-features/).

## v2 Management API

We've created a new version of the Gravitee API Management Management API (M-API). This new version of the Management API enables you to act on v4 APIs "as code" via the API. For more information on the v2 Management API, please refer to the [API reference documentation](docs/apim/4.0/reference/management-api-reference.md).

## New Kubernetes Operator enhancements

In addition to making Gravitee API Management more "event-native," we've also made it more "kube-native," with some major enhancements to our Kubernetes Operator:

* You can now maintain a unique custom resource definition (CRD) for your API across all Gravitee environments and verbalize some fields per environment. For example, you can change the endpoint target across dev, staging, and prod environments using CRDs.
* You can now manage application-level CRDs through the Gravitee Kubernetes Operator. This enables you to configure a platform level configuration using a k8s declarative approach
* The Kubernetes Operator now supports both local and global configurations. This means that you can define the ManagementContext for your CRD and control whether the API should be local or global.

For more information, please refer to our [Kubernetes Operator documentation](../../guides/gravitee-kubernetes-operator/).

### Gravitee as ingress controller

Another major update to the Gravitee Kubernetes Operator is its ability to act as an ingress controller. Now, you can use Gravitee as an ingress controller as opposed to using a third-party ingress controller, such as nginx or Traffik. This will result in less complexity and maintenance across the entirety of your infrastructure.

For more information please refer to our [Kubernetes Operator - Ingress Controller documentation](docs/apim/4.0/guides/gravitee-kubernetes-operator/gravitee-as-an-ingress-controller.md).

## More new features

While not included in this release's major highlights, here are the other features released in Gravitee API Management 4.0.

### New API Management Console support for v4 APIs

As a part of our additional support for v4 APIs and asynchronous APIs, we've added more support for v4 APIs in the UI. This support includes:

* **The API list:** you can now see and filter v4 APIs in the APIs list
* **API settings and details:** the following API settings and details can now be seen and/or configured in the Gravitee API Management Console UI:
  * API General page
  * Entrypoint configuration
  * Endpoint configuration
  * Plans
  * Subscriptions

### Datadog reporter

The Datadog reporter enables you to push API monitoring metrics and analytics into Datadog, so that you can ensure that your Datadog instance doesn't have any API monitoring blind spots. To learn more about the Datadog reporter, please refer to the [Datadog reporter documentation](../../getting-started/configuration/configure-reporters/#datadog-reporter).

### Redis repository plugin

The Redis repository plugin is now embedded in the default distribution, meaning you do not need to download and install it on your own. The Helm chart has been updated accordingly, so no additional configuration is required.
