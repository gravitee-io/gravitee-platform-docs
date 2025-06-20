---
description: >-
  This page contains the changelog entries for APIM 4.4.x and any future patch
  APIM 4.4.x releases
---

# APIM 4.4.x
 
## Gravitee API Management 4.4.31 - June 20, 2025
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


 
## Gravitee API Management 4.4.30 - June 13, 2025
<details>

<summary>Bug Fixes</summary>

**Management API**

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


 
## Gravitee API Management 4.4.29 - May 28, 2025
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


 
## Gravitee API Management 4.4.28 - May 9, 2025
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


 
## Gravitee API Management 4.4.27 - May 2, 2025
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


 
## Gravitee API Management 4.4.26 - April 25, 2025
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


 
## Gravitee API Management 4.4.25 - April 11, 2025
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

**Portal**

* Saved application alert in Dev Portal fails to display percentage value [#10446](https://github.com/gravitee-io/issues/issues/10446)
* Registration Confirmation URL incorrectly includes full path and query parameters [#10456](https://github.com/gravitee-io/issues/issues/10456)

</details>


 
## Gravitee API Management 4.4.24 - April 4, 2025
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

</details>


 
## Gravitee API Management 4.4.23 - March 27, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway fails to initialize API endpoints using dictionary values after restart [#10348](https://github.com/gravitee-io/issues/issues/10348)
* Attributes referencing properties and request headers are not populated after large call volumes when v4 emulation is enabled [#10368](https://github.com/gravitee-io/issues/issues/10368)
* Kafka connector showing messages flowing but not appearing on client side [#10433](https://github.com/gravitee-io/issues/issues/10433)

**Management API**

* Shared API key doesn't always bind to subscriptions when concurrent requests are made [#10146](https://github.com/gravitee-io/issues/issues/10146)
* Attribute not allowed: \[a]\[download] in API Documentation main page [#10338](https://github.com/gravitee-io/issues/issues/10338)
* Gateway fails to initialize API endpoints using dictionary values after restart [#10348](https://github.com/gravitee-io/issues/issues/10348)
* Renewed api key is "available" on closed subscription  [#10396](https://github.com/gravitee-io/issues/issues/10396)
* API flows are duplicated when called multiple times in row with the management API  [#10408](https://github.com/gravitee-io/issues/issues/10408)
* Import of an API does not ignore unknown access control groups that are present in another environment [#10414](https://github.com/gravitee-io/issues/issues/10414)

**Console**

* Shared API key doesn't always bind to subscriptions when concurrent requests are made [#10146](https://github.com/gravitee-io/issues/issues/10146)
* In logs, the "users" column is no more available  [#10311](https://github.com/gravitee-io/issues/issues/10311)
* When restoring an archived application, the page is neither refreshed nor redirected [#10397](https://github.com/gravitee-io/issues/issues/10397)

</details>


 
## Gravitee API Management 4.4.22 - March 14, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Memory leak with cached policy instances [#10370](https://github.com/gravitee-io/issues/issues/10370)

**Management API**

* User is not able to login using OIDC [#10262](https://github.com/gravitee-io/issues/issues/10262)
* Regex Threat Protection Policy Does Not Handle Multiline Payloads [#10260](https://github.com/gravitee-io/issues/issues/10260)
* Error for V4 API logs when analytics is disabled [#10347](https://github.com/gravitee-io/issues/issues/10347)

**Console**

* User is not able to login using OIDC [#10262](https://github.com/gravitee-io/issues/issues/10262)
* Text in API documentation does not breakline vertically within container [#10198](https://github.com/gravitee-io/issues/issues/10198)
* Documentation Read permission does not allow users to view document content [#10217](https://github.com/gravitee-io/issues/issues/10217)
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


 
## Gravitee API Management 4.4.21 - February 28, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* APIM gateway - webhook subscription failure due to invalid characters in header [#10253](https://github.com/gravitee-io/issues/issues/10253)

**Management API**

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


 
## Gravitee API Management 4.4.20 - February 14, 2025
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


## Gravitee API Management 4.4.19 - January 31, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Repeating Error Eventually Causing Restarts [#10225](https://github.com/gravitee-io/issues/issues/10225)

**Console**

* Missing "Add Member" Button in group settings [#10050](https://github.com/gravitee-io/issues/issues/10050)
* Application updates remove the picture [#10302](https://github.com/gravitee-io/issues/issues/10302)

**Portal**

* Subscribing to an API with general condition page when creating an application returns a 404 [#10103](https://github.com/gravitee-io/issues/issues/10103)

**Helm Charts**

* Repeating Error Eventually Causing Restarts [#10225](https://github.com/gravitee-io/issues/issues/10225)

</details>

## Gravitee API Management 4.4.18 - January 24, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Problem with request body size above 2MB on v2 APIs [#10291](https://github.com/gravitee-io/issues/issues/10291)

**Console**

* Path mapping does not work with hyphen [#10289](https://github.com/gravitee-io/issues/issues/10289)

**Portal**

* Developer Portal Preview not working in Multi-tenant mode [#10204](https://github.com/gravitee-io/issues/issues/10204)

</details>

## Gravitee API Management 4.4.17 - January 16, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* API Gateway - memory leak [#10220](https://github.com/gravitee-io/issues/issues/10220)
* 400 error "The plain HTTP request was sent to HTTPS port" when redirecting to HTTPS endpoint. [#10265](https://github.com/gravitee-io/issues/issues/10265)

**Management API**

* API closed subscription details not working [#10164](https://github.com/gravitee-io/issues/issues/10164)

**Console**

* Resource access is not allowed for a user with Publisher api role [#10032](https://github.com/gravitee-io/issues/issues/10032)
* Sharding tags removed when API configuration updated [#10191](https://github.com/gravitee-io/issues/issues/10191)
* API's member list cannot display more than 10 members [#10212](https://github.com/gravitee-io/issues/issues/10212)
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

## Gravitee API Management 4.4.16 - December 20, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* A WEIGHTED\_ROUND\_ROBIN on a unique endpoint with weight set to 0 leads to gateway thread blocked [#10241](https://github.com/gravitee-io/issues/issues/10241)

**Console**

* Empty endpoint group prevents the update of the Global Healthcheck without clear error message [#10216](https://github.com/gravitee-io/issues/issues/10216)

**Other**

* Warnings about Groovy classes [#10219](https://github.com/gravitee-io/issues/issues/10219)
* API not deployed if OAuth 2.0 resource (Generic and AM) set with system proxy enabled [#10223](https://github.com/gravitee-io/issues/issues/10223)

</details>

## Gravitee API Management 4.4.15 - December 5, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Websocket subprotocol doesn't work in API GW [#10023](https://github.com/gravitee-io/issues/issues/10023)
* Opensearch configuration and ism policy [#10100](https://github.com/gravitee-io/issues/issues/10100)

**Management API**

* Custom Api key is not reusable between multiple environments [#10131](https://github.com/gravitee-io/issues/issues/10131)
* Page Size Drop Down cannot exceed 100 [#10145](https://github.com/gravitee-io/issues/issues/10145)
* 500 error when listing API categories [#10158](https://github.com/gravitee-io/issues/issues/10158)
* \[APIM]\[Portal] Static data access [#10162](https://github.com/gravitee-io/issues/issues/10162)
* Unable to find users with emails containing uppercase letters in Gravitee APIM Console and API requests [#10167](https://github.com/gravitee-io/issues/issues/10167)
* Webhook notification for Subscription\_Accepted event is missing "owner" details [#10187](https://github.com/gravitee-io/issues/issues/10187)
* OpenAPI documentation "Show the URL to download the content" doesn't work [#9891](https://github.com/gravitee-io/issues/issues/9891)

**Other**

* DataDog issues with plugin v2.4.5 [#10176](https://github.com/gravitee-io/issues/issues/10176)
* Health endpoint result is impacted by filtered probes in timeout [#10189](https://github.com/gravitee-io/issues/issues/10189)
* \[gravitee-policy-cache] Timeouts occur when trying to cache a large payload [#10208](https://github.com/gravitee-io/issues/issues/10208)

</details>

<details>

<summary>Improvements</summary>

**Management API**

*   Improve `/apis/{apiId}/import/swagger?definitionVersion=2.0.0` endpoint performances [#10117](https://github.com/gravitee-io/issues/issues/10117)

    Note: Two new environment variables have been introduced to enhance the configuration. The first, `documentation.audit.max-content-size`, is designed to limit the size of the content saved in audits when a Page is created during an import. The second variable, `documentation.swagger.validate-safe-content`, determines whether the content of an imported OAS is validated for safety during the import process.

</details>

## Gravitee API Management 4.4.14 - November 21, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* SSE connections receives messages to the wrong API when connected to rabbitmq [#10020](https://github.com/gravitee-io/issues/issues/10020)

**Management API**

* API webhook notifier is not working for subscriptions [#10056](https://github.com/gravitee-io/issues/issues/10056)
* MAPI v2 : analytics : /respoinse-statuses : error 404 [#10175](https://github.com/gravitee-io/issues/issues/10175)

**Console**

* When creating an endpoint group, the page is not properly refreshed [#10129](https://github.com/gravitee-io/issues/issues/10129)

**Other**

* API CRD export mismatch on plan when using selection rules [#10179](https://github.com/gravitee-io/issues/issues/10179)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Support expression language in ip filtering policy [#10142](https://github.com/gravitee-io/issues/issues/10142)

</details>

## Gravitee API Management 4.4.13 - November 5, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Inconsistent application of validateSubscription flag [#10120](https://github.com/gravitee-io/issues/issues/10120)
* Sync process failed if subscription exists without the linked API [#10140](https://github.com/gravitee-io/issues/issues/10140)

**Management API**

* Page revisions are still present when the associated API is deleted [#10039](https://github.com/gravitee-io/issues/issues/10039)
* API webhook notifier is not working for subscriptions [#10056](https://github.com/gravitee-io/issues/issues/10056)
* Alert Templates are always created in default environment [#10126](https://github.com/gravitee-io/issues/issues/10126)

**Console**

* Code blocks and long strings of text cause overflow of documentation text in the new dev portal [#10048](https://github.com/gravitee-io/issues/issues/10048)

**Other**

* Gateways can not reconnect to the bridge mapi [#10101](https://github.com/gravitee-io/issues/issues/10101)
* \[gravitee-policy-jwt] Complete gateway disruption occurred in retrieving JWT public keys after startup under a heavy load of API calls [#10119](https://github.com/gravitee-io/issues/issues/10119)

</details>

## Gravitee API Management 4.4.12 - October 24, 2024

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

## Gravitee API Management 4.4.11 - October 10, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Invalid error content/type when using v4 emulation [#9930](https://github.com/gravitee-io/issues/issues/9930)
* \[3.20.X and 4.4.X] DNS Resolution fails for hosts having more than 30 A records [#10051](https://github.com/gravitee-io/issues/issues/10051)
* \[Gateway Distributed Sync] Properly differentiate v2 from v4 API events [#10055](https://github.com/gravitee-io/issues/issues/10055)
* \[gravitee-node] Gravitee metrics return NaN [#10070](https://github.com/gravitee-io/issues/issues/10070)
* Error Key champ not present when using Response Template [#9931](https://github.com/gravitee-io/issues/issues/9931)

**Management API**

* Missing braces in webhook notifier messages when special characters are present [#9856](https://github.com/gravitee-io/issues/issues/9856)
* Debug mode not working when too many gateway started events [#9977](https://github.com/gravitee-io/issues/issues/9977)
* Issue on permissions of the ORGANIZATION\_USER role [#10040](https://github.com/gravitee-io/issues/issues/10040)
* Upgrade fails from older version to 4.3.13 with SQL db [#10064](https://github.com/gravitee-io/issues/issues/10064)

**Console**

* Inconsistent display of total APIs between Dashboard and APIs page [#9868](https://github.com/gravitee-io/issues/issues/9868)
* Button color UI bug [#10035](https://github.com/gravitee-io/issues/issues/10035)

**Portal**

* Search bar not sorting results properly on portal for API [#10075](https://github.com/gravitee-io/issues/issues/10075)

**Helm Charts**

* Add serviceAccount in helm chart [#10057](https://github.com/gravitee-io/issues/issues/10057)
* Helm Chart Issue [#10091](https://github.com/gravitee-io/issues/issues/10091)

**Other**

* \[gravitee-policy-groovy] Groovy script compilation blocks the Vertx event loop [#9653](https://github.com/gravitee-io/issues/issues/9653)
* \[gravitee-policy-generate-jwt] Generate JWT policy generates incorrect tokens [#9975](https://github.com/gravitee-io/issues/issues/9975)

</details>

## Gravitee API Management 4.4.10 - September 30, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Transfer subscription does not use new plan when V4 emulation is disabled [#10047](https://github.com/gravitee-io/issues/issues/10047)

**Management API**

* Scheduled requests for dynamic properties are run for each pod in a deployment [#9941](https://github.com/gravitee-io/issues/issues/9941)
* mgmt-api ERROR i.g.r.a.s.n.i.EmailNotifierServiceImpl - No emails extracted from \[] [#9965](https://github.com/gravitee-io/issues/issues/9965)
* Dictionaries not deployed after migration from 3.20.x to 4.x [#10026](https://github.com/gravitee-io/issues/issues/10026)
* Validation for unique names is MISSING in Categories [#10053](https://github.com/gravitee-io/issues/issues/10053)

**Console**

* Info page of API does not refresh when duplicating the API [#9790](https://github.com/gravitee-io/issues/issues/9790)
* Display issue with lateral collapsed menu [#9792](https://github.com/gravitee-io/issues/issues/9792)
* API History shows warning for all policies [#9866](https://github.com/gravitee-io/issues/issues/9866)
* \[APIM] Read only Health check configuration [#9902](https://github.com/gravitee-io/issues/issues/9902)
* API Category endpoint does not work [#9906](https://github.com/gravitee-io/issues/issues/9906)
* Global Dashboard analytics. - filter by status code is not showing data as expected [#9958](https://github.com/gravitee-io/issues/issues/9958)
* Alert Engine parameter not getting updated after modification [#9972](https://github.com/gravitee-io/issues/issues/9972)
* Documentation : clicking "Reset" button doesn't work. [#9994](https://github.com/gravitee-io/issues/issues/9994)
* No display of resource property for redis cache [#10001](https://github.com/gravitee-io/issues/issues/10001)
* Not able to see API events in Dashboard [#10018](https://github.com/gravitee-io/issues/issues/10018)
* Analytics dashboard filtered become empty when a tenant is selected [#10019](https://github.com/gravitee-io/issues/issues/10019)
* Allow API member with right to Env Group to see all group member's of an API [#10021](https://github.com/gravitee-io/issues/issues/10021)
* Redirect user to login screen when JWT token has expired [#10029](https://github.com/gravitee-io/issues/issues/10029)

**Portal**

* Using EL for dynamic limit prevents API subscription through portal [#9978](https://github.com/gravitee-io/issues/issues/9978)
* Users without admin or API access cannot view application API keys in the new dev portal [#10014](https://github.com/gravitee-io/issues/issues/10014)

**Helm Charts**

* APIM Helm chart doesn't configure SSL keystore secret [#9854](https://github.com/gravitee-io/issues/issues/9854)

**Other**

* \[gravitee-entrypoint-webhook] V4 Message API Webhook Timeout Behavior [#9750](https://github.com/gravitee-io/issues/issues/9750)
* \[gravitee-policy-callout-http] Callout policy does not work as expected with fire\&forget mode on v4 engine for v2 API [#9937](https://github.com/gravitee-io/issues/issues/9937)
* Command creation failure in database when illegal character is used on a message header in a webhook API [#9979](https://github.com/gravitee-io/issues/issues/9979)
* \[gravitee-policy-message-filtering] Solace Message Acknowledgement [#10010](https://github.com/gravitee-io/issues/issues/10010)
* \[gravitee-policy-data-logging-masking] DLM policies will not allow the DataDog Reporter to forward logs to DataDog if a property is not found [#10044](https://github.com/gravitee-io/issues/issues/10044)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Management API having lots of "Thread blocked" since the v4 migration [#9952](https://github.com/gravitee-io/issues/issues/9952)

</details>

## Gravitee API Management 4.4.9 - September 13, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Debug mode can impact the sync process [#9976](https://github.com/gravitee-io/issues/issues/9976)
* Handle MongoDB timeout in GatewayNodeMetadataResolver During Installation ID Retrieval [#9982](https://github.com/gravitee-io/issues/issues/9982)

**Management API**

* Upgrade 4.2.5 -> 4.4.2 fails due to existing dashboards type column [#9893](https://github.com/gravitee-io/issues/issues/9893)
* Version is always #1 in api history [#9950](https://github.com/gravitee-io/issues/issues/9950)
* event\_organizations and events\_latest\_organizations liquibase creation script can fail if the organization is linked to multiple environments. [#10011](https://github.com/gravitee-io/issues/issues/10011)

**Console**

* Message-level conditions not working in v4 policy studio [#9335](https://github.com/gravitee-io/issues/issues/9335)
* Unable to change allowed grant type & redirect uri for an application [#9993](https://github.com/gravitee-io/issues/issues/9993)

**Helm Charts**

* \[Helm] Gateway technical ingress miss common label [#9998](https://github.com/gravitee-io/issues/issues/9998)

**Other**

* \[gravitee-tracer-opentelemetry] JWT plan 500 error NPE [#9995](https://github.com/gravitee-io/issues/issues/9995)
* \[gravitee-policy-assign-attributes] - Assign Attributes Policy value field needs to support multiline. [#10012](https://github.com/gravitee-io/issues/issues/10012)

</details>

<details>

<summary>Improvements</summary>

**Helm Charts**

* \[Helm] rework the definition of probes startup, liveness and readiness [#9996](https://github.com/gravitee-io/issues/issues/9996)

</details>

## Gravitee API Management 4.4.8 - August 30, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Decrypt api properties using debug mode [#9943](https://github.com/gravitee-io/issues/issues/9943)
* Impossible to create Date from string in groovy scripts [#9967](https://github.com/gravitee-io/issues/issues/9967)
* XPath not working as expected in gravitee expression language [#9974](https://github.com/gravitee-io/issues/issues/9974)

**Management API**

* Unresponsive/slow UI when emails are sent in APIM 3.x, 4.x [#9522](https://github.com/gravitee-io/issues/issues/9522)

**Console**

* Inappropriate rights for users [#9875](https://github.com/gravitee-io/issues/issues/9875)

</details>

## Gravitee API Management 4.4.7 - August 23, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Unable to start the Gateway when cloud enabled [#9954](https://github.com/gravitee-io/issues/issues/9954)

</details>

## Gravitee API Management 4.4.6 - August 21, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* gRPC APIs latency on remote gRPC backend with large response payloads [#9949](https://github.com/gravitee-io/issues/issues/9949)

**Console**

* gRPC APIs latency on remote gRPC backend with large response payloads [#9949](https://github.com/gravitee-io/issues/issues/9949)

</details>

{% hint style="warning" %}
**Using Cloud?**

Please skip this version and upgrade straight to 4.4.7 **if using Cloud.**
{% endhint %}

## Gravitee API Management 4.4.5 - August 14, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Memory leak when using rate-limit with non-responsive Redis [#9928](https://github.com/gravitee-io/issues/issues/9928)
* V4 api redeployments causes memory leak [#9936](https://github.com/gravitee-io/issues/issues/9936)

**Management API**

* Total APIs for Portal API Category endpoint always returns 0 [#9922](https://github.com/gravitee-io/issues/issues/9922)
* Re: \[APIM/Gateway] Override an email template doesn't work [#9934](https://github.com/gravitee-io/issues/issues/9934)

**Console**

* Application names overflow container under API, Plans and Subscriptions [#9872](https://github.com/gravitee-io/issues/issues/9872)
* UI Doesn't work behind google's Identity-Aware Proxy [#9919](https://github.com/gravitee-io/issues/issues/9919)

</details>

## Gravitee API Management 4.4.4 - August 1, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Request timeout in JWT Plan [#9911](https://github.com/gravitee-io/issues/issues/9911)
* Request timeout when HTTP callout policy with system proxy

**Management API**

* Missing semicolon in Subscriptions Export [#9878](https://github.com/gravitee-io/issues/issues/9878)

**Console**

* Logs Have No Option to Be Opened in New Tab/Window [#9764](https://github.com/gravitee-io/issues/issues/9764)
* Creating a personal token with the same name does not trigger a visual warning [#9873](https://github.com/gravitee-io/issues/issues/9873)

**Other**

* Upgrade failed from 4.3.1 to 4.4.2 [#9901](https://github.com/gravitee-io/issues/issues/9901)
* APIM RPM installation overwrite portal configuration [#9914](https://github.com/gravitee-io/issues/issues/9914)

</details>

{% hint style="warning" %}
**Using SQL database?**

Due to known bugs in 4.4.0 and 4.4.1, please skip these two versions and upgrade straight to 4.4.2 **if using SQL database.**
{% endhint %}

## Gravitee API Management 4.4.3 - July 19, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* OpenSSL is not available any more [#9849](https://github.com/gravitee-io/issues/issues/9849)
* Gateway Unhealthy when rate limit repository is set to none [#9869](https://github.com/gravitee-io/issues/issues/9869)

**Management API**

* We do not allow a different DNS for the API of the portal and the console [#9721](https://github.com/gravitee-io/issues/issues/9721)
* OpenSSL is not available any more [#9849](https://github.com/gravitee-io/issues/issues/9849)
* JDBC Connection Pool Management Error - follow up ticket [#9851](https://github.com/gravitee-io/issues/issues/9851)

**Console**

* Non idempotent operation when creating APIs/Appplications/Users [#9688](https://github.com/gravitee-io/issues/issues/9688)

**Helm Charts**

* We do not allow a different DNS for the API of the portal and the console [#9721](https://github.com/gravitee-io/issues/issues/9721)

</details>

<details>

<summary>Improvements</summary>

**Console**

* Paginated audit events loading to avoid memory issues [#9768](https://github.com/gravitee-io/issues/issues/9768)

</details>

## Gravitee API Management 4.4.2 - July 5, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Upgrade to gio 4.4.0 corrupts API Keys [#9834](https://github.com/gravitee-io/issues/issues/9834)
* Add Base64 class in Expression Language whitelist [#9850](https://github.com/gravitee-io/issues/issues/9850)

**Management API**

* Endpoint's target url can be saved with a space or tab [#9791](https://github.com/gravitee-io/issues/issues/9791)
* Unable delete existing PAT tokens [#9801](https://github.com/gravitee-io/issues/issues/9801)
* Error on platform analytics and logs screens when too many applications and/or APIs [#9823](https://github.com/gravitee-io/issues/issues/9823)

**Console**

* Cannot Save Dashboard Updates in UI [#9771](https://github.com/gravitee-io/issues/issues/9771)
* Unable to Add Members to Group During Group Creation [#9783](https://github.com/gravitee-io/issues/issues/9783)
* Endpoint's target url can be saved with a space or tab [#9791](https://github.com/gravitee-io/issues/issues/9791)
* Policy - losing focus when opening documentation [#9802](https://github.com/gravitee-io/issues/issues/9802)
* Dashboard widget not working [#9820](https://github.com/gravitee-io/issues/issues/9820)
* Client Id not saved between Security section and subscriptions during application creation [#9828](https://github.com/gravitee-io/issues/issues/9828)
* JSON to XML policy does not work with default configuration for V4 proxy APIs [#9833](https://github.com/gravitee-io/issues/issues/9833)

**Portal**

* \[portal-next] Curl command for API key in new portal is incorrect [#9843](https://github.com/gravitee-io/issues/issues/9843)

**Other**

* \[gravitee-resource-oauth2-provider-keycloak] Update of 'gravitee-resource-oauth2-provider-keycloak' Plugin [#9628](https://github.com/gravitee-io/issues/issues/9628)
* \[JDBC] Liquibase errors on upgrade to 4.4.x [#9835](https://github.com/gravitee-io/issues/issues/9835)
* \[JDBC] Getting bad SQL grammar exception when querying JDBC access points with pagination [#9836](https://github.com/gravitee-io/issues/issues/9836)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* PrimaryOwner not given in list of APIs [#9678](https://github.com/gravitee-io/issues/issues/9678)
* Improve API synchronization state computation [#9852](https://github.com/gravitee-io/issues/issues/9852)

</details>

## Gravitee API Management 4.4.1 - June 27, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* 500 Internal server error when logs enabled [#9719](https://github.com/gravitee-io/issues/issues/9719)
* Enabled Logging with condition does not work properly [#9756](https://github.com/gravitee-io/issues/issues/9756)

**Management API**

* Override an email template with multiple REST API [#9445](https://github.com/gravitee-io/issues/issues/9445)
* Cannot Create Local User (no email to set password) [#9680](https://github.com/gravitee-io/issues/issues/9680)
* Error in Gravitee OpenAPI spec [#9711](https://github.com/gravitee-io/issues/issues/9711)
* Improve V4 analytics performance [#9810](https://github.com/gravitee-io/issues/issues/9810)
* Unable to access portal from the redirection link [#9815](https://github.com/gravitee-io/issues/issues/9815)
* \[Multi-tenant] The link in the user creation email is invalid [#9816](https://github.com/gravitee-io/issues/issues/9816)
* \[Multi-tenant] The link in the subscription email is invalid [#9817](https://github.com/gravitee-io/issues/issues/9817)

**Console**

* Correct API properties Expression Language for v4 APIs [#9694](https://github.com/gravitee-io/issues/issues/9694)
* When updating a service account email through API, no mail validation is performed [#9709](https://github.com/gravitee-io/issues/issues/9709)
* Enabled Logging with condition does not work properly [#9756](https://github.com/gravitee-io/issues/issues/9756)

**Helm Charts**

* Missing hazelcast dependency in updater mode [#9809](https://github.com/gravitee-io/issues/issues/9809)

**Other**

* \[gravitee-policy-ipfiltering] CIDR block /32 (single IP) not working in the IP Filtering Policy [#9602](https://github.com/gravitee-io/issues/issues/9602)
* \[gravitee-policy-jwt] 500 error on jwt plan with GATEWAY\_KEYS when using "Emulate v4 engine" [#9693](https://github.com/gravitee-io/issues/issues/9693)
* \[MongoDb] Upgraders should use prefix for collection names [#9807](https://github.com/gravitee-io/issues/issues/9807)
* \[JDBC] Unable to search subscription with Postgresql [#9808](https://github.com/gravitee-io/issues/issues/9808)
* \[MongoDb] Api keys do not have the environment field [#9811](https://github.com/gravitee-io/issues/issues/9811)
* \[MongoDb] Subscription environment is erase when updating a subscription [#9812](https://github.com/gravitee-io/issues/issues/9812)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* The name of API/Application/Plan is not given in list of API's subscriptions [#9679](https://github.com/gravitee-io/issues/issues/9679)

**Other**

* \[gravitee-policy-aws-lambda] Allow to dynamically configure AWS policy credentials [#9444](https://github.com/gravitee-io/issues/issues/9444)

</details>

## Gravitee API Management 4.4.0 - June 27, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Error in the gateway when upgrading connection from http1.1 to http2 [#9757](https://github.com/gravitee-io/issues/issues/9757)
* Socket.io disconnect/reconnect latency [#9766](https://github.com/gravitee-io/issues/issues/9766)

**Management API**

* Pushing an API with API Designer fails [#9761](https://github.com/gravitee-io/issues/issues/9761)
* Inheritance of a V2 API endpoint configuration is not set when importing an OpenAPI spec [#9775](https://github.com/gravitee-io/issues/issues/9775)

**Console**

* Application analytics view logs navigation with filters [#9762](https://github.com/gravitee-io/issues/issues/9762)
* Login via OIDC on Management Console not possible [#9769](https://github.com/gravitee-io/issues/issues/9769)
* Transfer ownership to group shows as option for applications [#9774](https://github.com/gravitee-io/issues/issues/9774)
* Endpoint configuration enable proxy setup just after creation of endpoint [#9780](https://github.com/gravitee-io/issues/issues/9780)
* Filter on 208 status code not available [#9784](https://github.com/gravitee-io/issues/issues/9784)
* IDP Logout does not contain the correct subpath for console. [#9786](https://github.com/gravitee-io/issues/issues/9786)
* Display issues in token generation modal [#9793](https://github.com/gravitee-io/issues/issues/9793)
* In some cases it is difficult to view the configuration in the history menu. [#9800](https://github.com/gravitee-io/issues/issues/9800)

**Portal**

* Current portal incorrectly handles case where API description is "null" [#9785](https://github.com/gravitee-io/issues/issues/9785)
* Documentation too slow [#9788](https://github.com/gravitee-io/issues/issues/9788)

**Other**

* \[gravitee-policy-json-validation] v4 Policy Studio UI doesn't support multi-line values [#9799](https://github.com/gravitee-io/issues/issues/9799)

</details>

<details>

<summary>Improvements</summary>

**Other**

* \[gravitee-policy-groovy] Have access to the binary value of a message content [#9767](https://github.com/gravitee-io/issues/issues/9767)
* \[gravitee-endpoint-kafka] Add a option on kafka endpoint to remove Confluent Wire format header [#9795](https://github.com/gravitee-io/issues/issues/9795)

</details>
