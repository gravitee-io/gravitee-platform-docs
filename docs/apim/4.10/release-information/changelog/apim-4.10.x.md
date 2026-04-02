# APIM 4.10.x
 
## Gravitee API Management 4.10.10 - April 2, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* No error message for V2 API without V4 emulation in 4.9.x [#11126](https://github.com/gravitee-io/issues/issues/11126)

**Management API**

* Unable to import path mapping from swagger document [#10806](https://github.com/gravitee-io/issues/issues/10806)
* No error message for V2 API without V4 emulation in 4.9.x [#11126](https://github.com/gravitee-io/issues/issues/11126)
* Unable to resend or retrigger expired sign-up confirmation links [#11295](https://github.com/gravitee-io/issues/issues/11295)
* Error when deleting an API with pages [#11308](https://github.com/gravitee-io/issues/issues/11308)

**Console**

* No error message for V2 API without V4 emulation in 4.9.x [#11126](https://github.com/gravitee-io/issues/issues/11126)
* Unable to reset the password [#11289](https://github.com/gravitee-io/issues/issues/11289)

</details>

<details>

<summary>Improvements</summary>

**Other**

* PostgreSQL character limit of 256 for flows [#11087](https://github.com/gravitee-io/issues/issues/11087)
* Update IP Filtering policy documentation in  [#11251](https://github.com/gravitee-io/issues/issues/11251)

</details>


 
## Gravitee API Management 4.10.9 - March 27, 2026
<details>

<summary>Bug Fixes</summary>

**Gateway**

* SSL enforcement policy will return a 403 if if the SSL connection is terminated at the ingress level [#11234](https://github.com/gravitee-io/issues/issues/11234)
* Dynamic dictionary not deployed when environment is not the default one [#11236](https://github.com/gravitee-io/issues/issues/11236)
* JWT plans can only have one subscription transfer [#11246](https://github.com/gravitee-io/issues/issues/11246)
* Duplicate traceparent header [#11248](https://github.com/gravitee-io/issues/issues/11248)
* The Health Check of the API V4 is not working as expected with tenant [#11275](https://github.com/gravitee-io/issues/issues/11275)
* Secret resolution failure in SPG when combined with multiple policies [#11279](https://github.com/gravitee-io/issues/issues/11279)

**Management API**

* Promotion Button in UI Yields Parsing Error [#11277](https://github.com/gravitee-io/issues/issues/11277)

**Console**

* Missing fields when creating an alert [#10802](https://github.com/gravitee-io/issues/issues/10802)
* Locations in Admin Console time out due to requests being sent to old Groups API Endpoint where pagination is not implemented [#10843](https://github.com/gravitee-io/issues/issues/10843)
* \[Logging] API Level logs missing details if one of the checkbox is unchecked [#11116](https://github.com/gravitee-io/issues/issues/11116)
* Error when importing an API from OpenAPI Spec & "Add OpenAPI Specification Validation" enabled [#11128](https://github.com/gravitee-io/issues/issues/11128)
* Not able search/filter logs by path [#11255](https://github.com/gravitee-io/issues/issues/11255)
* v4 API promotions are stuck in a pending state [#11281](https://github.com/gravitee-io/issues/issues/11281)

**Portal**

* Portal-Next: MCP functionalities no longer shown [#11187](https://github.com/gravitee-io/issues/issues/11187)

**Other**

* Bootstrap URL for Kafka DLQ endpoint does not support Expression Language [#10906](https://github.com/gravitee-io/issues/issues/10906)
* Application menu not showing up on first login [#10951](https://github.com/gravitee-io/issues/issues/10951)
* Promotion request is not found in Audit of the target environment. [#11065](https://github.com/gravitee-io/issues/issues/11065)
* json-validation policy error key [#11152](https://github.com/gravitee-io/issues/issues/11152)
* Agent Mesh - Generate Tools from OpenAPI [#11165](https://github.com/gravitee-io/issues/issues/11165)
* \[V4 Emulation] IllegalStateException: HTTP/2 streams failing due to missing Content-Length validation [#11191](https://github.com/gravitee-io/issues/issues/11191)
* FreeMarker template error in v4-message-log.ftl when Kafka metadata contains byte\[] [#11220](https://github.com/gravitee-io/issues/issues/11220)
* OpenAPI Specification Validation Policy - Validation errors [#11223](https://github.com/gravitee-io/issues/issues/11223)
* MCP Tool Generation: Operation descriptions and business rules are missing from generated tools [#11226](https://github.com/gravitee-io/issues/issues/11226)
* Detaching an API looses API context after confirmation [#11239](https://github.com/gravitee-io/issues/issues/11239)
* Kafka gateways is throwing recurrent "Thread blocked" errors [#11242](https://github.com/gravitee-io/issues/issues/11242)
* Changing plan order removes the plan flows [#11247](https://github.com/gravitee-io/issues/issues/11247)
* OAuth2 token acquisition failure is silently swallowed [#11250](https://github.com/gravitee-io/issues/issues/11250)
* Webhook Logs toggle not updated after save/publish [#11257](https://github.com/gravitee-io/issues/issues/11257)
* Once I migrate certain V2 APIs to V4, they disappear from the list (/apis) in the UI [#11268](https://github.com/gravitee-io/issues/issues/11268)
* Migration to v4 engine : flows on deprecated plans not visible anymore [#11269](https://github.com/gravitee-io/issues/issues/11269)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Api Categories exported by IDs instead of names [#10944](https://github.com/gravitee-io/issues/issues/10944)
* Allow for larger values in APIM Dictionary properties [#11047](https://github.com/gravitee-io/issues/issues/11047)
* \[gravitee-policy-aws-lambda] Unexpected Retry and Duplicate Invocation of AWS Lambda via Gravitee API Gateway [#11096](https://github.com/gravitee-io/issues/issues/11096)
* "Thread blocked" error received when invalid creadentials set for Elastic Search [#11184](https://github.com/gravitee-io/issues/issues/11184)
* Support client_secret_basic authentication for OAuth2 token endpoint [#11249](https://github.com/gravitee-io/issues/issues/11249)

</details>


 
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
