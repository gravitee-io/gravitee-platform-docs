# Upgrade Guide

{% hint style="danger" %}
**Upgrade your license file**

If you are an existing Gravitee Enterprise customer upgrading to 4.x, please make sure that you upgrade your Gravitee license file. Reach out to your Customer Success Manager or Support team in order to receive a new 4.x license.
{% endhint %}

## Overview

Upgrading to APIM 4.5 is deployment-specific. The 4.0 breaking changes cited below must be noted and/or adopted for a successful upgrade.

{% hint style="warning" %}
* **If your upgrade will skip versions:** Read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.
* **Run scripts on the correct database:** `gravitee` is not always the default database. Run `show dbs` to return your database name.
* **Ensure that you are aware of the breaking changes and deprecated functionality:** For more information about the breaking changes and deprecated functionality, see [Breaking Changes and Deprecations](breaking-changes-and-deprecations.md).
{% endhint %}

## EE plugins

Particular plugins are only available to enterprise customers. [See Gravitee APIM Enterprise Edition](docs/apim/4.7/overview/enterprise-edition.md) for additional information.

## Running APIM

* Depending on your version of APIM, you must run the following versions of Java:
  * For versions 4.6 and before, APIM requires at least Java17.
  * For version for 4.7 and later, APIM requires at least Java21.&#x20;
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

## **Monitoring APIM**

* The name of the sync probe has been changed from `api-sync` to `sync-process` to make the completion of all sync processes explicit.
* The content of the sync handler has changed slightly to align with new concepts:
  * `initialDone`: `true` if the first initial synchronization is done
  * `counter`: The number of iterations
  * `nextSyncTime`: Time of the next synchronization
  * `lastOnError`: The latest synchronization with an error
  * `lastErrorMessage`: If `lastOnError` is `true`, the content of the error message
  * `totalOnErrors`: The number of iterations with an error

## **Managing APIs**

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
* The Webhook subscription configuration structure has changed.
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

## Updating the Cloud connection

APIM 4.2 brings improved management of multi-tenancy mode, where one APIM installation now tends to multiple tenants on either the Organization on Environment level.\
\
Multi-tenancy support in Gravitee 4.2 necessitated changes to both APIM and Cloud, but customer deployments may continue to function as `standalone` APIM installations. A `standalone` installation behaves the same as APIM 4.1 connected to Cloud.\
\
APIM installations connected to Cloud require changes to the Management API's `gravitee.yml` file.

### APIM 4.2 with Cloud connected

{% hint style="warning" %}
The user must edit the Management API's `gravitee.yaml`.
{% endhint %}

If an APIM installation connected to Cloud is upgraded to 4.2, the user must make the following changes to the Management API's `gravitee.yaml` file for the installation to function as `standalone`:

```yaml
installation:
  type: standalone # Could be either standalone, multi-tenant; Default is standalone.
  # Specify the URL of Management API of this instance, mandatory if you want to connect it to Cloud
  api:
    # Specify the URLs of Management API, mandatory if you want to connect it to Cloud with a standalone installation
    url: http://localhost:8083
    proxyPath:
      management: ${http.api.management.entrypoint} # By default /management
      portal: ${http.api.portal.entrypoint}  # By default /portal
  standalone:
    # Specify the URL of Console UI of this instance, mandatory if you want to connect it to Cloud with a standalone installation
    console:
      url: http://localhost:3000
    # Specify the URL of Portal UI of this instance
    portal:
      url: http://localhost:4100
```

### APIM 4.2+ and multiple Consoles/Portals in a connected Cloud

{% hint style="warning" %}
The user must edit the Management API's `gravitee.yaml`.
{% endhint %}

If an APIM installation with multiple Consoles and/or Portals set up in a connected Cloud is upgraded to 4.2, the user must make the following changes to the Management API's `gravitee.yaml` file for the installation to function as `standalone`:

```yaml
installation:
  type: standalone # Could be either standalone, multi-tenant; Default is standalone.
  # Specify the URL of Management API of this instance, mandatory if you want to connect it to Cloud
  api:
    proxyPath:
      management: ${http.api.management.entrypoint} # By default /management
      portal: ${http.api.portal.entrypoint}  # By default /portal
  standalone:
    api:
    # Specify the URLs of Management API, mandatory if you want to connect it to Cloud with a standalone installation
      url: http://localhost:8083
    # Specify the URL of Console UI of this instance, mandatory if you want to connect it to Cloud with a standalone installation
    console:
      urls:
        - orgId: DEFAULT
          url: http://localhost:3000
        - orgId: organization#2
          url: http:/localhost:3001
    portal:
      urls:
        - envId: DEFAULT
          url: http://localhost:4100
        - envId: environment#2
          url: http:/localhost:4101
```

## APIM 4.4.+ & Hybrid Gateways:

Starting with APIM 4.4.0, gateways need to explicitly disable certificate checks. The default "trust all" value was `true` it is now `false` for management of type "http".

You **need to** update `gravitee.yml` or your Helm's `values.yaml` if your configuration match **all of** the following:

* You were using a secured connection between Hybrid Gateway and Bridge Server (Gateway or Management API)
* You were using the default value (unset param)
* You were using a non-public CA to sign your certificate
* Your \`gateway.http.management.ssl configuration do not use a trust store to accept the server certificate.

The can explicitly disable certificate checks in the `gravitee.yaml`:

```yaml
management:
  http:
    ssl:
      trustAll: true
```

Or if you are using Helm charts, you can set it in your `values.yaml` file:

```yaml
gateway:
  management:
    http:
      ssl:
        trustAll: true
```

Or you can use an environment variable:

```
GRAVITEE_MANAGEMENT_HTTP_SSL_TRUSTALL="true"
```

{% hint style="warning" %}
The "trust all" configuration parameter was formerly named `trustall`, it is now named `trustAll` for consistency. To avoid a breaking change both names work, but the former has been deprecated.
{% endhint %}
