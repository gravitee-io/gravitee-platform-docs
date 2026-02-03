# GatewayClassParameters

## Overview

The GatewayClassParameters custom resource is the Gravitee.io extension point that allows you to configure our implementation of the [Kubernetes Gateway API](https://gateway-api.sigs.k8s.io/). It defines a set of configuration options to control how Gravitee Gateways are deployed and behave when managed via the Gateway API, including licensing, Kafka support, and Kubernetes-specific deployment settings.

### Prerequisites&#x20;

The Gateway API controller requires cluster-scoped installation because the GatewayClass resource is cluster-scoped.&#x20;

Before using `GatewayClassParameters` and the Gateway API controller, ensure you configure it with the following:

```yaml
gatewayAPI:
  controller:
    enabled: true
manager:
  scope:
    cluster: true
    namespaces: []
```

{% hint style="warning" %}
You cannot define specific namespaces (`manager.scope.namespaces`) when the Gateway API controller is enabled.
{% endhint %}

## Example

This configuration enables Kafka support in the Gravitee Gateway by setting the Kafka feature to enabled and referencing a Kubernetes Secret that contains a valid license through the licenseRef field.

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
  kubernetes:
    deployment:
      template:
        spec:
          containers:
          - name: gateway
            image: graviteeio/apim-gateway:4.8.0
```
{% endcode %}

### Gravitee Configuration

The `gravitee` section controls Gravitee specific features and allows you to configure and customize our implementation of the Kubernetes Gateway API.

#### License Reference

A reference to a Kubernetes Secret that contains your Gravitee license key. This license is required to unlock advanced capabilities like Kafka protocol support.

#### Kafka Support

The kafka block enables Kafka traffic routing in the Gateway. By default, Kafka support is disabled and must be explicitly turned on.

When enabled, you can also configure:

* Broker Domain Pattern: Defines how broker hostnames are constructed. Defaults to `broker-{brokerId}-{apiHost}`.
* Bootstrap Domain Pattern: Defines the hostname for Kafka bootstrap connections. Defaults to `{apiHost}`.

You can find details about these configurations options in our [documentation](https://documentation.gravitee.io/apim/kafka-gateway/configure-the-kafka-gateway-and-client).

#### Gravitee YAML

An optional yaml field allows you to provide custom gateway configuration, giving you control over additional configuration blocks available in the gateway [settings](https://documentation.gravitee.io/apim/configure-apim/apim-components/gravitee-gateway).

However, this does not allow you to configure:

* Listeners, as they are automatically built from your Gateway specification.
* Disabling Kubernetes sync, since it is required for your routes to be deployed to the Gateway.
* Connecting your Gateway to a management repository, because Gateway API gateways are designed to sync their configuration directly from your Kubernetes cluster.

#### Configuring Kubernetes Components

Within the kubernetes block of the GatewayClassParameters spec, the `deployment` and `service` sections allow you to fine-tune how the Gravitee Gateway runs within your Kubernetes cluster by customizing core Kubernetes resources:

**Deployment**

You can modify pod labels and annotations, adjust the number of replicas to control scaling, specify update strategies for rolling updates, and override the pod template to customize container specs, security settings, or environment variables. This gives you flexible control over how the Gateway pods are deployed and managed.

The template.spec field under the Kubernetes deployment section uses the standard Kubernetes Pod template specification, and its contents will be merged using a [strategic merge patch](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/update-api-object-kubectl-patch/) with Gravitee's default deployment configuration. This allows you to override only the parts you need, such as the container image or security settings, without redefining the entire deployment.

**Service**

You can customize the Kubernetes Service that exposes the Gateway by adding labels and annotations, choosing the service type (the default type is `LoadBalancer`), configuring the external traffic policy, and specifying the load balancer class. These settings influence how the Gateway is accessed both inside and outside the cluster.

{% hint style="info" %}
**For more information**

* The `GatewayClassParameters` CRD API reference is documented [here](../../reference/api-reference.md).
{% endhint %}
