# GKO 4.7.x

4.7.9-alpha was not created in Jira. Assuming no changelog should be generated.


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
