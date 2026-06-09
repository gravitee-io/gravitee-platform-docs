---
description: Information about kubernetes.
metaLinks:
  alternates:
    - ./
hidden: true
noIndex: true
---

# Kubernetes

## Deployment methods

* [Vanilla Kubernetes](vanilla-kubernetes/)
* [AWS EKS](aws-eks.md)
* [Azure AKS](azure-aks.md)
* [OpenShift](openshift.md)
* GCP GKE

## Proxy configuration

To route Gateway traffic through a corporate proxy (for example, for backend API calls or JWKS retrieval from external identity providers like Microsoft Entra ID), add the following `gravitee_system_proxy_*` environment variables to the Gateway section of your `values.yaml`:

```yaml
gateway:
  env:
    - name: gravitee_system_proxy_enabled
      value: "true"
    - name: gravitee_system_proxy_type
      value: "HTTP"
    - name: gravitee_system_proxy_host
      value: "<proxy-host>"
    - name: gravitee_system_proxy_port
      value: "<proxy-port>"
    - name: gravitee_system_proxy_https_host
      value: "<proxy-host>"
    - name: gravitee_system_proxy_https_port
      value: "<proxy-port>"
```

For the full configuration reference including proxy authentication and `gravitee.yml` equivalents, see [Configure Helm values](../proxy-configuration/system-proxy-for-backend-apis.md#configure-helm-values). For an overview of all proxy methods, see [Proxy Configuration](../proxy-configuration/).

## Ingress body size limit

Kubernetes deployments that front APIM components with the NGINX Ingress Controller are subject to a request body size limit enforced by the ingress, not by Gravitee. When a client sends a request larger than this limit, the ingress rejects it with `413 Request Entity Too Large` before the request reaches any Gravitee component.

The APIM Helm chart doesn't set a body size annotation on any ingress by default. If requests to the Gateway, the Management API, or the Portal API exceed the limit configured on your ingress controller, raise the limit by setting the `nginx.ingress.kubernetes.io/proxy-body-size` annotation on the affected ingress.

The APIM Helm chart doesn't set a body size annotation on any ingress by default. If requests to the Gateway, the Management API, or the Portal API exceed the limit configured on your ingress controller, raise the limit by setting the `nginx.ingress.kubernetes.io/proxy-body-size` annotation on the affected ingress.

{% hint style="info" %}
`nginx.ingress.kubernetes.io/proxy-body-size` is an annotation of the NGINX Ingress Controller. For the annotation's default, accepted value format, and the `0` setting that disables the check entirely, see the [NGINX Ingress Controller annotation reference](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#custom-max-body-size). If your cluster uses a different ingress controller, refer to that controller's documentation for the equivalent setting.
{% endhint %}

### Apply the annotation to each ingress

Each APIM component exposes its ingress through a separate Helm value path. Set `proxy-body-size` on every ingress whose traffic carries request bodies you need to accept:

| Ingress           | Helm value path                      | Traffic                                                                                                                                                                      |
| ----------------- | ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gateway dataplane | `gateway.ingress.annotations`        | Incoming API calls from consumers to the Gateway. Size this to the largest request body an API on the Gateway accepts.                                                       |
| Management API    | `api.ingress.management.annotations` | Calls to the Management REST API, including API imports, policy definitions, and configuration uploads. Size this to the largest import or configuration payload you submit. |
| Portal API        | `api.ingress.portal.annotations`     | Calls to the Portal REST API from the Developer Portal. Size this if consumers submit large payloads through the Portal.                                                     |

The following excerpt shows the annotation applied to the Gateway and Management API ingresses in `values.yaml`:

```yaml
api:
  ingress:
    management:
      annotations:
        kubernetes.io/ingress.class: nginx
        nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    portal:
      annotations:
        kubernetes.io/ingress.class: nginx
        nginx.ingress.kubernetes.io/proxy-body-size: "50m"

gateway:
  ingress:
    annotations:
      kubernetes.io/ingress.class: nginx
      nginx.ingress.kubernetes.io/proxy-body-size: "50m"
```

The `50m` value is an example, not a recommended default. Set each limit based on the largest payload you expect to send through that ingress.

### Hybrid Gateway deployments

In a Hybrid Gateway deployment, only the Gateway ingress runs in your cluster. The Management API and Portal API run in the Gravitee Cloud control plane, so their ingresses aren't part of your Helm values. Apply `proxy-body-size` to `gateway.ingress.annotations` to raise the Gateway dataplane limit for the Hybrid cluster you manage. For the body size limits enforced by Gravitee Cloud on the control-plane side, contact Gravitee support.

## Harden the security context

All APIM container images run as non-root users by default. The Helm chart configures a `securityContext` on each component's deployment that enforces non-root execution.

#### Default security context values

The following table lists the default container-level `securityContext` values for each APIM component:

| Component        | Helm value path                      | `runAsUser` | `runAsGroup` | `runAsNonRoot` |
| ---------------- | ------------------------------------ | ----------- | ------------ | -------------- |
| Management API   | `api.deployment.securityContext`     | `1001`      | -            | `true`         |
| Gateway          | `gateway.deployment.securityContext` | `1001`      | -            | `true`         |
| Console UI       | `ui.deployment.securityContext`      | `101`       | `101`        | `true`         |
| Developer Portal | `portal.deployment.securityContext`  | `101`       | `101`        | `true`         |
| Init containers  | `initContainers.securityContext`     | `1001`      | -            | `true`         |

Each component also supports a pod-level `podSecurityContext` (for example, `api.deployment.podSecurityContext`) for settings like `fsGroup` that apply to all containers in the pod.

#### Apply additional hardening

To restrict privilege escalation, drop all Linux capabilities, and apply a seccomp profile, add the following to your `values.yaml`:

```yaml
api:
  deployment:
    securityContext:
      runAsUser: 1001
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault

gateway:
  deployment:
    securityContext:
      runAsUser: 1001
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault

ui:
  deployment:
    securityContext:
      runAsUser: 101
      runAsGroup: 101
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault

portal:
  deployment:
    securityContext:
      runAsUser: 101
      runAsGroup: 101
      runAsNonRoot: true
      allowPrivilegeEscalation: false
      capabilities:
        drop: ["ALL"]
      seccompProfile:
        type: RuntimeDefault

initContainers:
  securityContext:
    runAsUser: 1001
    runAsNonRoot: true
    allowPrivilegeEscalation: false
    capabilities:
      drop: ["ALL"]
    seccompProfile:
      type: RuntimeDefault
```

These settings prevent containers from gaining elevated privileges at runtime and align with the Kubernetes [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) `restricted` profile.

{% hint style="info" %}
For OpenShift deployments, set `runAsUser` and `runAsGroup` to `null` instead of explicit UIDs. OpenShift assigns UIDs from a namespace-specific range. For the full OpenShift configuration, see [OpenShift.](openshift.md)
{% endhint %}
