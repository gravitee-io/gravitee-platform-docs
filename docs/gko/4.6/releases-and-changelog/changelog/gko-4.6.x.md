# GKO 4.6.x

## Gravitee Kubernetes Operator 4.6.4 - February 17, 2025
    
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
