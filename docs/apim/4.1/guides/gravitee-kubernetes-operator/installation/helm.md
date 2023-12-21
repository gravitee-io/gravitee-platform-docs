# Helm

## Overview

Starting with GKO 1.0.0, Helm is the preferred method for installing the operator. The bundle file shipped with v0.x releases is no longer provided, but must be built using Helm template capabilities.

## Installation

The steps to install the GKO on an existing Kubernetes cluster are described below. The Helm Chart is released with each new version of the operator, meaning that upgrading to the latest version consists of upgrading your Helm repository and Helm releases.

### Prerequisites <a href="#prerequisites" id="prerequisites"></a>

* Kubernetes: `>=1.16.0-0`
* ​[Helm v3](https://helm.sh/docs/intro/install/)​
* ​[cert-manager](https://cert-manager.io/docs/installation/) must be installed on the cluster.

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

Assuming that the repository has been aliased as `graviteeio` and that the release name is `graviteeio-gko`:

```bash
$ helm repo update graviteeio
$ helm upgrade --install graviteeio-gko graviteeio/gko
```

## Configuration parameters <a href="#configuration-parameters" id="configuration-parameters"></a>

The Gravitee Kubernetes Operator Helm Chart supports configuration of the following:

* [RBAC](helm.md#rbac)
* [RBAC Proxy](helm.md#rbac-proxy)
* [Controller Manager](helm.md#controller-manager)
* [Ingress](helm.md#ingress)

{% tabs %}
{% tab title="RBAC" %}
Required RBAC resources are created by default for all components involved in the release.

<table><thead><tr><th>Name</th><th width="233">Description</th><th>Value</th></tr></thead><tbody><tr><td><code>serviceAccount.create</code></td><td>Specifies if a service account should be created for the manager pod.</td><td><code>true</code></td></tr><tr><td><code>serviceAccount.name</code></td><td><a data-footnote-ref href="#user-content-fn-1">Specifies the service account name to use. </a>If the operator is deployed in multiple namespaces by setting <code>scope.cluster</code> to <code>false</code>, a different service account name must be used for each installation.</td><td><code>gko-controller-manager</code></td></tr><tr><td><code>rbac.create</code></td><td>Specifies if RBAC resources should be created.</td><td><code>true</code></td></tr><tr><td><code>rbac.skipClusterRoles</code></td><td>Specifies if cluster roles should be created when RBAC resources are created.</td><td><code>false</code></td></tr></tbody></table>
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
| `rbacProxy.image.pullPolicy` | Specifies the pull policy to apply to the RBAC proxy image.   | `Always`                         |
{% endtab %}

{% tab title="Controller Manager" %}
Use these parameters to configure the deployment and the ways in which the operator will interact with APIM and custom resources in your cluster.

| Name                                             | Description                                                                                                                                                            | Value                            |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| `manager.image.repository`                       | Specifies the Docker registry and image name to use.                                                                                                                   | `graviteeio/kubernetes-operator` |
| `manager.image.tag`                              | Specifies the Docker image tag to use.                                                                                                                                 | `latest`                         |
| `manager.image.pullPolicy`                       | Specifies the pull policy to apply to the controller manager image.                                                                                                    | `Always`                         |
| `manager.log.format`                             | Specifies log output format. Can be either JSON or console.                                                                                                            | `json`                           |
| `manager.log.level`                              | Specifies log level. Can be either debug, info, warn, or error.                                                                                                        | `info`                           |
| `manager.log.timestamp.field`                    | Specifies the name of the field to use for the timestamp.                                                                                                              | `timestamp`                      |
| `manager.log.timestamp.format`                   | Specifies the format to use for the timestamp. Can be iso-8601, epoch-second, epoch-millis or epoch-nano.                                                              | `epoch-second`                   |
| `manager.configMap.name`                         | The name of the ConfigMap used to set the manager config from these values.                                                                                            | `gko-config`                     |
| `manager.resources.limits.cpu`                   | The CPU resource limits for the GKO Manager container.                                                                                                                 | `500m`                           |
| `manager.resources.limits.memory`                | The memory resources limits for the GKO Manager container.                                                                                                             | `128Mi`                          |
| `manager.resources.requests.cpu`                 | The requested CPU for the GKO Manager container.                                                                                                                       | `5m`                             |
| `manager.resources.requests.memory`              | The requested memory for the GKO Manager container.                                                                                                                    | `64Mi`                           |
| `manager.scope.cluster`                          | Use `false` to listen only in the release namespace.                                                                                                                   | `true`                           |
| `manager.metrics.enabled`                        | If true, a metrics server will be created so that metrics can be scraped using Prometheus.                                                                             | `true`                           |
| `manager.metrics.secured`                        | If true, the metrics will be served over TLS.                                                                                                                          | `true`                           |
| `manager.metrics.monitor.create`                 | If true, a service monitor will be created for the metrics server (requires the [prometheus operator](https://prometheus-operator.dev/) to be running on the cluster). | `false`                          |
| `manager.metrics.monitor.insecureSkipCertVerify` | If true, the service monitor will not verify the certificate used by the metrics server.                                                                               | `true`                           |
| `manager.metrics.certDir`                        | The directory where the TLS certificate and key will be stored. If empty, a self signed certificate will be generated.                                                 | `""`                             |
| `manager.metrics.port`                           | Which port the metrics server will bind to.                                                                                                                            | `8080`                           |
| `manager.probe.port`                             | The port the readiness and liveness probes will listen to.                                                                                                             | `8081`                           |
| `manager.httpClient.insecureSkipCertVerify`      | If true, the manager HTTP client will not verify the certificate used by the Management API.                                                                           | `false`                          |
| `manager.httpClient.timeoutSeconds`              | The timeout (in seconds) used when issuing requests to the Management API.                                                                                             | `10`                             |
| `manager.webhook.enabled`                        | If true, the manager will register a Webhook server operating on custom resources.                                                                                     | `true`                           |
| `manager.webhook.service.name`                   | The service used to expose the Webhook server.                                                                                                                         | `gko-webhook`                    |
| `manager.webhook.service.port`                   | The port the Webhook server will listen to.                                                                                                                            | `9443`                           |
| `manager.webhook.cert.create`                    | If true, a secret will be created to store the Webhook server certificate.                                                                                             | `true`                           |
| `manager.webhook.cert.name`                      | The name of the cert-manager certificate used by the Webhook server.                                                                                                   | `gko-webhook-cert`               |
| `manager.webhook.cert.secret.name`               | The name of the secret storing the Webhook server certificate.                                                                                                         | `gko-webhook-cert`               |
| `manager.volumes`                                | Volumes to add to the manager pod.                                                                                                                                     | `[]`                             |
| `manager.volumeMounts`                           | Volume mounts to add to the manager container.                                                                                                                         | `[]`                             |
{% endtab %}

{% tab title="Ingress" %}
Use the following parameters to configure the behavior of the ingress controller.

When storing templates in ConfigMaps, the ConfigMap should contain a `content` key and a `contentType` key, for example:

```yaml
content: '{ "message": "Not Found" }'
contentType: application/json
```

<table><thead><tr><th width="229">Name</th><th width="271">Description</th><th>Value</th></tr></thead><tbody><tr><td><code>ingress.templates.404.name</code></td><td>Name of the ConfigMap storing the HTTP 404 ingress response template.</td><td><code>""</code></td></tr><tr><td><code>ingress.templates.404.namespace</code></td><td>Namespace of the ConfigMap storing the HTTP 404 ingress response template.</td><td><code>""</code></td></tr></tbody></table>
{% endtab %}
{% endtabs %}

[^1]: I forgot to add a precision here. Something like: "If you are deploying the operator in several namespaces ny setting \`scope.cluster\` to \`false\`, a different service account name \*must\* be used on each installation.
