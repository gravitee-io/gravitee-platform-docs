---
description: >-
  This page contains the changelog entries for APIM 4.4.x and any future patch
  APIM 4.4.x releases
---

# APIM 4.4.x
 
## Gravitee API Management 4.4.1 - June 27, 2024
<details>

<summary>Bug Fixes</summary>

**Gateway**

* 500 Internal server error when logs enabled [#9719](https://github.com/gravitee-io/issues/issues/9719)
* Enabled Logging with condition does not work properly [#9756](https://github.com/gravitee-io/issues/issues/9756)

**Management API**

* Override an email template with multiple REST API [#9445](https://github.com/gravitee-io/issues/issues/9445)
* Cannot Create Local User (no email to set password) [#9680](https://github.com/gravitee-io/issues/issues/9680)
* Error in Gravitee OpenAPI spec [#9711](https://github.com/gravitee-io/issues/issues/9711)
* Improve V4 analytics performance [#9810](https://github.com/gravitee-io/issues/issues/9810)
* Unable to access portal from the redirection link [#9815](https://github.com/gravitee-io/issues/issues/9815)
* \[Multi-tenant] The link in the user creation email is invalid [#9816](https://github.com/gravitee-io/issues/issues/9816)
* \[Multi-tenant] The link in the subscription email is invalid [#9817](https://github.com/gravitee-io/issues/issues/9817)

**Console**

* Correct API properties Expression Language for v4 APIs [#9694](https://github.com/gravitee-io/issues/issues/9694)
* When updating a service account email through API, no mail validation is performed [#9709](https://github.com/gravitee-io/issues/issues/9709)
* Enabled Logging with condition does not work properly [#9756](https://github.com/gravitee-io/issues/issues/9756)

**Helm Charts**

* Missing hazelcast dependency in updater mode [#9809](https://github.com/gravitee-io/issues/issues/9809)

**Other**

* \[gravitee-policy-ipfiltering] CIDR block /32 (single IP) not working in the IP Filtering Policy [#9602](https://github.com/gravitee-io/issues/issues/9602)
* \[gravitee-policy-jwt] 500 error on jwt plan with GATEWAY_KEYS when using  "Emulate v4 engine" [#9693](https://github.com/gravitee-io/issues/issues/9693)
* \[MongoDb] Upgraders should use prefix for collection names [#9807](https://github.com/gravitee-io/issues/issues/9807)
* \[JDBC] Unable to search subscription with Postgresql [#9808](https://github.com/gravitee-io/issues/issues/9808)
* \[MongoDb] Api keys do not have the environment field [#9811](https://github.com/gravitee-io/issues/issues/9811)
* \[MongoDb] Subscription environment is erase when updating a subscription [#9812](https://github.com/gravitee-io/issues/issues/9812)

</details>

<details>

<summary>Improvements</summary>

**Management API**

* The name of API/Application/Plan is not given in list of API's subscriptions [#9679](https://github.com/gravitee-io/issues/issues/9679)

**Other**

* \[gravitee-policy-aws-lambda] Allow to dynamically configure AWS policy credentials [#9444](https://github.com/gravitee-io/issues/issues/9444)

</details>


