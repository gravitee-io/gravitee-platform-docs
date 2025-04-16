# Gravitee Gateway

## Introduction

This guide will walk through how to configure your general Gravitee API Management (APIM) Gateway settings using the `gravitee.yaml` file. As described in [APIM Components](./#configuring-apim-components), you can override these settings by using system properties or environment variables.

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
**Format sensitive**

YAML (`yml`) format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

## Configure your HTTP Server

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

### **Enable HTTPS support**

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

### **Enable HTTP/2 support**

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

### **Enable WebSocket support**

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

### Enable certificate-based client authentication

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

### Multi-server support

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

## Configure services

You can update the default APIM Gateway default values. All services are enabled by default. To stop a service, you need to add the property '`enabled: false`' (you can see an example in the '`local`' service).

```yaml
services:
  # Synchronization daemon used to keep the Gateway state in sync with the configuration from the management repository
  # Be aware that, by disabling it, the Gateway will not be sync with the configuration done through Management API and Management Console
  sync:
    # Synchronization is done each 5 seconds
    cron: '*/5 * * * * *'

  # Service used to store and cache api-keys from the management repository to avoid direct repository communication
  # while serving requests.
  apikeyscache:
    delay: 10000
    unit: MILLISECONDS
    threads: 3 # Threads core size used to retrieve api-keys from repository.

  # Local registry service.
  # This registry is used to load API Definition with json format from the file system. By doing so, you do not need
  # to configure your API using the web console or the rest API (but you need to know and understand the json descriptor
  # format to make it work....)
  local:
    enabled: false
    path: ${gravitee.home}/apis # The path to API descriptors

  # Gateway monitoring service.
  # This service retrieves metrics like os / process / jvm metrics and send them to an underlying reporting service.
  monitoring:
    delay: 5000
    unit: MILLISECONDS

  # Endpoint healthcheck service.
  healthcheck:
    threads: 3 # Threads core size used to check endpoint availability
```

## Configure transaction ID and request ID headers

By default, the APIM Gateway will generate an id for each request and set it in the following headers:

* `X-Gravitee-Transaction-Id`: This header represents the identifier for the entire transaction, which typically encompasses multiple calls or requests. It allows the tracking of a series of related requests and responses that are part of a larger transaction.
* `X-Gravitee-Request-Id`: This header represents the identifier for a single call or request within the transaction. Every individual request receives a unique identifier, which allows each request to be tracked separately.

Both of these headers can be customized. You can provide your own header names:

```yaml
handlers:
  request:
    transaction:
      header: X-Custom-Transaction-Id
    request:
      header: X-Custom-Request-Id
```

Also, you can configure the APIM Gateway behavior when the backend itself sets the same headers. To do so you need to set the `overrideMode` attribute. The following values are available:

* `override`: The header set by the APIM Gateway will override the one provided by the backend
* `merge`: Both headers set by the APIM Gateway and the backend will be kept (as headers can be multivalued)
* `keep`: The header set by the backend will be kept and the one provided by the APIM Gateway discarded

Both transaction and request headers can be configured independently:

```yaml
handlers:
  request:
    transaction:
      header: X-Custom-Transaction-Id
      overrideMode: merge
    request:
      header: X-Custom-Request-Id
      overrideMode: keep
```

## Default `gravitee.yaml` config file

The following is a reference of the default configuration of APIM Gateway in your `gravitee.yml` file:

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-api-management/blob/master/gravitee-apim-gateway/gravitee-apim-gateway-standalone/gravitee-apim-gateway-standalone-distribution/src/main/resources/config/gravitee.yml" %}
