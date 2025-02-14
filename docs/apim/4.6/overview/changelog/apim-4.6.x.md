---
description: >-
  This page contains the changelog entries for APIM 4.6.x and any future patch
  APIM 4.6.x releases
---

# APIM 4.6.x
 
## Gravitee API Management 4.6.4 - February 14, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* \[Kafka Gateway] Make the ACL policy can be used before a TopicMapping Policy [#10280](https://github.com/gravitee-io/issues/issues/10280)
* \[Kafka Gateway] ACL policy fix various bugs like topic list visibility [#10335](https://github.com/gravitee-io/issues/issues/10335)
* Thread block while deploying APIs with very long read timeouts set in the Endpoints configuration [#10340](https://github.com/gravitee-io/issues/issues/10340)

**Management API**

* 4.6:Webhook policy flow cannot be saved [#10342](https://github.com/gravitee-io/issues/issues/10342)

**Portal**

* Public APIs not accessible to anonymous users through categories in the portal [#10274](https://github.com/gravitee-io/issues/issues/10274)

**Helm Charts**

* \[Helm charts] kafka configuration is missing some fields [#10330](https://github.com/gravitee-io/issues/issues/10330)
* Typo in values.yaml and missing Helm chart mapping for gravitee.yml [#10343](https://github.com/gravitee-io/issues/issues/10343)

**Other**

* Can't see Logs for JWT enabled API's in API Management portal (401 response only) [#10076](https://github.com/gravitee-io/issues/issues/10076)

</details>

<details>

<summary>Improvements</summary>

**Gateway**

* \[Kafka Gateway] Allow to customize the rewritten broker domain [#10337](https://github.com/gravitee-io/issues/issues/10337)

</details>


 
## Gravitee API Management 4.6.3 - February 7, 2025

**Technical release**

No fixes or features have been added.
 
## Gravitee API Management 4.6.2 - January 31, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Repeating Error Eventually Causing Restarts [#10225](https://github.com/gravitee-io/issues/issues/10225)
* Kafka Gateway issue with confluent [#10321](https://github.com/gravitee-io/issues/issues/10321)

**Console**

* Missing "Add Member" Button in group settings [#10050](https://github.com/gravitee-io/issues/issues/10050)
* Application updates remove the picture  [#10302](https://github.com/gravitee-io/issues/issues/10302)

**Portal**

* Subscribing to an API with general condition page when creating an application returns a 404 [#10103](https://github.com/gravitee-io/issues/issues/10103)

**Helm Charts**

* Repeating Error Eventually Causing Restarts [#10225](https://github.com/gravitee-io/issues/issues/10225)

**Other**

* Changes needed to rpm packages [#9728](https://github.com/gravitee-io/issues/issues/9728)
* Reporter file in CSV format doesn't work [#10181](https://github.com/gravitee-io/issues/issues/10181)
* \[RPM upgrade] Lucene issue on upgrading from 4.4.9 to 4.5.0 [#10192](https://github.com/gravitee-io/issues/issues/10192)

</details>


 
## Gravitee API Management 4.6.1 - January 24, 2025
<details>

<summary>Bug Fixes</summary>

**Gateway**

* Dictionaries stop working [#10286](https://github.com/gravitee-io/issues/issues/10286)
* Problem with request body size above 2MB when using V4 Engine [#10291](https://github.com/gravitee-io/issues/issues/10291)
* Fix issue with a iokafka python client [#10303](https://github.com/gravitee-io/issues/issues/10303)

**Console**

* Path mapping does not work with hyphen [#10289](https://github.com/gravitee-io/issues/issues/10289)

</details>



