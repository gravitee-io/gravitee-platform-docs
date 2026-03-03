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

The keystore file is automatically watched for any modifications and reloaded without having to restart the Gateway server.
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

You then need to enable `alpn` in your Gateway configuration:

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
http:
  alpn: true
  ...
```
{% endtab %}

{% tab title="Helm values.yml" %}
```yaml
gateway:
  servers:
    - type: http
      alpn: true
      ...
```
{% endtab %}
{% endtabs %}

You can now consume your API with both HTTP/1 and HTTP/2 protocols:

```sh
curl -k -v --http2 https://localhost:8082/my_api
```

## **Enable WebSocket support**

To enable WebSocket support, you will need to update your Gateway configuration:

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
http:
  websocket:
    enabled: true
```
{% endtab %}

{% tab title="Helm values.yml" %}
```yaml
gateway:
  websocket: true
  servers:
    - type: http
      ... 
      websocket:
        enabled: true
        # subProtocols: v10.stomp, v11.stomp, v12.stomp
        # perMessageWebSocketCompressionSupported: true
        # perFrameWebSocketCompressionSupported: true
        # maxWebSocketFrameSize: 65536
        # maxWebSocketMessageSize: 262144 # 4 full frames worth of data
```
{% endtab %}
{% endtabs %}

You can now consume your API via both WS and (secure) WSS protocols:

```sh
curl ws://localhost:8082/my_websocket
curl wss://localhost:8082/my_websocket
```

## Enable certificate based client authentication <a href="#enable-certificate-based-client-authentication" id="enable-certificate-based-client-authentication"></a>

Follow these steps to enable the certificate based client authentication:&#x20;

```yaml
http:
  ssl:
    clientAuth: none # Supports none, request, required
    truststore:
      path: /path/to/truststore.jks
      password: adminadmin
```

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
http:
  ssl:
    clientAuth: none # Supports none, request, required
    truststore:
      path: /path/to/truststore.jks
      password: adminadmin
```
{% endtab %}

{% tab title="Helm values.yml" %}
<pre class="language-yaml"><code class="lang-yaml">gateway:
  servers:
    - type: http
      ... 
      ssl:
<strong>        clientAuth: none # Supports none, request, required
</strong>#        tlsProtocols: TLSv1.2, TLSv1.3
#        tlsCiphers: TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA
#        keystore:
#          type: jks # Supports jks, pem, pkcs12, self-signed
#          path: ${gravitee.home}/security/keystore.jks # A path is required if certificate's type is jks or pkcs12
#          password: changeit
#          watch: true # Watch for any updates on the keystore and reload it. Default is true.
#          # The following is for type 'pem', report to 'secrets' section for other secret-provider plugins.
#          # This method is now the preferred way for kubernetes: /namespace/secrets/my-tls-secret
#          secret: secret://kubernetes/my-tls-secret
        truststore:
          type: jks # Supports jks, pem, pkcs12, pem-folder (for the latter watch supports added/updated/removed files)
          path: ${gravitee.home}/security/truststore.jks
          password: changeit
          watch: true # Watch for any updates on the keystore and reload it. Default is true.
#        sni: false
        openssl: false # Used to rely on OpenSSL Engine instead of default JDK SSL Engine
</code></pre>
{% endtab %}
{% endtabs %}

Available modes for `clientAuth` are:

* None: Client authentication is disabled (replacement of the `false` value)
* Request: Client authentication is not required but can be if using SSL enforcement policy
* Requires: Client authentication is required (replacement of `true` value)

## Multi-server support

The Gravitee APIM Gateway currently supports a multi-server architecture which allows one Gateway to support multiple protocols. For example, the Gateway can now proxy both HTTP and HTTPS requests by running two servers on different ports simultaneously.

To enable this feature, you must use an alternate configuration in the `gravitee.yaml` file:

* The root-level `http` configuration property should be replaced with the root-level `servers` property. The `servers` property allows for an array of servers in the configuration file.
* An `id` property has been added to identify and compare servers.
* The `type` Property is now mandatory and at the moment, only supports a value of `http`.

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
