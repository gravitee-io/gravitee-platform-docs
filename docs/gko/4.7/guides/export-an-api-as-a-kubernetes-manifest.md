---
description: Easily transition from the GUI to a Kubernetes resource
---

# Export an API as a Kubernetes manifest

Gravitee API Management lets you export a v2 or v4 API defined in the GUI as a Kubernetes manifest for the Gravitee Kubernetes Operator. You may want to do this because:

* It is an easy way to bootstrap an `ApiV4Definition` or `ApiDefinition` resource without needing to know the exact YAML syntax.
* You can create a workflow where users create APIs in the APIM UI during development, then transition to use a GitOps workflow with GKO for downstream environments like staging and production.

Export can be done through the UI, or using the Management API (which is very practical for integration with CI pipelines).

## Exporting from the UI

In the Gravitee API Management Console, go to the overview of any v2 or v4 API and click the **Export** button to view the available export options.

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

In the modal that opens, select the **CRD API Definition** tab and click the **Export** button.

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

You will be prompted to save your API definition YAML Kubernetes manifest to disk.

## Exporting from the Management API

The APIM Management API provides an export endpoint you can use to export an API as an `ApiDefinition` resource. This allows you to easily create an `ApiDefinition` from a given environment by calling the endpoint and piping the result to a `kubectl` command. For example:

{% code overflow="wrap" %}
```sh
curl -s -H "Authorization: Bearer $TOKEN" "https://apim-example-api.team-gko.gravitee.xyz/management/organizations/DEFAULT/environments/DEFAULT/apis/$API_ID/crd" | kubectl apply -f -
```
{% endcode %}
