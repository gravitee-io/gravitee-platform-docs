---
description: Documentation about apim 4.9.x in the context of APIs.
metaLinks:
  alternates:
    - /broken/spaces/bGmDEarvnV52XdcOiV8o/pages/0oVQWkw8tEgZsegmlu1I
---

# APIM 4.9.x
 
## Gravitee API Management 4.9.16 - March 27, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* SSL enforcement policy will return a 403 if if the SSL connection is terminated at the ingress level [#11234](https://github.com/gravitee-io/issues/issues/11234)
* Dynamic dictionary not deployed when environment is not the default one [#11236](https://github.com/gravitee-io/issues/issues/11236)
* JWT plans can only have one subscription transfer [#11246](https://github.com/gravitee-io/issues/issues/11246)
* Duplicate traceparent header [#11248](https://github.com/gravitee-io/issues/issues/11248)
* The Health Check of the API V4 is not working as expected with tenant [#11275](https://github.com/gravitee-io/issues/issues/11275)
* Secret resolution failure in SPG when combined with multiple policies [#11279](https://github.com/gravitee-io/issues/issues/11279)

**Management API**

* Promotion Button in UI Yields Parsing Error [#11277](https://github.com/gravitee-io/issues/issues/11277)

**Console**

* Missing fields when creating an alert [#10802](https://github.com/gravitee-io/issues/issues/10802)
* Locations in Admin Console time out due to requests being sent to old Groups API Endpoint where pagination is not implemented [#10843](https://github.com/gravitee-io/issues/issues/10843)
* \[Logging] API Level logs missing details if one of the checkbox is unchecked [#11116](https://github.com/gravitee-io/issues/issues/11116)
* Not able search/filter logs by path [#11255](https://github.com/gravitee-io/issues/issues/11255)

**Other**

* Bootstrap URL for Kafka DLQ endpoint does not support Expression Language [#10906](https://github.com/gravitee-io/issues/issues/10906)
* Application menu not showing up on first login [#10951](https://github.com/gravitee-io/issues/issues/10951)
* Promotion request is not found in Audit of the target environment. [#11065](https://github.com/gravitee-io/issues/issues/11065)
* json-validation policy error key [#11152](https://github.com/gravitee-io/issues/issues/11152)
* Agent Mesh - Generate Tools from OpenAPI [#11165](https://github.com/gravitee-io/issues/issues/11165)
* \[V4 Emulation] IllegalStateException: HTTP/2 streams failing due to missing Content-Length validation [#11191](https://github.com/gravitee-io/issues/issues/11191)
* API export as CRD fails if API has no (direct) members [#11193](https://github.com/gravitee-io/issues/issues/11193)
* FreeMarker template error in v4-message-log.ftl when Kafka metadata contains byte\[] [#11220](https://github.com/gravitee-io/issues/issues/11220)
* OpenAPI Specification Validation Policy - Validation errors [#11223](https://github.com/gravitee-io/issues/issues/11223)
* MCP Tool Generation: Operation descriptions and business rules are missing from generated tools [#11226](https://github.com/gravitee-io/issues/issues/11226)
* Detaching an API looses API context after confirmation [#11239](https://github.com/gravitee-io/issues/issues/11239)
* Kafka gateways is throwing recurrent "Thread blocked" errors [#11242](https://github.com/gravitee-io/issues/issues/11242)
* Changing plan order removes the plan flows [#11247](https://github.com/gravitee-io/issues/issues/11247)
* OAuth2 token acquisition failure is silently swallowed [#11250](https://github.com/gravitee-io/issues/issues/11250)
* Once I migrate certain V2 APIs to V4, they disappear from the list (/apis) in the UI [#11268](https://github.com/gravitee-io/issues/issues/11268)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Api Categories exported by IDs instead of names [#10944](https://github.com/gravitee-io/issues/issues/10944)
* Allow for larger values in APIM Dictionary properties [#11047](https://github.com/gravitee-io/issues/issues/11047)
* \[gravitee-policy-aws-lambda] Unexpected Retry and Duplicate Invocation of AWS Lambda via Gravitee API Gateway [#11096](https://github.com/gravitee-io/issues/issues/11096)
* "Thread blocked" error received when invalid creadentials set for Elastic Search [#11184](https://github.com/gravitee-io/issues/issues/11184)
* Support client_secret_basic authentication for OAuth2 token endpoint [#11249](https://github.com/gravitee-io/issues/issues/11249)

</details>


 
## Gravitee API Management 4.9.15 - March 12, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Not able to reference kubernetes secret in Sharedpolicy group resource and then use it in api for use case such as Oauth server authentication [#11041](https://github.com/gravitee-io/issues/issues/11041)
* Missing node_health prometheus metric with 4.9.11 [#11095](https://github.com/gravitee-io/issues/issues/11095)
* Keystore watch stop working after KeyStore failed to load [#11121](https://github.com/gravitee-io/issues/issues/11121)

**Management API**

* User Attributes Not Resolved in Mail Templates [#11207](https://github.com/gravitee-io/issues/issues/11207)

**Console**

* Entrypoints mapping display bug. [#11053](https://github.com/gravitee-io/issues/issues/11053)
* Dynamic property - Fix the help message under cron expression [#11140](https://github.com/gravitee-io/issues/issues/11140)
* Broken 'Open log settings' link in V4 Protocol Mediation API log details [#11167](https://github.com/gravitee-io/issues/issues/11167)
* Custom statistics on the User-Agent [#11203](https://github.com/gravitee-io/issues/issues/11203)

**Portal**

* Button "back to category" disappears in dev portal [#11204](https://github.com/gravitee-io/issues/issues/11204)
* Ui bug in developer portal [#11214](https://github.com/gravitee-io/issues/issues/11214)

**Other**

* Kafka OAUTHBEARER reconnection not triggered by the Kafka Client with JWT Plan [#10491](https://github.com/gravitee-io/issues/issues/10491)
* 404 (Not Found) requests not visible in Console Analytics despite correct configuration [#11014](https://github.com/gravitee-io/issues/issues/11014)
* JSON Web Token policy always returns fails to validate token [#11233](https://github.com/gravitee-io/issues/issues/11233)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Intermittent 500 Error during API Creation: primaryOwner.notFound [#11229](https://github.com/gravitee-io/issues/issues/11229)

</details>


 
## Gravitee API Management 4.9.14 - February 27, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Failover retries leak endpoint query parameters across attempts in HTTP proxy connector [#11164](https://github.com/gravitee-io/issues/issues/11164)
* Gateway cannot auto-recover if Elasticsearch goes down and then comes back online [#11176](https://github.com/gravitee-io/issues/issues/11176)

**Management API**

* The mAPI is unreachable when a connection cannot be made to Cloud [#10307](https://github.com/gravitee-io/issues/issues/10307)
* V4 Migration: 400 Error on endpoint updates when 'System Proxy' is enabled in V2 [#11113](https://github.com/gravitee-io/issues/issues/11113)
* Automatic cleanup failure in commands table due to missing expired_at values [#11136](https://github.com/gravitee-io/issues/issues/11136)

**Console**

* \[UI Bug] LDAP Resource "User search base" field auto-populates with default value on edit [#11072](https://github.com/gravitee-io/issues/issues/11072)

**Portal**

* API Catalog API Visibility [#11155](https://github.com/gravitee-io/issues/issues/11155)

**Other**

* Promotion requests accepted from the main dashboard are not auto refreshed [#11062](https://github.com/gravitee-io/issues/issues/11062)
* Assign content policy doesn't support message.topic for kafka native API [#11194](https://github.com/gravitee-io/issues/issues/11194)
* 500 Internal Error against the Tasks endpoint [#11208](https://github.com/gravitee-io/issues/issues/11208)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Fix performance degradation in 4.9 compared to 4.8 [#11211](https://github.com/gravitee-io/issues/issues/11211)
* Make 401 Error Details Available in Response [#11212](https://github.com/gravitee-io/issues/issues/11212)

**Console**

* API Mgmt Management Console task list takes too long to load [#11049](https://github.com/gravitee-io/issues/issues/11049)
* Debug Mode Enhancement: Increase Timeout & Implement Long-Poll UI [#11180](https://github.com/gravitee-io/issues/issues/11180)

**Helm Charts**

* Make 401 Error Details Available in Response [#11212](https://github.com/gravitee-io/issues/issues/11212)

**Other**
* OpenAPI Validation Policy fails with OAS 3.1 discriminator schemas [#10763](https://github.com/gravitee-io/issues/issues/10763)

</details>


 
## Gravitee API Management 4.9.13 - February 13, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* \[Protocol Mediation] subscription is not available in EL during PUBLISH and SUBSCRIBE phase [#11101](https://github.com/gravitee-io/issues/issues/11101)
* Error 503 and Thread Blocked from weighted_round_robin  [#11132](https://github.com/gravitee-io/issues/issues/11132)
* Gateway - Secrets with long content  [#11144](https://github.com/gravitee-io/issues/issues/11144)

**Management API**

* Multiple PRIMARY_OWNERs after "Transfer Ownership" [#11045](https://github.com/gravitee-io/issues/issues/11045)
* Re: Unable to view log of API unless Instance READ permission is added to API Publisher [#11051](https://github.com/gravitee-io/issues/issues/11051)
* Http Client Common Configuration Regression [#11159](https://github.com/gravitee-io/issues/issues/11159)

**Console**

* Re: Unable to view log of API unless Instance READ permission is added to API Publisher [#11051](https://github.com/gravitee-io/issues/issues/11051)
* Permission Denied on IPV4_ONLY=true [#11130](https://github.com/gravitee-io/issues/issues/11130)

**Other**

* \[Kafka Gateway] Azure Service Bus fails with higher ApiVersions [#11109](https://github.com/gravitee-io/issues/issues/11109)
* \[Kafka Gateway] Bad ApiVersions when gateway doesn't supports the min version of an api key [#11118](https://github.com/gravitee-io/issues/issues/11118)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Request response times spike when health checks are performed [#11141](https://github.com/gravitee-io/issues/issues/11141)

**Other**

* \[gravitee-policy-callout-http] Allow to evaluate variables as Object [#11137](https://github.com/gravitee-io/issues/issues/11137)

</details>


 
## Gravitee API Management 4.9.12 - January 30, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Double / when in the called url when using Service discovery plugin [#11076](https://github.com/gravitee-io/issues/issues/11076)

**Management API**

* Impossible to add a new group member [#11050](https://github.com/gravitee-io/issues/issues/11050)
* Prevent multiple primary owners through ownership transfer [#11102](https://github.com/gravitee-io/issues/issues/11102)

**Portal**

* \[PORTAL] Filtering Problem  [#11028](https://github.com/gravitee-io/issues/issues/11028)

**Other**

* SSL enforcement policy issue [#11009](https://github.com/gravitee-io/issues/issues/11009)
* Group Management follow-up (still broken in some places) [#11042](https://github.com/gravitee-io/issues/issues/11042)
* \[Kafka Gateway] Side effects on upstream connection when EL is used to configure SASL [#11103](https://github.com/gravitee-io/issues/issues/11103)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* JAVA_OPTS displays password parameters in gateway logs [#11073](https://github.com/gravitee-io/issues/issues/11073)

**Management API**

* JAVA_OPTS displays password parameters in gateway logs [#11073](https://github.com/gravitee-io/issues/issues/11073)
* \[Perf] Improve APIM management API overall performance [#11088](https://github.com/gravitee-io/issues/issues/11088)

</details>


 
## Gravitee API Management 4.9.11 - January 16, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* Save changes button does not appear on policy studio when jwt policy is dropped [#11011](https://github.com/gravitee-io/issues/issues/11011)

**Other**

* User is unable to use guard rails policy with debug mode [#11070](https://github.com/gravitee-io/issues/issues/11070)

</details>



## Gravitee API Management 4.9.10 - December 19, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* 504 Gateway Timeout logs show server as Null [#10295](https://github.com/gravitee-io/issues/issues/10295)
* V4 WebSocket backend fails when sec-websocket-protocol header is provided [#10987](https://github.com/gravitee-io/issues/issues/10987)

**Management API**

* Duplicate user entries appearing randomly in search results [#10744](https://github.com/gravitee-io/issues/issues/10744)
* Portal notification configuration upgrade failure after APIM upgrade [#11030](https://github.com/gravitee-io/issues/issues/11030)

**Console**

* Management UIs logout URL missing id\_token\_hint [#10399](https://github.com/gravitee-io/issues/issues/10399)
* Group Roles not shown until page refresh when added to a user [#11026](https://github.com/gravitee-io/issues/issues/11026)
* Headers in logs for V4 messages APIs not loading correctly in UI [#11027](https://github.com/gravitee-io/issues/issues/11027)

**Portal**

* Developer portal is impossible to use with a lot of applications [#10784](https://github.com/gravitee-io/issues/issues/10784)

**Other**

* Shared Policy Group data cache lost on API redeploy [#10797](https://github.com/gravitee-io/issues/issues/10797)
* Healthcheck on api migrated to V4 does not work [#10982](https://github.com/gravitee-io/issues/issues/10982)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Improve “no subscription” error message formatting & masking for error transparency flow [#11032](https://github.com/gravitee-io/issues/issues/11032)

</details>

## Gravitee API Management 4.9.9 - December 10, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Incorrect HTTP request metrics for V4 APIs [#10994](https://github.com/gravitee-io/issues/issues/10994)
* Revert - disabled resource has no effect \[10831] [#11019](https://github.com/gravitee-io/issues/issues/11019)

**Management API**

* Silent failure when changing email to one already in use [#11017](https://github.com/gravitee-io/issues/issues/11017)

**Console**

* Silent failure when changing email to one already in use [#11017](https://github.com/gravitee-io/issues/issues/11017)

</details>

## Gravitee API Management 4.9.8 - December 5, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* v2 API with SSE Endpoint not receiving connection close event from client [#10766](https://github.com/gravitee-io/issues/issues/10766)
* Disabled OAuth2 resource has no effect - APIM OAuth2 plans continue allowing access [#10831](https://github.com/gravitee-io/issues/issues/10831)

**Management API**

* IDP role mapping computed each authentication cannot replace admin-set roles for IDP users [#10497](https://github.com/gravitee-io/issues/issues/10497)
* V4 APIs created via import always set the importing user as the primary owner [#10854](https://github.com/gravitee-io/issues/issues/10854)
* API out of sync using dynamic properties [#10917](https://github.com/gravitee-io/issues/issues/10917)
* Make API list search case insensitive [#10970](https://github.com/gravitee-io/issues/issues/10970)
* Redoc set as default is not working [#10988](https://github.com/gravitee-io/issues/issues/10988)
* Missing endpoint-request-uri in V4 API logs [#11004](https://github.com/gravitee-io/issues/issues/11004)

**Console**

* For a user, it should not be possible to change its group API role to something else than PO, if the group is a PO of at least one API. [#10685](https://github.com/gravitee-io/issues/issues/10685)
* V4 APIs created via import always set the importing user as the primary owner [#10854](https://github.com/gravitee-io/issues/issues/10854)

**Other**

* Cache-redis plugin 4.0.2 JDBC issue [#11013](https://github.com/gravitee-io/issues/issues/11013)

</details>

<details>

<summary>Improvements</summary>

**Console**

* V4 API log attribute order inconsistency [#10995](https://github.com/gravitee-io/issues/issues/10995)

**Other**

* Handle X-Forwarded-Prefix and X-Original-Forwarded-Host headers to properly build links for portal [#10993](https://github.com/gravitee-io/issues/issues/10993)
* JWT policy missing in error transparency execution logs [#11005](https://github.com/gravitee-io/issues/issues/11005)
* Client aborted during response missing in error transparency execution logs [#11006](https://github.com/gravitee-io/issues/issues/11006)

</details>

## Gravitee API Management 4.9.7 - November 25, 2025

<details>

<summary>Bug Fixes</summary>

**Management API**

* After deleting a federated API, the API count is not updating [#10980](https://github.com/gravitee-io/issues/issues/10980)

**Other**

* Intermittent 503s on OAuth2 Introspection due to Stale Connection Reuse [#10984](https://github.com/gravitee-io/issues/issues/10984)

</details>

## Gravitee API Management 4.9.6 - November 21, 2025

<details>

<summary>Bug Fixes</summary>

**Management API**

* DCR Provider: Trust Store Persistence Failure on PostgreSQL [#10925](https://github.com/gravitee-io/issues/issues/10925)
* Valid OpenAPI are being rejected at import for v4 APIs [#10975](https://github.com/gravitee-io/issues/issues/10975)
* Audit 4.9.3 menu not working [#10981](https://github.com/gravitee-io/issues/issues/10981)

**Console**

* Applications Graph analytics issue [#10837](https://github.com/gravitee-io/issues/issues/10837)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Performance Optimisation for API Configuration Validation [#10989](https://github.com/gravitee-io/issues/issues/10989)

</details>

## Gravitee API Management 4.9.5 - November 17, 2025

<details>

<summary>Bug Fixes</summary>

**Console**

* Export was exposing unwanted `hrid` field in CRD export [#10937](https://github.com/gravitee-io/issues/issues/10937)

**Other**

* Lost api notifications after upgrade [#10924](https://github.com/gravitee-io/issues/issues/10924)
* Missing sharding tag on plan after migration from 4.4.9 to 4.9.2 [#10959](https://github.com/gravitee-io/issues/issues/10959)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Redis - Unable to connect to Redis WRONGPASS invalid username-password pair or user is disabled [#10966](https://github.com/gravitee-io/issues/issues/10966)

</details>

## Gravitee API Management 4.9.4 - November 14, 2025

<details>

<summary>Bug Fixes</summary>

**Management API**

* Shared policy not being executed in debug mode [#10885](https://github.com/gravitee-io/issues/issues/10885)

**Portal**

* Documentation pages in new dev portal show misaligned content [#10947](https://github.com/gravitee-io/issues/issues/10947)

**Other**

* Developer portal links disappear post-upgrade to 4.9 [#10956](https://github.com/gravitee-io/issues/issues/10956)
* AI Prompt Token Tracking Policy skipped with Non-Strict application/json Content-Type [#10964](https://github.com/gravitee-io/issues/issues/10964)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* User groups API now supports filtering by environmentId query parameter [#10788](https://github.com/gravitee-io/issues/issues/10788)

**Other**

* Allow Json validation policy to use a nullable field if provided in schema [#10828](https://github.com/gravitee-io/issues/issues/10828)
* OpenTelemetry API gateway attribute values and trace linking [#10898](https://github.com/gravitee-io/issues/issues/10898)

</details>

## Gravitee API Management 4.9.3 - November 7, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Allow disabling Vertx Native Transport [#10889](https://github.com/gravitee-io/issues/issues/10889)
* API are not updated in the Gateway when using JDBC repository [#10930](https://github.com/gravitee-io/issues/issues/10930)
* Sec-WebSocket-Protocol header not propagated in WebSocket connections for v4 APIs [#10950](https://github.com/gravitee-io/issues/issues/10950)

**Management API**

* Using payload filter in v2 API logs does not always return correct number of results [#10747](https://github.com/gravitee-io/issues/issues/10747)
* Difference between policy names based on the creation method. [#10803](https://github.com/gravitee-io/issues/issues/10803)
* Search API feature not working on Developer Portal [#10892](https://github.com/gravitee-io/issues/issues/10892)
* Path mapping on import fails for certain paths [#10909](https://github.com/gravitee-io/issues/issues/10909)

**Console**

* Applied filter tags disappear in log view [#10931](https://github.com/gravitee-io/issues/issues/10931)

**Other**

* UI Text Overflow in "User Permissions" Tab [#10882](https://github.com/gravitee-io/issues/issues/10882) **Management API**

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* API traffic runtime logs incorrectly show endpoint response 200 [#10896](https://github.com/gravitee-io/issues/issues/10896)

**Console**

* Update Management API connection failure banner copy [#10945](https://github.com/gravitee-io/issues/issues/10945)

**Other**

* Enable configurable API Key header name in API Key plan [#10939](https://github.com/gravitee-io/issues/issues/10939)

</details>

## Gravitee API Management 4.9.2 - October 24, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* K8s Synchronizer revokes secrets on API update in v4.9.0 [#10908](https://github.com/gravitee-io/issues/issues/10908)

**Management API**

* Flow id missing in create api response of V4 APIs [#10888](https://github.com/gravitee-io/issues/issues/10888)
* Visibility flag is not getting updated as part of api creation using mAPI [#10895](https://github.com/gravitee-io/issues/issues/10895)
* API Filters do not recognize status changes [#10910](https://github.com/gravitee-io/issues/issues/10910)

**Console**

* Fetching groups for an application takes a really long time [#10709](https://github.com/gravitee-io/issues/issues/10709)
* Impossible to delete member group [#10836](https://github.com/gravitee-io/issues/issues/10836)

**Other**

* Webhook Entrypoint: Linear retry delay incorrectly interpreted as milliseconds instead of seconds [#10520](https://github.com/gravitee-io/issues/issues/10520)
* Ensure IPv4 backward compatibility in docker images [#10859](https://github.com/gravitee-io/issues/issues/10859)
* Requests blocked (403) when IP Filtering Policy contains both hostname and IP [#10866](https://github.com/gravitee-io/issues/issues/10866)
* Inconsistency in portal sub-path configuration between IPv4 and IPv6 NGINX files [#10904](https://github.com/gravitee-io/issues/issues/10904)
* Migration v2->v4 API is falling for some APIs [#10918](https://github.com/gravitee-io/issues/issues/10918)

</details>

## Gravitee API Management 4.9.1 - October 21, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* K8s Synchronizer revokes secrets on API update in v4.9.0 [#10908](https://github.com/gravitee-io/issues/issues/10908)

**Management API**

* ThreadBlocked can occurs when fetching token when Federation agent connects [#10913](https://github.com/gravitee-io/issues/issues/10913)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Getting 502 Bad Gateway error while invoking the request. [#10863](https://github.com/gravitee-io/issues/issues/10863)

**Console**

* Getting 502 Bad Gateway error while invoking the request. [#10863](https://github.com/gravitee-io/issues/issues/10863)

</details>
