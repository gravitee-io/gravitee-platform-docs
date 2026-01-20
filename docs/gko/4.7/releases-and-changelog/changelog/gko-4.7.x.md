---
description: Overview of GKO.
---

# GKO 4.7.x

## Gravitee Kubernetes Operator 4.7.23 - January 20, 2026

There is nothing new in version 4.7.23.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.7.22 - December 19, 2025

There is nothing new in version 4.7.22.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.7.21 - December 19, 2025

There is nothing new in version 4.7.21.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.7.20 - December 8, 2025

<details>
<summary>Bug fixes</summary>

  **APIM**

  * V4 & JSON exports incorrectly embed HTTP-fetcher page content [#10985](https://github.com/gravitee-io/issues/issues/10985)

</details>

## Gravitee Kubernetes Operator 4.7.19 - November 25, 2025

There is nothing new in version 4.7.19.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.


## Gravitee Kubernetes Operator 4.7.18 - November 14, 2025

There is nothing new in version 4.7.18.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.7.17 - October 28, 2025

There is nothing new in version 4.7.17.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.7.16 - October 15, 2025

There is nothing new in version 4.7.16.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.7.15 - September 29, 2025

<details>

<summary>Bug fixes</summary>

**GKO**

* Can't delete SharedPolicyGroup [#10827](https://github.com/gravitee-io/issues/issues/10827)
* Finalizer of a secret un-referenced by a context don't get removed on update [#10707](https://github.com/gravitee-io/issues/issues/10707)

</details>

<details>

<summary>Improvements</summary>

**GKO**

* Add proxy support for HTTP client [#10830](https://github.com/gravitee-io/issues/issues/10830)

</details>

## Gravitee Kubernetes Operator 4.7.13 - September 2, 2025

There is nothing new in version 4.7.13.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.7.12 - August 22, 2025

<details>

<summary>Bug fixes</summary>

* GKO-created applications can be deleted through the portal UI [#10651](https://github.com/gravitee-io/issues/issues/10651)

</details>

## Gravitee Kubernetes Operator 4.7.11 - August 4, 2025

There is nothing new in version 4.7.11.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.7.10 - July 22, 2025

There is nothing new in version 4.7.10.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.7.9 - July 15, 2025

<details>

<summary>Bug fixes</summary>

* Promotion between multiple clusters fails because of plan IDs duplication [#10641](https://github.com/gravitee-io/issues/issues/10641)

</details>

4.7.9-alpha was not created in Jira. Assuming no changelog should be generated.

## Gravitee Kubernetes Operator 4.7.8 - June 24, 2025

There is nothing new in version 4.7.8.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.7.7 - June 16, 2025

<details>

<summary>Improvements</summary>

* Allow to specify custom annotations and labels on manager deployment / pod [#10613](https://github.com/gravitee-io/issues/issues/10613)

</details>

## Gravitee Kubernetes Operator 4.7.6 - June 5, 2025

There is nothing new in version 4.7.6.

> This version was generated to keep the kubernetes operator in sync with other gravitee products.

## Gravitee Kubernetes Operator 4.7.5 - May 14, 2025

<details>

<summary>Bug fixes</summary>

* Management Context Could not be resolved in Webhook when GKO deployed on multiple namespaces [#10562](https://github.com/gravitee-io/issues/issues/10562)
* Unable to delete APIs using GKO templating [#10554](https://github.com/gravitee-io/issues/issues/10554)
* API Policies show disabled in the UI for V4 API's created via the GKO operator. [#10543](https://github.com/gravitee-io/issues/issues/10543)
* mAPI throws exception an Application is created using GKO with empty pictureUrl [#10531](https://github.com/gravitee-io/issues/issues/10531)

</details>

## Gravitee Kubernetes Operator 4.7.4 - April 28, 2025

<details>

<summary>Bug fixes</summary>

* auto-assigned groups are not added to applications [#10513](https://github.com/gravitee-io/issues/issues/10513)
* Unable to remove kubernetes secret used as template for an APIV4 [#10510](https://github.com/gravitee-io/issues/issues/10510)
* Change in Config Maps or Secrets used for templating are not reflected in targeted resources [#10498](https://github.com/gravitee-io/issues/issues/10498)

</details>

## Gravitee Kubernetes Operator 4.7.3 - April 17, 2025

<details>

<summary>Bug fixes</summary>

* APIs updated via GKO lose automatic group associations if not present on the CRD [#10508](https://github.com/gravitee-io/issues/issues/10508)
* Installing several operators in multiple namespaces is not possible due to webhook conflict [#10499](https://github.com/gravitee-io/issues/issues/10499)
* Validation webhook accepts MTLS plan for native APIs [#10506](https://github.com/gravitee-io/issues/issues/10506)

</details>

## Gravitee Kubernetes Operator 4.7.2 - April 14, 2025

<details>

<summary>Bug fixes</summary>

* v4 APIs created via GKO not displayed in assigned Category [#10448](https://github.com/gravitee-io/issues/issues/10448)

</details>

## Gravitee Kubernetes Operator 4.7.1 - April 8, 2025

<details>

<summary>Improvements</summary>

* Allow to set `hostNetwork` flag in manager deployment [#10478](https://github.com/gravitee-io/issues/issues/10478)

</details>
