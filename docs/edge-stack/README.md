---
noIndex: true
---

# Ambassador Edge Stack Quick Start

To begin using Ambassador Edge Stack, you’ll start by obtaining a license, applying the license to your environment, installing Ambassador Edge Stack, and configuring it to route traffic from the edge of your Kubernetes cluster. This guide walks you through each step so you can quickly get started.

### Obtaining a license

To obtain a license for Ambassador Edge Stack, [contact us](https://www.getambassador.io/contact-us). Our team will provide a JSON Web Token (JWT).

We recommend saving your license as a variable using the `export LICENSE_KEY="your-jwt-token"` command. Then, you can reference it as `$LICENSE_KEY` in the following steps.

### Applying the JWT to your environment

After you obtain your JWT, apply it to your environment either manually or using Helm. If you're using the Helm installation option, we recommend applying the JWT during installation. For more information, see [Install using Helm](./#install-using-helm).

#### Apply the JWT manually

To manually apply the JWT to your cluster, you need to Base64 encode it.

1.  Use the following command to encode the license.

    ```shell
    echo LICENSE_KEY | base64
    ```
2.  Create a Kubernetes secret named `ambassador-edge-stack` in the `ambassador` namespace, and then set its `license-key` field to your Base64-encoded license key. The following example shows what the resulting secret should look like.

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: ambassador-edge-stack
      namespace: ambassador
    data:
      license-key: LICENSE_KEY
    ```

    > **Note:** If you're transitioning from an Ambassador Cloud token to a JWT, delete the cloud token secret after applying the new JWT secret. Edge Stack will automatically detect and use the JWT secret for licensing.

### Installing Ambassador Edge Stack

You can install Ambassador Edge Stack either manually or using Helm.

#### Install manually

Use the following procedure to install Ambassador Edge Stack manually.

1.  Apply Kubernetes Custom Resource Definitions (CRDs) and wait for the deployment.

    ```shell
    kubectl apply -f https://app.getambassador.io/yaml/edge-stack/3.12.9/aes-crds.yaml && \
    kubectl wait --timeout=90s --for=condition=available deployment emissary-apiext -n emissary-system
    ```
2.  Install the components and wait for Ambassador Edge Stack.

    ```shell
    kubectl apply -f https://app.getambassador.io/yaml/edge-stack/3.12.9/aes.yaml && \
    kubectl -n ambassador wait --for condition=available --timeout=90s deploy -l product=aes
    ```

#### Install using Helm

Use the following procedure to install Ambassador Edge Stack using Helm.

> **Note:** If you didn't apply the JWT manually, use the following flag with the `helm install` command: `--set licenseKey.value=$LICENSE_KEY`.

1.  Add the repository.

    ```shell
    helm repo add datawire https://app.getambassador.io
    ```

    ```shell
    helm repo update
    ```
2.  Create a namespace and install.

    ```shell
    kubectl create namespace ambassador && \
    kubectl apply -f https://app.getambassador.io/yaml/edge-stack/3.12.9/aes-crds.yaml
    ```

    ```shell
    kubectl wait --timeout=90s --for=condition=available deployment emissary-apiext -n emissary-system
    ```

    ```shell
    helm install edge-stack --namespace ambassador datawire/edge-stack && \
    kubectl -n ambassador wait --for condition=available --timeout=90s deploy -l product=aes
    ```

### Routing traffic from the edge

Ambassador Edge Stack uses Kubernetes Custom Resource Definitions (CRDs) to declaratively define its desired state. The workflow you're going to build uses a simple demo app, `Listener` CRD, and `Mapping` CRD. The `Listener` CRD tells Ambassador Edge Stack which port to listen on, and the `Mapping` CRD tells Ambassador Edge Stack how to route incoming requests from the edge of your cluster to the correct Kubernetes service based on the request’s host and URL path.

1.  Create a `Listener` resource for HTTP on port 8080.

    ```shell
    kubectl apply -f - <<EOF
    ---
    apiVersion: getambassador.io/v3alpha1
    kind: Listener
    metadata:
      name: edge-stack-listener-8080
      namespace: ambassador
    spec:
      port: 8080
      protocol: HTTP
      securityModel: XFP
      hostBinding:
        namespace:
          from: ALL
    ---
    apiVersion: getambassador.io/v3alpha1
    kind: Listener
    metadata:
      name: edge-stack-listener-8443
      namespace: ambassador
    spec:
      port: 8443
      protocol: HTTPS
      securityModel: XFP
      hostBinding:
        namespace:
          from: ALL
    EOF
    ```
2.  Apply the following YAML for the `quote` service.

    ```shell
    kubectl apply -f https://app.getambassador.io/yaml/v2-docs/3.9.1/quickstart/qotm.yaml
    ```

    \{% hint style="info" %\} The service and deployment are created in your default namespace. You can use `kubectl get services,deployments quote` to see their status. \{% endhint %\}3. Apply the following YAML to your target cluster to tell Ambassador Edge Stack to route all inbound traffic to the `/backend/` path to the `quote` service.

    ```sh
    kubectl apply -f - <<EOF
    ---
    apiVersion: getambassador.io/v3alpha1
    kind: Mapping
    metadata:
      name: quote-backend
    spec:
      hostname: "*"
      prefix: /backend/
      service: quote
      docs:
        path: "/.ambassador-internal/openapi-docs"
    EOF
    ```
3.  Store the Ambassador Edge Stack load balancer IP address using a local environment variable. You'll use this variable to test access to your service.

    ```sh
    export LB_ENDPOINT=$(kubectl -n ambassador get svc  edge-stack \
      -o "go-template={{range .status.loadBalancer.ingress}}{{or .ip .hostname}}{{end}}")
    ```
4.  Test the configuration by accessing the service through the Ambassador Edge Stack load balancer.

    ```
    $ curl -Lki https://$LB_ENDPOINT/backend/

      HTTP/1.1 200 OK
      content-type: application/json
      date: Wed, 23 Jun 2021 16:49:46 GMT
      content-length: 163
      x-envoy-upstream-service-time: 0
      server: envoy

      {
          "server": "serene-grapefruit-gjd4yodo",
          "quote": "The last sentence you read is often sensible nonsense.",
          "time": "2021-06-23T16:49:46.613322198Z"
      }
    ```

### Next steps

Explore some of the popular tutorials on Ambassador Edge Stack:

* [the-mapping-resource.md](technical-reference/using-custom-resources/the-mapping-resource.md "mention"): Declaratively route traffic from the edge of your cluster to a Kubernetes service.
* [the-host-resource.md](technical-reference/using-custom-resources/the-host-resource.md "mention"): Configure a hostname and TLS options for your ingress.
* [rate-limiting-reference.md](edge-stack-user-guide/rate-limiting/rate-limiting-reference.md "mention"): Create policies to control sustained traffic loads.

Ambassador Edge Stack has a comprehensive range of [features-and-benefits.md](features-and-benefits.md "mention") to support the requirements of any edge microservice. To learn more about how Ambassador Edge Stack works, see [why-ambassador-edge-stack.md](why-ambassador-edge-stack.md "mention")
