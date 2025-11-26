---
description: An overview about Logging.
---

# Logging

## Overview

This article describes logging at both the Gateway and API level and how to expose metrics to Prometheus.

* [Gateway-level logging](logging.md#gateway-level-logging)
* [API-level logging](logging.md#api-level-logging)
* [Expose metrics to Prometheus](logging.md#expose-metrics-to-prometheus)

## Gateway-level logging

This section describes the Gateway logging capabilities that are applied to all v4 Gateway APIs by default.

{% hint style="info" %}
These settings can be overridden by logging settings that are applied at the individual API level.
{% endhint %}

### Configure logging

To configure runtime logging for your v4 Gateway APIs:

1. Open your API Management Console
2. Go to **Settings** in the left sidebar
3. Click on **API logging** in the inner left sidebar

<figure><img src="../../../.gitbook/assets/global api logging settings_CROP.png" alt=""><figcaption></figcaption></figure>

Configurable settings are grouped in the following categories:

{% tabs %}
{% tab title="Duration" %}
Limit the duration of logging by entering a numeric value (ms) in the **Maximum duration** field. This avoids the prolonged capture of headers and/or body payload and excessive CPU/memory consumption.

The default value (90000 ms) logs minimal call information. A value of 0 is interpreted as no maximum duration.
{% endtab %}

{% tab title="Audit" %}
When enabled, the following options track who accessed specific data from the audit view:

* **Enable audit on API Logging consultation**
* **Generate API Logging audit events (API\_LOGGING\_ENABLED, API\_LOGGING\_DISABLED, API\_LOGGING\_UPDATED)**
{% endtab %}

{% tab title="User" %}
Toggle **Display end user on API Logging (in case of OAuth2/JWT plan)** to include information about the the end user in the API logging. This is useful when using an OAuth2 or JWT plan.
{% endtab %}

{% tab title="Message Sampling" %}
{% hint style="info" %}
Sampling is used to avoid excessive resource consumption and is only relevant to v4 message APIs.
{% endhint %}

Set the defaults and limits of the possible sampling configurations.

* **Probabilistic:** Messages are sampled based on a specified probability value between 0.01 and 0.5.
* **Count:** One message is sampled for every number specified, where the specified value must be greater than 1.
* **Temporal:** Messages are sampled based on a specified time duration value that conforms to ISO-8601 format.
{% endtab %}
{% endtabs %}

## API-level logging

The following sections describe the logging capabilities for v4 APIs.

### View record of logs

Comprehensive connection logs allow you to analyze the usage of your v4 message APIs or v4 proxy APIs. To view the runtime logs associated with calls to your API:

1. Open your API Management Console
2. Go to **APIs** in the left sidebar
3. Select your API
4. Click on **API Traffic** in the inner left sidebar

Logs are displayed under the **Runtime Logs** tab in reverse chronological order:

<figure><img src="../../../.gitbook/assets/runtime logs_list message CROP.png" alt=""><figcaption><p>Sample v4 message API runtime log entries</p></figcaption></figure>

The filters above the list of logs allow you to filter records by timeframe, HTTP method, or plan. The **More** button offers additional filtering options.

If logging is disabled, existing logs are still displayed, but a banner indicates that the record is not current.

### Modify logging information

Logging information can be modified by configuring the options under the **Settings** tab. To view and modify the logging options:

1. Open your API Management Console
2. Go to **APIs** in the left sidebar
3. Select your API
4. Click on **API Traffic** in the inner left sidebar
5. Click on the **Settings** tab

{% hint style="info" %}
Select logging options judiciously to optimize the value of recorded data against the potential for impact to API performance. Sampling is used to avoid excessive resource consumption and is only relevant to v4 message APIs.
{% endhint %}

To configure which information is recorded, select from the following options:

* **Logging mode:** Select from **Entrypoint** and **Endpoint** to customize which modes are logged.
* **Logging phase:** Select from **Request** and **Response** to customize which phases are logged.
* **Content data:** Select from **Message content**, **Message headers**, **Message metadata** and **Headers** to customize which data is logged.
* **Message sampling:** Select an option to customize the sampling configuration.
  * **Probabilistic:** Messages are sampled based on a specified probability value between 0.01 and 0.5.
  * **Count:** One message is sampled for every number specified, where the specified value must be greater than 1.
  * **Temporal:** Messages are sampled based on a specified time duration value that conforms to ISO-8601 format.
* **Display conditions:** You have the ability to filter the message data based on **Request phase condition** and **Message condition**. Each of these fields supports the use of [Gravitee Expression Language](../../../guides/gravitee-expression-language.md).

<figure><img src="../../../.gitbook/assets/runtime logs_settings message CROP.png" alt=""><figcaption><p>Runtime logs settings</p></figcaption></figure>

#### Configure sampling methods with `gravitee.yml`

{% hint style="info" %}
If a setting is configured in `gravitee.yml`, the corresponding field is disabled in the Management Console.
{% endhint %}

Sampling methods for v4 message APIs can also be configured in the `gravitee.yml` file. The `messageSampling` configuration option determines, for each sampling method, whether it can be used, its default value, and its max value:

* **Probabilistic:** Must be a `double` representing a percentage (min value 0.01, max value 0.5)
* **Count:** Must be an `integer` (min value 1)
* **Temporal:** Must be a `string` in ISO 8601 format

{% code title="gravitee.yaml" %}
```
```
{% endcode %}

\`\`\`\`yaml \`\`\` logging: messageSampling: probabilistic: default: 0.01 limit: 0.5 count: default: 100 limit: 10000 temporal: default: PT1S limit: PT1S \`\`\` \`\`\`\` \{% endcode %\} \{% endtab %\}

\{% tab title="v4 proxy APIs" %\} {% hint style="info" %} Select logging options judiciously to optimize the value of recorded data against the potential for impact to API performance. {% endhint %}

To configure which information is recorded, select from the following options:

* **Logging mode:** Select from **Entrypoint** and **Endpoint** to customize which modes are logged.
* **Logging phase:** Select from **Request** and **Response** to customize which phases are logged.
* **Content data:** Select from **Headers** and **Payload** to customize which data is logged.
* **Display conditions:** You have the ability to filter data based on **Request phase condition**. This field supports the use of [Gravitee Expression Language](../../../guides/gravitee-expression-language.md).

<figure><img src="../../../.gitbook/assets/proxy API settings_CROP.png" alt=""><figcaption><p>Runtime logs settings</p></figcaption></figure>

\{% endtab %\} \{% endtabs %\}

### View messages

To view the details of any entry in the list of runtime logs:

1. Open your API Management Console
2. Go to **APIs** in the left sidebar
3. Select your API
4. Click on **API Traffic** in the inner left sidebar
5. Click on the **Runtime Logs** tab
6. Click on **View details** for a particular entry

\{% tabs %\} \{% tab title="v4 message APIs" %\} Under the **Connection Logs** tab, logs for the entry are grouped by **Entrypoint Request**, **Endpoint Request**, **Entrypoint Response**, and **Endpoint Response**:

<figure><img src="../../../.gitbook/assets/connection details_CROP.png" alt=""><figcaption><p>View log details</p></figcaption></figure>

Under the **Messages** header, entrypoint and endpoint message details are grouped by date code:

<figure><img src="../../../.gitbook/assets/message details_CROP.png" alt=""><figcaption><p>View message details</p></figcaption></figure>

Each message record includes placeholder tabs for raw content, headers, and metadata. If the corresponding data was recorded, it will appear under the tab. If no data was recorded, the field will be empty. \{% endtab %\}

\{% tab title="v4 proxy APIs" %\} Under **Details**, logs for the entry are grouped by **Entrypoint Request**, **Endpoint Request**, **Entrypoint Response**, and **Endpoint Response**, with **Headers** and **Payload** as the content:

<figure><img src="../../../.gitbook/assets/proxy logs_CROP.png" alt=""><figcaption><p>View log details</p></figcaption></figure>

\{% endtab %\} \{% endtabs %\}

## Expose metrics to Prometheus

The following sections detail the configurations necessary to expose metrics to Prometheus.

### Enable the metrics service

Prometheus support is activated and exposed using the component’s internal API. The metrics service can be enabled in the \`

gravitee.yml\` configuration file:

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

The list of available labels can be found [here](https://vertx.io/docs/apidocs/io/vertx/micrometer/Label.html).

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

{% hint style="info" %}
When running Prometheus, the UI is exposed at `http://localhost:9090/graph` by default.
{% endhint %}
