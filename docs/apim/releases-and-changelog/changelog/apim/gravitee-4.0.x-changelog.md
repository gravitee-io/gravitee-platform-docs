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

**API Management Console**

* API List support for v4 APIs
* New API General page for for v4 APIs
* New support for configuring v4 APIs:
  * Dynamic Entrypoint configuration
  * Dynamic Endpoint configuration
  * Plan configuration
  * Subscription configuration

**API Creation Wizard**

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

**Policy Design and Enforcement**

* New Policy Studio that supports v4 APIs
* v4 Policy Studio support for message-level policies
* v4 Policy Studio support for policy enforcement on publish and subscribe phases for pub/sub communication
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

**Developer Portal**

* Configure Webhook subscription details in the Developer Portal (by the consumer/subscriber)

**Integrations**

* Datadog reporter

**Management API**

* v2 Management API that supports actions for v4 APIs

**Kubernetes Operator**

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

**Running APIM**
* APIM now requires a minimum of JDK 17.
* Starting with 4.0.0, there will not be enterprise tags (i.e. suffixed by `-ee`) anymore.
* Cluster managers are now available as plugins and so Hazelcast Cluster Manager has been removed from the default distribution.

**Monitoring APIM**
* The name of the sync probe has been changed from `api-sync` to `sync-process` to make it explicit when all sync processes have been completed.
  * The content of the sync handler has slightly changed to align with new concepts:
    * `initialDone`: `true` if the first initial synchronization is done
    * `counter`: the number of iterations
    * `nextSyncTime`: when is the next synchronization
    * `lastOnError`: the latest synchronization with an error
    * `lastErrorMessage`: if `lastOnError` is `true`, the content of the error message
    * `totalOnErrors`: the number of iterations with an error
* v4 APIs currently only support the Elasticsearch reporter. If any other reporter is configured at Gateway level, each v4 API call will produce an error log.&#x20;
  * However, when using a different reporter, it remains possible to disable analytics on a per-API basis to avoid generating error logs for v4 APIs.

**Managing APIs**
* The endpoint configuration is now split into a shared configuration that can be used at the group level and a configuration dedicated to the endpoint that can override the shared configuration. Existing v4 APIs need to be updated and reconfigured accordingly.
* Removed an unused and outdated feature regarding file synchronization known as `localregistry`.
* Subscriptions with `type: SUBSCRIPTION` have been renamed to `type: PUSH`. Plans have a new field called `mode` that is `STANDARD` by default but needs to be `PUSH` for all Push plans.
  * A mongo script is available to migrate the data in MongoDB [https://github.com/gravitee-io/gravitee-api-management/tree/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/4.0.0](https://github.com/gravitee-io/gravitee-api-management/tree/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/4.0.0))
* Jupiter mode has been replaced with the v4 emulation engine:
  * `jupiterModeEnabled` configuration has been removed and cannot be disabled anymore.
  * By default, any v2 API created or imported will emulate V4 Engine.
  * All new requests will use the new `HttpProtocolVerticle` introduced with the V4 engine. The old `ReactorVerticle` has been removed.
  * The default timeout is set to 30s for any request.
* Security Policies such as Keyless, ApiKey, JWT, or Oauth2 have been updated to return a simple Unauthorized message in case of an error. No additional details are provided to protect against a potential attacker. **This impact both v2 and v4 APIs.** However, error keys are still available for error templating. Here is a list of error keys by policy:
  * ApiKey
    * API\_KEY\_MISSING
    * API\_KEY\_INVALID
  * JWT
    * JWT\_MISSING\_TOKEN
    * JWT\_INVALID\_TOKEN
  * Oauth2
    * OAUTH2\_MISSING\_SERVER
    * OAUTH2\_MISSING\_HEADER
    * OAUTH2\_MISSING\_ACCESS\_TOKEN
    * OAUTH2\_INVALID\_ACCESS\_TOKEN
    * OAUTH2\_INVALID\_SERVER\_RESPONSE
    * OAUTH2\_INSUFFICIENT\_SCOPE
    * OAUTH2\_SERVER\_UNAVAILABLE

</details>
