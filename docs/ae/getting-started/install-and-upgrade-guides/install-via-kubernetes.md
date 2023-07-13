---
description: This article walks through how to install Gravitee Alert Engine via Kubernetes
---

# Install via Kubernetes

## Introduction

This section explains how to deploy Alert Engine (AE) in Kubernetes. These procedures are intended for users who are already familiar with Kubernetes.

## Gravitee Alert Engine Helm Chart

### **Chart supported versions: 1.0.x and higher**

#### Components

This chart will deploy the following:

* Gravitee Alert Engine

## Kubernetes and Hazelcast

AE embeds Hazelcast to propagate and process events between each node. In order to make Hazelcast work best when embedded and deployed under a Kubernetes cluster, we pre-configured the auto-discovery to work with the Kubernetes API.

> Kubernetes API mode means that each node makes a REST call to Kubernetes Master in order to discover IPs of PODs (with Hazelcast members).]

In order to make it work, you need to grant access to the Kubernetes API:

{% code overflow="wrap" %}
```
$ kubectl apply -f https://gh.gravitee.io/gravitee-io/helm-charts/master/ae/rbac.yml
```
{% endcode %}

If you want to let Helm to create the Service Account with required cluster role while installing the Chart, use `--set engine.managedServiceAccount=true`

Please note that `managedServiceAccount` is enabled by default and so, you’ll have to switch it off if you want to manage the Service Account by yourself.

{% hint style="info" %}
**Use the correct namespace**

rbac.yml comes with default graviteeio namespace. Make sure to use the right namespace if you have overridden it.
{% endhint %}

### Installation

Follow these steps to install:

*   Add the Gravitee helm charts repo

    ```
    $ helm repo add graviteeio https://helm.gravitee.io
    ```
*   Install it

    ```
    $ helm install --name graviteeio-ae graviteeio/ae
    ```

### Create a chart archive

To package this chart directory into a chart archive, run:

```
$ helm package .
```

### Installing the Chart

To install the chart from the Helm repository with the release name `graviteeio-ae`:

```
$ helm install --name graviteeio-ae graviteeio/ae
```

To install the chart using the chart archive, run:

```
$ helm install ae-1.0.0.tgz
```

### License

Alert Engine need an enterprise license to work. You can define it by:

* fill the `license.key` field in the `values.yml` file.
* add helm arg: `--set license.key=<license.key in base64>`

To get the license.key value, encode your file `license.key` in `base64`:

* linux: `base64 -w 0 license.key`
* macOS: `base64 license.key`

Example:

```
export GRAVITEESOURCE_LICENSE_B64="$(base64 -w 0 license.key)"

helm install \
  --set license.key=${GRAVITEESOURCE_LICENSE_B64} \
  graviteeio-ae \
  graviteeio/ae
```

## Configuration

The following tables list the configurable parameters of the Gravitee Alert Engine chart and their default values.

### **Shared configuration**

To configure common features such as:

