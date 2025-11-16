---
description: >-
  This page contains the changelog entries for APIM 4.0.x and any future patch
  APIM 4.0.x releases
---

# APIM 4.0.x
 
## Gravitee API Management 4.0.29 - July 19, 2024
<details>

<summary>Bug Fixes</summary>

**Management API**

* JDBC Connection Pool Management Error - follow up ticket [#9851](https://github.com/gravitee-io/issues/issues/9851)

**Console**

* Non idempotent operation when creating APIs/Appplications/Users [#9688](https://github.com/gravitee-io/issues/issues/9688)

</details>

<details>

<summary>Improvements</summary>

**Console**

* Paginated audit events loading to avoid memory issues [#9768](https://github.com/gravitee-io/issues/issues/9768)

</details>


 
## Gravitee API Management 4.0.28 - July 5, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* 500 Internal server error when logs enabled [#9719](https://github.com/gravitee-io/issues/issues/9719)
* Enabled Logging with condition does not work properly [#9756](https://github.com/gravitee-io/issues/issues/9756)
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
* When updating a service account email through API, no mail validation is performed [#9709](https://github.com/gravitee-io/issues/issues/9709)
* Unable to Add or Remove Context Path Segments for a v4 API [#9716](https://github.com/gravitee-io/issues/issues/9716)
* Enabled Logging with condition does not work properly [#9756](https://github.com/gravitee-io/issues/issues/9756)
* Cannot subscribe to API plans via the web [#9758](https://github.com/gravitee-io/issues/issues/9758)
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


 
## Gravitee API Management 4.0.27 - June 19, 2024
<details>

<summary>Bug Fixes</summary>

**Console**

* Filter on 208 status code not available [#9784](https://github.com/gravitee-io/issues/issues/9784)

**Portal**

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

* \[gravitee-endpoint-kafka] Add a option on kafka endpoint to remove Confluent Wire format header [#9795](https://github.com/gravitee-io/issues/issues/9795)

</details>


 
## Gravitee API Management 4.0.26 - June 7, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Error in the gateway when upgrading connection from http1.1 to http2 [#9757](https://github.com/gravitee-io/issues/issues/9757)
* Socket.io disconnect/reconnect latency [#9766](https://github.com/gravitee-io/issues/issues/9766)

**Management API**

* Gitlab fetcher CronSequenceGenerator deprecation [#9733](https://github.com/gravitee-io/issues/issues/9733)
* Inheritance of a V2 API endpoint configuration is not set when importing an OpenAPI spec [#9775](https://github.com/gravitee-io/issues/issues/9775)

</details>

<details>

<summary>Improvements</summary>

**Other**

* \[gravitee-policy-groovy] Have access to the binary value of a message content [#9767](https://github.com/gravitee-io/issues/issues/9767)

</details>



## Gravitee API Management 4.0.25 - May 24, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Gateway monitoring page has no data [#9677](https://github.com/gravitee-io/issues/issues/9677)
* The Assign Content policy seems to be broken when using with Retry policy [#9737](https://github.com/gravitee-io/issues/issues/9737)

**Management API**

* Logs mismatched between environments [#9599](https://github.com/gravitee-io/issues/issues/9599)
* Unable to Search Users by Company Name and Country in Users API [#9702](https://github.com/gravitee-io/issues/issues/9702)

</details>

## Gravitee API Management 4.0.24 - May 10, 2024

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

</details>

## Gravitee API Management 4.0.23 - April 26, 2024

<details>

<summary>Bug fixes</summary>

**Management API**

* Error in OpenApi spec [#9665](https://github.com/gravitee-io/issues/issues/9665)
* Unable to update the service account email through API [#9682](https://github.com/gravitee-io/issues/issues/9682)

**Console**

* Cannot create Backend-to-Backend Application from UI Console [#9636](https://github.com/gravitee-io/issues/issues/9636)

**Portal**

* Problem of swagger interpretation with redocly [#9673](https://github.com/gravitee-io/issues/issues/9673)

**Other**

* \[gravitee-policy-cache] Cache Policy Always Caches the First Response [#9534](https://github.com/gravitee-io/issues/issues/9534)
* \[gravitee-policy-cache] Cache Policy Does Not Correctly Return Images [#9585](https://github.com/gravitee-io/issues/issues/9585)
* \[gravitee-policy-cache] Time to live setting not working [#9692](https://github.com/gravitee-io/issues/issues/9692)

</details>

## Gravitee API Management 4.0.22 - April 11, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Secret Provider Setup [#9586](https://github.com/gravitee-io/issues/issues/9586)
* 431 (Request Header Fields Too Large) when submitting large JWT to gRPC API [#9652](https://github.com/gravitee-io/issues/issues/9652)

**Console**

* Performance issue with the analytics dashboard [#9658](https://github.com/gravitee-io/issues/issues/9658)

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

## Gravitee API Management 4.0.21 - March 29, 2024

<details>

<summary>Bug fixes</summary>

**Management API**

* Update import remove all members when a group is defined as a PO [#9596](https://github.com/gravitee-io/issues/issues/9596)
* Gravitee 4.2 OpenAPI issues [#9632](https://github.com/gravitee-io/issues/issues/9632)

**Other**

* \[gravitee-policy-ipfiltering] DNS Lookup fails with some DNS servers [#9592](https://github.com/gravitee-io/issues/issues/9592)
* \[gravitee-resource-auth-provider-http] Timeout when authentication condition is failing [#9611](https://github.com/gravitee-io/issues/issues/9611)
* Liquibase changelog 4.0.20-dashboards adding NOT NULL column without default value [#9626](https://github.com/gravitee-io/issues/issues/9626)
* APIM DashboardTypeUpgrader raises an error when used with DocumentDB [#9631](https://github.com/gravitee-io/issues/issues/9631)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Allow to configure KeepAliveTimeout for HTTP endpoint [#9541](https://github.com/gravitee-io/issues/issues/9541)

</details>

## Gravitee API Management 4.0.20 - March 21, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Improve HealthCheck service for v2 APIs [#9543](https://github.com/gravitee-io/issues/issues/9543)

**Management API**

* Condition field in JDBC dbs is too short [#9595](https://github.com/gravitee-io/issues/issues/9595)

**Console**

* \[shared API key] API key mode not displayed on application screen [#9612](https://github.com/gravitee-io/issues/issues/9612)

**Other**

* API v4 proxy - problem with client SSL certificate

</details>

<details>

<summary>Improvements</summary>

**Portal**

* Do not allow user to change their email through the Portal [#9617](https://github.com/gravitee-io/issues/issues/9617)

</details>

## Gravitee API Management 4.0.19 - March 1, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Override HTTP Method [#9526](https://github.com/gravitee-io/issues/issues/9526)

**Management API**

* Shared API Key Does Not Always Bind to Subscriptions When Concurrent Requests Are Made [#9502](https://github.com/gravitee-io/issues/issues/9502)
* NullPointer Exception when importing an API with group as PO and members [#9507](https://github.com/gravitee-io/issues/issues/9507)
* APIM: Creating application with "@" in name automatically converts it to "@" [#9514](https://github.com/gravitee-io/issues/issues/9514)
* API description required with POST /apis/ on mAPI v2 [#9527](https://github.com/gravitee-io/issues/issues/9527)
* Importing an API with a group as PO but no PO user in this group should not be possible [#9587](https://github.com/gravitee-io/issues/issues/9587)

**Console**

* No longer possible to compare "published" and "to deploy" status [#9491](https://github.com/gravitee-io/issues/issues/9491)
* Re: Error when clicking on top failed API in platform dashboard [#9498](https://github.com/gravitee-io/issues/issues/9498)
* Remove last user in group shows error [#9517](https://github.com/gravitee-io/issues/issues/9517)

**Portal**

* Documentation menu hidden [#9590](https://github.com/gravitee-io/issues/issues/9590)

</details>

## Gravitee API Management 4.0.18 - February 16, 2024

<details>

<summary>Bug fixes</summary>

**Management API**

* Excluded groups on plan are not displayed after being imported or promoted to a new environment [#9116](https://github.com/gravitee-io/issues/issues/9116)
* Private APIs on the Portal are wrongly displayed [#9513](https://github.com/gravitee-io/issues/issues/9513)
* Modifying API definition causes loss of endpoint configuration [#9520](https://github.com/gravitee-io/issues/issues/9520)

**Console**

* When validating a JWT subscription, I'm asked to customize an APIkey [#9489](https://github.com/gravitee-io/issues/issues/9489)

**Portal**

* Documentation gets encoded after deployment [#9490](https://github.com/gravitee-io/issues/issues/9490)
* Customization problems in the Developer Portal [#9495](https://github.com/gravitee-io/issues/issues/9495)
* Subscriptions Not Visible in Portal If There Is a Push Plan [#9511](https://github.com/gravitee-io/issues/issues/9511)

**Other**

* "Propagate client Accept-Encoding header" option missing in V4 [#9475](https://github.com/gravitee-io/issues/issues/9475)

</details>

## Gravitee API Management 4.0.17 - February 2, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Unable to populate attributes using the Assign Attributes policy due to enabled v4 Engine [#9420](https://github.com/gravitee-io/issues/issues/9420)
* Conditional logging [#9486](https://github.com/gravitee-io/issues/issues/9486)
* Timeout when connecting to WebSocket API using header Connection:Upgrade,Keep-Alive [#9487](https://github.com/gravitee-io/issues/issues/9487)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Add API ID in healthcheck logs [#9493](https://github.com/gravitee-io/issues/issues/9493)

</details>

## Gravitee API Management 4.0.16 - January 19, 2024

<details>

<summary>Bug fixes</summary>

**Gateway**

* Sometimes path-mapping is not working [#9450](https://github.com/gravitee-io/issues/issues/9450)
* Management API does not encode a value in the URL used in a pipe [#9461](https://github.com/gravitee-io/issues/issues/9461)
* gRPC backend received unexpected headers [#9463](https://github.com/gravitee-io/issues/issues/9463)

**Management API**

* Unable to switch to gRPC endpoint type from the Console UI [#9456](https://github.com/gravitee-io/issues/issues/9456)
* Updating an API reset the gRPC type of the endpoint [#9464](https://github.com/gravitee-io/issues/issues/9464)
* Can't create 2 virtualhosts having the same path but different host [#9466](https://github.com/gravitee-io/issues/issues/9466)

**Console**

* Can't create 2 virtualhosts having the same path but different host [#9466](https://github.com/gravitee-io/issues/issues/9466)
* Navigation in a multi-environments console is messed up [#9467](https://github.com/gravitee-io/issues/issues/9467)

**Portal**

* Docs not loaded instantly [#9452](https://github.com/gravitee-io/issues/issues/9452)

**Helm Charts**

* Backward incompatibility during Helm upgrade with old `values.yml` [#9446](https://github.com/gravitee-io/issues/issues/9446)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Access request host property in Expression Language [#9453](https://github.com/gravitee-io/issues/issues/9453)

</details>

## Gravitee API Management 4.0.15 - December 21, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Healthcheck service never stopped when using Service Discovery [#9437](https://github.com/gravitee-io/issues/issues/9437)

**Management API**

* API Does Not Deploy if a Common Flow Exists with Multiple Entrypoints Selected [#9415](https://github.com/gravitee-io/issues/issues/9415)
* Cannot delete API with too many events [#9439](https://github.com/gravitee-io/issues/issues/9439)

**Console**

* Inconsistency on "Inheritance" flag for endpoints/groups between frontend and backend [#9407](https://github.com/gravitee-io/issues/issues/9407)
* Flow Name Display Does Not Match Gateway Behavior [#9416](https://github.com/gravitee-io/issues/issues/9416)
* Log view too wide [#9429](https://github.com/gravitee-io/issues/issues/9429)

**Portal**

* Tickets Inaccessible When an API with Open Tickets Is Deleted [#9422](https://github.com/gravitee-io/issues/issues/9422)
* Cannot Scroll in Markdown Documentation in Portal [#9424](https://github.com/gravitee-io/issues/issues/9424)
* Synchronization inconsistency on ALL APIs page on Portal [#9432](https://github.com/gravitee-io/issues/issues/9432)
* Sign up doesn't work anymore [#9440](https://github.com/gravitee-io/issues/issues/9440)

**Other**

* Make some non-migrated policies available on REQUEST phase for message APIs [#9430](https://github.com/gravitee-io/issues/issues/9430)

</details>

<details>

<summary>Improvements</summary>

**Other**

* \[JDBC] Improve Flows loading [#9436](https://github.com/gravitee-io/issues/issues/9436)

</details>

## Gravitee API Management 4.0.14 - December 7, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* EL: Request's local address is evaluated in place of remote address [#9408](https://github.com/gravitee-io/issues/issues/9408)

**Management API**

* Can't stop a deprecated API [#9406](https://github.com/gravitee-io/issues/issues/9406)

**Console**

* Deploy banner not displayed when updating details of a plan [#9380](https://github.com/gravitee-io/issues/issues/9380)
* Error in Swagger documentation both in Portal and Console [#9391](https://github.com/gravitee-io/issues/issues/9391)
* Bad management of required file in OpenAPI [#9414](https://github.com/gravitee-io/issues/issues/9414)

**Portal**

* Error in Swagger documentation both in Portal and Console [#9391](https://github.com/gravitee-io/issues/issues/9391)

**Helm Charts**

* Alert Engine: System mail notification [#9402](https://github.com/gravitee-io/issues/issues/9402)
* License deleted after Helm upgrade [#9411](https://github.com/gravitee-io/issues/issues/9411)

**Other**

* Transform Query Parameters policy [#9383](https://github.com/gravitee-io/issues/issues/9383)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Add a resource in management API v1 to fetch API subscribers with pagination info [#9410](https://github.com/gravitee-io/issues/issues/9410)

**Portal**

* Update chore dependencies of Gravitee Portal [#9418](https://github.com/gravitee-io/issues/issues/9418)

</details>

## Gravitee API Management 4.0.13 - November 24, 2023

<details>

<summary>Bug fixes</summary>

**Management API**

* Application `api_key_mode` is automatically and incorrectly set to EXCLUSIVE mode without owner consent [#9348](https://github.com/gravitee-io/issues/issues/9348)
* Environment rights: API "update" right is not enough to edit the entrypoint [#9372](https://github.com/gravitee-io/issues/issues/9372)
* APIM: Flows table / name column / extend column size [#9377](https://github.com/gravitee-io/issues/issues/9377)
* Cannot Import API Definition with Automatic Group Association [#9385](https://github.com/gravitee-io/issues/issues/9385)

**Console**

* API subscription fails with insufficient rights error [#9341](https://github.com/gravitee-io/issues/issues/9341)
* History not available if too many deployments [#9359](https://github.com/gravitee-io/issues/issues/9359)
* APIM Console doc links point to old documentation site [#9386](https://github.com/gravitee-io/issues/issues/9386)

**Portal**

* API subscription fails with insufficient rights error [#9341](https://github.com/gravitee-io/issues/issues/9341)
* The "All rights reserved" mention on Portal is using an old date [#9384](https://github.com/gravitee-io/issues/issues/9384)

**Other**

* Configuration files are being overwritten during Yum update [#9368](https://github.com/gravitee-io/issues/issues/9368)
* Transform Headers policy should be case insensitive [#9378](https://github.com/gravitee-io/issues/issues/9378)
* Generate JWT policy Key Resolver wrong value [#9389](https://github.com/gravitee-io/issues/issues/9389)
* OAuth2 introspection and userinfo should send a 503 when technical exception instead of 401 [#9390](https://github.com/gravitee-io/issues/issues/9390)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Health Check: Allow to use response time in assertion [#9388](https://github.com/gravitee-io/issues/issues/9388)

**Helm Charts**

* Allow to configure Gateway timeouts in the Helm Chart [#9392](https://github.com/gravitee-io/issues/issues/9392)

</details>

## Gravitee API Management 4.0.12 - November 10, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Gateways not able to send bulk index data to ES8 [#9361](https://github.com/gravitee-io/issues/issues/9361)
* When using push plan there is no log when subscription webhook ends in error [#9363](https://github.com/gravitee-io/issues/issues/9363)

**Management API**

* Email related to closed, paused and resumed subscription of API\_KEY plan are sent with an empty body [#9355](https://github.com/gravitee-io/issues/issues/9355)
* JDBC deadlocks on Command table when running multiple Management API [#9356](https://github.com/gravitee-io/issues/issues/9356)
* Error running graviteeio-apim-rest-api-4.1.2 [#9360](https://github.com/gravitee-io/issues/issues/9360)
* Unable to access Alerts screen when there are millions of AlertEvents [#9362](https://github.com/gravitee-io/issues/issues/9362)
* Unable to deploy an API with huge API definition and already a lot of deployments [#9364](https://github.com/gravitee-io/issues/issues/9364)
* Security - Enforce password policy for users [#9374](https://github.com/gravitee-io/issues/issues/9374)

**Other**

* GKO - API state does not get updated [#9338](https://github.com/gravitee-io/issues/issues/9338)
* \[RabbitMQ] message not logged when Rabbit's message does not defined correlationId [#9353](https://github.com/gravitee-io/issues/issues/9353)
* Groovy policy with On-request script not working in v4 engine emulation mode [#9367](https://github.com/gravitee-io/issues/issues/9367)
* Generate JWT not working with APIM 4.x [#9371](https://github.com/gravitee-io/issues/issues/9371)
* Missing “generate JWT policy” on a v4 message API entrypoint Request phase [#9373](https://github.com/gravitee-io/issues/issues/9373)

</details>

## Gravitee API Management 4.0.11 - October 27, 2023

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

## Gravitee API Management 4.0.10 - October 13, 2023

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

**Other**

* User claim in OAuth2 resource is ignored [#9168](https://github.com/gravitee-io/issues/issues/9168)
* Typo in the documentation of `cache-policy` [#9262](https://github.com/gravitee-io/issues/issues/9262)

</details>

## Gravitee API Management 4.0.9 - September 28, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* 401 Error with OAuth2 plan after API synchronization [#9251](https://github.com/gravitee-io/issues/issues/9251)
* Metrics for long running connection reported only once closed [#9259](https://github.com/gravitee-io/issues/issues/9259)
* Metrics timers for message API request are not set [#9263](https://github.com/gravitee-io/issues/issues/9263)

**Console**

* Deprecated API is displayed as Published on Dashboard (CE only), Published appears twice [#9249](https://github.com/gravitee-io/issues/issues/9249)
* API Status shows a default API picture icon instead of the configured one [#9250](https://github.com/gravitee-io/issues/issues/9250)
* DCR Provider Does Not Appear in UI [#9257](https://github.com/gravitee-io/issues/issues/9257)

**Other**

* Mock Policy - Example value is not correct when the GET method returns an array [#6289](https://github.com/gravitee-io/issues/issues/6289)
* \[MQTT5.x] Improve security choice [#9173](https://github.com/gravitee-io/issues/issues/9173)
* No flow in Design API [#9242](https://github.com/gravitee-io/issues/issues/9242)
* Remove SMTP default example configuration in Helm [#9243](https://github.com/gravitee-io/issues/issues/9243)
* Allow ingress wildcard in Helm chart [#9246](https://github.com/gravitee-io/issues/issues/9246)
* Getting 400 bad requests and random timeouts APIM version 3.20.14 [#9266](https://github.com/gravitee-io/issues/issues/9266)

</details>

## Gravitee API Management 4.0.8 - September 14, 2023

<details>

<summary>Bug fixes</summary>

**Management API**

* Path with ":\*" in path mappings is breaking down the environment [#9214](https://github.com/gravitee-io/issues/issues/9214)
* Upgrade Guava to `32.1.2-jre` [#9223](https://github.com/gravitee-io/issues/issues/9223)
* Add support for MTLS certificate-bound tokens verification in the JWT policy

</details>

## Gravitee API Management 4.0.7 - September 11, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Do not consider semicolon as query param separator [#9131](https://github.com/gravitee-io/issues/issues/9131)
* Gateway defaults to v3 execution mode while APIM defaults to v4 [#9217](https://github.com/gravitee-io/issues/issues/9217)
* APIs with `null` sharding tags shouldn't be deployed on Gateway with tags [#9219](https://github.com/gravitee-io/issues/issues/9219)

**Console**

* Restarting UI container leads to HTTP 301 [#9186](https://github.com/gravitee-io/issues/issues/9186)

</details>

## Gravitee API Management 4.0.6 - August 31, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Override Kafka topic using attribute isn't possible at the moment [#9201](https://github.com/gravitee-io/issues/issues/9201)

**Management API**

* Webhook Notifier has hardcoded 200 value for status code and will not accept other 20x codes [#9096](https://github.com/gravitee-io/issues/issues/9096)

**Console**

* Service Discovery configuration isn't taken in account [#9152](https://github.com/gravitee-io/issues/issues/9152)
* Fix permissions for new ng routes [#9164](https://github.com/gravitee-io/issues/issues/9164)

</details>

## Gravitee API Management 4.0.5 - August 28, 2023

<details>

<summary>Bug fixes</summary>

**Management API**

* Primary owner can remove himself from application with Management API [#9171](https://github.com/gravitee-io/issues/issues/9171)
* v4 API analytics sampling not mapped on get or export [#9203](https://github.com/gravitee-io/issues/issues/9203)

**Console**

* A right-click on an item link in the side navigation menu does not allow "open in a new tab" [#9146](https://github.com/gravitee-io/issues/issues/9146)
* 503 errors when tenants are specified [#9176](https://github.com/gravitee-io/issues/issues/9176)
* Redeploy banner not shown when new plan published [#9200](https://github.com/gravitee-io/issues/issues/9200)

**Other**

* ElasticSearch configuration for keystore certs and keys not mapped correctly [#9208](https://github.com/gravitee-io/issues/issues/9208)

</details>

## Gravitee API Management 4.0.4 - August 18, 2023

<details>

<summary>Bug fixes</summary>

**Management API**

* "Export as CSV" on Subscriptions only exports displayed values [#8965](https://github.com/gravitee-io/issues/issues/8965)
* Membership duplication ignores Primary Owner of source API and can create a duplicated membership in the new API [#9184](https://github.com/gravitee-io/issues/issues/9184)
* Page duplication does not update lastContributor attribute [#9185](https://github.com/gravitee-io/issues/issues/9185)

**Console**

* Console Analytics & Logs: 500 error is displayed when trying to view analytics and logs using a date range greater than 90 days [#6777](https://github.com/gravitee-io/issues/issues/6777)
* Health Check Active When Configured Globally but Not Enabled on the Endpoint [#9149](https://github.com/gravitee-io/issues/issues/9149)

**Other**

* Improve permission granulation for environment settings [#9150](https://github.com/gravitee-io/issues/issues/9150)

</details>

## Gravitee API Management 4.0.3 - August 10, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Snappy dependency error when calling Kafka API [#9181](https://github.com/gravitee-io/issues/issues/9181)

**Management API**

* Improve MongoDB indices [#9162](https://github.com/gravitee-io/issues/issues/9162)
* Improve v4 API import [#9163](https://github.com/gravitee-io/issues/issues/9163)
* DB upgrade fails on JDBC repositories 3.20.x to 4.x [#9182](https://github.com/gravitee-io/issues/issues/9182)

**Console**

* After creation of a plan, user should be redirected to the staging view [#9166](https://github.com/gravitee-io/issues/issues/9166)
* Subscription creation is not possible for APIs created with the Kubernetes Operator [#9175](https://github.com/gravitee-io/issues/issues/9175)

</details>

## Gravitee API Management 4.0.2 - August 4, 2023

<details>

<summary>Bug fixes</summary>

**Portal**

* Logout issue on portal [#9156](https://github.com/gravitee-io/issues/issues/9156)

**Other**

* API promotion fails if sharding tags applied on API [#9121](https://github.com/gravitee-io/issues/issues/9121)

</details>

## Gravitee API Management 4.0.1 - August 4, 2023

<details>

<summary>Bug fixes</summary>

**Gateway**

* Log exception parameter of execution failure [#9148](https://github.com/gravitee-io/issues/issues/9148)

**Management API**

* Dashboard for analytics is shown for all environments [#9058](https://github.com/gravitee-io/issues/issues/9058)
* First API export causes API desynchronization [#9059](https://github.com/gravitee-io/issues/issues/9059)
* Creating a plan on a v2 API leads to null values in the description [#9153](https://github.com/gravitee-io/issues/issues/9153)

</details>

## Gravitee API Management 4.0.0 - July 20, 2023

For more in-depth information on what's new, please refer to the [Gravitee APIM 4.0 release notes](../release-notes/apim-4.0.md).

<details>

<summary>What's new</summary>

**API Management Console**

* API List support for v4 APIs
* New API General page for for v4 APIs
* New support for configuring v4 APIs:
  * Dynamic Entrypoint configuration
  * Dynamic Endpoint configuration
  * Plan configuration
  * Subscription configuration

**API Creation Wizard**

* New API creation wizard that supports the Gravitee v4 API definition.
* v4 API Creation wizard support for the following Endpoints:
  * Kafka
  * MQTT
  * RabbitMQ (if using AMQP 0-9-1 protocol)
  * Mock
* v4 API Creation wizard support for the following Entrypoints:
  * WebSocket
  * Webhooks
  * Server-sent Events (SSE)
  * HTTP GET
  * HTTP POST
* Support for Gravitee protocol mediation in the new v4 API Creation Wizard
* New RabbitMQ endpoint

**Policy Design and Enforcement**

* New Policy Studio that supports v4 APIs
* v4 Policy Studio support for message-level policies
* v4 Policy Studio support for policy enforcement on publish and subscribe phases for pub/sub communication
* Made existing Gravitee policies enforceable for v4 APIs:
  * API key policy
  * JWT policy
  * Keyless policy
  * OAuth2 policy
  * JSON to JSON policy
  * JSON to XML policy
  * XML to JSON
  * Assign attributes policy
  * Latency policy
  * Circuit breaker policy
  * Retry policy
  * Cache policy
  * Transform headers policy
* New Cloud Events policy
* New serialization and deserialization policies
  * JSON to Avro policy
  * Avro to JSON policy

**Developer Portal**

* Configure Webhook subscription details in the Developer Portal (by the consumer/subscriber)

**Integrations**

* Datadog reporter

**Management API**

* v2 Management API that supports actions for v4 APIs

**Kubernetes Operator**

* Use the Kubernetes Operator as a Kubernetes ingress controller
* Maintain a unique custom resource definition (CRD) for your API across all Gravitee environments
* Manage application-level CRDs through the Gravitee Kubernetes Operator
* Define the ManagementContext for your CRD and control whether the API should be local or global

**MongoDB Migration Scripts**

* MongoDB migration scripts are now embedded and automatically executed when starting APIM. There is no longer a need to run JavaScript scripts manually.

</details>

<details>

<summary>Breaking Changes</summary>

**EE plugins**

* Starting with APIM 4.0, particular plugins are only available to enterprise customers. [See Gravitee APIM Enterprise Edition](../../overview/ee-vs-oss/README.md) for additional information.

**Running APIM**

* APIM now requires a minimum of JDK 17.
* Starting with 4.0.0, there will no longer be enterprise tags (i.e. suffixed by `-ee`).
* Cluster managers are now available as plugins. Therefore, Hazelcast Cluster Manager has been removed from the default distribution.
* TLS 1.0 and TLS 1.1 protocols are disabled by default. You can still enable these protocols with the proper TCP SSL configuration of the Gateway:

{% code title="gravitee.yaml" %}
```yaml
http:
  ssl:
    tlsProtocols: TLSv1.0, TLSv1.1, TLSv1.2
```
{% endcode %}

or using environment variables:

```bash
GRAVITEE_HTTP_SSL_TLSPROTOCOLS=TLSv1.0,TLSv1.1,TLSv1.2
```

**Docker images**

To be compliant with [CIS\_Docker\_v1.5.0\_L1](https://www.tenable.com/audits/items/CIS\_Docker\_v1.5.0\_L1\_Docker\_Linux.audit:bdcea17ac365110218526796ae3095b1), the Docker images are now using a dedicated user: `graviteeio`.

This means that if you:

* Use the official images and deploy them to Kubernetes, nothing changes.
* Build your own Dockerfile based on Gravitee images, you must ensure the correct rights are set on the files and directories you add to the image.
* Deploy in `openshift`, you have to add the following configuration to your deployment:

```yaml
securityContext:
    runAsGroup: 1000
```

**Monitoring APIM**

* The name of the sync probe has been changed from `api-sync` to `sync-process` to make it explicit when all sync processes have been completed.
* The content of the sync handler has changed slightly to align with new concepts:
  * `initialDone`: `true` if the first initial synchronization is done
  * `counter`: The number of iterations
  * `nextSyncTime`: Time of the next synchronization
  * `lastOnError`: The latest synchronization with an error
  * `lastErrorMessage`: If `lastOnError` is `true`, the content of the error message
  * `totalOnErrors`: The number of iterations with an error
* v4 APIs currently only support the ElasticSearch reporter. If any other reporter is configured at the Gateway level, each v4 API call will produce an error log.
  * When using a different reporter, it remains possible to disable analytics on a per-API basis to avoid generating error logs for v4 APIs.

**Managing APIs**

*   The endpoint configuration is now split into:

    * A shared configuration that can be used at the group level
    * A configuration dedicated to the endpoint that can override the shared configuration.

    Existing v4 APIs need to be updated and reconfigured accordingly.
* An unused and outdated feature regarding file synchronization known as `localregistry` has been removed.
* Subscriptions with `type: SUBSCRIPTION` have been renamed to `type: PUSH`. Plans have a new field called `mode` that is `STANDARD` by default but needs to be `PUSH` for all Push plans.
  * A [mongo script](https://github.com/gravitee-io/gravitee-api-management/tree/master/gravitee-apim-repository/gravitee-apim-repository-mongodb/src/main/resources/scripts/4.0.0) is available to migrate the data in MongoDB.
* Jupiter mode has been replaced with the v4 emulation engine:
  * `jupiterModeEnabled` configuration has been removed and can no longer be disabled.
  * By default, any v2 API created or imported will emulate V4 Engine.
  * All new requests will use the new `HttpProtocolVerticle` introduced with the V4 engine. The old `ReactorVerticle` has been removed.
  * The default timeout is set to 30s for any request.
*   Security policies such as Keyless, ApiKey, JWT, and Oauth2 have been updated to return a simple Unauthorized message in case of an error. No additional details are provided to protect against a potential attacker. **This impacts both v2 and v4 APIs.** Error keys remain available for error templating. Here is a list of error keys by policy:

    **ApiKey**

    * API\_KEY\_MISSING
    * API\_KEY\_INVALID
    * JWT
      * JWT\_MISSING\_TOKEN
      * JWT\_INVALID\_TOKEN

    **Oauth2**

    * OAUTH2\_MISSING\_SERVER
    * OAUTH2\_MISSING\_HEADER
    * OAUTH2\_MISSING\_ACCESS\_TOKEN
    * OAUTH2\_INVALID\_ACCESS\_TOKEN
    * OAUTH2\_INVALID\_SERVER\_RESPONSE
    * OAUTH2\_INSUFFICIENT\_SCOPE
    * OAUTH2\_SERVER\_UNAVAILABLE
*   Plan selection has been changed to reflect the actual security applied on the API:

    **Keyless**

    * Will ignore any type of security (API key, Bearer token, etc.).
    * **If another plan has detected a security token, valid or invalid, all flows assigned to the Keyless plan will be ignored.**

    **API Key**

    * Retrieve the API key from the request header or query parameters (default header: `X-Gravitee-Api-Key` and default query parameter: `api-key`).
    * While it was previously ignored, **an empty API key is now considered invalid**.

    **JWT**

    * Retrieve JWT from `Authorization` header or query parameters.
    * Ignore empty `Authorization` header or any type other than Bearer.
    * While it was previously ignored, **an empty Bearer token is now considered invalid**.

    **OAuth2**

    * Retrieve OAuth2 from `Authorization` header or query parameters.
    * Ignore empty `Authorization` header or any type other than Bearer.
    * While it was previously ignored, **an empty Bearer token is now considered invalid**.
* Plugins are now overridden when duplicates (id/type) are found. The plugin zip file with the most recent modified time is kept and others are ignored. Notably, this allows `additionalPlugins` for Helm chart-based deployment to operate efficiently without the need to remove bundled plugins.
* The v4 API definition now expects a `FlowExecution` object instead of a `FlowMode` enumeration.
* The Gravitee Expression Language (EL) syntax to access custom API properties has changed from `{#properties}` to `{#api.properties}`.
* The `Endpoint` schema is now split into two schemas and the `Endpoint` object contains two string fields to manage both the configuration specific to the endpoint and the configuration that may be overridden from the `EndpointGroup`.
* Endpoint name and endpoint group name must be unique.
*   Analytics have been introduced and the old logging configuration has been moved. **For v4 APIs only**, a new `Analytics` object is available on the API allowing you to configure all aspects of analytics:

    ```json
    "analytics": {
      "enabled" : true|false,
      "logging": { ... },
      "messageSampling" : { ... }
    }
    ```
* The Webhook subscription configuration structure has changed.
* `ApiType` enumeration has been renamed: `SYNC` becomes `PROXY` and `ASYNC` becomes `MESSAGE`). v4 APIs and PUBLISH\_API events related to V4 APIs with old values may prevent the service to start properly. **The following script migrates data for MongoDB:**

```
print('Rename ApiType from SYNC & ASYNC to PROXY & MESSAGE');
// Override this variable if you use prefix
const prefix = "";

let apisCollection = db.getCollection(`${prefix}apis`);
apisCollection.find({"definitionVersion": "V4"}).forEach((api) => {
	if (api.type == "SYNC") {
		api.definition = api.definition.replace('"type" : "sync"', '"type" : "proxy"');
		api.type = "PROXY";
        	apisCollection.replaceOne({ _id: api._id }, api);
	}
	if (api.type == "ASYNC") {
		api.definition = api.definition.replace('"type" : "async"', '"type" : "message"');
		api.type = "MESSAGE";
	        apisCollection.replaceOne({ _id: api._id }, api);
	}
});


let eventsCollection = db.getCollection(`${prefix}events`);
eventsCollection.find({"type": "PUBLISH_API"}).forEach((event) => {

       event.payload = event.payload.replace('\\"type\\" : \\"sync\\"', '\\"type\\" : \\"proxy\\"');
       event.payload = event.payload.replace('\\"type\\" : \\"async\\"', '\\"type\\" : \\"message\\"');
	event.payload = event.payload.replace('"type" : "sync"', '"type" : "proxy"');
	event.payload = event.payload.replace('"type" : "async"', '"type" : "message"');
		
       eventsCollection.replaceOne({ _id: event._id }, event);
});
```

**Login Endpoint**

In previous versions, sending a POST request to `/user/login` without an `Authorization` header returned HTTP Response 200.

Starting with 4.0.0, if a POST request to `/user/login` does not have an `Authorization` header, it will receive an HTTP response 401 - Unauthorized.

</details>
