---
description: Configuration guide for deployments.
metaLinks:
  alternates:
    - deployments.md
---

# Deployments

## Console and Portal APIs

Gravitee APIM Management API lets you simultaneously expose the APIM Console and Developer Portal REST APIs. This speeds up configuration for new users discovering the platform.

If the Console and Developer Portal are not intended for the same category of users, we recommend that you deploy them on separate APIM instances, where the Console API is only enabled for instances dedicated to the Console and the Developer Portal API is only enabled for instances dedicated to the Developer Portal.

In the `gravitee.yaml` file of instances dedicated to the Management Console:

* Enable the `management` parameter by setting `enabled = true`.
* Disable the `portal` parameter by setting `enabled = false`.

```yaml
http:
  api:
    management:
      enabled: true
    portal:
      enabled: false
```

In the `gravitee.yaml` file of instances dedicated to the Developer Portal:

* Enable the `management` parameter by setting `enabled = false`.
* Disable the `portal` parameter by setting `enabled = true`.

```yaml
http:
  api:
    management:
      enabled: false
    portal:
      enabled: true
```

With this configuration, the Console REST API remains publicly inaccessible even if you decide to expose your Developer Portal.

{% hint style="info" %}
For security, do not publicly expose either your Console or Developer Portal unless there is a compelling business requirement.
{% endhint %}

## Enable HTTPS

To protect against man-in-the-middle attacks, ensure that your REST APIs are only reachable over HTTPS.

Methods to configure TLS depend on installation type. To let Gravitee manage the TLS connection directly, use the following configuration for the `jetty` section of `your gravitee.yaml` file:

```yaml
jetty:
  secured: true
  ssl:
    keystore:
      type: jks # Supports jks, pkcs12
      path: <keystore_path>
      password: <keystore_secret>
```

## Logging

APIM lets you log the headers and payloads of requests at each stage of the processing flow. While logs provide valuable information, the logging process is resource-intensive.

{% hint style="warning" %}
Whenever possible, you should disable logging for APIs in a production environment. Logging impacts API performance, and storing data in the Gateway memory increases the heap pressure on the Gateway, which can lead to a Gateway crash.
{% endhint %}

To enable logging in your production environment, complete the following steps:

1. In your `gravitee.yml` file, navigate to the `reporters` section.
2. Set the `max_size` to `256KB`. The default value is `-1`, which indicates no limit.

Here is an example configuration:

```yaml
reporters:
# logging configuration
  logging:
    max_size: 256KB # max size per API log content respectively : client-request, client-response, proxy-request and proxy-response in MB (-1 means no limit)
```

{% hint style="info" %}
For hybrid Gateways connected to Gravitee Cloud, `max_size` is automatically set to 256KB.
{% endhint %}

### LogGuard

Gravitee's LogGuard feature prevents the Gateway from experiencing an out-of-memory crash due to high throughput or large payloads. Once the memory pressure of the Gateway exceeds a certain threshold, LogGuard deactivates logging.

To enable LogGuard, you must complete the following steps:

* Enable the health probes in the `health` section of your `gravitee.yaml` file. LogGuard relies on the `gc-pressure` probe.
* Enable the `memory_pressure_guard` in the `reporters` section of your `gravitee.yaml` file.

The GC pressure probe measures the percentage of CPU time used by the GC. To dynamically disable memory-consuming features, the probe output is sampled at a frequency defined by the `delay` parameter of the `health` configuration, and then compared to the pressure threshold specified by the `gcPressureThreshold` parameter.

The following example configures the GC pressure probe:

```yaml
health:
    enabled: true
    delay: 5000
    unit: MILLISECONDS
    #The thresholds to determine if a probe is healthy or not
    threshold:
      cpu: 80 # Default is 80%
      memory: 80 # Default is 80%
      gc-pressure: 15 # Default is 15%
```

If the pressure exceeds the threshold, which is set to a default value of 15%, the `LogGuardService` activates a cooldown strategy with a fixed delay of 1 minute. The `LogGuardService` is configured in the `reporters` section of the `gravitee.yaml` file.

The following example configures `reporters` to enable LogGuard:

