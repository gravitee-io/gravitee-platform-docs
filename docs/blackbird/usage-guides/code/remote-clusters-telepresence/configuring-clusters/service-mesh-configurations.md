---
description: Overview of Service Mesh Configurations.
noIndex: true
---

# Service Mesh Configurations

Service meshes manage and control all networking functions within a cluster, including traffic routing, DNS resolution, and firewall rule configuration. Because of this, integrating the connectivity and interception capabilities of Blackbird cluster (powered by Telepresence) with a service mesh can be challenging. It's essential to properly configure your system to ensure compatibility and prevent conflicts.

Using this page, you can learn about:

* [Istio service mesh configurations](service-mesh-configurations.md#istio-service-mesh-configurations)
* [Linkerd service mesh configurations](service-mesh-configurations.md#linkerd-service-mesh-configurations)

## Istio service mesh configurations

An Istio service mesh is an open-source service mesh that provides traffic management, security, and observability without requiring changes to application code. For most use cases, you can use it out of the box.

To get started, configure your Helm values so Istio is enabled.

```console
$ blackbird cluster helm install --set trafficManager.serviceMesh.type=istio
```

### Intercepting services with numeric ports

When intercepting a service that uses a numeric port instead of a symbolic port, Blackbird's `initContainer` will conflict with Istio's init container. Instead of injecting an init container when running in Istio, Blackbird creates a `networking.istio.io/v1alpha3` sidecar resource to configure Istio's own sidecar to direct traffic to the Blackbird agent.

For example, if you have a service similar to the following:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: your-service
spec:
  type: ClusterIP
  selector:
    service: your-service
  ports:
    - port: 80
      targetPort: 8080
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-service
  labels:
    service: your-service
spec:
  replicas: 1
  selector:
    matchLabels:
      service: your-service
  template:
    metadata:
      labels:
        service: your-service
    spec:
      containers:
        - name: your-container
          image: jmalloc/echo-server
          ports:
            - containerPort: 8080
```

And you intercept the service:

```console
$ blackbird cluster intercept your-service --port 8080
```

Blackbird creates a sidecar to direct traffic to the agent port:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  labels:
    app.kubernetes.io/created-by: traffic-manager
    app.kubernetes.io/name: telepresence-your-service
    telepresence.io/workloadName: your-service
  name: telepresence-your-service
spec:
  ingress:
  - defaultEndpoint: 127.0.0.1:9900
    port:
      number: 8080
      protocol: TCP
  workloadSelector:
    labels:
      telepresence.io/workloadEnabled: "true"
      telepresence.io/workloadName: your-service
```

#### Sidecar conflicts

If you have sidecar configurations that are selecting your service, they can cause conflicts that produce errors in Blackbird.

Using the example in the previous section, if you created a sidecar that selects your workload instead of running `blackbird cluster intercept`:

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Sidecar
metadata:
  name: egress-config
spec:
  workloadSelector:
    labels:
      service: your-service
  egress:
  - port:
      number: 9080
      protocol: HTTP
      name: egresshttp
    hosts:
    - "prod-us1/*"
  - hosts:
    - "istio-system/*"
```

When you attempt to intercept, Blackbird will produce an error.

```console
$ blackbird cluster intercept your-service --port 8080
blackbird cluster intercept: error: Error creating: admission webhook "agent-injector-ambassador.getambassador.io" denied the request: existing sidecar egress-config conflicts with new sidecar for workload your-service
```

To resolve this, you can add a name to your port to prevent any conflicts with existing sidecar configs:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: your-service
spec:
  type: ClusterIP
  selector:
    service: your-service
  ports:
    - port: 80
      targetPort: http
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-service
  labels:
    service: your-service
spec:
  replicas: 1
  selector:
    matchLabels:
      service: your-service
  template:
    metadata:
      labels:
        service: your-service
    spec:
      containers:
        - name: your-container
          image: jmalloc/echo-server
          ports:
            - containerPort: 8080
              name: http
```

## Linkerd service mesh configurations

A Linkerd service mesh is an open-source service mesh designed to manage, secure, and observe communication between microservices.

To get started with Linkerd, you can add an annotation to your deployment:

```yaml
spec:
  template:
    metadata:
      annotations:
        config.linkerd.io/skip-outbound-ports: "8081"
```

The local system and the Traffic Agent connect to the Traffic Manager using its gRPC API on port `8081`. Configuring Linkerd to exclude that port allows the Traffic Agent sidecar to establish full communication with the Traffic Manager, enabling a seamless integration with the rest of Blackbird.

### Deploy

Save and deploy the following YAML.

Note the `config.linkerd.io/skip-outbound-ports` annotation in the metadata of the Pod template:

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quote
spec:
  replicas: 1
  selector:
    matchLabels:
      app: quote
  strategy:
    type: RollingUpdate
  template:
    metadata:
      annotations:
        linkerd.io/inject: "enabled"
        config.linkerd.io/skip-outbound-ports: "8081,8022,6001"
      labels:
        app: quote
    spec:
      containers:
      - name: backend
        image: docker.io/datawire/quote:0.4.1
        ports:
        - name: http
          containerPort: 8000
        env:
        - name: PORT
          value: "8000"
        resources:
          limits:
            cpu: "0.1"
            memory: 100Mi
```

### Connect to the cluster

Run `blackbird cluster connect` to connect to the cluster. Then, run `blackbird cluster list` to show the `quote` deployment as `ready to intercept`:

```
$ blackbird cluster list

  quote: ready to intercept (traffic-agent not yet installed)
```

### Run the intercept

Run `blackbird cluster intercept quote --port 8080:80` to direct traffic from the `quote` deployment to port `8080` on your local system. If a service is listening on port `8080`, accessing the quote service should display your local service.
