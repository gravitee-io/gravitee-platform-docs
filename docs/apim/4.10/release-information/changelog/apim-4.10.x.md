# APIM 4.10.x

## Gravitee API Management 4.10.6 - February 14, 2026
<details>

<summary>Bug Fixes</summary>

**Other**

* Automatic cleanup failure in commands table due to missing expired_at values [#11136](https://github.com/gravitee-io/issues/issues/11136)
  * Once this version applied, you should consider removing commands with null `expiredAt` attribute.  
</details>


 
## Gravitee API Management 4.10.5 - February 13, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* \[Protocol Mediation] subscription is not available in EL during PUBLISH and SUBSCRIBE phase [#11101](https://github.com/gravitee-io/issues/issues/11101)
* Error 503 and Thread Blocked from weighted_round_robin  [#11132](https://github.com/gravitee-io/issues/issues/11132)
* Debug Mode does not work with OAuth Plan on v4 APIs [#11142](https://github.com/gravitee-io/issues/issues/11142)
* Gateway - Secrets with long content  [#11144](https://github.com/gravitee-io/issues/issues/11144)
* LLM Proxy API with Gemini: function_response.response must be a JSON object but non-object values are sent as-is [#11147](https://github.com/gravitee-io/issues/issues/11147)
* LLM Proxy seems to add a fixed 30 seconds to the response time [#11160](https://github.com/gravitee-io/issues/issues/11160)

**Management API**

* Multiple PRIMARY_OWNERs after "Transfer Ownership" [#11045](https://github.com/gravitee-io/issues/issues/11045)
* Http Client Common Configuration Regression [#11159](https://github.com/gravitee-io/issues/issues/11159)

**Console**

* Missing license banner incorrectly show with a license containing only "agent-mesh" pack [#11127](https://github.com/gravitee-io/issues/issues/11127)
* Permission Denied on IPV4_ONLY=true [#11130](https://github.com/gravitee-io/issues/issues/11130)

**Portal**

* Portal-Next: Portal Navigation Items returning 401 for anon user [#11139](https://github.com/gravitee-io/issues/issues/11139)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Request response times spike when health checks are performed [#11141](https://github.com/gravitee-io/issues/issues/11141)

**Other**

* \[gravitee-policy-callout-http] Allow to evaluate variables as Object [#11137](https://github.com/gravitee-io/issues/issues/11137)

</details>


 
## Gravitee API Management 4.10.4 - February 4, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Error when request of vendor comes with X-Forwarded Header [#11097](https://github.com/gravitee-io/issues/issues/11097)

**Management API**

* Re: Unable to view log of API unless Instance READ permission is added to API Publisher [#11051](https://github.com/gravitee-io/issues/issues/11051)
* API promotion issue [#11117](https://github.com/gravitee-io/issues/issues/11117)

**Console**

* Re: Unable to view log of API unless Instance READ permission is added to API Publisher [#11051](https://github.com/gravitee-io/issues/issues/11051)

**Portal**

* Portal-Next: Unable to confirm user account [#11111](https://github.com/gravitee-io/issues/issues/11111)

**Other**

* \[Kafka Gateway] Azure Service Bus fails with higher ApiVersions [#11109](https://github.com/gravitee-io/issues/issues/11109)
* \[Kafka Gateway] Bad ApiVersions when gateway doesn't supports the min version of an api key [#11118](https://github.com/gravitee-io/issues/issues/11118)

</details>


 
## Gravitee API Management 4.10.3 - January 30, 2026
<details>

<summary>Bug Fixes</summary>

**Management API**

* Impossible to add a new group member [#11050](https://github.com/gravitee-io/issues/issues/11050)
* Prevent multiple primary owners through ownership transfer [#11102](https://github.com/gravitee-io/issues/issues/11102)

**Portal**

* Error while creating a backend-to-backend application in next gen portal [#11084](https://github.com/gravitee-io/issues/issues/11084)

**Other**

* SSL enforcement policy issue [#11009](https://github.com/gravitee-io/issues/issues/11009)
* Group Management follow-up (still broken in some places) [#11042](https://github.com/gravitee-io/issues/issues/11042)
* \[Kafka Gateway] Side effects on upstream connection when EL is used to configure SASL [#11103](https://github.com/gravitee-io/issues/issues/11103)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* \[Perf] Improve APIM management API overall performance [#11088](https://github.com/gravitee-io/issues/issues/11088)

**Console**

* \[Policy Studio] Improve entrypoint / endpoint UI [#11059](https://github.com/gravitee-io/issues/issues/11059)
* Support outputSchema and annotation from recent MCP spec for MCP Tool Server [#11083](https://github.com/gravitee-io/issues/issues/11083)

</details>



## Gravitee API Management 4.10.2 - January 22, 2026

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Double / when in the called url when using Service discovery plugin [#11076](https://github.com/gravitee-io/issues/issues/11076)

**Console**

* Change default color order of analytics dashboard [#11080](https://github.com/gravitee-io/issues/issues/11080)

**Portal**

* \[PORTAL] Filtering Problem [#11028](https://github.com/gravitee-io/issues/issues/11028)

**Other**

* Kafka gateway fails when older version of ApiVersions is provided [#11078](https://github.com/gravitee-io/issues/issues/11078)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* JAVA\_OPTS displays password parameters in gateway logs [#11073](https://github.com/gravitee-io/issues/issues/11073)

**Management API**

* JAVA\_OPTS displays password parameters in gateway logs [#11073](https://github.com/gravitee-io/issues/issues/11073)

</details>

## Gravitee API Management 4.10.1 - January 19, 2026

<details>

<summary>Bug Fixes</summary>

**Other**

* User is unable to use guard rails policy with debug mode [#11070](https://github.com/gravitee-io/issues/issues/11070)
* Gateway doesn't support older kafka versions [#11071](https://github.com/gravitee-io/issues/issues/11071)

</details>
