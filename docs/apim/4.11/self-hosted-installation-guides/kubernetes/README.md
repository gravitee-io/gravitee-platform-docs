---
description: Information about kubernetes.
metaLinks:
  alternates:
    - ./
---

# Kubernetes

## Deployment methods

* [Vanilla Kubernetes](vanilla-kubernetes/README.md)
* [AWS EKS](aws-eks.md)
* [Azure AKS](azure-aks.md)
* [OpenShift](openshift.md)
* GCP GKE

## Kubernetes version support

The APIM Helm chart requires Kubernetes version 1.14 or later. The chart declares this requirement in its `kubeVersion` field, which Helm validates when you install or upgrade the chart. For details about how Helm applies this constraint, see the [Helm documentation](https://helm.sh/docs/topics/charts/#the-chartyaml-file).

The chart doesn't set an upper Kubernetes version bound, and it doesn't impose version constraints specific to managed Kubernetes services such as Azure AKS, Amazon EKS, or Google GKE. The same minimum Kubernetes version applies to any cluster where you install the chart.

## Pin the chart and image versions

The APIM Helm chart and the APIM product share the same version number. Since chart 4.2.0, the chart version and its `appVersion` are identical, so chart `4.11.x` deploys the APIM `4.11.x` component images.

When you don't set an image tag, the chart derives each component's tag from its `appVersion`: the Gateway and the Management API images default to the `<version>-debian` tag, and the Console and the Developer Portal images default to the `<version>` tag. Pinning the chart version therefore pins the component versions.

Gravitee recommends pinning the chart version in production and pre-production so that a chart repository update or a pod restart never changes the version you run:

```bash
helm repo add graviteeio https://helm.gravitee.io
helm upgrade --install graviteeio-apim graviteeio/apim \
  --namespace gravitee-apim \
  -f values.yaml \
  --version 4.11.16
```

Optional: pin each component's image tag explicitly with the `gateway.image.tag`, `api.image.tag`, `ui.image.tag`, and `portal.image.tag` values for an extra layer of auditability in GitOps workflows. Keep any explicit image tag aligned with the chart version.

{% hint style="warning" %}
Don't use the `latest` image tag in production. The default image `pullPolicy` is `Always`, so a pod restart can pull a newer image without warning. APIM applies forward-only data migrations when a newer Management API version starts, so an uncontrolled upgrade isn't reversible. For more information, see [Upgrade Guides](../../upgrade-guides/README.md).
{% endhint %}

## Configure the chart for production

The chart defaults favor quick starts. The following table lists the chart options to review before you run APIM in production. Replace the `<component>` placeholder with `gateway`, `api`, `ui`, or `portal`.

| Concern | Helm values | Notes |
|:--------|:------------|:------|
| Replicas and autoscaling | `<component>.autoscaling`, `<component>.replicaCount` | Autoscaling is enabled by default with `minReplicas: 1` and `maxReplicas: 3`, and it supports a `behavior` block. `replicaCount` applies only when `autoscaling.enabled` is `false`. |
| Pod disruption budgets | `<component>.pdb` | Disabled by default. Set `enabled: true` with `minAvailable` or `maxUnavailable`. The default `maxUnavailable` is `50%`. |
| Zone and node spreading | `<component>.deployment.affinity`, `<component>.deployment.topologySpreadConstraints` | Empty by default. The chart doesn't generate anti-affinity rules, so supply the full block yourself. |
| Node placement | `<component>.deployment.nodeSelector`, `<component>.deployment.tolerations`, `<component>.priorityClassName` | Empty by default. |
| Resource requests and limits | `<component>.resources` | The defaults are modest. For example, the Gateway ships with a `500m` CPU and `512Mi` memory limit. Size each component per the [sizing guidelines](../../prepare-a-production-environment/gateway-resource-sizing-guidelines.md). |
| Rollout strategy | `<component>.deployment.strategy` | Defaults to `RollingUpdate` with `maxUnavailable: 1`. |
| Graceful shutdown | `<component>.terminationGracePeriod`, `<component>.lifecycle` | The grace period defaults to `30` seconds. `lifecycle` accepts `preStop` and `postStart` commands. |
| Probes | `<component>.deployment.livenessProbe`, `<component>.deployment.readinessProbe`, `<component>.deployment.startupProbe` | For the Management API, Console, and Developer Portal, every probe field is configurable in values. For the Gateway, disable the built-in probe with `enabled: false` and set the matching `customLivenessProbe`, `customReadinessProbe`, or `customStartupProbe` block. |
| Network policy | `networkPolicy` (top level) | Empty by default. The chart renders a single `NetworkPolicy` resource from the spec you provide. |
| Service account and IAM annotations | `apim.managedServiceAccount`, `apim.serviceAccount`, `apim.serviceAccountAnnotations`, `<component>.deployment.serviceAccount` | The chart manages one ServiceAccount by default. `apim.serviceAccountAnnotations` attaches annotations to it, such as an AWS IAM role ARN for IAM Roles for Service Accounts (IRSA). |
| JVM tuning | `<component>.env` | The chart has no dedicated JVM values. Pass JVM-related environment variables through `env`. For memory sizing guidance, see the [sizing guidelines](../../prepare-a-production-environment/gateway-resource-sizing-guidelines.md). |

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

For the full configuration reference including proxy authentication and `gravitee.yml` equivalents, see [Configure Helm values](../proxy-configuration/system-proxy-for-backend-apis.md#configure-helm-values). For an overview of all proxy methods, see [Proxy Configuration](../proxy-configuration/README.md).

## Ingress body size limit

Kubernetes deployments that front APIM components with the NGINX Ingress Controller are subject to a request body size limit enforced by the ingress, not by Gravitee. When a client sends a request larger than this limit, the ingress rejects it with `413 Request Entity Too Large` before the request reaches any Gravitee component.

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
