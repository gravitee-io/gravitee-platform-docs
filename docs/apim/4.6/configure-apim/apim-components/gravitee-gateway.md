---
description: Tutorial on gravitee gateway.
---

# Gravitee Gateway

## Introduction

This guide will walk through how to configure your general Gravitee API Management (APIM) Gateway settings using the `gravitee.yaml` file. As described in [APIM Components](./#configuring-apim-components), you can override these settings by using system properties or environment variables.

The `gravitee.yaml` file, found in `GRAVITEE_HOME/config/`, is the default way to configure APIM.

{% hint style="info" %}
**Format sensitive**

YAML (`yml`) format is sensitive to indentation. Ensure you include the correct number of spaces and use spaces instead of tabs.
{% endhint %}

With the `gravitee.yaml` file, you can configure the following:

* [HTTP Server](gravitee-gateway.md#configure-your-http-server)
* [Plugins repository](gravitee-gateway.md#configure-the-plugins-directory)
* [Management repository](gravitee-gateway.md#configure-the-management-repository)
* [Rate Limit repository](gravitee-gateway.md#configure-the-rate-limit-repository)
* [Reporters](gravitee-gateway.md#configure-reporters)
* [Services](gravitee-gateway.md#configure-services)
* [Sharding tags](gravitee-gateway.md#configure-sharding-tags)
* [Organizations and environments](gravitee-gateway.md#configure-organizations-and-environments)
* [Transaction ID and request ID headers](gravitee-gateway.md#configure-transaction-id-and-request-id-headers)

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

This section discusses how to enable support for:

* [HTTPS](gravitee-gateway.md#enable-https-support)
* [HTTP/2](gravitee-gateway.md#enable-http-2-support)
* [WebSocket](gravitee-gateway.md#enable-websocket-support)
* [Certificate-based client authentication](gravitee-gateway.md#enable-certificate-based-client-authentication)
* [Multi-server](gravitee-gateway.md#multi-server-support)

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

## Configure the plugins directory

The plugins directory can be configured via either local installation or Helm.

{% tabs %}
{% tab title="Local installation" %}
You can configure the APIM Gateway [plugins](../../getting-started/plugins/) directory with `plugins.path` configuration property:

```yaml
plugins:
  path: ${gravitee.home}/plugins
```

Users can add plugins not included in APIM's default distribution to this directory. This includes different versions of Gravitee plugins or their own [custom plugins](../../getting-started/plugins/customization.md).

{% hint style="info" %}
To understand how Gravitee handles duplicate plugins, see plugins [discovery and loading.](../../getting-started/plugins/deployment.md#discovery-and-loading)
{% endhint %}

If you do not wish to modify the default directory, Gravitee also lets you specify additional folders in an array:

```yaml
plugins:
  path:
  - ${gravitee.home}/plugins
  - ${gravitee.home}/plugins-ext 
```

In this example, bundled plugins remain in the default directory. This configuration adds an additional `plugins-ext` directory for the user to add plugins not included in APIM's default distribution.
{% endtab %}

{% tab title="Helm Chart" %}
Gravitee's Helm Chart protects the bundled plugins directory by default. This is a sample configuration of how to add additional plugins:

{% code title="value.yaml" %}
```yaml
gateway:
  additionalPlugins:
  - http://host:port/path/to/my-plugin.zip
  - http://host:port/path/to/my-gateway-plugin.zip
api:
  additionalPlugins:
  - http://host:port/path/to/my-plugin.zip
```
{% endcode %}

The property `removePlugins` has been removed from the Helm chart as it is no longer necessary. See [plugin discovery and loading](../../getting-started/plugins/deployment.md#discovery-and-loading) for more information.
{% endtab %}
{% endtabs %}

## Configure the Management repository

The Management repository is used to store global configurations such as APIs, applications and API keys. The default configuration uses MongoDB (single server). You can configure the Management repository using the `gravitee.yaml` file:

{% code overflow="wrap" %}
```yaml
management:
  type: mongodb
  mongodb:
    dbname: ${ds.mongodb.dbname}
    host: ${ds.mongodb.host}
    port: ${ds.mongodb.port}
#    username:
#    password:
#    connectionsPerHost: 0
#    connectTimeout: 500
#    maxWaitTime: 120000
#    socketTimeout: 500
#    socketKeepAlive: false
#    maxConnectionLifeTime: 0
#    maxConnectionIdleTime: 0
#    serverSelectionTimeout: 0
#    description: gravitee.io
#    heartbeatFrequency: 10000
#    minHeartbeatFrequency: 500
#    heartbeatConnectTimeout: 1000
#    heartbeatSocketTimeout: 20000
#    localThreshold: 15
#    minConnectionsPerHost: 0
#    threadsAllowedToBlockForConnectionMultiplier: 5
#    cursorFinalizerEnabled: true
## SSL settings (Available in APIM 3.10.14+, 3.15.8+, 3.16.4+, 3.17.2+, 3.18+)
#    sslEnabled:
#    keystore:
#      path:
#      type:
#      password:
#      keyPassword:
#    truststore:
#      path:
#      type:
#      password:
## Deprecated SSL settings that will be removed in 3.19.0
#    sslEnabled:
#    keystore:
#    keystorePassword:
#    keyPassword:

# Management repository: single MongoDB using URI
# For more information about MongoDB configuration using URI, please have a look to:
# - http://api.mongodb.org/java/current/com/mongodb/MongoClientURI.html
#management:
#  type: mongodb
#  mongodb:
#    uri: mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]

# Management repository: clustered MongoDB
#management:
#  type: mongodb
#  mongodb:
#    servers:
#      - host: mongo1
#        port: 27017
#      - host: mongo2
#        port: 27017
#    dbname: ${ds.mongodb.dbname}
#    connectTimeout: 500
#    socketTimeout: 250
```
{% endcode %}

## Configure the Rate Limit repository

When defining the Rate Limiting policy, the Gravitee APIM Gateway needs to store data to share with other APIM Gateway instances.

For Management repositories, you can define a custom prefix for the Rate Limit table or collection name.

Counters can be stored in MongoDB, JDBC, or Redis Standalone.

{% tabs %}
{% tab title="MongoDB" %}
To store counters in MongoDB:

```yaml
ratelimit:
  type: mongodb
  mongodb:
    uri: mongodb://${ds.mongodb.host}/${ds.mongodb.dbname}
    prefix: # collection prefix
```

If you want to use a custom prefix, you need to follow the following [instructions](../repositories/#use-a-custom-prefix).
{% endtab %}

{% tab title="JDBC" %}
To store counters in JDBC:

```yaml
ratelimit:
  type: jdbc
  jdbc:
    url: jdbc:postgresql://host:port/dbname
    password: # password
    username: # username
    prefix:   # collection prefix
```

If you want to use a custom prefix, you need to follow these [instructions](../repositories/#use-a-custom-prefix-1).
{% endtab %}

{% tab title="Redis Standalone" %}
To store counters in Redis Standalone:

```yaml
ratelimit:
  type: redis
  redis:
    host: 'redis.mycompany'
    port: 6379
    password: 'mysecretpassword'
```

Redis Sentinel and Redis SSL configuration options are presented [here](../repositories/redis.md#redis).
{% endtab %}
{% endtabs %}

## Configure reporters

You can configure various aspects of reporters, such as reporting monitoring data, request metrics, and health checks. All reporters are enabled by default. To stop a reporter, you need to add the property `enabled: false`:

```yaml
reporters:
  elasticsearch:
    endpoints:
      - http://localhost:9200
#    index: gravitee
#    bulk:
#       actions: 500           # Number of requests action before flush
#       flush_interval: 1      # Flush interval in seconds
#    security:
#       username:
#       password:
```

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

## Configure sharding tags

You can apply sharding on APIM Gateway instances either at the system property level or with `gravitee.yml`.

In this example, we are configuring deployment only for APIs tagged as `product` or `store` and of those, we are excluding APIs tagged as `international`.

```
tags: 'product,store,!international'
```

For more in-depth information on how to configure sharding tags, please refer to the [sharding tags documentation.](../../gravitee-gateway/sharding-tags.md)

## Configure organizations and environments

You can configure organizations and environments using their `hrids` on APIM Gateway instances either at the system property level or with `gravitee.yml`.

Only APIs and dictionaries belonging to the configured organizations and environments will be loaded.

If only the `organizations` configuration is set, then all environments belonging to these organizations are used. If only the `environments` configuration is set, then all environments matching the setting will be used, regardless of their organization. If both `organizations` and `environments` are set, all environments matching the setting and belonging to these organizations will be used. If none of these fields is set, then all organizations and environments are used.

In this example, we are configuring deployment only for `dev` and `integration` environments for `mycompany` organization.

```
organizations: mycompany
environments: dev,integration
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
