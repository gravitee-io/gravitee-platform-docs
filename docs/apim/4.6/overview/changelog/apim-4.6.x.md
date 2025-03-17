---
description: >-
  This page contains the changelog entries for APIM 4.6.x and any future patch
  APIM 4.6.x releases
---

# APIM 4.6.x
 
## Gravitee API Management 4.6.6 - March 14, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Memory leak with cached policy instances [#10370](https://github.com/gravitee-io/issues/issues/10370)
* Missing SNI causes kafka gateway crash [#10422](https://github.com/gravitee-io/issues/issues/10422)

**Management API**

* User is not able to login using OIDC [#10262](https://github.com/gravitee-io/issues/issues/10262)
* Regex Threat Protection Policy Does Not Handle Multiline Payloads [#10260](https://github.com/gravitee-io/issues/issues/10260)
* Shared policy group edits cause audit errors [#10316](https://github.com/gravitee-io/issues/issues/10316)
* Error for V4 API logs when analytics is disabled [#10347](https://github.com/gravitee-io/issues/issues/10347)
* "Name is Null" Error on Subscription Details for Pre-Existing Subscriptions [#10384](https://github.com/gravitee-io/issues/issues/10384)

**Console**

* User is not able to login using OIDC [#10262](https://github.com/gravitee-io/issues/issues/10262)
* Text in API documentation does not breakline vertically within container [#10198](https://github.com/gravitee-io/issues/issues/10198)
* Documentation Read permission does not allow users to view document content [#10217](https://github.com/gravitee-io/issues/issues/10217)
* Shared policy group edits cause audit errors [#10316](https://github.com/gravitee-io/issues/issues/10316)
* Error for V4 API logs when analytics is disabled [#10347](https://github.com/gravitee-io/issues/issues/10347)
* IPv6 crashes UI container if IPv6 is not enabled in environment [#10392](https://github.com/gravitee-io/issues/issues/10392)
* Absolute links in gravitee-apim-console-webui (ignoring <base href...>) [#10394](https://github.com/gravitee-io/issues/issues/10394)

**Portal**

* Text in API documentation does not breakline vertically within container [#10198](https://github.com/gravitee-io/issues/issues/10198)
* Table of content on right side should be wrapped. [#10290](https://github.com/gravitee-io/issues/issues/10290)
* New Developer Portal - Changes to Header and Footer Not being applied [#10319](https://github.com/gravitee-io/issues/issues/10319)
* IPv6 crashes UI container if IPv6 is not enabled in environment [#10392](https://github.com/gravitee-io/issues/issues/10392)

**Other**

* JSON validation policy causes the message not to be published [#10323](https://github.com/gravitee-io/issues/issues/10323)
* Impossible to edit / save a V4 Kafka Gateway API using Postgres as the Management DB [#10393](https://github.com/gravitee-io/issues/issues/10393)
* 500 error on jwt plan when using  "Emulate v4 engine" and gateway keys configuration [#10420](https://github.com/gravitee-io/issues/issues/10420)

</details>

<details>

<summary>Improvements</summary>

**Console**

* Remove Associations from Groups maintenance if not authorized [#9832](https://github.com/gravitee-io/issues/issues/9832)

</details>


 
## Gravitee API Management 4.6.5 - February 28, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* APIM gateway - webhook subscription failure due to invalid characters in header [#10253](https://github.com/gravitee-io/issues/issues/10253)
* Some OpenTelemetry settings do not work and README is misleading [#10253](https://github.com/gravitee-io/issues/issues/10356)

**Management API**

* Application can not be updated when using JDBC DB [#10171](https://github.com/gravitee-io/issues/issues/10171)
* Unnecessary Unicode characters in default data for new Shared Policy Groups [#10183](https://github.com/gravitee-io/issues/issues/10183)
* UUID of groups associated to application does not show in paginated view [#10270](https://github.com/gravitee-io/issues/issues/10270)
* Issue with Webhook notifications [#10293](https://github.com/gravitee-io/issues/issues/10293)
* API Docs: 204 Status Code Missing for /memberships Endpoint [#10336](https://github.com/gravitee-io/issues/issues/10336)
* API flows are duplicated when saved multiple times in the row  [#10355](https://github.com/gravitee-io/issues/issues/10355)

**Console**

* Enhance Rights Message in Management Portal [#10138](https://github.com/gravitee-io/issues/issues/10138)
* Platform analytics shows incorrect result in status pie-chart [#10267](https://github.com/gravitee-io/issues/issues/10267)
* Analytics logs exported as CSV are entirely on one line [#10350](https://github.com/gravitee-io/issues/issues/10350)
* API flows are duplicated when saved multiple times in the row  [#10355](https://github.com/gravitee-io/issues/issues/10355)

**Portal**

* Application logs in portal - http status criteria not persisted after search validation [#10308](https://github.com/gravitee-io/issues/issues/10308)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Adapt service discovery to properly handle HTTP graceful shutdown after changes in AbstractHttpConnector [#10345](https://github.com/gravitee-io/issues/issues/10345)

</details>


 
## Gravitee API Management 4.6.4 - February 14, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* \[Kafka Gateway] Make the ACL policy can be used before a TopicMapping Policy [#10280](https://github.com/gravitee-io/issues/issues/10280)
* \[Kafka Gateway] ACL policy fix various bugs like topic list visibility [#10335](https://github.com/gravitee-io/issues/issues/10335)
* Thread block while deploying APIs with very long read timeouts set in the Endpoints configuration [#10340](https://github.com/gravitee-io/issues/issues/10340)

**Management API**

* 4.6:Webhook policy flow cannot be saved [#10342](https://github.com/gravitee-io/issues/issues/10342)

**Portal**

* Public APIs not accessible to anonymous users through categories in the portal [#10274](https://github.com/gravitee-io/issues/issues/10274)

**Helm Charts**

* \[Helm charts] kafka configuration is missing some fields [#10330](https://github.com/gravitee-io/issues/issues/10330)
* Typo in values.yaml and missing Helm chart mapping for gravitee.yml [#10343](https://github.com/gravitee-io/issues/issues/10343)

**Other**

* Can't see Logs for JWT enabled API's in API Management portal (401 response only) [#10076](https://github.com/gravitee-io/issues/issues/10076)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* \[Kafka Gateway] Allow to customize the rewritten broker domain [#10337](https://github.com/gravitee-io/issues/issues/10337)

</details>

{% hint style="warning" %}
**Using Service Discovery?**

When using Service Discovery the Gateway may not wait for pending connections to finish on API redeploy or API stop **if using Service Discovery.**
{% endhint %}

## Gravitee API Management 4.6.3 - February 7, 2025

**Technical release**

No fixes or features have been added.
 
## Gravitee API Management 4.6.2 - January 31, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Repeating Error Eventually Causing Restarts [#10225](https://github.com/gravitee-io/issues/issues/10225)
* Kafka Gateway issue with confluent [#10321](https://github.com/gravitee-io/issues/issues/10321)

**Console**

* Missing "Add Member" Button in group settings [#10050](https://github.com/gravitee-io/issues/issues/10050)
* Application updates remove the picture  [#10302](https://github.com/gravitee-io/issues/issues/10302)

**Portal**

* Subscribing to an API with general condition page when creating an application returns a 404 [#10103](https://github.com/gravitee-io/issues/issues/10103)

**Helm Charts**

* Repeating Error Eventually Causing Restarts [#10225](https://github.com/gravitee-io/issues/issues/10225)

**Other**

* Changes needed to rpm packages [#9728](https://github.com/gravitee-io/issues/issues/9728)
* Reporter file in CSV format doesn't work [#10181](https://github.com/gravitee-io/issues/issues/10181)
* \[RPM upgrade] Lucene issue on upgrading from 4.4.9 to 4.5.0 [#10192](https://github.com/gravitee-io/issues/issues/10192)

</details>


 
## Gravitee API Management 4.6.1 - January 24, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Dictionaries stop working [#10286](https://github.com/gravitee-io/issues/issues/10286)
* Problem with request body size above 2MB when using V4 Engine [#10291](https://github.com/gravitee-io/issues/issues/10291)
* Fix issue with a iokafka python client [#10303](https://github.com/gravitee-io/issues/issues/10303)

**Console**

* Path mapping does not work with hyphen [#10289](https://github.com/gravitee-io/issues/issues/10289)

</details>



