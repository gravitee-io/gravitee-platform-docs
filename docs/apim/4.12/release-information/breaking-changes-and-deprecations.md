---
description: Information about breaking changes and deprecations.
metaLinks:
  alternates:
    - breaking-changes-and-deprecations.md
---

# Breaking Changes and Deprecations

## Breaking changes

Here are the breaking changes for versions 4.X of Gravitee and versions 3.X of Gravitee

### Breaking changes from 4.X

Here are the breaking changes from versions 4.X of Gravitee.

#### 4.12.0

**JSON Validation policy: response error keys corrected**

The JSON Validation policy now emits error keys that match their documented names for response-scope failures in V4 APIs. Previously, the keys were swapped: `JSON_INVALID_RESPONSE_FORMAT` was emitted for parse failures, and `JSON_INVALID_RESPONSE_PAYLOAD` for schema validation failures.

If you configured response templates using these error keys, you must update them to use the correct key names.

**`gravitee-resource-cache-redis` requires version 5.0.0**

If you use the `gravitee-resource-cache-redis` plugin, you must upgrade it to version 5.0.0 when upgrading to APIM 4.12. This plugin is not included in the default APIM bundle and must be managed independently. Running an older version of `gravitee-resource-cache-redis` with APIM 4.12 is not supported.

**Redis cache resource now uses a shared connection pool**

The Redis cache resource now uses a shared Redis client factory with gateway-wide connection pool and timeout settings. Previously, each API using a Redis cache resource maintained its own dedicated connection to Redis, so 100 APIs with a Redis cache resource resulted in 100 active Redis connections to the server.

If you use the `gravitee-resource-cache-redis` or `aiVectorStoreRedis` resource, review and adjust the following settings to suit your workload:

* `resources.aiVectorStoreRedis.maxPoolSize`
* `gateway.cacheRedis.maxPoolSize`
* Timeout settings for both resources

**v1 API definitions removed from the Management API v2 contract**

From 4.12.0, APIM no longer supports v1 APIs. The `ApiV1` and `Rule` schemas and the `V1` value of the `DefinitionVersion` enum are removed from the Management API v2 OpenAPI specification. Migrate any remaining v1 APIs to at least a v2 definition before you upgrade. For more information about how APIM handles v1 APIs, see [Support for v1 APIs](support-for-v1-apis.md).

**Automation API restricts shared policy group API types and phases**

The Automation API now accepts shared policy groups only for the `PROXY` and `MESSAGE` API types. The `apiType` property of a shared policy group no longer accepts `NATIVE`, `A2A_PROXY`, `LLM_PROXY`, or `MCP_PROXY`, and the `FlowPhase` schema no longer includes the `ENTRYPOINT_CONNECT` and `INTERACT` values. The Automation API rejects a shared policy group specification that uses one of the removed values.

This change affects Automation API clients, including the Gravitee Kubernetes Operator (GKO) and the Gravitee Terraform provider. These API types and phases remain available for shared policy groups in the Management API v2 and the Console.

**`hidden` property removed from the Automation API metadata schema**

The `Metadata` schema of the Automation API no longer includes the `hidden` property. This change affects API and application metadata that you manage through the Automation API. If you use the Terraform provider, see the migration steps in the [Terraform provider release notes](../terraform/release-notes.md).

**Cluster creation through the Management API v2 requires a cluster type**

The request body of the Create Cluster endpoint of the Management API v2 (`POST /environments/{envId}/clusters`) now requires a `type` property with one of the following values: `KAFKA_CLUSTER_STANDALONE`, `KAFKA_CLUSTER`, or `KAFKA_VIRTUAL_CLUSTER`. In earlier versions, the request body schema didn't include a `type` property. Update any clients or scripts that create clusters to include the `type` property.

#### 4.11.14

**API Key policy: the header name set on a plan takes precedence over the Gateway setting**

APIM 4.11.14 and later bundle version 6.0.0 or later of the API Key policy, which changes how the Gateway resolves the name of the header that carries the API key. The Gateway now applies the header name set on the plan whenever that value isn't empty, and it no longer checks the plan's `enableCustomApiKeyHeader` option. Previously, the Gateway applied the header name set on the plan only when `enableCustomApiKeyHeader` was `true`, and that option defaults to `false`, so a plan left at that default fell back to the `policy.api-key.header` value from `gravitee.yml`. V2 APIs that don't run on the emulation engine keep the earlier behavior and still require `enableCustomApiKeyHeader`.

