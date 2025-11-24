---
description: Easily transition from the GUI to a Kubernetes resource
---

# Export an API as a Kubernetes manifest

Gravitee API Management provides the ability to export v2 and v4 APIs defined in the GUI as a Kubernetes manifest for the Gravitee Kubernetes Operator.

There are a few use cases for exporting your API created in APIM as a Kubernetes manifest for GKO:

* It is an easy way to bootstrap an `ApiV4Definition` or `ApiDefinition` resource without needed to know the yaml syntax by heart
* You can create a workflow in which users start by creating APIs in the APIM UI during development, and then transition to using a GitOps workflow with the Gravitee Kubernetes Operator for downstream environments like staging and production.

Export can be done through the UI, or using the management API (which is very practical for integration with CI pipelines).

## Exporting from the UI

In the Gravitee API Management console, head to the overview of any v2 or v4 API and hit the export button to view the available export options.

<figure><img src="../.gitbook/assets/image (2) (1).png" alt=""><figcaption><p>The Export button</p></figcaption></figure>

In the modal that opens, select the **CRD API Definition** tab and click the **Export** button.

<figure><img src="../.gitbook/assets/image (1) (1).png" alt=""><figcaption></figcaption></figure>

You will then be prompted to save your API definition yaml Kubernetes manifest to disk.

## Exporting from the management API

The APIM management API provides an export endpoint that allows you to export an API as an API Definition resource.

This allows you to easily create an API Definition from a given environment by calling the endpoint and piping the result to a `kubectl` command. For example:

{% code overflow="wrap" %}
```sh
curl -s -H "Authorization: Bearer $TOKEN" "https://apim-example-api.team-gko.gravitee.xyz/management/organizations/DEFAULT/environments/DEFAULT/apis/$API_ID/crd" | kubectl apply -f -
```
{% endcode %}
