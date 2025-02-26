---
description: >-
  This page contains the changelog entries for APIM 4.5.x and any future patch
  APIM 4.5.x releases
---

# APIM 4.5.x
 
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

* Custom Api key is not resuable between multiple environments [#10131](https://github.com/gravitee-io/issues/issues/10131)
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
