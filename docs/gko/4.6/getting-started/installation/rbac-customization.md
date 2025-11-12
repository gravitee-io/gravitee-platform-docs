---
description: RBAC customization for GKO
---

# RBAC customization

## Introduction

Kubernetes role-based access control (RBAC) mechanism is a method of regulating access to computer or network resources based on the roles of individual users within your organization. When you use RBAC, you must be familiar with the following two modes (scopes) that you can install GKO in:

* Cluster scope
* Namespaced Mode

### Cluster Scope

With Cluster scope, there is normally a single Gravitee Kubernetes Operator (GKO) instance running in the cluster that is watching several namespaces in the cluster. In this case, GKO needs to have Cluster-Role and Cluster-Role-bindings assigned to it to have access to different resources. For example, CRDs or secrets, and ConfigMaps in different namespaces.

### Namespaced Mode

With Namespaced Mode, GKO only listens to a single namespace or specific namespaces. So, it does not need to have broad access to all the resources at the cluster level.

## Required Resources for GKO

The following diagram provides a visual breakdown of the resources GKO might need access to, along with the corresponding permissions required for each.

<figure><img src="../../.gitbook/assets/image (18).png" alt=""><figcaption><p>GKO required permissions</p></figcaption></figure>

GKO needs access to the following resources:

1. **GKO Admission/Mutation webhooks**: We create the following two webhooks, and we need to have GET/UPDATE access to them: _gko-validating-webhook-configurations_ and _gko-mutating-webhook-configurations._
2. **All GKO CRDs**: GKO needs to have access to all our CRDs and their finalizers. For example, APIDefinition, Application, and Subscription.
3. We expect at least the following access to our resources: GET, UPDATE, LIST and WATCH. For finalizers, we need to have UPDATE access to our finalizers. If you want GKO to automatically apply CRD updates on "helm upgrades", then GKO also needs to be able to GET, CREATE, and PATTCH our CRDs at the cluster level.
4. **ConfigMaps**: We might need to have access to ConfigMaps for 2 reasons:
   1. &#x20;You try to use GKO [templating](/gravitee-kubernetes-operator-gko/guides/templating). For more information about templating, see [templating.md](docs/gko/4.6/guides/templating.md "mention").
   2. You do not want to use APIM, and you want to only install our CRDs locally. In this case, GKO writes the API definitions to ConfigMaps. GKO needs the proper permissions to CREATE, UPDATE, LIST, and DELETE ConfigMaps.
5. **Secrets**: GKO needs to have GET, CREATE and UPDATE access to its secret, which is used for our Admission/Mutation webhook. By default, it is called **gko-webhook-cert**. Also, if you are using  GKO templating, we might need to have access to your secrets. For more information about templating, see [templating.md](docs/gko/4.6/guides/templating.md "mention"). If you use GKO to handle your ingress resources, GKO needs access to all the secrets that are referred to inside your Ingress resources.
6. **Ingress**: If you want APIM Gateway as your ingress controller, GKO needs the following access to your Ingress Resources, GET, UPDATE, WATCH and LIST.
7. **Tokenreviews**: If you want to enable, GKO rbacProxy, we need to have Cluster-Role to create this resource.

## Default RBAC Settings in GKO

1. GET, UPDATE, WATCH, and LIST access to all our CRDs in the whole cluster. We assume that users install a single instance of GKO in one namespace; but they deploy their CRDs in several namespaces. For example, you might have DEV, TEST, PROD environments, or you have different namespaces for each team. So, GKO needs to have access to the resources in all these namespaces. If you watch only specific namespaces, the RBAC adjusts accordingly, and GKO has access only to the CRDs in those specified namespaces.
2. GET, UPDATE, WATCH, and LIST access to all Secrets and ConfigMaps in the whole cluster. GKO needs this access for the following reasons:
   1. We assume that people use GKO templating in different namespaces, and GKO needs to have access to these two resources.&#x20;
   2. if you want to apply the CRDs locally without relying on Management Context and mAPI console, GKO also need to CREATE/DELETE ConfigMaps .
3. GET, CREATE, UPDATE to the secret that we create or update for our Admission and Mutation Webhooks. By default, this secret is called **"gko-webhook-cert"** .
4. Create and update access to our Admission and Mutation webhook resources.

## Modify GKO RBAC Settings

Here are the following values that you can use to adjust RBAC.

```yaml
manager:
  scope:
    cluster: true # set to false so GKO will listen only to its own Namespace

    # you can specify namespaces that GKO is listening to 
    # please bear in mind that if you set namespaces in here, then you need to keep the cluster scope as "true"
    namespaces: ["ns1", "ns2", "ns3"]

  # This feature is deprecated and will be replaced in a future release. If true, the manager will patch Custom Resource Definitions on startup.
  applyCRDs: true # set to false if you want to manually apply latest GKO CRDs in your cluster

  webhook:
    cert:
      secret:
        name: gko-webhook-cert # you can change the secret name if needed

rbac:
  create: true # set to false if you don't want GKO to create/configure RBAC
```

