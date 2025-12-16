---
description: An overview about Reporters.
---

# Reporters

## Overview

Reporters are designed to record a variety of events occurring in the Gravitee API Management (APIM) Gateway and output them to a new source in their order of occurrence. This enables you to manage your data using a solution of your choice.

The following sections detail:

* [Supported event types](README.md#event-types)
* [Available reporters](README.md#available-reporters)
* [Reporter configurations](README.md#configuring-reporters)

## Event types

The following event types are supported:

<table><thead><tr><th width="214.5">Type</th><th>Description</th></tr></thead><tbody><tr><td><code>request</code></td><td>This event type provides common request and response metrics, such as response time, application, request ID, and more.</td></tr><tr><td><code>log</code></td><td>This event type provides more detailed request and response metrics. It is reported when logging has been enabled at the API level.</td></tr><tr><td><code>healthcheck</code></td><td>This event type allows for healthcheck events to be reported when a healthcheck endpoint has been configured and enabled on an API.</td></tr><tr><td><code>node</code></td><td>This event type provides some system and JVM metrics for the node Gravitee is running on.</td></tr></tbody></table>

## Available reporters

The following reporters are currently compatible with APIM:

<table><thead><tr><th width="151">Type</th><th data-type="checkbox">Bundled in Distribution</th><th data-type="checkbox">Default</th><th data-type="checkbox">Enterprise only</th></tr></thead><tbody><tr><td><a href="./#elasticsearch-reporter">Elasticsearch</a></td><td>true</td><td>true</td><td>false</td></tr><tr><td><a href="./#file-reporter">File</a></td><td>true</td><td>false</td><td>false</td></tr><tr><td><a href="./#tcp-reporter">TCP</a></td><td>true</td><td>false</td><td>true</td></tr><tr><td><a href="./#datadog-reporter">Datadog</a></td><td>false</td><td>false</td><td>true</td></tr></tbody></table>

{% hint style="warning" %}
To learn more about Gravitee Enterprise and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../../overview/gravitee-apim-enterprise-edition/README.md)
* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

## Configuring reporters

Elasticsearch is the default reporter, but this section will show you how to configure different reporters. If you wish to use a reporter not included in the default distribution, you must first add the reporter as a plugin. Refer to the [Plugins](../../../overview/plugins.md) guide to learn more.

### Elasticsearch reporter

Configuration details for the Elasticsearch reporter are available in the [Elasticsearch Repository](../repositories/elasticsearch.md#elasticsearch) documentation.

### File reporter

{% tabs %}
{% tab title="Configuration parameters" %}
The file reporter has the following configuration parameters:

<table><thead><tr><th width="181">Parameter name</th><th width="235">Description</th><th>Default value</th></tr></thead><tbody><tr><td><code>enabled</code></td><td>This setting determines whether the file reporter should be started or not. The default value is <code>false</code>.</td><td>false</td></tr><tr><td><code>fileName</code></td><td>The path events should be written to. Use the <code>%s-yyyy_mm_dd</code> pattern to create one file per event type on a daily basis.</td><td>#{systemProperties['gravitee.home']}/metrics/%s-yyyy_mm_dd}</td></tr><tr><td><code>output</code></td><td>Output file type - json, message_pack, elasticsearch, csv.</td><td>json</td></tr><tr><td><code>flushInterval</code></td><td>File flush interval (in ms).</td><td>1000</td></tr><tr><td><code>retainDays</code></td><td>The number of days to retain files before deleting one.</td><td>0 (to retain forever)</td></tr><tr><td><code>&#x3C;EVENT_TYPE>.exclude</code></td><td>Fields to exclude from the output. Available for <code>json</code> and <code>message_pack</code> outputs only.</td><td>none</td></tr><tr><td><code>&#x3C;EVENT_TYPE>.include</code></td><td>Fields to include in the output. Available for <code>json</code> and <code>message_pack</code> outputs and only if excludes have been defined.</td><td>none</td></tr><tr><td><code>&#x3C;EVENT_TYPE>.rename</code></td><td>Fields to rename when writing the output. Available for <code>json</code> and <code>message_pack</code> outputs only.</td><td>none</td></tr></tbody></table>
{% endtab %}

{% tab title="Example" %}
The configuration example below excludes all fields from the request JSON file except the `api` and `application` fields, renames the `application` field to `app`, and excludes `log`, `node`, and `healthcheck` events from being reported:

```yaml
reporters:
  file:
    enabled: true
    fileName: ${gravitee.home}/metrics/%s-yyyy_mm_dd
    output: json
    request:
      exclude:
        - "*"
      include:
        - api
        - application
      rename:
        application: app
    log:
      exclude:
        - "*"
    node:
      exclude:
        - "*"
    health-check:
      exclude:
        - "*"
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
\<EVENT\_TYPE> refers to the kind of event reported by the Gateway and can be either `request`, `log`, `node` or `health-check`. Fields referenced as `exclude`, `include` and `rename` items all support [jsonPath](https://github.com/json-path/JsonPath) for accessing nested elements.
{% endhint %}

### TCP reporter

{% tabs %}
{% tab title="Configuration parameters" %}
The file reporter has the following configuration parameters:

| Parameter name            | Description                                                                                                                                                           | Default value |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `enabled`                 | This setting determines whether the TCP reporter should be started or not. The default value is `false`.                                                              | false         |
| `output`                  | Format of the data written to the TCP socket - json, message\_pack, elasticsearch, csv.                                                                               | json          |
| `host`                    | The TCP host where the event should be published. This can be a valid host name or an IP address.                                                                     | localhost     |
| `port`                    | The TCP port used to connect to the host.                                                                                                                             | 8123          |
| `connectTimeout`          | Maximum time allowed to establish the TCP connection in milliseconds.                                                                                                 | 10000         |
| `reconnectAttempts`       | This setting determines how many times the socket should try to establish a connection in case of failure.                                                            | 10            |
| `reconnectInterval`       | Time (in milliseconds) between socket connection attempts.                                                                                                            | 500           |
| `retryTimeout`            | If the max reconnect attempts have been reached, this setting determines how long (in milliseconds) the reporter should wait before trying to connect again.          | 5000          |
| `tls.enabled`             | Enable TLS                                                                                                                                                            | false         |
| `tls.verifyClient`        | If true, client certificate will be sent for mutual TLS negotiation. When enabling this, providing a key-store is required so that mutual TLS negotiation can happen. | false         |
| `tls.keystore.type`       | The type of key-store to use (either PEM, JKS or PFX)                                                                                                                 | null          |
| `tls.keystore.password`   | The password to use for the key-store (only for JKS and PFX types)                                                                                                    | null          |
| `tls.keystore.certs`      | The list of certificates used, when type is PEM                                                                                                                       | null          |
| `tls.keystore.keys`       | The list of keys used, when type is PEM                                                                                                                               | null          |
| `tls.truststore.type`     | The type of trust-store to use (either PEM, JKS or PFX)                                                                                                               | null          |
| `tls.truststore.password` | The password to use for the trust-store (only for JKS and PFX types)                                                                                                  | null          |
| `tls.keystore.certs`      | The list of certificates to trust, when type is PEM                                                                                                                   | null          |
{% endtab %}

{% tab title="Example" %}
The following example uses the same configuration as the file reporter example above, but writes the events to a TCP socket instead of a file:

```yaml
reporters:
  tcp:
    enabled: true
    host: localhost
    port: 9001
    output: json
    request:
      exclude:
        - "*"
      include:
        - api
        - application
      rename:
        application: app
    log:
      exclude:
        - "*"
    node:
      exclude:
        - "*"
    health-check:
      exclude:
        - "*"
    tls:
      enabled: true
      verifyClient: true
      keystore: 
        type: pem
        keys:
        - client.key
        certs:
        - client.crt
      truststore:
        type: pem 
        certs:
        - logstash.crt
```
{% endtab %}
{% endtabs %}

### Datadog reporter

{% tabs %}
{% tab title="Datadog conversions" %}
This reporter allows you to send APIM Gateway events to Datadog listening server.

In the following table, you can see how different data from Gravitee has been transformed into the Datadog format.

| Gravitee         | Datadog |
| ---------------- | ------- |
| `Monitor`        | Metrics |
| `EndpointStatus` | Events  |
| `Metrics`        | Metrics |
| `Log`            | Log     |
{% endtab %}

{% tab title="Configuration parameters" %}
The Datadog reporter has the following configuration parameters:

<table><thead><tr><th width="192">Parameter name</th><th width="278">Description</th><th>Default value</th></tr></thead><tbody><tr><td><code>enabled</code></td><td>This setting determines whether the Datadog reporter should be started or not. The default value is <code>false</code>.</td><td>false</td></tr><tr><td><code>site</code></td><td>If you don’t use the default website of Datadog, for example if the data center is in the EU, then you need to set this variable.</td><td>null</td></tr><tr><td><code>authentication</code></td><td>In order to send data to Datadog, you need to provide your Authentication details and all supported Datadog Authentication mechanisms can be used in here as well. You need to choose only one Authentication type and remove the rest.</td><td>N/A</td></tr></tbody></table>
{% endtab %}

{% tab title="Example" %}
The configuration is loaded from the common APIM Gateway configuration file, `gravitee.yml`. This will send the data to your Datadog account:

```yaml
reporters:
  datadog:
    enabled: true
    site: "datadoghq.eu"
    authentication:
      #apiKeyPrefix: ""
      apiKey: "YOUR_API_KEY"
      #appKey: "YOUR_APP_KEY"
      #tokenScheme: ""
      #token: "YOUR_TOKEN"
      #username: "YOUR_USERNAME"
      #password: "YOUR_PASSWORD"
    #http:
    #  proxy:
    #    type: HTTP #HTTP, SOCK4, SOCK5
    #    https:
    #      host: localhost
    #      port: 3128
    #      username: user
    #      password: secret
    #customTags: >
    #  s1.company.com:9092,
    #  s2.company.com:9092,
    #  s3.company.com:9092
    #log: # (Following mapping section is also available for other types: node, health-check, log)
    #  exclude: # Can be a wildcard (ie '*') to exclude all fields (supports json path)
    #    - clientRequest
    #    - clientResponse
    #    - proxyRequest
    #request: # (Following mapping section is also available for other types: node, health-check, log)
    #  exclude: 
    #    - apiResponseTimeMs
```
{% endtab %}
{% endtabs %}
