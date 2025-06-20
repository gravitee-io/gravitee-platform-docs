# Gateway API - KafkaRoute (Experimental)

⚠️ Disclaimer

KafkaRoute and ACLFilter support is experimental and subject to change in future releases as our implementation of the Gateway API evolves.

The Gateway API controller is disabled by default in the Kubernetes Operator. To enable it, set the Helm value `gatewayAPI.controller.enabled` to true when installing or upgrading with Helm.

## Overview

The KafkaRoute custom resource is designed to let you declaratively define how Kafka traffic is routed through your Kubernetes cluster by leveraging the [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/).

This allows you to deploy gateways and manage traffic through them using a unified, well-defined API, just as the Gateway API already does with HTTPRoute resources.

> The KafkaRoute resource depends on licensed runtime features. To enable this functionality, please visit our [website](https://www.gravitee.io/try-gravitee) to request a valid license.

## Example

This example demonstrates the minimal set of resources required to expose and route both Kafka and HTTP traffic using Gravitee's Kubernetes-native Gateway. The Kafka cluster is assumed to be accessible via a Kubernetes Service named `my-cluster-kafka-bootstrap` in the default namespace.

The Gateway resource includes the necessary annotations for [cert-manager](https://cert-manager.io/docs/usage/gateway/) to automatically create and manage TLS certificates.

{% code lineNumbers="true" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: GatewayClassParameters
metadata:
  name: gravitee-gateway
spec:
  gravitee:
    licenseRef:
      name: gravitee-license
    kafka:
      enabled: true
---
kind: GatewayClass
apiVersion: gateway.networking.k8s.io/v1
metadata:
  name: gravitee-gateway
spec:
  controllerName: apim.gravitee.io/gateway
  parametersRef:
    kind: GatewayClassParameters
    group: gravitee.io
    name: gravitee-gateway
    namespace: default
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gravitee-gateway
  annotations:
    cert-manager.io/cluster-issuer: self-signed
    cert-manager.io/usages: "server auth"
    cert-manager.io/subject-organizations: gravitee
    cert-manager.io/common-name: "*.kafka.example.dev"
spec:
  gatewayClassName: gravitee-gateway
  listeners:
    - name: http
      port: 80
      protocol: HTTP
    - name: https
      port: 443
      protocol: HTTPS
      hostname: '*.apis.example.dev'
      tls:
        certificateRefs:
          - group: ""
            kind: Secret
            name: "https-server"
    - name: kafka
      port: 9092
      protocol: TLS
      hostname: '*.kafka.example.dev'
      tls:
        certificateRefs:
          - group: ""
            kind: Secret
            name: "kafka-server"
      allowedRoutes:
        kinds:
        - group: gravitee.io
          kind: KafkaRoute
---
apiVersion: gravitee.io/v1alpha1
kind: KafkaRoute
metadata:
  name: kafka-route-demo
spec:
  parentRefs:
    - name: gravitee-gateway
      kind: Gateway
      group: gateway.networking.k8s.io
      namespace: default
  hostname: demo.kafka.example.dev
  backendRefs:
    - group: ""
      kind: Service
      name: my-cluster-kafka-bootstrap
      namespace: default
      port: 9092
```

Before deploying this configuration, you must create a Kubernetes Secret containing your Gravitee license file. This license is required to enable Kafka protocol support within the Gravitee Gateway. The license **must** be accessible through a secret data key named `license.key`.

```sh
kubectl create secret generic gravitee-license \
  --from-file=license.key \
  -n default
```

> This command creates a secret named `gravitee-license` in the default namespace, containing the license.key file content. Ensure the namespace matches the one referenced in your `GatewayClassParameters`.

Additionally, to enable Kafka traffic, Kafka support **must** be explicitly enabled in the `GatewayClassParameters` resource by setting the `gravitee.kafka.enabled` property to true.

### The Gateway resource

To be able to route Kafka trafic your gateway resource **must** define a TLS listener that declares the gravitee.io KafkaRoute as a supported kind.

```yaml
name: kafka
port: 9092
protocol: TLS
hostname: '*.kafka.example.dev'
tls:
certificateRefs:
    - group: ""
    kind: Secret
    name: "kafka-server"
allowedRoutes:
kinds:
- group: gravitee.io
    kind: KafkaRoute
```

Here, the listener is set to accept traffic on any subdomain of kafka.example.dev using a wildcard. If you use cert-manager to create certificates, the `cert-manager.io/common-name` annotation on your Gateway **must** also be set to `*.kafka.example.dev`. This tells cert-manager to create a certificate matching that domain, stored in the `kafka-server` secret referenced in the listener’s TLS configuration.

Applying these resources will create all the components needed for the gateway to accept Kafka traffic on port 9092 (routing connections to `demo.kafka.example.dev` through the KafkaRoute to the `my-cluster-kafka-bootstrap` service), as well as HTTP traffic on ports 80 and 443.

### Adding access controls to the Kafka Route through the ACL Filter

The KafkaRoute resource includes an ACL Filter that lets you define fine-grained ACLs (Access Control Lists) on Kafka cluster resources proxied by the Gateway. You can specify permissions for topics, clusters, consumer groups, and transactional IDs.

{% code lineNumbers="true" %}
```yaml
apiVersion: gravitee.io/v1alpha1
kind: KafkaRoute
metadata:
  name: kafka-route-demo
spec:
  parentRefs:
    - name: gravitee-gateway
      kind: Gateway
      group: gateway.networking.k8s.io
      namespace: default
  hostname: demo.kafka.example.dev
  filters:
  - type: ACL
    acl:
      rules:
        - resources:
          - type: Topic
            match:
              type: Exact
              value: demo
            operations:
              - Read
              - Write
              - Create
          - type: Group
            match:
              type: Exact
              value: demo-consumer-group
            operations:
              - Read
  backendRefs:
    - group: ""
      kind: Service
      name: my-cluster-kafka-bootstrap
      namespace: default
      port: 9092
```

In this example, the AccessControl filter grants `read`, `write`, and `create` permissions on the `demo` topic, and `read` permission on the `demo-consumer-group` consumer group. Any attempt to access other topics or groups not listed in the ACL will be denied.

{% hint style="info" %}
**For more information**

* The `KafkaRoute` CRD API reference is documented [here](../../reference/api-reference.md).
{% endhint %}
