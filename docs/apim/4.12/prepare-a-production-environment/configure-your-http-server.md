---
description: Configuration guide for configure your http server.
metaLinks:
  alternates:
    - configure-your-http-server.md
hidden: true
noIndex: true
---

# Configure your HTTP Server

## Default HTTP server configuration

Configure the Gateway HTTP server by setting the following properties. Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
Update the following section of the `gravitee.yaml` file:

```yaml
http:
  port: 8082
  host: 0.0.0.0
  idleTimeout: 0
  tcpKeepAlive: true
  compressionSupported: false
  maxHeaderSize: 8192
  maxChunkSize: 8192
  maxInitialLineLength: 4096
  instances: 0
  requestTimeout: 30000
  requestTimeoutGraceDelay: 30
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
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Gateway service:

```bash
gravitee_http_port=8082
gravitee_http_host=0.0.0.0
gravitee_http_idleTimeout=0
gravitee_http_tcpKeepAlive=true
gravitee_http_compressionSupported=false
gravitee_http_maxHeaderSize=8192
gravitee_http_maxChunkSize=8192
gravitee_http_maxInitialLineLength=4096
gravitee_http_instances=0
gravitee_http_requestTimeout=30000
gravitee_http_requestTimeoutGraceDelay=30
gravitee_http_secured=false
gravitee_http_alpn=false
gravitee_http_ssl_clientAuth=none
gravitee_http_ssl_keystore_path=/opt/graviteeio-gateway/security/keystore.jks
gravitee_http_ssl_keystore_password=secret
gravitee_http_ssl_truststore_path=/opt/graviteeio-gateway/security/truststore.jks
gravitee_http_ssl_truststore_password=secret
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Update the `gateway:` section of your `values.yaml` file. The APIM Helm chart renders these values into the Gateway `gravitee.yml` at install time:

```yaml
gateway:
  service:
    internalPort: 8082
  http:
    requestTimeout: 30000
    requestTimeoutGraceDelay: 30
    maxHeaderSize: 8192
    maxChunkSize: 8192
    maxInitialLineLength: 4096
    maxFormAttributeSize: 2048
    alpn: "true"
  ssl:
    enabled: false
    clientAuth: none # Supports none, request, required
    keystore:
      type: jks
      path: ${gravitee.home}/security/keystore.jks
      password: secret
    truststore:
      type: jks
      path: ${gravitee.home}/security/truststore.jks
      password: secret
  websocket: false
```

{% hint style="info" %}
In single-server mode the Helm chart fixes `host` to `0.0.0.0` and doesn't expose `idleTimeout`, `tcpKeepAlive`, `compressionSupported`, or `instances`. To override any of those fields, switch to the `gateway.servers[]` array described in [Multi-server support.](configure-your-http-server.md#multi-server-support)
{% endhint %}
{% endtab %}
{% endtabs %}

## Enable HTTPS support

To enable HTTPS, turn on secure mode and provide a keystore. Generate a keystore if you don't already have one, or reference an existing file path or Kubernetes location.

## Generate a keystore

Generate a keystore with `keytool`:

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

### Reference a keystore file

Point the Gateway at the keystore that contains the certificate and private key. Supported keystore types are `jks`, `pem`, `pkcs12`, and `self-signed`. For PEM keystores, use the `certificates` array form instead of `path`.

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
http:
  # ... skipped for simplicity
  secured: true
  ssl:
    clientAuth: none # Supports none, request, required
    tlsProtocols: TLSv1.2, TLSv1.3
    tlsCiphers: TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    keystore:
      type: jks # Supports jks, pem, pkcs12, self-signed
      path: /path/to/keystore.jks
      password: adminadmin
      watch: true # Reloads the keystore on filesystem changes. Default true.
      defaultAlias: # Optional. Target a specific key pair when the keystore contains more than one.
    truststore:
      type: jks # Supports jks, pem, pkcs12, pem-folder
      path:
      password:
      watch: true # Reloads the truststore on filesystem changes. Default true.
```

For a PEM keystore, use the `certificates` array instead of `path`:

```yaml
http:
  secured: true
  ssl:
    keystore:
      type: pem
      certificates:
        - cert: /path/to/mycompany.org.pem
          key: /path/to/mycompany.org.key
        - cert: /path/to/mycompany.com.pem
          key: /path/to/mycompany.com.key
      watch: true
```
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_http_secured=true
gravitee_http_ssl_clientAuth=none
gravitee_http_ssl_tlsProtocols=TLSv1.2,TLSv1.3
gravitee_http_ssl_keystore_type=jks
gravitee_http_ssl_keystore_path=/path/to/keystore.jks
gravitee_http_ssl_keystore_password=adminadmin
gravitee_http_ssl_keystore_watch=true
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  ssl:
    enabled: true
    clientAuth: none # Supports none, request, required
    keystore:
      type: jks # Supports jks, pem, pkcs12, self-signed
      path: /path/to/keystore.jks
      password: adminadmin
      watch: true
    truststore:
      type: jks # Supports jks, pem, pkcs12, pem-folder
```

