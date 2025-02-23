# Logging

## Overview

This article describes logging at both the Gateway and API level and how to expose metrics to Prometheus.

* [Gateway-level logging](logging.md#gateway-level-logging)
* [API-level logging](logging.md#api-level-logging)
* [Expose metrics to Prometheus](logging.md#expose-metrics-to-prometheus)

## Gateway-level logging

This section describes the Gateway logging capabilities that are applied to all v4 Gateway APIs by default.

### Configure logging

To configure runtime logging for your v4 Gateway APIs:

1. Open your API Management Console
2. Go to **Settings** in the left sidebar
3. Click on **API logging** in the inner left sidebar

<figure><img src="../../../.gitbook/assets/2023-06-28_10-39-47 (1).gif" alt=""><figcaption></figcaption></figure>

You can choose to enable:

* Auditing API Logging consultation
* End user information displayed as part of API logging (this is useful if you are using an OAuth2 or JWT plan)
* Generation of API logging as audit events (API\_LOGGING\_ENABLED, API\_LOGGING\_DISABLED, API\_LOGGING\_UPDATED)

You can also define the maximum duration (in ms) of logging mode activation by entering a numeric value in the **Maximum duration** text field.

## API-level logging

The following sections describe the logging capabilities for v4 message APIs.

{% hint style="info" %}
Runtime logs are not yet available for v4 proxy APIs.&#x20;
{% endhint %}

### View record of logs

Comprehensive connection logs allow you to analyze the usage of your v4 message APIs. To view the runtime logs associated with calls to your API:

1. Open your API Management Console
2. Go to **APIs** in the left sidebar
3. Select your API
4. Click on **Runtime Logs** in the inner left sidebar

Logs will be displayed under the Runtime Logs tab in reverse chronological order:

<figure><img src="../../../.gitbook/assets/runtime logs chron order.png" alt=""><figcaption><p>History of up-to-date runtime logs</p></figcaption></figure>

The record of logs will be paginated, with no limit to the number of pages. If logging is disabled, existing logs will still be displayed, but a banner will indicate that the record is not current:

<figure><img src="../../../.gitbook/assets/runtime logs not current.png" alt=""><figcaption><p>History of existing runtime logs</p></figcaption></figure>

### Modify logging information

{% hint style="info" %}
Select logging options judiciously to optimize the value of recorded data against the potential for impact to API performance.
{% endhint %}

To record additional data, modify the **Runtime Logs** settings under the **Settings** tab:

<figure><img src="../../../.gitbook/assets/runtime logs settings.png" alt=""><figcaption><p>Runtime logs settings</p></figcaption></figure>

The **Settings** page allows you to define the following:

* **Logging mode:** Select from **Entrypoint** and **Endpoint** to customize which modes are logged.
* **Logging phase:** Select from **Request** and **Response** to customize which phases are logged.
* **Content data:** Select from **Message content**, **Message headers**, **Message metadata** and **Headers** to customize which data is logged.
* **Message sampling:** Select an option to customize the sampling configuration.
  * **Probabilistic:** Messages are sampled based on a specified probability value between 0.01 and 0.5.
  * **Count:** One message is sampled for every number specified, where the specified value must be greater than 10.
  * **Temporal:** Messages are sampled based on a specified time duration value that conforms to ISO-8601 format.
* **Display conditions:** You have the ability to filter the message data based on **Request phase condition** and **Message condition**. Each of these fields supports the use of [Gravitee Expression Language](../../../guides/gravitee-expression-language.md).

### View messages

To view the details of any entry in the list of runtime logs, click on **View messages**:

<figure><img src="../../../.gitbook/assets/runtime logs view messages.png" alt=""><figcaption><p>View messages for log details</p></figcaption></figure>

The messages captured by the runtime log will be grouped by correlation ID and listed in reverse chronological order. They will also be paginated, with a button at the bottom of the page to load additional messages.

Each message record will include placeholder tabs for raw content, header and metadata. If the corresponding data was recorded, it will appear under the tab. If no data was recorded, the field will be empty.

## Expose metrics to Prometheus

The following sections detail the configurations necessary to expose metrics to Prometheus.

### Enable the metrics service

Prometheus support is activated and exposed using the component’s internal API. The metrics service can be enabled in the `gravitee.yml` configuration file:

```yaml
services:
  metrics:
    enabled: true
    prometheus:
      enabled: true
```

{% hint style="info" %}
By default, the internal component API is bound to `localhost` only and must not be invoked outside `localhost`. To widely expose the API, you may need to set the `services.core.http.host` property to the correct network interface. If you are running the application in a Docker container, set the IP to the IP address of the container. Each change requires a restart.
{% endhint %}

### Configure labels

Labels are used to provide dimensionality to a metric. For example, metrics related to a HTTP request have an `http_path` label that allows them to query timeseries for a specific path, or any other operation.

You can specify which labels to use in the configuration file:

```yaml
services:
  metrics:
    enabled: true
    labels:
      - local
      - remote
      - http_method
      - http_code
      - http_path
    prometheus:ya
      enabled: true
```

The list of available labels can be found [here](https://Vertx.io/docs/apidocs/io/Vertx/micrometer/Label.html).

{% hint style="info" %}
Enabling labels may result in a high cardinality in values, which can cause issues on the metrics backend (i.e., the Gateway) and affect performance. In general, enabling labels will not impact performance when the set of possible values is bounded.
{% endhint %}

Default values are `local`, `http_method` and `http_code`.

Vert.x 4 is used by default. We have introduced a new field in the Prometheus configuration to enable the use of Vert.x 3 label names. To use old labels, set `version` to `3.10`:

```yaml
services:
  metrics:
    prometheus:
      naming:
        version: 3.10
```

### Prometheus configuration

The following example requests Prometheus to scrape the formatted metrics available in the Gateway internal API:

```
scrape_configs:
  - job_name: 'gio-gw'
    basic_auth:
      username: admin
      password: adminadmin
    metrics_path: /_node/metrics/prometheus
    static_configs:
      - targets: ['localhost:18082']
```

#### Prometheus UI

When running Prometheus, the UI is exposed at `http://localhost:9090/graph` by default.
