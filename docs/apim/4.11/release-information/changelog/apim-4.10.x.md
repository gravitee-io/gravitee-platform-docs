# APIM 4.10.x
 
## Gravitee API Management 4.10.8 - March 12, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Not able to reference kubernetes secret in Sharedpolicy group resource and then use it in api for use case such as Oauth server authentication [#11041](https://github.com/gravitee-io/issues/issues/11041)
* Missing node_health prometheus metric with 4.9.11 [#11095](https://github.com/gravitee-io/issues/issues/11095)
* Keystore watch stop working after KeyStore failed to load [#11121](https://github.com/gravitee-io/issues/issues/11121)

**Management API**

* User Attributes Not Resolved in Mail Templates [#11207](https://github.com/gravitee-io/issues/issues/11207)

**Console**

* Entrypoints mapping display bug. [#11053](https://github.com/gravitee-io/issues/issues/11053)
* For large number of requests Min Response Time says: No data to display [#11086](https://github.com/gravitee-io/issues/issues/11086)
* Dynamic property - Fix the help message under cron expression [#11140](https://github.com/gravitee-io/issues/issues/11140)
* Broken 'Open log settings' link in V4 Protocol Mediation API log details [#11167](https://github.com/gravitee-io/issues/issues/11167)
* Dynamic properties not getting saved in 4.10.X [#11175](https://github.com/gravitee-io/issues/issues/11175)
* Custom statistics on the User-Agent [#11203](https://github.com/gravitee-io/issues/issues/11203)

**Portal**

* Button "back to category" disappears in dev portal [#11204](https://github.com/gravitee-io/issues/issues/11204)
* Ui bug in developer portal [#11214](https://github.com/gravitee-io/issues/issues/11214)

**Other**

* Kafka OAUTHBEARER reconnection not triggered by the Kafka Client with JWT Plan [#10491](https://github.com/gravitee-io/issues/issues/10491)
* 404 (Not Found) requests not visible in Console Analytics despite correct configuration [#11014](https://github.com/gravitee-io/issues/issues/11014)
* Azure OpenAI model name mismatch prevents LLM cost metrics from being sent [#11227](https://github.com/gravitee-io/issues/issues/11227)
* JSON Web Token policy always returns fails to validate token [#11233](https://github.com/gravitee-io/issues/issues/11233)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* Intermittent 500 Error during API Creation: primaryOwner.notFound [#11229](https://github.com/gravitee-io/issues/issues/11229)

**Other**

* Support EL secret for authentication in LLM Proxy endpoints [#11198](https://github.com/gravitee-io/issues/issues/11198)

</details>


 
## Gravitee API Management 4.10.7 - February 27, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Failover retries leak endpoint query parameters across attempts in HTTP proxy connector [#11164](https://github.com/gravitee-io/issues/issues/11164)
* Gateway cannot auto-recover if Elasticsearch goes down and then comes back online [#11176](https://github.com/gravitee-io/issues/issues/11176)
* Cannot override cloud client http version [#11186](https://github.com/gravitee-io/issues/issues/11186)
* ECS Logging format support [#11189](https://github.com/gravitee-io/issues/issues/11189)

**Management API**

* The mAPI is unreachable when a connection cannot be made to Cloud [#10307](https://github.com/gravitee-io/issues/issues/10307)
* V4 Migration: 400 Error on endpoint updates when 'System Proxy' is enabled in V2 [#11113](https://github.com/gravitee-io/issues/issues/11113)
* Cannot override cloud client http version [#11186](https://github.com/gravitee-io/issues/issues/11186)

**Console**

* \[UI Bug] LDAP Resource "User search base" field auto-populates with default value on edit [#11072](https://github.com/gravitee-io/issues/issues/11072)

**Portal**

* Portal-Next: AsyncAPI rendering not working [#11119](https://github.com/gravitee-io/issues/issues/11119)
* API Catalog API Visibility [#11155](https://github.com/gravitee-io/issues/issues/11155)

**Other**

* Promotion requests accepted from the main dashboard are not auto refreshed [#11062](https://github.com/gravitee-io/issues/issues/11062)
* APIs that do not pass the security chain are not shown in the new v4 analytics dashboard [#11131](https://github.com/gravitee-io/issues/issues/11131)
* Lack of resources configuration validation and sanitization for Native APIs [#11161](https://github.com/gravitee-io/issues/issues/11161)
* \[mcp-acl] policy does not return valid JSON-RPC response in case of error [#11192](https://github.com/gravitee-io/issues/issues/11192)
* Assign content policy doesn't support message.topic for kafka native API [#11194](https://github.com/gravitee-io/issues/issues/11194)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Fix performance degradation in 4.9 compared to 4.8  [#11211](https://github.com/gravitee-io/issues/issues/11211)
* Make 401 Error Details Available in Response [#11212](https://github.com/gravitee-io/issues/issues/11212)

**Console**

* API Mgmt Management Console task list takes too long to load [#11049](https://github.com/gravitee-io/issues/issues/11049)
* Debug Mode Enhancement: Increase Timeout & Implement Long-Poll UI [#11180](https://github.com/gravitee-io/issues/issues/11180)

**Helm Charts**

* Make 401 Error Details Available in Response [#11212](https://github.com/gravitee-io/issues/issues/11212)

**Other**
* OpenAPI Validation Policy fails with OAS 3.1 discriminator schemas [#10763](https://github.com/gravitee-io/issues/issues/10763)

</details>



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
