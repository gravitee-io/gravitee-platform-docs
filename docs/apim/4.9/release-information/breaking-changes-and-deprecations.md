# Breaking Changes and Deprecations

## Breaking changes

Here are the breaking changes for versions 4.X of Gravitee and versions 3.X of Gravitee

### Breaking changes from 4.X

Here are the breaking changes from versions 4.X of Gravitee.

#### 4.9.0

**Update to OpenShift compatibility**

Before 4.9.0, users had to override the `runAsGroup`'s `securityContext` to set the GID to 1000.&#x20;

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

#### 4.8.0

**APIM standalone components**

The APIM standalone components that were available to download from [Gravitee.io downloads - apim/components](https://download.gravitee.io/#graviteeio-apim/components/) are no longer available or supported.&#x20;

You can use the full distribution .ZIP file instead. To download the full distribution .ZIP file, go to [Gravitee.io downloads - apim/distributions](https://download.gravitee.io/#graviteeio-apim/distributions/).

**Lucene update 10**

Lucene has been upgraded to 10. Before starting the Management API (mAPI), you must clean the `/data` directory in your `GRAVITEE_HOME` containing Lucene working files. Otherwise, the mAPI does not start. There is no impact. When mAPI restarts, it re-indexes.&#x20;

**Custom plugin development**&#x20;

If a plugin is referencing `io.gravitee.gateway.reactor.ReactableApi`, it needs to be recompiled with APIM 4.8 dependencies because `ReactableApi` it is now an interface rather than an abstract class. Without recompilation, the plugin throws a `java.lang.IncompatibleClassChangeError` .

#### 4.7.0

**Hazelcast**

During a rolling upgrade in Kubernetes, if a pod with the version about to be replaced is still running, mAPI throws these warnings:

`09:36:15.515 [graviteeio-node] WARN c.h.i.impl.HazelcastInstanceFactory - Hazelcast is starting in a Java modular environment (Java 9 and newer) but without proper access to required Java packages. Use additional Java arguments to provide Hazelcast access to Java internal API. The internal API access is used to get the best performance results. Arguments to be used: --add-modules <http://java.se|java.se> --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED --add-opens jdk.management/com.sun.management.internal=ALL-UNNAMED 09:36:24.589 [graviteeio-node] WARN c.h.kubernetes.KubernetesClient - Cannot fetch public IPs of Hazelcast Member PODs, you won't be able to use Hazelcast MULTI_MEMBER or ALL_MEMBERS routing Clients from outside of the Kubernetes network`

Once the pod is terminated, `cache-hazelcast` installs successfully. The upgrade process then continues as expected with the upgrader scripts, which means that there will be a brief downtime when upgrading to 4.7.x.

**Azure API Management update**

There is a new parameter for ingesting Azure APIs. To ingest Azure APIs, you must set `gravitee_integration_providers_0_configuration_subscriptionApprovalType` in your `docker-compose.yaml` and set the `SUBSCRIPTION_APPROVAL_TYPE`  in your `.env` file to `AUTOMATIC` , `MANUAL` or `ALL` .

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