When a plan stores a header name, that name now overrides `policy.api-key.header`. A request that sends the key only on the Gateway-level header returns `401 Unauthorized`, because the Gateway reads the header name set on the plan and then falls back to the `api-key` query parameter. Before you upgrade, open each API Key plan and check the **API Key Header** field. Set the field to the header name that your clients send, or clear it on plans that rely on the Gateway-level header.

APIM 4.12.0 and later also bundle version 6.x. For the full resolution order, see [API Key](../create-and-configure-apis/apply-policies/policy-reference/api-key.md).

#### 4.11.0

**A2A Proxy APIs architecture**

The A2A proxy architecture introduces the `A2A_PROXY` API type. With this change, you must create your A2A Proxy APIs again to avoid any issues and to align with the new architecture.

**Next-Gen Developer Portal APIs and documentation pages must be published again**

When you upgrade to APIM 4.11, any APIs and documentation pages that you published to the New Developer Portal are no longer published. After you upgrade to 4.11, publish your APIs and documentation pages again through the **Navigation items** section of the New Developer Portal settings.

**New Developer Portal subscriptions require published API pages**

When you upgrade to APIM 4.11, an API accepts subscriptions through the New Developer Portal only after you publish the API's pages. To enable subscriptions to an API, publish the API's pages through the **Navigation items** section of the New Developer Portal settings.


#### 4.10.0

**Kafka Native APIs Analytics**

Elasticsearch indices used by Kafka Native APIs have been modified for better compatibility with OpenSearch and better accuracy.

You might have to do a roll-over of your `gravitee-event-metrics` index.

Previous indexed document is deleted. However, they are no longer be taken into account in Gravitee Dashboards.

#### 4.9.0

**Update to OpenShift compatibility**

Before 4.9.0, users had to override the `runAsGroup`'s `securityContext` to set the GID to 1000.

With this update, the user must set the `runAsGroup`'s `securityContext` to `null` to allow OpenShift to select the root group.

**Customization on Federation ingress**

If the `integration-controller` ingress uses the same host as the `management` ingress, it no longer inherits the annotation of the `management` ingress. With 4.9.0, you must configure the `integration-controller` ingress with the following values:

```yaml
api:
  federation:
    ingress:
      enabled: true
      path: /integration-controller(/.*)?
      pathType: Prefix
      hosts:
        - apim.example.com
      annotations:
        kubernetes.io/ingress.class: nginx
        nginx.ingress.kubernetes.io/proxy-read-timeout: 3600   
```

If you want the `integration-controller` ingress to use the same host as the `management` ingress, set the same values for `hosts` and `tls` in the `integration-controller` ingress, `management` ingress, and `federation` ingress.

**Elasticsearch template updates required**

When you upgrade to 4.9.0, you must update Elasticsearch templates to support execution transparency analytics with error and warning component tracking. If you manage your own Elasticsearch installation, update index templates before you upgrade. Elasticsearch auto-generates templates if you do not manually update them, but this results in suboptimal field mappings. Gravitee-managed Elasticsearch or SaaS deployments update automatically.

#### 4.8.0

**APIM standalone components**

