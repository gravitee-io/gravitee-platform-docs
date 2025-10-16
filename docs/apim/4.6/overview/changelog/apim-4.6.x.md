---
description: >-
  This page contains the changelog entries for APIM 4.6.x and any future patch
  APIM 4.6.x releases
---

# APIM 4.6.x

## Gravitee API Management 4.6.22 - October 10, 2025
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

## Gravitee API Management 4.6.21 - September 26, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway rejects client certificates missing BEGIN/END markers in X-Gravitee-Client-Cert header [#10816](https://github.com/gravitee-io/issues/issues/10816)

**Management API**

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



## Gravitee API Management 4.6.20 - September 12, 2025
<details>

<summary>Bug Fixes</summary>

**Management API**

* Memory issues when loading audit events [#10582](https://github.com/gravitee-io/issues/issues/10582)
* Heavy latencies using Audit section with a larger number of apps.[#10783](https://github.com/gravitee-io/issues/issues/10783)
* Audit History groups fetch timeout[#10682](https://github.com/gravitee-io/issues/issues/10682)
* Bad behavior on weighted round robin[#10405](https://github.com/gravitee-io/issues/issues/10405)

**Console**

* Unable to import path mapping from swagger document [#10810](https://github.com/gravitee-io/issues/issues/10810)
* Alert creation form missing fields on smaller screens[#10823](https://github.com/gravitee-io/issues/issues/10823)
* Slow loading when viewing 'Tasks' on Console[#10650](https://github.com/gravitee-io/issues/issues/10650)
* Bad behavior on weighted round robin[#10405](https://github.com/gravitee-io/issues/issues/10405)

</details>


## Gravitee API Management 4.6.19 - August 29, 2025
<details>

<summary>Bug Fixes</summary>

**Management API**

* Random configuration fields updated when associating a group to an API [#10632](https://github.com/gravitee-io/issues/issues/10632)
* Unable to Sync API [#10662](https://github.com/gravitee-io/issues/issues/10662)
* Import V4 definition won't set flowExecution's matchRequired attribute [#10715](https://github.com/gravitee-io/issues/issues/10715)
* User with an ADMIN environment role is unable to view a documentation page they just created in the Admin Console, receiving a 401 Unauthorized error [#10749](https://github.com/gravitee-io/issues/issues/10749)

**Console**

* Random configuration fields updated when associating a group to an API [#10632](https://github.com/gravitee-io/issues/issues/10632)
* Orphan gateways result in other gateways not being displayed in the console UI [#10653](https://github.com/gravitee-io/issues/issues/10653)
* User with an ADMIN environment role is unable to view a documentation page they just created in the Admin Console, receiving a 401 Unauthorized error [#10749](https://github.com/gravitee-io/issues/issues/10749)
* Current page of paged application api resource is off by 1 [#10756](https://github.com/gravitee-io/issues/issues/10756)
* Application name has max length limit only when updating in the UI [#10761](https://github.com/gravitee-io/issues/issues/10761)
* Primary group owner field is inaccessible when creating v2 APIs [#10762](https://github.com/gravitee-io/issues/issues/10762)

</details>



## Gravitee API Management 4.6.18 - August 15, 2025
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
 
## Gravitee API Management 4.6.17 - August 1, 2025
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

* The error key CLIENT_ABORTED_DURING_RESPONSE_ERROR is not present in the console UI. [#10683](https://github.com/gravitee-io/issues/issues/10683)

**Portal**

*  Portal Try it Out feature taking a long time to load [#10595](https://github.com/gravitee-io/issues/issues/10595)
* Openapi contracts with binary examples can not be read by the dev portal  [#10639](https://github.com/gravitee-io/issues/issues/10639)

**Other**

* JDBC Error in Gravitee when querying large number of applications using IN clause  [#10496](https://github.com/gravitee-io/issues/issues/10496)
* Console : Image Not Fitting Avatar Due to Aspect Ratio [#10649](https://github.com/gravitee-io/issues/issues/10649)

</details>


 
## Gravitee API Management 4.6.16 - July 18, 2025
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


 
## Gravitee API Management 4.6.15 - July 4, 2025
<details>

<summary>Bug Fixes</summary>

**Management API**

* Subscriptions in the subscriptions tab of an application seem to only show the first 10 item [#10529](https://github.com/gravitee-io/issues/issues/10529)
* Users with both group inheritance and individual access to applications are limited in which applications to which they can subscribe [#10601](https://github.com/gravitee-io/issues/issues/10601)
* Using jsonPath in Assign Attributes policy prevents sending transformed body in HTTP Callout policy

**Console**

* Triggered alerts do not send notification [#10440](https://github.com/gravitee-io/issues/issues/10440)
* Wrong display when adding a user to a group [#10558](https://github.com/gravitee-io/issues/issues/10558)
* Prevent API Modification for Unauthorized API Users [#10594](https://github.com/gravitee-io/issues/issues/10594)

**Portal**

* Subscriptions in the subscriptions tab of an application seem to only show the first 10 item [#10529](https://github.com/gravitee-io/issues/issues/10529)

**Other**

* Unable to add a group to an existing user using console [#10378](https://github.com/gravitee-io/issues/issues/10378)
* Console : Categories Page doesn't show updated image for any category [#10523](https://github.com/gravitee-io/issues/issues/10523)
* Primary owner Group should not be removed from an API  [#10580](https://github.com/gravitee-io/issues/issues/10580)
* Custom policy depending on gravitee-resource-oauth2-provider-generic  [#10620](https://github.com/gravitee-io/issues/issues/10620)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Enable multi-tenant support for Dictionaries by default [#10637](https://github.com/gravitee-io/issues/issues/10637)

**Other**

* Increase character limit of condition field in flow_selectors table [#10560](https://github.com/gravitee-io/issues/issues/10560)

</details>



## Gravitee API Management 4.6.14 - June 20, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Debug mode adding extra slash on endpoint [#10438](https://github.com/gravitee-io/issues/issues/10438)

**Management API**

* Error on import v4 definition [#10593](https://github.com/gravitee-io/issues/issues/10593)
* Error on Portal admin login when subscription has null API [#10618](https://github.com/gravitee-io/issues/issues/10618)

**Console**

* No error message raised while deleting folder [#10608](https://github.com/gravitee-io/issues/issues/10608)

**Helm Charts**

* Multi-Tenant dictionaries: align values.yml and gravitee.yml [#10627](https://github.com/gravitee-io/issues/issues/10627)

**Other**

* Problem IP Filtering / Host resolving [#10592](https://github.com/gravitee-io/issues/issues/10592)
* Solace webhook subscription 500 internal server error [#10622](https://github.com/gravitee-io/issues/issues/10622)

</details>

## Gravitee API Management 4.6.13 - June 13, 2025

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

## Gravitee API Management 4.6.12 - May 28, 2025

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

**Other**

* Unable to launch Lambda with lambda Policy [#10570](https://github.com/gravitee-io/issues/issues/10570)

</details>

<details>

<summary>Improvements</summary>

**Console**

* \[UI] Add text to indicate max image size allowed [#10561](https://github.com/gravitee-io/issues/issues/10561)

</details>

## Gravitee API Management 4.6.11 - May 9, 2025

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

* Portal-Next shows all Unpublished apis [#10505](https://github.com/gravitee-io/issues/issues/10505)

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
* v4 api : Unable to manage groups for all api types [#10471](https://github.com/gravitee-io/issues/issues/10471)
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
* Renewed api key is "available" on closed subscription [#10396](https://github.com/gravitee-io/issues/issues/10396)
* API flows are duplicated when called multiple times in row with the management API [#10408](https://github.com/gravitee-io/issues/issues/10408)
* Import of an API does not ignore unknown access control groups that are present in another environment [#10414](https://github.com/gravitee-io/issues/issues/10414)
* Cannot list applications on Portal UI when group is removed from console [#10419](https://github.com/gravitee-io/issues/issues/10419)

**Console**

* Shared API key doesn't always bind to subscriptions when concurrent requests are made [#10146](https://github.com/gravitee-io/issues/issues/10146)
* In logs, the "users" column is no more available [#10311](https://github.com/gravitee-io/issues/issues/10311)
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
* Absolute links in gravitee-apim-console-webui (ignoring ) [#10394](https://github.com/gravitee-io/issues/issues/10394)

**Portal**

* Text in API documentation does not breakline vertically within container [#10198](https://github.com/gravitee-io/issues/issues/10198)
* Table of content on right side should be wrapped. [#10290](https://github.com/gravitee-io/issues/issues/10290)
* New Developer Portal - Changes to Header and Footer Not being applied [#10319](https://github.com/gravitee-io/issues/issues/10319)
* IPv6 crashes UI container if IPv6 is not enabled in environment [#10392](https://github.com/gravitee-io/issues/issues/10392)

**Other**

* JSON validation policy causes the message not to be published [#10323](https://github.com/gravitee-io/issues/issues/10323)
* Impossible to edit / save a V4 Kafka Gateway API using Postgres as the Management DB [#10393](https://github.com/gravitee-io/issues/issues/10393)
* 500 error on jwt plan when using "Emulate v4 engine" and gateway keys configuration [#10420](https://github.com/gravitee-io/issues/issues/10420)

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
* API flows are duplicated when saved multiple times in the row [#10355](https://github.com/gravitee-io/issues/issues/10355)

**Console**

* Enhance Rights Message in Management Portal [#10138](https://github.com/gravitee-io/issues/issues/10138)
* Platform analytics shows incorrect result in status pie-chart [#10267](https://github.com/gravitee-io/issues/issues/10267)
* Analytics logs exported as CSV are entirely on one line [#10350](https://github.com/gravitee-io/issues/issues/10350)
* API flows are duplicated when saved multiple times in the row [#10355](https://github.com/gravitee-io/issues/issues/10355)

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
* Application updates remove the picture [#10302](https://github.com/gravitee-io/issues/issues/10302)

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
