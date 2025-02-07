# GKO 4.6.x

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
