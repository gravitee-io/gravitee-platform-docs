# DNS with external-dns

## Overview

[external-dns](https://github.com/kubernetes-sigs/external-dns) automates DNS record management in Kubernetes. It watches for Kubernetes Services with specific annotations and creates corresponding DNS records in your DNS provider (for example, AWS Route 53, Google Cloud DNS, Cloudflare, or Azure DNS).

When GKO deploys a Gravitee Gateway from a `Gateway` resource, it creates a Kubernetes `LoadBalancer` Service. By adding external-dns annotations to the `GatewayClassParameters` resource, GKO propagates those annotations to the deployed Service. external-dns then detects the annotated Service and creates DNS records pointing to the Gateway's load balancer IP.

### How it works

The external-dns integration follows this flow:

1. Define external-dns annotations in the `GatewayClassParameters` resource under `spec.kubernetes.service.annotations`.
2. GKO creates the Gateway's Kubernetes Service with those annotations applied.
3. external-dns detects the annotated `LoadBalancer` Service and reads the `external-dns.alpha.kubernetes.io/hostname` annotation.
4. external-dns creates or updates DNS records in your configured DNS provider, mapping the hostname to the load balancer's external IP.
5. Traffic reaches the Gravitee Gateway through the DNS hostname.

## Prerequisites

Before configuring DNS with external-dns:

* Install GKO with the Gateway API controller enabled. See [Gateway API](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/gateway-api) for setup instructions.
* Verify a `GatewayClass` and `GatewayClassParameters` resource exist and the GatewayClass is in `Accepted=True` state.
* Install external-dns in your cluster with access to your DNS provider. See the [external-dns documentation](https://kubernetes-sigs.github.io/external-dns/) for provider-specific setup guides.

{% hint style="info" %}
external-dns requires a cloud-based DNS provider. It doesn't function in local development environments (for example, Docker Desktop, kind, or minikube) unless configured with a provider that supports local testing.
{% endhint %}

## Configure GatewayClassParameters with DNS annotations

Add the `external-dns.alpha.kubernetes.io/hostname` annotation to the `spec.kubernetes.service.annotations` field in your `GatewayClassParameters` resource. GKO copies all annotations defined here onto the deployed Gateway's Kubernetes Service.

{% code lineNumbers="true" %}

```yaml
apiVersion: gravitee.io/v1alpha1
kind: GatewayClassParameters
metadata:
  name: gravitee-gateway
spec:
  kubernetes:
    service:
      type: LoadBalancer
      annotations:
        external-dns.alpha.kubernetes.io/hostname: "api.example.dev"
    deployment:
      template:
        spec:
          containers:
          - name: gateway
            image: graviteeio/apim-gateway
```

{% endcode %}

Apply the GatewayClassParameters:

```sh
kubectl apply -f gateway-class-parameters.yaml
```

### Service configuration fields

The `spec.kubernetes.service` section of `GatewayClassParameters` supports the following fields:

| Field | Description | Default |
| --- | --- | --- |
| `type` | Kubernetes Service type | `LoadBalancer` |
| `externalTrafficPolicy` | External traffic routing policy (`Cluster` or `Local`) | `Cluster` |
| `loadBalancerClass` | Load balancer implementation class | — |
| `annotations` | Annotations propagated to the Service (for example, external-dns annotations) | — |
| `labels` | Labels propagated to the Service | — |

### external-dns annotations

The following external-dns annotations are commonly used on the Service:

| Annotation | Description | Example |
| --- | --- | --- |
| `external-dns.alpha.kubernetes.io/hostname` | Comma-separated list of DNS hostnames to create records for | `api.example.dev` |
| `external-dns.alpha.kubernetes.io/ttl` | TTL (in seconds) for the DNS record | `300` |
| `external-dns.alpha.kubernetes.io/target` | Override the target IP or hostname for the DNS record | `10.0.0.1` |

For a full list of supported annotations, see the [external-dns FAQ](https://kubernetes-sigs.github.io/external-dns/latest/faq/).

## Create the GatewayClass and Gateway

1. Create the GatewayClass referencing the annotated GatewayClassParameters:

    ```yaml
    apiVersion: gateway.networking.k8s.io/v1
    kind: GatewayClass
    metadata:
      name: gravitee-gateway
    spec:
      controllerName: apim.gravitee.io/gateway
      parametersRef:
        kind: GatewayClassParameters
        group: gravitee.io
        name: gravitee-gateway
        namespace: default
    ```

2. Create the Gateway:

    ```yaml
    apiVersion: gateway.networking.k8s.io/v1
    kind: Gateway
    metadata:
      name: gravitee-gateway
    spec:
      gatewayClassName: gravitee-gateway
      listeners:
        - name: http
          port: 80
          protocol: HTTP
    ```

3. Apply both resources:

    ```sh
    kubectl apply -f gateway-class.yaml
    kubectl apply -f gateway.yaml
    ```

When GKO reconciles the Gateway, it creates a `LoadBalancer` Service with the external-dns annotations from the `GatewayClassParameters`.

## Verification

To verify external-dns annotation propagation is working as expected, follow these steps:

1. Verify the Gateway is programmed:

    ```sh
    kubectl get gateway gravitee-gateway \
      -o jsonpath='{"Programmed="}{.status.conditions[?(@.type=="Programmed")].status}{"\n"}'
    ```

    This command results in the following output:

    ```
    Programmed=True
    ```

2. Verify the annotations are present on the deployed Service:

    ```sh
    kubectl get svc gravitee-gateway \
      -o jsonpath='{.metadata.annotations.external-dns\.alpha\.kubernetes\.io/hostname}'
    ```

    This command results in the following output:

    ```
    api.example.dev
    ```

3. Verify the Service type is `LoadBalancer`:

    ```sh
    kubectl get svc gravitee-gateway \
      -o jsonpath='{.spec.type}'
    ```

    This command results in the following output:

    ```
    LoadBalancer
    ```

4. Retrieve the Gateway's external address:

    ```sh
    export GW_ADDR=$(kubectl get gateway gravitee-gateway \
      -o jsonpath='{.status.addresses[0].value}')
    echo "$GW_ADDR"
    ```

5. If external-dns is running and configured with your DNS provider, verify the DNS record was created:

    ```sh
    dig +short api.example.dev
    ```

    The output shows the load balancer IP that external-dns configured.

6. Test connectivity through the DNS hostname:

    ```sh
    curl -i http://api.example.dev/bin/hostname
    ```

    The response includes `X-Gravitee-Transaction-Id` and `X-Gravitee-Request-Id` headers, confirming the request reached the Gravitee Gateway through the DNS hostname.

## Full example with TLS

This example combines external-dns for DNS automation with cert-manager for TLS certificate provisioning to create a fully automated HTTPS Gateway.

{% code lineNumbers="true" %}

```yaml
apiVersion: gravitee.io/v1alpha1
kind: GatewayClassParameters
metadata:
  name: gravitee-gateway
spec:
  kubernetes:
    service:
      type: LoadBalancer
      annotations:
        external-dns.alpha.kubernetes.io/hostname: "api.example.dev"
    deployment:
      template:
        spec:
          containers:
          - name: gateway
            image: graviteeio/apim-gateway
---
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
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
    cert-manager.io/cluster-issuer: letsencrypt-prod
    cert-manager.io/usages: "server auth"
spec:
  gatewayClassName: gravitee-gateway
  listeners:
    - name: http
      port: 80
      protocol: HTTP
    - name: https
      port: 443
      protocol: HTTPS
      hostname: '*.api.example.dev'
      tls:
        certificateRefs:
          - group: ""
            kind: Secret
            name: "gateway-tls"
```

{% endcode %}

When applied:

* GKO deploys the Gateway and creates a `LoadBalancer` Service with the external-dns hostname annotation.
* external-dns creates a DNS record for `api.example.dev` pointing to the load balancer IP.
* cert-manager provisions a TLS certificate for `*.api.example.dev` and stores it in the `gateway-tls` Secret.
* GKO configures the Gravitee Gateway with the TLS certificate.
* Traffic reaches the Gateway over HTTPS through the DNS hostname with a valid TLS certificate.

For detailed cert-manager configuration, see [TLS with cert-manager](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/gateway-api/tls-with-cert-manager).

## Multiple hostnames

To create DNS records for multiple hostnames, pass a comma-separated list in the annotation:

```yaml
spec:
  kubernetes:
    service:
      annotations:
        external-dns.alpha.kubernetes.io/hostname: "api.example.dev,gateway.example.dev"
```

## Constraints

* external-dns reads annotations from the Kubernetes Service, not from the Gateway resource directly. Define annotations in `GatewayClassParameters` for GKO to propagate them.
* The Service type defaults to `LoadBalancer`. external-dns typically doesn't create records for `ClusterIP` or `NodePort` Services unless configured to do so.
* DNS record creation depends on external-dns having the correct permissions for your DNS provider. Verify your external-dns deployment has the required IAM roles or API keys.
* Changing the hostname annotation in `GatewayClassParameters` triggers a GKO reconciliation that updates the Service annotations. external-dns then detects the change and updates the DNS records.

## What's next

* [Gateway API overview](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/gateway-api): Set up GatewayClass, GatewayClassParameters, and Gateway resources.
* [TLS with cert-manager](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/gateway-api/tls-with-cert-manager): Automate TLS certificate provisioning for Gateway HTTPS listeners.
* [HTTPRoute](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/gateway-api/httproute): Configure path-based routing, header matching, and traffic splitting.
* [GatewayClassParameters](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/overview/custom-resource-definitions/gatewayclassparameters): Configure Gravitee-specific Gateway API settings.
* [external-dns documentation](https://kubernetes-sigs.github.io/external-dns/): Full reference for external-dns setup and provider configuration.
