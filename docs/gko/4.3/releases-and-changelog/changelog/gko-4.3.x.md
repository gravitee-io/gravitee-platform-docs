---
description: Overview of GKO.
---

# GKO 4.3.x

## Gravitee Kubernetes Operator 4.3.27 - March 28, 2025

<details>

<summary>Security</summary>

* update module github.com/golang-jwt/jwt/v5 to v5.2.2 [#10452](https://github.com/gravitee-io/issues/issues/10452)

</details>

## Gravitee Kubernetes Operator 4.3.26 - March 17, 2025

There is nothing new in version 4.3.26.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.3.25 - March 6, 2025

There is nothing new in version 4.3.25.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.3.24 - February 17, 2025

There is nothing new in version 4.3.24.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.3.23 - February 5, 2025

There is nothing new in version 4.3.23.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.3.22 - January 27, 2025

There is nothing new in version 4.3.22.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.3.16 - October 28, 2024

There is nothing new in version 4.3.16.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.3.15 - October 14, 2024

<details>

<summary>Bug fixes</summary>

* Allow to set imagePullSecrets in deployments using Helm [#10092](https://github.com/gravitee-io/issues/issues/10092)

</details>

## Gravitee Kubernetes Operator 4.3.12 - September 2, 2024

<details>

<summary>Bug fixes</summary>

* Application description should be mandatory [#9963](https://github.com/gravitee-io/issues/issues/9963)

</details>

## Gravitee Kubernetes Operator 4.3.11 - August 19, 2024

<details>

<summary>Bug fixes</summary>

* v2 API properties are not readonly in APIM UI when the API is managed by the operator [#9892](https://github.com/gravitee-io/issues/issues/9892)

</details>

## Gravitee Kubernetes Operator 4.3.10 - August 5, 2024

<details>

<summary>Improvements</summary>

* Make APIM HTTP client timeout configurable [#9890](https://github.com/gravitee-io/issues/issues/9890)

</details>

## Gravitee Kubernetes Operator 4.3.9 - July 22, 2024

<details>

<summary>Bug fixes</summary>

* Execution mode cannot be configured for v2 ApiDefinition resources [#9867](https://github.com/gravitee-io/issues/issues/9867)
* Group gets removed from API on updates when API PO is the group PO [#9846](https://github.com/gravitee-io/issues/issues/9846)

</details>

## Gravitee Kubernetes Operator 4.3.8 - July 5, 2024

<details>

<summary>Bug fixes</summary>

* false values are not persisted for `disable_membership_notifications` in applications [#9847](https://github.com/gravitee-io/issues/issues/9847)
* v2 crd export fails because of unknown plan fields [#9830](https://github.com/gravitee-io/issues/issues/9830)
* v2 API exported as CRD can't be re-imported due to unknown field status [#9824](https://github.com/gravitee-io/issues/issues/9824)

</details>

<details>

<summary>Improvements</summary>

* make image pull policies configurable in helm chart [#9819](https://github.com/gravitee-io/issues/issues/9819)

</details>

<details>

<summary>Security</summary>

* default image tag for Kube RBAC proxy should be upgraded [#9825](https://github.com/gravitee-io/issues/issues/9825)

</details>

## Gravitee Kubernetes Operator 4.3.7 - June 24, 2024

GKO 4.3.7 is a tag based on GKO 0.13.1. For details of changes that came in releases from GKO 4.3.7 and earlier, please take a look at the change logs in Github.

There is a change in the compatibility policies between GKO 4.3 and GKO 4.4. As of GKO 4.4, GKO follows a strict compatibility policy whereby a given minor version of GKO requires the same minor version of APIM. As such, GKO 4.4 is compatible with APIM 4.4.

GKO 4.3 is compatible for the most part with APIM 4.3, 4.2, and 4.1.
