---
description: Learn how to configure Cloud gateway client
hidden: true
noIndex: true
---

# Configure Cloud Gateway Client

## Overview

In a hybrid deployment, your Gateway and Management API connect to Gravitee Cloud Gateway through several endpoints. The unified `cloud.client.*` configuration in `gravitee.yml` sets the HTTP, proxy, and SSL options for all of them in one place.

The global configuration applies to the following Cloud Gateway endpoints:

<table><thead><tr><th width="220">Endpoint</th><th>Purpose</th></tr></thead><tbody><tr><td><code>/sync</code></td><td>Repository synchronization</td></tr><tr><td><code>/reports</code></td><td>Analytics and metrics reporting</td></tr><tr><td><code>/apim/integration</code></td><td>Federation agent API discovery</td></tr></tbody></table>

## Configure the Cloud Gateway client

Add the following block to your `gravitee.yml` file. All values shown are defaults except `cloud.enabled` and `cloud.token`:

```yaml
cloud:
  enabled: true
  token: ${CLOUD_TOKEN}
  client:
    http:
      idleTimeout: 60000              # Idle timeout in ms
      connectTimeout: 5000            # Connection timeout in ms
      keepAlive: true                 # Enable keep-alive
      maxConcurrentConnections: 100   # Maximum concurrent connections
      http2MultiplexingLimit: -1      # HTTP/2 streams per connection; -1 means unlimited
      version: HTTP_2                 # HTTP_1_1 or HTTP_2
      clearTextUpgrade: true          # HTTP/2 clear-text upgrade
    proxy:
      enabled: false
      type: HTTP                      # HTTP, SOCKS4, or SOCKS5
      host: localhost
      port: 3128
      username: user                  # Optional
      password: secret                # Optional
      useSystemProxy: false
    ssl:
      trustAll: false
      hostnameVerifier: true
      truststore:
        type: NONE                    # PEM, PKCS12, JKS, or NONE
        path:                         # Path to the truststore file
        content:                      # Base64-encoded content; alternative to path
        password:                     # Required for PKCS12 and JKS
        alias:                        # Optional for PKCS12 and JKS
```

## Common scenarios

Below are common use-cases based on your workflows:

### Route Cloud Gateway traffic through a corporate proxy

Set the proxy block to direct all Cloud Gateway connections through a corporate proxy:

```yaml
cloud:
  enabled: true
  token: ${CLOUD_TOKEN}
  client:
    proxy:
      enabled: true
      host: corporate-proxy.company.com
      port: 3128
      username: ${PROXY_USER}
      password: ${PROXY_PASSWORD}
```

### Configure a proxy that performs SSL interception

{% hint style="warning" %}
**Vert.x limitation with SSL-intercepting proxies**

If your corporate proxy intercepts SSL traffic (for example, Zscaler or Blue Coat), the `cloud.client.ssl.truststore.*` configuration doesn't apply because of a Vert.x limitation. Add the proxy CA certificate to the Java truststore instead.
{% endhint %}

Import the proxy CA certificate into the JVM `cacerts` truststore:

```sh
keytool -import -trustcacerts \
  -alias corporate-proxy-ca \
  -file /path/to/proxy-ca-cert.pem \
  -cacerts \
  -storepass changeit
```

### Connect to a Cloud Gateway with a custom certificate

When you connect directly to a Cloud Gateway that uses a custom or self-signed certificate without a proxy, configure the truststore.

PEM truststore:

```yaml
cloud:
  client:
    ssl:
      truststore:
        type: PEM
        path: /path/to/custom-ca.pem
```

PKCS12 or JKS truststore:

```yaml
cloud:
  client:
    ssl:
      truststore:
        type: JKS
        path: /path/to/truststore.jks
        password: ${TRUSTSTORE_PASSWORD}
```

## Override the global configuration for a specific component

The global `cloud.client.*` configuration applies to every Cloud Gateway endpoint. To use different settings for a single component, add a per-component block. The per-component block takes precedence over the global one.

### Override settings for the repository bridge

Use `management.http.*` to override settings for the `/sync` endpoint only:

```yaml
cloud:
  client:
    proxy:
      host: corporate-proxy.com
management:
  http:
    proxy:
      host: special-proxy.com
```

### Override settings for the federation agent

Use `integration.connector.ws.*` to override settings for the `/apim/integration` endpoint only:

```yaml
cloud:
  client:
    proxy:
      host: corporate-proxy.com
integration:
  connector:
    ws:
      proxy:
        host: special-proxy.com
```

## Configuration reference

Below are all the configuration references:&#x20;

### HTTP client properties

