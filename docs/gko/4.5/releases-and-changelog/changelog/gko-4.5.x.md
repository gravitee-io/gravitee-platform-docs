# GKO 4.5.x

## Gravitee Kubernetes Operator 4.5.22 - July 21, 2025

There is nothing new in version 4.5.22.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.5.21 - July 15, 2025
    
<details>
<summary>Bug fixes</summary>

  * Promotion between multiple clusters fails because of plan IDs duplication [#10641](https://github.com/gravitee-io/issues/issues/10641)
</details>


## Gravitee Kubernetes Operator 4.5.20 - June 24, 2025

There is nothing new in version 4.5.20.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.5.19 - June 16, 2025
    
<details>
<summary>Improvements</summary>

  * Allow to specify custom annotations and labels on manager deployment / pod [#10613](https://github.com/gravitee-io/issues/issues/10613)
</details>


## Gravitee Kubernetes Operator 4.5.18 - June 5, 2025

There is nothing new in version 4.5.18.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.5.17 - May 14, 2025
    
<details>
<summary>Bug fixes</summary>

  * Management Context Could not be resolved in Webhook when GKO deployed on multiple namespaces [#10562](https://github.com/gravitee-io/issues/issues/10562)
</details>


## Gravitee Kubernetes Operator 4.5.16 - May 6, 2025
    
<details>
<summary>Bug fixes</summary>

  * mAPI throws an exception when an Application is created using GKO with empty pictureUrl [#10531](https://github.com/gravitee-io/issues/issues/10531)
</details>


## Gravitee Kubernetes Operator 4.5.15 - April 28, 2025
    
<details>
<summary>Bug fixes</summary>

  * Installing several operators in multiple namespaces is not possible due to webhook conflict [#10499](https://github.com/gravitee-io/issues/issues/10499)
</details>


## Gravitee Kubernetes Operator 4.5.14 - April 14, 2025
    
<details>
<summary>Bug fixes</summary>

  * v4 APIs created via GKO not displayed in assigned Category [#10448](https://github.com/gravitee-io/issues/issues/10448)
</details>


## Gravitee Kubernetes Operator 4.5.13 - April 8, 2025
    
<details>
<summary>Improvements</summary>

  * Allow to set `hostNetwork` flag in manager deployment [#10478](https://github.com/gravitee-io/issues/issues/10478)
</details>


## Gravitee Kubernetes Operator 4.5.12 - March 28, 2025
    
<details>
<summary>Bug fixes</summary>

  * Severe error when deploying Native v4 API [#10406](https://github.com/gravitee-io/issues/issues/10406)
</details>


<details>
<summary>Security</summary>

  * update module github.com/golang-jwt/jwt/v5 to v5.2.2 [#10452](https://github.com/gravitee-io/issues/issues/10452)
</details>


## Gravitee Kubernetes Operator 4.5.11 - March 17, 2025

There is nothing new in version 4.5.11.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.5.10 - March 6, 2025
    
<details>
<summary>Bug fixes</summary>

  * V4 API deletion happens without waiting for the plan to be deleted [#10376](https://github.com/gravitee-io/issues/issues/10376)
  * Remove releaseTimestamp annotation from manager deployment [#10358](https://github.com/gravitee-io/issues/issues/10358)
</details>


## Gravitee Kubernetes Operator 4.5.9 - February 17, 2025
    
<details>
<summary>Bug fixes</summary>

  * API v2 local flag is true by default when the API reference states it is false [#10339](https://github.com/gravitee-io/issues/issues/10339)
  * GKO v4 API CRD is missing the analytics tracing attribute [#10322](https://github.com/gravitee-io/issues/issues/10322)
  * Operator is reconciling every secrets on startup [#10284](https://github.com/gravitee-io/issues/issues/10284)
</details>


<details>
<summary>Improvements</summary>

  * Allow to disable ingress controller in helm values [#10327](https://github.com/gravitee-io/issues/issues/10327)
  * Make the operator able to run in cluster mode but only monitor a set of namespaces listed in helm values [#10297](https://github.com/gravitee-io/issues/issues/10297)
</details>


<details>
<summary>Security</summary>

  * Narrow down verbs allowed for the manager role regarding custom resources [#10328](https://github.com/gravitee-io/issues/issues/10328)
</details>


## Gravitee Kubernetes Operator 4.5.8 - February 5, 2025
    
<details>
<summary>Bug fixes</summary>

  * Management context secret resolution fails when API is in another namespace [#10315](https://github.com/gravitee-io/issues/issues/10315)
  * GKO Helm chart causes Argo CD reconciliation loop [#10306](https://github.com/gravitee-io/issues/issues/10306)
  * API v2 CRD export generates bad format for headers [#10288](https://github.com/gravitee-io/issues/issues/10288)
</details>


## Gravitee Kubernetes Operator 4.5.7 - January 27, 2025
    
<details>
<summary>Bug fixes</summary>

  * RBAC creation is inconsistent for admission webhook when scope is not cluster [#10294](https://github.com/gravitee-io/issues/issues/10294)
  * Re-deploying an exported API CRD fails due to unknown metadata field [#10282](https://github.com/gravitee-io/issues/issues/10282)
  * Documentation page not visible if parent field doesn't match folder name [#10281](https://github.com/gravitee-io/issues/issues/10281)
</details>


<details>
<summary>Security</summary>

  * Webhook cluster role access should be narrowed down to resource names we use [#10296](https://github.com/gravitee-io/issues/issues/10296)
</details>


## Gravitee Kubernetes Operator 4.5.6 - January 17, 2025

<details>

<summary>Bug fixes</summary>

* Admission panics when Management Context references a secret in another namespace [#10275](https://github.com/gravitee-io/issues/issues/10275)

</details>

<details>

<summary>Security</summary>

* Update module golang.org/x/net to v0.33.0 [#10254](https://github.com/gravitee-io/issues/issues/10254)

</details>

<details>

<summary>Improvements</summary>

* Upcoming 4.6 Gravitee Cloud support has been backported

</details>

🚀 Kudos to [@jachymsol](https://github.com/jachymsol) for making his first contribution to the Kubernetes Operator with [98ddc38](https://github.com/gravitee-io/gravitee-kubernetes-operator/commit/98ddc38ec043eb7812e6d334c1d4c8b6dcc4275a)

## Gravitee Kubernetes Operator 4.5.5 - December 20, 2024

<details>

<summary>Bug fixes</summary>

* Missing deprecated status in API definition for plans [#10248](https://github.com/gravitee-io/issues/issues/10248)
* Application notifyMembers doesn't work [#10231](https://github.com/gravitee-io/issues/issues/10231)
* Editable HTTP configuration when an API is managed by the operator [#10221](https://github.com/gravitee-io/issues/issues/10221)
* Template strings are not resolved for API Resources references [#10214](https://github.com/gravitee-io/issues/issues/10214)
* Unable to import two v2 plans with same type in APIM [#10195](https://github.com/gravitee-io/issues/issues/10195)

</details>

## Gravitee Kubernetes Operator 4.5.4 - December 9, 2024

<details>

<summary>Improvements</summary>

* Issue a clear warning when attempting to apply a group with an API primary owner [#10094](https://github.com/gravitee-io/issues/issues/10094)
* Improve OAuth application settings validation [#10079](https://github.com/gravitee-io/issues/issues/10079)

</details>

<details>

<summary>Bug fixes</summary>

* Missing Key and Trust Store fields in API Definition [#10215](https://github.com/gravitee-io/issues/issues/10215)

</details>

## Gravitee Kubernetes Operator 4.5.3 - November 21, 2024

<details>

<summary>Bug fixes</summary>

* API v2 CRD export cannot be applied when setting selection rules on plans [#10185](https://github.com/gravitee-io/issues/issues/10185)
* Adding a page is allowed for v4 APIs managed by the operator [#10184](https://github.com/gravitee-io/issues/issues/10184)
* API state is not exported when the API is stopped [#10172](https://github.com/gravitee-io/issues/issues/10172)
* Cloud context fails with token stored in a secret [#10170](https://github.com/gravitee-io/issues/issues/10170)
* Webhook validation fails when management context references a secret [#10168](https://github.com/gravitee-io/issues/issues/10168)
* The notifyMembers property is ignored for V2 APIs [#10163](https://github.com/gravitee-io/issues/issues/10163)
* Empty map values are ignored when persisting resources [#10161](https://github.com/gravitee-io/issues/issues/10161)
* Plan IDs are regenerated for V2 APIs after GKO upgrade [#10159](https://github.com/gravitee-io/issues/issues/10159)
* GKO - API Definition - Default System Folder "Aside" [#10152](https://github.com/gravitee-io/issues/issues/10152)
* Edit on Github button deactivated when deploying github fetcher [#10078](https://github.com/gravitee-io/issues/issues/10078)
* API Pages are not deleted when combining http-fetcher (or markdown) and github-fetchers together [#10087](https://github.com/gravitee-io/issues/issues/10087)

</details>

## Gravitee Kubernetes Operator 4.5.2 - November 12, 2024

<details>

<summary>Bug fixes</summary>

* Having two plans with same name lead to duplicate key error on API v4 export [#10128](https://github.com/gravitee-io/issues/issues/10128)
* APIs sourced from kubernetes config map get out of sync after some time [#10095](https://github.com/gravitee-io/issues/issues/10095)
* Adding a member with an existing role id to a V2 API issues a warning [#10096](https://github.com/gravitee-io/issues/issues/10096)
* GKO removes attributes with empty value from API Definition [#10034](https://github.com/gravitee-io/issues/issues/10034)

</details>

<details>

<summary>Improvements</summary>

* Filter out v2 pages that are fetched from a root repo on CRD export [#10093](https://github.com/gravitee-io/issues/issues/10093)

</details>

## Gravitee Kubernetes Operator 4.5.1 - October 28, 2024

<details>

<summary>Improvements</summary>

* Filter out v2 pages that are fetched from a root repo on CRD export [#10093](https://github.com/gravitee-io/issues/issues/10093)
* Add support for pod tolerations in Helm charts [#10135](https://github.com/gravitee-io/issues/issues/10135)

</details>

<details>

<summary>Security</summary>

* Narrow down webhook configurations role permissions [#10105](https://github.com/gravitee-io/issues/issues/10105)

</details>

🚀 Kudos to [@lucamaggioni](https://github.com/lucamaggioni) for making his first contribution to the Kubernetes Operator with [13c1bf0](https://github.com/gravitee-io/gravitee-kubernetes-operator/commit/13c1bf043f61564d8ef77cad27521a5cef7844e4)
