# System Proxy for Backend APIs

## Overview

This guide explains how to configure a **System Proxy** that the Gravitee Gateway uses to communicate with backend APIs. This is useful when:

* Your Gateway needs to reach external backend APIs through a corporate proxy.
* You want a central proxy configuration for all API endpoints.&#x20;
* APIs are configured with `useSystemProxy:true` in their endpoint settings.

## How it Works

1. Configure the system proxy in the Gateway.&#x20;
2. Create an API with an endpoint pointing to your backend.
3. Enable `useSystemProxy` on each endpoint that should route through the proxy.&#x20;
4. The Gateway routes all backend calls for that API through the system proxy.&#x20;

{% hint style="info" %}
**Selective Proxy Usage**

The system proxy is only used for APIs that enable `useSystemProxy: true` in their endpoint configuration. Internal APIs can bypass the proxy by leaving this option disabled.
{% endhint %}

{% hint style="info" %}
**JWKS retrieval through a proxy**

The system proxy also applies to JWT plan JWKS retrieval when **Use system proxy** is enabled in the [JWT plan configuration](../../secure-and-expose-apis/plans/jwt.md#jwks-retrieval-through-a-corporate-proxy). This is required when the Gateway retrieves JWKS from external identity providers (for example, Microsoft Entra ID, Google, or Okta) through a corporate proxy.
{% endhint %}

## Prerequisites

* Kubernetes cluster with Helm installed
* Corporate proxy server hostname and port
* Proxy authentication credentials&#x20;

## Configuration

### Create Kubernetes Secrets

Create a secret for proxy credentials using the following commands:

```sh
# Create namespace
kubectl create namespace gravitee-apim

# Create proxy credentials secret
kubectl create secret generic system-proxy-credentials \
  --from-literal=username=proxy-user \
  --from-literal=password=proxy-password \
  -n gravitee-apim
```

### Configure Helm Values

The Helm values file defines the system proxy settings that the Gateway uses at runtime. Create a `values.yaml` file with the system proxy configuration using the following configuration:

{% tabs %}
{% tab title="Helm values.yaml" %}
```yaml
management:
  type: mongodb

ratelimit:
  type: mongodb

gateway:
  enabled: true

  # System Proxy Configuration (via environment variables)
  env:
    # Enable System Proxy
    - name: gravitee_system_proxy_enabled
      value: "true"

    # Proxy Type
    - name: gravitee_system_proxy_type
      value: "HTTP"                            # Options: HTTP, SOCKS4, SOCKS5

    # HTTP Proxy Host and Port
    - name: gravitee_system_proxy_host
      value: "corporate-proxy.internal"        # REPLACE with your proxy hostname
    - name: gravitee_system_proxy_port
      value: "8080"                            # REPLACE with your proxy port

    # HTTPS Proxy Host and Port
    - name: gravitee_system_proxy_https_host
      value: "corporate-proxy.internal"        # REPLACE with your HTTPS proxy hostname
    - name: gravitee_system_proxy_https_port
      value: "8080"                            # REPLACE with your HTTPS proxy port

    # Proxy Authentication (using Kubernetes Secrets)
    - name: gravitee_system_proxy_username
      valueFrom:
        secretKeyRef:
          name: system-proxy-credentials
          key: username
    - name: gravitee_system_proxy_password
      valueFrom:
        secretKeyRef:
          name: system-proxy-credentials
          key: password
```
{% endtab %}

{% tab title="Environment Variables" %}
For deployments using environment variables directly:

```
gravitee_system_proxy_enabled=true
gravitee_system_proxy_type=HTTP
gravitee_system_proxy_host=corporate-proxy.internal
gravitee_system_proxy_port=8080
gravitee_system_proxy_https_host=corporate-proxy.internal
gravitee_system_proxy_https_port=8080
gravitee_system_proxy_username=proxy-user
gravitee_system_proxy_password=proxy-password
```
{% endtab %}

{% tab title="gravitee.yml" %}
For reference, the equivalent `gravitee.yml` configuration:

```yaml
system:
  proxy:
    enabled: true
    type: HTTP        # HTTP, SOCKS4, SOCKS5
    host: corporate-proxy.internal
    port: 8080
    https:
      host: corporate-proxy.internal
      port: 8080
    username: proxy-user
    password: proxy-password
```
{% endtab %}
{% endtabs %}

### Deploy with Helm

Install the Gateway with your proxy configuration using the following commands:

```sh
helm repo add gravitee https://helm.gravitee.io

helm repo update

helm install gravitee-apim gravitee/apim \
  --namespace gravitee-apim \
  -f values.yaml \
  --wait
```

### Configuration Reference

#### System Proxy Environment Variables

The following table describes the available environment variables for configuring the system proxy:

| Variable                              | Type    | Description                                        |
| ------------------------------------- | ------- | -------------------------------------------------- |
| `gravitee_system_proxy_enabled`       | boolean | Enable the system proxy                            |
| `gravitee_system_proxy_type`          | string  | Proxy protocol: `HTTP`, `SOCKS4`, or `SOCKS5`     |
| `gravitee_system_proxy_host`          | string  | HTTP proxy server hostname                         |
| `gravitee_system_proxy_port`          | integer | HTTP proxy server port                             |
| `gravitee_system_proxy_https_host`    | string  | HTTPS proxy server hostname                        |
| `gravitee_system_proxy_https_port`    | integer | HTTPS proxy server port                            |
| `gravitee_system_proxy_username`      | string  | Proxy authentication username                      |
| `gravitee_system_proxy_password`      | string  | Proxy authentication password                      |

## Configure APIs to Use System Proxy

After deploying the Gateway with the system proxy configured, you must enable it on each API endpoint that should route traffic through the proxy. Each endpoint has a `useSystemProxy` setting that defaults to false.

### Management Console UI

#### **For an existing API:**

1.  From the dashboard, click **APIs** from the left menu, then select the API you want to configure.

    <figure><img src="../../.gitbook/assets/Screenshot 2026-02-09 at 04.08.03.png" alt=""><figcaption></figcaption></figure>
2.  Select **Endpoints**, then select the endpoint group you want to modify.

    <figure><img src="../../.gitbook/assets/Screenshot 2026-02-09 at 04.10.05.png" alt=""><figcaption></figcaption></figure>
3.  Select **Configuration**.

    <figure><img src="../../.gitbook/assets/Screenshot 2026-02-09 at 04.10.55.png" alt=""><figcaption></figcaption></figure>
4.  Scroll to the **Proxy** section and enable **Use System Proxy**.

    <figure><img src="../../.gitbook/assets/image (193).png" alt=""><figcaption></figcaption></figure>
5. Save and deploy your API.&#x20;

#### **For a new API:**

1.  From the dashboard, click **APIs** from the left menu, then click **Add API**.<br>

    <figure><img src="../../.gitbook/assets/Screenshot 2026-02-09 at 03.52.04.png" alt=""><figcaption></figcaption></figure>
2.  Follow the API creation wizard to configure your API details.

    <figure><img src="../../.gitbook/assets/Screenshot 2026-02-09 at 03.54.27.png" alt=""><figcaption></figcaption></figure>
3.  In the **Endpoints** configuration step, input the HTTP proxy target URL.

    <figure><img src="../../.gitbook/assets/Screenshot 2026-02-09 at 03.56.14.png" alt=""><figcaption></figcaption></figure>
4.  In the **Configuration** section, scroll to the **Proxy** section and enable **Use System Proxy**.

    <figure><img src="../../.gitbook/assets/Screenshot 2026-02-09 at 03.56.58.png" alt=""><figcaption></figcaption></figure>
5.  Complete the remaining steps in the API creation wizard, and deploy your API.

    <figure><img src="../../.gitbook/assets/deploy-api-system-proxy.png" alt=""><figcaption></figcaption></figure>

## Verification

#### Verify Gateway Configuration

Confirm that the Gateway has loaded the proxy settings by checking pod environment variables:

```sh
# Check Gateway pod environment variables
kubectl get pod -n gravitee-apim -l app.kubernetes.io/component=gateway \
  -o jsonpath='{.items[0].spec.containers[0].env}' | \
  jq '.[] | select(.name | startswith("gravitee_system_proxy"))'

# Check Gateway logs for proxy configuration
kubectl logs -n gravitee-apim -l app.kubernetes.io/component=gateway | grep -i "system.*proxy"
```

#### Test API Through Proxy

Validate that traffic flows through the proxy by creating a test API:

1. Create a test API pointing to an external backend:
   * Context path: `/test-proxy`
   * Backend: `https://httpbin.org/get`
   * Enable `Use System Proxy` in endpoint configuration
2. Deploy the API
3.  Test through the Gateway:

    ```sh
    curl https://<your-gateway-url>/test-proxy
    ```
4. Check proxy server logs to verify traffic flows through the proxy
