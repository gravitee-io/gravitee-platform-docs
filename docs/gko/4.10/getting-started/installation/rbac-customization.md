---
description: RBAC customization for GKO
---


# RBAC Customization

## Introduction

The Kubernetes Role-Based Access Control (RBAC) mechanism is essential for regulating access to cluster resources. When deploying the Gravitee Kubernetes Operator (GKO), it's crucial to understand the two primary operational modes (scopes) that dictate its required permissions:

* Cluster Scope
* Namespaced Scope

### Cluster Scope

In Cluster Scope, a single GKO instance typically runs within the cluster, monitoring resources across multiple namespaces. To function effectively, the GKO requires ClusterRole and ClusterRoleBinding resources. These grant the necessary cluster-level access to various resources, such as Custom Resource Definitions (CRDs) and Secrets or ConfigMaps residing in different namespaces.

### Namespaced Scope

In Namespaced Scope, the GKO only monitors a single namespace or a predefined list of specific namespaces. Consequently, it does not require the broad, cluster-level access needed in the Cluster Scope mode.

## Required Resources

The following diagram provides a visual breakdown of the resources the GKO might need access to, along with the corresponding permissions required for each.

<figure><img src="../../.gitbook/assets/image (18).png" alt=""><figcaption><p>GKO Required Permissions</p></figcaption></figure>

The GKO requires access to the following resources:

1.  GKO Admission/Mutation Webhooks: The Operator creates the following two webhooks and requires GET/UPDATE access to them: gko-validating-webhook-configurations and gko-mutating-webhook-configurations.
2.  All GKO CRDs: The GKO requires access to all its CRDs and their finalizers (e.g., APIDefinition, Application, and Subscription). The expected access level for the CRD resources is GET, UPDATE, LIST, and WATCH. For finalizers, UPDATE access is required. If you configure the GKO to automatically apply CRD updates during Helm upgrades, the GKO will also need GET, CREATE, and PATCH access to its CRDs at the cluster level.
3.  ConfigMaps: Access to ConfigMaps may be required for two reasons:
    a. You are using GKO templating for dynamic configuration (for more information, see [templating.md](docs/gko/4.10/guides/templating.md "mention")).
    b. You are deploying CRDs locally without using APIM. In this scenario, the GKO writes the API definitions to ConfigMaps and requires the proper permissions (CREATE, UPDATE, LIST, and DELETE) to manage these resources.
4.  Secrets: The GKO requires GET, CREATE, and UPDATE access to its dedicated secret (default name: gko-webhook-cert), which is used for the Admission/Mutation webhook. If you use GKO templating, the GKO may also require access to your specific secrets (for more information, see [templating.md](docs/gko/4.10/guides/templating.md "mention")). Additionally, if the GKO is managing your Ingress resources, it will need access to all Secrets referenced within those resources.
5.  Ingress: If you intend to use the APIM Gateway as your ingress controller, the GKO requires the following access to your Ingress Resources: GET, UPDATE, WATCH, and LIST.
6.  TokenReviews: To enable the optional GKO rbacProxy, a ClusterRole is needed to allow the GKO to create this resource.

## Default RBAC Settings

The default RBAC configuration grants the GKO access for the following primary reasons:

1.  It is assumed that users may utilize GKO templating across different namespaces, necessitating access to the related resources.
2.  To support users who apply CRDs locally without relying on a Management Context or mAPI console, the GKO requires CREATE/DELETE access to ConfigMaps.
3.  It requires GET, CREATE, and UPDATE access to the secret (gko-webhook-cert by default) created or updated for the Admission and Mutation Webhooks.
4.  It requires CREATE and UPDATE access to the Admission and Mutation webhook resources themselves.

## Modify GKO RBAC Settings

The following values can be used in your Helm chart to adjust the GKO's RBAC settings.

