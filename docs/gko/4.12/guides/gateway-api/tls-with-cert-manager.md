# Configure TLS with cert-manager

## Overview

[cert-manager](https://cert-manager.io/) automates TLS certificate provisioning in Kubernetes. When integrated with the GKO Gateway API controller, cert-manager automatically creates and renews TLS certificates for your Gateway HTTPS listeners.

The integration is cooperative: cert-manager watches your `Gateway` resource for annotations and creates the TLS Secret, while GKO watches the Secret and configures the Gravitee Gateway to use it. No direct dependency exists between the two — they communicate through standard Kubernetes resources.

### How it works

The cert-manager integration follows this flow:

1. Create a `Gateway` resource with cert-manager annotations and a `certificateRefs` entry on the HTTPS listener.
2. cert-manager detects the Gateway, reads the annotations, and creates a `Certificate` resource.
3. cert-manager provisions the TLS certificate and stores it in a Kubernetes Secret matching the `certificateRefs` name.
4. GKO detects the Secret, validates it contains PEM-encoded `tls.crt` and `tls.key` data, and reconciles the Gateway.
5. The Gravitee Gateway serves HTTPS traffic using the provisioned certificate.
6. cert-manager automatically renews the certificate before expiry.

{% hint style="info" %}
Each HTTPS listener supports exactly one `certificateRef`. Specifying multiple certificate references on a single listener isn't supported.
{% endhint %}

## Prerequisites

Before configuring TLS with cert-manager, verify the following:

* Install GKO with the Gateway API controller enabled. See [Gateway API](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/gateway-api) for setup instructions.
* Verify a `GatewayClass` and `GatewayClassParameters` resource exist and the GatewayClass is in `Accepted=True` state.

## Install cert-manager

1. Add the Jetstack Helm repository:

    ```sh
    helm repo add jetstack https://charts.jetstack.io
    helm repo update jetstack
    ```

2. Install cert-manager with Gateway API support enabled:

    ```sh
    helm upgrade --install cert-manager jetstack/cert-manager \
      --namespace cert-manager \
      --create-namespace \
      --version v1.17.0 \
      --set crds.enabled=true \
      --set config.kind="ControllerConfiguration" \
      --set config.enableGatewayAPI=true
    ```

    {% hint style="warning" %}
    The `config.enableGatewayAPI=true` flag is required. Without it, cert-manager won't watch `Gateway` resources for certificate provisioning.
    {% endhint %}

3. Verify all cert-manager pods are running:

    ```sh
    kubectl get pods -n cert-manager
    ```

    This command results in the following output:

    ```
    NAME                                       READY   STATUS
    cert-manager-...                           1/1     Running
    cert-manager-cainjector-...                1/1     Running
    cert-manager-webhook-...                   1/1     Running
    ```

## Create a ClusterIssuer

A `ClusterIssuer` defines how cert-manager obtains certificates. This example creates a self-signed issuer for testing:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: self-signed
spec:
  selfSigned: {}
```

Apply the ClusterIssuer:

```sh
kubectl apply -f cluster-issuer.yaml
```

Verify it's ready:

```sh
kubectl get clusterissuers
```

This command results in the following output:

```
NAME          READY   AGE
self-signed   True    10s
```

{% hint style="info" %}
For production environments, use a ClusterIssuer backed by [Let's Encrypt](https://cert-manager.io/docs/configuration/acme/) or your organization's internal CA instead of a self-signed issuer. See the [cert-manager issuer documentation](https://cert-manager.io/docs/configuration/) for all available issuer types.
{% endhint %}

## Configure the Gateway with HTTPS

Add cert-manager annotations to the `Gateway` resource metadata and define an HTTPS listener with a `certificateRefs` entry. The `certificateRefs` name (`https-server` in this example) tells cert-manager what to name the Secret it creates.

### Cert-manager annotations

The following cert-manager annotations are supported on `Gateway` resources:

| Annotation | Description | Example |
| --- | --- | --- |
| `cert-manager.io/cluster-issuer` | Name of the `ClusterIssuer` to use for certificate provisioning | `self-signed` |
| `cert-manager.io/issuer` | Name of a namespace-scoped `Issuer` (alternative to `cluster-issuer`) | `my-ca-issuer` |
| `cert-manager.io/usages` | Comma-separated list of certificate key usages | `server auth` |
| `cert-manager.io/common-name` | Common Name (CN) for the certificate subject | `*.apis.example.dev` |
| `cert-manager.io/subject-organizations` | Organization (O) for the certificate subject | `gravitee` |

For a full list of supported annotations, see the [cert-manager Gateway API documentation](https://cert-manager.io/docs/usage/gateway/).

### Gateway manifest

{% code lineNumbers="true" %}

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gravitee-gateway
  annotations:
    cert-manager.io/cluster-issuer: self-signed
    cert-manager.io/usages: "server auth"
    cert-manager.io/subject-organizations: gravitee
    cert-manager.io/common-name: "*.apis.example.dev"
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
```

{% endcode %}

Apply the Gateway:

```sh
kubectl apply -f gateway.yaml
```

When this Gateway is created, the following occurs:

* cert-manager reads the annotations and the HTTPS listener's `hostname` field.
* cert-manager creates a `Certificate` resource with the Secret name `https-server`, DNS names from the listener hostname (`*.apis.example.dev`), and subject fields from the annotations.
* cert-manager provisions the certificate and stores it in the `https-server` Secret.
* GKO validates the Secret and configures the Gravitee Gateway with a PEM keystore referencing the Secret.

## Verification

To verify cert-manager integration is working as expected, follow these steps:

1. Check that cert-manager created the Certificate resource:

    ```sh
    kubectl get certificates
    ```

    This command results in the following output:

    ```
    NAME           READY   SECRET         AGE
    https-server   True    https-server   30s
    ```

2. Inspect the Certificate details:

    ```sh
    kubectl describe certificate https-server
    ```

    Verify the output shows:
    * `Status: True` for the `Ready` condition
    * `Dns Names` matching the listener hostname
    * `Issuer Ref` pointing to the ClusterIssuer
    * `Secret Name` matching the `certificateRefs` name

3. Verify the TLS Secret contains valid certificate data:

    ```sh
    kubectl get secret https-server -o jsonpath='{.data.tls\.crt}' \
      | base64 -d \
      | openssl x509 -noout -subject -issuer -dates
    ```

    This command results in the following output (values depend on your ClusterIssuer configuration):

    ```
    subject=O=gravitee, CN=*.apis.example.dev
    issuer=O=gravitee, CN=*.apis.example.dev
    notBefore=...
    notAfter=...
    ```

4. Verify the Gateway HTTPS listener resolved the certificate reference:

    ```sh
    kubectl get gateway gravitee-gateway \
      -o jsonpath='{.status.listeners[?(@.name=="https")].conditions[?(@.type=="ResolvedRefs")].status}'
    ```

    This command results in the following output:

    ```
    True
    ```

5. Retrieve the Gateway's external address:

    ```sh
    export GW_ADDR=$(kubectl get gateway gravitee-gateway \
      -o jsonpath='{.status.addresses[0].value}')
    echo "$GW_ADDR"
    ```

    {% hint style="info" %}
    If using a `kind` cluster with [cloud-provider-kind](https://github.com/kubernetes-sigs/cloud-provider-kind), the address is the IP assigned to the LoadBalancer Service. If using Docker Desktop or a cloud provider, the address is typically `localhost` or an external IP.
    {% endhint %}

6. Verify the Gravitee Gateway serves the certificate over HTTPS:

    ```sh
    echo | openssl s_client -connect "$GW_ADDR":443 \
      -servername demo.apis.example.dev 2>/dev/null \
      | openssl x509 -noout -subject -issuer
    ```

    The output confirms the certificate subject and issuer match what cert-manager provisioned.

7. Test an HTTPS request through the Gateway:

    ```sh
    curl -ik --resolve demo.apis.example.dev:443:"$GW_ADDR" \
      https://demo.apis.example.dev/bin/hostname
    ```

    The response includes `X-Gravitee-Transaction-Id` and `X-Gravitee-Request-Id` headers, confirming the request passed through the Gravitee Gateway over HTTPS.

    {% hint style="info" %}
    The `-k` flag skips certificate verification, which is necessary for self-signed certificates. For production deployments with certificates from a trusted CA, omit the `-k` flag.
    {% endhint %}

## Full example

This example deploys a complete Gateway API setup with TLS, routing traffic from an HTTPS listener to a backend service.

### 1. Create the ClusterIssuer

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: self-signed
spec:
  selfSigned: {}
```

### 2. Create GatewayClassParameters and GatewayClass

{% code lineNumbers="true" %}

```yaml
apiVersion: gravitee.io/v1alpha1
kind: GatewayClassParameters
metadata:
  name: gravitee-gateway
spec:
  kubernetes:
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
```

{% endcode %}

### 3. Create the Gateway with cert-manager annotations

{% code lineNumbers="true" %}

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: gravitee-gateway
  annotations:
    cert-manager.io/cluster-issuer: self-signed
    cert-manager.io/usages: "server auth"
    cert-manager.io/subject-organizations: gravitee
    cert-manager.io/common-name: "*.apis.example.dev"
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
```

{% endcode %}

### 4. Deploy a backend service

{% code lineNumbers="true" %}

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpbin-1
  labels:
    type: httpbin-1
spec:
  replicas: 1
  selector:
    matchLabels:
      type: httpbin-1
  template:
    metadata:
      labels:
        type: httpbin-1
    spec:
      containers:
      - name: httpbin-1
        image: mccutchen/go-httpbin:latest
        ports:
        - containerPort: 8080
        env:
        - name: USE_REAL_HOSTNAME
          value: "true"
---
apiVersion: v1
kind: Service
metadata:
  name: httpbin-1
  labels:
    type: httpbin-1
spec:
  ports:
    - port: 8080
      targetPort: 8080
  selector:
    type: httpbin-1
```

{% endcode %}

### 5. Create an HTTPRoute

{% code lineNumbers="true" %}

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: http-route-demo
spec:
  parentRefs:
  - name: gravitee-gateway
    kind: Gateway
    group: gateway.networking.k8s.io
    namespace: default
  hostnames:
   - demo.apis.example.dev
  rules:
    - matches:
       - path:
           type: PathPrefix
           value: /bin
      backendRefs:
        - kind: Service
          group: ""
          name: httpbin-1
          namespace: default
          port: 8080
```

{% endcode %}

### 6. Apply all resources

```sh
kubectl apply -f cluster-issuer.yaml
kubectl apply -f gateway-class-parameters.yaml
kubectl apply -f gateway.yaml
kubectl apply -f backend.yaml
kubectl apply -f http-route.yaml
```

### 7. Wait for the Gateway to be ready

```sh
kubectl wait --for=condition=programmed gateway/gravitee-gateway --timeout=300s
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=gravitee-gateway --timeout=300s
```

### 8. Get the Gateway address and test

```sh
export GW_ADDR=$(kubectl get gateway gravitee-gateway \
  -o jsonpath='{.status.addresses[0].value}')
```

Test HTTP:

```sh
curl -i --resolve demo.apis.example.dev:80:"$GW_ADDR" \
  http://demo.apis.example.dev/bin/hostname
```

Test HTTPS:

```sh
curl -ik --resolve demo.apis.example.dev:443:"$GW_ADDR" \
  https://demo.apis.example.dev/bin/hostname
```

Both requests return `X-Gravitee-*` headers, confirming the Gravitee Gateway processed the request. The HTTPS request uses the certificate provisioned by cert-manager.

## Cross-namespace certificate references

To reference a TLS Secret in a different namespace from the Gateway, create a `ReferenceGrant` in the Secret's namespace:

{% code lineNumbers="true" %}

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: ReferenceGrant
metadata:
  name: allow-gateway-tls
  namespace: cert-secrets
spec:
  from:
    - group: gateway.networking.k8s.io
      kind: Gateway
      namespace: default
  to:
    - group: ""
      kind: Secret
```

{% endcode %}

This grants the Gateway in the `default` namespace permission to reference Secrets in the `cert-secrets` namespace.

## Constraints

* Each HTTPS listener accepts exactly **one** `certificateRef`. Specifying multiple references causes the listener to enter a `TooManyCertificateRefs` state.
* The `certificateRef` kind is `Secret` and the group is `""` (Kubernetes core API group). Other kinds aren't supported.
* The Secret contains PEM-encoded `tls.crt` and `tls.key` fields. Secrets with missing or malformed PEM data are rejected.
* GKO watches for changes to referenced Secrets and automatically re-reconciles the Gateway when a certificate is renewed.

## What's next

* [Gateway API overview](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/gateway-api): Set up GatewayClass, GatewayClassParameters, and Gateway resources.
* [Configure DNS with external-dns](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/gateway-api/dns-with-external-dns): Configure DNS record creation for Gateway Services.
* [HTTPRoute](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/guides/gateway-api/httproute): Configure path-based routing, header matching, and traffic splitting.
* [GatewayClassParameters](https://documentation.gravitee.io/gravitee-kubernetes-operator-gko/overview/custom-resource-definitions/gatewayclassparameters): Configure Gravitee-specific Gateway API settings.
* [cert-manager Gateway API documentation](https://cert-manager.io/docs/usage/gateway/): Full reference for cert-manager's Gateway API integration.
