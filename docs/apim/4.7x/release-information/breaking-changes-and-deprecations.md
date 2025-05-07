# Breaking Changes & Deprecations

## Overview

This page describes the breaking changes and deprecated functionality that impact each version of Gravitee API Management.

## Breaking changes from 4.x

Here are the breaking changes from versions 4.X of Gravitee.

### 4.7.0

**Hazelcast**

During a rolling upgrade in Kubernetes, if a pod with the version about to be replaced is still running, mAPI throws these warnings:

`09:36:15.515 [graviteeio-node] WARN c.h.i.impl.HazelcastInstanceFactory - Hazelcast is starting in a Java modular environment (Java 9 and newer) but without proper access to required Java packages. Use additional Java arguments to provide Hazelcast access to Java internal API. The internal API access is used to get the best performance results. Arguments to be used: --add-modules <http://java.se|java.se> --add-exports java.base/jdk.internal.ref=ALL-UNNAMED --add-opens java.base/java.lang=ALL-UNNAMED --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.management/sun.management=ALL-UNNAMED --add-opens jdk.management/com.sun.management.internal=ALL-UNNAMED 09:36:24.589 [graviteeio-node] WARN c.h.kubernetes.KubernetesClient - Cannot fetch public IPs of Hazelcast Member PODs, you won't be able to use Hazelcast MULTI_MEMBER or ALL_MEMBERS routing Clients from outside of the Kubernetes network`

Once the pod is terminated, `cache-hazelcast` installs successfully. The upgrade process then continues as expected with the upgrader scripts, which means that there will be a brief downtime when upgrading to 4.7.x.

**Azure API Management update**

There is a new parameter for ingesting Azure APIs. To ingest Azure APIs, you must set `gravitee_integration_providers_0_configuration_subscriptionApprovalType` in your `docker-compose.yaml` and set the `SUBSCRIPTION_APPROVAL_TYPE`  in your `.env` file to `AUTOMATIC` , `MANUAL` or `ALL` .

To keep the previous behavior of Azure API Management, set the `SUBSCRIPTION_APPROVAL_TYPE` to `AUTOMATIC` .

### 4.6.0

**OpenTracing replaced by OpenTelemetry**

OpenTracing has been replaced by OpenTelemetry. If you use OpenTracing with the Jaeger plugin, you must update your configuration to target your OpenTelemetry endpoint.

### 4.4.0

**gateway.management.http.trustall update**

The gateway.management.http.trustall has been renamed to trustALL. By default, trustAll is set to `false`. A public CA or a well configured continue to work.

**gateway|api.services.bridge.ssl.clientAuth no longer use a boolean value**

gateway|api.services.bridge.ssl.clientAuth no longer use a boolean value. Possible values are now the following values:

* `none`. This value was previously false
* `required`. Backward compatibility is maintained, true means required
* `request`.

### 4.0.27

**ssl-redirect option changed to default**

