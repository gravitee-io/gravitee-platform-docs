---
description: Overview of Access Control Configurations.
noIndex: true
---

# Role-based Access Control Configurations

Blackbird cluster (powered by Telepresence) allows you to manage permissions for components in a cluster for security purposes using role-based access control (RBAC). RBAC is a security model used to restrict system access based on a user's role within an organization. Instead of assigning permissions directly to individuals, RBAC assigns permissions to roles, and users are then assigned to those roles.

Using this page, you can learn about:

* [Editing your kubeconfig file](role-based-access-control-configurations.md#editing-your-kubeconfig-file)
* [Administrative access configurations](role-based-access-control-configurations.md#administrative-access-configurations)
* [Cluster-wide access configurations](role-based-access-control-configurations.md#cluster-wide-user-access)
* [Namespace access configurations](role-based-access-control-configurations.md#namespace-access-configurations)

> **Note:** This page uses service accounts to assign roles and bindings, but there are other methods of RBAC administration and enforcement available. For more information, see [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) in the Kubernetes documentation.

## Prerequisites

* You have a version of Kubernetes that's 1.16 or higher.
* You have cluster administration permissions to apply RBAC.
* You're using a kubeconfig file that's specified by the `KUBECONFIG` environment variable.

## Editing your kubeconfig file

Your kubeconfig file is a YAML file that contains the cluster's API endpoint information and the user data that's supplied for authentication. In the example below, the service account name is `tp-user`. You can replace this name with any value, as long as references to the service account are consistent throughout the YAML file. After an administrator has applied the RBAC configuration, the user needs to create a `config.yaml` in their current directory. Use the following example as a template.

```yaml
apiVersion: v1
kind: Config
clusters:
- name: my-cluster # Must match the cluster value in the contexts config.
  cluster:
    ## The cluster field is highly cloud dependent.
contexts:
- name: my-context
  context:
    cluster: my-cluster # Must match the name field in the clusters config.
    user: tp-user
users:
- name: tp-user # Must match the name of the service account created by the cluster administrator.
  user:
    token: <service-account-token> # See the following note.
```

The cluster administrator can obtain the service account token after they create the user's service account. Creating the service account will create an associated Secret in the same namespace with the format `<service-account-name>-token-<uuid>`. Your cluster administrator can obtain this token by running `kubectl get secret -n ambassador <service-account-secret-name> -o jsonpath='{.data.token}' | base64 -d`.

After the user creates a `config.yaml` in their current directory, they can export the file's location to `KUBECONFIG` by running `export KUBECONFIG=$(pwd)/config.yaml`. Then, they can switch to this context by running `kubectl config use-context my-context`.

## Administrative access configurations

Administrating Blackbird clusters (powered by Telepresence) requires permissions for creating `Namespaces`, `ServiceAccounts`, `ClusterRoles`, `ClusterRoleBindings`, `Secrets`, `Services`, and `MutatingWebhookConfiguration`, along with the ability to deploy the `traffic-manager`, which is typically done by a full cluster administrator. The following permissions are required for administration.

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: telepresence-admin
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: telepresence-admin-role
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "create", "delete", "watch"]
  - apiGroups: [""]
    resources: ["services"]
    verbs: ["get", "list", "update", "create", "delete"]
  - apiGroups: [""]
    resources: ["pods/portforward"]
    verbs: ["create"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets", "statefulsets"]
    verbs: ["get", "list", "update", "create", "delete", "watch"]
  - apiGroups: ["rbac.authorization.k8s.io"]
    resources: ["clusterroles", "clusterrolebindings", "roles", "rolebindings"]
    verbs: ["get", "list", "watch", "create", "delete"]
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["create"]
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list", "watch", "delete"]
    resourceNames: ["telepresence-agents"]
  - apiGroups: [""]
    resources: ["namespaces"]
    verbs: ["get", "list", "watch", "create"]
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "create", "list", "delete"]
  - apiGroups: [""]
    resources: ["serviceaccounts"]
    verbs: ["get", "create", "delete"]
  - apiGroups: ["admissionregistration.k8s.io"]
    resources: ["mutatingwebhookconfigurations"]
    verbs: ["get", "create", "delete"]
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["list", "get", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: telepresence-clusterrolebinding
subjects:
  - name: telepresence-admin
    kind: ServiceAccount
    namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  name: telepresence-admin-role
  kind: ClusterRole
```

## Cluster-wide user access

Administrators can allow a user to make intercepts across all namespaces with more limited `kubectl` permissions using the following `ServiceAccount`, `ClusterRole`, and `ClusterRoleBinding` RBAC configurations. This provides full `blackbird cluster intercept` functionality.

> **Note:** To use the following RBAC configurations, you must have a Traffic Manager deployment set up by an administrator.

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tp-user                                       # Update value for appropriate value
  namespace: ambassador                                # Traffic-Manager is deployed to Ambassador namespace
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: telepresence-role
rules:
# For gather-logs command
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list"]
# Needed in order to maintain a list of workloads
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets", "statefulsets"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["namespaces", "services"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: telepresence-rolebinding
subjects:
- name: tp-user
  kind: ServiceAccount
  namespace: ambassador
roleRef:
  apiGroup: rbac.authorization.k8s.io
  name: telepresence-role
  kind: ClusterRole
```

### Traffic Manager connect permissions

Along with cluster-wide permissions, the client must have the following namespace-scoped permissions in the Traffic Manager's namespace to set up the necessary port forward.

```yaml
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name:  traffic-manager-connect
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods/portforward"]
    verbs: ["create"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: traffic-manager-connect
subjects:
  - name: telepresence-test-developer
    kind: ServiceAccount
    namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  name: traffic-manager-connect
  kind: Role
```

## Namespace access configurations

Administrators can also implement RBAC configurations for multi-tenant environments where multiple development teams share a single cluster, with users restricted to a specific namespace.

> **Note:** To use the following RBAC configurations, you must have a Traffic Manager deployment set up by an administrator and [Traffic Manager connect permissions](role-based-access-control-configurations.md#traffic-manager-connect-permissions).

For each accessible namespace:

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tp-user             # Update value for appropriate user name
  namespace: tp-namespace   # Update value for appropriate namespace
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name:  telepresence-role
  namespace: tp-namespace    # Should be the same as metadata.namespace of above  ServiceAccount
rules:
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets", "statefulsets"]
  verbs: ["get", "list", "watch"]
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: telepresence-role-binding
  namespace: tp-namespace   # Should be the same as metadata.namespace of above  ServiceAccount
subjects:
- kind: ServiceAccount
  name: tp-user             # Should be the same as metadata.name of above ServiceAccount
roleRef:
  kind: Role
  name: telepresence-role
  apiGroup: rbac.authorization.k8s.io
```
