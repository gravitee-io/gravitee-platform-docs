# Hybrid Gateway Proxy Configuration

## Overview

This guide explains how to configure a Hybrid Gateway that connects to a remote Management API Bridge or Gravitee Cloud Platform through a corporate proxy. Use this configuration when your Gateway is deployed on-premise or behind a firewall and reaches external services through a corporate proxy.

## Prerequisites

Before you begin, ensure you have the following:

* Kubernetes cluster with [Helm](https://helm.sh/docs/intro/install/) installed.&#x20;
* Corporate proxy server hostname and port.&#x20;
* Proxy authentication credentials.&#x20;
* Bridge Server URL or Gravitee Cloud account.&#x20;
* Bridge authentication credentials.&#x20;

## Configuration

To configure a Hybrid Gateway with a corporate proxy, complete the following steps:

* [#create-kubernetes-secrets](hybrid-gateway-proxy-configuration.md#create-kubernetes-secrets "mention")
* [#configure-helm-values](hybrid-gateway-proxy-configuration.md#configure-helm-values "mention")
* [#deploy-with-helm](hybrid-gateway-proxy-configuration.md#deploy-with-helm "mention")

### Create Kubernetes Secrets

Create secrets for proxy and Bridge authentication credentials using the following commands:

```sh
# Create namespace
kubectl create namespace gravitee-apim

# Create proxy credentials secret
kubectl create secret generic proxy-credentials \
  --from-literal=username=proxy-user \
  --from-literal=password=proxy-password \
  -n gravitee-apim

# Create Bridge authentication secret
kubectl create secret generic bridge-auth \
  --from-literal=username=hybrid-gateway \
  --from-literal=password=bridge-password \
  -n gravitee-apim
```

### Configure Helm Values

Create a `values.yaml` file with the following proxy configurations:

{% tabs %}
{% tab title="Helm values.yaml" %}
```yaml
# Set management type to 'http' for Hybrid Gateway
management:
  type: http

gateway:
  enabled: true

  management:
    http:
      # Bridge Server or Gravitee Cloud URL
      url: "https://bridge.gravitee.io:18092"  # REPLACE with your Bridge URL

      # Connection settings
      keepAlive: true
      idleTimeout: 30000
      connectTimeout: 5000
      readTimeout: 10000
      useCompression: true
      version: HTTP_1_1

      # Connection retry configuration
      connectionRetry:
        delaySec: 2
        maxDelaySec: 60
        backoffFactor: 1.5

      # Bridge authentication
      authentication:
        type: basic
        basic:
          username: hybrid-gateway
          password: your-bridge-password  # Or use secret reference

      # SSL/TLS configuration
      ssl:
        trustAll: false
        verifyHostname: true

      # HTTP Repository Proxy Configuration
      proxy:
        enabled: true
        type: HTTP              # Options: HTTP, SOCKS4, SOCKS5
        host: corporate-proxy.internal
        port: 8080
        username: proxy-user
        password: proxy-password

  # Cloud Reporter Proxy (via environment variables)
  env:
    - name: gravitee_cloud_client_proxy_enabled
      value: "true"
    - name: gravitee_cloud_client_proxy_type
      value: "HTTP"
    - name: gravitee_cloud_client_proxy_host
      value: "corporate-proxy.internal"
    - name: gravitee_cloud_client_proxy_port
      value: "8080"
    - name: gravitee_cloud_client_proxy_username
      valueFrom:
        secretKeyRef:
          name: proxy-credentials
          key: username
    - name: gravitee_cloud_client_proxy_password
      valueFrom:
        secretKeyRef:
          name: proxy-credentials
          key: password
```
{% endtab %}

{% tab title="Environment Variables" %}
When deploying outside of Kubernetes, such as with Docker Compose, systemd services, or standalone Java processes, use environment variables. This approach works for quick testing or for deployment tooling that manages configuration through environment variables rather than configuration files.



**HTTP Repository Proxy:**

```
gravitee_gateway_management_http_proxy_enabled=true
gravitee_gateway_management_http_proxy_type=HTTP
gravitee_gateway_management_http_proxy_host=corporate-proxy.internal
gravitee_gateway_management_http_proxy_port=8080
gravitee_gateway_management_http_proxy_username=proxy-user
gravitee_gateway_management_http_proxy_password=proxy-password
```

**Cloud Reporter Proxy:**

```
gravitee_cloud_client_proxy_enabled=true
gravitee_cloud_client_proxy_type=HTTP
gravitee_cloud_client_proxy_host=corporate-proxy.internal
gravitee_cloud_client_proxy_port=8080
gravitee_cloud_client_proxy_username=proxy-user
gravitee_cloud_client_proxy_password=proxy-password
```
{% endtab %}
{% endtabs %}

### Deploy with Helm

Install the proxy configuration with the following commands:&#x20;

```sh
helm repo add gravitee https://helm.gravitee.io

helm repo update

helm install gravitee-hybrid-gateway gravitee/apim \
  --namespace gravitee-apim \
  -f values.yaml \
  --wait
```

## Configuration Reference

The following sections provide reference information for proxy configuration:

* [#http-repository-proxy-options](hybrid-gateway-proxy-configuration.md#http-repository-proxy-options "mention")
* [#cloud-reporter-proxy-environment-variables](hybrid-gateway-proxy-configuration.md#cloud-reporter-proxy-environment-variables "mention")
* [#using-kubernetes-secrets](hybrid-gateway-proxy-configuration.md#using-kubernetes-secrets "mention")

### HTTP Repository Proxy Options

The following table describes the available configuration options for the HTTP repository proxy under `gateway.management.http.proxy`:&#x20;

| Parameter              | Type    | Default | Description                                   |
| ---------------------- | ------- | ------- | --------------------------------------------- |
| `proxy.enabled`        | boolean | `false` | Enable proxy for Bridge/Cloud connection      |
| `proxy.type`           | string  | `HTTP`  | Proxy protocol: `HTTP`, `SOCKS4`, or `SOCKS5` |
| `proxy.host`           | string  | -       | Proxy server hostname                         |
| `proxy.port`           | integer | -       | Proxy server port                             |
| `proxy.username`       | string  | -       | Proxy authentication username                 |
| `proxy.password`       | string  | -       | Proxy authentication password                 |
| `proxy.useSystemProxy` | boolean | `false` | Use the Gateway system proxy configuration    |

### Cloud Reporter Proxy Environment Variables

The following table describes the available environment variables for configuring the Cloud Reporter proxy:

| Variable                               | Description                                   |
| -------------------------------------- | --------------------------------------------- |
| `gravitee_cloud_client_proxy_enabled`  | Enable proxy for Cloud Reporter               |
| `gravitee_cloud_client_proxy_type`     | Proxy protocol: `HTTP`, `SOCKS4`, or `SOCKS5` |
| `gravitee_cloud_client_proxy_host`     | Proxy server hostname                         |
| `gravitee_cloud_client_proxy_port`     | Proxy server port                             |
| `gravitee_cloud_client_proxy_username` | Proxy authentication username                 |
| `gravitee_cloud_client_proxy_password` | Proxy authentication password                 |

### Using Kubernetes Secrets

Kubernetes Secrets provide encrypted storage and access control for sensitive data.

{% hint style="warning" %}
**Production Recommendation**

Always use Kubernetes Secrets for credentials in production environments.
{% endhint %}

Reference secrets in your values.yaml:

The `secret://kubernetes/` syntax allows Gravitee to resolve credentials directly from Kubernetes secrets at runtime, keeping sensitive values out of your Helm values files.

```yaml
gateway:
  # Enable Kubernetes secret provider for secret:// syntax
  secrets:
    kubernetes:
      enabled: true
  management:
    http:
      authentication:
        basic:
          username: secret://kubernetes/bridge-auth:username
          password: secret://kubernetes/bridge-auth:password
      proxy:
        username: secret://kubernetes/proxy-credentials:username
        password: secret://kubernetes/proxy-credentials:password
```

Alternatively, use `valueFrom` in environment variables. This approach injects secret values as environment variables when the pod starts, which is useful when other applications in your stack also expect credentials through environment variables.

```yaml
gateway:
  env:
    - name: gravitee_cloud_client_proxy_username
      valueFrom:
        secretKeyRef:
          name: proxy-credentials
          key: username
    - name: gravitee_cloud_client_proxy_password
      valueFrom:
        secretKeyRef:
          name: proxy-credentials
          key: password
```

## Verification

After deployment, verify the proxy configuration using the following commands:

```sh
# Check Gateway logs for proxy-related messages
kubectl logs -n gravitee-apim -l app.kubernetes.io/component=gateway | grep -i proxy

# Verify Gateway pod environment variables
kubectl get pod -n gravitee-apim -l app.kubernetes.io/component=gateway \
  -o jsonpath='{.items[0].spec.containers[0].env}' | jq '.[] | select(.name | contains("proxy"))'
```
