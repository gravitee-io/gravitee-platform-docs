---
description: Learn more about the Gravitee Kubernetes Operator
---

# Gravitee Kubernetes Operator

## Overview

The Gravitee Kubernetes Operator (GKO) is designed to be deployed on an existing Gravitee API Management (APIM)-ready Kubernetes cluster, or locally for testing purposes.

The GKO uses custom resource definitions (CRDs) to define, deploy, and publish APIs to your Developer Portal and API Gateway. It includes three CRDs: `ManagementContext`, `ApiDefinition`, and `ApiResource`.

The [`ApiResource`](custom-resource-definitions/apiresource.md) CRD is used to create reusable [API resources](../api-configuration/resources.md) such as cache or authentication providers. These can be defined a single time and maintained in a single place for reuse in multiple APIs. Updates to a resource will be automatically propagated to all APIs containing a reference to that resource.

Choose from the guides below to learn how to use CRDs and synchronize your API CRDs with the APIM Management API, including how to start, stop, update, and delete your APIs.

{% hint style="info" %}
**GKO limitations**

The GKO is not yet at full feature parity with the Management API and APIM Console. The GKO cannot configure:

* A plan to be used across multiple APIs. Plans can only be configured per API using the `ApiDefinition` CRD.
* Flows/policies to be used across multiple APIs. These can only be configured per API using the `ApiDefinition` CRD.
* Component resources
* API documentation pages
* API media
* Alerts
* Users/groups/permissions
* Subscriptions and/or keys
* Developer Portal themes
* APIM dictionaries
{% endhint %}

<table data-view="cards"><thead><tr><th></th><th></th><th></th><th data-hidden data-card-target data-type="content-ref"></th></tr></thead><tbody><tr><td></td><td>Quick Start</td><td></td><td><a href="quick-start.md">quick-start.md</a></td></tr><tr><td></td><td>Installation</td><td></td><td><a href="installation.md">installation.md</a></td></tr><tr><td></td><td>Test GKO after Deployment</td><td></td><td><a href="test-gko-after-deployment.md">test-gko-after-deployment.md</a></td></tr><tr><td></td><td>Gravitee as an Ingress Controller</td><td></td><td><a href="gravitee-as-an-ingress-controller.md">gravitee-as-an-ingress-controller.md</a></td></tr><tr><td></td><td>Custom Resource Definitions</td><td></td><td><a href="custom-resource-definitions/">custom-resource-definitions</a></td></tr></tbody></table>
