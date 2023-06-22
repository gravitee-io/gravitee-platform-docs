---
description: This article covers the new features released in Gravitee 4.0
---

# APIM 4.0

## The new v4 API creation wizard

{% @arcade/embed flowId="IoH5bZLjSO6ce8UbgMmc" url="https://app.arcade.software/share/IoH5bZLjSO6ce8UbgMmc" fullWidth="true" %}

The new v4 API creation wizard enables you to use the Gravitee API Management Console to create Gateway APIs that use the Gravitee v4 API defintion. The v4 API definition enables organizations to start using Gravitee to secure, expose, and govern both their synchronous and asynchronous APIs. The new creation wizard enables you to expose Kafka, MQTT, RabbitMQ, and Mock (simulated backend for testing purposes) backends as either REST, WebSocket, Webhook, or Server-sent events (SSE) APIs.

For more information on how to use the new v4 API Creation wizard, please refer to the [v4 API Creation Wizard documentation. ](../../../guides/create-apis/how-to/v4-api-creation-wizard-docs.md)

## The new v4 Policy Design Studio

(Insert Arcade)

We've released a brand new Policy Design Studio that enables you to design policy flows and enforcement mechanisms for v4 APIs. Policies designed using the new v4 API Design Studio can be designed and enforced at the request, response, publish, and/or subscribe phases. They can also be enforced at the message level for use cases where message-based APIs and communication are being utilized. This enables greater API governance, as you can now use a one, centralized tool and approach to make sure synchronous and asynchronous APIs are secured, made reliable, transformed, etc.

For more information on how to use the v4 Policy Desig studio, please refer to the&#x20;

### Existing Gravitee policies that now support v4 APIs

As a part of the new Policy Design Studio release, we've migrated over some existing Gravitee to the new policy execution engine, which will enable these policies to work for v4 APIs. These policies are:

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

### New policies for v4 APIs

We've also released brand new policies for v4 APIs tha&#x20;

### Support for Schema registry as a resource

## Webhook subscription configuration in the Developer Portal

## v2 Management API

## New Kubernetes Operator enhancements

## More new features

### New API Management Console support for v4 APIs

### Datadog reporter

