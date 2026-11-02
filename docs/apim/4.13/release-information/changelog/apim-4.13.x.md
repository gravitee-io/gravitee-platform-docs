---
hidden: false
noIndex: false
description: The API Management 4.13 changelog lists the bug fixes in each patch release, with a link to the GitHub issue for every fix. Find the fixes in your release.
---

# APIM 4.13.x
 
## Gravitee API Management 4.13.2 - November 2, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* HTTP fetcher, Kafka console proxy and debug mode leak one Vert.x HttpClient per call [#11974](https://github.com/gravitee-io/issues/issues/11974)
* SSE event with multiline data not well formatted [#12001](https://github.com/gravitee-io/issues/issues/12001)
* API Traffic entrypoint response status and header are wrongly captured [#12002](https://github.com/gravitee-io/issues/issues/12002)

**Management API**

* MCP entrypoint: form-urlencoded bodies sent as JSON, conversion ignores form bodies and required request bodies, backend errors returned as successful results [#11950](https://github.com/gravitee-io/issues/issues/11950)

**Console**

* MCP entrypoint: form-urlencoded bodies sent as JSON, conversion ignores form bodies and required request bodies, backend errors returned as successful results [#11950](https://github.com/gravitee-io/issues/issues/11950)
* Custom/shared API key fields sometimes missing when creation a subscription from API [#11975](https://github.com/gravitee-io/issues/issues/11975)

**Event Stream Management**

* Kafka Gateway accepts client connections with no upper limit and OOMs into a cascade [#11995](https://github.com/gravitee-io/issues/issues/11995)
* Native Kafka gateway gives the load balancer no signal to stop routing new connections to a pod near capacity [#11996](https://github.com/gravitee-io/issues/issues/11996)

**AI Agent Management**

* MCP Studio: passthrough upstream auth doesn't forward the caller's token to HTTP tool backends [#11905](https://github.com/gravitee-io/issues/issues/11905)
* Classic console: saving an MCP Studio's HTTP tool endpoint deletes all its tools [#11906](https://github.com/gravitee-io/issues/issues/11906)
* Gamma Studio: Passthrough is missing for HTTP tool sources and Save tools clears it [#12011](https://github.com/gravitee-io/issues/issues/12011)

**Other**

* V4→V2 rollback refused by the plan check leaves the API half-converted, and the Console API list returns 500 for the whole environment [#11931](https://github.com/gravitee-io/issues/issues/11931)
* v4 HTTP proxy: a failover retry on a failure-condition match drops the request path, and the retried attempt is sent to next endpoint's bare target [#11959](https://github.com/gravitee-io/issues/issues/11959)
* subscription - PAUSED, RESUMED and CLOSED events do not carry the subscription id [#11973](https://github.com/gravitee-io/issues/issues/11973)
* Async rate-limit flush fails with Redis timeouts when many keys are pending [#11980](https://github.com/gravitee-io/issues/issues/11980)
* \[4.13] Management API returns HTTP 500 “Unknown dialect” when importing a v4 API that uses a policy whose schema declares JSON Schema 2019-09 [#11988](https://github.com/gravitee-io/issues/issues/11988)
* Policy Studio spins forever on MCP Studio APIs because mcp-studio is missing from the plugin list [#11999](https://github.com/gravitee-io/issues/issues/11999)
* Group: Primary_owner role transfer doesn't work [#12005](https://github.com/gravitee-io/issues/issues/12005)
* Dead Letter Queue (DLQ) not working for Webhook API [#12009](https://github.com/gravitee-io/issues/issues/12009)

</details>


 
## Gravitee API Management 4.13.1 - October 23, 2026
<details>

<summary>Bug Fixes</summary>

**Other**

* DCR application_type case-sensitive comparison causes WEB/NATIVE/BROWSER apps to be classified as SERVICE [#11230](https://github.com/gravitee-io/issues/issues/11230)

</details>


