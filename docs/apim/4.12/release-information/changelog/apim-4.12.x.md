---
hidden: false
noIndex: false
---

# APIM 4.12.x
 
## Gravitee API Management 4.12.18 - August 31, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Intermittent 502 / GATEWAY_CLIENT_CONNECTION_ERROR on keep-alive reuse when upstream closes connection (no silent retry) [#11702](https://github.com/gravitee-io/issues/issues/11702)

**Console**

* Organization-level Identity Provider (IdP) "Disable" toggle only hides UI element, remains active in backend [#11717](https://github.com/gravitee-io/issues/issues/11717)

**Portal**

* Developer Portal — "Featured banner" not displaying on 4.12.1 (worked on 4.9.2) [#11751](https://github.com/gravitee-io/issues/issues/11751)

**Event Stream Management**

* Kafka Gateway: DescribeCluster on a virtual cluster bootstrap connection never answers [#11758](https://github.com/gravitee-io/issues/issues/11758)
* Kafka Gateway: virtual cluster controllerId has two sources that diverge after a controller change [#11759](https://github.com/gravitee-io/issues/issues/11759)

**Other**

* Promotion on v4: Response template Status code set to 0 [#11605](https://github.com/gravitee-io/issues/issues/11605)
* JMS endpoint: JNDI initial context factory resolved via TCCL, ignoring plugins/ext/jms libraries [#11701](https://github.com/gravitee-io/issues/issues/11701)
* ClearTextUpgrade still defaults to true on new HTTP/1.1 endpoints [#11741](https://github.com/gravitee-io/issues/issues/11741)
* Webhook entrypoint: OAuth2 token request is sent using the absolute-form request line, and is rejected by intermediate proxies [#11745](https://github.com/gravitee-io/issues/issues/11745)
* Portal Next — login page not centered in Firefox [#11748](https://github.com/gravitee-io/issues/issues/11748)
* policy-circuit-breaker opens on a single call and ignores interrupted calls [#11767](https://github.com/gravitee-io/issues/issues/11767)
* Time-series analytics return buckets outside the requested window, shifting every point by one interval

</details>

<details>

<summary>Improvements</summary>

**Other**

* Support CORS configuration on LLM Proxy [#11699](https://github.com/gravitee-io/issues/issues/11699)

</details>


 
## Gravitee API Management 4.12.17 - August 21, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* analytics/facets APPLICATION COUNT sum ≠ analytics/measures COUNT (stable on closed months) [#11693](https://github.com/gravitee-io/issues/issues/11693)

**Other**

* High cardinality of APM data due to transaction.name including concrete path values and query params [#11673](https://github.com/gravitee-io/issues/issues/11673)
* Two dictionaries can share one runtime slot; removing either breaks the other until restart [#11674](https://github.com/gravitee-io/issues/issues/11674)
* Metadata block export after v4 migration [#11726](https://github.com/gravitee-io/issues/issues/11726)
* Rate Limit and Quota policies can be saved without a limit, causing every request to fail with a 500 [#11727](https://github.com/gravitee-io/issues/issues/11727)
* Issue | Error parsing request header [#11730](https://github.com/gravitee-io/issues/issues/11730)

</details>

<details>

<summary>Improvements</summary>

**Console**

* API Runtime Logs: default Period to Last 5 Minutes instead of None [#11739](https://github.com/gravitee-io/issues/issues/11739)

</details>


 
## Gravitee API Management 4.12.16 - August 18, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* \[V3 engine] X-Gravitee-Transaction-Id and X-Gravitee-Request-Id not set on gateway error responses (auth/IP-filter/quota) [#11657](https://github.com/gravitee-io/issues/issues/11657)

**Console**

* Console UI: Clicking any "Template to include" always opens the same template when multiple exist [#11711](https://github.com/gravitee-io/issues/issues/11711)

**Other**

* Terraform Drift [#11470](https://github.com/gravitee-io/issues/issues/11470)
* Domain pattern properties are not available in case of multiple domains used [#11660](https://github.com/gravitee-io/issues/issues/11660)
* Multiple applications can be created with the same client id [#11692](https://github.com/gravitee-io/issues/issues/11692)
* Nil pointer panic in subscription webhook when Application/API has no context defined [#11722](https://github.com/gravitee-io/issues/issues/11722)
* JMS endpoint: consumer never recovers after a broker connection loss, and IBM MQ auto-reconnect cannot be enabled as a workaround [#11731](https://github.com/gravitee-io/issues/issues/11731)
* Gateway leaks one Vert.x NetClient per health check execution since 4.12
* Registration email sent before approval, allowing pending users to set a password and then fail login
* API Score Evaluate fails when many custom rulesets are configured (works if rules are merged into fewer files)

</details>

<details>

<summary>Improvements</summary>

**Console**

* leave XSLT parameters unbound when their expression resolves to no value [#11738](https://github.com/gravitee-io/issues/issues/11738)

**Other**

* \[APIM] Creating a service account without `lastname` via mAPI fails        with 500 instead of 400 [#11685](https://github.com/gravitee-io/issues/issues/11685)
* Report the full upstream response time, so gateway latency reflects only gateway time [#11719](https://github.com/gravitee-io/issues/issues/11719)
* Report a streaming response cut short under its own error key, with a message that names the timeout responsible [#11735](https://github.com/gravitee-io/issues/issues/11735)

</details>


 
## Gravitee API Management 4.12.15 - August 12, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Native Kafka: dropping a record mid-fetch renumbers the offsets of the surviving records [#11714](https://github.com/gravitee-io/issues/issues/11714)

**Management API**

* MAPI v1 ApiConverter Incorrectly Deserializes V4 API Definitions, Causing Repeated Errors in Management API Logs [#11586](https://github.com/gravitee-io/issues/issues/11586)

**Other**

* API Key plan creation form pre-fills "API Key Header" with static "X-Gravitee-Api-Key" instead of the environment default [#11659](https://github.com/gravitee-io/issues/issues/11659)
* Native Kafka API — a deprecated keyless plan doesn't prevent publishing a secure plan (and breaks the gateway) [#11683](https://github.com/gravitee-io/issues/issues/11683)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Report the full upstream response time, so gateway latency reflects only gateway time [#11719](https://github.com/gravitee-io/issues/issues/11719)

</details>


 
## Gravitee API Management 4.12.14 - August 7, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* Unable to update membership groups across multiple environments after upgrade [#11656](https://github.com/gravitee-io/issues/issues/11656)
* \[Gamma/AIM] LLM Proxy with provider OPEN_AI_COMPATIBLE shows no models — LlmRequestFormat enum is narrower than the llm-proxy connector's [#11677](https://github.com/gravitee-io/issues/issues/11677)
* No data on Observability dashboards for API_PUBLISHER [#11651](https://github.com/gravitee-io/issues/issues/11651)
* Reporting is disabled banner is always present [#11658](https://github.com/gravitee-io/issues/issues/11658)
* APIM 4.12.9 bundles pre-Vert.x-5 fetcher plugins (gitlab/github/bitbucket) → NoSuchMethodError on any fetcher-backed page write [#11667](https://github.com/gravitee-io/issues/issues/11667)


**Portal**

* Role permission are overlapping with environment [#11404](https://github.com/gravitee-io/issues/issues/11404)

**Other**

* Endpoint Health Check Dashboard raises an error in case of disabled ElasticSearch DB [#11530](https://github.com/gravitee-io/issues/issues/11530)
* API promotion fails with DuplicateKeyException on apim_promotions [#11591](https://github.com/gravitee-io/issues/issues/11591)
* PostgreSQL deadlock in JdbcCommandRepository.delete() during search indexer command cleanup [#11644](https://github.com/gravitee-io/issues/issues/11644)
* ApiEndpointWeightUpgrader fails to deserialize V4 Native APIs (InvalidTypeIdException: type id 'native') [#11662](https://github.com/gravitee-io/issues/issues/11662)
* Impossible to filter by deprecated plan into subscriptions list [#11663](https://github.com/gravitee-io/issues/issues/11663)
* RemoveDeletedGroupsFromApisUpgrader skipped because of incompatible database [#11668](https://github.com/gravitee-io/issues/issues/11668)
* Debug request fails without a Host header [#11670](https://github.com/gravitee-io/issues/issues/11670)
* Overview Total Requests can be lower than the count for a single entrypoint [#11695](https://github.com/gravitee-io/issues/issues/11695)

</details>


 
## Gravitee API Management 4.12.13 - July 31, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* The GW should return 405 Method Not Allowed on SSE GET request [#11682](https://github.com/gravitee-io/issues/issues/11682)

**Other**

* Webhook OAuth2 "Client Secret (Basic)" auth incorrectly URL-encodes Client ID/Secret before Base64, breaking credentials containing special characters [#11570](https://github.com/gravitee-io/issues/issues/11570)
* clearTextUpgrade Defaults to true with HTTP_1_1 on Newly Added Endpoints [#11598](https://github.com/gravitee-io/issues/issues/11598)
* Console Audit screen returns HTTP 500 — missing AUTHORIZATION_POLICY/AUTHORIZATION_ENTITY in repository Audit.AuditProperties enum [#11650](https://github.com/gravitee-io/issues/issues/11650)
* OAS Validation policy falsely rejects valid string parameters when schema uses top-level oneOf/anyOf without type (OAS 3.0 / Atlassian SRV path) [#11675](https://github.com/gravitee-io/issues/issues/11675)
* Console: Dictionary property edit dialog enforces 160-character limit (create has no limit) [#11680](https://github.com/gravitee-io/issues/issues/11680)

</details>


 
## Gravitee API Management 4.12.12 - July 28, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* User details - Groups roles name are truncated [#11545](https://github.com/gravitee-io/issues/issues/11545)
* Observability Requests widget is permanently filtered only to proxy APIs [#11636](https://github.com/gravitee-io/issues/issues/11636)

**Portal**

* Portal analytics/logs date filter unusable when browser language is not English [#11626](https://github.com/gravitee-io/issues/issues/11626)

**Other**

* Retry policy on legacy engine always throws error [#11671](https://github.com/gravitee-io/issues/issues/11671)

</details>

<details>

<summary>Improvements</summary>

**Console**

* Trim leading and trailing whitespace from the client_id field in the UI [#11655](https://github.com/gravitee-io/issues/issues/11655)

**Portal**

* Trim leading and trailing whitespace from the client_id field in the UI [#11655](https://github.com/gravitee-io/issues/issues/11655)

</details>


 
## Gravitee API Management 4.12.11 - July 22, 2026
<details>

<summary>Bug Fixes</summary>

**Other**

* Redis resources cannot be disabled [#11407](https://github.com/gravitee-io/issues/issues/11407)

</details>


 
## Gravitee API Management 4.12.10 - July 21, 2026

{% hint style="warning" %}
There is a known issue with API synchronizations in this version of APIM. Upgrade to version 4.12.11+.
{% endhint %}

<details>

<summary>Bug Fixes</summary>

**Management API**

* \[API Product] HTTP 500 on batch update when API search returns duplicate IDs — Collectors.toMap without merge function [#11648](https://github.com/gravitee-io/issues/issues/11648)

**Other**

* Latency issue using redis rate-limit. [#11546](https://github.com/gravitee-io/issues/issues/11546)
* \[gravitee-policy-aws-lambda] 3.4.0 Upgrade Causing Blocked Thread Warnings and Potential Gateway Performance Impact [#11552](https://github.com/gravitee-io/issues/issues/11552)
* Overview dashboard does not respect role permissions [#11555](https://github.com/gravitee-io/issues/issues/11555)
* services.metrics.domains config silently ignored due to singular/plural key mismatch in VertxFactory [#11566](https://github.com/gravitee-io/issues/issues/11566)
* Unrecognized character escape ''' (code 39) when logging Webhook API [#11581](https://github.com/gravitee-io/issues/issues/11581)
* Portal exposes other user's subscription details to users without applications [#11584](https://github.com/gravitee-io/issues/issues/11584)
* Regression: V4 endpoint colon-in-relative-path returns 503 on 4.12.x (APIM-14220 not forward-ported) [#11620](https://github.com/gravitee-io/issues/issues/11620)
* Policy "Interrupt" in response flow [#11623](https://github.com/gravitee-io/issues/issues/11623)
* GW simple perf improvement [#11635](https://github.com/gravitee-io/issues/issues/11635)
* Documentation - Swagger viewing issue  [#11638](https://github.com/gravitee-io/issues/issues/11638)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* v4 HTTP proxy: configurable connection pool wait-queue size (all versions) and max connection lifetime (4.12+) [#11641](https://github.com/gravitee-io/issues/issues/11641)

**Management API**

* v4 HTTP proxy: configurable connection pool wait-queue size (all versions) and max connection lifetime (4.12+) [#11641](https://github.com/gravitee-io/issues/issues/11641)

**Console**

* Increase broadcast message character limit [#11515](https://github.com/gravitee-io/issues/issues/11515)

**Other**

* UI Clutterness in Debug Feature  [#11645](https://github.com/gravitee-io/issues/issues/11645)

</details>


 
## Gravitee API Management 4.12.9 - July 16, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* API list no longer shows when an API is out of sync [#11610](https://github.com/gravitee-io/issues/issues/11610)

**Other**

* EL Not Evaluated in List<CustomObject> Fields by ConfigurationEvaluatorProcessor [#11589](https://github.com/gravitee-io/issues/issues/11589)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Write OTEL trace ID in logs [#11609](https://github.com/gravitee-io/issues/issues/11609)
* Response templates: expose the analytics error detail via {#error.cause} [#11630](https://github.com/gravitee-io/issues/issues/11630)

</details>


 
## Gravitee API Management 4.12.8 - July 14, 2026
<details>

<summary>Bug Fixes</summary>

**Other**

* APIM -  Traffic Shadowing Policy giving status 0 [#11506](https://github.com/gravitee-io/issues/issues/11506)
* Support EL in the headers of MCP Proxy endpoint

</details>


 
## Gravitee API Management 4.12.7 - July 13, 2026
<details>

<summary>Improvements</summary>

**Gateway**

* Improve the GW performance (subscriptions cache improved) [#11627](https://github.com/gravitee-io/issues/issues/11627)

</details>


 
## Gravitee API Management 4.12.6 - July 11, 2026
<details>

<summary>Bug Fixes</summary>

**Other**

* SSE Messages Received Out of Order [#11587](https://github.com/gravitee-io/issues/issues/11587)
* Groovy error after upgrading from APIM 4.9.26 to 4.9.27 [#11625](https://github.com/gravitee-io/issues/issues/11625)

</details>


 
## Gravitee API Management 4.12.5 - July 9, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Rate limit silently bypassed on 4.11.16 (Redis: Connection is closed) [#11621](https://github.com/gravitee-io/issues/issues/11621)

**Console**

* Custom API Key header toggle is hidden in the console, blocking custom-header configuration on gateways < 4.11.1 [#11616](https://github.com/gravitee-io/issues/issues/11616)
* Groovy policy configuration form shows the wrong fields in the console [#11617](https://github.com/gravitee-io/issues/issues/11617)

**Other**

* MCP Studio: tools/call -> -32602 'Unknown tool' — tools-http endpoint connector loads 0 tools (4.12.0/4.12.1) [#11588](https://github.com/gravitee-io/issues/issues/11588)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* API Product - distributed sync enablement [#11579](https://github.com/gravitee-io/issues/issues/11579)

</details>


 
## Gravitee API Management 4.12.4 - July 7, 2026

 
## Gravitee API Management 4.12.3 - July 3, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Client abort does not release the http-proxy endpoint connection pool slot (v4 API) [#11596](https://github.com/gravitee-io/issues/issues/11596)

**Management API**

* Cannot save or import V4 HTTP proxy APIs with default SSL “None” configuration [#11593](https://github.com/gravitee-io/issues/issues/11593)
* DELETE API returns 500 instead of 404 when API doesn't exist - causes GKO reconcile loop [#11597](https://github.com/gravitee-io/issues/issues/11597)

</details>


 
## Gravitee API Management 4.12.2 - July 1, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* Impossible to set a group admin [#11544](https://github.com/gravitee-io/issues/issues/11544)
* User details - Groups roles name are truncated [#11545](https://github.com/gravitee-io/issues/issues/11545)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Auto-scroll to created nav item [#11577](https://github.com/gravitee-io/issues/issues/11577)

</details>


 
## Gravitee API Management 4.12.1 - June 30, 2026
<details>

<summary>Bug Fixes</summary>

**Console**

* 2nd level menu on settings page is not full height [#11575](https://github.com/gravitee-io/issues/issues/11575)

**Other**

* Gateway Helm chart renders invalid gravitee.yml when Hazelcast cluster and Redis distributed sync are enabled [#11583](https://github.com/gravitee-io/issues/issues/11583)

</details>

