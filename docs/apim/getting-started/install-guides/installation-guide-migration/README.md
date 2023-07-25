# Upgrade Guide

## Overview

If you plan to skip versions when you upgrade, ensure that you read the version-specific upgrade notes for each intermediate version. You may be required to perform manual actions as part of the upgrade.

{% hint style="warning" %}
Make sure to run scripts on the correct database since `gravitee` is not always the default database! Check your db name by running `show dbs`.
{% endhint %}

## Upgrade to 4.0

{% hint style="warning" %}
**Coming soon!** The 4.0 upgrade guide will be available after the 4.0 launch.
{% endhint %}



**Running APIM**

* APIM now requires a minimum of JDK 17.
* Starting with 4.0.0, there will no longer be enterprise tags (i.e. suffixed by `-ee`).
* Cluster managers are now available as plugins. Therefore, Hazelcast Cluster Manager has been removed from the default distribution.
* TLS 1.0 and TLS 1.1 protocols are disabled by default. You can still enable these protocols with the proper TCP SSL configuration of the Gateway.

{% code title="gravitee.yaml" %}
```yaml
http:
  ssl:
    tlsProtocols: TLSv1.0, TLSv1.1, TLSv1.2
```
{% endcode %}

Or using environment variables:

```bash
GRAVITEE_HTTP_SSL_TLSPROTOCOLS=TLSv1.0,TLSv1.1,TLSv1.2
```

**Monitoring APIM**

* The name of the sync probe has been changed from `api-sync` to `sync-process` to make it explicit when all sync processes have been completed.
  * The content of the sync handler has slightly changed to align with new concepts:
    * `initialDone`: `true` if the first initial synchronization is done
    * `counter`: the number of iterations
    * `nextSyncTime`: when is the next synchronization
    * `lastOnError`: the latest synchronization with an error
    * `lastErrorMessage`: if `lastOnError` is `true`, the content of the error message
    * `totalOnErrors`: the number of iterations with an error
* v4 APIs currently only support the Elasticsearch reporter. If any other reporter is configured at Gateway level, each v4 API call will produce an error log.
  * However, when using a different reporter, it remains possible to disable analytics on a per-API basis to avoid generating error logs for v4 APIs.

**Managing APIs**

* The endpoint configuration is now split into a shared configuration that can be used at the group level and a configuration dedicated to the endpoint that can override the shared configuration. Existing v4 APIs need to be updated and reconfigured accordingly.
* Removed an unused and outdated feature regarding file synchronization known as `localregistry`.
* Subscriptions with `type: SUBSCRIPTION` have been renamed to `type: PUSH`. Plans have a new field called `mode` that is `STANDARD` by default but needs to be `PUSH` for all Push plans.
  * A [mongo script](https://github.com/gravitee-io/gravitee-api-management/tree/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/4.0.0) is available to migrate the data in MongoDB
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
* Plan selection has been changed to reflect the actual security applied on the API:
  * Keyless
    * Will ignore any type of security (API key, Bearer token, etc.)
    * **If another plan has detected a security token, valid or invalid, all flows assigned to the Keyless plan will be ignored**
  * API Key
    * Retrieve the API key from the request header or query parameters (default header: `X-Gravitee-Api-Key` and default query parameter: `api-key`)
    * While it was previously ignored, **an empty API key is now considered invalid**
  * JWT
    * Retrieve JWT from `Authorization` Header or query parameters
    * Ignore empty `Authorization` Header or any type other than Bearer
    * While it was previously ignored, **an empty Bearer token is now considered invalid**
  * OAuth2
    * Retrieve OAuth2 from `Authorization` Header or query parameters
    * Ignore empty `Authorization` Header or any type other than Bearer
    * While it was previously ignored, **an empty Bearer token is now considered invalid**
* Plugins are now overridden when duplicates (id/type) are found. The plugin zip file having the most recent modified time is kept and others are ignored. Notably, this allows `additionalPlugins` for Helm charts-based deployment to work efficiently without any need to remove bundled plugins.
* The v4 API definition now expects a `FlowExecution` object instead of a `FlowMode` enumeration.
* The `Endpoint` schema is now split into two schemas and the `Endpoint` object contains two string fields to manage the configuration specific to the endpoint and the configuration that may be overridden from the `EndpointGroup`.
* Endpoint name and endpoint group name have to be unique.
*   Analytics have been introduced and the old logging configuration has been moved. The following is only applicable for v4 APIs.

    A new `Analytics` object is available on the API allowing you to configure of all analytics aspects:

    ```json
    "analytics": {
      "enabled" : true|false,
      "logging": { ... },
      "messageSampling" : { ... }
    }
    ```
* The webhook subscription configuration structure has changed.
* `ApiType` enumeration has been renamed: `SYNC` becomes `PROXY` and `ASYNC` becomes `MESSAGE`). v4 APIs and PUBLISH\_API events related to V4 APIs with old values may prevent the service to start properly. **The following script migrates data for mongodb:**

```
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
