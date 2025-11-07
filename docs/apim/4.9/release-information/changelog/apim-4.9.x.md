# APIM 4.9.x
 
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

* UI Text Overflow in "User Permissions" Tab [#10882](https://github.com/gravitee-io/issues/issues/10882)

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