```yaml
manager:
  scope:
    cluster: true # set to false for Namespaced Scope: GKO will only watch its own Namespace

    # You can specify namespaces that GKO monitors.
    # Note: If namespaces are explicitly set here, the 'cluster' scope must remain 'true'.
    namespaces: ["ns1", "ns2", "ns3"]

  # This feature is deprecated and will be replaced in a future release. If true, the manager will patch Custom Resource Definitions on startup.
  applyCRDs: true # set to false if you want to manually apply the latest GKO CRDs in your cluster

  webhook:
    cert:
      secret:
        name: gko-webhook-cert # The secret name can be customized
        
rbac:
  create: true # set to false if you don't want GKO to automatically create/configure RBAC
````

### Cluster Scope

By default, the GKO applies its RBAC configuration using a ClusterRole and ClusterRoleBinding at the cluster level. No modification is required for this default behavior.

### Namespaced Scope

If you want the GKO to monitor a specific list of namespaces, use the following configuration to allow the GKO to modify the necessary RBAC resources:

```yaml
manager:
  scope:
    cluster: true
    namespaces: ["ns1", "ns2", "ns3"]
```

With this setting, the GKO will only have access to resources within the specified namespaces.

### Single Namespaced Scope

To configure the GKO to only monitor its own namespace, set the following Helm values:

```yaml
manager:
  scope:
    cluster: false
```

In this configuration, the GKO will not have access to resources like Secrets or ConfigMaps in any other namespace.

### Disable GKO RBAC Creation

To prevent the GKO from automatically creating and configuring RBAC resources, use the following values in your Helm chart:

```yaml
serviceAccount:
  create: false  # GKO will not create the Service Account automatically
  name: gko-controller-manager # The ServiceAccount name can also be modified

rbac:
  create: false # GKO will NOT create any RBAC resources automatically
```

## Customizing RBAC Manually

You can manually customize the RBAC settings using Gravitee's provided RBAC templates. To review these templates, refer to the following files in the Gravitee Kubernetes Operator GitHub repository:

  * For single-namespace deployments: [manager-role.yaml](https://www.google.com/search?q=https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/helm/gko/templates/rbac/manager-role.yaml)
  * For multi-namespace (cluster) deployments: [manager-cluster-role.yaml](https://www.google.com/search?q=https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/helm/gko/templates/rbac/manager-cluster-role.yaml)

Here is a summary of the minimum permissions required for the GKO to function correctly:

### Required Permissions for GKO CRDs

The GKO requires GET, UPDATE, WATCH, and LIST access to all of its CRDs to reconcile the resources when they are applied. This access can be granted via a Role (for Namespaced Scope) or a ClusterRole (for Cluster Scope).

Below is a generic ClusterRole example:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: gko-controller-manager-cluster-role
rules:
  - verbs:
      - create
      - get
      - list
      - update
      - watch
    apiGroups:
      - ''
    resources:
      - secrets
  - verbs:
      - create
      - delete
      - get
      - list
      - update
      - watch
    apiGroups:
      - ''
    resources:
      - configmaps
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - gravitee.io
    resources:
      - apidefinitions
  - verbs:
      - update
    apiGroups:
      - gravitee.io
    resources:
      - apidefinitions/finalizers
  - verbs:
      - get
      - update
    apiGroups:
      - gravitee.io
    resources:
      - apidefinitions/status
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - gravitee.io
    resources:
      - apiv4definitions
  - verbs:
      - update
    apiGroups:
      - gravitee.io
    resources:
      - apiv4definitions/finalizers
  - verbs:
      - get
      - update
    apiGroups:
      - gravitee.io
    resources:
      - apiv4definitions/status
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - gravitee.io
    resources:
      - apiresources
  - verbs:
      - update
    apiGroups:
      - gravitee.io
    resources:
      - apiresources/finalizers
  - verbs:
      - get
      - update
    apiGroups:
      - gravitee.io
    resources:
      - apiresources/status
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - gravitee.io
    resources:
      - managementcontexts
  - verbs:
      - update
    apiGroups:
      - gravitee.io
    resources:
      - managementcontexts/finalizers
  - verbs:
      - get
      - update
    apiGroups:
      - gravitee.io
    resources:
      - managementcontexts/status
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - networking.k8s.io
    resources:
      - ingresses
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - gravitee.io
    resources:
      - applications
  - verbs:
      - update
    apiGroups:
      - gravitee.io
    resources:
      - applications/finalizers
  - verbs:
      - get
      - update
    apiGroups:
      - gravitee.io
    resources:
      - applications/status
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - gravitee.io
    resources:
      - subscriptions
```

