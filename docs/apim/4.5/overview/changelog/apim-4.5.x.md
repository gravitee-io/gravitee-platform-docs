---
description: >-
  This page contains the changelog entries for APIM 4.5.x and any future patch
  APIM 4.5.x releases
---

# APIM 4.5.x
 
## Gravitee API Management 4.5.20 - June 20, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Debug mode adding extra slash on endpoint [#10438](https://github.com/gravitee-io/issues/issues/10438)

**Management API**

* Error on Portal admin login when subscription has null API [#10618](https://github.com/gravitee-io/issues/issues/10618)

**Console**

* No error message raised while deleting folder [#10608](https://github.com/gravitee-io/issues/issues/10608)

**Helm Charts**

* Multi-Tenant dictionaries: align values.yml and gravitee.yml [#10627](https://github.com/gravitee-io/issues/issues/10627)

**Other**

* Problem IP Filtering / Host resolving [#10592](https://github.com/gravitee-io/issues/issues/10592)
* Solace webhook subscription 500 internal server error [#10622](https://github.com/gravitee-io/issues/issues/10622)

</details>


 
## Gravitee API Management 4.5.19 - June 13, 2025
<details>

<summary>Bug Fixes</summary>

**Management API**

* Updated name of shared policy group is not reflected in the API's in which its being used [#10553](https://github.com/gravitee-io/issues/issues/10553)
* Custom metrics with a value of 1 appear as a question mark in Analytics [#10564](https://github.com/gravitee-io/issues/issues/10564)
* Specific API logging configuration causes warning messages [#10577](https://github.com/gravitee-io/issues/issues/10577)
* On API groups update, if the groups field is null it should keep its current value [#10581](https://github.com/gravitee-io/issues/issues/10581)
* Extra / is added in Context path in V4 API [#10606](https://github.com/gravitee-io/issues/issues/10606)

**Console**

* Groups are removed from V4 APIs when no changes are saved [#10590](https://github.com/gravitee-io/issues/issues/10590)

**Helm Charts**

* \[Helm] Management API configuration has wrong default logs path [#10524](https://github.com/gravitee-io/issues/issues/10524)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Memory handling in gravitee entrypoint. [#10600](https://github.com/gravitee-io/issues/issues/10600)

**Management API**

* Memory handling in gravitee entrypoint. [#10600](https://github.com/gravitee-io/issues/issues/10600)

</details>


 
## Gravitee API Management 4.5.18 - May 28, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Dictionaries are unable to be created with the same name across environments or organizations. [#10537](https://github.com/gravitee-io/issues/issues/10537)
* Status code 0 in Analytics when V4 emulation engine is activated [#10579](https://github.com/gravitee-io/issues/issues/10579)

**Management API**

* Intermittent errors when using request content and fire & forget in HTTP callout policy [#10424](https://github.com/gravitee-io/issues/issues/10424)
* Http Callout policy does not work with V4 emulation and Fire and forget [#10494](https://github.com/gravitee-io/issues/issues/10494)
* Tenant name verification issue [#10517](https://github.com/gravitee-io/issues/issues/10517)
* Alert filter doesn't show list of APIs in selection box. [#10532](https://github.com/gravitee-io/issues/issues/10532)
* Improve error logs in upgrader [#10535](https://github.com/gravitee-io/issues/issues/10535)
* Dictionaries are unable to be created with the same name across environments or organizations. [#10537](https://github.com/gravitee-io/issues/issues/10537)
* Management transfer_ownership API is allowing multiple primary owners on applications  [#10572](https://github.com/gravitee-io/issues/issues/10572)
* Remove System.out.println statement [#10583](https://github.com/gravitee-io/issues/issues/10583)

**Console**

* Tenant name verification issue [#10517](https://github.com/gravitee-io/issues/issues/10517)
* Alert filter doesn't show list of APIs in selection box. [#10532](https://github.com/gravitee-io/issues/issues/10532)
* Groups page fails to load when too many groups exist because no pagination [#10538](https://github.com/gravitee-io/issues/issues/10538)
* Group management for APIs broken [#10542](https://github.com/gravitee-io/issues/issues/10542)
* Application filter 'not equals to' operator is unusable [#10546](https://github.com/gravitee-io/issues/issues/10546)

**Helm Charts**

* Fix Elasticsearch dependency configuration of replicas in APIM helm chart [#10541](https://github.com/gravitee-io/issues/issues/10541)

**Other**

* Unable to launch Lambda with lambda Policy [#10570](https://github.com/gravitee-io/issues/issues/10570)

</details>

<details>

<summary>Improvements</summary>

**Console**

* \[UI] Add text to indicate max image size allowed [#10561](https://github.com/gravitee-io/issues/issues/10561)

</details>


 
## Gravitee API Management 4.5.17 - May 9, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* CompositeByteBuf is creating a high volume of logs [#10539](https://github.com/gravitee-io/issues/issues/10539)

**Console**

* Local link to internal section dose not work in documentation [#10180](https://github.com/gravitee-io/issues/issues/10180)
* APIM API Throwing HTTP 500 On a Specific Returned Page [#10372](https://github.com/gravitee-io/issues/issues/10372)
* UX problem in condition alerting threshold [#10514](https://github.com/gravitee-io/issues/issues/10514)

**Other**

* Schema registry resource URL not fully taken into account [#10530](https://github.com/gravitee-io/issues/issues/10530)

</details>


 
## Gravitee API Management 4.5.16 - May 2, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Problems with HTTP code 502 because of keepalive

**Management API**

*  Rollback does not work for the v4 emulation button [#10190](https://github.com/gravitee-io/issues/issues/10190)
* Application search does not work if search term pattern matches _id pattern [#10487](https://github.com/gravitee-io/issues/issues/10487)

**Console**

* Settings-> Groups : 'Allows invitation via user search' is NOT working as expected [#10485](https://github.com/gravitee-io/issues/issues/10485)
* Application search does not work if search term pattern matches _id pattern [#10487](https://github.com/gravitee-io/issues/issues/10487)

**Other**

* Response time different between log file and UI [#10301](https://github.com/gravitee-io/issues/issues/10301)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Use Gravitee GPG Key to sign RPM package [#10450](https://github.com/gravitee-io/issues/issues/10450)

</details>


 
## Gravitee API Management 4.5.15 - April 25, 2025
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


 
## Gravitee API Management 4.5.14 - April 11, 2025
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

**Console**

* Only 200 HTTP Status calls rendered in API analytics in Console UI [#10098](https://github.com/gravitee-io/issues/issues/10098)
* Failed association of groups to APIs [#10211](https://github.com/gravitee-io/issues/issues/10211)
* V4 Flows cannot be duplicated or disabled [#10242](https://github.com/gravitee-io/issues/issues/10242)
* Unable to update Alert Rate Condition after clearing aggregation field [#10332](https://github.com/gravitee-io/issues/issues/10332)
* Newly created applications are not associated to groups that have "Associate automatically to every new application" enabled [#10457](https://github.com/gravitee-io/issues/issues/10457)

**Portal**

* Saved application alert in Dev Portal fails to display percentage value [#10446](https://github.com/gravitee-io/issues/issues/10446)
* Registration Confirmation URL incorrectly includes full path and query parameters [#10456](https://github.com/gravitee-io/issues/issues/10456)

</details>


 
## Gravitee API Management 4.5.13 - April 4, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway stops syncing apis after failing to connect to jdbc datasource [#10441](https://github.com/gravitee-io/issues/issues/10441)

**Management API**

* API key is not working for API subscriptions when we use Shared API key [#10122](https://github.com/gravitee-io/issues/issues/10122)
* Adding an unknown group id to excluded groups on a plan removes all excluded groups and prevents exports of the API [#10389](https://github.com/gravitee-io/issues/issues/10389)

**Console**

* API key is not working for API subscriptions when we use Shared API key [#10122](https://github.com/gravitee-io/issues/issues/10122)
* Account page is broken [#10451](https://github.com/gravitee-io/issues/issues/10451)

**Portal**

* NewDevPortal - Swagger expands outside of allowed frame [#10461](https://github.com/gravitee-io/issues/issues/10461)

**Other**

* Groups not automatically added to new applications when they should be [#10470](https://github.com/gravitee-io/issues/issues/10470)

</details>


 
## Gravitee API Management 4.5.12 - March 27, 2025
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


 
## Gravitee API Management 4.5.11 - March 14, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Memory leak with cached policy instances [#10370](https://github.com/gravitee-io/issues/issues/10370)

**Management API**

* User is not able to login using OIDC [#10262](https://github.com/gravitee-io/issues/issues/10262)
* Regex Threat Protection Policy Does Not Handle Multiline Payloads [#10260](https://github.com/gravitee-io/issues/issues/10260)
* Shared policy group edits cause audit errors [#10316](https://github.com/gravitee-io/issues/issues/10316)
* Error for V4 API logs when analytics is disabled [#10347](https://github.com/gravitee-io/issues/issues/10347)

**Console**

* User is not able to login using OIDC [#10262](https://github.com/gravitee-io/issues/issues/10262)
* Text in API documentation does not breakline vertically within container [#10198](https://github.com/gravitee-io/issues/issues/10198)
* Documentation Read permission does not allow users to view document content [#10217](https://github.com/gravitee-io/issues/issues/10217)
* Shared policy group edits cause audit errors [#10316](https://github.com/gravitee-io/issues/issues/10316)
* Error for V4 API logs when analytics is disabled [#10347](https://github.com/gravitee-io/issues/issues/10347)
* Absolute links in gravitee-apim-console-webui (ignoring <base href...>) [#10394](https://github.com/gravitee-io/issues/issues/10394)

**Portal**

* Text in API documentation does not breakline vertically within container [#10198](https://github.com/gravitee-io/issues/issues/10198)
* Table of content on right side should be wrapped. [#10290](https://github.com/gravitee-io/issues/issues/10290)
* New Developer Portal - Changes to Header and Footer Not being applied [#10319](https://github.com/gravitee-io/issues/issues/10319)

**Other**

* Impossible to edit / save a V4 Kafka Gateway API using Postgres as the Management DB [#10393](https://github.com/gravitee-io/issues/issues/10393)
* 500 error on jwt plan when using  "Emulate v4 engine" and gateway keys configuration [#10420](https://github.com/gravitee-io/issues/issues/10420)

</details>

<details>

<summary>Improvements</summary>

**Console**

* Remove Associations from Groups maintenance if not authorized [#9832](https://github.com/gravitee-io/issues/issues/9832)

</details>


 
## Gravitee API Management 4.5.10 - February 28, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* APIM gateway - webhook subscription failure due to invalid characters in header [#10253](https://github.com/gravitee-io/issues/issues/10253)

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


 
## Gravitee API Management 4.5.9 - February 14, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Webhook subscription failing to get messages from a Kafka topic [#10320](https://github.com/gravitee-io/issues/issues/10320)
* Thread block while deploying APIs with very long read timeouts set in the Endpoints configuration [#10340](https://github.com/gravitee-io/issues/issues/10340)

**Portal**

* Public APIs not accessible to anonymous users through categories in the portal [#10274](https://github.com/gravitee-io/issues/issues/10274)

**Helm Charts**

* Typo in values.yaml and missing Helm chart mapping for gravitee.yml [#10343](https://github.com/gravitee-io/issues/issues/10343)

**Other**

* Can't see Logs for JWT enabled API's in API Management portal (401 response only) [#10076](https://github.com/gravitee-io/issues/issues/10076)

</details>

{% hint style="warning" %}
**Using Service Discovery?**

When using Service Discovery the Gateway may not wait for pending connections to finish on API redeploy or API stop **if using Service Discovery.**
{% endhint %}
 
## Gravitee API Management 4.5.8 - January 31, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Repeating Error Eventually Causing Restarts [#10225](https://github.com/gravitee-io/issues/issues/10225)

**Console**

* Missing "Add Member" Button in group settings [#10050](https://github.com/gravitee-io/issues/issues/10050)
* Application updates remove the picture  [#10302](https://github.com/gravitee-io/issues/issues/10302)

**Portal**

* Subscribing to an API with general condition page when creating an application returns a 404 [#10103](https://github.com/gravitee-io/issues/issues/10103)

**Helm Charts**

* Repeating Error Eventually Causing Restarts [#10225](https://github.com/gravitee-io/issues/issues/10225)

**Other**

* Reporter file in CSV format doesn't work [#10181](https://github.com/gravitee-io/issues/issues/10181)

</details>


 
## Gravitee API Management 4.5.7 - January 24, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Problem with request body size above 2MB when using V4 Engine [#10291](https://github.com/gravitee-io/issues/issues/10291)

**Console**

* Path mapping does not work with hyphen [#10289](https://github.com/gravitee-io/issues/issues/10289)

**Portal**

* Developer Portal Preview not working in Multi-tenant mode [#10204](https://github.com/gravitee-io/issues/issues/10204)

</details>


 
## Gravitee API Management 4.5.6 - January 16, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* API Gateway - memory leak [#10220](https://github.com/gravitee-io/issues/issues/10220)
* 400 error "The plain HTTP request was sent to HTTPS port" when redirecting to HTTPS endpoint. [#10265](https://github.com/gravitee-io/issues/issues/10265)

**Management API**

* It is possible to create objects in APIM with ID value ""  [#10213](https://github.com/gravitee-io/issues/issues/10213)
* API closed subscription details not working [#10164](https://github.com/gravitee-io/issues/issues/10164)

**Console**

* Resource access is not allowed for a user with Publisher api role [#10032](https://github.com/gravitee-io/issues/issues/10032)
* Sharding tags removed when API configuration updated [#10191](https://github.com/gravitee-io/issues/issues/10191)
* API's member list cannot display more than 10 members  [#10212](https://github.com/gravitee-io/issues/issues/10212)
* Changing flow selection (DEFAULT/Best Match) does not show deploy banner [#10235](https://github.com/gravitee-io/issues/issues/10235)
* Analytics filters are not applied when the dashboard is changed [#10238](https://github.com/gravitee-io/issues/issues/10238)

**Portal**

* Title of developer portal browser tab is not translated [#10263](https://github.com/gravitee-io/issues/issues/10263)

</details>

<details>

<summary>Improvements</summary>

**Helm Charts**

* Helm chart - improve support of scale up/down policies [#10255](https://github.com/gravitee-io/issues/issues/10255)

</details>


 
## Gravitee API Management 4.5.5 - December 20, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* A WEIGHTED_ROUND_ROBIN on a unique endpoint with weight set to 0 leads to gateway thread blocked [#10241](https://github.com/gravitee-io/issues/issues/10241)

**Console**

* Empty endpoint group prevents the update of the Global Healthcheck without clear error message [#10216](https://github.com/gravitee-io/issues/issues/10216)

**Other**

* Warnings about Groovy classes  [#10219](https://github.com/gravitee-io/issues/issues/10219)
* API not deployed if OAuth 2.0 resource (Generic and AM) set with system proxy enabled [#10223](https://github.com/gravitee-io/issues/issues/10223)

</details>


 
## Gravitee API Management 4.5.4 - December 5, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Websocket subprotocol doesn't work in API GW [#10023](https://github.com/gravitee-io/issues/issues/10023)
* Opensearch configuration and ism policy [#10100](https://github.com/gravitee-io/issues/issues/10100)
* Creating a Cache Policy with 4.5.3 or newer is not activating the trigger condition in the debug mode  [#10209](https://github.com/gravitee-io/issues/issues/10209)

**Management API**

* Custom Api key is not reusable between multiple environments [#10131](https://github.com/gravitee-io/issues/issues/10131)
* Page Size Drop Down cannot exceed 100 [#10145](https://github.com/gravitee-io/issues/issues/10145)
* \[APIM]\[Portal] Static data access  [#10162](https://github.com/gravitee-io/issues/issues/10162)
* Unable to find users with emails containing uppercase letters in Gravitee APIM Console and API requests [#10167](https://github.com/gravitee-io/issues/issues/10167)
* Webhook notification for Subscription_Accepted event is missing "owner" details [#10187](https://github.com/gravitee-io/issues/issues/10187)
* OpenAPI documentation "Show the URL to download the content" doesn't work [#9891](https://github.com/gravitee-io/issues/issues/9891)

**Other**

* \[gravitee-policy-cache] Timeouts occur when trying to cache a large payload [#10208](https://github.com/gravitee-io/issues/issues/10208)


</details>

<details>

<summary>Improvements</summary>

**Management API**

* Improve `/apis/{apiId}/import/swagger?definitionVersion=2.0.0` endpoint performances [#10117](https://github.com/gravitee-io/issues/issues/10117)

  Note: Two new environment variables have been introduced to enhance the configuration. The first, `documentation.audit.max-content-size`, is designed to limit the size of the content saved in audits when a Page is created during an import. The second variable, `documentation.swagger.validate-safe-content`, determines whether the content of an imported OAS is validated for safety during the import process.

</details>


 
## Gravitee API Management 4.5.3 - November 21, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* SSE connections receives messages to the wrong API when connected to rabbitmq  [#10020](https://github.com/gravitee-io/issues/issues/10020)

**Management API**

* API webhook notifier is not working for subscriptions [#10056](https://github.com/gravitee-io/issues/issues/10056)
* MAPI v2 : analytics : /respoinse-statuses : error 404 [#10175](https://github.com/gravitee-io/issues/issues/10175)

**Console**

* When creating an endpoint group, the page is not properly refreshed [#10129](https://github.com/gravitee-io/issues/issues/10129)
* Malformed EL and grammar issues [#10149](https://github.com/gravitee-io/issues/issues/10149)

**Other**

* DataDog issues with plugin v2.4.5 [#10157](https://github.com/gravitee-io/issues/issues/10157)
* API CRD export mismatch on plan when using selection rules [#10179](https://github.com/gravitee-io/issues/issues/10179)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Support expression language in ip filtering policy [#10142](https://github.com/gravitee-io/issues/issues/10142)

</details>



## Gravitee API Management 4.5.2 - November 5, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Inconsistent application of validateSubscription flag [#10120](https://github.com/gravitee-io/issues/issues/10120)
* Sync process failed if subscription exists without the linked API [#10140](https://github.com/gravitee-io/issues/issues/10140)

**Management API**

* Page revisions are still present when the associated API is deleted [#10039](https://github.com/gravitee-io/issues/issues/10039)
* API webhook notifier is not working for subscriptions [#10056](https://github.com/gravitee-io/issues/issues/10056)
* Alert Templates are always created in default environment [#10126](https://github.com/gravitee-io/issues/issues/10126)
* Updating the application generates an exception. [#10130](https://github.com/gravitee-io/issues/issues/10130)

**Console**

* Code blocks and long strings of text cause overflow of documentation text in the new dev portal [#10048](https://github.com/gravitee-io/issues/issues/10048)

**Other**

* Gateways can not reconnect to the bridge mapi [#10101](https://github.com/gravitee-io/issues/issues/10101)
* \[gravitee-policy-jwt] Complete gateway disruption occurred in retrieving JWT public keys after startup under a heavy load of API calls [#10119](https://github.com/gravitee-io/issues/issues/10119)

</details>

## Gravitee API Management 4.5.1 - October 24, 2024

<details>

<summary>Bug Fixes</summary>

**Management API**

* Dictionaries not deployed after migration from 3.20.x to 4.x [#10026](https://github.com/gravitee-io/issues/issues/10026)
* User with environment role is not able to create notifications [#10068](https://github.com/gravitee-io/issues/issues/10068)

**Console**

* Unable to delete Cors Allow-Origin URL [#9765](https://github.com/gravitee-io/issues/issues/9765)
* Error on sharding tags page refresh [#10067](https://github.com/gravitee-io/issues/issues/10067)
* Rollback from history removes groups of users from API [#10074](https://github.com/gravitee-io/issues/issues/10074)
* Upgrade nginx image to 1.27.2 [#10116](https://github.com/gravitee-io/issues/issues/10116)

**Portal**

* Swagger Documentation not showing in portal [#9946](https://github.com/gravitee-io/issues/issues/9946)
* Upgrade nginx image to 1.27.2 [#10116](https://github.com/gravitee-io/issues/issues/10116)

**Helm Charts**

* Set the HaProxy.ProxyProtocol with the Helm chart [#10027](https://github.com/gravitee-io/issues/issues/10027)

**Other**

* \[JDBC] Unable to create federation [#10107](https://github.com/gravitee-io/issues/issues/10107)

</details>

## Gravitee API Management 4.5.0 - October 10, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Transfer subscription does not use new plan when V4 emulation is disabled [#10047](https://github.com/gravitee-io/issues/issues/10047)
* \[3.20.X and 4.4.X] DNS Resolution fails for hosts having more than 30 A records [#10051](https://github.com/gravitee-io/issues/issues/10051)
* \[Gateway Distributed Sync] Properly differentiate v2 from v4 API events [#10055](https://github.com/gravitee-io/issues/issues/10055)
* \[gravitee-node] Gravitee metrics return NaN [#10070](https://github.com/gravitee-io/issues/issues/10070)

**Management API**

* Issue on permissions of the ORGANIZATION_USER role [#10040](https://github.com/gravitee-io/issues/issues/10040)

**Console**

* Not able to see API events in Dashboard [#10018](https://github.com/gravitee-io/issues/issues/10018)
* Analytics dashboard filtered become empty when a tenant is selected [#10019](https://github.com/gravitee-io/issues/issues/10019)
* Redirect user to login screen when JWT token has expired [#10029](https://github.com/gravitee-io/issues/issues/10029)
* Button color UI bug [#10035](https://github.com/gravitee-io/issues/issues/10035)

**Portal**

* Users without admin or API access cannot view application API keys in the new dev portal [#10014](https://github.com/gravitee-io/issues/issues/10014)
* Search bar not sorting results properly on portal for API [#10075](https://github.com/gravitee-io/issues/issues/10075)

**Helm Charts**

* Add serviceAccount in helm chart  [#10057](https://github.com/gravitee-io/issues/issues/10057)
* Update values.yml to Values.gateway.ratelimit.management.http.url  [#10091](https://github.com/gravitee-io/issues/issues/10091)

**Other**

* \[gravitee-policy-data-logging-masking] DLM policies will not allow the DataDog Reporter to forward logs to DataDog if a property is not found [#10044](https://github.com/gravitee-io/issues/issues/10044)

</details>