<table><thead><tr><th width="300">Property</th><th width="100">Type</th><th width="110">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>cloud.client.http.version</code></td><td>String</td><td><code>HTTP_2</code></td><td>HTTP protocol version. Accepted values: <code>HTTP_1_1</code>, <code>HTTP_2</code></td></tr><tr><td><code>cloud.client.http.idleTimeout</code></td><td>Long</td><td><code>60000</code></td><td>Idle timeout in milliseconds</td></tr><tr><td><code>cloud.client.http.connectTimeout</code></td><td>Long</td><td><code>5000</code></td><td>Connection timeout in milliseconds</td></tr><tr><td><code>cloud.client.http.keepAlive</code></td><td>Boolean</td><td><code>true</code></td><td>Enable HTTP keep-alive</td></tr><tr><td><code>cloud.client.http.maxConcurrentConnections</code></td><td>Integer</td><td><code>100</code></td><td>Maximum concurrent connections</td></tr><tr><td><code>cloud.client.http.http2MultiplexingLimit</code></td><td>Integer</td><td><code>-1</code></td><td>HTTP/2 concurrent streams per connection. <code>-1</code> means unlimited</td></tr><tr><td><code>cloud.client.http.clearTextUpgrade</code></td><td>Boolean</td><td><code>true</code></td><td>Enable HTTP/2 clear-text upgrade</td></tr></tbody></table>

### Proxy properties

<table><thead><tr><th width="300">Property</th><th width="100">Type</th><th width="110">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>cloud.client.proxy.enabled</code></td><td>Boolean</td><td><code>false</code></td><td>Enable the proxy</td></tr><tr><td><code>cloud.client.proxy.type</code></td><td>String</td><td><code>HTTP</code></td><td>Proxy type. Accepted values: <code>HTTP</code>, <code>SOCKS4</code>, <code>SOCKS5</code></td></tr><tr><td><code>cloud.client.proxy.host</code></td><td>String</td><td>-</td><td>Proxy hostname</td></tr><tr><td><code>cloud.client.proxy.port</code></td><td>Integer</td><td><code>3128</code></td><td>Proxy port</td></tr><tr><td><code>cloud.client.proxy.username</code></td><td>String</td><td>-</td><td>Proxy username. Optional</td></tr><tr><td><code>cloud.client.proxy.password</code></td><td>String</td><td>-</td><td>Proxy password. Optional</td></tr><tr><td><code>cloud.client.proxy.useSystemProxy</code></td><td>Boolean</td><td><code>false</code></td><td>Use system proxy settings</td></tr></tbody></table>

### SSL properties

<table><thead><tr><th width="320">Property</th><th width="100">Type</th><th width="110">Default</th><th>Description</th></tr></thead><tbody><tr><td><code>cloud.client.ssl.trustAll</code></td><td>Boolean</td><td><code>false</code></td><td>Trust all certificates. Not recommended for production</td></tr><tr><td><code>cloud.client.ssl.hostnameVerifier</code></td><td>Boolean</td><td><code>true</code></td><td>Enable hostname verification</td></tr><tr><td><code>cloud.client.ssl.truststore.type</code></td><td>String</td><td><code>NONE</code></td><td>Truststore type. Accepted values: <code>PEM</code>, <code>PKCS12</code>, <code>JKS</code>, <code>NONE</code></td></tr><tr><td><code>cloud.client.ssl.truststore.path</code></td><td>String</td><td>-</td><td>Path to the truststore file</td></tr><tr><td><code>cloud.client.ssl.truststore.content</code></td><td>String</td><td>-</td><td>Base64-encoded truststore content. Alternative to <code>path</code></td></tr><tr><td><code>cloud.client.ssl.truststore.password</code></td><td>String</td><td>-</td><td>Truststore password. Required for PKCS12 and JKS</td></tr><tr><td><code>cloud.client.ssl.truststore.alias</code></td><td>String</td><td>-</td><td>Certificate alias. Optional for PKCS12 and JKS</td></tr></tbody></table>

{% hint style="warning" %}
**SSL truststore and intercepting proxies**

The `cloud.client.ssl.truststore.*` configuration doesn't work with proxies that perform SSL interception. For those environments, add the proxy CA certificate to the Java truststore as described in Configure a proxy that performs SSL interception.
{% endhint %}

## Verification

To verify the Cloud Gateway client configuration is applied as expected, follow these steps:

1.  Confirm that the Gateway and Management API pods read the `cloud.client.*` settings from `gravitee.yml`:

    ```sh
    kubectl get pod -n gravitee-apim -l app.kubernetes.io/component=gateway \
      -o jsonpath='{.items[0].spec.containers[0].env}' | \
      jq '.[] | select(.name | startswith("gravitee_cloud_client"))'
    ```
2.  Check the Gateway logs for Cloud Gateway connection messages:

    ```sh
    kubectl logs -n gravitee-apim -l app.kubernetes.io/component=gateway | grep -i "cloud"
    ```
3. Confirm that traffic flows through the proxy by checking the proxy server access log for connections to the Cloud Gateway hostname.
