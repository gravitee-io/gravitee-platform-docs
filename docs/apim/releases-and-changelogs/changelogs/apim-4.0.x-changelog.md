---
description: >-
  This page contains the changelog entries for APIM 4.0.x and any future patch
  APIM 4.0.x releases
---

# APIM 4.0.x

## Gravitee API Management 4.0.5 - August 28, 2023

<details>

<summary>Bug fixes</summary>

**Management API**

* Primary owner can remove himself from application with Management API [#9171](https://github.com/gravitee-io/issues/issues/9171)
* v4 API analytics sampling not mapped on get or export [#9203](https://github.com/gravitee-io/issues/issues/9203)

**Console**

* A right-click on an item link in the side navigation menu does not allow "open in a new tab" [#9146](https://github.com/gravitee-io/issues/issues/9146)
* 503 errors when tenants are specified [#9176](https://github.com/gravitee-io/issues/issues/9176)
* Redeploy banner not shown when new plan published [#9200](https://github.com/gravitee-io/issues/issues/9200)

**Other**

* Unable to connect to a self-signed ElasticSearch due to multiple issues [#9208](https://github.com/gravitee-io/issues/issues/9208)

</details>

## Gravitee API Management 4.0.4 - August 18, 2023

<details>

<summary>Bug fixes</summary>

**Management API**

* "Export as CSV" on Subscriptions only exports displayed values [#8965](https://github.com/gravitee-io/issues/issues/8965)
* Membership duplication ignores Primary Owner of source API and can create a duplicated membership in the new API [#9184](https://github.com/gravitee-io/issues/issues/9184)
* Page duplication does not update lastContributor attribute [#9185](https://github.com/gravitee-io/issues/issues/9185)

**Console**

* Console Analytics & Logs: 500 error is displayed when trying to view analytics and logs using a date range greater than 90 days [#6777](https://github.com/gravitee-io/issues/issues/6777)
* Health Check Active When Configured Globally but Not Enabled on the Endpoint [#9149](https://github.com/gravitee-io/issues/issues/9149)

**Other**

* Improve permission granulation for environment settings [#9150](https://github.com/gravitee-io/issues/issues/9150)

</details>

## Gravitee API Management 4.0.3 - August 10, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Snappy dependency error when calling Kafka API [#9181](https://github.com/gravitee-io/issues/issues/9181)

**Management API**

* Improve MongoDB indices [#9162](https://github.com/gravitee-io/issues/issues/9162)
* Improve v4 API import [#9163](https://github.com/gravitee-io/issues/issues/9163)
* DB upgrade fails on JDBC repositories 3.20.x to 4.x [#9182](https://github.com/gravitee-io/issues/issues/9182)

**Console**

* After creation of a plan, user should be redirected to the staging view [#9166](https://github.com/gravitee-io/issues/issues/9166)
* Subscription creation is not possible for APIs created with the Kubernetes Operator [#9175](https://github.com/gravitee-io/issues/issues/9175)

</details>

## Gravitee API Management 4.0.2 - August 4, 2023

<details>

<summary>Bug fixes</summary>

**Portal**

* Logout issue on portal [#9156](https://github.com/gravitee-io/issues/issues/9156)

**Other**

* API promotion fails if sharding tags applied on API [#9121](https://github.com/gravitee-io/issues/issues/9121)

</details>

## Gravitee API Management 4.0.1 - August 4, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Log exception parameter of execution failure [#9148](https://github.com/gravitee-io/issues/issues/9148)

**Management API**

* Dashboard for analytics is shown for all environments [#9058](https://github.com/gravitee-io/issues/issues/9058)
* First API export causes API desynchronization [#9059](https://github.com/gravitee-io/issues/issues/9059)
* Creating a plan on a v2 API leads to null values in the description [#9153](https://github.com/gravitee-io/issues/issues/9153)

</details>

## Gravitee API Management 4.0.0 - July 20, 2023

For more in-depth information on what's new, please refer to the [Gravitee APIM 4.0 release notes](../release-notes/gravitee-4.x/apim-4.0.md).

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
* Maintain a unique custom resource definition (CRD) for your API across all Gravitee environments
* Manage application-level CRDs through the Gravitee Kubernetes Operator
* Define the ManagementContext for your CRD and control whether the API should be local or global

**MongoDB Migration Scripts**

* MongoDB migration scripts are now embedded and automatically executed when starting APIM. There is no longer a need to run JavaScript scripts manually.

</details>

<details>

<summary>Breaking Changes</summary>

**EE plugins**

* Starting with APIM 4.0, particular plugins are only available to enterprise customers. [See Gravitee APIM Enterprise Edition](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md) for additional information.

**Running APIM**

* APIM now requires a minimum of JDK 17.
* Starting with 4.0.0, there will no longer be enterprise tags (i.e. suffixed by `-ee`).
* Cluster managers are now available as plugins. Therefore, Hazelcast Cluster Manager has been removed from the default distribution.
* TLS 1.0 and TLS 1.1 protocols are disabled by default. You can still enable these protocols with the proper TCP SSL configuration of the Gateway:

{% code title="gravitee.yaml" %}
```yaml
http:
  ssl:
    tlsProtocols: TLSv1.0, TLSv1.1, TLSv1.2
```
{% endcode %}

or using environment variables:

```bash
GRAVITEE_HTTP_SSL_TLSPROTOCOLS=TLSv1.0,TLSv1.1,TLSv1.2
```

**Docker images**

To be compliant with [CIS\_Docker\_v1.5.0\_L1](https://www.tenable.com/audits/items/CIS\_Docker\_v1.5.0\_L1\_Docker\_Linux.audit:bdcea17ac365110218526796ae3095b1), the Docker images are now using a dedicated user: `graviteeio`.

This means that if you:

* Use the official images and deploy them to Kubernetes, nothing changes.
* Build your own Dockerfile based on Gravitee images, you must ensure the correct rights are set on the files and directories you add to the image.
* Deploy in `openshift`, you have to add the following configuration to your deployment:

```yaml
securityContext:
    runAsGroup: 1000
```

**Monitoring APIM**

* The name of the sync probe has been changed from `api-sync` to `sync-process` to make it explicit when all sync processes have been completed.
* The content of the sync handler has changed slightly to align with new concepts:
  * `initialDone`: `true` if the first initial synchronization is done
  * `counter`: The number of iterations
  * `nextSyncTime`: Time of the next synchronization
  * `lastOnError`: The latest synchronization with an error
  * `lastErrorMessage`: If `lastOnError` is `true`, the content of the error message
  * `totalOnErrors`: The number of iterations with an error
* v4 APIs currently only support the ElasticSearch reporter. If any other reporter is configured at the Gateway level, each v4 API call will produce an error log.
  * When using a different reporter, it remains possible to disable analytics on a per-API basis to avoid generating error logs for v4 APIs.

**Managing APIs**

*   The endpoint configuration is now split into:

    * A shared configuration that can be used at the group level
    * A configuration dedicated to the endpoint that can override the shared configuration.

    Existing v4 APIs need to be updated and reconfigured accordingly.
* An unused and outdated feature regarding file synchronization known as `localregistry` has been removed.
* Subscriptions with `type: SUBSCRIPTION` have been renamed to `type: PUSH`. Plans have a new field called `mode` that is `STANDARD` by default but needs to be `PUSH` for all Push plans.
  * A [mongo script](https://github.com/gravitee-io/gravitee-api-management/tree/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/4.0.0) is available to migrate the data in MongoDB.
* Jupiter mode has been replaced with the v4 emulation engine:
  * `jupiterModeEnabled` configuration has been removed and can no longer be disabled.
  * By default, any v2 API created or imported will emulate V4 Engine.
  * All new requests will use the new `HttpProtocolVerticle` introduced with the V4 engine. The old `ReactorVerticle` has been removed.
  * The default timeout is set to 30s for any request.
*   Security policies such as Keyless, ApiKey, JWT, and Oauth2 have been updated to return a simple Unauthorized message in case of an error. No additional details are provided to protect against a potential attacker. **This impacts both v2 and v4 APIs.** Error keys remain available for error templating. Here is a list of error keys by policy:

    **ApiKey**

    * API\_KEY\_MISSING
    * API\_KEY\_INVALID
    * JWT
      * JWT\_MISSING\_TOKEN
      * JWT\_INVALID\_TOKEN

    **Oauth2**

    * OAUTH2\_MISSING\_SERVER
    * OAUTH2\_MISSING\_HEADER
    * OAUTH2\_MISSING\_ACCESS\_TOKEN
    * OAUTH2\_INVALID\_ACCESS\_TOKEN
    * OAUTH2\_INVALID\_SERVER\_RESPONSE
    * OAUTH2\_INSUFFICIENT\_SCOPE
    * OAUTH2\_SERVER\_UNAVAILABLE
*   Plan selection has been changed to reflect the actual security applied on the API:

    **Keyless**

    * Will ignore any type of security (API key, Bearer token, etc.).
    * **If another plan has detected a security token, valid or invalid, all flows assigned to the Keyless plan will be ignored.**

    **API Key**

    * Retrieve the API key from the request header or query parameters (default header: `X-Gravitee-Api-Key` and default query parameter: `api-key`).
    * While it was previously ignored, **an empty API key is now considered invalid**.

    **JWT**

    * Retrieve JWT from `Authorization` header or query parameters.
    * Ignore empty `Authorization` header or any type other than Bearer.
    * While it was previously ignored, **an empty Bearer token is now considered invalid**.

    **OAuth2**

    * Retrieve OAuth2 from `Authorization` header or query parameters.
    * Ignore empty `Authorization` header or any type other than Bearer.
    * While it was previously ignored, **an empty Bearer token is now considered invalid**.
* Plugins are now overridden when duplicates (id/type) are found. The plugin zip file with the most recent modified time is kept and others are ignored. Notably, this allows `additionalPlugins` for Helm chart-based deployment to operate efficiently without the need to remove bundled plugins.
* The v4 API definition now expects a `FlowExecution` object instead of a `FlowMode` enumeration.
* The Gravitee Expression Language (EL) syntax to access custom API properties has changed from `{#properties}` to `{#api.properties}`.
* The `Endpoint` schema is now split into two schemas and the `Endpoint` object contains two string fields to manage both the configuration specific to the endpoint and the configuration that may be overridden from the `EndpointGroup`.
* Endpoint name and endpoint group name must be unique.
*   Analytics have been introduced and the old logging configuration has been moved. **For v4 APIs only**, a new `Analytics` object is available on the API allowing you to configure all aspects of analytics:

    ```json
    "analytics": {
      "enabled" : true|false,
      "logging": { ... },
      "messageSampling" : { ... }
    }
    ```
* The Webhook subscription configuration structure has changed.
* `ApiType` enumeration has been renamed: `SYNC` becomes `PROXY` and `ASYNC` becomes `MESSAGE`). v4 APIs and PUBLISH\_API events related to V4 APIs with old values may prevent the service to start properly. **The following script migrates data for MongoDB:**

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

**Login Endpoint**

In previous versions, sending a POST request to `/user/login` without an `Authorization` header returned HTTP Response 200.

Starting with 4.0.0, if a POST request to `/user/login` does not have an `Authorization` header, it will receive an HTTP response 401 - Unauthorized.

</details>
