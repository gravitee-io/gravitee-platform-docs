---
description: >-
  This page contains the changelog entries for APIM 4.5.x and any future patch
  APIM 4.5.x releases
---

# APIM 4.5.x

## Gravitee API Management 4.5.2 - November 5, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Inconsistent application of validateSubscription flag [#10120](https://github.com/gravitee-io/issues/issues/10120)
* Sync process failed if subscription exists without the linked API [#10140](https://github.com/gravitee-io/issues/issues/10140)

**Management API**

* Page revisions are still present when the associated API is deleted [#10039](https://github.com/gravitee-io/issues/issues/10039)
* API webhook notifier is not working for subscriptions [#10056](https://github.com/gravitee-io/issues/issues/10056)
* Alert Templates are always created in default environment [#10126](https://github.com/gravitee-io/issues/issues/10126)
* Updating the application generates an exception. [#10130](https://github.com/gravitee-io/issues/issues/10130)

**Console**

* Code blocks and long strings of text cause overflow of documentation text in the new dev portal [#10048](https://github.com/gravitee-io/issues/issues/10048)

**Other**

* Gateways can not reconnect to the bridge mapi [#10101](https://github.com/gravitee-io/issues/issues/10101)
* \[gravitee-policy-jwt] Complete gateway disruption occurred in retrieving JWT public keys after startup under a heavy load of API calls [#10119](https://github.com/gravitee-io/issues/issues/10119)

</details>

## Gravitee API Management 4.5.1 - October 24, 2024

<details>

<summary>Bug Fixes</summary>

**Management API**

* Dictionaries not deployed after migration from 3.20.x to 4.x [#10026](https://github.com/gravitee-io/issues/issues/10026)
* User with environment role is not able to create notifications [#10068](https://github.com/gravitee-io/issues/issues/10068)

**Console**

* Unable to delete Cors Allow-Origin URL [#9765](https://github.com/gravitee-io/issues/issues/9765)
* Error on sharding tags page refresh [#10067](https://github.com/gravitee-io/issues/issues/10067)
* Rollback from history removes groups of users from API [#10074](https://github.com/gravitee-io/issues/issues/10074)
* Upgrade nginx image to 1.27.2 [#10116](https://github.com/gravitee-io/issues/issues/10116)

**Portal**

* Swagger Documentation not showing in portal [#9946](https://github.com/gravitee-io/issues/issues/9946)
* Upgrade nginx image to 1.27.2 [#10116](https://github.com/gravitee-io/issues/issues/10116)

**Helm Charts**

* Set the HaProxy.ProxyProtocol with the Helm chart [#10027](https://github.com/gravitee-io/issues/issues/10027)

**Other**

* \[JDBC] Unable to create federation [#10107](https://github.com/gravitee-io/issues/issues/10107)

</details>

## Gravitee API Management 4.5.0 - October 10, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Transfer subscription does not use new plan when V4 emulation is disabled [#10047](https://github.com/gravitee-io/issues/issues/10047)
* \[3.20.X and 4.4.X] DNS Resolution fails for hosts having more than 30 A records [#10051](https://github.com/gravitee-io/issues/issues/10051)
* \[Gateway Distributed Sync] Properly differentiate v2 from v4 API events [#10055](https://github.com/gravitee-io/issues/issues/10055)
* \[gravitee-node] Gravitee metrics return NaN [#10070](https://github.com/gravitee-io/issues/issues/10070)

**Management API**

* Issue on permissions of the ORGANIZATION_USER role [#10040](https://github.com/gravitee-io/issues/issues/10040)

**Console**

* Not able to see API events in Dashboard [#10018](https://github.com/gravitee-io/issues/issues/10018)
* Analytics dashboard filtered become empty when a tenant is selected [#10019](https://github.com/gravitee-io/issues/issues/10019)
* Redirect user to login screen when JWT token has expired [#10029](https://github.com/gravitee-io/issues/issues/10029)
* Button color UI bug [#10035](https://github.com/gravitee-io/issues/issues/10035)

**Portal**

* Users without admin or API access cannot view application API keys in the new dev portal [#10014](https://github.com/gravitee-io/issues/issues/10014)
* Search bar not sorting results properly on portal for API [#10075](https://github.com/gravitee-io/issues/issues/10075)

**Helm Charts**

* Add serviceAccount in helm chart  [#10057](https://github.com/gravitee-io/issues/issues/10057)
* Update values.yml to Values.gateway.ratelimit.management.http.url  [#10091](https://github.com/gravitee-io/issues/issues/10091)

**Other**

* \[gravitee-policy-data-logging-masking] DLM policies will not allow the DataDog Reporter to forward logs to DataDog if a property is not found [#10044](https://github.com/gravitee-io/issues/issues/10044)

</details>
