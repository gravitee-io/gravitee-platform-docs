---
description: This article covers the new features released in Gravitee API Management 4.0
---

# APIM 4.0

## Introduction

Gravitee 4.0 was released on July 20th, 2023, and introduced broadened support for asynchronous APIs, event brokers, and protocol mediation-especially as it pertains to what is surfaced in the API Management Console. For a more paired down version of what was released, please see the [changelog for Gravitee APIM 4.x](../../changelog/apim/gravitee-4.0.x-changelog.md). Otherwise, keep reading for a more in-depth exploration of everything that was released in APIM 4.0.

## The new v4 API creation wizard

{% @arcade/embed flowId="IoH5bZLjSO6ce8UbgMmc" url="https://app.arcade.software/share/IoH5bZLjSO6ce8UbgMmc" fullWidth="true" %}

The new v4 API creation wizard enables you to use the Gravitee API Management Console to create Gateway APIs that use the Gravitee v4 API defintion. The v4 API definition enables organizations to start using Gravitee to secure, expose, and govern both their synchronous and asynchronous APIs. The new creation wizard enables you to create APIs that expose Kafka, MQTT, (new) RabbitMQ (if using AMQP 0-9-1 protocol), and Mock (simulated backend for testing purposes) backends as either REST, WebSocket, Webhook, or Server-sent events (SSE) APIs, all using the Gravitee API Management Console.

For more information on how to use the new v4 API Creation wizard, please refer to the [v4 API Creation Wizard documentation. ](../../../guides/create-apis/how-to/v4-api-creation-wizard.md)

## The new v4 Policy Design Studio

(Insert Arcade)

We've released a brand new Policy Design Studio that enables you to design policy flows and enforcement mechanisms for v4 APIs. Policies designed using the new v4 API Design Studio can be designed and enforced at the request, response, publish, and/or subscribe phases. They can also be enforced at the message level for use cases where message-based APIs and communication are being utilized. This enables greater API governance, as you can now use a one, centralized tool and approach to make sure synchronous and asynchronous APIs are secured, made reliable, transformed, etc.

For more information on how to use the v4 Policy Design studio, please refer to the [v4 Policy Design Studio documentation](../../../guides/policy-design/v4-api-policy-design-studio.md).&#x20;

### Existing Gravitee policies that now support v4 APIs

As a part of the new Policy Design Studio release, we've made some existing Gravitee policies work for v4 APIs. These policies are:

* API key policy
* JWT policy
* Keyless policy
* OAuth2 policy
* JSON to JSON policy&#x20;
* JSON to XML policy
* XML to JSON policy
* Assign attributes policy&#x20;
* Latency policy&#x20;
* Circuit breaker policy&#x20;
* Retry policy&#x20;
* Cache policy&#x20;
* Transform headers policy

For more information on policies, please refer to our policy reference documentation.

### New policies for v4 APIs

We've also released brand new policies that will support v4 APIs:

* Cloud Events policy: this policy enables the Gateway to transform incoming data into Cloud Events format.&#x20;
* Serialization and Deserialization policies:
  * JSON to Avro: transform information in JSON format to Avro format
  * Avro to Json: transform information from Avro format into JSON format

For more information on policies, please refer to our policy reference documentation.

## Support for Schema registry as a resource

(Insert arcade)

When designing policies and flows, you can now define Confluent Schema Registry as a resource. This allows Gravitee to serialize and deserialize information between Avro and JSON via various serialization and deserialization policies. Serialization and deserialization will be validated against target schemas stored in specified schema registries. The schema ID can be obtained dynamically through a message header or attribute.

## Webhook subscription configuration in the Developer Portal

(Insert arcade)

We released support for Webhook subscriptions a while ago, but now we've made the consumer experience much better with the ability to define your Webhook subscription in the Gravitee Developer Portal.&#x20;

When in the Developer Portal, you'll be able to:

* Configure the details of your plan in the portal, including defining a custom Webhook callback URL
* Add basic authentication and an API key as a bearer token

This will all be done while creating an application in the Gravitee Developer Portal. For more information, please refer to the Developer Portal documentation.&#x20;

## v2 Management API

We've created a new version of the Gravitee API Management Management API (M-API). This new version of the Management API enables you to act on v4 APIs "as code" via the API. For more information on the v2 Management API, please refer to the API reference documentation.

## New Kubernetes Operator enhancements

In addition to making Gravitee API Management more "event-native," we've also made it more "kube-native," with some major enhancements to our Kubernetes Operator:

* You can now maintain a unique custom resource defintion (CRD) for your API across all Gravitee environments and verbalize some fields per enviornment. For example, you can change the endpoint target across dev, staging, and prod environments using CRDs.
* You can now manage application-level CRDs through the Gravitee Kubernetes Operator. This enables you to configure an platform level configuration using a k8s declarative approach
* The Kubernetes Operator now supports both local and global configurations. This means that you can define the ManagementContext for your CRD and control whether the API should be local or global.&#x20;

### Gravitee as ingress controller

(insert arcade)

Another major update to the Gravitee Kubernetes Operator is it's ability to act as an ingress controller. Now, you can use Gravitee as an ingress controller as opposed to using a third-party ingress controller, such as NGNIx or traffik. This will result in less complexity and maintenance across the entirety of your infrastructure.&#x20;

## More new features

While not included in this release's major highlights, here are the other features released in Gravitee API Management 4.0.

### New API Management Console support for v4 APIs

(Insert arcade)

As a part of our additional support for v4 APIs and asynchronous APIs, we've added more support for v4 APIs in the UI. This support includes:

* **The API list:** you can now see and filter v4 APIs in the APIs list
* **API settings and details:** the following API settings and details can now be seen and/or configured in the Gravitee API Management Console UI:&#x20;
  * API General page
  * Entrypoint configuration
  * Endpoint configuration
  * Plans
  * Subscriptions

### Datadog reporter

The Datadog reporter enables you to push API moniotring metrics and analytics into Datadog, so that you can ensure that your Datadog instance doesn't have any API monitoring blind spots. To learn more about the Datadog reporter, please refer to the Datadog reporter documentation.

