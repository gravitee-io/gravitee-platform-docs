# Configure Reporters

## Introduction

Reporters are designed to record a variety of events occurring in the Gravitee API Management (APIM) Gateway and output them to a new source in their order of occurrence. This enables you to manage your data using a solution of your choice.

## Event types

The following event types are supported:

| Type          | Description                                                                                                                         |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `request`     | This event type provides common request and response metrics, such as response time, application, request ID, and more.             |
| `log`         | This event type provides more detailed request and response metrics. It is reported when logging has been enabled at the API level. |
| `healthcheck` | This event type allows for healthcheck events to be reported when a healthcheck endpoint has been configured and enabled on an API. |
| `node`        | This event type provides some system and JVM metrics for the node Gravitee is running on.                                           |

## Available Reporters

The following reporters are currently compatible with APIM:

<table><thead><tr><th>Type</th><th data-type="checkbox">Bundled in Distribution</th><th data-type="checkbox">Default</th></tr></thead><tbody><tr><td>Elasticsearch</td><td>true</td><td>true</td></tr><tr><td>File</td><td>true</td><td>false</td></tr><tr><td>TCP</td><td>true</td><td>false</td></tr><tr><td>Datadog</td><td>false</td><td>false</td></tr></tbody></table>

## Configuring Reporters

Elasticsearch is the default reporter, but this section will show you how to configure different reporters. If you wish to use a reporter not included in the default distribution, you must first add the reporter as a plugin. Refer to the [Plugins](../../overview/introduction-to-gravitee-api-management-apim/plugins.md) guide to learn more.

### Elasticsearch Reporter

Configuration details for the Elasticsearch reporter are available in the [Elasticsearch Repository](configure-repositories.md#elasticsearch) documentation.

### File Reporter

#### **Configuration Parameters**

| Parameter name         | Description                                                                                                               | Default value                                                      |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `enabled`              | This setting determines whether the file reporter should be started or not. The default value is `false`.                 | false                                                              |
| `fileName`             | The path events should be written to. Use the `%s-yyyy_mm_dd` pattern to create one file per event type on a daily basis. | **#{systemProperties\['gravitee.home']}/metrics/%s-yyyy\_mm\_dd}** |
| `output`               | Output file type - json, message\_pack, elasticsearch, csv.                                                               | **json**                                                           |
| `flushInterval`        | File flush interval (in ms).                                                                                              | **1000**                                                           |
| `retainDays`           | The number of days to retain files before deleting one.                                                                   | **0 (to retain forever)**                                          |
| `<EVENT_TYPE>.exclude` | Fields to exclude from the output. Available for `json` and `message_pack` outputs only.                                  | **none**                                                           |
| `<EVENT_TYPE>.include` | Fields to include in the output. Available for `json` and `message_pack` outputs and only if excludes have been defined.  | **none**                                                           |
| `<EVENT_TYPE>.rename`  | Fields to rename when writing the output. Available for `json` and `message_pack` outputs only.                           | **none**                                                           |

{% hint style="info" %}
\<EVENT\_TYPE> refers to the kind of event reported by the Gateway and can be either `request`, `log`, `node` or `healthcheck`. Fields referenced as `exclude`, `include` and `rename` items all support [jsonPath](https://github.com/json-path/JsonPath) for accessing nested elements.
{% endhint %}

#### **Example**

The configuration example below excludes all fields from the request JSON file except the `api` and `application` fields, renames the `application` field to `app`, and excludes `log`, `node`, and `healthcheck` events from being reported.

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
      exclude: *
    node:
      exclude: *
    healthcheck:
      exclude: *
```

### TCP Reporter



{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, the TCP Reporter is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)
* [Book a demo](http://127.0.0.1:5000/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

{% hint style="warning" %}
Does not yet support v4 APIs. Learn more [here](../../overview/gravitee-api-definitions-and-execution-engines/).
{% endhint %}

#### **Configuration Parameters**

| Parameter name      | Description                                                                                                                                                  | Default value |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------- |
| `enabled`           | This setting determines whether the TCP reporter should be started or not. The default value is `false`.                                                     | false         |
| `output`            | Format of the data written to the TCP socket - json, message\_pack, elasticsearch, csv.                                                                      | **json**      |
| `host`              | The TCP host where the event should be published. This can be a valid host name or an IP address.                                                            | **localhost** |
| `port`              | The TCP port used to connect to the host.                                                                                                                    | **8123**      |
| `connectTimeout`    | Maximum time allowed to establish the TCP connection in milliseconds.                                                                                        | **10000**     |
| `reconnectAttempts` | This setting determines how many times the socket should try to establish a connection in case of failure.                                                   | **10**        |
| `reconnectInterval` | Time (in milliseconds) between socket connection attempts.                                                                                                   | **500**       |
| `retryTimeout`      | If the max reconnect attempts have been reached, this setting determines how long (in milliseconds) the reporter should wait before trying to connect again. | **5000**      |

#### **Example**

The following example uses the same configuration as the previous example above, however it writes the events to a TCP socket instead of a file.

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
      exclude: *
    node:
      exclude: *
    healthcheck:
      exclude: *
```

### Datadog Reporter

{% hint style="warning" %}
**Enterprise only**

As of Gravitee 4.0, the Datadog Reporter is an Enterprise Edition capability. To learn more about Gravitee Enterprise, and what's included in various enterprise packages, please:

* [Refer to the EE vs OSS documentation](../../overview/introduction-to-gravitee-api-management-apim/ee-vs-oss.md)
* [Book a demo](http://127.0.0.1:5000/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

{% hint style="warning" %}
Does not yet support v4 APIs. Learn more [here](../../overview/gravitee-api-definitions-and-execution-engines/).
{% endhint %}

This reporter allows you to send APIM Gateway events to Datadog listening server.

#### **Datadog conversions**

In the following table, you can see how different data from Gravitee has been transformed into the Datadog format.

| Gravitee         | Datadog |
| ---------------- | ------- |
| `Monitor`        | Metrics |
| `EndpointStatus` | Events  |
| `Metrics`        | Metrics |
| `Log`            | Log     |

#### **Configuration Parameters**

| Parameter name   | Description                                                                                                                                                                                                                             | Default value |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| `enabled`        | This setting determines whether the Datadog reporter should be started or not. The default value is `false`.                                                                                                                            | false         |
| `site`           | If you don’t use the default website of Datadog, for example if the data center is in the EU, then you need to set this variable.                                                                                                       | **null**      |
| `host`           | The TCP host where the event should be published. This can be a valid host name or an IP address.                                                                                                                                       | **localhost** |
| `authentication` | In order to send data to Datadog, you need to provide your Authentication details and all supported Datadog Authentication mechanisms can be used in here as well. You need to choose only one Authentication type and remove the rest. | **N/A**       |

#### **Example**

The configuration is loaded from the common APIM Gateway configuration file, `gravitee.yml`. This will send the data to your Datadog account.

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
```
