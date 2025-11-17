---
description: Learn more about the Gravitee Kubernetes Operator
---

# Gravitee Kubernetes Operator

{% embed url="https://www.loom.com/share/f13544964f9b4b8c9fd8852aaa7e211d?sid=997c11ad-57ba-44f4-aae8-12df348e1a86" %}
Brief intro to the GKO
{% endembed %}

## Overview

The Gravitee Kubernetes Operator (GKO) is a technical component designed to be deployed on an existing Gravitee API Management (APIM)-ready Kubernetes cluster. It can also be deployed on a local cluster for testing purposes.

You can use the GKO to define, deploy, and publish APIs to your API Developer Portal and API Gateway via custom resource definitions (CRDs). The Gravitee Kubernetes Operator includes three CRDs: `ManagementContext`, `ApiDefinition`, and `ApiResource`, which are described in detail [here](custom-resource-definitions/README.md).

By applying the [`ApiResource`](custom-resource-definitions/apiresource-crd.md) CRD, you can create reusable [API resources](../api-configuration/resources.md) such as cache or authentication providers. These can be defined a single time and maintained in a single place for reuse in multiple APIs. Any further updates to the resource will be automatically propagated to all APIs containing a reference to that resource.

Choose from the guides below to learn how to use CRDs and synchronize your API CRDs with the APIM Management API, including how to start, stop, update, and delete your APIs.

{% hint style="info" %}
**Existing Gravitee Kubernetes Operator limitations**

The Gravitee Kubernetes Operator is not yet at full feature-parity with  Gravitee Management API and Gravitee APIM Console. The GKO cannot:

* Configure a plan to be used across multiple APIs. Currently, you can only configure plans on a per-API basis using the `ApiDefinition` CRD.
* Configure flows/policies to be used across multiple APIs. Currently, you can only configure flows/policies on a per-API basis using the `ApiDefinition` CRD.
* Configure component resources
* Configure your API documentation page
* Configure API media
* Configure alerts
* Configure users/Groups
* Configure subscriptions and/or keys
* Configure Developer Portal themes
* Configure permissions
* Configure APIM dictionaries
{% endhint %}

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>Quick Start</td><td></td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td></td><td>Installation</td><td></td><td><a href="broken-reference">Broken link</a></td></tr><tr><td></td><td>Test GKO after deployment</td><td></td><td><a href="test-gko-after-deployment.md">test-gko-after-deployment.md</a></td></tr><tr><td></td><td>Gravitee as an ingress controller</td><td></td><td><a href="gravitee-as-an-ingress-controller.md">gravitee-as-an-ingress-controller.md</a></td></tr><tr><td></td><td>Custom resource definitions</td><td></td><td><a href="custom-resource-definitions/">custom-resource-definitions</a></td></tr></tbody></table>
