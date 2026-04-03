---
hidden: true
noIndex: true
---

# APIM 4.11.x
 
## Gravitee API Management 4.11.0 - April 3, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* SSL enforcement policy will return a 403 if if the SSL connection is terminated at the ingress level [#11234](https://github.com/gravitee-io/issues/issues/11234)
* Duplicate traceparent header [#11248](https://github.com/gravitee-io/issues/issues/11248)
* The Health Check of the API V4 is not working as expected with tenant [#11275](https://github.com/gravitee-io/issues/issues/11275)
* Secret resolution failure in SPG when combined with multiple policies [#11279](https://github.com/gravitee-io/issues/issues/11279)
* gravitee-resource-cache-redis leaks LettuceConnectionFactory on every API redeploy [#11314](https://github.com/gravitee-io/issues/issues/11314)

**Management API**

* Promotion Button in UI Yields Parsing Error [#11277](https://github.com/gravitee-io/issues/issues/11277)
* Unable to resend or retrigger expired sign-up confirmation links [#11295](https://github.com/gravitee-io/issues/issues/11295)
* Error when deleting an API with pages [#11308](https://github.com/gravitee-io/issues/issues/11308)

**Console**

* Not able search/filter logs by path [#11255](https://github.com/gravitee-io/issues/issues/11255)
* v4 API promotions are stuck in a pending state [#11281](https://github.com/gravitee-io/issues/issues/11281)
* Unable to reset the password [#11289](https://github.com/gravitee-io/issues/issues/11289)

**Other**

* JSON Web Token policy always returns fails to validate token [#11233](https://github.com/gravitee-io/issues/issues/11233)
* Changing plan order removes the plan flows [#11247](https://github.com/gravitee-io/issues/issues/11247)
* OAuth2 token acquisition failure is silently swallowed [#11250](https://github.com/gravitee-io/issues/issues/11250)
* Webhook Logs toggle not updated after save/publish [#11257](https://github.com/gravitee-io/issues/issues/11257)
* Once I migrate certain V2 APIs to V4, they disappear from the list (/apis) in the UI [#11268](https://github.com/gravitee-io/issues/issues/11268)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* MCP Proxy: serve .well-known/oauth-protected-resource at RFC 9728 compliant host-scoped URL [#11299](https://github.com/gravitee-io/issues/issues/11299)

**Management API**

* Intermittent 500 Error during API Creation: primaryOwner.notFound [#11229](https://github.com/gravitee-io/issues/issues/11229)

**Other**

* Support client_secret_basic authentication for OAuth2 token endpoint [#11249](https://github.com/gravitee-io/issues/issues/11249)
* Update IP Filtering policy documentation in  [#11251](https://github.com/gravitee-io/issues/issues/11251)
* Add the scope field to the WWW-Authenticate header in the OAuth2 Policy [#11307](https://github.com/gravitee-io/issues/issues/11307)

</details>



