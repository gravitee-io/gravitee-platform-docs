---
description: >-
  This page contains the changelog entries for APIM 4.1.x and any future patch
  APIM 4.1.x releases
---

# APIM 4.1.x
 
## Gravitee API Management 4.1.1 - October 13, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Health Check doesn't support Endpoint with EL [#8700](https://github.com/gravitee-io/issues/issues/8700)
* resource-filtering policy does not work with debug mode [#9267](https://github.com/gravitee-io/issues/issues/9267)
* Gateways take proxy configuration while it mustn't  [#9278](https://github.com/gravitee-io/issues/issues/9278)

**Management API**

* Email related to closed, paused and resumed subscription of PUSH plan are not sent [#9281](https://github.com/gravitee-io/issues/issues/9281)
* unable to update health checks on endpoints with REST API v2 [#9283](https://github.com/gravitee-io/issues/issues/9283)

**Console**

* Configure logging mode link not working [#9213](https://github.com/gravitee-io/issues/issues/9213)
* Add members button does not work for group admin [#9241](https://github.com/gravitee-io/issues/issues/9241)
* Unable to remove expiration date of an API Key [#9248](https://github.com/gravitee-io/issues/issues/9248)
* Non admin users can't see api keys of APIs they created [#9268](https://github.com/gravitee-io/issues/issues/9268)
* Console - Add date time picker instead of only date for subscription date field [#9271](https://github.com/gravitee-io/issues/issues/9271)
* Log Content Not Visible in V2 API Logs [#9290](https://github.com/gravitee-io/issues/issues/9290)

**Other**

* User claim in OAuth2 resource seems ignored [#9168](https://github.com/gravitee-io/issues/issues/9168)
* Typo in the documentation of  "cache policy" [#9262](https://github.com/gravitee-io/issues/issues/9262)

</details>

## Gravitee API Management 4.1.0 - September 28, 2023

For more in-depth information on what's new, please refer to the [Gravitee APIM 4.1 release notes](../release-notes/apim-4.1.md).

<details>

<summary>What's new</summary>

**Installing APIM on Kubernetes**

* Helm Chart configuration now supports DB-less mode

**v4 API Configuration**

* Webhook entrypoint configuration supports Dead Letter Queue
* Enhanced single endpoint and endpoint group management
* Default single endpoint and endpoint group settings inheritance to streamline configuration
* Enhancements to user and group access, including transfer of ownership

**Creating v4 APIs**

* A v4 API can be created by importing an existing Gravitee v4 API definition in JSON format
* v4 API duplication is now supported

**Logging**

* Comprehensive connection logs to analyze the usage of v4 message APIs
* Customizable data capture and message content details

</details>

<details>

<summary>Breaking Changes</summary>

No breaking changes

</details>
