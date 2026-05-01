# APIM 4.11.x
 
## Gravitee API Management 4.11.5 - April 30, 2026
<details>

<summary>Bug Fixes</summary>

**Management API**

* NullPointerException when opening the Audit Log page in the Management UI, caused by a missing DASHBOARD reference type mapping in the service layer. [#11339](https://github.com/gravitee-io/issues/issues/11339)
* Creating a subscription on an api key plan results on two api keys generation [#11347](https://github.com/gravitee-io/issues/issues/11347)
* Console sends undefined API ID for V2 API when closing plan [#11367](https://github.com/gravitee-io/issues/issues/11367)

**Console**

* API members with Member Read and Definition Update permissions can modify group access [#11259](https://github.com/gravitee-io/issues/issues/11259)
* Re: Search user api wrong result when paginated [#11311](https://github.com/gravitee-io/issues/issues/11311)
* Roles permissions are in-consistent.  [#11324](https://github.com/gravitee-io/issues/issues/11324)

**Portal**

* Default portal navigation items are created on every Cloud environment update [#11369](https://github.com/gravitee-io/issues/issues/11369)

**Other**

* Consuming Kafka tombstone messages causes NullPointerException [#11353](https://github.com/gravitee-io/issues/issues/11353)
* PromptGuardRails policy - contentChecks filter not applied to block reason, exposing unintended classifier labels in error response [#11373](https://github.com/gravitee-io/issues/issues/11373)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Some warnings displayed after upgrade to v 4.7.x [#10862](https://github.com/gravitee-io/issues/issues/10862)

**Management API**

* Some warnings displayed after upgrade to v 4.7.x [#10862](https://github.com/gravitee-io/issues/issues/10862)
* Include API metadata in the same endpoint response as the rest of the API data [#10971](https://github.com/gravitee-io/issues/issues/10971)

**Console**

* Portal navigation items: open context menu with right click [#11384](https://github.com/gravitee-io/issues/issues/11384)

**Other**

* Add opt-in URL path normalization to the Resource Filtering policy [#11337](https://github.com/gravitee-io/issues/issues/11337)

</details>


 
## Gravitee API Management 4.11.4 - April 21, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* Unable to edit inline Markdown document/page for v2 APIs and portal documentation [#11348](https://github.com/gravitee-io/issues/issues/11348)

**Portal**

* Group users of an API cannot see it in the Next Gen Portal [#11360](https://github.com/gravitee-io/issues/issues/11360)
* Documentation items permissions are different from catalog permissions [#11361](https://github.com/gravitee-io/issues/issues/11361)

</details>


 
## Gravitee API Management 4.11.3 - April 21, 2026
<details>

<summary>Bug Fixes</summary>

**Management API**

* Users that do not have any API Products permissions receive an error on the general configuration page of v4 APIs [#11350](https://github.com/gravitee-io/issues/issues/11350)

**Console**

* Users that do not have any API Products permissions receive an error on the general configuration page of v4 APIs [#11350](https://github.com/gravitee-io/issues/issues/11350)

**Helm Charts**

* 4.11 upgrade attempt with helm failing with openshift context error  [#11359](https://github.com/gravitee-io/issues/issues/11359)

</details>


 
## Gravitee API Management 4.11.2 - April 17, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Prometheus scrapping error: scrape request times out [#11036](https://github.com/gravitee-io/issues/issues/11036)
* Data masking policy masks the whole payload [#11303](https://github.com/gravitee-io/issues/issues/11303)
* Gateway ConcurrentModificationException during request dispatch [#11312](https://github.com/gravitee-io/issues/issues/11312)
* OpenAPI Specification Validation Policy - Validation errors [#11330](https://github.com/gravitee-io/issues/issues/11330)
* Dictionaries not available in v2 API resource configuration [#11346](https://github.com/gravitee-io/issues/issues/11346)

**Management API**

* V2 API failed to migrate to v4 due to endpoint configuration [#11264](https://github.com/gravitee-io/issues/issues/11264)
* v4 API logs are inaccessible when the analytics type is none [#11297](https://github.com/gravitee-io/issues/issues/11297)

**Console**

* endpointGroups.sharedConfiguration.headers and endpointGroups.sharedConfiguration.http Cannot Be Applied Together in v4 api defintion [#11163](https://github.com/gravitee-io/issues/issues/11163)
* endpointGroups.sharedConfiguration.headers and endpointGroups.sharedConfiguration.http Cannot Be Applied Together in v4 api defintion [#11168](https://github.com/gravitee-io/issues/issues/11168)
* The filters applied in the v4 API logs are not preserved  [#11302](https://github.com/gravitee-io/issues/issues/11302)

**Other**

* Warning - Failed to evaluate duration [#11341](https://github.com/gravitee-io/issues/issues/11341)

</details>

<details>

<summary>Improvements</summary>

**Console**

* Add Entra ID to the OAuth2 API Resources [#11345](https://github.com/gravitee-io/issues/issues/11345)

**Other**

* When returning the protected resource metadata from the OAuth2 policy, it should include the scopes [#11343](https://github.com/gravitee-io/issues/issues/11343)

**Helm chart**

* Improve JDBC driver delivery options in the Helm chart:
  * `auto` uses bundled PostgreSQL, MariaDB, and SQL Server drivers, and uses startup download for MySQL and other custom JDBC families
  * `image` allows using a dedicated customer-provided JDBC image instead of downloading the driver at startup
  * `download` keeps the explicit startup download mode
  * `preinstalled` allows using JDBC drivers already baked into custom API and Gateway runtime images, without JDBC runtime provisioning
* Validate `jdbc.driverSource` values during chart rendering and fail on unsupported values.

</details>


 
## Gravitee API Management 4.11.1 - April 4, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* Revert: Unable to reset the password [#11289](https://github.com/gravitee-io/issues/issues/11289)

</details>


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

* Support client\_secret\_basic authentication for OAuth2 token endpoint [#11249](https://github.com/gravitee-io/issues/issues/11249)
* Update IP Filtering policy documentation in [#11251](https://github.com/gravitee-io/issues/issues/11251)
* Add the scope field to the WWW-Authenticate header in the OAuth2 Policy [#11307](https://github.com/gravitee-io/issues/issues/11307)

</details>
