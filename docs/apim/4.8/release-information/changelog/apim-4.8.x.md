# APIM 4.8.x
 
## Gravitee API Management 4.8.13 - November 21, 2025
<details>

<summary>Bug Fixes</summary>

**Management API**

* Shared policy not being executed in debug mode [#10885](https://github.com/gravitee-io/issues/issues/10885)
* Valid OpenAPI are being rejected at import for v4 APIs [#10975](https://github.com/gravitee-io/issues/issues/10975)

**Console**

* Applications Graph analytics issue [#10837](https://github.com/gravitee-io/issues/issues/10837)
* Export was exposing unwanted `hrid` field in CRD export [#10937](https://github.com/gravitee-io/issues/issues/10937)

**Portal**

* Documentation pages in new dev portal show misaligned content [#10947](https://github.com/gravitee-io/issues/issues/10947)
* New Developer Portal - Guide Navigation Redirects Incorrectly [#10962](https://github.com/gravitee-io/issues/issues/10962)

**Other**

* Cannot use access_token in SASL JAAS config for OAUTHBEARER mechanism [#10927](https://github.com/gravitee-io/issues/issues/10927)
* AI Prompt Token Tracking Policy skipped with Non-Strict application/json Content-Type [#10964](https://github.com/gravitee-io/issues/issues/10964)

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
* Performance Optimization for API Configuration Validation [#10989](https://github.com/gravitee-io/issues/issues/10989)

</details>


 
## Gravitee API Management 4.8.12 - November 7, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Allow disabling Vertx Native Transport [#10889](https://github.com/gravitee-io/issues/issues/10889)
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

* Enable configurable API Key header name in API Key plan [#10939](https://github.com/gravitee-io/issues/issues/10939)

</details>


 
## Gravitee API Management 4.8.11 - October 24, 2025
<details>

<summary>Bug Fixes</summary>

**Management API**

* Flow id missing in create api response of V4 APIs [#10888](https://github.com/gravitee-io/issues/issues/10888)
* Visibility flag is not getting updated as part of api creation using mAPI [#10895](https://github.com/gravitee-io/issues/issues/10895)
* Federation Agent connection causes ThreadBlocked while fetching token [#10913](https://github.com/gravitee-io/issues/issues/10913)

**Console**

* Fetching groups for an application takes a really long time [#10709](https://github.com/gravitee-io/issues/issues/10709)
* Impossible to delete member group [#10836](https://github.com/gravitee-io/issues/issues/10836)

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

* 502 Bad Gateway Error when backend response headers exceed endpoint size limit [#10863](https://github.com/gravitee-io/issues/issues/10863)

</details>


 
## Gravitee API Management 4.8.10 - October 17, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Debug mode can trigger ThreadBlocked with Bridge repository [#10886](https://github.com/gravitee-io/issues/issues/10886)

**Console**

* Adding a policy at Org level causes a "HTTP 404 Not Found" error in UI. [#10666](https://github.com/gravitee-io/issues/issues/10666)

</details>

<details>

<summary>Improvements</summary>

**Console**

* New updated API picture & background not visible without refreshing the page [#10857](https://github.com/gravitee-io/issues/issues/10857)

**Helm Charts**

* Gravitee Gateway removes password attribute from SSL section when password is empty string "" [#10861](https://github.com/gravitee-io/issues/issues/10861)

</details>


 
## Gravitee API Management 4.8.9 - October 10, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Read timeout on v4 returns 500 [#10767](https://github.com/gravitee-io/issues/issues/10767)
* EL request.xmlContent Fails with XML Declaration [#10842](https://github.com/gravitee-io/issues/issues/10842)
* Impossible to increase backend HTTP/2 window sizes [#10852](https://github.com/gravitee-io/issues/issues/10852)

**Management API**

* Image not updated with mAPI [#10809](https://github.com/gravitee-io/issues/issues/10809)
* Error when trying to retrieve the portal notification settings [#10870](https://github.com/gravitee-io/issues/issues/10870)

**Other**

* Two users created with identical email addresses [#10423](https://github.com/gravitee-io/issues/issues/10423)
* Webhook Entrypoint: "No Retry" configuration ignores setting and uses default linear retry. [#10519](https://github.com/gravitee-io/issues/issues/10519)
* Upgrader error on PortalNotificationConfig repository when upgrading from 4.2 to 4.8 [#10847](https://github.com/gravitee-io/issues/issues/10847)
* Custom API keys are truncated to 64 characters when created through the console UI [#10873](https://github.com/gravitee-io/issues/issues/10873)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Character length for API description is only 4000 for Postgres [#10825](https://github.com/gravitee-io/issues/issues/10825)
* File reporter creates empty log files despite event exclusion. [#10853](https://github.com/gravitee-io/issues/issues/10853)

</details>


 
## Gravitee API Management 4.8.8 - September 26, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway rejects client certificates missing BEGIN/END markers in X-Gravitee-Client-Cert header [#10816](https://github.com/gravitee-io/issues/issues/10816)

**Management API**

* Unable to search federated APIs using metadata [#10676](https://github.com/gravitee-io/issues/issues/10676)
* Group edit fails for APIs with missing visibility [#10804](https://github.com/gravitee-io/issues/issues/10804)
* Health-check endpoint target returns type instead of full URL after 4.8 upgrade [#10818](https://github.com/gravitee-io/issues/issues/10818)

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



## Gravitee API Management 4.8.7 - September 12, 2025
<details>

<summary>Bug Fixes</summary>


**Gateway**

* Unable to retrieve secrets from HashiCorp[#10760](https://github.com/gravitee-io/issues/issues/10760)

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

**Other**

* Elastic reporter fails with ES7 and V4 Proxy API[#10772](https://github.com/gravitee-io/issues/issues/10772)
* APIs with MCP enabled require the Accept header to be present in debug requests [#10652](https://github.com/gravitee-io/issues/issues/10652)

</details>

 
## Gravitee API Management 4.8.6 - September 1, 2025
<details>
<summary>Security</summary>

* Harden authorization controls for the automation API [#10771](https://github.com/gravitee-io/issues/issues/10771)
</details>
 
## Gravitee API Management 4.8.5 - August 29, 2025
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

**Other**

* Kafka ACLs not properly refreshed during fetch  [#10735](https://github.com/gravitee-io/issues/issues/10735)
* Kafka ACL - optimize ActionFilter instantiation [#10745](https://github.com/gravitee-io/issues/issues/10745)
* Kafka Gateway - ACL Policy Issue for Virtual Topics [#10754](https://github.com/gravitee-io/issues/issues/10754)

</details>


 
## Gravitee API Management 4.8.4 - August 14, 2025
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
* \[MCP Entrypoint] POST operation through the MCP server gives a 500 / timeout. [#10720](https://github.com/gravitee-io/issues/issues/10720)
* UI Bug: Management Console application logs headers are truncated/squished with long values [#10721](https://github.com/gravitee-io/issues/issues/10721)
* OOM error in gateway when management repository becomes unresponsive causes worker thread starvation and analytics reporter blockage [#10723](https://github.com/gravitee-io/issues/issues/10723)
* A2A Proxy does not support Strands AI SDK  [#10743](https://github.com/gravitee-io/issues/issues/10743)
* Gravitee gateway sending thousands of requests per second [#10732](https://github.com/gravitee-io/issues/issues/10732)


</details>

<details>

<summary>Improvements</summary>

**Other**

* Add generic consumer to PROTOBUF-JSON plugin [#10716](https://github.com/gravitee-io/issues/issues/10716)
* Update oas-validation policy's swagger-request-validator version [#10742](https://github.com/gravitee-io/issues/issues/10742)

</details>


 
## Gravitee API Management 4.8.3 - August 1, 2025
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
* Unable to modify set/replace/append headers in the UI for the Transform Headers policy [#10655](https://github.com/gravitee-io/issues/issues/10655)
* Unable to access Logs details [#10695](https://github.com/gravitee-io/issues/issues/10695)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Disable cleanup events and audits services by default [#10708](https://github.com/gravitee-io/issues/issues/10708)

</details>


 
## Gravitee API Management 4.8.2 - July 18, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Traceparent HTTP header is not available in the policy chain [#10511](https://github.com/gravitee-io/issues/issues/10511)
* Kafka TLS keystore loaded too many times [#10646](https://github.com/gravitee-io/issues/issues/10646)

**Management API**

* Wrong count in the analytics of API v4 [#10604](https://github.com/gravitee-io/issues/issues/10604)
* Entrypoint cannot be found error when using tags [#10667](https://github.com/gravitee-io/issues/issues/10667)

**Console**

* Identity provider roles mapping UI bug [#10503](https://github.com/gravitee-io/issues/issues/10503)
* Instances of calling the groups endpoint on create V2 API page time out when a large number of groups exist [#10603](https://github.com/gravitee-io/issues/issues/10603)

**Other**

* Mock policy is not generated if the openAPI spec data uses a type of string and format of date-time [#10619](https://github.com/gravitee-io/issues/issues/10619)
* \[Kafka Offloading Policy] Large Payloads Support [#10674](https://github.com/gravitee-io/issues/issues/10674)

</details>



## Gravitee API Management 4.8.1 - July 7, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Hardcoded value for health check in 4.7 versions and above in docker images ( for both gateway and mapi ) [#10644](https://github.com/gravitee-io/issues/issues/10644)

**Management API**

* Subscriptions in the subscriptions tab of an application seem to only show the first 10 item [#10529](https://github.com/gravitee-io/issues/issues/10529)
* Users with both group inheritance and individual access to applications are limited in which applications to which they can subscribe [#10601](https://github.com/gravitee-io/issues/issues/10601)
* Hardcoded value for health check in 4.7 versions and above in docker images ( for both gateway and mapi ) [#10644](https://github.com/gravitee-io/issues/issues/10644)
* Debug mode for v4 proxy apis returns a 500 response [#10648](https://github.com/gravitee-io/issues/issues/10648)
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
* Portal Theme Settings : UNABLE to change Theme color [#10647](https://github.com/gravitee-io/issues/issues/10647)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Enable multi-tenant support for Dictionaries by default [#10637](https://github.com/gravitee-io/issues/issues/10637)

**Other**

* Increase character limit of condition field in flow\_selectors table [#10560](https://github.com/gravitee-io/issues/issues/10560)

</details>
