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
  
## Gravitee API Management 4.4.0 - June 27, 2024

<details>

<summary>Bug Fixes</summary>

**Gateway**

* Error in the gateway when upgrading connection from http1.1 to http2 [#9757](https://github.com/gravitee-io/issues/issues/9757)
* Socket.io disconnect/reconnect latency [#9766](https://github.com/gravitee-io/issues/issues/9766)

**Management API**

* Pushing an API with API Designer fails [#9761](https://github.com/gravitee-io/issues/issues/9761)
* Inheritance of a V2 API endpoint configuration is not set when importing an OpenAPI spec [#9775](https://github.com/gravitee-io/issues/issues/9775)

**Console**

* Application analytics view logs navigation with filters [#9762](https://github.com/gravitee-io/issues/issues/9762)
* Login via OIDC on Management Console not possible [#9769](https://github.com/gravitee-io/issues/issues/9769)
* Transfer ownership to group shows as option for applications [#9774](https://github.com/gravitee-io/issues/issues/9774)
* Endpoint configuration enable proxy setup just after creation of endpoint [#9780](https://github.com/gravitee-io/issues/issues/9780)
* Filter on 208 status code not available [#9784](https://github.com/gravitee-io/issues/issues/9784)
* IDP Logout does not contain the correct subpath for console. [#9786](https://github.com/gravitee-io/issues/issues/9786)
* Display issues in token generation modal [#9793](https://github.com/gravitee-io/issues/issues/9793)
* In some cases it is difficult to view the configuration in the history menu. [#9800](https://github.com/gravitee-io/issues/issues/9800)

**Portal**

* Current portal incorrectly handles case where API description is "null" [#9785](https://github.com/gravitee-io/issues/issues/9785)
* Documentation too slow [#9788](https://github.com/gravitee-io/issues/issues/9788)

**Other**

* \[gravitee-policy-json-validation] v4 Policy Studio UI doesn't support multi-line values [#9799](https://github.com/gravitee-io/issues/issues/9799)

</details>

<details>

<summary>Improvements</summary>

**Other**

* \[gravitee-policy-groovy] Have access to the binary value of a message content [#9767](https://github.com/gravitee-io/issues/issues/9767)
* \[gravitee-endpoint-kafka] Add a option on kafka endpoint to remove Confluent Wire format header [#9795](https://github.com/gravitee-io/issues/issues/9795)

</details>


