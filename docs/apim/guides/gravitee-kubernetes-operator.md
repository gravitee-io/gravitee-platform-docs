# Gravitee Kubernetes Operator

The Gravitee Kubernetes Operator (GKO) is a technical component designed to be deployed on an existing Gravitee API Management (APIM) ready Kubernetes Cluster. It can also be deployed on a local cluster for testing purposes.

You can use the GKO to define, deploy, and publish APIs to your API Portal and API Gateway and to manage Custom Resource Definitions (CRDs) as part of the process.

The GKO also enables you to create reusable [API resources](api-configuration/resources.md) by applying the [`ApiResource` custom resource definition](https://docs.gravitee.io/apim/3.x/apim\_kubernetes\_operator\_user\_guide\_reusable\_resources.html). This enables you to define resources such as cache or authentication providers a single time and maintain them in a single place for reuse in multiple APIs. Any further updates to such a resource will be automatically propagated to all APIs containing a reference to that resource.

In this guide, you will learn how to work with CRDs and how to synchronize your API CRDs with the APIM management API — including how to start, stop, update, and delete your APIs.

{% hint style="info" %}
In future releases, the GKO will support additional functionality to enable the following:

* Using the GKO as an Ingress Controller for deploying Ingresses to an API Gateway.
* Deploying Gravitee products (API Management, Access Management, Alert Engine).
* Improving automation processes by covering CICD aspects when using Kubernetes with APIM.
* Managing most API Management resources without directly relying on the Console or the Management API.
{% endhint %}