The APIM standalone components that were available to download from [Gravitee.io downloads - apim/components](https://download.gravitee.io/#graviteeio-apim/components/) are no longer available or supported.

You can use the full distribution .ZIP file instead. To download the full distribution .ZIP file, go to [Gravitee.io downloads - apim/distributions](https://download.gravitee.io/#graviteeio-apim/distributions/).

**Lucene update 10**

Lucene has been upgraded to 10. Before starting the Management API (mAPI), you must clean the `/data` directory in your `GRAVITEE_HOME` containing Lucene working files. Otherwise, the mAPI does not start. There is no impact. When mAPI restarts, it re-indexes.

**Custom plugin development**

If a plugin is referencing `io.gravitee.gateway.reactor.ReactableApi`, it needs to be recompiled with APIM 4.8 dependencies because `ReactableApi` it is now an interface rather than an abstract class. Without recompilation, the plugin throws a `java.lang.IncompatibleClassChangeError` .

#### 4.7.0

**Hazelcast**

During a rolling upgrade in Kubernetes, if a pod with the version about to be replaced is still running, mAPI throws these warnings:

`09:36:15.515 [graviteeio-node] WARN c.h.i.impl.HazelcastInstanceFactory - Hazelcast is starting in a Java modular environment (Java 9 and newer) but without proper access to required Java packages. Use additional Java arguments to provide Hazelcast access to Java internal API. The internal API access is used to get the best performance results. Arguments to be used: --add-modules <http://java.se|java.se> --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED --add-opens jdk.management/com.sun.management.internal=ALL-UNNAMED 09:36:24.589 [graviteeio-node] WARN c.h.kubernetes.KubernetesClient - Cannot fetch public IPs of Hazelcast Member PODs, you won't be able to use Hazelcast MULTI_MEMBER or ALL_MEMBERS routing Clients from outside of the Kubernetes network`

Once the pod is terminated, `cache-hazelcast` installs successfully. The upgrade process then continues as expected with the upgrader scripts, which means that there will be a brief downtime when upgrading to 4.7.x.

**Azure API Management update**

There is a new parameter for ingesting Azure APIs. To ingest Azure APIs, you must set `gravitee_integration_providers_0_configuration_subscriptionApprovalType` in your `docker-compose.yaml` and set the `SUBSCRIPTION_APPROVAL_TYPE` in your `.env` file to `AUTOMATIC` , `MANUAL` or `ALL` .

To keep the previous behavior of Azure API Management, set the `SUBSCRIPTION_APPROVAL_TYPE` to `AUTOMATIC` .

#### 4.6.0

**OpenTracing replaced by OpenTelemetry**

OpenTracing has been replaced by OpenTelemetry. If you use OpenTracing with the Jaeger plugin, you must update your configuration to target your OpenTelemetry endpoint.

#### 4.4.0

**gateway.management.http.trustall update**

The gateway.management.http.trustall has been renamed to trustALL. By default, trustAll is set to `false`. A public CA or a well configured continue to work.

**gateway|api.services.bridge.ssl.clientAuth no longer use a boolean value**

gateway|api.services.bridge.ssl.clientAuth no longer use a boolean value. Possible values are now the following values:

* `none`. This value was previously false
* `required`. Backward compatibility is maintained, true means required
* `request`.

#### 4.0.27

**ssl-redirect option changed to default**

In gateway ingress controller, the ssl-redirect option was changed from "false" to default. For more information about this change, go to [Server-side HTTPS enforcement through redirect](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#server-side-https-enforcement-through-redirect).

### Breaking changes from 3.X

Here are the breaking changes from versions 3.X of Gravitee.

#### 3.2.0

**Moved Probes configuration**

Probes configuration was moved under deployment.

**Probe default configuration**

Changed probe default configuration. For more information about the change to the default configuration, go to the following [GitHub pull request](https://github.com/gravitee-io/gravitee-api-management/pull/8885).

**Removed the apiSync parameter**

Under gateway.readinessProbe, the apiSync parameter was removed.

#### 3.1.55

**Use of smtp.properties.starttlsEnable**

Use smtp.properties.starttls.enable instead of smtp.properties.starttlsEnable.

## Deprecated functionality

Here is the deprecated functionality for 4.X versions of Gravitee and 3.X version of Gravitee.

### Deprecated functionality 4.X

Here is the deprecated functionality from 4.X of Gravitee

#### 4.4.0

**gateway.management.http.username deprecation**

To allow JWT auth to be configured, gateway.management.http.username and password have been deprecated to allow JWT auth to be configured. For more information about the deprecation, go to [Changelog](https://github.com/gravitee-io/gravitee-api-management/blob/master/helm/CHANGELOG.md).

### Deprecated functionality 3.X

Here is the deprecated functionality from 3.X of Gravitee

#### 3.20.28

**Deprecated api | gateway | ui | portal.security context is removed**

The deprecated api | gateway | ui | portal.security context has been removed.
