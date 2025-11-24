---
description: Installation guide for Namespaced Install.
---

# Cluster vs Namespaced Install

The Gravitee Kubernetes Operator (GKO) can either be configured to listen to resources across an entire cluster or scoped to a single namespace. The `manager.scope.cluster` boolean parameter is used to determine which installation method is used by the GKO Helm Chart.

{% tabs %}
{% tab title="Cluster Mode" %}
By default, the Gravitee Kubernetes Operator is set up to listen to the custom resources it owns at the cluster level.

In this mode, a single operator must be installed in the cluster to handle resources, regardless of the namespaces they have been created in. For each resource created in a specific namespace, the operator creates a ConfigMap in the same namespace that contains an API definition that is synced with an APIM Gateway.

By default, an APIM Gateway installed using the Helm Chart includes a limited set of permissions, and the Gateway is only able to access ConfigMaps created in its own namespace. However, giving a Gateway the cluster role allows it to access ConfigMaps created by the operator at the cluster level.

An overview of this architecture is described by the diagram below.

<figure><img src="broken-reference" alt=""><figcaption><p>Default Cluster Mode architecture</p></figcaption></figure>
{% endtab %}

{% tab title="Namespaced Mode" %}
The Gravitee Kubernetes Operator can be set up to listen to a single namespace in a Kubernetes cluster. One operator is deployed per namespace, and each listens to the custom resources created in its namespace only.

To achieve this architecture, the `manager.scope.cluster` value must be set to `false` during the Helm install. Role names are computed from the service account name, so each install must set a dedicated service account name for each operator using the `serviceAccount.name` Helm value.

To ensure the webhook configuration used by each namespaced operator is unique and accessible only to the service account defined using the `serviceAccount.name` value, set `manager.webhook.configuration.useAutoUniqueNames` to `true`.

An overview of this architecture is described by the diagram below.

<figure><img src="broken-reference" alt=""><figcaption><p>Multiple operators, each listening to its own namespace</p></figcaption></figure>
{% endtab %}
{% endtabs %}