In gateway ingress controller, the ssl-redirect option was changed from "false" to default. For more information about this change, go to [Server-side HTTPS enforcement through redirect](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#server-side-https-enforcement-through-redirect).

### 4.0.0

#### EE plugins

Particular plugins are only available to enterprise customers. [See Gravitee APIM Enterprise Edition](../introduction/open-source-vs-enterprise-edition.md) for additional information.

#### Running APIM

* APIM requires a minimum of JDK 17.
* There are no longer enterprise tags (i.e., suffixed by `-ee`).
* Cluster managers are available as plugins. Hazelcast Cluster Manager has been removed from the default distribution.
* TLS 1.0 and TLS 1.1 protocols are disabled by default. You can enable these protocols with the proper TCP SSL configuration of the Gateway:

{% code overflow="wrap" %}
````
```yaml
http:
  ssl:
    tlsProtocols: TLSv1.0, TLSv1.1, TLSv1.2
```
````
{% endcode %}

```
&#x20;or using environment variables:

```

{% code overflow="wrap" %}
````
```bash
GRAVITEE_HTTP_SSL_TLSPROTOCOLS=TLSv1.0,TLSv1.1,TLSv1.2
```
````
{% endcode %}

#### **Monitoring APIM**

* The name of the sync probe has been changed from `api-sync` to `sync-process` to make the completion of all sync processes explicit.
* The content of the sync handler has changed slightly to align with new concepts:
  * `initialDone`: `true` if the first initial synchronization is done
  * `counter`: The number of iterations
  * `nextSyncTime`: Time of the next synchronization
  * `lastOnError`: The latest synchronization with an error
  * `lastErrorMessage`: If `lastOnError` is `true`, the content of the error message
  * `totalOnErrors`: The number of iterations with an error

#### **Managing APIs**

*   The endpoint configuration is now split into:

    * A shared configuration that can be used at the group level
    * A configuration dedicated to the endpoint that can override the shared configuration

    Existing v4 APIs need to be updated and reconfigured accordingly.
* An unused and outdated file synchronization feature known as `localregistry` has been removed.
* Subscriptions with `type: SUBSCRIPTION` have been renamed to `type: PUSH`. Plans have a new field called `mode` that is `STANDARD` by default but needs to be `PUSH` for all Push plans.
  * A [mongo script](https://github.com/gravitee-io/gravitee-api-management/tree/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/4.0.0) is available to migrate the data in MongoDB.
* Jupiter mode has been replaced with the v4 emulation engine:
  * `jupiterModeEnabled` configuration has been removed and can no longer be disabled.
  * By default, any v2 API created or imported will emulate v4 Engine.
  * All new requests will use the new `HttpProtocolVerticle` introduced with the v4 engine. The legacy `ReactorVerticle` has been removed.
  * The default timeout is set to 30s for any request.
*   Security policies such as Keyless, ApiKey, JWT, and OAuth2 have been updated to return a simple unauthorized message in case of an error. No additional details are provided to protect against a potential attacker. **This impacts both v2 and v4 APIs.** Error keys remain available for error templating. Error keys by policy:

    <table><thead><tr><th width="148">Policy</th><th>Error key</th></tr></thead><tbody><tr><td>ApiKey</td><td><ul><li>API_KEY_MISSING</li><li>API_KEY_INVALID</li><li><p>JWT</p><ul><li>JWT_MISSING_TOKEN</li><li>JWT_INVALID_TOKEN</li></ul></li></ul></td></tr><tr><td>OAuth2</td><td><ul><li>OAUTH2_MISSING_SERVER</li><li>OAUTH2_MISSING_HEADER</li><li>OAUTH2_MISSING_ACCESS_TOKEN</li><li>OAUTH2_INVALID_ACCESS_TOKEN</li><li>OAUTH2_INVALID_SERVER_RESPONSE</li><li>OAUTH2_INSUFFICIENT_SCOPE</li><li>OAUTH2_SERVER_UNAVAILABLE</li></ul></td></tr></tbody></table>
*   Plan selection has been changed to reflect the actual security applied on the API:

    <table><thead><tr><th width="124">Plan</th><th>Security</th></tr></thead><tbody><tr><td>Keyless</td><td><ul><li>Will ignore any type of security (API key, Bearer token, etc.)</li><li>If another plan has detected a security token, valid or invalid, all flows assigned to the Keyless plan will be ignored.</li></ul></td></tr><tr><td>API Key</td><td><ul><li>Retrieve the API key from the request header or query parameters (default header: <code>X-Gravitee-Api-Key</code> and default query parameter: <code>api-key</code>).</li><li>While it was previously ignored, an empty API key is now considered invalid.</li></ul></td></tr><tr><td>JWT</td><td><ul><li>Retrieve JWT from <code>Authorization</code> header or query parameters.</li><li>Ignore empty <code>Authorization</code> header or any type other than Bearer.</li><li>While it was previously ignored, an empty Bearer token is now considered invalid.</li></ul></td></tr><tr><td>OAuth2</td><td><ul><li>Retrieve OAuth2 from <code>Authorization</code> header or query parameters.</li><li>Ignore empty <code>Authorization</code> header or any type other than Bearer.</li><li>While it was previously ignored, an empty Bearer token is now considered invalid.</li></ul></td></tr></tbody></table>
* Plugins are overridden when duplicates (id/type) are found. The plugin zip file with the most recent modified time is kept and others are ignored. This allows `additionalPlugins` for Helm Chart-based deployment to operate efficiently without the need to remove bundled plugins.
* The v4 API definition expects a `FlowExecution` object instead of a `FlowMode` enumeration.
* The Gravitee Expression Language (EL) syntax to access custom API properties has changed from `{#properties}` to `{#api.properties}`.
* The `Endpoint` schema is now split into two schemas and the `Endpoint` object contains two string fields to manage both the configuration specific to the endpoint and the configuration that may be overridden from the `EndpointGroup`.
* Endpoint name and endpoint group name must be unique.
*   Analytics have been introduced and the legacy logging configuration has been moved. For v4 APIs only, a new `Analytics` object is available on the API allowing you to configure all aspects of analytics:

    ```json
    "analytics": {
      "enabled" : true|false,
      "logging": { ... },
      "messageSampling" : { ... }
    }
    ```
* The webhook subscription configuration structure has changed.
*   `ApiType` enumeration has been renamed: `SYNC` becomes `PROXY` and `ASYNC` becomes `MESSAGE`. v4 APIs and PUBLISH\_API events related to V4 APIs with old values may prevent the service to start properly. **The following script migrates data for MongoDB:**

    ```bash
    print('Rename ApiType from SYNC & ASYNC to PROXY & MESSAGE');
    // Override this variable if you use prefix
    const prefix = "";

    let apisCollection = db.getCollection(`${prefix}apis`);
    apisCollection.find({"definitionVersion": "V4"}).forEach((api) => {
    	if (api.type == "SYNC") {
    		api.definition = api.definition.replace('"type" : "sync"', '"type" : "proxy"');
    		api.type = "PROXY";
            	apisCollection.replaceOne({ _id: api._id }, api);
    	}
    	if (api.type == "ASYNC") {
    		api.definition = api.definition.replace('"type" : "async"', '"type" : "message"');
    		api.type = "MESSAGE";
    	        apisCollection.replaceOne({ _id: api._id }, api);
    	}
    });


    let eventsCollection = db.getCollection(`${prefix}events`);
    eventsCollection.find({"type": "PUBLISH_API"}).forEach((event) => {

           event.payload = event.payload.replace('\\"type\\" : \\"sync\\"', '\\"type\\" : \\"proxy\\"');
           event.payload = event.payload.replace('\\"type\\" : \\"async\\"', '\\"type\\" : \\"message\\"');
    	event.payload = event.payload.replace('"type" : "sync"', '"type" : "proxy"');
    	event.payload = event.payload.replace('"type" : "async"', '"type" : "message"');
    		
           eventsCollection.replaceOne({ _id: event._id }, event);
    });
    ```

## Breaking changes from 3.X

Here are the breaking changes from versions 3.X of Gravitee.

### 3.2.0

**Moved Probes configuration**

Probes configuration was moved under deployment.

**Probe default configuration**

Changed probe default configuration. For more information about the change to the default configuration, go to the following [GitHub pull request](https://github.com/gravitee-io/gravitee-api-management/pull/8885).

**Removed the apiSync parameter**

Under gateway.readinessProbe, the apiSync parameter was removed.

### 3.1.55

**Use of smtp.properties.starttlsEnable**

Use smtp.properties.starttls.enable instead of smtp.properties.starttlsEnable.

## Deprecations from 4.x

Here is deprecated functionality for Gravitee 4.X.

### 4.4.0

**gateway.management.http.username deprecation**

To allow JWT auth to be configured, gateway.management.http.username and password have been deprecated to allow JWT auth to be configured. For more information about the deprecation, go to [Changelog](https://github.com/gravitee-io/gravitee-api-management/blob/master/helm/CHANGELOG.md).

## Deprecations from 3.X

Here is deprecated functionality for Gravitee 3.X.

### 3.20.28

**Deprecated api | gateway | ui | portal.security context is removed**

The deprecated api | gateway | ui | portal.security context has been removed.
