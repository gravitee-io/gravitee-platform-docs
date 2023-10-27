---
description: >-
  This page contains the changelog entries for APIM 4.1.x and any future patch
  APIM 4.1.x releases
---

# APIM 4.1.x

## Gravitee API Management 4.1.2 - October 27, 2023

<details>

<summary>Bug fixes</summary>

**Management API**

* Can't create Backend-to-Backend applications [#9157](https://github.com/gravitee-io/issues/issues/9157)
* Can't assign a group to a Backend-to-Backend application [#9158](https://github.com/gravitee-io/issues/issues/9158)
* Invalid CORS Allow Origin Can Be Imported To Create New API [#9212](https://github.com/gravitee-io/issues/issues/9212)
* Unable to create custom email notification template [#9284](https://github.com/gravitee-io/issues/issues/9284)
* Attached Media is lost when the API Documentation is renamed [#9285](https://github.com/gravitee-io/issues/issues/9285)
* User email address policy treats valid email address as invalid [#9293](https://github.com/gravitee-io/issues/issues/9293)
* Endpoint Configuration Resets to Default after Redeployment [#9296](https://github.com/gravitee-io/issues/issues/9296)
* Alert template not automatically applied to new APIs [#9323](https://github.com/gravitee-io/issues/issues/9323)
* Unable to import OpenAPI spec with unused `variables` in `servers` definition [#9329](https://github.com/gravitee-io/issues/issues/9329)
* User with quotes in last name isn't properly sanitized [#9336](https://github.com/gravitee-io/issues/issues/9336)
* Listening Hosts are mandatory in Virtual Hosts mode [#9343](https://github.com/gravitee-io/issues/issues/9343)
* The OpenAPI schema to close a plan has incorrect response code [#9351](https://github.com/gravitee-io/issues/issues/9351)

**Console**

* Unable to Update API with Open API YAML File [#9202](https://github.com/gravitee-io/issues/issues/9202)
* Unable to edit flows once saved with an invalid configuration [#9274](https://github.com/gravitee-io/issues/issues/9274)
* No Backend-to-Backend application type available [#9334](https://github.com/gravitee-io/issues/issues/9334)

**Portal**

* Custom wide logo is too small in the Portal header [#9337](https://github.com/gravitee-io/issues/issues/9337)

**Other**

* IP Filtering policy blacklist does not work if there is a space in the IP address [#9083](https://github.com/gravitee-io/issues/issues/9083)
* Domain name (host) in whitelist does not work in IP Filtering policy [#9198](https://github.com/gravitee-io/issues/issues/9198)
* JWS policy doesn't work with Java 17 [#9211](https://github.com/gravitee-io/issues/issues/9211)
* Data Logging Masking policy [#9215](https://github.com/gravitee-io/issues/issues/9215)
* Jaeger not working with APIM 4+ [#9331](https://github.com/gravitee-io/issues/issues/9331)
* Quotify the namespace defined in ServiceAccount to avoid errors [#9345](https://github.com/gravitee-io/issues/issues/9345)

</details>

## Gravitee API Management 4.1.1 - October 13, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Health check doesn't support endpoint with EL [#8700](https://github.com/gravitee-io/issues/issues/8700)
* `resource-filtering` policy does not work with debug mode [#9267](https://github.com/gravitee-io/issues/issues/9267)
* Gateways take proxy configuration but should not [#9278](https://github.com/gravitee-io/issues/issues/9278)

**Management API**

* Emails related to closed, paused, and resumed subscription of PUSH plan are not sent [#9281](https://github.com/gravitee-io/issues/issues/9281)
* Unable to update health checks on endpoints with REST API v2 [#9283](https://github.com/gravitee-io/issues/issues/9283)

**Console**

* "Configure logging mode" link not working [#9213](https://github.com/gravitee-io/issues/issues/9213)
* "Add members" button does not work for group admin [#9241](https://github.com/gravitee-io/issues/issues/9241)
* Unable to remove expiration date of an API Key [#9248](https://github.com/gravitee-io/issues/issues/9248)
* Non-admin users can't see API Keys of APIs they created [#9268](https://github.com/gravitee-io/issues/issues/9268)
* Console: Add date time picker instead of only date for subscription date field [#9271](https://github.com/gravitee-io/issues/issues/9271)
* Log Content Not Visible in V2 API Logs [#9290](https://github.com/gravitee-io/issues/issues/9290)

**Other**

* User claim in OAuth2 resource is ignored [#9168](https://github.com/gravitee-io/issues/issues/9168)
* Typo in the documentation of `cache-policy` [#9262](https://github.com/gravitee-io/issues/issues/9262)

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