The single-server `gateway.ssl.*` block renders only `keystore.{type,path,password,kubernetes,watch,secret}`, `truststore.{type,path,password}`, `clientAuth`, `crl.{path,watch}`, and `sni`. To set `tlsProtocols`, `tlsCiphers`, `defaultAlias`, `openssl`, the `certificates` array, or any per-truststore reload setting on a Helm install, switch to the `gateway.servers[]` array form described in [Multi-server support.](configure-your-http-server.md#multi-server-support)
{% endtab %}
{% endtabs %}

{% hint style="info" %}
**Automatic watching**

As of Gravitee APIM v3.13.0, the keystore file is automatically watched for any modifications and reloaded without having to restart the Gateway server.
{% endhint %}

### Load a keystore from a Kubernetes secret or configmap

Load the keystore directly from a Kubernetes secret or configmap by specifying the location. Two forms are available:

* `ssl.keystore.secret: secret://kubernetes/<secret-name>` is the preferred form. It uses the Gravitee secret-provider plugin system, which also supports other providers such as HashiCorp Vault and AWS Secrets Manager.
* `ssl.keystore.kubernetes: /<namespace>/<type>/<name>/<key>` is the legacy form, kept for backward compatibility.

{% tabs %}
{% tab title="gravitee.yaml" %}
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
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_http_secured=true
gravitee_http_ssl_clientAuth=none
gravitee_http_ssl_keystore_type=pkcs12
gravitee_http_ssl_keystore_kubernetes=/my-namespace/secrets/my-secret/keystore
gravitee_http_ssl_keystore_password=adminadmin
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  ssl:
    enabled: true
    clientAuth: none # Supports none, request, required
    keystore:
      type: pkcs12
      kubernetes: /my-namespace/secrets/my-secret/keystore
      password: adminadmin
```
{% endtab %}
{% endtabs %}

The expected `http.ssl.keystore.kubernetes` value is structured as `/{namespace}/{type}/{name}/{key}`:

* `namespace`: the name of the targeted Kubernetes namespace
* `type`: either `secrets` or `configmaps`, depending on the Kubernetes resource type
* `name`: the name of the secret or configmap to retrieve
* `key`: the name of the key holding the value to retrieve. The `key` is optional when using a standard `kubernetes.io/tls` secret (note: it only supports PEM cert & key). The `key` is mandatory for any `Opaque` secret or configmap (note: they only support JKS & PKC12 keystore type).

The keystore (or PEM cert & key) stored in the Kubernetes secret or configmap is automatically watched for any modifications and reloaded without restarting the Gateway server.

### Enable SNI and the OpenSSL engine

Enable Server Name Indication (SNI) when a single Gateway listener serves multiple certificates. SNI lets the Gateway select the correct certificate at TLS handshake time based on the hostname the client requested. Enable `openssl` to route TLS through the OpenSSL engine instead of the default JDK SSL engine.

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
http:
  secured: true
  ssl:
    sni: true
    openssl: true
```
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_http_secured=true
gravitee_http_ssl_sni=true
gravitee_http_ssl_openssl=true
```
{% endtab %}

{% tab title="Helm values.yaml" %}
The single-server `gateway.ssl.*` form supports `sni` but doesn't render `openssl`. To set `openssl` on a Helm install, use the `gateway.servers[]` array described in [Multi-server support.](configure-your-http-server.md#multi-server-support)

```yaml
gateway:
  ssl:
    enabled: true
    sni: true
```
{% endtab %}
{% endtabs %}

### HTTPS configuration reference

The following fields configure HTTPS on the Gateway HTTP server. Set them under `http:` in `gravitee.yml`, or under `gateway.ssl.*` in Helm `values.yaml` when the field is exposed by the chart's single-server form.

<table>
    <thead>
        <tr>
            <th width="240">Property</th>
            <th>Description</th>
            <th width="140">Default</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>http.secured</code></td>
            <td>Enables HTTPS on the Gateway HTTP server.</td>
            <td><code>false</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.clientAuth</code></td>
            <td>Client certificate authentication mode. Accepts <code>none</code>, <code>request</code>, or <code>required</code>.</td>
            <td><code>none</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.clientAuthHeader.name</code></td>
            <td>Header name to extract the client certificate from. Use this when NGINX or another load balancer terminates TLS in front of the Gateway.</td>
            <td>-</td>
        </tr>
        <tr>
            <td><code>http.ssl.tlsProtocols</code></td>
            <td>Comma-separated allow list of TLS protocol versions.</td>
            <td><code>TLSv1.2, TLSv1.3</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.tlsCiphers</code></td>
            <td>Comma-separated allow list of TLS cipher suites.</td>
            <td>See <code>gravitee.yml</code> template</td>
        </tr>
        <tr>
            <td><code>http.ssl.keystore.type</code></td>
            <td>Keystore type. Accepts <code>jks</code>, <code>pem</code>, <code>pkcs12</code>, or <code>self-signed</code>.</td>
            <td><code>jks</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.keystore.path</code></td>
            <td>Filesystem path to the keystore. Required when <code>type</code> is <code>jks</code> or <code>pkcs12</code>.</td>
            <td><code>${gravitee.home}/security/keystore.jks</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.keystore.password</code></td>
            <td>Keystore password.</td>
            <td><code>secret</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.keystore.certificates</code></td>
            <td>Array of <code>cert</code> and <code>key</code> file pairs. Required when <code>type</code> is <code>pem</code>.</td>
            <td>-</td>
        </tr>
        <tr>
            <td><code>http.ssl.keystore.watch</code></td>
            <td>When <code>true</code>, the Gateway watches the keystore file and reloads on changes without restarting.</td>
            <td><code>true</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.keystore.defaultAlias</code></td>
            <td>Target alias to select a specific key pair when the keystore contains more than one.</td>
            <td>-</td>
        </tr>
        <tr>
            <td><code>http.ssl.keystore.kubernetes</code></td>
            <td>Legacy Kubernetes secret or configmap location, in the form <code>/&#x3C;namespace>/&#x3C;type>/&#x3C;name>/&#x3C;key></code>.</td>
            <td>-</td>
        </tr>
        <tr>
            <td><code>http.ssl.keystore.secret</code></td>
            <td>Preferred secret-provider reference, in the form <code>secret://kubernetes/&#x3C;secret-name></code>. Supports Kubernetes, HashiCorp Vault, AWS Secrets Manager, and other configured providers.</td>
            <td>-</td>
        </tr>
        <tr>
            <td><code>http.ssl.truststore.type</code></td>
            <td>Truststore type. Accepts <code>jks</code>, <code>pem</code>, <code>pkcs12</code>, or <code>pem-folder</code>. The <code>pem-folder</code> type watches a folder for added, updated, or removed PEM files.</td>
            <td><code>jks</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.truststore.path</code></td>
            <td>Filesystem path to the truststore.</td>
            <td><code>${gravitee.home}/security/truststore.jks</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.truststore.password</code></td>
            <td>Truststore password.</td>
            <td><code>secret</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.truststore.watch</code></td>
            <td>When <code>true</code>, the Gateway watches the truststore file or folder and reloads on changes.</td>
            <td><code>true</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.sni</code></td>
            <td>Enables Server Name Indication. Set to <code>true</code> when a single Gateway listener serves multiple certificates.</td>
            <td><code>false</code></td>
        </tr>
        <tr>
            <td><code>http.ssl.openssl</code></td>
            <td>Routes TLS through the OpenSSL engine instead of the default JDK SSL engine.</td>
            <td><code>false</code></td>
        </tr>
    </tbody>
</table>

For CRL configuration, see the [CRL configuration reference](#crl-configuration-reference) below.

## Enable HTTP/2 support

First, enable HTTPS as described above. Then turn on `alpn`.

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
http:
  alpn: true
  ...
```
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_http_alpn=true
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  http:
    alpn: "true"
```
{% endtab %}
{% endtabs %}

Consume your API with both HTTP/1 and HTTP/2 protocols:

```sh
curl -k -v --http2 https://localhost:8082/my_api
```

## Enable WebSocket support

Turn on WebSocket support for the Gateway.

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
http:
  websocket:
    enabled: true
```
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_http_websocket_enabled=true
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  websocket: true
```
{% endtab %}
{% endtabs %}

Consume your API via both WS and WSS protocols:

```sh
curl ws://localhost:8082/my_websocket
```

## Enable certificate-based client authentication

Configure a truststore and set `clientAuth` to the desired mode.

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

{% tab title=".env" %}
```bash
gravitee_http_ssl_clientAuth=none
gravitee_http_ssl_truststore_path=/path/to/truststore.jks
gravitee_http_ssl_truststore_password=adminadmin
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  ssl:
    enabled: true
    clientAuth: none # Supports none, request, required
    truststore:
      type: jks
      path: /path/to/truststore.jks
      password: adminadmin
```
{% endtab %}
{% endtabs %}

Available modes for `clientAuth`:

* `none`: Client authentication is disabled (replacement of the `false` value)
* `request`: Client authentication isn't required but can be if using the SSL enforcement policy
* `required`: Client authentication is required (replacement of the `true` value)



## Reject revoked client certificates with a CRL

Starting with Gravitee APIM 4.10, the Gateway can reject mTLS connections from clients whose certificates appear on a Certificate Revocation List (CRL). When CRL checking is enabled, the Gateway evaluates each client certificate against the loaded CRLs during the TLS handshake. If the certificate is revoked, the handshake fails and the request doesn't reach plan evaluation. This applies to every mTLS flow, including [mTLS plans.](../secure-and-expose-apis/plans/mtls.md)

Point the Gateway at a single CRL file or at a folder that contains multiple CRL files. The Gateway accepts X.509 CRLs in DER or PEM format.

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
http:
  ssl:
    crl:
      path: /path/to/crl        # File or folder of CRL files
      watch: true               # Hot-reload on filesystem changes
```
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_http_ssl_crl_path=/path/to/crl
gravitee_http_ssl_crl_watch=true
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  ssl:
    crl:
      path: /path/to/crl
      watch: true
```
{% endtab %}
{% endtabs %}

### CRL configuration reference

<table><thead><tr><th width="220">Property</th><th>Description</th><th width="110">Default</th><th data-type="checkbox">Required</th></tr></thead><tbody><tr><td><code>http.ssl.crl.path</code></td><td>Path to a single CRL file or to a folder that contains one or more CRL files. Accepted formats: DER and PEM. When unset, CRL checking is disabled.</td><td>-</td><td>false</td></tr><tr><td><code>http.ssl.crl.watch</code></td><td>When <code>true</code>, the Gateway watches the CRL path and reloads CRLs on create, modify, and delete events. When <code>false</code>, CRLs are loaded once at Gateway startup.</td><td><code>true</code></td><td>false</td></tr></tbody></table>

### CRL loading behavior

* **Path unset**: CRL checking is disabled. The Gateway doesn't evaluate client certificates against any CRL.
* **Path points to a file**: the Gateway loads the file as an X.509 CRL. If the file can't be parsed, the Gateway logs the failure and proceeds with an empty CRL set.
* **Path points to a folder**: the Gateway loads every regular file inside the folder as an X.509 CRL and combines them into a single revocation set.
* **Path must exist at startup**: the Gateway doesn't start if the path doesn't resolve to an existing file or folder. Create the path before starting the Gateway.
* **Hot reload with `watch: true`**: the Gateway registers a filesystem watcher on the CRL path (or its parent directory when the path points to a single file) and reloads CRLs when a file is created, modified, or deleted.
* **Startup-only with `watch: false`**: CRLs are loaded once at Gateway startup. Restart the Gateway to pick up changes.
* **Revoked certificate rejection**: when a client presents a revoked certificate, the Gateway throws a `CertificateException` that identifies the serial number and subject, and the TLS handshake fails.

{% hint style="info" %}
CRL checking runs at the server-level TLS handshake, before the Gateway evaluates plans. Subscription certificates registered by mTLS plans go through the same trust manager, so revoked certificates are rejected before subscription matching.
{% endhint %}

### Apply CRL checking to other Gateway servers

The `ssl.crl` block is available under every server prefix. Enable CRL checking on the top-level TCP server, on the Kafka Gateway server, and on each entry of the `servers[]` array by adding the same block under the corresponding prefix.

{% code title="gravitee.yaml" %}
```yaml
tcp:
  ssl:
    crl:
      path: /path/to/crl
      watch: true

kafka:
  ssl:
    crl:
      path: /path/to/crl
      watch: true

servers:
  - id: "http_secured"
    type: http
    ssl:
      crl:
        path: /path/to/crl
        watch: true
```
{% endcode %}

## Multi-server support

The Gravitee APIM Gateway supports a multi-server architecture that lets one Gateway expose multiple protocols. For example, the Gateway can proxy both HTTP and HTTPS by running two servers on different ports simultaneously.

To enable this, replace the root-level `http` property with the root-level `servers` array. Each entry requires:

* An `id` property to identify and compare servers
* A `type` property (currently only `http` is supported)

{% hint style="info" %}
Gravitee still fully supports configurations that use `http` as the root-level property.
{% endhint %}

The rest of the configuration schema is unchanged. The following example configures one Gateway to support both HTTP and HTTPS.

{% tabs %}
{% tab title="gravitee.yaml" %}
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
{% endtab %}

{% tab title=".env" %}
Docker Compose can't express the `servers[]` array through flat environment variables. Mount a custom `gravitee.yml` into the Gateway container instead:

```yaml
services:
  gateway:
    image: graviteeio/apim-gateway:latest
    volumes:
      - ./gravitee.yml:/opt/graviteeio-gateway/config/gravitee.yml
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  servers:
    - type: http
      port: 8092
    - type: http
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
{% endtab %}
{% endtabs %}
