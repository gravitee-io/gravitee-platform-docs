# GKO 4.6.x

## Gravitee Kubernetes Operator 4.6.13 - June 16, 2025
    
<details>
<summary>Improvements</summary>

  * Allow to specify custom annotations and labels on manager deployment / pod [#10613](https://github.com/gravitee-io/issues/issues/10613)
</details>


## Gravitee Kubernetes Operator 4.6.12 - June 5, 2025

There is nothing new in version 4.6.12.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.6.11 - May 14, 2025
    
<details>
<summary>Bug fixes</summary>

  * Management Context Could not be resolved in Webhook when GKO deployed on multiple namespaces [#10562](https://github.com/gravitee-io/issues/issues/10562)
  * Unable to delete APIs using GKO templating [#10554](https://github.com/gravitee-io/issues/issues/10554)
  * API Policies show disabled in the UI for V4 API's created via the GKO operator. [#10543](https://github.com/gravitee-io/issues/issues/10543)
  * mAPI throws exception an Application is created using GKO with empty pictureUrl [#10531](https://github.com/gravitee-io/issues/issues/10531)
</details>


## Gravitee Kubernetes Operator 4.6.10 - April 28, 2025
    
<details>
<summary>Bug fixes</summary>

  * Unable to remove kubernetes secret used as template for an APIV4 [#10510](https://github.com/gravitee-io/issues/issues/10510)
  * Installing several operators in multiple namespaces is not possible due to webhook conflict [#10499](https://github.com/gravitee-io/issues/issues/10499)
  * Change in Config Maps or Secrets used for templating are not reflected in targeted resources [#10498](https://github.com/gravitee-io/issues/issues/10498)
</details>


## Gravitee Kubernetes Operator 4.6.9 - April 14, 2025
    
<details>
<summary>Bug fixes</summary>

  * v4 APIs created via GKO not displayed in assigned Category [#10448](https://github.com/gravitee-io/issues/issues/10448)
</details>


## Gravitee Kubernetes Operator 4.6.8 - April 8, 2025
    
<details>
<summary>Improvements</summary>

  * Allow to set `hostNetwork` flag in manager deployment [#10478](https://github.com/gravitee-io/issues/issues/10478)
</details>


## Gravitee Kubernetes Operator 4.6.7 - March 28, 2025
    
<details>
<summary>Bug fixes</summary>

  * GKO fails to start with specific namespace given at Helm install [#10426](https://github.com/gravitee-io/issues/issues/10426)
  * Severe error when deploying Native v4 API [#10406](https://github.com/gravitee-io/issues/issues/10406)
</details>


<details>
<summary>Security</summary>

  * update module github.com/golang-jwt/jwt/v5 to v5.2.2 [#10452](https://github.com/gravitee-io/issues/issues/10452)
</details>


## Gravitee Kubernetes Operator 4.6.6 - March 17, 2025
    
<details>
<summary>Bug fixes</summary>

  * Object status and metadata meta should be ignored when compiling template strings [#10410](https://github.com/gravitee-io/issues/issues/10410)
</details>


## Gravitee Kubernetes Operator 4.6.5 - March 6, 2025
    
<details>
<summary>Bug fixes</summary>

  * V4 API deletion happens without waiting for the plan to be deleted [#10376](https://github.com/gravitee-io/issues/issues/10376)
  * RBAC for config map should not be required when local mode is never used [#10371](https://github.com/gravitee-io/issues/issues/10371)
  * Remove releaseTimestamp annotation from manager deployment [#10358](https://github.com/gravitee-io/issues/issues/10358)
</details>


## Gravitee Kubernetes Operator 4.6.4 - February 17, 2025

### Deprecations warning

  The following Helm values are deprecated and marked for removal in 4.7.0.

  * `httpClient.insecureSkipCertVerify` is deprecated at the root level and should be configured inside the `manager` section
  * `rbac.skipClusterRoles` is deprecated in favour of `rbac.create`. This means that starting from 4.7.0 all RBAC related resources have to be applied separately if you want to handle cluster roles separately. A guide has been published in our doc site in order to help with [RBAC customization](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/getting-started/installation/rbac-customization).
  * `manager.logs.json` is deprecated in favour of `manager.logs.format`.
  * `webhook.enabled` is deprecated. Starting from 4.7.0, the admission webhook will be a mandatory feature of the operator.

    
<details>
<summary>Bug fixes</summary>

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


## Gravitee Kubernetes Operator 4.6.3 - February 7, 2025

There is nothing new in version 4.6.3.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.6.2 - February 5, 2025
    
<details>
<summary>Bug fixes</summary>

  * Management context secret resolution fails when API is in another namespace [#10315](https://github.com/gravitee-io/issues/issues/10315)
  * GKO Helm chart causes Argo CD reconciliation loop [#10306](https://github.com/gravitee-io/issues/issues/10306)
  * No validation for already existing listener host for native APIs [#10305](https://github.com/gravitee-io/issues/issues/10305)
  * API v2 CRD export generates bad format for headers [#10288](https://github.com/gravitee-io/issues/issues/10288)
</details>


## Gravitee Kubernetes Operator 4.6.1 - January 27, 2025
    
<details>
<summary>Bug fixes</summary>

  * RBAC creation is inconsistent for admission webhook when scope is not cluster [#10294](https://github.com/gravitee-io/issues/issues/10294)
  * Admission panics when Management Context references a secret in another namespace [#10279](https://github.com/gravitee-io/issues/issues/10279)
  * Re-deploying an exported API CRD fails due to unknown metadata field [#10282](https://github.com/gravitee-io/issues/issues/10282)
  * Documentation page not visible if parent field doesn't match folder name [#10281](https://github.com/gravitee-io/issues/issues/10281)
  * Details of flow configuration of Native API are not exported  [#10287](https://github.com/gravitee-io/issues/issues/10287)
</details>


<details>
<summary>Security</summary>

  * Webhook cluster role access should be narrowed down to resource names we use [#10296](https://github.com/gravitee-io/issues/issues/10296)
</details>
