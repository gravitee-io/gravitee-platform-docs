---
description: Information about kubernetes.
metaLinks:
  alternates:
    - ./
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
