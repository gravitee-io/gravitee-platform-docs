---
description: Restrict who can create Ambassador Edge Stack resources with Kubernetes RBAC.
noIndex: true
---

# Controlling Who Can Configure Ambassador Edge Stack

Ambassador Edge Stack is configured with Kubernetes resources, such as `Mapping`, `Host`, and `AuthService`. Ambassador Edge Stack doesn't decide who can create those resources. Kubernetes role-based access control (RBAC) does. This page explains why that permission needs the same care as administrator access to the gateway, and shows example roles that you can start from.

## Who can create Edge Stack resources

Treat permission to create or change any Ambassador Edge Stack resource as administrator-level access to the gateway, even when it's limited to a single namespace. This applies to every kind in the `getambassador.io` and `gateway.getambassador.io` API groups, including the following:

* `Mapping` and `TCPMapping`
* `AuthService`, `RateLimitService`, `LogService`, and `TracingService`
* `Filter`, `FilterPolicy`, `WebApplicationFirewall`, and `WebApplicationFirewallPolicy`
* `Module`, `Listener`, `Host`, and `TLSContext`
* `KubernetesEndpointResolver`, `KubernetesServiceResolver`, and `ConsulResolver`
* `RateLimit`, `DevPortal`, `EnvoyFilter`, and `EnvoyFilterPolicy`

To list the kinds that your installation supports, run `kubectl api-resources --api-group=getambassador.io` and `kubectl api-resources --api-group=gateway.getambassador.io`.

### Why this permission is administrator-level

* **These resources choose where Ambassador Edge Stack connects.** The `service` of a `Mapping`, and the address of an `AuthService`, `RateLimitService`, `LogService`, `TracingService`, `Filter`, or `ConsulResolver`, can be any hostname, IP address, or Kubernetes Service that the Ambassador Edge Stack pods can reach. Ambassador Edge Stack connects to it from inside the cluster. This includes Services in other namespaces, internal components of Ambassador Edge Stack such as its Redis instance and admin ports, and cloud provider metadata endpoints. A user who can't reach those addresses directly can reach them through a `Mapping`.
* **A `Mapping` can expose data from the Ambassador Edge Stack container.** `error_response_overrides` with `text_format_source` returns the contents of any file that the Ambassador Edge Stack container can read as a response body. Headers and response bodies can use Envoy command operators (`%...%`), which expand to data about the request and the proxy. A user who can create a `Mapping` can therefore see data that's available to Ambassador Edge Stack itself.
* **Some resources apply to many routes at once.** A `Module` or `Listener` changes how every request is accepted. A `Host` or `TLSContext` changes how requests for its hostnames are accepted and how TLS is terminated. `Filter`, `FilterPolicy`, and `WebApplicationFirewall` resources change how requests are authenticated and inspected.
* **A `Mapping` can claim routes that other teams own.** A `Mapping` in one team's namespace can use any hostname and prefix that a `Host` accepts, including routes that another team expects to own. A `Host`'s `mappingSelector` limits which `Mapping` resources it accepts by label, but the author of a `Mapping` chooses its labels.

Ambassador Edge Stack also reads most core resources, such as `Mapping`, `Module`, `AuthService`, `Host`, and `TLSContext`, from `getambassador.io/config` annotations on Services and Ingresses. Permission to edit Services or Ingresses in a namespace that Ambassador Edge Stack watches is as powerful as permission to create those resources directly. [`AMBASSADOR_DISABLE_ANNOTATION_MAPPINGS=true`](ambassador-edge-stack-environment-variables-and-ports.md#ambassador_disable_annotation_mappings) stops annotations from defining `Mapping` resources, but annotations can still define the other kinds.

### Example roles

The Ambassador Edge Stack Helm chart (v8.15.0 and later) can install two example ClusterRoles. They're off by default, and the chart doesn't bind them to anyone. To install them, add the following to your Helm values, and then run `helm upgrade`:

```yaml
rbacExamples:
  create: true
```

If you don't use the Helm chart, create the equivalent roles from the following manifests. The chart names them `<release-fullname>-admin` and `<release-fullname>-route-editor` (or uses `rbac.nameOverride` in place of the full name), which is `edge-stack-admin` and `edge-stack-route-editor` for a release named `edge-stack`. The chart creates ClusterRoles, so installing them needs permission to create cluster-scoped RBAC objects.

#### `edge-stack-admin`

This role can manage every Ambassador Edge Stack kind. Grant it only to the people and service accounts that administer the gateway, for example with a ClusterRoleBinding.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: edge-stack-admin
rules:
  # "*" also covers kinds added by future Ambassador Edge Stack releases.
  - apiGroups: ["getambassador.io", "gateway.getambassador.io"]
    resources: ["*"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete", "deletecollection"]
```

#### `edge-stack-route-editor`

This role can manage only `Mapping` resources, in the namespaces where you bind it. Bind it in a namespace with a RoleBinding rather than a ClusterRoleBinding:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: edge-stack-route-editor
rules:
  - apiGroups: ["getambassador.io"]
    resources: ["mappings"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

```bash
kubectl create rolebinding team-a-routes -n team-a --clusterrole=edge-stack-route-editor --group=team-a
```

{% hint style="warning" %}
The route editor role limits which kinds of resources a user can change, which helps prevent mistakes. It isn't a security boundary. A `Mapping` in the bound namespace can still target internal addresses, return files from the Ambassador Edge Stack container through `error_response_overrides`, and claim routes on any `Host` that accepts it. Grant this role only to users that you'd trust with administrator access to Ambassador Edge Stack.

The following steps reduce the risk, but don't remove it:

* Make sure the users can't edit Services or Ingresses in namespaces that Ambassador Edge Stack watches. `AMBASSADOR_DISABLE_ANNOTATION_MAPPINGS=true` only stops annotations from defining `Mapping` resources.
* Restrict the `mappingSelector` of each `Host`, and use an admission policy, for example a Kubernetes ValidatingAdmissionPolicy, to control which labels a `Mapping` in each namespace can set. Don't set `DISABLE_STRICT_LABEL_SELECTORS=true`, which lets a `Host` accept a `Mapping` by hostname alone.
* Enable protection against `Mapping` resources that target internal addresses when it's available. An upcoming Ambassador Edge Stack release adds this as an opt-in setting, `AMBASSADOR_BLOCK_INTERNAL_UPSTREAMS=true`. Check the [release notes](../../release-notes.md) for availability.
{% endhint %}

Neither role is aggregated into the built-in Kubernetes `admin` or `edit` ClusterRoles. Aggregating them would give every namespace administrator or editor the access described on this page.

### Review existing access

Users and service accounts can already hold Ambassador Edge Stack permissions through other roles, for example a ClusterRole that grants `*` on all API groups. To check whether a particular user or service account can create a resource, use `kubectl auth can-i` with impersonation:

```bash
kubectl auth can-i create mappings.getambassador.io --all-namespaces --as=jane@example.com
kubectl auth can-i create mappings.getambassador.io -n team-a --as=system:serviceaccount:team-a:deployer
```

## Protecting Redis

Ambassador Edge Stack stores OAuth2 sessions and rate limit counters in Redis. Starting with Helm chart v8.15.0, the Redis instance that the chart creates requires a password by default. For more information, see [Redis password in the Helm chart](ambassador-edge-stack-and-redis.md#redis-password-in-the-helm-chart).
