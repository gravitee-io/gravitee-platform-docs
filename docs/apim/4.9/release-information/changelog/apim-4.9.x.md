# APIM 4.9.x
 
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
