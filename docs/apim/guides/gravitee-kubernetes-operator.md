# Gravitee Kubernetes Operator

The Gravitee Kubernetes Operator (GKO) is a technical component designed to be deployed on an existing Gravitee API Management (APIM) ready Kubernetes Cluster. It can also be deployed on a local cluster for testing purposes.

You can use the GKO to define, deploy, and publish APIs to your API Developer Portal and API Gateway with Custom Resource Definitions (CRDs). The Gravitee Kubernetes Operator comes with three CRDs - `ManagementContext`, `ApiDefinition`, and `ApiResource`. They are described in detail further in this guide.

The GKO also enables you to create reusable [API resources](api-configuration/resources.md) by applying the [`ApiResource` custom resource definition](gravitee-kubernetes-operator/custom-resource-definitions/apiresource-crd.md). This allows you to define resources such as cache or authentication providers a single time and maintain them in a single place for reuse in multiple APIs. Any further updates to such a resource will be automatically propagated to all APIs containing a reference to that resource.

In this guide, you will learn how to work with CRDs and how to synchronize your API CRDs with the APIM Management API — including how to start, stop, update, and delete your APIs.

{% hint style="info" %}
**Existing Gravitee Kubernetes Operator limitations**

The Gravitee Kubernetes Operator is not yet at full feature-parity with the Gravitee Management API and the Gravitee APIM Console, and we are planning to fill at least some of these gaps in future releases. As of today, the GKO cannot:

* Support the v4 API definition
* Configure a plan to be used across multiple APIs. Currently, you can only configure plans on a per API basis using the ApiDefinition CRD
* Configure flows/policies to be used across multiple APIs. Currently, you can only configure flows/policies on a per API basis using the ApiDefinition CRD
* Configuring component resources
* Configuring your API documentation page
* Configure API media
* Configure Alerts
* Configure Users/Groups
* Configure Subscriptions and/or keys
* Configure Developer Portal themes
* Configure permissions
* Configure APIM dictionaries
{% endhint %}
