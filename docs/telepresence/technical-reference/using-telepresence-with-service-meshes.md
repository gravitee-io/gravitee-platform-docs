---
noIndex: true
---

# Using Telepresence with Service Meshes

Service meshes take over and operate on all networking functions in your cluster. They route traffic, add DNS entries, and set up firewall rules. Because of this, it can be tricky to get Telepresence's own connectivity and intercepting functionality to work with a service mesh.

This page has two sections. The [Integrations](using-telepresence-with-service-meshes.md#integrations) section discusses the native Telepresence integration with the Istio service mesh. This service mesh should be easy to configure and should work out of the box for most use cases. The [Workarounds](using-telepresence-with-service-meshes.md#workarounds) section discusses how Telepresence can sometimes operate in a service mesh such as Linkerd with certain workarounds. In these cases, some functionality may be limited.

## Integrations

### Istio

To get started with Telepresence on Istio, all you have to do is [configure your Helm values](cluster-side-configuration.md#service-mesh) on installing so that istio is enabled:

```console
$ telepresence helm install --set trafficManager.serviceMesh.type=istio
```

This will enable the Istio integration, allowing for some native Istio features to be used by Telepresence.

#### Intercepting services with numeric ports

When intercepting a service that uses a numeric port instead of a symbolic port, Telepresence's [init container](cluster-side-configuration.md#note-on-numeric-ports) will conflict with Istio's own init container. Instead of injecting an init container, when running in Istio, Telepresence will create a `networking.istio.io/v1alpha3` `Sidecar` resource to configure Istio's own sidecar to direct traffic to the Telepresence agent.

For example, if you have a service that looks like:

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

And you intercept it:

```console
$ telepresence intercept your-service --port 8080
```

Then Telepresence will create a sidecar to direct traffic to the agent port:

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

**Sidecar conflicts**

If you already have `Sidecars` that are selecting your service, then this may cause conflicts which Telepresence will error on.

Take the example workload from the previous section, but let's say you hadn't run `telepresence intercept` and had instead created a sidecar that selects your workload:

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

When you go intercept now, Telepresence will give you an error:

```console
$ telepresence intercept your-service --port 8080
telepresence intercept: error: Error creating: admission webhook "agent-injector-ambassador.getambassador.io" denied the request: existing sidecar egress-config conflicts with new sidecar for workload your-service
```

At this point, your best bet is to add a name to your port; that will prevent any conflicts with existing sidecar configs:

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

## Workarounds

### Linkerd

Getting started with Telepresence on Linkerd services is as simple as adding an annotation to your Deployment:

```yaml
spec:
  template:
    metadata:
      annotations:
        config.linkerd.io/skip-outbound-ports: "8081"
```

The local system and the Traffic Agent connect to the Traffic Manager using its gRPC API on port 8081. Telling Linkerd to skip that port allows the Traffic Agent sidecar to fully communicate with the Traffic Manager, and therefore the rest of the Telepresence system.

#### Deploy

Save and deploy the following YAML. Note the `config.linkerd.io/skip-outbound-ports` annotation in the metadata of the pod template.

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

#### Connect to Telepresence

Run `telepresence connect` to connect to the cluster. Then `telepresence list` should show the `quote` deployment as `ready to intercept`:

```
$ telepresence list

  quote: ready to intercept (traffic-agent not yet installed)
```

#### Run the intercept

Run `telepresence intercept quote --port 8080:80` to direct traffic from the `quote` deployment to port 8080 on your local system. Assuming you have something listening on 8080, you should now be able to see your local service whenever attempting to access the `quote` service.