```yaml
reporters:
# logging configuration
  logging:
    max_size: -1 # max size per API log content respectively : client-request, client-response, proxy-request and proxy-response in MB (-1 means no limit)
    excluded_response_types: video.*|audio.*|image.*|application\/octet-stream|application\/pdf # Response content types to exclude in logging (must be a regular expression)
    memory_pressure_guard:
      enabled: true
      strategy:
        type: cooldown #type of strategy (default is cooldown)
        cooldown:
          duration: 60 #duration in seconds (default is 60 seconds)
```

{% hint style="warning" %}
If LogGuard is triggered, both the request body and response body are unavailable to the UI. They are replaced with the message `BODY NOT CAPTURED`. The request body and response body are also unavailable to external monitoring systems, such as Datadog.
{% endhint %}

## Kubernetes deployments

The Gravitee Helm chart ships conservative defaults that are safe for a first install but are not sufficient for high availability on their own. Review the following settings for each component you deploy (`api`, `gateway`, `portal`, `ui`, and, if enabled, `gammaUi` and `kafkaConsole`) before going to production.

{% hint style="info" %}
`gammaUi` and `kafkaConsole` are disabled by default (`enabled: false`) and only apply if you've enabled those features.
{% endhint %}

### Minimum HA replicas

| Component | Helm value | Chart default | Recommendation |
|---|---|---|---|
| `api` (Management API) | `api.replicaCount` | `1` | `2`+ |
| `gateway` | `gateway.replicaCount` | `1` | `3`+ |
| `portal` | `portal.replicaCount` | `1` | `2`+ |
| `ui` (Console webui) | `ui.replicaCount` | `1` | `2`+ |
| `gammaUi` | `gammaUi.replicaCount` | `1` | `2`+ if enabled |
| `kafkaConsole` | `kafkaConsole.replicaCount` | `1` | `2`+ if enabled |

**Example** (`values-production.yaml`):

```yaml
api:
  replicaCount: 2

gateway:
  replicaCount: 3
```

### Pod Disruption Budgets

{% hint style="warning" %}
Every component ships with `pdb.enabled: false`. Nothing stops a node drain or cluster upgrade from evicting every replica of a component at once unless you enable this explicitly.
{% endhint %}

| Component | Helm value | Chart default | Recommendation |
|---|---|---|---|
| `api` | `api.pdb.enabled` / `minAvailable` / `maxUnavailable` | `false` / `""` / `"50%"` | Enable; set `minAvailable: 1` (or `replicas - 1`) |
| `gateway` | `gateway.pdb.*` | `false` / `""` / `"50%"` | Enable; set `minAvailable: 1` |
| `portal` | `portal.pdb.*` | `false` / `""` / `"50%"` | Enable; set `minAvailable: 1` |
| `ui` | `ui.pdb.*` | `false` / `""` / `"50%"` | Enable; set `minAvailable: 1` |
| `gammaUi` | `gammaUi.pdb.*` | `false` / `""` / `"50%"` | Enable if the component is in use |
| `kafkaConsole` | `kafkaConsole.pdb.*` | `false` / `""` / `"50%"` | Enable if the component is in use |

**Example** (`values-production.yaml`):

```yaml
api:
  pdb:
    enabled: true
    minAvailable: 1
    maxUnavailable: ""   # must clear this — Kubernetes rejects a PDB with both set

gateway:
  pdb:
    enabled: true
    minAvailable: 2      # gateway runs 3+ replicas, so keep 2 available during a drain
    maxUnavailable: ""
```

### Pod anti-affinity

{% hint style="warning" %}
No component configures anti-affinity out of the box (`deployment.affinity: {}` for all of them). Replicas can land on the same node with no anti-affinity rule in place.
{% endhint %}