* chaos testing (see [chaoskube](https://github.com/kubernetes/charts/tree/master/stable/chaoskube) chart)

| Parameter       | Description       | Default |
| --------------- | ----------------- | ------- |
| `chaos.enabled` | Enable Chaos test | false   |

### **Gravitee Alert Engine**

| Key                                                                         | Type   | Default                                                                                                                                                                                                                                                                                                                                                                       | Description |
| --------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| engine.authentication.adminPassword                                         | string | `"adminadmin"`                                                                                                                                                                                                                                                                                                                                                                |             |
| engine.authentication.enabled                                               | bool   | `true`                                                                                                                                                                                                                                                                                                                                                                        |             |
| engine.autoscaling.enabled                                                  | bool   | `true`                                                                                                                                                                                                                                                                                                                                                                        |             |
| engine.autoscaling.maxReplicas                                              | int    | `3`                                                                                                                                                                                                                                                                                                                                                                           |             |
| engine.autoscaling.minReplicas                                              | int    | `1`                                                                                                                                                                                                                                                                                                                                                                           |             |
| engine.autoscaling.targetAverageUtilization                                 | int    | `50`                                                                                                                                                                                                                                                                                                                                                                          |             |
| engine.autoscaling.targetMemoryAverageUtilization                           | int    | `80`                                                                                                                                                                                                                                                                                                                                                                          |             |
| engine.enabled                                                              | bool   | `true`                                                                                                                                                                                                                                                                                                                                                                        |             |
| engine.image.pullPolicy                                                     | string | `"Always"`                                                                                                                                                                                                                                                                                                                                                                    |             |
| engine.image.repository                                                     | string | `"graviteeio/ae-engine"`                                                                                                                                                                                                                                                                                                                                                      |             |
| engine.ingress.annotations."kubernetes.io/app-root"                         | string | `"/"`                                                                                                                                                                                                                                                                                                                                                                         |             |
| engine.ingress.annotations."kubernetes.io/ingress.class"                    | string | `"nginx"`                                                                                                                                                                                                                                                                                                                                                                     |             |
| engine.ingress.annotations."kubernetes.io/rewrite-target"                   | string | `"/"`                                                                                                                                                                                                                                                                                                                                                                         |             |
| engine.ingress.annotations."nginx.ingress.kubernetes.io/enable-rewrite-log" | string | `"true"`                                                                                                                                                                                                                                                                                                                                                                      |             |
| engine.ingress.annotations."nginx.ingress.kubernetes.io/ssl-redirect"       | string | `"false"`                                                                                                                                                                                                                                                                                                                                                                     |             |
| engine.ingress.enabled                                                      | bool   | `true`                                                                                                                                                                                                                                                                                                                                                                        |             |
| engine.ingress.hosts\[0]                                                    | string | `"ae.example.com"`                                                                                                                                                                                                                                                                                                                                                            |             |
| engine.ingress.path                                                         | string | `"/"`                                                                                                                                                                                                                                                                                                                                                                         |             |
| engine.ingress.tls\[0].hosts\[0]                                            | string | `"ae.example.com"`                                                                                                                                                                                                                                                                                                                                                            |             |
| engine.ingress.tls\[0].secretName                                           | string | `"api-custom-cert"`                                                                                                                                                                                                                                                                                                                                                           |             |
| engine.logging.debug                                                        | bool   | `false`                                                                                                                                                                                                                                                                                                                                                                       |             |
| engine.logging.file.enabled                                                 | bool   | `true`                                                                                                                                                                                                                                                                                                                                                                        |             |
| engine.logging.file.encoderPattern                                          | string | `"%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n"`                                                                                                                                                                                                                                                                                                        |             |
| engine.logging.file.rollingPolicy                                           | string | `"\u003crollingPolicy class=\"ch.qos.logback.core.rolling.TimeBasedRollingPolicy\"\u003e\n \u003c!-- daily rollover --\u003e\n \u003cfileNamePattern\u003e${gravitee.home}/logs/gravitee_%d{yyyy-MM-dd}.log\u003c/fileNamePattern\u003e\n \u003c!-- keep 30 days' worth of history --\u003e\n \u003cmaxHistory\u003e30\u003c/maxHistory\u003e\n\u003c/rollingPolicy\u003e\n"` |             |
| engine.logging.graviteeLevel                                                | string | `"DEBUG"`                                                                                                                                                                                                                                                                                                                                                                     |             |
| engine.logging.stdout.encoderPattern                                        | string | `"%d{HH:mm:ss.SSS} [%thread] [%X{api}] %-5level %logger{36} - %msg%n"`                                                                                                                                                                                                                                                                                                        |             |
| engine.name                                                                 | string | `"engine"`                                                                                                                                                                                                                                                                                                                                                                    |             |
| engine.reloadOnConfigChange                                                 | bool   | `true`                                                                                                                                                                                                                                                                                                                                                                        |             |
| engine.replicaCount                                                         | int    | `1`                                                                                                                                                                                                                                                                                                                                                                           |             |
| engine.resources.limits.cpu                                                 | string | `"500m"`                                                                                                                                                                                                                                                                                                                                                                      |             |
| engine.resources.limits.memory                                              | string | `"512Mi"`                                                                                                                                                                                                                                                                                                                                                                     |             |
| engine.resources.requests.cpu                                               | string | `"200m"`                                                                                                                                                                                                                                                                                                                                                                      |             |
| engine.resources.requests.memory                                            | string | `"256Mi"`                                                                                                                                                                                                                                                                                                                                                                     |             |
| engine.service.externalPort                                                 | int    | `82`                                                                                                                                                                                                                                                                                                                                                                          |             |
| engine.service.internalPort                                                 | int    | `8072`                                                                                                                                                                                                                                                                                                                                                                        |             |
| engine.service.internalPortName                                             | string | `"http"`                                                                                                                                                                                                                                                                                                                                                                      |             |
| engine.service.type                                                         | string | `"ClusterIP"`                                                                                                                                                                                                                                                                                                                                                                 |             |
| engine.ssl.clientAuth                                                       | bool   | `false`                                                                                                                                                                                                                                                                                                                                                                       |             |
| engine.ssl.enabled                                                          | bool   | `false`                                                                                                                                                                                                                                                                                                                                                                       |             |
| engine.type                                                                 | string | `"Deployment"`                                                                                                                                                                                                                                                                                                                                                                |             |
| license.key                                                                 | string | license.key file encoded in base64                                                                                                                                                                                                                                                                                                                                            |             |

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```
$ helm install --name my-release -f values.yaml gravitee
```

> **Tip**: You can use the default values.yaml

## **Recommendations for a production environment**

For a production ready environment, we recommend to apply the following settings.

### **Memory**

For large environments handling a lot of events, we recommend specifying enough memory available for the JVM to be able to process all events in real time.

```
engine:
  env:
     - name: GIO_MIN_MEM
       value: 1024m
     - name: GIO_MAX_MEM
       value: 1024m
     - name: gravitee_ingesters_ws_compressionSupported
       value: "true"
```

You must also adapt the memory request and limit at the pod level. When using 1Go at the JVM level, we recommend to set 1.5Go at pod level to make sure the pod will not run out of memory and get killed.

```
  resources:
    limits:
      memory: 1.5Gi
    requests:
      memory: 1.5Gi
```

### **CPU**

The following default values should be enough in most cases and should allow handling approximately 2000 events per seconds with only 2 pods (see autoscaling section to specify min and max pods).

```
  resources:
    limits:
      cpu: 1000m
    requests:
      cpu: 500m
```

### **Autoscaling**

By default, there is only 1 AE pod started (up to 3 pods). To make the system error proof and able to handle more events at high throughput, you may configure the autoscaler with a minimum of 2 pods and increase the number of maximum pods.

```
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 5
    targetAverageUtilization: 50
    targetMemoryAverageUtilization: null
```

You may also disable the autoscaling based on memory average utilization except if you have a specific metrics server able to calculate the memory used by a JVM running in a container.

### **Readiness and liveness probes**

Depending on your usage of AE, you can also fine tune the different probes used by the cluster to determine the current status of each AE pod.

The default values are optimized for a healthy ratio between speed and reliability.

```
# This probe is use only during startup phase
startupProbe:
  tcpSocket:
    port: http # Same as engine.service.internalPortName
  initialDelaySeconds: 30
  periodSeconds: 5
  failureThreshold: 20

# This probe is used to determine if the pod is still alive.
livenessProbe:
  tcpSocket:
    port: http # Same as engine.service.internalPortName
  periodSeconds: 10
  failureThreshold: 5

# This probe is used to determine if the pod can still handle traffic. If not, it will be removed from the service and not reachable until it is ready again.
readinessProbe:
  tcpSocket:
    port: http # Same as engine.service.internalPortName
  periodSeconds: 5
  failureThreshold: 3
```

Depending on the amount of cpu you give to each pod you should be able to change the different settings of the startupProbe such as `initialDelaySeconds`.

The more processors you have, the faster the server will start, the lower you can set the `initialDelaySeconds` value.

### **Enable compression**

To optimize network transfer between Gravitee API Management or Access Management and Alert Engine, it could be useful to enable compression.

{% hint style="info" %}
**Be aware of cpu costs**

Compression comes with cpu costs (on both client and server sides). You may balance the choice analyzing cpu cost versus network and response time improvements.
{% endhint %}

```
engine:
  env:
     - name: gravitee_ingesters_ws_compressionSupported
       value: "true"
```

Make sure `alerts.alert-engine.ws.tryCompression` is set to true on the APIM / AM side.\
