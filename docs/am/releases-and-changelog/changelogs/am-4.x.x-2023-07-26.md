---
description: >-
  This page contains the changelog entries for AM 4.0 and any future minor or
  patch AM 4.x.x releases
---

# AM 4.x.x (2023-07-26)

## Gravitee Access Management 4.0 - July 20, 2023

For more in-depth information on what's new, please refer to the [Gravitee AM 4.0 release notes](../release-notes.md).

<details>

<summary>What's new</summary>

**Enterprise Edition**

Some plugins are now part of the Enterprise Edition:

* idp-saml2
* idp-ldap
* idp-azure-ad
* idp-franceconnect
* idp-salesforce
* factor-call
* factor-sms&#x20;
* factor-fido2
* factor-http
* factor-recovery-code
* factor-otp-sender
* resource-twilio

**Community Edition**

If you use the Community Edition, for each enterprise feature you will have a dedicated pop-up to suggest the enterprise version.

* Password - Password salt format option
* Flows - add new TOKEN flow
* MFA - initiating MFA Enrollment via OpenID Connect 1.0
* Send email verification link
* \[Admin] Be able to re-trigger verification email
* Passwordless - Name passwordless device

**Gateway**

* **\[gateway]\[audit]:** It is impossible to see the user that consented the user consent in the audit log https://github.com/gravitee-io/issues/issues/9049\[#9049]
* **\[gateway]\[mfa]:** Allow OTP factor to handle clock drift issues https://github.com/gravitee-io/issues/issues/9074\[#9074]

**Management API**

* Create account with uppercase username https://github.com/gravitee-io/issues/issues/8966\[#8966]

**Other**

* Index name too long https://github.com/gravitee-io/issues/issues/8814\[#8814]
* \[policies] allow Enrich User Profile policy to accept objects as new claims
* WebAuthn post login flow does not contain webAuthnCredentialId
* Column messages in i18n\_dictionary\_entries  table has too little characters

</details>

<details>

<summary>Breaking Changes</summary>

## Running APIM

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

## **Monitoring APIM**

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

## **Managing APIs**

*   The endpoint configuration is now split into:

    * A shared configuration that can be used at the group level
    * A configuration dedicated to the endpoint that can override the shared configuration.&#x20;

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

</details>
