# GKO 4.5.x

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
