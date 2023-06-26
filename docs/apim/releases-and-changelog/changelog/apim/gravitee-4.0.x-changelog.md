---
description: >-
  This page contains the changelog entries for APIM 4.0 and any future minor
  APIM 4.x.x releases
---

# APIM 4.x.x (2023-07-20)

## About upgrades

For upgrade instructions, please refer to the [APIM Upgrade Guide.](../../../getting-started/install-guides/installation-guide-migration/)

{% hint style="danger" %}
If you plan to skip versions when you upgrade, ensure that you read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.
{% endhint %}

## Default policy distribution

Need to include a list of policies and their version in each release of APIM



## Gravitee API Management 4.0 - July 20, 2023

For more in-depth information on what's new, please refer to the [Gravitee APIM 4.0 release notes](../../release-notes/gravitee-4.x/apim-4.0.md).

<details>

<summary>What's new</summary>

#### API Management Console

* API List support for v4 APIs
* New API General page for for v4 APIs
* New support for configuring v4 APIs:
  * Dynamic Entrypoint configuration
  * Dynamic Endpoint configuration
  * Plan configuration
  * Subscription configuration

#### API Creation Wizard

* New API creation wizard that supports the Gravitee v4 API definition.
* v4 API Creation wizard support for the following Endpoints:
  * Kafka
  * MQTT
  * RabbitMQ (if using AMQP 0-9-1 protocol)
  * Mock
* v4 API Creation wizard support for the following Entrypoints:
  * WebSocket
  * Webhooks
  * Server-sent Events (SSE)
  * HTTP GET
  * HTTP POST
* Support for Gravitee protocol mediation in the new v4 API Creation Wizard
* New RabbitMQ endpoint

#### Policy Design and Enforcement

* New Policy Design Studio that supports v4 APIs
* v4 Policy Design Studio support for message-level policies
* v4 Policy Design Studio support for policy enforcement on publish and subscribe phases for pub/sub communication
* Made existing Gravitee policies enforceable for v4 APIs:
  * API key policy
  * JWT policy
  * Keyless policy
  * OAuth2 policy
  * JSON to JSON policy
  * JSON to XML policy
  * XML to JSON
  * Assign attributes policy
  * Latency policy
  * Circuit breaker policy
  * Retry policy
  * Cache policy
  * Transform headers policy
* New Cloud Events policy
* New serialization and deserialization policies
  * JSON to Avro policy
  * Avro to JSON policy

#### Developer Portal

* Configure Webhook subscription details in the Developer Portal (by the consumer/subscriber)

#### Integrations

* Datadog reporter

#### Management API

* v2 Management API that supports actions for v4 APIs

#### Kubernetes Operator

* Use the Kubernetes Operator as a Kubernetes ingress controller
* Maintain a unique custom resource defintion (CRD) for your API across all Gravitee environments
* Manage application-level CRDs through the Gravitee Kubernetes Operator
* Define the ManagementContext for your CRD and control whether the API should be local or global

</details>

<details>

<summary>Bug Fixes</summary>

* Insert bug fixes

</details>

<details>

<summary>Breaking Changes</summary>

* Insert breaking changes

</details>