A second ClusterRole is needed to grant the GKO GET, CREATE, and PATCH access to its CRDs only if you want the GKO to apply updated CRD versions during Helm upgrades. If you prefer to manage CRD updates manually, this access is not required.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: gko-controller-manager-crd-patch-cluster-role
rules:
  - verbs:
      - get
    apiGroups:
      - apiextensions.k8s.io
    resources:
      - customresourcedefinitions
  - verbs:
      - patch
      - create
    apiGroups:
      - apiextensions.k8s.io
    resources:
      - customresourcedefinitions
    resourceNames:
      - managementcontexts.gravitee.io
      - apidefinitions.gravitee.io
      - apiv4definitions.gravitee.io
      - applications.gravitee.io
      - apiresources.gravitee.io
      - subscriptions.gravitee.io
      - sharedpolicygroups.gravitee.io
      - groups.gravitee.io
  - verbs:
      - create
      - patch
    apiGroups:
      - ''
    resources:
      - events
```

### GKO Admission/Mutation Webhooks

A ClusterRole is required for the Admission/Mutation webhooks. More details can be found in the [admission-webhook-cluster-role.yaml file in the GitHub repository.](https://www.google.com/search?q=https://github.com/gravitee-io/gravitee-kubernetes-operator/blob/master/helm/gko/templates/rbac/admission-webhook-cluster-role.yaml)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: gko-controller-manager-validation-webhook-cluster-role
rules:
  - verbs:
      - get
      - update
    apiGroups:
      - admissionregistration.k8s.io
    resources:
      - validatingwebhookconfigurations
    resourceNames:
      - gko-validating-webhook-configurations
  - verbs:
      - get
      - update
    apiGroups:
      - admissionregistration.k8s.io
    resources:
      - mutatingwebhookconfigurations
    resourceNames:
      - gko-mutating-webhook-configurations
```

### (Optional) ConfigMaps

Permissions for ConfigMaps can be applied in either Cluster or Namespaced scope.

The GKO can operate without access to any ConfigMaps. If you do not plan to use ConfigMaps for GKO Templating or for deploying CRDs locally, you do not need to apply any ConfigMap-related permissions.

If you are only using GKO templating and know the names of the ConfigMaps that will be used, you can limit access to those specific resources:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: gko-controller-manager-role-configmaps
rules:
  - verbs:
      - get
      - update
    apiGroups:
      - ''
    resources:
      - configmaps
    resourceNames: ["my-config-1", "my-config-2"]
```

If you intend to apply CRDs locally, the GKO will need GET, CREATE, UPDATE, LIST, and DELETE access to ConfigMaps, as it manages a ConfigMap for each APIDefinition CRD.

### Secrets

Permissions for Secrets can be applied in either Cluster or Namespaced scope.

The only secret the GKO absolutely requires access to is the gko-webhook-cert secret, which is necessary for the Admission/Mutation webhooks to function. The GKO needs GET, CREATE, and UPDATE access to this secret. Its name can be customized using the following values:

```yaml
manager:
  webhook:
    cert:
      secret:
        name: gko-webhook-cert
```

#### (Cluster-) Role for Webhook Secret

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: gko-controller-manager-role-secrets
rules:
  - verbs:
      - create
      - get
      - update
    apiGroups:
      - ''
    resources:
      - secrets
    resourceNames: ["gko-webhook-cert"]
```

If you are not using GKO templating and the GKO is not managing your Ingress resources, this is the only Secret access required.

If you are using templating, and you know the names of the secrets you will reference (either directly or within ManagementContext CRDs), you can grant GET, UPDATE, and LIST access to those specific secrets.

If the GKO is managing your Ingress resources, it will need access to any Secrets referenced within those Ingress resources.

### Ingress

Permissions for Ingress resources can be applied in either Cluster or Namespaced scope.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: gko-controller-manager-cluster-role-ingress
rules:
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - networking.k8s.io
    resources:
      - ingresses
```
