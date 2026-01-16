---
description: Documentation about apim 4.9.x in the context of APIs.
metaLinks:
  alternates:
    - /broken/spaces/bGmDEarvnV52XdcOiV8o/pages/0oVQWkw8tEgZsegmlu1I
---

# APIM 4.9.x
 
## Gravitee API Management 4.9.11 - January 16, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* Save changes button does not appear on policy studio when jwt policy is dropped [#11011](https://github.com/gravitee-io/issues/issues/11011)

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
