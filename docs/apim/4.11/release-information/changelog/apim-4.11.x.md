# APIM 4.11.x
 
## Gravitee API Management 4.11.19 - July 13, 2026
<details>

<summary>Improvements</summary>

**Gateway**

* Improve the GW performance (subscriptions cache improved) [#11627](https://github.com/gravitee-io/issues/issues/11627)

</details>


 
## Gravitee API Management 4.11.18 - July 11, 2026
<details>

<summary>Bug Fixes</summary>

**Other**

* SSE Messages Received Out of Order [#11587](https://github.com/gravitee-io/issues/issues/11587)
* Groovy error after upgrading from APIM 4.9.26 to 4.9.27 [#11625](https://github.com/gravitee-io/issues/issues/11625)

</details>


 
## Gravitee API Management 4.11.17 - July 9, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Rate limit silently bypassed on 4.11.16 (Redis: Connection is closed) [#11621](https://github.com/gravitee-io/issues/issues/11621)

</details>


 
## Gravitee API Management 4.11.16 - July 8, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* Custom API Key header toggle is hidden in the console, blocking custom-header configuration on gateways < 4.11.1 [#11616](https://github.com/gravitee-io/issues/issues/11616)
* Groovy policy configuration form shows the wrong fields in the console [#11617](https://github.com/gravitee-io/issues/issues/11617)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* API Product - distributed sync enablement [#11579](https://github.com/gravitee-io/issues/issues/11579)

</details>


 
## Gravitee API Management 4.11.15 - July 3, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Client abort does not release the http-proxy endpoint connection pool slot (v4 API) [#11596](https://github.com/gravitee-io/issues/issues/11596)

**Management API**

* DELETE API returns 500 instead of 404 when API doesn't exist - causes GKO reconcile loop [#11597](https://github.com/gravitee-io/issues/issues/11597)

</details>


 
## Gravitee API Management 4.11.14 - July 1, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway requestTimeout ignored in helm charts [#11500](https://github.com/gravitee-io/issues/issues/11500)
* #request.xmlContent on malformed XML blocks the Vert.x event loop (sanitizeContent infinite loop) [#11522](https://github.com/gravitee-io/issues/issues/11522)

**Console**

* Impossible to set a group admin [#11544](https://github.com/gravitee-io/issues/issues/11544)
* User details - Groups roles name are truncated [#11545](https://github.com/gravitee-io/issues/issues/11545)
* Certificate expire date time is missing [#11559](https://github.com/gravitee-io/issues/issues/11559)

**Other**

* Long version number breaks the layout in the Developer Portal [#11364](https://github.com/gravitee-io/issues/issues/11364)
* Traffic shadowing does not work with failover for v2 APIs [#11477](https://github.com/gravitee-io/issues/issues/11477)
* Cannot edit existing subscription in developer portal for API with a custom subscription form [#11563](https://github.com/gravitee-io/issues/issues/11563)

</details>


 
## Gravitee API Management 4.11.13 - June 25, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway with LLM proxy API deployed won't start  [#11574](https://github.com/gravitee-io/issues/issues/11574)

</details>


 
## Gravitee API Management 4.11.12 - June 24, 2026

{% hint style="warning" %}
There is a known issue with LLM Proxy APIs in this version of APIM. If you have at least an LLM Proxy API deployed to your Gateway, do not upgrade to this version of APIM. Upgrade to version 4.11.13+.
{% endhint %}

<details>

<summary>Bug Fixes</summary>

**Console**

* Debug mode selects SaaS gateway instead of hybrid gateway when API has a sharding tag [#11533](https://github.com/gravitee-io/issues/issues/11533)

**Other**

* Dynamic Routing redirect rules broken  [#11571](https://github.com/gravitee-io/issues/issues/11571)

</details>


 
## Gravitee API Management 4.11.11 - June 20, 2026

{% hint style="warning" %}
There is a known issue with the flows in this version of APIM. Do not upgrade to this version of APIM. Upgrade to version 4.11.13+.
{% endhint %}

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Produce OpenTelemetry server spans [#11046](https://github.com/gravitee-io/issues/issues/11046)
* Disable external entities on the EL xmlContent XMLInputFactory (XXE hardening) [#11527](https://github.com/gravitee-io/issues/issues/11527)
* ClassCastException in reactive contextual logging when ATTR_REQUEST_METHOD is set to HttpMethod by rest-to-soap policy [#11532](https://github.com/gravitee-io/issues/issues/11532)

**Console**

* Use default scopes for OpenID Connect identity providers [#11322](https://github.com/gravitee-io/issues/issues/11322)
* Debug Mode Trailing Slash Behavior – Clarification [#11428](https://github.com/gravitee-io/issues/issues/11428)
* Account settings - Problem updating avatar [#11538](https://github.com/gravitee-io/issues/issues/11538)

**Other**

* MCP Proxy built-in {{/.well-known/oauth-protected-resource}} handling breaks backward compatibility with externally deployed APIs at the same path [#11450](https://github.com/gravitee-io/issues/issues/11450)
* EL not supported for Kafka producer topics [#11482](https://github.com/gravitee-io/issues/issues/11482)
* NGINX error on response when using Assing Content on Request [#11483](https://github.com/gravitee-io/issues/issues/11483)
* Gateway Cannot Write to /models Directory in Debian Image [#11492](https://github.com/gravitee-io/issues/issues/11492)
* APIM 4.11  – Developer Portal – Documentation Display Issue [#11496](https://github.com/gravitee-io/issues/issues/11496)
* Equals operator should not be able to be saved with a wildcard path in flow configuration [#11512](https://github.com/gravitee-io/issues/issues/11512)
* Subscription metadata silently ignored on POST /management/v2/environments/{envId}/apis/{apiId}/subscriptions [#11513](https://github.com/gravitee-io/issues/issues/11513)
* Subscription metadata not synced to gateway in live requires restart to take effect [#11517](https://github.com/gravitee-io/issues/issues/11517)
* Do not cache empty or errored EL resolution of ACL resource patterns [#11528](https://github.com/gravitee-io/issues/issues/11528)
* A single log entry with a malformed @timestamp breaks the entire logs page (HTTP 500) [#11529](https://github.com/gravitee-io/issues/issues/11529)
* Transform Headers policy addHeaders not propagated to upstream provider call on LLM Proxy APIs [#11531](https://github.com/gravitee-io/issues/issues/11531)
* V2 API duplication with plans fails: plan not copied, "Api \[<environmentId>] cannot be found" [#11535](https://github.com/gravitee-io/issues/issues/11535)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Classify gateway to backend connection failures into specific error keys [#11554](https://github.com/gravitee-io/issues/issues/11554)

**Console**

* Events are not filtered in Global Analytics graphs [#11520](https://github.com/gravitee-io/issues/issues/11520)

**Other**

* API export silently returns empty file when serialization fails [#11320](https://github.com/gravitee-io/issues/issues/11320)
* AVRO→JSON: decode Kafka record key on subscribe phase [#11507](https://github.com/gravitee-io/issues/issues/11507)

</details>


 
## Gravitee API Management 4.11.10 - June 8, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* BUG: LLM_PROXY, Bedrock streaming [#11426](https://github.com/gravitee-io/issues/issues/11426)
* \[Kafka Topic Mapping policy] OffsetFetch fails with UNKNOWN_SERVER_ERROR when client requests offsets for all topics of a group [#11495](https://github.com/gravitee-io/issues/issues/11495)

**Management API**

* MCP Tool Generation – Nullable field handling in generated inputSchema (OpenAPI import) [#11340](https://github.com/gravitee-io/issues/issues/11340)
* API rollback of undeployed changes leaves API in "out of sync" state [#11459](https://github.com/gravitee-io/issues/issues/11459)
* V4 _import/crd create path ignores flowExecution and persists defaults (mode=default, matchRequired=false) [#11476](https://github.com/gravitee-io/issues/issues/11476)
* encodage UTF-8 [#11480](https://github.com/gravitee-io/issues/issues/11480)
* JDBC: gateway warmup ApiKey appender Seq-scans key_subscriptions (missing subscription_id index) [#11494](https://github.com/gravitee-io/issues/issues/11494)
* Group error when updating V2 API settings after upgrade to 4.11.9, 4.10.16, 4.9.21 or 4.8.28 [#11510](https://github.com/gravitee-io/issues/issues/11510)

**Console**

* SharedPolicyGroup for API Message are undeployable [#11182](https://github.com/gravitee-io/issues/issues/11182)
* Platform alert API filter dropdown fails to load any APIs (v2 or v4) in v4.8.8 [#11466](https://github.com/gravitee-io/issues/issues/11466)
* Documentation - Swagger viewing issue  [#11485](https://github.com/gravitee-io/issues/issues/11485)
* Observability & Analytics Sidebar Navigation Broken in APIM 4.11.x [#11505](https://github.com/gravitee-io/issues/issues/11505)

**Portal**

* Query params for Try it out does not work [#11481](https://github.com/gravitee-io/issues/issues/11481)

**Other**

* Allow default role mapping through API V2 group endpoint [#11300](https://github.com/gravitee-io/issues/issues/11300)
* Token type validation disabled still rejects tokens with typ: JWS due to restrictive Nimbus default verifier [#11380](https://github.com/gravitee-io/issues/issues/11380)
* SSO Icon icons/thirdparty.svg not displaying in dev portal -> login [#11418](https://github.com/gravitee-io/issues/issues/11418)

</details>

<details>

<summary>Improvements</summary>

**Other**

* HTTP Callout Policy "Request body" needs to support multi-line UI. [#11504](https://github.com/gravitee-io/issues/issues/11504)

</details>


 
## Gravitee API Management 4.11.9 - June 1, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Gateway primary stays unhealthy after restart when distributed sync is enabled [#11468](https://github.com/gravitee-io/issues/issues/11468)
* Gateway sync can hang indefinitely on slow bridge responses (no per-request timeout) [#11469](https://github.com/gravitee-io/issues/issues/11469)

**Management API**

* MAPI v2 doesn't accept group names [#11351](https://github.com/gravitee-io/issues/issues/11351)
* Audit retention cleaner fails with SocketTimeoutException on populated `audits` collections [#11434](https://github.com/gravitee-io/issues/issues/11434)

**Console**

* Audit Log event type filter in the APIM Console does not populate v4 APIs [#11429](https://github.com/gravitee-io/issues/issues/11429)
* API v2 Logging configuration - Problem when using a combination of criteria in the EL expression  [#11472](https://github.com/gravitee-io/issues/issues/11472)

**Other**

* Setting Redoc viewer as default does not apply for v4 API documents [#11188](https://github.com/gravitee-io/issues/issues/11188)
* Prometheus label http_route / http_path not appearing on proxy traffic metrics [#11335](https://github.com/gravitee-io/issues/issues/11335)
* Viewing MD documentation in the developer portal [#11366](https://github.com/gravitee-io/issues/issues/11366)
* Groups settings are not accessible, requires read permissions on organisation settings [#11388](https://github.com/gravitee-io/issues/issues/11388)
* Incorrect Response Status and Missing Error Details in Azure Service Bus Logs [#11392](https://github.com/gravitee-io/issues/issues/11392)
* Promoting APIs that exist in the target env causes subscription errors [#11398](https://github.com/gravitee-io/issues/issues/11398)
* Webhook notification configuration error [#11408](https://github.com/gravitee-io/issues/issues/11408)
* Advanced configuration is not accessible for push plan subscriptions [#11414](https://github.com/gravitee-io/issues/issues/11414)
* Regression Dynamic Routing policy with retry policy [#11444](https://github.com/gravitee-io/issues/issues/11444)
* Can't change group permission on api [#11449](https://github.com/gravitee-io/issues/issues/11449)
* Scrolling issue in the API Management UI [#11465](https://github.com/gravitee-io/issues/issues/11465)
* deadlocked on lock resources with another process errors [#11475](https://github.com/gravitee-io/issues/issues/11475)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Optimize gateway-sync SubscriptionFetcher: env-prefix index and cursor pagination [#11432](https://github.com/gravitee-io/issues/issues/11432)
* Optimize gateway-sync ApiKeyFetcher + ApiKeyAppender: cursor pagination (mirror of APIM-14087) [#11474](https://github.com/gravitee-io/issues/issues/11474)

**Management API**

* Optimize subscription expiration schedulers: ESR-correct index and remove redundant default sort [#11431](https://github.com/gravitee-io/issues/issues/11431)
* Optimize APIs search: collapse `$or \[definitionVersion IN, isNull]` and add ESR-ordered compound index [#11433](https://github.com/gravitee-io/issues/issues/11433)
* Add compound index for subscription search by plan list [#11436](https://github.com/gravitee-io/issues/issues/11436)
* Add compound index on `apis` collection for catalog category filtering [#11437](https://github.com/gravitee-io/issues/issues/11437)
* Cap `count()` cost on paginated Mongo repository searches with `maxTimeMS` [#11438](https://github.com/gravitee-io/issues/issues/11438)
* Optimize ApiKey pre-expiration scheduler fan-out (mirror of APIM-14086) [#11456](https://github.com/gravitee-io/issues/issues/11456)

**Console**

* DCR configuration UI: clarify {#client_id} placeholder and fix example renew secret endpoint [#11430](https://github.com/gravitee-io/issues/issues/11430)
* Cap `count()` cost on paginated Mongo repository searches with `maxTimeMS` [#11438](https://github.com/gravitee-io/issues/issues/11438)

**New indexes**
* Added the following indexes, which you can add manually before you upgrade to 4.11.9:
```bash
db.apis.createIndex({ environmentId:1, categories:1, name:1 }, { name: "ei1c1n1" });
  db.apis.createIndex({ environmentId:1, definitionVersion:1, name:1 }, { name: "ei1dv1n1" });
  db.keys.createIndex({ environmentId:1, updatedAt:1, _id:1 }, { name: "e1ua1i1" });
  db.keys.createIndex({ revoked:1, expireAt:1 }, { name: "r1ea1" });
  db.plans.createIndex({ crossId:1 }, { name: "ci1" });
  db.subscriptions.createIndex({ environmentId:1, updatedAt:1, _id:1 }, { name: "e1ua1i1" });
  db.subscriptions.createIndex({ plan:1, _id:1 }, { name: "p1i1" });
  db.subscriptions.createIndex({ plan:1, updatedAt:1 }, { name: "p1ua1" });
  db.subscriptions.createIndex({ status:1, endingAt:1 }, { name: "s1ea1" });
  db.audits.createIndex({ environmentId:1, createdAt:1 }, { name: "e1c1" });
```
</details>


 
## Gravitee API Management 4.11.8 - June 1, 2026
<details>

<summary>Bug Fixes</summary>

**Management API**

* v4 HTTP Proxy API — null pathOperator in flow HTTP selector causes 500 NPE instead of 400 [#11491](https://github.com/gravitee-io/issues/issues/11491)

</details>


 
## Gravitee API Management 4.11.7 - May 19, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Health Check endpoint doesn't execute [#11394](https://github.com/gravitee-io/issues/issues/11394)
* Gravitee API Product adoption issues [#11417](https://github.com/gravitee-io/issues/issues/11417)
* Webhook subscriptions fail with NPE [#11419](https://github.com/gravitee-io/issues/issues/11419)

**Management API**

* APIM v4.11.x Failing Changeset || Orphan plans [#11365](https://github.com/gravitee-io/issues/issues/11365)
* API Proxy deployment using Terraform provider fail [#11378](https://github.com/gravitee-io/issues/issues/11378)
* Validation of duplicated context paths does not check secondary context paths [#11409](https://github.com/gravitee-io/issues/issues/11409)
* Shared API key renewal persists new key with environmentId=null [#11439](https://github.com/gravitee-io/issues/issues/11439)
* JDBC: Liquibase changeset 1.25.2-rebuild-key-pk-other precondition is schema-blind on Postgres/MSSQL/H2 [#11440](https://github.com/gravitee-io/issues/issues/11440)

**Console**

* Unable to Change the Custom Timeframe after Error [#11154](https://github.com/gravitee-io/issues/issues/11154)
* Deprecated plans missing from Policy Studio for v4 APIs [#11399](https://github.com/gravitee-io/issues/issues/11399)
* Payload Search Not Working [#11403](https://github.com/gravitee-io/issues/issues/11403)

**Portal**

* Payload Search Not Working [#11403](https://github.com/gravitee-io/issues/issues/11403)
* Error 500 when trying to filter logs in the developer portal [#11405](https://github.com/gravitee-io/issues/issues/11405)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Maintain an in-memory API path index to avoid full-catalog scan on path collision check [#11424](https://github.com/gravitee-io/issues/issues/11424)

</details>


 
## Gravitee API Management 4.11.6 - May 7, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* OTEL: policy.trigger.executed always true for conditional policies [#11385](https://github.com/gravitee-io/issues/issues/11385)

**Management API**

* Access control references to deleted groups prevents promotions [#11334](https://github.com/gravitee-io/issues/issues/11334)
* Global policies deleted [#11390](https://github.com/gravitee-io/issues/issues/11390)
* Exposed Entrypoints bug when using sharding tags and virtual host [#11395](https://github.com/gravitee-io/issues/issues/11395)
* Unable to connect to console anymore [#11406](https://github.com/gravitee-io/issues/issues/11406)

**Other**

* Not possible to use EL for Solace Topics  [#11261](https://github.com/gravitee-io/issues/issues/11261)
* APIM - Host in healthcheck Header  does not work [#11328](https://github.com/gravitee-io/issues/issues/11328)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Support PNA on the gateway [#11252](https://github.com/gravitee-io/issues/issues/11252)

**Management API**

* JDBC: migrate emoji-bearing NVARCHAR columns from utf8mb3 to utf8mb4 on MySQL/MariaDB [#11400](https://github.com/gravitee-io/issues/issues/11400)
* JDBC repository: support MySQL deployments with sql_require_primary_key=ON [#11401](https://github.com/gravitee-io/issues/issues/11401)
* SubscriptionReferenceTypeUpgrader & PlanReferenceTypeUpgrader improvement [#11402](https://github.com/gravitee-io/issues/issues/11402)

</details>


 
## Gravitee API Management 4.11.5 - April 30, 2026
<details>

<summary>Bug Fixes</summary>

**Management API**

* NullPointerException when opening the Audit Log page in the Management UI, caused by a missing DASHBOARD reference type mapping in the service layer. [#11339](https://github.com/gravitee-io/issues/issues/11339)
* Creating a subscription on an api key plan results on two api keys generation [#11347](https://github.com/gravitee-io/issues/issues/11347)
* Console sends undefined API ID for V2 API when closing plan [#11367](https://github.com/gravitee-io/issues/issues/11367)

**Console**

* API members with Member Read and Definition Update permissions can modify group access [#11259](https://github.com/gravitee-io/issues/issues/11259)
* Re: Search user api wrong result when paginated [#11311](https://github.com/gravitee-io/issues/issues/11311)
* Roles permissions are in-consistent.  [#11324](https://github.com/gravitee-io/issues/issues/11324)

**Portal**

* Default portal navigation items are created on every Cloud environment update [#11369](https://github.com/gravitee-io/issues/issues/11369)

**Other**

* Consuming Kafka tombstone messages causes NullPointerException [#11353](https://github.com/gravitee-io/issues/issues/11353)
* PromptGuardRails policy - contentChecks filter not applied to block reason, exposing unintended classifier labels in error response [#11373](https://github.com/gravitee-io/issues/issues/11373)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Some warnings displayed after upgrade to v 4.7.x [#10862](https://github.com/gravitee-io/issues/issues/10862)

**Management API**

* Some warnings displayed after upgrade to v 4.7.x [#10862](https://github.com/gravitee-io/issues/issues/10862)
* Include API metadata in the same endpoint response as the rest of the API data [#10971](https://github.com/gravitee-io/issues/issues/10971)

**Console**

* Portal navigation items: open context menu with right click [#11384](https://github.com/gravitee-io/issues/issues/11384)

**Other**

* Add opt-in URL path normalization to the Resource Filtering policy [#11337](https://github.com/gravitee-io/issues/issues/11337)

</details>


 
## Gravitee API Management 4.11.4 - April 21, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* Unable to edit inline Markdown document/page for v2 APIs and portal documentation [#11348](https://github.com/gravitee-io/issues/issues/11348)

**Portal**

* Group users of an API cannot see it in the Next Gen Portal [#11360](https://github.com/gravitee-io/issues/issues/11360)
* Documentation items permissions are different from catalog permissions [#11361](https://github.com/gravitee-io/issues/issues/11361)

</details>


 
## Gravitee API Management 4.11.3 - April 21, 2026
<details>

<summary>Bug Fixes</summary>

**Management API**

* Users that do not have any API Products permissions receive an error on the general configuration page of v4 APIs [#11350](https://github.com/gravitee-io/issues/issues/11350)

**Console**

* Users that do not have any API Products permissions receive an error on the general configuration page of v4 APIs [#11350](https://github.com/gravitee-io/issues/issues/11350)

**Helm Charts**

* 4.11 upgrade attempt with helm failing with openshift context error  [#11359](https://github.com/gravitee-io/issues/issues/11359)

</details>


 
## Gravitee API Management 4.11.2 - April 17, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Prometheus scrapping error: scrape request times out [#11036](https://github.com/gravitee-io/issues/issues/11036)
* Data masking policy masks the whole payload [#11303](https://github.com/gravitee-io/issues/issues/11303)
* Gateway ConcurrentModificationException during request dispatch [#11312](https://github.com/gravitee-io/issues/issues/11312)
* OpenAPI Specification Validation Policy - Validation errors [#11330](https://github.com/gravitee-io/issues/issues/11330)
* Dictionaries not available in v2 API resource configuration [#11346](https://github.com/gravitee-io/issues/issues/11346)

**Management API**

* V2 API failed to migrate to v4 due to endpoint configuration [#11264](https://github.com/gravitee-io/issues/issues/11264)
* v4 API logs are inaccessible when the analytics type is none [#11297](https://github.com/gravitee-io/issues/issues/11297)

**Console**

* endpointGroups.sharedConfiguration.headers and endpointGroups.sharedConfiguration.http Cannot Be Applied Together in v4 api defintion [#11163](https://github.com/gravitee-io/issues/issues/11163)
* endpointGroups.sharedConfiguration.headers and endpointGroups.sharedConfiguration.http Cannot Be Applied Together in v4 api defintion [#11168](https://github.com/gravitee-io/issues/issues/11168)
* The filters applied in the v4 API logs are not preserved  [#11302](https://github.com/gravitee-io/issues/issues/11302)

**Other**

* Warning - Failed to evaluate duration [#11341](https://github.com/gravitee-io/issues/issues/11341)

</details>

<details>

<summary>Improvements</summary>

**Console**

* Add Entra ID to the OAuth2 API Resources [#11345](https://github.com/gravitee-io/issues/issues/11345)

**Other**

* When returning the protected resource metadata from the OAuth2 policy, it should include the scopes [#11343](https://github.com/gravitee-io/issues/issues/11343)

**Helm chart**

* Improve JDBC driver delivery options in the Helm chart:
  * `auto` uses bundled PostgreSQL, MariaDB, and SQL Server drivers, and uses startup download for MySQL and other custom JDBC families
  * `image` allows using a dedicated customer-provided JDBC image instead of downloading the driver at startup
  * `download` keeps the explicit startup download mode
  * `preinstalled` allows using JDBC drivers already baked into custom API and Gateway runtime images, without JDBC runtime provisioning
* Validate `jdbc.driverSource` values during chart rendering and fail on unsupported values.

</details>


 
## Gravitee API Management 4.11.1 - April 4, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* Revert: Unable to reset the password [#11289](https://github.com/gravitee-io/issues/issues/11289)

</details>


## Gravitee API Management 4.11.0 - April 3, 2026

<details>

<summary>Bug Fixes</summary>

**Gateway**

* SSL enforcement policy will return a 403 if if the SSL connection is terminated at the ingress level [#11234](https://github.com/gravitee-io/issues/issues/11234)
* Duplicate traceparent header [#11248](https://github.com/gravitee-io/issues/issues/11248)
* The Health Check of the API V4 is not working as expected with tenant [#11275](https://github.com/gravitee-io/issues/issues/11275)
* Secret resolution failure in SPG when combined with multiple policies [#11279](https://github.com/gravitee-io/issues/issues/11279)
* gravitee-resource-cache-redis leaks LettuceConnectionFactory on every API redeploy [#11314](https://github.com/gravitee-io/issues/issues/11314)

**Management API**

* Promotion Button in UI Yields Parsing Error [#11277](https://github.com/gravitee-io/issues/issues/11277)
* Unable to resend or retrigger expired sign-up confirmation links [#11295](https://github.com/gravitee-io/issues/issues/11295)
* Error when deleting an API with pages [#11308](https://github.com/gravitee-io/issues/issues/11308)

**Console**

* Not able search/filter logs by path [#11255](https://github.com/gravitee-io/issues/issues/11255)
* v4 API promotions are stuck in a pending state [#11281](https://github.com/gravitee-io/issues/issues/11281)
* Unable to reset the password [#11289](https://github.com/gravitee-io/issues/issues/11289)

**Other**

* JSON Web Token policy always returns fails to validate token [#11233](https://github.com/gravitee-io/issues/issues/11233)
* Changing plan order removes the plan flows [#11247](https://github.com/gravitee-io/issues/issues/11247)
* OAuth2 token acquisition failure is silently swallowed [#11250](https://github.com/gravitee-io/issues/issues/11250)
* Webhook Logs toggle not updated after save/publish [#11257](https://github.com/gravitee-io/issues/issues/11257)
* Once I migrate certain V2 APIs to V4, they disappear from the list (/apis) in the UI [#11268](https://github.com/gravitee-io/issues/issues/11268)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* MCP Proxy: serve .well-known/oauth-protected-resource at RFC 9728 compliant host-scoped URL [#11299](https://github.com/gravitee-io/issues/issues/11299)

**Management API**

* Intermittent 500 Error during API Creation: primaryOwner.notFound [#11229](https://github.com/gravitee-io/issues/issues/11229)

**Other**

* Support client\_secret\_basic authentication for OAuth2 token endpoint [#11249](https://github.com/gravitee-io/issues/issues/11249)
* Update IP Filtering policy documentation in [#11251](https://github.com/gravitee-io/issues/issues/11251)
* Add the scope field to the WWW-Authenticate header in the OAuth2 Policy [#11307](https://github.com/gravitee-io/issues/issues/11307)

</details>
