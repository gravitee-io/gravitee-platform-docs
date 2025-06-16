# GKO 4.4.x

## Gravitee Kubernetes Operator 4.4.30 - June 16, 2025

There is nothing new in version 4.4.30.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.4.29 - June 5, 2025

There is nothing new in version 4.4.29.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.4.28 - May 14, 2025
    
<details>
<summary>Bug fixes</summary>

  * mAPI throws exception an Application is created using GKO with empty pictureUrl [#10531](https://github.com/gravitee-io/issues/issues/10531)
</details>


## Gravitee Kubernetes Operator 4.4.27 - May 6, 2025
    
<details>
<summary>Bug fixes</summary>

  * mAPI throws exception an Application is created using GKO with empty pictureUrl [#10531](https://github.com/gravitee-io/issues/issues/10531)
</details>


## Gravitee Kubernetes Operator 4.4.26 - April 28, 2025

There is nothing new in version 4.4.26.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.4.25 - April 14, 2025
    
<details>
<summary>Bug fixes</summary>

  * v4 APIs created via GKO not displayed in assigned Category [#10448](https://github.com/gravitee-io/issues/issues/10448)
</details>


## Gravitee Kubernetes Operator 4.4.24 - April 8, 2025

There is nothing new in version 4.4.24.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.4.23 - March 28, 2025
    
<details>
<summary>Security</summary>

  * update module github.com/golang-jwt/jwt/v5 to v5.2.2 [#10452](https://github.com/gravitee-io/issues/issues/10452)
</details>


## Gravitee Kubernetes Operator 4.4.22 - March 17, 2025

There is nothing new in version 4.4.22.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.4.21 - March 6, 2025
    
<details>
<summary>Bug fixes</summary>

  * V4 API deletion happens without waiting for the plan to be deleted [#10376](https://github.com/gravitee-io/issues/issues/10376)
</details>


## Gravitee Kubernetes Operator 4.4.20 - February 17, 2025
    
<details>
<summary>Bug fixes</summary>

  * GKO v4 API CRD is missing the analytics tracing attribute [#10322](https://github.com/gravitee-io/issues/issues/10322)
</details>


## Gravitee Kubernetes Operator 4.4.19 - February 5, 2025

    
<details>
<summary>Bug fixes</summary>

  * API v2 CRD export generates bad format for headers [#10288](https://github.com/gravitee-io/issues/issues/10288)
</details>


## Gravitee Kubernetes Operator 4.4.18 - January 27, 2025
    
<details>
<summary>Bug fixes</summary>

  * RBAC creation is inconsistent for admission webhook when scope is not cluster [#10294](https://github.com/gravitee-io/issues/issues/10294)
  * Re-deploying an exported API CRD fails due to unknown metadata field [#10282](https://github.com/gravitee-io/issues/issues/10282)
</details>


<details>
<summary>Security</summary>

  * Webhook cluster role access should be narrowed down to resource names we use [#10296](https://github.com/gravitee-io/issues/issues/10296)
</details>


## Gravitee Kubernetes Operator 4.4.17 - January 17, 2025
    
<details>
<summary>Security</summary>

  * Update module golang.org/x/net to v0.33.0 [#10254](https://github.com/gravitee-io/issues/issues/10254)
</details>



## Gravitee Kubernetes Operator 4.4.16 - December 20, 2024

<details>
<summary>Bug fixes</summary>

  * Missing deprecated status in API definition for plans [#10248](https://github.com/gravitee-io/issues/issues/10248)
  * Application notifyMembers doesn't work [#10231](https://github.com/gravitee-io/issues/issues/10231)
  * Editable HTTP configuration when an API is managed by the operator [#10221](https://github.com/gravitee-io/issues/issues/10221)
</details>


## Gravitee Kubernetes Operator 4.4.15 - December 9, 2024
    
<details>
<summary>Bug fixes</summary>

  * Missing Key and Trust Store  fields in API Definition [#10215](https://github.com/gravitee-io/issues/issues/10215)
  * Template strings are not resolved for API Resources references [#10214](https://github.com/gravitee-io/issues/issues/10214)
  * Gateway throws NPE watching GKO configmaps [#10210](https://github.com/gravitee-io/issues/issues/10210)
</details>


## Gravitee Kubernetes Operator 4.4.14 - November 21, 2024
    
<details>
<summary>Bug fixes</summary>

  * API v2 CRD export cannot be applied when setting selection rules on plans [#10185](https://github.com/gravitee-io/issues/issues/10185)
</details>


## Gravitee Kubernetes Operator 4.4.13 - November 12, 2024
    
<details>
<summary>Bug fixes</summary>

  * Having two plans with same name lead to duplicate key error on API v4 export [#10128](https://github.com/gravitee-io/issues/issues/10128)
</details>


## Gravitee Kubernetes Operator 4.4.12 - October 28, 2024

There is nothing new in version 4.4.12.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.4.11 - October 14, 2024
    
<details>
<summary>Bug fixes</summary>

  * Allow to set imagePullSecrets in deployments using Helm [#10092](https://github.com/gravitee-io/issues/issues/10092)
</details>

## Gravitee Kubernetes Operator 4.4.10 - October 1, 2024

<details>
<summary>Bug fixes</summary>

  * GKO - Unable to import API V4 Message with push plan - 400 Bad Request : PlanSecurityType empty [#10036](https://github.com/gravitee-io/issues/issues/10036)
  * Plan description field is optional in APIM but required in GKO [#10041](https://github.com/gravitee-io/issues/issues/10041)
</details>

## Gravitee Kubernetes Operator 4.4.9 - September 16, 2024

<details>
<summary>Bug fixes</summary>

  * updates to API v4 are not deployed on the gateway [#10009](https://github.com/gravitee-io/issues/issues/10009)
  * sync-process probe passes to healthy before APIs are deployed [#9797](https://github.com/gravitee-io/issues/issues/9797)
</details>

## Gravitee Kubernetes Operator 4.4.8 - September 2, 2024
    
<details>
<summary>Bug fixes</summary>

  * Application description should be mandatory [#9963](https://github.com/gravitee-io/issues/issues/9963)
</details>


## Gravitee Kubernetes Operator 4.4.7 - September 2, 2024

There is nothing new in version 4.4.7.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.4.6 - September 2, 2024

There is nothing new in version 4.4.6.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.4.5 - August 19, 2024
    
<details>
<summary>Bug fixes</summary>

  * GKO Categories not being created or associated [Split from #9654] [#9905](https://github.com/gravitee-io/issues/issues/9905)
  * v2 API properties are not readonly in APIM UI when the API is managed by the operator [#9892](https://github.com/gravitee-io/issues/issues/9892)
</details>


## Gravitee Kubernetes Operator 4.4.4 - August 5, 2024
    
<details>
<summary>Bug fixes</summary>

  * v4 documentation not fully read-only [#9826](https://github.com/gravitee-io/issues/issues/9826)
</details>


<details>
<summary>Improvements</summary>

  * Make APIM HTTP client timeout configurable [#9890](https://github.com/gravitee-io/issues/issues/9890)
  * Support access controls and visibility when fetching from `ROOT pages in v2 API definition [#9889](https://github.com/gravitee-io/issues/issues/9889)
</details>


## Gravitee Kubernetes Operator 4.4.3 - July 22, 2024
    
<details>
<summary>Bug fixes</summary>

  * Kubernetes export of v2 API with pages can fail because of pages without names [#9883](https://github.com/gravitee-io/issues/issues/9883)
  * Cannot reference member role by id in v4 API definition members [#9880](https://github.com/gravitee-io/issues/issues/9880)
  * API primary owner deduced from group cannot view API on portal [#9877](https://github.com/gravitee-io/issues/issues/9877)
  * Execution mode cannot be configured for v2 ApiDefinition resources [#9867](https://github.com/gravitee-io/issues/issues/9867)
  * Group gets removed from API on updates when API PO is the group PO [#9846](https://github.com/gravitee-io/issues/issues/9846)
  * Can't change role of member when using id in v4 API CRD [#9827](https://github.com/gravitee-io/issues/issues/9827)
</details>


<details>
<summary>Improvements</summary>

  * Notifications sent to new members of an API cannot be turned on / off on operator resources [#9886](https://github.com/gravitee-io/issues/issues/9886)
  * Add support for ROOT page type in v2 API definitions [#9885](https://github.com/gravitee-io/issues/issues/9885)
</details>


## Gravitee Kubernetes Operator 4.4.2 - July 5, 2024
    
<details>
<summary>Bug fixes</summary>

  * false values are not persisted for `disable_membership_notifications` in applications [#9847](https://github.com/gravitee-io/issues/issues/9847)
  * v2 crd export fails because of unknown plan fields [#9830](https://github.com/gravitee-io/issues/issues/9830)
</details>


## Gravitee Kubernetes Operator 4.4.1 - June 26, 2024

<details>

<summary>Bug fixes</summary>

* default image tag for Kube RBAC proxy should be upgraded [9825](https://github.com/gravitee-io/issues/issues/9825)
* v2 API exported as CRD can't be re-imported due to unknown field status [9824](https://github.com/gravitee-io/issues/issues/9824)

</details>

## Gravitee Kubernetes Operator 4.4.0 - June 24, 2024

<details>

<summary>Improvements</summary>

* Core support for v4 API definition
* Documentation page support for v2 and v4 API definitions
* Groups and member support for v2 and v4 API definitions
* Categories support for v2 and v4 API definitions

</details>
