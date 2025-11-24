---
description: API documentation explaining apim 4.7.x.
---

# APIM 4.7.x

## Gravitee API Management 4.7.19 - November 21, 2025

<details>

<summary>Bug Fixes</summary>

**Management API**

* Valid OpenAPI are being rejected at import for v4 APIs [#10975](https://github.com/gravitee-io/issues/issues/10975)

**Console**

* Applications Graph analytics issue [#10837](https://github.com/gravitee-io/issues/issues/10837)

**Portal**

* Documentation pages in new dev portal show misaligned content [#10947](https://github.com/gravitee-io/issues/issues/10947)
* New Developer Portal - Guide Navigation Redirects Incorrectly [#10962](https://github.com/gravitee-io/issues/issues/10962)

**Other**

* Cannot use access\_token in SASL JAAS config for OAUTHBEARER mechanism [#10927](https://github.com/gravitee-io/issues/issues/10927)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Redis - Unable to connect to Redis WRONGPASS invalid username-password pair or user is disabled [#10966](https://github.com/gravitee-io/issues/issues/10966)

**Management API**

* User groups API now supports filtering by environmentId query parameter [#10788](https://github.com/gravitee-io/issues/issues/10788)

**Other**

* Allow Json validation policy to use a nullable field if provided in schema [#10828](https://github.com/gravitee-io/issues/issues/10828)
* OpenTelemetry API gateway attribute values and trace linking [#10898](https://github.com/gravitee-io/issues/issues/10898)

</details>

## Gravitee API Management 4.7.18 - November 7, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Sec-WebSocket-Protocol header not propagated in WebSocket connections for v4 APIs [#10950](https://github.com/gravitee-io/issues/issues/10950)

**Management API**

* Using payload filter in v2 API logs does not always return correct number of results [#10747](https://github.com/gravitee-io/issues/issues/10747)
* Difference between policy names based on the creation method. [#10803](https://github.com/gravitee-io/issues/issues/10803)
* Search API feature not working on Developer Portal [#10892](https://github.com/gravitee-io/issues/issues/10892)
* Path mapping on import fails for certain paths [#10909](https://github.com/gravitee-io/issues/issues/10909)

**Console**

* Applied filter tags disappear in log view [#10931](https://github.com/gravitee-io/issues/issues/10931)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* API traffic runtime logs incorrectly show endpoint response 200 [#10896](https://github.com/gravitee-io/issues/issues/10896)

**Console**

* Update Management API connection failure banner copy [#10945](https://github.com/gravitee-io/issues/issues/10945)

**Other**

* Configure the header name to read API Key from [#10939](https://github.com/gravitee-io/issues/issues/10939)

</details>

## Gravitee API Management 4.7.17 - October 24, 2025

<details>

<summary>Bug Fixes</summary>

**Management API**

* Flow id missing in create api response of V4 APIs [#10888](https://github.com/gravitee-io/issues/issues/10888)
* Visibility flag is not getting updated as part of api creation using mAPI [#10895](https://github.com/gravitee-io/issues/issues/10895)
* Federation Agent connection causes ThreadBlocked while fetching token [#10913](https://github.com/gravitee-io/issues/issues/10913)

**Console**

* Fetching groups for an application takes a really long time [#10709](https://github.com/gravitee-io/issues/issues/10709)

**Other**

* Webhook Entrypoint: Linear retry delay incorrectly interpreted as milliseconds instead of seconds [#10520](https://github.com/gravitee-io/issues/issues/10520)
* Ensure IPv4 backward compatibility in docker images [#10859](https://github.com/gravitee-io/issues/issues/10859)
* Requests blocked (403) when IP Filtering Policy contains both hostname and IP [#10866](https://github.com/gravitee-io/issues/issues/10866)
* Inconsistency in portal sub-path configuration between IPv4 and IPv6 NGINX files [#10904](https://github.com/gravitee-io/issues/issues/10904)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* 502 Bad Gateway Error when backend response headers exceed endpoint size limit [#10863](https://github.com/gravitee-io/issues/issues/10863)

**Console**

* New updated API picture & background not visible without refreshing the page [#10857](https://github.com/gravitee-io/issues/issues/10857)
* 502 Bad Gateway Error when backend response headers exceed endpoint size limit [#10863](https://github.com/gravitee-io/issues/issues/10863)

**Helm Charts**

* Gravitee Gateway removes password attribute from SSL section when password is empty string "" [#10861](https://github.com/gravitee-io/issues/issues/10861)

</details>

## Gravitee API Management 4.7.16 - October 10, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Read timeout on v4 returns 500 [#10767](https://github.com/gravitee-io/issues/issues/10767)
* Webhook subscription is not stopped on 500 error [#10799](https://github.com/gravitee-io/issues/issues/10799)
* EL request.xmlContent Fails with XML Declaration [#10842](https://github.com/gravitee-io/issues/issues/10842)
* Impossible to increase backend HTTP/2 window sizes [#10852](https://github.com/gravitee-io/issues/issues/10852)

**Management API**

* Image not updated with mAPI [#10809](https://github.com/gravitee-io/issues/issues/10809)

**Other**

* Two users created with identical email addresses [#10423](https://github.com/gravitee-io/issues/issues/10423)
* Webhook Entrypoint: "No Retry" configuration ignores setting and uses default linear retry. [#10519](https://github.com/gravitee-io/issues/issues/10519)
* Custom API keys are truncated to 64 characters when created through the console UI [#10873](https://github.com/gravitee-io/issues/issues/10873)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Character length for API description is only 4000 for Postgres [#10825](https://github.com/gravitee-io/issues/issues/10825)
* File reporter creates empty log files despite event exclusion. [#10853](https://github.com/gravitee-io/issues/issues/10853)

</details>

## Gravitee API Management 4.7.15 - September 26, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway rejects client certificates missing BEGIN/END markers in X-Gravitee-Client-Cert header [#10816](https://github.com/gravitee-io/issues/issues/10816)

**Management API**

* Unable to search federated APIs using metadata [#10676](https://github.com/gravitee-io/issues/issues/10676)
* Group edit fails for APIs with missing visibility [#10804](https://github.com/gravitee-io/issues/issues/10804)

**Console**

* Prevent multiple primary owners when API Primary Owner mode is set to Group [#10629](https://github.com/gravitee-io/issues/issues/10629)
* Gap between the "Health Check Dashboard" date and the "Dashboard API Traffic" date [#10813](https://github.com/gravitee-io/issues/issues/10813)
* Audit history shows incorrect API groups and path mappings deletion [#10814](https://github.com/gravitee-io/issues/issues/10814)
* Image appears too large inside dropdown menu [#10819](https://github.com/gravitee-io/issues/issues/10819)

**Helm Charts**

* Frequent Prometheus endpoint calls can cause OOM errors [#10466](https://github.com/gravitee-io/issues/issues/10466)

**Other**

* IPV6 CIDR ranges do not work in the IP filtering policy [#10656](https://github.com/gravitee-io/issues/issues/10656)
* Using Check Topic Existence with the AWS MSK IAM SASL mechanism results in errors [#10746](https://github.com/gravitee-io/issues/issues/10746)
* Remove corrupted subscriptions from database [#10821](https://github.com/gravitee-io/issues/issues/10821)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Character length for entrypoints is only 64 for Postgres [#10698](https://github.com/gravitee-io/issues/issues/10698)

**Helm Charts**

* Add helm.sh/chart to pod template annotations [#10832](https://github.com/gravitee-io/issues/issues/10832)

**Other**

* \[JSON threat protection policy] add an option to block JSON with duplicated keys [#10841](https://github.com/gravitee-io/issues/issues/10841)
* OAS Plugin decoding issue – validation fails with encoded values [#10845](https://github.com/gravitee-io/issues/issues/10845)

</details>

## Gravitee API Management 4.7.14 - September 12, 2025

<details>

<summary>Bug Fixes</summary>

**Management API**

* Memory issues when loading audit events [#10582](https://github.com/gravitee-io/issues/issues/10582)
* Heavy latencies using Audit section with a larger number of apps.[#10783](https://github.com/gravitee-io/issues/issues/10783)
* Audit History groups fetch timeout[#10682](https://github.com/gravitee-io/issues/issues/10682)
* Bad behavior on weighted round robin[#10405](https://github.com/gravitee-io/issues/issues/10405)
* Dynamic Properties configuration is not exported when exporting a V4 API[#10726](https://github.com/gravitee-io/issues/issues/10726)

**Console**

* Unable to import path mapping from swagger document [#10810](https://github.com/gravitee-io/issues/issues/10810)
* Alert creation form missing fields on smaller screens[#10823](https://github.com/gravitee-io/issues/issues/10823)
* Slow loading when viewing 'Tasks' on Console[#10650](https://github.com/gravitee-io/issues/issues/10650)
* Bad behavior on weighted round robin[#10405](https://github.com/gravitee-io/issues/issues/10405)

</details>

## Gravitee API Management 4.7.13 - August 29, 2025

<details>

<summary>Bug Fixes</summary>

**Management API**

* Random configuration fields updated when associating a group to an API [#10632](https://github.com/gravitee-io/issues/issues/10632)
* Unable to Sync API [#10662](https://github.com/gravitee-io/issues/issues/10662)
* Import V4 definition won't set flowExecution's matchRequired attribute [#10715](https://github.com/gravitee-io/issues/issues/10715)
* User with an ADMIN environment role is unable to view a documentation page they just created in the Admin Console, receiving a 401 Unauthorized error [#10749](https://github.com/gravitee-io/issues/issues/10749)
* API V4 export does not include CORS configuration [#10755](https://github.com/gravitee-io/issues/issues/10755)

**Console**

* Random configuration fields updated when associating a group to an API [#10632](https://github.com/gravitee-io/issues/issues/10632)
* Orphan gateways result in other gateways not being displayed in the console UI [#10653](https://github.com/gravitee-io/issues/issues/10653)
* User with an ADMIN environment role is unable to view a documentation page they just created in the Admin Console, receiving a 401 Unauthorized error [#10749](https://github.com/gravitee-io/issues/issues/10749)
* Current page of paged application api resource is off by 1 [#10756](https://github.com/gravitee-io/issues/issues/10756)
* Application name has max length limit only when updating in the UI [#10761](https://github.com/gravitee-io/issues/issues/10761)
* Primary group owner field is inaccessible when creating v2 APIs [#10762](https://github.com/gravitee-io/issues/issues/10762)

</details>

## Gravitee API Management 4.7.12 - August 15, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Bump gravitee-endpoint-rabbitmq post APIM-10477 [#10741](https://github.com/gravitee-io/issues/issues/10741)

**Management API**

* Searching with ownerName in Developer Portal does not result in correct behaviour after a change in the group name. [#10380](https://github.com/gravitee-io/issues/issues/10380)
* The first deployments of a v2 API have a repeat publish number in the audit history [#10566](https://github.com/gravitee-io/issues/issues/10566)
* Updates to individual API endpoint configurations do not prompt the deploy API banner [#10568](https://github.com/gravitee-io/issues/issues/10568)
* V4 plan update without validation field can cause API error [#10660](https://github.com/gravitee-io/issues/issues/10660)
* Application creation error [#10717](https://github.com/gravitee-io/issues/issues/10717)
* Api not being able to be deploy when out of sync [#10725](https://github.com/gravitee-io/issues/issues/10725)
* Stale Search Index After API Ownership Transfer [#10730](https://github.com/gravitee-io/issues/issues/10730)

**Console**

* “Delete” button disappears for folders and pages when the browser window is too narrow [#10692](https://github.com/gravitee-io/issues/issues/10692)
* APIM Console - Long email in User Account causing display issue [#10734](https://github.com/gravitee-io/issues/issues/10734)

**Portal**

* Use of additional config metadata in portal API when creating applications [#10563](https://github.com/gravitee-io/issues/issues/10563)

**Other**

* Http code 0 in log list while log details gives a code 200 prevent correct count in analytics [#10607](https://github.com/gravitee-io/issues/issues/10607)
* \[gravitee-policy-kafka-acl] Partial authorization on a multi topics PRODUCE & FETCH [#10714](https://github.com/gravitee-io/issues/issues/10714)
* UI Bug: Management Console application logs headers are truncated/squished with long values [#10721](https://github.com/gravitee-io/issues/issues/10721)
* OOM error in gateway when management repository becomes unresponsive causes worker thread starvation and analytics reporter blockage [#10723](https://github.com/gravitee-io/issues/issues/10723)
* Gravitee gateway sending thousands of requests per second [#10732](https://github.com/gravitee-io/issues/issues/10732)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Update oas-validation policy's swagger-request-validator version [#10742](https://github.com/gravitee-io/issues/issues/10742)

</details>

## Gravitee API Management 4.7.11 - August 1, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Heap memory possible leakage due to missing equals and hashcode methods on all fields. [#10701](https://github.com/gravitee-io/issues/issues/10701)

**Management API**

* Groups Mappings do not work if no Default Role is selected to API and Application [#10271](https://github.com/gravitee-io/issues/issues/10271)
* Sharding Tag Persists on API preview After Deletion [#10626](https://github.com/gravitee-io/issues/issues/10626)
* Unable to search by label for v4 APIs [#10671](https://github.com/gravitee-io/issues/issues/10671)
* If we send null for the groups field the value should not be updated in DB in any scenario (PO is a user, PO is a group, etc) [#10686](https://github.com/gravitee-io/issues/issues/10686)

**Console**

* The error key CLIENT\_ABORTED\_DURING\_RESPONSE\_ERROR is not present in the console UI. [#10683](https://github.com/gravitee-io/issues/issues/10683)

**Portal**

* Portal Try it Out feature taking a long time to load [#10595](https://github.com/gravitee-io/issues/issues/10595)
* Openapi contracts with binary examples can not be read by the dev portal [#10639](https://github.com/gravitee-io/issues/issues/10639)

**Other**

* JDBC Error in Gravitee when querying large number of applications using IN clause [#10496](https://github.com/gravitee-io/issues/issues/10496)
* Console : Image Not Fitting Avatar Due to Aspect Ratio [#10649](https://github.com/gravitee-io/issues/issues/10649)

</details>

## Gravitee API Management 4.7.10 - July 18, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Traceparent HTTP header is not available in the policy chain [#10511](https://github.com/gravitee-io/issues/issues/10511)
* Kafka TLS keystore loaded too many times [#10646](https://github.com/gravitee-io/issues/issues/10646)

**Management API**

* Wrong count in the analytics of API v4 [#10604](https://github.com/gravitee-io/issues/issues/10604)

**Console**

* Identity provider roles mapping UI bug [#10503](https://github.com/gravitee-io/issues/issues/10503)
* Instances of calling the groups endpoint on create V2 API page time out when a large number of groups exist [#10603](https://github.com/gravitee-io/issues/issues/10603)

**Other**

* Mock policy is not generated if the openAPI spec data uses a type of string and format of date-time [#10619](https://github.com/gravitee-io/issues/issues/10619)

</details>

## Gravitee API Management 4.7.9 - July 4, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Hardcoded value for health check in 4.7 versions and above in docker images ( for both gateway and mapi ) [#10644](https://github.com/gravitee-io/issues/issues/10644)

**Management API**

* Subscriptions in the subscriptions tab of an application seem to only show the first 10 item [#10529](https://github.com/gravitee-io/issues/issues/10529)
* Users with both group inheritance and individual access to applications are limited in which applications to which they can subscribe [#10601](https://github.com/gravitee-io/issues/issues/10601)
* Hardcoded value for health check in 4.7 versions and above in docker images ( for both gateway and mapi ) [#10644](https://github.com/gravitee-io/issues/issues/10644)
* Using jsonPath in Assign Attributes policy prevents sending transformed body in HTTP Callout policy

**Console**

* Wrong display when adding a user to a group [#10558](https://github.com/gravitee-io/issues/issues/10558)
* Prevent API Modification for Unauthorized API Users [#10594](https://github.com/gravitee-io/issues/issues/10594)

**Portal**

* Subscriptions in the subscriptions tab of an application seem to only show the first 10 item [#10529](https://github.com/gravitee-io/issues/issues/10529)

**Other**

* Unable to add a group to an existing user using console [#10378](https://github.com/gravitee-io/issues/issues/10378)
* Console : Categories Page doesn't show updated image for any category [#10523](https://github.com/gravitee-io/issues/issues/10523)
* Primary owner Group should not be removed from an API [#10580](https://github.com/gravitee-io/issues/issues/10580)
* Custom policy depending on gravitee-resource-oauth2-provider-generic [#10620](https://github.com/gravitee-io/issues/issues/10620)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Enable multi-tenant support for Dictionaries by default [#10637](https://github.com/gravitee-io/issues/issues/10637)

**Other**

* Increase character limit of condition field in flow\_selectors table [#10560](https://github.com/gravitee-io/issues/issues/10560)

</details>

## Gravitee API Management 4.7.8 - June 20, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Debug mode adding extra slash on endpoint [#10438](https://github.com/gravitee-io/issues/issues/10438)

**Console**

* No error message raised while deleting folder [#10608](https://github.com/gravitee-io/issues/issues/10608)

**Helm Charts**

* Multi-Tenant dictionaries: align values.yml and gravitee.yml [#10627](https://github.com/gravitee-io/issues/issues/10627)

**Other**

* Problem IP Filtering / Host resolving [#10592](https://github.com/gravitee-io/issues/issues/10592)
* Solace webhook subscription 500 internal server error [#10622](https://github.com/gravitee-io/issues/issues/10622)

</details>

## Gravitee API Management 4.7.7 - June 13, 2025

<details>

<summary>Bug Fixes</summary>

**Management API**

* Portal & Email/Webhook notification not working for registered user [#10387](https://github.com/gravitee-io/issues/issues/10387)
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

## Gravitee API Management 4.7.6 - May 28, 2025

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
* Alert is getting triggered, we are seeing it in the history tab, but we cannot see the alert in webhook. [#10550](https://github.com/gravitee-io/issues/issues/10550)
* Management transfer\_ownership API is allowing multiple primary owners on applications [#10572](https://github.com/gravitee-io/issues/issues/10572)
* Remove System.out.println statement [#10583](https://github.com/gravitee-io/issues/issues/10583)

**Console**

* Tenant name verification issue [#10517](https://github.com/gravitee-io/issues/issues/10517)
* Alert filter doesn't show list of APIs in selection box. [#10532](https://github.com/gravitee-io/issues/issues/10532)
* Groups page fails to load when too many groups exist because no pagination [#10538](https://github.com/gravitee-io/issues/issues/10538)
* Group management for APIs broken [#10542](https://github.com/gravitee-io/issues/issues/10542)
* Application filter 'not equals to' operator is unusable [#10546](https://github.com/gravitee-io/issues/issues/10546)
* \[Console] Add endpoint group creates an infinite loop [#10584](https://github.com/gravitee-io/issues/issues/10584)

**Helm Charts**

* Fix Elasticsearch dependency configuration of replicas in APIM helm chart [#10541](https://github.com/gravitee-io/issues/issues/10541)

</details>

<details>

<summary>Improvements</summary>

**Console**

* \[UI] Add text to indicate max image size allowed [#10561](https://github.com/gravitee-io/issues/issues/10561)

</details>

## Gravitee API Management 4.7.5 - May 9, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* CompositeByteBuf is creating a high volume of logs [#10539](https://github.com/gravitee-io/issues/issues/10539)
* Problems with HTTP code 502 because of keepalive

**Management API**

* Rollback does not work for the v4 emulation button [#10190](https://github.com/gravitee-io/issues/issues/10190)
* Application search does not work if search term pattern matches \_id pattern [#10487](https://github.com/gravitee-io/issues/issues/10487)

**Console**

* Local link to internal section dose not work in documentation [#10180](https://github.com/gravitee-io/issues/issues/10180)
* APIM API Throwing HTTP 500 On a Specific Returned Page [#10372](https://github.com/gravitee-io/issues/issues/10372)
* Settings-> Groups : 'Allows invitation via user search' is NOT working as expected [#10485](https://github.com/gravitee-io/issues/issues/10485)
* Application search does not work if search term pattern matches \_id pattern [#10487](https://github.com/gravitee-io/issues/issues/10487)
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

## Gravitee API Management 4.7.4 - April 25, 2025

<details>

<summary>Bug Fixes</summary>

**Management API**

* Global Alert configuration page does not refresh properly after change [#10436](https://github.com/gravitee-io/issues/issues/10436)
* Issue with Policy Execution Order [#10486](https://github.com/gravitee-io/issues/issues/10486)

**Console**

* API Traffic Settings page is not visible for V4 Message APIs due to permission issue for default roles [#10386](https://github.com/gravitee-io/issues/issues/10386)

**Portal**

* Portal-Next shows all Unpublished apis [#10505](https://github.com/gravitee-io/issues/issues/10505)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Type of application is removed after update\[ApplicationType \[null] cannot be found]. [#10359](https://github.com/gravitee-io/issues/issues/10359)

</details>

## Gravitee API Management 4.7.3 - April 17, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Bug in io.gravitee.connector.http.HttpConnection.java exceptionHandler [#10439](https://github.com/gravitee-io/issues/issues/10439)

**Console**

* Logs filter display Unpublished plan [#10480](https://github.com/gravitee-io/issues/issues/10480)

</details>

## Gravitee API Management 4.7.2 - April 11, 2025

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
* Data export inconsistencies in APIv4 (members, metadata, and plans) [#10459](https://github.com/gravitee-io/issues/issues/10459)
* v4 api : Unable to manage groups for all api types [#10471](https://github.com/gravitee-io/issues/issues/10471)
* Adding an unknown group id to excluded groups on a plan in v4 apis removes all excluded groups and prevents exports of the API [#10473](https://github.com/gravitee-io/issues/issues/10473)

**Console**

* Failed association of groups to APIs [#10211](https://github.com/gravitee-io/issues/issues/10211)
* V4 Flows cannot be duplicated or disabled [#10242](https://github.com/gravitee-io/issues/issues/10242)
* Unable to update Alert Rate Condition after clearing aggregation field [#10332](https://github.com/gravitee-io/issues/issues/10332)
* Newly created applications are not associated to groups that have "Associate automatically to every new application" enabled [#10457](https://github.com/gravitee-io/issues/issues/10457)
* Resolver parameter for JWT plan none accessible [#10476](https://github.com/gravitee-io/issues/issues/10476)

**Portal**

* Saved application alert in Dev Portal fails to display percentage value [#10446](https://github.com/gravitee-io/issues/issues/10446)
* Registration Confirmation URL incorrectly includes full path and query parameters [#10456](https://github.com/gravitee-io/issues/issues/10456)

</details>

## Gravitee API Management 4.7.1 - April 4, 2025

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
* API Export does not "respect" selected export options [#10455](https://github.com/gravitee-io/issues/issues/10455)
* Display only http methods in debug mode tool [#10467](https://github.com/gravitee-io/issues/issues/10467)

**Portal**

* NewDevPortal - Swagger expands outside of allowed frame [#10461](https://github.com/gravitee-io/issues/issues/10461)
* Unable to show Swagger docs for Native api on Portal-Next [#10462](https://github.com/gravitee-io/issues/issues/10462)

**Other**

* Groups not automatically added to new applications when they should be [#10470](https://github.com/gravitee-io/issues/issues/10470)

</details>
