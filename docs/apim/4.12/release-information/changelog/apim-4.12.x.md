---
hidden: false
noIndex: false
---

# APIM 4.12.x
 
## Gravitee API Management 4.12.10 - July 21, 2026
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

