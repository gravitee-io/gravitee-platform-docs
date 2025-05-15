---
description: >-
  This page contains the changelog entries for APIM 4.6.x and any future patch
  APIM 4.6.x releases
---

# APIM 4.6.x
 
## Gravitee API Management 4.6.11 - May 9, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* CompositeByteBuf is creating a high volume of logs [#10539](https://github.com/gravitee-io/issues/issues/10539)
* Problems with HTTP code 502 because of keepalive

**Management API**

*  Rollback does not work for the v4 emulation button [#10190](https://github.com/gravitee-io/issues/issues/10190)
* Application search does not work if search term pattern matches _id pattern [#10487](https://github.com/gravitee-io/issues/issues/10487)

**Console**

* Local link to internal section dose not work in documentation [#10180](https://github.com/gravitee-io/issues/issues/10180)
* APIM API Throwing HTTP 500 On a Specific Returned Page [#10372](https://github.com/gravitee-io/issues/issues/10372)
* Settings-> Groups : 'Allows invitation via user search' is NOT working as expected [#10485](https://github.com/gravitee-io/issues/issues/10485)
* Application search does not work if search term pattern matches _id pattern [#10487](https://github.com/gravitee-io/issues/issues/10487)
* UX problem in condition alerting threshold [#10514](https://github.com/gravitee-io/issues/issues/10514)

**Other**

* Response time different between log file and UI [#10301](https://github.com/gravitee-io/issues/issues/10301)
* Schema registry resource URL not fully taken into account [#10530](https://github.com/gravitee-io/issues/issues/10530)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Use Gravitee GPG Key to sign RPM package [#10450](https://github.com/gravitee-io/issues/issues/10450)

</details>


 
## Gravitee API Management 4.6.10 - April 25, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Bug in io.gravitee.connector.http.HttpConnection.java exceptionHandler [#10439](https://github.com/gravitee-io/issues/issues/10439)

**Management API**

* Global Alert configuration page does not refresh properly after change [#10436](https://github.com/gravitee-io/issues/issues/10436)
* Issue with Policy Execution Order [#10486](https://github.com/gravitee-io/issues/issues/10486)

**Console**

* API Traffic Settings page is not visible for V4 Message APIs due to permission issue for default roles [#10386](https://github.com/gravitee-io/issues/issues/10386)
* Logs filter display Unpublished plan [#10480](https://github.com/gravitee-io/issues/issues/10480)

**Portal**

* Portal-Next shows all Unpublished apis  [#10505](https://github.com/gravitee-io/issues/issues/10505)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Type of application is removed after update\[ApplicationType \[null] cannot be found]. [#10359](https://github.com/gravitee-io/issues/issues/10359)

</details>


 
## Gravitee API Management 4.6.9 - April 11, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* XSLT Transformation not applied when in response phase of v4 APIs [#10354](https://github.com/gravitee-io/issues/issues/10354)
* IP filtering policy does not check all the IPs for a host in white/blacklist [#10373](https://github.com/gravitee-io/issues/issues/10373)
* Unbounded Gateway memory growth in Openshift Kubernetes cluster [#10483](https://github.com/gravitee-io/issues/issues/10483)

**Management API**

* Failed association of groups to APIs [#10211](https://github.com/gravitee-io/issues/issues/10211)
* Custom API Key not taken into account when created through API Plan [#10324](https://github.com/gravitee-io/issues/issues/10324)
* Prevent Primary Owner removal when updating application's membership via cURL [#10382](https://github.com/gravitee-io/issues/issues/10382)
* v4 api : Unable to manage groups for all api types  [#10471](https://github.com/gravitee-io/issues/issues/10471)
* Adding an unknown group id to excluded groups on a plan in v4 apis removes all excluded groups and prevents exports of the API [#10473](https://github.com/gravitee-io/issues/issues/10473)

**Console**

* Only 200 HTTP Status calls rendered in API analytics in Console UI [#10098](https://github.com/gravitee-io/issues/issues/10098)
* Failed association of groups to APIs [#10211](https://github.com/gravitee-io/issues/issues/10211)
* V4 Flows cannot be duplicated or disabled [#10242](https://github.com/gravitee-io/issues/issues/10242)
* Unable to update Alert Rate Condition after clearing aggregation field [#10332](https://github.com/gravitee-io/issues/issues/10332)
* Newly created applications are not associated to groups that have "Associate automatically to every new application" enabled [#10457](https://github.com/gravitee-io/issues/issues/10457)
* Resolver parameter for JWT plan none accessible [#10476](https://github.com/gravitee-io/issues/issues/10476)

**Portal**

* Saved application alert in Dev Portal fails to display percentage value [#10446](https://github.com/gravitee-io/issues/issues/10446)
* Registration Confirmation URL incorrectly includes full path and query parameters [#10456](https://github.com/gravitee-io/issues/issues/10456)

</details>


 
## Gravitee API Management 4.6.8 - April 4, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway stops syncing apis after failing to connect to jdbc datasource [#10441](https://github.com/gravitee-io/issues/issues/10441)

**Management API**

* API key is not working for API subscriptions when we use Shared API key [#10122](https://github.com/gravitee-io/issues/issues/10122)
* Adding an unknown group id to excluded groups on a plan removes all excluded groups and prevents exports of the API [#10389](https://github.com/gravitee-io/issues/issues/10389)

**Console**

* API key is not working for API subscriptions when we use Shared API key [#10122](https://github.com/gravitee-io/issues/issues/10122)
* Account page broken in multi-environment installation [#10451](https://github.com/gravitee-io/issues/issues/10451)
* Display only http methods in debug mode tool [#10467](https://github.com/gravitee-io/issues/issues/10467)

**Portal**

* NewDevPortal - Swagger expands outside of allowed frame [#10461](https://github.com/gravitee-io/issues/issues/10461)
* Unable to show Swagger docs for Native api on Portal-Next [#10462](https://github.com/gravitee-io/issues/issues/10462)

**Other**

* Groups not automatically added to new applications when they should be [#10470](https://github.com/gravitee-io/issues/issues/10470)

</details>


 
## Gravitee API Management 4.6.7 - March 27, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Attributes referencing properties and request headers are not populated after large call volumes when v4 emulation is enabled [#10368](https://github.com/gravitee-io/issues/issues/10368)
* Kafka connector showing messages flowing but not appearing on client side [#10433](https://github.com/gravitee-io/issues/issues/10433)

**Management API**

* Shared API key doesn't always bind to subscriptions when concurrent requests are made [#10146](https://github.com/gravitee-io/issues/issues/10146)
* Attribute not allowed: \[a]\[download] in API Documentation main page [#10338](https://github.com/gravitee-io/issues/issues/10338)
* Renewed api key is "available" on closed subscription  [#10396](https://github.com/gravitee-io/issues/issues/10396)
* API flows are duplicated when called multiple times in row with the management API  [#10408](https://github.com/gravitee-io/issues/issues/10408)
* Import of an API does not ignore unknown access control groups that are present in another environment [#10414](https://github.com/gravitee-io/issues/issues/10414)
* Cannot list applications on Portal UI when group is removed from console [#10419](https://github.com/gravitee-io/issues/issues/10419)

**Console**

* Shared API key doesn't always bind to subscriptions when concurrent requests are made [#10146](https://github.com/gravitee-io/issues/issues/10146)
* In logs, the "users" column is no more available  [#10311](https://github.com/gravitee-io/issues/issues/10311)
* When restoring an archived application, the page is neither refreshed nor redirected [#10397](https://github.com/gravitee-io/issues/issues/10397)

**Portal**

* Cannot list applications on Portal UI when group is removed from console [#10419](https://github.com/gravitee-io/issues/issues/10419)

</details>


 
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



