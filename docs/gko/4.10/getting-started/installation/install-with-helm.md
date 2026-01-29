# Install with Helm

## Overview

Helm is the preferred method for installing the Gravitee Kubernetes Operator.

{% hint style="warning" %}
Existing Gravitee Helm Charts do not support the creation of a TCP server on the Gateway. User customization of the Helm Charts is required for TCP proxy APIs.
{% endhint %}

## Installation

The steps to install the GKO on an existing Kubernetes cluster are described below. The GKO Helm Chart is released with each new version of the operator, meaning that upgrading to the latest version consists of upgrading your Helm repository and Helm releases.

### Prerequisites <a href="#prerequisites" id="prerequisites"></a>

* Kubernetes: `>=1.16.0-0`
* ​[Helm v3](https://helm.sh/docs/intro/install/)​

### Installation steps <a href="#install-steps" id="install-steps"></a>

1.  Add the Gravitee Helm Chart repo:

    ```bash
    helm repo add graviteeio https://helm.gravitee.io
    ```
2.  Install the chart with the release name `graviteeio-gko`:

    ```bash
    helm install graviteeio-gko graviteeio/gko
    ```

## Upgrading the Operator <a href="#upgrading-the-operator" id="upgrading-the-operator"></a>

The following commands assume that the repository has been aliased as `graviteeio` and that the release name is `graviteeio-gko`:

```bash
$ helm repo update graviteeio
$ helm upgrade --install graviteeio-gko graviteeio/gko
```

## Configuration parameters <a href="#configuration-parameters" id="configuration-parameters"></a>

The Gravitee Kubernetes Operator Helm Chart supports the configuration of the following:

* [RBAC](install-with-helm.md#rbac)
* [RBAC Proxy](install-with-helm.md#rbac-proxy)
* [Controller Manager](install-with-helm.md#controller-manager)
* [Ingress](install-with-helm.md#ingress)

{% tabs %}
{% tab title="RBAC" %}
Required RBAC resources are created by default for all components involved in the release.

<table><thead><tr><th width="272">Name</th><th width="233">Description</th><th>Value</th></tr></thead><tbody><tr><td><code>serviceAccount.create</code></td><td>Specifies if a service account should be created for the manager pod.</td><td><code>true</code></td></tr><tr><td><code>serviceAccount.name</code></td><td><a data-footnote-ref href="#user-content-fn-1">Specifies the service account name to use. </a>If the operator is deployed in multiple namespaces by setting <code>scope.cluster</code> to <code>false</code>, a different service account name must be used for each installation.</td><td><code>gko-controller-manager</code></td></tr><tr><td><code>rbac.create</code></td><td>Specifies if RBAC resources should be created.</td><td><code>true</code></td></tr><tr><td><code>rbac.skipClusterRoles</code></td><td>Specifies if cluster roles should be created when RBAC resources are created. You may need to disable templating for the manager to read secrets and ConfigMaps in other namespaces.</td><td><code>false</code></td></tr><tr><td><code>manager.scope.namespaces</code></td><td>Specify a list of namespaces that GKO is going to watch for CRDs in the following form: <code>["ns1", "ns2", "ns3"]</code>. With this parameter,  GKO does not need ClusterRole-Binding and has access to resources in only these specific namespaces. If you provide this list, ensure that <code>manager.scope.cluster=true</code></td><td><code>[]</code></td></tr></tbody></table>
{% endtab %}

{% tab title="RBAC Proxy" %}
Kube RBAC Proxy is deployed as a sidecar container and restricts access to the Prometheus metrics endpoint.

{% hint style="warning" %}
If this is disabled, the Prometheus metrics endpoint will be exposed with no access control at all.
{% endhint %}

| Name                         | Description                                                   | Value                            |
| ---------------------------- | ------------------------------------------------------------- | -------------------------------- |
| `rbacProxy.enabled`          | Specifies if the `kube-rbac-proxy` sidecar should be enabled. | `true`                           |
| `rbacProxy.image.repository` | Specifies the Docker registry and image name to use.          | `quay.io/brancz/kube-rbac-proxy` |
| `rbacProxy.image.tag`        | Specifies the Docker image tag to use.                        | `v0.14.3`                        |
{% endtab %}

{% tab title="Controller Manager" %}
Use these parameters to configure the deployment, and the ways in which the operator will interact with APIM and custom resources in your cluster.

| Name                                        | Description                                                                                  | Value                            |
| ------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------- |
| `manager.image.repository`                  | Specifies the Docker registry and image name to use.                                         | `graviteeio/kubernetes-operator` |
| `manager.image.tag`                         | Specifies the Docker image tag to use.                                                       | `latest`                         |
| `manager.log.json`                          | If true, the manager logs are written in JSON format.                                        | `true`                           |
| `manager.configMap.name`                    | The name of the ConfigMap used to set the manager config from these values.                  | `gko-config`                     |
| `manager.resources.limits.cpu`              | The CPU resource limits for the GKO Manager container.                                       | `500m`                           |
| `manager.resources.limits.memory`           | The memory resources limits for the GKO Manager container.                                   | `128Mi`                          |
| `manager.resources.requests.cpu`            | The requested CPU for the GKO Manager container.                                             | `5m`                             |
| `manager.resources.requests.memory`         | The requested memory for the GKO Manager container.                                          | `64Mi`                           |
| `manager.scope.cluster`                     | Use `false` to listen only in the release namespace.                                         | `true`                           |
| `manager.metrics.enabled`                   | If true, a metrics server will be created so that metrics can be scraped using Prometheus.   | `true`                           |
| `manager.probe.port`                        | The port the readiness and liveness probes will listen to.                                   | `8081`                           |
| `manager.httpClient.insecureSkipCertVerify` | If true, the manager HTTP client will not verify the certificate used by the Management API. | `false`                          |
| `manager.httpClient.timeoutSeconds`         | The timeout (in seconds) used when issuing requests to the Management API.                    | `5`                              |
| `manager.httpClient.proxy.enabled`          | If true, GKO will use your proxy when making any external call                               | `false`                          |
| `manager.httpClient.proxy.useSystemProxy`   | If true, GKO will use `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` environment variables (or lowercase versions).| `false`            |
| `manager.httpClient.proxy.url`              | The proxy URL, e.g., `http://localhost:8080` or `socks5://localhost:1080`.                           | `""`                             |
| `manager.httpClient.proxy.username`         | The proxy username if authentication is needed                                               | `""`                             |
| `manager.httpClient.proxy.password`         | The proxy password if authentication is needed                                               | `""`                             |
| `manager.httpClient.trustStore.path`        | Path to a custom trust store file (PEM format). Not needed if certificates are in `/etc/ssl/certs`. | `""` |
| `manager.templating.enabled`                | If false resources containing markers `[[...]]` will not be evaluated.                       | `true`                           |


{% endtab %}

{% tab title="Ingress" %}
Use the following parameters to configure the behavior of the ingress controller.

<table><thead><tr><th width="229">Name</th><th width="271">Description</th><th>Value</th></tr></thead><tbody><tr><td><code>ingress.templates.404.name</code></td><td>Name of the ConfigMap storing the HTTP 404 ingress response template.</td><td><code>""</code></td></tr><tr><td><code>ingress.templates.404.namespace</code></td><td>Namespace of the ConfigMap storing the HTTP 404 ingress response template.</td><td><code>""</code></td></tr><tr><td><code>ingress.controller.enabled</code></td><td>Indicates if the GKO ingress controller is enabled or not.</td><td><code>true</code></td></tr></tbody></table>

When storing templates in ConfigMaps, the ConfigMap should contain a `content` key and a `contentType` key, for example:

```yaml
content: '{ "message": "Not Found" }'
contentType: application/json
```
{% endtab %}
{% endtabs %}

[^1]: I forgot to add a precision here. Something like: "If you are deploying the operator in several namespaces ny setting \`scope.cluster\` to \`false\`, a different service account name \*must\* be used on each installation.
