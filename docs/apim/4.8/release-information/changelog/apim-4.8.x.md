# APIM 4.8.x
 
## Gravitee API Management 4.8.3 - August 1, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Heap memory possible leakage due to missing equals and hashcode methods on all fields. [#10701](https://github.com/gravitee-io/issues/issues/10701)

**Management API**

* Groups Mappings do not work if no Default Role is selected to API and Application [#10271](https://github.com/gravitee-io/issues/issues/10271)
* Sharding Tag Persists on API preview After Deletion [#10626](https://github.com/gravitee-io/issues/issues/10626)
* Unable to search by label for v4 APIs [#10671](https://github.com/gravitee-io/issues/issues/10671)
* If we send null for the groups field the value should not be updated in DB in any scenario (PO is a user, PO is a group, etc) [#10686](https://github.com/gravitee-io/issues/issues/10686)

**Console**

* The error key CLIENT_ABORTED_DURING_RESPONSE_ERROR is not present in the console UI. [#10683](https://github.com/gravitee-io/issues/issues/10683)

**Portal**

*  Portal Try it Out feature taking a long time to load [#10595](https://github.com/gravitee-io/issues/issues/10595)
* Openapi contracts with binary examples can not be read by the dev portal  [#10639](https://github.com/gravitee-io/issues/issues/10639)

**Other**

* JDBC Error in Gravitee when querying large number of applications using IN clause  [#10496](https://github.com/gravitee-io/issues/issues/10496)
* Console : Image Not Fitting Avatar Due to Aspect Ratio [#10649](https://github.com/gravitee-io/issues/issues/10649)
* Unable to modify set/replace/append headers in the UI for the Transform Headers policy [#10655](https://github.com/gravitee-io/issues/issues/10655)
* Unable to access Logs details [#10695](https://github.com/gravitee-io/issues/issues/10695)

</details>

<details>

<summary>Improvements</summary>

**Other**

* Disable cleanup events and audits services by default [#10708](https://github.com/gravitee-io/issues/issues/10708)

</details>


 
## Gravitee API Management 4.8.2 - July 18, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Traceparent HTTP header is not available in the policy chain [#10511](https://github.com/gravitee-io/issues/issues/10511)
* Kafka TLS keystore loaded too many times [#10646](https://github.com/gravitee-io/issues/issues/10646)

**Management API**

* Wrong count in the analytics of API v4 [#10604](https://github.com/gravitee-io/issues/issues/10604)
* Entrypoint cannot be found error when using tags [#10667](https://github.com/gravitee-io/issues/issues/10667)

**Console**

* Identity provider roles mapping UI bug [#10503](https://github.com/gravitee-io/issues/issues/10503)
* Instances of calling the groups endpoint on create V2 API page time out when a large number of groups exist [#10603](https://github.com/gravitee-io/issues/issues/10603)

**Other**

* Mock policy is not generated if the openAPI spec data uses a type of string and format of date-time [#10619](https://github.com/gravitee-io/issues/issues/10619)
* \[Kafka Offloading Policy] Large Payloads Support [#10674](https://github.com/gravitee-io/issues/issues/10674)

</details>



## Gravitee API Management 4.8.1 - July 7, 2025

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Hardcoded value for health check in 4.7 versions and above in docker images ( for both gateway and mapi ) [#10644](https://github.com/gravitee-io/issues/issues/10644)

**Management API**

* Subscriptions in the subscriptions tab of an application seem to only show the first 10 item [#10529](https://github.com/gravitee-io/issues/issues/10529)
* Users with both group inheritance and individual access to applications are limited in which applications to which they can subscribe [#10601](https://github.com/gravitee-io/issues/issues/10601)
* Hardcoded value for health check in 4.7 versions and above in docker images ( for both gateway and mapi ) [#10644](https://github.com/gravitee-io/issues/issues/10644)
* Debug mode for v4 proxy apis returns a 500 response [#10648](https://github.com/gravitee-io/issues/issues/10648)
* Using jsonPath in Assign Attributes policy prevents sending transformed body in HTTP Callout policy

**Console**

* Wrong display when adding a user to a group [#10558](https://github.com/gravitee-io/issues/issues/10558)
* Prevent API Modification for Unauthorized API Users [#10594](https://github.com/gravitee-io/issues/issues/10594)

**Portal**

* Subscriptions in the subscriptions tab of an application seem to only show the first 10 item [#10529](https://github.com/gravitee-io/issues/issues/10529)

**Other**

* Unable to add a group to an existing user using console [#10378](https://github.com/gravitee-io/issues/issues/10378)
* Console : Categories Page doesn't show updated image for any category [#10523](https://github.com/gravitee-io/issues/issues/10523)
* Primary owner Group should not be removed from an API [#10580](https://github.com/gravitee-io/issues/issues/10580)
* Custom policy depending on gravitee-resource-oauth2-provider-generic [#10620](https://github.com/gravitee-io/issues/issues/10620)
* Portal Theme Settings : UNABLE to change Theme color [#10647](https://github.com/gravitee-io/issues/issues/10647)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* Enable multi-tenant support for Dictionaries by default [#10637](https://github.com/gravitee-io/issues/issues/10637)

**Other**

* Increase character limit of condition field in flow\_selectors table [#10560](https://github.com/gravitee-io/issues/issues/10560)

</details>