### Cluster Scope

By default, GKO applies its RBAC using Cluster-Role and Cluster-Role-Binding in cluster scope. You do not need to modify anything.

### Namespaced Scope

If you use GKO on specific namespaces, you have to sue the following values to allow GKO modify RBAC for you:

```yaml
manager:
  scope:
    cluster: true
    namespaces: ["ns1", "ns2", "ns3"]
```

In this case, GKO only has access to the resources in those specified namespaces.

### Single Namespaced Scope

If you want GKO to watch only its namespace, you can set the following helm values:&#x20;

```yaml
manager:
  scope:
    cluster: false
```

With this configuration, GKO does not have access to any other namespaces for resources like Secrets or ConfigMaps.

### Disable GKO RBAC Creation

To disable GKO RBAC creation, see the following values in your helm chart:

```yaml
serviceAccount:
  create: false  # GKO will not create SA automatically
  name: gko-controller-manager # You can also modify the name if needed

rbac:
  create: false # GKO will NOT create any RBAC automatically
```

## Customizing RBAC Manually

You can customize RBAC with Gravitee's RBAC templates. To learn more about Gravitee's templates, go to [GitHub](https://github.com/gravitee-io/gravitee-kubernetes-operator/tree/master/helm/gko/templates/rbac).

Here is a summary of what is needed for GKO to work properly:

### Required Permissions for GKO CRDs

* GKO needs GET, UPDATE, WATCH and LIST to all our CRDs. GKO needs to  reconcile your resources when they are applied. This can be both Role or ClusterRole. Here is a generic ClusterRole example that you can apply in your cluster:

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
  - verbs:
      - update
    apiGroups:
      - gravitee.io
    resources:
      - subscriptions/finalizers
  - verbs:
      - get
      - patch
      - update
    apiGroups:
      - gravitee.io
    resources:
      - subscriptions/status
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - gravitee.io
    resources:
      - groups
  - verbs:
      - update
    apiGroups:
      - gravitee.io
    resources:
      - groups/finalizers
  - verbs:
      - get
      - update
    apiGroups:
      - gravitee.io
    resources:
      - groups/status
  - verbs:
      - get
      - list
      - update
      - watch
    apiGroups:
      - gravitee.io
    resources:
      - sharedpolicygroups
  - verbs:
      - update
    apiGroups:
      - gravitee.io
    resources:
      - sharedpolicygroups/finalizers
  - verbs:
      - get
      - update
    apiGroups:
      - gravitee.io
    resources:
      - sharedpolicygroups/status
```

* GKO ClusterRole to GET, CREATE, PATCH our CRDs, only if you want GKO to apply the updated versions of our CRDs on "helm upgrades". If you want to do this manually, there is no reason to provide this access.

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

* **ClusterRole is required** for Admission/Mutation webhooks.

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

### (Optional) ConfigMaps &#x20;

* This can be applied in both Cluster or Namespaced mode

GKO can work without having access to any ConfigMaps. And if you don't want to use ConfigMaps for GKO Templating or if you don't want to deploy your CRDs locally, they you don't need to apply any changes for ConfigMaps.

But If you just want to use GKO templating and you already know the name of ConfigMaps that you might be using, then you can only give access to those specific ConfigMaps.

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
    resourceNames: ["my-cofig-1", "my-config-2"]
```

If you want to apply CRDs locally, then you need to give GKO GET, CREATE, UPDATE,   LIST and DELETE access to your ConfigMaps. This is because GKO needs to create/update and delete ConfigMaps for each APIDefinition CRD.

### Secrets&#x20;

* This can be applied in both Cluster or Namespaced mode

The only secret that GKO needs to have access to work is called "gko-webhook-cert", which is required for our Admission/Mutation to work. GKO needs GET, CREATE and UPDATE access to this secret. The name can be changed using the following values:

```yaml
manager:
  webhook:
    cert:
      secret:
        name: gko-webhook-cert
```

### (Cluster-) Role

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

If you are not using GKO templating and you do not use GKO to handle your Ingress resources, that's the only secret the GKO needs to have access to.

If you use templating, and you already know the name of the secrets that you might use, or you have secrets that you referred to inside your ManagementContext CRDs, then you can give GET, UPDATE and LIST access to those specific secrets.

And if you use GKO for your ingress, then you can also access the GKO access to those specific Secrets if needed.

### Ingress&#x20;

* This can be applied in both Cluster or Namespaced mode

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

### Tokenreviews (Optional)

* This is Cluster level&#x20;

Doesn't need to be applied if you don't use the GKO RBAC proxy.

```yaml
rules:
 - verbs:
 - create
 apiGroups:
 - authentication.k8s.io
 resources:
 - tokenreviews
 - verbs:
 - create
 apiGroups:
 - authorization.k8s.io
 resources:
 - subjectaccessreviews
```

The RBAC Proxy can be disabled using:

```yaml
rbacProxy:
  enabled: false
```
