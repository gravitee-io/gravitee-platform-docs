---
description: Configuration guide for configure your http server.
metaLinks:
  alternates:
    - configure-your-http-server.md
---

# Configure your HTTP Server

## `gravitee.yaml` configuration

You configure the HTTP Server configuration in the following section of the `gravitee.yaml` file:

```yaml
http:
  port: 8082
  host: 0.0.0.0
  idleTimeout: 0
  tcpKeepAlive: true
  compressionSupported: false
  maxHeaderSize: 8192
  maxChunkSize: 8192
  instances: 0
  requestTimeout: 30000
  secured: false
  alpn: false
  ssl:
    clientAuth: none # Supports none, request, required
    keystore:
      path: ${gravitee.home}/security/keystore.jks
      password: secret
    truststore:
      path: ${gravitee.home}/security/truststore.jks
      password: secret
```

## **Enable HTTPS support**

You can use the gravitee.yaml file to configure HTTPS support. However, you first need to enable secure mode in `gravitee.yml` and provide a keystore. You can generate a keystore if you don't have one, or use the file path or Kubernetes location.

{% tabs %}
{% tab title="Generate a keystore" %}
Generate a keystore:

```sh
keytool -genkey \
  -alias test \
  -keyalg RSA \
  -keystore server-keystore.jks \
  -keysize 2048 \
  -validity 360 \
  -dname CN=localhost \
  -keypass secret \
  -storepass secret
```
{% endtab %}

{% tab title="File keystore" %}
Provide a path pointing to the keystore containing the certificate and the associated private key:

```yaml
http:
  # ... skipped for simplicity
  secured: true
  ssl:
    clientAuth: none # Supports none, request, required
    keystore:
      path: /path/to/keystore.jks
      password: adminadmin
    truststore:
      path:
      password:
```

{% hint style="info" %}
**Automatic watching**

As of Gravitee APIM v3.13.0, the keystore file is automatically watched for any modifications and reloaded without having to restart the Gateway server.
{% endhint %}
{% endtab %}

{% tab title="K8s secret / configmap keystore" %}
It is possible to load the keystore directly from the Kubernetes secret or configmap by specifying the appropriate Kubernetes location in the `gravitee.yaml` file:

```yaml
http:
  # ... skipped for simplicity
  secured: true
  ssl:
    clientAuth: none # Supports none, request, required
    keystore:
      type: pkcs12
      kubernetes: /my-namespace/secrets/my-secret/keystore
      password: adminadmin
```

The expected `http.ssl.keystore.kubernetes` is structured as follows: `/{namespace}/{type}/{name}/{key}` with:

* `namespace`: the name of the targeted Kubernetes namespace
* `type`: can be either `secrets` or `configmaps`, depending on the type of Kubernetes resources being retrieved
* `name`: the name of the secret or configmap to retrieve
* `key`: the name of the key holding the value to retrieve. The `key` is optional when using a standard `kubernetes.io/tls` secret (note: it only supports PEM cert & key). The `key` is mandatory for any `Opaque` secret or configmap (note: they only support JKS & PKC12 keystore type).

The keystore (or PEM cert & key) stored in the Kubernetes secret or configmap is automatically watched for any modifications and reloaded without having to restart the Gateway server.
{% endtab %}
{% endtabs %}

## **Enable HTTP/2 support**

First, enable HTTPS support as described in the section above.

You then need to enable `alpn` in `gravitee.yaml`:

```yaml
http:
  alpn: true
  ...
```

You can now consume your API with both HTTP/1 and HTTP/2 protocols:

```sh
curl -k -v --http2 https://localhost:8082/my_api
```

## **Enable WebSocket support**

To enable WebSocket support, update the `gravitee.yaml` file:

```yaml
http:
  websocket:
    enabled: true
```

You can now consume your API via both WS and WSS protocols:

```sh
curl ws://localhost:8082/my_websocket
```

## Enable certificate-based client authentication

```yaml
http:
  ssl:
    clientAuth: none # Supports none, request, required
    truststore:
      path: /path/to/truststore.jks
      password: adminadmin
```

Available modes for `clientAuth` are:

* None: Client authentication is disabled (replacement of the `false` value)
* Request: Client authentication is not required but can be if using SSL enforcement policy
* Requires: Client authentication is required (replacement of `true` value)

## Multi-server support

The Gravitee APIM Gateway currently supports a multi-server architecture which allows one Gateway to support multiple protocols. For example, the Gateway can now proxy both HTTP and HTTPS requests by running two servers on different ports simultaneously.

To enable this feature, you must use an alternate configuration in the `gravitee.yaml` file:

* The root-level `http` configuration property should be replaced with the root-level `servers` property. The `servers` property allows for an array of servers in the configuration file.
* An `id` property has been added to identify and compare servers.
* The `type` property is now mandatory and at the moment, only supports a value of `http`.

{% hint style="info" %}
Gravitee still fully supports all configurations using `http` as the root-level property.
{% endhint %}

The rest of the configuration schema remains unchanged. Here is an example of a configuration that allows one Gateway to support `HTTP` and `HTTPS`:

{% code title="gravitee.yaml" %}
```yaml
# Gateway servers
servers:
  - id: "http"
    type: http
    port: 8092
  - id: "http_secured"
    type: http
    port: 8443
    secured: true
    alpn: true
    ssl:
      keystore:
        type: jks
        path: ${gravitee.home}/security/keystore.jks
      sni: true
      openssl: true
```
{% endcode %}
