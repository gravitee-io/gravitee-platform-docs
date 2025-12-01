---
description: Documentation about apim 4.9.x in the context of APIs.
---

# APIM 4.9.x
 
## Gravitee API Management 4.9.7 - November 27, 2025
<details>

<summary>Bug Fixes</summary>

**Management API**

* After deleting a federated, API count is not updating [#10980](https://github.com/gravitee-io/issues/issues/10980)

**Other**

* Intermittent 503s on OAuth2 Introspection due to Stale Connection Reuse [#10984](https://github.com/gravitee-io/issues/issues/10984)

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