| Component | Helm value | Chart default | Recommendation |
|---|---|---|---|
| `api` | `api.deployment.affinity` | `{}` (none) | Add a `podAntiAffinity` rule keyed on the `api` pod label |
| `gateway` | `gateway.deployment.affinity` | `{}` (none) | Add a `podAntiAffinity` rule keyed on the `gateway` pod label |
| `portal` | `portal.deployment.affinity` | `{}` (none) | Add a `podAntiAffinity` rule keyed on the `portal` pod label |
| `ui` | `ui.deployment.affinity` | `{}` (none) | Add a `podAntiAffinity` rule keyed on the `ui` pod label |
| `gammaUi` | `gammaUi.deployment.affinity` | `{}` (none) | Add if the component is in use |
| `kafkaConsole` | `kafkaConsole.deployment.affinity` | `{}` (none) | Add if the component is in use |

**Example** (`values-production.yaml`):

The chart injects this value as literal YAML (no templating), so reference the real pod labels directly. Each component is labeled with `app.kubernetes.io/name: apim` and `app.kubernetes.io/component: <api|gateway|portal|ui|gamma|kafkaConsole>` (note: `gammaUi`'s component label value is `gamma`, not `gammaUi`). Add `app.kubernetes.io/instance: <your-release-name>` too if more than one `apim` release runs in the same namespace.

```yaml
api:
  deployment:
    affinity:
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              topologyKey: kubernetes.io/hostname
              labelSelector:
                matchLabels:
                  app.kubernetes.io/name: apim
                  app.kubernetes.io/component: api

gateway:
  deployment:
    affinity:
      podAntiAffinity:
        preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              topologyKey: kubernetes.io/hostname
              labelSelector:
                matchLabels:
                  app.kubernetes.io/name: apim
                  app.kubernetes.io/component: gateway
```

{% hint style="info" %}
`preferredDuringSchedulingIgnoredDuringExecution` (soft anti-affinity) is used here rather than `requiredDuringSchedulingIgnoredDuringExecution` (hard). Hard anti-affinity blocks scheduling entirely if there aren't enough nodes to spread every replica, which is usually worse than accepting occasional co-location.
{% endhint %}

### Controlled HPA scaling behavior

| Component | Helm value | Chart default | Recommendation |
|---|---|---|---|
| `api` | `api.autoscaling.*` | `enabled: true`, `minReplicas: 1` / `maxReplicas: 3`, CPU `50%` / memory `80%`, `behavior` unset | Set `behavior.scaleDown.stabilizationWindowSeconds` (300-600) and a bounded `scaleUp` policy |
| `gateway` | `gateway.autoscaling.*` | Same defaults | Same tuning; the gateway is the component most exposed to traffic bursts |
| `portal` | `portal.autoscaling.*` | Same defaults | Same tuning |
| `ui` | `ui.autoscaling.*` | Same defaults | Same tuning |
| `gammaUi` | `gammaUi.autoscaling.*` | Same defaults | Same tuning, if enabled |
| `kafkaConsole` | `kafkaConsole.autoscaling.*` | Same defaults | Same tuning, if enabled |

{% hint style="info" %}
`autoscaling.enabled` defaults to `true` for every component, so a `HorizontalPodAutoscaler` is created out of the box. The chart leaves `behavior` commented out, so Kubernetes' own default scaling behavior applies (near-instant scale-up, a 300-second scale-down stabilization window) until you set it explicitly.
{% endhint %}

**Example** (`values-production.yaml`):

```yaml
api:
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 6
    targetAverageUtilization: 50
    targetMemoryAverageUtilization: 80
    behavior:
      scaleDown:
        stabilizationWindowSeconds: 300
        policies:
          - type: Pods
            value: 1
            periodSeconds: 60
      scaleUp:
        stabilizationWindowSeconds: 0
        policies:
          - type: Pods
            value: 2
            periodSeconds: 60

gateway:
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetAverageUtilization: 50
    targetMemoryAverageUtilization: 80
    behavior:
      scaleDown:
        stabilizationWindowSeconds: 600   # gateway sees bursty traffic — hold off scaling down longer
        policies:
          - type: Pods
            value: 1
            periodSeconds: 60
      scaleUp:
        stabilizationWindowSeconds: 0
        policies:
          - type: Pods
            value: 2
            periodSeconds: 60
```

{% hint style="info" %}
Scale-up is intentionally fast (`stabilizationWindowSeconds: 0`) and scale-down is intentionally slow — this asymmetry avoids dropping capacity too early during a temporary traffic dip.
{% endhint %}
