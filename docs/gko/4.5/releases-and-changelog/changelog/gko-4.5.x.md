# GKO 4.5.x

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
