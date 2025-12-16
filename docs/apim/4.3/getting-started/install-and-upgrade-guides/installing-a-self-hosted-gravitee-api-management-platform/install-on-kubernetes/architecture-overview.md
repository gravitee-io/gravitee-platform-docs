---
description: >-
  In order to meet your architecture requirements, various deployment strategies
  can be applied when installing the GKO. This section examines these different
  models and their required configurations.
---

# Architecture Overview

## Context for introducing an operator

Gravitee is able to deploy the following components:

* APIs and associated applications
* The API Gateway and the Management Console

An increasing number of Gravitee users are implementing infrastructure-as-code (IAC). To support IAC-based use cases, Gravitee enables platform deployment “as code” by performing the actions below without the use of a UI:

* Push/deploy APIs to the API Gateway
* Test the APIs
* Promote the APIs across different environments (test, UAT, dev, prod, etc.)

Historically, Gravitee customers have deployed APIs using the following:

* **Gravitee Management Console:** Gravitee includes an easy-to-use, self-serve UI. The Console is often used as a development tool and is connected to a backend service that is part of the Gravitee web application.
* **Gravitee Management API:** Every action in the Gravitee Management Console represents a REST API with a JSON payload that is documented using an API spec. Consequently, every UI action can be performed via REST API calls backed by JSON files. A Gravitee API definition is also a JSON file that explains endpoints, protections, etc.

While the REST API method is compatible with IaC, customer feedback favors a Kubernetes-native deployment of APIs, the Gravitee APIM Gateway and the Console via [Custom Resource Definitions (CRDs)](../../../../guides/gravitee-kubernetes-operator/custom-resource-definitions/README.md). The introduction of the Gravitee Kubernetes Operator (GKO) makes this possible.

## Deployment strategies

The current functionality of the Gravitee Kubernetes Operator supports three main deployment scenarios, as described below.

{% hint style="info" %}
While an APIM instance is only required to handle multi-cluster API deployments, all of the architectures described below support using an APIM instance to sync resources deployed through the operator with the Console.
{% endhint %}

{% tabs %}
{% tab title="Cluster Mode" %}
By default, the Gravitee Kubernetes Operator is set up to listen to the custom resources it owns at the cluster level.

In this mode, a single operator must be installed in the cluster to handle resources, regardless of the namespaces they have been created in. For each resource created in a specific namespace, the operator creates a ConfigMap in the same namespace that contains an API definition to be synced with an APIM Gateway.

By default, an APIM Gateway installed using the Helm Chart includes a limited set of permissions, and the Gateway is only able to access ConfigMaps created in its own namespace. However, giving a Gateway the cluster role allows it to access ConfigMaps created by the operator at the cluster level.

An overview of this architecture is described by the diagram below.

<figure><img src="../../../../.gitbook/assets/k8s cluster mode.png" alt=""><figcaption><p>Default Cluster Mode architecture</p></figcaption></figure>
{% endtab %}

{% tab title="Namespaced Mode" %}
The Gravitee Kubernetes Operator can be set up to listen to a single namespace in a Kubernetes cluster. One operator is deployed per namespace, and each listens to the custom resources created in its namespace only.

To achieve this architecture, the `manager.scope.cluster` value must be set to `false` during the Helm install. Role names are computed from the service account name, so each install must set a dedicated service account name for each operator using the `serviceAccount.name` Helm value.

An overview of this architecture is described by the diagram below.

<figure><img src="../../../../.gitbook/assets/k8s namespaced mode.png" alt=""><figcaption><p>Multiple operators, each listening to its own namespace</p></figcaption></figure>
{% endtab %}

{% tab title="Multi-Cluster Mode" %}
In a multi-cluster architecture, you can set up Gateways on different Kubernetes clusters or virtual machines, then use an operator to generate an API definition that is accessible from each of these Gateways. This means that:

* An APIM instance is required to act as a source of truth for the Gateways
* The operator will obtain the API definition from APIM instead of creating one in a ConfigMap
* The API definition requires a Management Context
* The `local` flag of the API definition must be set to `false`

The following snippet contains the relevant specification properties for the API definition in a multi-cluster architecture:

```yaml
apiVersion: gravitee.io/v1alpha1
kind: ApiDefinition
metadata:
  name: multi-cluster-api
spec:
  contextRef:
    name: apim-ctx
    namespace: gravitee
  local: false
  # [...]
```

An overview of this architecture is described by the diagram below.

<figure><img src="../../../../.gitbook/assets/k8s multi-cluster mode.png" alt=""><figcaption><p>One operator, multiple clusters/regions</p></figcaption></figure>
{% endtab %}
{% endtabs %}
