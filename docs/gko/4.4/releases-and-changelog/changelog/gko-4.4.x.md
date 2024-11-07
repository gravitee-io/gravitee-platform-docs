# GKO 4.4.x

## Gravitee Kubernetes Operator 4.4.12 - October 28, 2024

There is nothing new in version 4.4.12.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.4.11 - October 14, 2024
    
<details>
<summary>Bug fixes</summary>

  * Allow to set imagePullSecrets in deployments using Helm [#10092](https://github.com/gravitee-io/issues/issues/10092)
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
