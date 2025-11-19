---
noIndex: true
---

# Cluster Configurations

In most cases, Blackbird cluster (powered by Telepresence) doesn't require any configuration within the cluster. It can be used immediately in any cluster, provided you have the necessary role-based access control (RBAC) permissions and the cluster is running Kubernetes version 1.19.0 or later. However, there are several configuration options you can use based on your use case.

Using this page, you can learn about:

* [Helm chart configurations](cluster-configurations.md#helm-chart-configurations)
* [Client configurations](cluster-configurations.md#client-configurations)
* [Traffic Manager configurations](cluster-configurations.md#traffic-manager-configurations)
* [Agent configurations](cluster-configurations.md#agent-configurations)
* [Transport Layer Security (TLS) configurations](cluster-configurations.md#transport-layer-security-tls-configurations)
* [Mutating webhook configurations](cluster-configurations.md#mutating-webhook-configurations)
* [Environment variable configurations](cluster-configurations.md#environment-variable-configurations)
* [Enabling errors when attempting to access an intercept that has expired](cluster-configurations.md#enabling-errors-when-attempting-to-access-an-intercept-that-has-expired)

## Helm chart configurations

Some cluster specific configuration can be provided when installing or upgrading the Blackbird cluster installation using Helm. Once installed, the Blackbird client will configure itself from values that it receives when connecting to the Traffic Manager.

For a full list of configuration settings, see the Helm chart [README](https://artifacthub.io/packages/helm/datawire/telepresence).

### Values

To add configuration, create a YAML file with the configuration values, and then use it executing `blackbird cluster helm install [--upgrade] --values <values yaml>`.

## Client configurations

You can use the Traffic Manager to automatically push configurations to all connecting clients.

## Traffic Manager configurations

The `trafficManager` structure of the Helm chart configures the behavior of the Telepresence Traffic Manager.

### Service mesh

The `trafficManager.serviceMesh` structure is used to configure Blackbird integrations with service meshes. You should configure this if your cluster is running a compatible service mesh, as it's often needed to be able to intercept all workloads. Currently only `istio` is supported. Valid values include:

| Value  | Resulting action                                                                                 |
| ------ | ------------------------------------------------------------------------------------------------ |
| `type` | The type of service mesh that's used by your cluster. Supports `none` (the default) and `istio`. |

For more information, see [service-mesh-configurations.md](service-mesh-configurations.md "mention").

## Agent configurations

The `agent` structure of the Helm chart configures the behavior of the Blackbird agents.

### Application protocol selection

The `agent.appProtocolStrategy` is useful when using personal intercepts, and it controls how Blackbird selects the application protocol to use when intercepting a service that has no `service.ports.appProtocol` declared. The port's `appProtocol` is always trusted if it is present. Valid values include:

| Value        | Resulting action                                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `http2Probe` | The Blackbird Traffic Agent will probe the intercepted container to check whether it supports http2. This is the default. |
| `portName`   | Blackbird will make an educated guess about the protocol based on the name of the service port                            |
| `http`       | Blackbird will use http.                                                                                                  |
| `http2`      | Blackbird will use http2.                                                                                                 |

When `portName` is used, Blackbird will determine the protocol by the name of the port: `<protocol>[-suffix]`. The following protocols are recognized:

| Protocol | Meaning                               |
| -------- | ------------------------------------- |
| `http`   | Plaintext HTTP/1.1 traffic            |
| `http2`  | Plaintext HTTP/2 traffic              |
| `https`  | TLS Encrypted HTTP (1.1 or 2) traffic |
| `grpc`   | Same as http2                         |

> **Note:** The application protocol strategy can also be configured on a workstation.

### Envoy configuration

The `agent.envoy` structure contains three values:

| Setting      | Meaning                                                   |
| ------------ | --------------------------------------------------------- |
| `logLevel`   | Log level used by the Envoy proxy. Defaults to "warning". |
| `serverPort` | Port used by the Envoy server. Default 18000.             |
| `adminPort`  | Port used for Envoy administration. Default 19000.        |

### Image configuration

The `agent.image` structure contains the following values:

| Setting    | Meaning                                                                     |
| ---------- | --------------------------------------------------------------------------- |
| `registry` | Registry used when downloading the image. Defaults to "docker.io/datawire". |
| `name`     | The name of the image.                                                      |
| `tag`      | The tag of the image.                                                       |

### Log level

The `agent.LogLevel` controls the log level of the Traffic Manager.

### Resources

`agent.resources` and `agent.initResources` will be used as the `resources` element when injecting Traffic Agents and init containers.

## Transport Layer Security (TLS) configurations

In this example, other applications in the cluster expect to speak TLS to your intercepted application (perhaps you're using a service-mesh that does mTLS). To use `--mechanism=http`, or any features that imply `--mechanism=http`, you need to tell Blackbird about the TLS certificates in use.

You can tell Blackbird about the certificates in use by adjusting your workload's Pod template to set a couple of annotations on the intercepted Pods:

```diff
 spec:
   template:
     metadata:
       labels:
         service: your-service
+      annotations:
+        "telepresence.getambassador.io/inject-terminating-tls-secret": "your-terminating-secret"  # optional
+        "telepresence.getambassador.io/inject-originating-tls-secret": "your-originating-secret"  # optional
```

* The `getambassador.io/inject-terminating-tls-secret` annotation (optional) names the Kubernetes Secret that contains the TLS server certificate to use for decrypting and responding to incoming requests. When Blackbird modifies the service and workload port definitions to point at the Blackbird Agent sidecar's port instead of your application's actual port, the sidecar will use this certificate to terminate TLS.
* The `getambassador.io/inject-originating-tls-secret` annotation (optional) names the Kubernetes Secret that contains the TLS client certificate to use for communicating with your application. You must set this if your application expects incoming requests to speak TLS. For example, your code expects to handle mTLS itself instead of letting a service mesh sidecar handle mTLS for it, or the port definition that Blackbird modified pointed at the service mesh sidecar instead of your application. If you do set this, you should to set it to the same client certificate Secret that you configure Ambassador Edge Stack to use for mTLS. You can only refer to a Secret that's in the same namespace as the Pod. The Secret will be mounted into the Traffic Agent's container.

Blackbird understands `type: kubernetes.io/tls` Secrets and `type: istio.io/key-and-cert` Secrets; as well as `type: Opaque` Secrets that it detects to be formatted as one of those types.

#### Helm chart manages the secret

1. Obtain a JSON web token (JWT) from the downloaded license file.

```
$ cat ~/Downloads/ambassador.License_for_yourcluster
eyJhbGnotarealtoken.butanexample
```

2. Create the following values file, substituting your real JWT for the one used in the example below. For this example, the following is placed in a file called license-values.yaml.

```
licenseKey:
  # This mounts the secret into the Traffic Manager.
  create: true
  # This is the value from the license file you download. The value is an example and won't work.
  value: eyJhbGnotarealtoken.butanexample
  secret:
    # This tells the Helm chart to create the secret.
    create: true
```

3. Install the Helm chart into the cluster.

```
blackbird cluster helm install -f license-values.yaml
```

If you're using Helm to install the server-side components, see the chart's README to learn how to configure the image registry and license secret.

## Mutating webhook configurations

Blackbird uses a mutating webhook to inject the Traffic Agent sidecar container and update the port definitions. This means that an intercepted workload (Deployment, StatefulSet, ReplicaSet, or Argo Rollout) will remain untouched and in sync as far as GitOps workflows, such as ArgoCD, are concerned. The injection will happen on demand the first time an attempt is made to intercept the workload. If you want to prevent the injection from happening, add the `telepresence.getambassador.io/inject-traffic-agent: disabled` annotation to your workload template's annotations:

```diff
 spec:
   template:
     metadata:
       labels:
         service: your-service
+      annotations:
+        telepresence.getambassador.io/inject-traffic-agent: disabled
     spec:
       containers:
```

### Service name and port annotations

Blackbird will automatically find all services and ports that will connect to a workload and make them available for an intercept, but you can explicitly define that only one service and/or port can be intercepted.

```diff
 spec:
   template:
     metadata:
       labels:
         service: your-service
       annotations:
+        telepresence.getambassador.io/inject-service-name: my-service
+        telepresence.getambassador.io/inject-service-port: https
     spec:
       containers:
```

### Ignore certain volume mounts

An annotation `telepresence.getambassador.io/inject-ignore-volume-mounts` can be used to make the injector ignore certain volume mounts.

### Numeric ports

If the `targetPort` of your intercepted service is pointing at a port number, in addition to injecting the Traffic Agent sidecar, Blackbird will also inject an `initContainer` that will reconfigure the Pod's firewall rules to redirect traffic to the Traffic Agent.

> **Note:** This `initContainer` requires `NET_ADMIN` capabilities. If your cluster administrator has disabled them, you will be unable to use numeric ports with the agent injector.

If you need to use numeric ports without these capabilities, you can manually install the agent. For example, the following service is using a numeric port, so Blackbird will inject an initContainer into it:

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
      annotations:
        telepresence.getambassador.io/inject-traffic-agent: enabled
      labels:
        service: your-service
    spec:
      containers:
        - name: your-container
          image: jmalloc/echo-server
          ports:
            - containerPort: 8080
```

## Environment variable configurations

If your Pod contains sensitive variables, such as a database password or third-party API Key, you can exclude them from being propagated through an intercept. Blackbird allows you to configure this through a ConfigMap that removes the sensitive variables. You can use one of the following approaches.

When installing your Traffic Manager through Helm, you can use the `--set` flag and pass a comma-separated list of variables:

`blackbird cluster helm install --set intercept.environment.excluded="{DATABASE_PASSWORD,API_KEY}"`

This also applies when upgrading:

`clackbird cluster helm upgrade --set intercept.environment.excluded="{DATABASE_PASSWORD,API_KEY}"`

Once this is completed, the environment variables will no longer be in the environment file created by an intercept.

The other way to complete this is in your custom `values.yaml` file.

```yaml
intercept:
  environment:
    excluded: ['DATABASE_PASSWORD', 'API_KEY']
```

You can exclude any number of variables. They just need to match the `key` of the variable within a Pod.

## Enabling errors when attempting to access an intercept that has expired

Blackbird supports personal intercepts. When this option is enabled:

* You can define a specific HTTP header. Any request matching it will be redirected to your machine.
* If the intercept isn't active, the requests will be redirected to the real application.
* If your intercept stops or expires, but you keep providing the HTTP header, the requests will result in errors for a certain amount of time.

With the last option, you can enable or adjust errors using the following configuration in your Helm chart values:

```yaml
intercept:
  expiredNotifications:
    enabled: true
    deadline: 24h # Amount of time before it stops returning an error after intercept removal / expiration.
```
