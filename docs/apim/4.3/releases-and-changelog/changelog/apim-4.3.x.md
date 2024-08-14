---
description: >-
  This page contains the changelog entries for APIM 4.3.x and any future patch
  APIM 4.3.x releases
---

# APIM 4.3.x
 
## Gravitee API Management 4.3.11 - August 14, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway issue - Memory Leak [#9924](https://github.com/gravitee-io/issues/issues/9924)
* Memory leak when using rate-limit with non-responsive Redis [#9928](https://github.com/gravitee-io/issues/issues/9928)

**Management API**

* Total APIs for Portal API Category endpoint always returns 0 [#9922](https://github.com/gravitee-io/issues/issues/9922)
* Re: \[APIM/Gateway] Override an email template doesn't work [#9934](https://github.com/gravitee-io/issues/issues/9934)

**Console**

* Application names overflow container under API, Plans and Subscriptions [#9872](https://github.com/gravitee-io/issues/issues/9872)
* UI Doesn't work behind google's Identity-Aware Proxy [#9919](https://github.com/gravitee-io/issues/issues/9919)

</details>


 
## Gravitee API Management 4.3.10 - August 1, 2024
<details>

<summary>Bug Fixes</summary>

**Management API**

* Missing semicolon in Subscriptions Export [#9878](https://github.com/gravitee-io/issues/issues/9878)

**Console**

* Logs Have No Option to Be Opened in New Tab/Window [#9764](https://github.com/gravitee-io/issues/issues/9764)
* Creating a personal token with the same name does not trigger a visual warning [#9873](https://github.com/gravitee-io/issues/issues/9873)

**Other**

* APIM RPM installation overwrite portal configuration [#9914](https://github.com/gravitee-io/issues/issues/9914)

</details>


 
## Gravitee API Management 4.3.8 - July 5, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* 500 Internal server error when logs enabled [#9719](https://github.com/gravitee-io/issues/issues/9719)
* Enabled Logging with condition does not work properly [#9756](https://github.com/gravitee-io/issues/issues/9756)
* Transfer subscription does not use new plan when V4 emulation is disabled [#9772](https://github.com/gravitee-io/issues/issues/9772)
* Upgrade to gio 4.4.0 corrupts API Keys [#9834](https://github.com/gravitee-io/issues/issues/9834)
* Add Base64 class in Expression Language whitelist [#9850](https://github.com/gravitee-io/issues/issues/9850)

**Management API**

* Override an email template with multiple REST API [#9445](https://github.com/gravitee-io/issues/issues/9445)
* Cannot Create Local User (no email to set password) [#9680](https://github.com/gravitee-io/issues/issues/9680)
* Error in Gravitee OpenAPI spec [#9711](https://github.com/gravitee-io/issues/issues/9711)
* Endpoint's target url can be saved with a space or tab [#9791](https://github.com/gravitee-io/issues/issues/9791)
* Unable delete existing PAT tokens [#9801](https://github.com/gravitee-io/issues/issues/9801)
* Error on platform analytics and logs screens when too many applications and/or APIs [#9823](https://github.com/gravitee-io/issues/issues/9823)

**Console**

* Correct API properties Expression Language for v4 APIs [#9694](https://github.com/gravitee-io/issues/issues/9694)
* Deploy button got non clickable when we go out of focus  [#9705](https://github.com/gravitee-io/issues/issues/9705)
* When updating a service account email through API, no mail validation is performed [#9709](https://github.com/gravitee-io/issues/issues/9709)
* Enabled Logging with condition does not work properly [#9756](https://github.com/gravitee-io/issues/issues/9756)
* Cannot subscribe to API plans via the web [#9758](https://github.com/gravitee-io/issues/issues/9758)
* Unable to update application name in console. [#9770](https://github.com/gravitee-io/issues/issues/9770)
* Cannot Save Dashboard Updates in UI [#9771](https://github.com/gravitee-io/issues/issues/9771)
* Unable to Add Members to Group During Group Creation [#9783](https://github.com/gravitee-io/issues/issues/9783)
* Endpoint's target url can be saved with a space or tab [#9791](https://github.com/gravitee-io/issues/issues/9791)
* In some cases it is difficult to view the configuration in the history menu. [#9800](https://github.com/gravitee-io/issues/issues/9800)
* Policy - losing focus when opening documentation [#9802](https://github.com/gravitee-io/issues/issues/9802)
* Dashboard widget not working  [#9820](https://github.com/gravitee-io/issues/issues/9820)
* Client Id not saved between Security section and subscriptions during application creation [#9828](https://github.com/gravitee-io/issues/issues/9828)
* JSON to XML policy does not work with default configuration for V4 proxy APIs [#9833](https://github.com/gravitee-io/issues/issues/9833)

**Other**

* \[gravitee-policy-ipfiltering] CIDR block /32 (single IP) not working in the IP Filtering Policy [#9602](https://github.com/gravitee-io/issues/issues/9602)
* \[gravitee-resource-oauth2-provider-keycloak] Update of 'gravitee-resource-oauth2-provider-keycloak' Plugin [#9628](https://github.com/gravitee-io/issues/issues/9628)
* \[gravitee-policy-jwt] 500 error on jwt plan with GATEWAY_KEYS when using  "Emulate v4 engine" [#9693](https://github.com/gravitee-io/issues/issues/9693)
* \[MongoDb] Upgraders should use prefix for collection names [#9807](https://github.com/gravitee-io/issues/issues/9807)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* PrimaryOwner not given in list of APIs [#9678](https://github.com/gravitee-io/issues/issues/9678)
* The name of API/Application/Plan is not given in list of API's subscriptions [#9679](https://github.com/gravitee-io/issues/issues/9679)
* Improve API synchronization state computation [#9852](https://github.com/gravitee-io/issues/issues/9852)

**Other**

* \[gravitee-policy-aws-lambda] Allow to dynamically configure AWS policy credentials [#9444](https://github.com/gravitee-io/issues/issues/9444)

</details>


 
## Gravitee API Management 4.3.7 - June 19, 2024
<details>

<summary>Bug Fixes</summary>

**Console**

* Allow users to configure keepalive timeout in the console for V2 APIs [#9651](https://github.com/gravitee-io/issues/issues/9651)
* Application analytics view logs navigation with filters [#9762](https://github.com/gravitee-io/issues/issues/9762)
* Transfer ownership to group shows as option for applications [#9774](https://github.com/gravitee-io/issues/issues/9774)
* Endpoint configuration enable proxy setup just after creation of endpoint [#9780](https://github.com/gravitee-io/issues/issues/9780)
* Clicking on existing Doc/Page shows an empty screen [#9781](https://github.com/gravitee-io/issues/issues/9781)
* Filter on 208 status code not available [#9784](https://github.com/gravitee-io/issues/issues/9784)
* IDP Logout does not contain the correct subpath for console. [#9786](https://github.com/gravitee-io/issues/issues/9786)
* Display issues in token generation modal [#9793](https://github.com/gravitee-io/issues/issues/9793)

**Portal**

* Current portal incorrectly handles case where API description is "null" [#9785](https://github.com/gravitee-io/issues/issues/9785)
* Documentation too slow [#9788](https://github.com/gravitee-io/issues/issues/9788)

**Helm Charts**

* Improve the ingress configuration to redirect HTTPS [#9710](https://github.com/gravitee-io/issues/issues/9710)

**Other**

* \[gravitee-endpoint-kafka] Kafka sender options customization not taken into account [#9656](https://github.com/gravitee-io/issues/issues/9656)
* \[gravitee-policy-json-validation] v4 Policy Studio UI doesn't support multi-line values [#9799](https://github.com/gravitee-io/issues/issues/9799)

</details>

<details>

<summary>Improvements</summary>

**Other**

* \[gravitee-entrypoint-webhook] Support 500 responses for DLQ : add client_id and errors stack in the message sent to DLQ [#9740](https://github.com/gravitee-io/issues/issues/9740)
* \[gravitee-endpoint-kafka] Add a option on kafka endpoint to remove Confluent Wire format header [#9795](https://github.com/gravitee-io/issues/issues/9795)

</details>


 
## Gravitee API Management 4.3.6 - June 7, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Error in the gateway when upgrading connection from http1.1 to http2 [#9757](https://github.com/gravitee-io/issues/issues/9757)
* Socket.io disconnect/reconnect latency [#9766](https://github.com/gravitee-io/issues/issues/9766)

**Management API**

* Pushing an API with API Designer fails [#9761](https://github.com/gravitee-io/issues/issues/9761)
* Gitlab fetcher CronSequenceGenerator deprecation [#9733](https://github.com/gravitee-io/issues/issues/9733)
* Inheritance of a V2 API endpoint configuration is not set when importing an OpenAPI spec [#9775](https://github.com/gravitee-io/issues/issues/9775)

**Console**

* Documentation not appearing for 4.3.2 / 4.3.3 Policies (on the RHS) [#9760](https://github.com/gravitee-io/issues/issues/9760)
* Login via OIDC on Management Console not possible [#9769](https://github.com/gravitee-io/issues/issues/9769)

</details>

<details>

<summary>Improvements</summary>

**Other**

* \[gravitee-policy-groovy] Have access to the binary value of a message content [#9767](https://github.com/gravitee-io/issues/issues/9767)

</details>



## Gravitee API Management 4.3.5 - May 24, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Gateway monitoring page has no data [#9677](https://github.com/gravitee-io/issues/issues/9677)
* The Assign Content policy seems to be broken when using with Retry policy [#9737](https://github.com/gravitee-io/issues/issues/9737)

**Management API**

* Logs mismatched between environments [#9599](https://github.com/gravitee-io/issues/issues/9599)
* Incompatible QoS between entrypoints and endpoints [#9608](https://github.com/gravitee-io/issues/issues/9608)
* Unable to Search Users by Company Name and Country in Users API [#9702](https://github.com/gravitee-io/issues/issues/9702)

**Console**

* Incompatible QoS between entrypoints and endpoints [#9608](https://github.com/gravitee-io/issues/issues/9608)
* OpenAPI component references are not read correctly when uploading the Swagger document [#9738](https://github.com/gravitee-io/issues/issues/9738)
* Dashboard Overview Widgets Loading Too Long [#9747](https://github.com/gravitee-io/issues/issues/9747)

**Portal**

* OpenAPI component references are not read correctly when uploading the Swagger document [#9738](https://github.com/gravitee-io/issues/issues/9738)

</details>

## Gravitee API Management 4.3.4 - May 10, 2024

<details>

<summary>Bug fixes</summary>

**Management API**

* Portal global API search is returning a 500 "maxClauseCount is set to 1024" [#9730](https://github.com/gravitee-io/issues/issues/9730)

**Other**

* \[gravitee-policy-ratelimit] Thread Blocked on AsyncRateLimitRepository [#9717](https://github.com/gravitee-io/issues/issues/9717)

</details>

<details>

<summary>Improvements</summary>

**Helm Charts**

* Enhance the experience of deploying Gateway with Redis SSL using Helm Chart [#9726](https://github.com/gravitee-io/issues/issues/9726)

**Other**

* \[gravitee-entrypoint-webhook] Support 500 responses for DLQ [#9722](https://github.com/gravitee-io/issues/issues/9722)

</details>

## Gravitee API Management 4.3.3 - April 26, 2024

<details>

<summary>Bug fixes</summary>

**Management API**

* Error in OpenApi spec [#9665](https://github.com/gravitee-io/issues/issues/9665)
* Unable to update the service account email through API [#9682](https://github.com/gravitee-io/issues/issues/9682)
* Debug Mode Unavailable [#9684](https://github.com/gravitee-io/issues/issues/9684)

**Console**

* Cannot create Backend-to-Backend Application from UI Console [#9636](https://github.com/gravitee-io/issues/issues/9636)
* Dashboard page is not refreshing automatically when swapping environments [#9639](https://github.com/gravitee-io/issues/issues/9639)

**Other**

* \[gravitee-policy-cache] Cache Policy Always Caches the First Response [#9534](https://github.com/gravitee-io/issues/issues/9534)
* \[gravitee-policy-cache] Cache Policy Does Not Correctly Return Images [#9585](https://github.com/gravitee-io/issues/issues/9585)
* \[gravitee-policy-cache] Time to live setting not working [#9692](https://github.com/gravitee-io/issues/issues/9692)

</details>

## Gravitee API Management 4.3.2 - April 11, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Secret Provider Setup [#9586](https://github.com/gravitee-io/issues/issues/9586)
* 431 (Request Header Fields Too Large) when submitting large JWT to gRPC API [#9652](https://github.com/gravitee-io/issues/issues/9652)

**Management API**

* Installation collection can have more than one entry [#9641](https://github.com/gravitee-io/issues/issues/9641)

**Console**

* Cannot navigate to the next or previous logs [#9637](https://github.com/gravitee-io/issues/issues/9637)
* Unable to load API Management UI in Browser [#9644](https://github.com/gravitee-io/issues/issues/9644)
* Performance issue with the analytics dashboard [#9658](https://github.com/gravitee-io/issues/issues/9658)
* Redirection to a particular API is not working in 4.3 [#9666](https://github.com/gravitee-io/issues/issues/9666)

**Portal**

* Cannot Scroll in Markdown Documents [#9634](https://github.com/gravitee-io/issues/issues/9634)
* Showing Gravitee.io in Dev Portal browser tab only while the page loads [#9663](https://github.com/gravitee-io/issues/issues/9663)

**Other**

* Fail to enable the service on SUSE [#9501](https://github.com/gravitee-io/issues/issues/9501)
* Upgrade 3.20.22 to 4.2.2 - File report missing node metrics [#9589](https://github.com/gravitee-io/issues/issues/9589)
* \[gravitee-policy-cache] Concurrency issue with v4 emulation engine [#9635](https://github.com/gravitee-io/issues/issues/9635)
* \[gravitee-resource-auth-provider-http] Timeout when body parsing is failing [#9640](https://github.com/gravitee-io/issues/issues/9640)
* API List showing type as "Undefined" for v4 APIs in Postgres env [#9643](https://github.com/gravitee-io/issues/issues/9643)
* Authentication Provider table column too small [#9664](https://github.com/gravitee-io/issues/issues/9664)

</details>

## Gravitee API Management 4.3.1 - April 2, 2024

<details>

<summary>Bug fixes</summary>

**Other**

* Organization licenses are not working when using bridge architecture [#9638](https://github.com/gravitee-io/issues/issues/9638)

</details>
