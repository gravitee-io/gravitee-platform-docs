---
description: An overview about logging.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/analyze-and-monitor-apis/logging
---

# Logging

## Overview

This guide explains logging at both the Gateway and API levels and how to expose metrics to Prometheus.

This guide explains the following topics regarding logging:

* [#gateway-level-logging](logging.md#gateway-level-logging "mention")
* [#api-level-logging](logging.md#api-level-logging "mention")
* [#expose-metrics-to-prometheus](logging.md#expose-metrics-to-prometheus "mention")

## Gateway-level logging

This section describes the Gateway logging capabilities that are applied to all V4 Gateway APIs by default.

{% hint style="info" %}
These settings can be overridden by logging settings that are applied at the individual API level.
{% endhint %}

### Configure logging

1.  From the **Dashboard**, click **Settings**.

    <figure><img src="../.gitbook/assets/CFB0E2FD-AF9C-4175-80FF-C1F227860D8A_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  In the **Settings** menu, click **API Logging**.

    <figure><img src="../.gitbook/assets/0AA53CCF-8D03-400B-8BB2-A3081C3FDCFD_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

Configurable settings are grouped in the following categories:

{% tabs %}
{% tab title="Duration" %}
Limit the duration of logging by entering a numeric value, in ms, in the **Maximum duration** field. This avoids the prolonged capture of headers, body payload, and excessive CPU/memory consumption.

The default value is 90000 ms. This value logs minimal call information. A value of 0 is interpreted as no maximum duration.

<figure><img src="../.gitbook/assets/image (360) (1).png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Audit" %}
When enabled, the following options track who accessed specific data from the audit view:

* Enable audit on API Logging consultation
*   Generate API Logging audit events (API\_LOGGING\_ENABLED, API\_LOGGING\_DISABLED, API\_LOGGING\_UPDATED)

    <figure><img src="../.gitbook/assets/image (361) (1).png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="User" %}
Toggle **Display end user on API Logging (in case of OAuth2/JWT plan)** to include information about the end user in the API logging. This is useful when using an OAuth2 or JWT plan.

<figure><img src="../.gitbook/assets/image (362) (1).png" alt=""><figcaption></figcaption></figure>
{% endtab %}

{% tab title="Message Sampling" %}
{% hint style="info" %}
V4-Message APIs only: Message sampling is used to avoid excessive resource consumption and is only relevant to V4-Message APIs.
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

1.  From the **Dashboard**, click **APIs**.<br>

    <figure><img src="../.gitbook/assets/DB2B50A2-4291-41F4-8BE4-87694C0FCDDC (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  Select your API that you want to view the logs for.

    <figure><img src="../.gitbook/assets/EF1F9221-58FE-470A-8192-7A9468FEF998_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3.  From the menu, click **Logs.**

    <figure><img src="../.gitbook/assets/67DC788E-B000-4F17-8547-2D34EE35FB89_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

The filters above the list of logs allow you to filter records by timeframe, HTTP method, or plan. The **More** button offers additional filtering options.

If logging is disabled, existing logs are still displayed, but a banner indicates that the record is not current.

#### Filtering API logs

You can filter API logs by the following information:

* Period. This is the time period that you want to view logs for.
* Entrypoints. This the Entrypoint that the user used to interact with the API.
* HTTP methods. This is the method the user used to interact with the API.
*   Plan. This is the plan that the user used to interact with the API.

    <figure><img src="../.gitbook/assets/image (363) (1).png" alt=""><figcaption></figcaption></figure>

### Modify logging information

You can modify logging information can be modified by configuring the options under the **Settings** tab. To view and modify the logging options:

1.  From the **Dashboard**, click **APIs**.

    <figure><img src="../.gitbook/assets/DB2B50A2-4291-41F4-8BE4-87694C0FCDDC (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  Select your API that you want to modify the logs for.

    <figure><img src="../.gitbook/assets/EF1F9221-58FE-470A-8192-7A9468FEF998_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
3.  From the menu, click **Logs.**

    <figure><img src="../.gitbook/assets/67DC788E-B000-4F17-8547-2D34EE35FB89_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
4.  Click **Configure Reporting**.

    <figure><img src="../.gitbook/assets/4BE464F6-77A8-4B28-AFDB-EC8790CA8E94_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

{% tabs %}
{% tab title="V4 message APIs" %}
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
*   **Display conditions:** You have the ability to filter the message data based on **Request phase condition** and **Message condition**. Each of these fields supports the use of [Gravitee Expression Language](../gravitee-expression-language.md).

    <figure><img src="../.gitbook/assets/image (364) (1).png" alt=""><figcaption></figcaption></figure>

**Configure sampling methods with `gravitee.yml`**

{% hint style="info" %}
If a setting is configured in `gravitee.yml`, the corresponding field is disabled in the Management Console.
{% endhint %}

Sampling methods for v4 message APIs can also be configured in the `gravitee.yml` file. The `messageSampling` configuration option determines, for each sampling method, whether it can be used, its default value, and its max value:

* **Probabilistic:** Must be a `double` representing a percentage (min value 0.01, max value 0.5)
* **Count:** Must be an `integer` (min value 1)
* **Temporal:** Must be a `string` in ISO 8601 format

{% code title="gravitee.yaml" %}
```yaml
logging: 
   messageSampling: 
      probabilistic: 
         default: 0.01 
         limit: 0.5 
      count: 
         default: 100 
         limit: 10000 
      temporal: 
         default: PT1S 
         limit: PT1S
```
{% endcode %}
{% endtab %}

{% tab title="V4 proxy APIs" %}
{% hint style="info" %}
Select logging options judiciously to optimize the value of recorded data against the potential for impact to API performance.
{% endhint %}

* To configure which information is recorded, select from the following options:
* **Logging mode:** Select from **Entrypoint** and **Endpoint** to customize which modes are logged.
* **Logging phase:** Select from **Request** and **Response** to customize which phases are logged.
* **Content data:** Select from **Headers** and **Payload** to customize which data is logged.
*   **Display conditions:** You have the ability to filter data based on **Request phase condition**. This field supports the use of [Gravitee Expression Language](../gravitee-expression-language.md).

    <figure><img src="../.gitbook/assets/image (365) (1).png" alt=""><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

### View messages

To view the details of any entry in the list of runtime logs:

1.  From the **Dashboard**, click **APIs**.

    <figure><img src="../.gitbook/assets/7142A579-577C-48F7-BF1F-35F6229DBB88_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>
2.  Select the API that you want to view the runtime logs for.

    <figure><img src="../.gitbook/assets/image (366) (1).png" alt=""><figcaption></figcaption></figure>
3.  Click **Logs**. You are shown a list of API logs.

    <figure><img src="../.gitbook/assets/image (367) (1).png" alt=""><figcaption></figcaption></figure>
4.  Click **the eye symbol** next to the log that you want to view the details of.

    <figure><img src="../.gitbook/assets/321F6892-812F-4DAA-AEE6-0CA0C44BEFF4_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

{% tabs %}
{% tab title="V4 message APIs" %}
Under the **Connection Logs** tab, logs for the entry are grouped by **Entrypoint Request**, **Endpoint Request**, **Entrypoint Response**, and **Endpoint Response**:

<figure><img src="../.gitbook/assets/connection details_CROP (1).png" alt=""><figcaption><p>View log details</p></figcaption></figure>

Under the **Messages** header, entrypoint and endpoint message details are grouped by date code:

<figure><img src="../.gitbook/assets/message details_CROP (1).png" alt=""><figcaption><p>View message details</p></figcaption></figure>

Each message record includes placeholder tabs for raw content, headers, and metadata. If the corresponding data was recorded, it will appear under the tab. If no data was recorded, the field will be empty.
{% endtab %}

{% tab title="V4 proxy APIs" %}
In the logs screen, you see the following information about your API logs:

<figure><img src="../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

**Overview**

The overview section provides information about the Request and Response phase of the API.

<figure><img src="../.gitbook/assets/image (368) (1).png" alt=""><figcaption></figcaption></figure>

**More details**

The more detail drop-down menu shows information about the following topics:

* Application
* Plan
* Endpoint
* Gateway Host
* Gateway IP

<figure><img src="../.gitbook/assets/E28EB0D9-6405-4876-8730-BFA28645A4D5_1_201_a (1).jpeg" alt=""><figcaption></figcaption></figure>

**Details**

The details menu shows the information about the following topics:

**Request**

In the request section, you see the information about the following topics:

* **Consumer**
  * Method
  * URI
* **Gateway**
  * Method
  * URI
* **Headers**. This section lists all the headers that user or the backend sends in the request.
* **Body**
  *   Shows the body sent in the request.

      <figure><img src="../.gitbook/assets/image (369) (1) (1).png" alt=""><figcaption></figcaption></figure>

**Response**

* **Consumer**
  * Status
* **Gateway**
  * Status
* **Headers**. This section lists all the headers that is sent by the user or the backend in the response phase.
* Body
  *   Shows the body returned in the response

      <figure><img src="../.gitbook/assets/2421DA4C-35BB-4DAD-A6FA-642B70A17486_4_5005_c (1).jpeg" alt=""><figcaption></figcaption></figure>
{% endtab %}
{% endtabs %}

## Expose metrics to Prometheus

The following sections detail the configurations necessary to expose metrics to Prometheus.

### Enable the metrics service

Prometheus support is activated and exposed using the component’s internal API. The metrics service can be enabled in the `gravitee.yml` configuration file:

{% code title="gravitee.yml" %}
```yaml
services:
  metrics:
    enabled: true
    prometheus:
      enabled: true
```
{% endcode %}

{% hint style="info" %}
* By default, the internal component API is bound to `localhost` only and must not be invoked outside `localhost`. To widely expose the API, you may need to set the `services.core.http.host` property to the correct network interface.
* If you run the application in a Docker container, set the IP address to 0.0.0.0.
{% endhint %}

### Configure labels

{% hint style="warning" %}
Enabling labels may result in a high cardinality in values, which can cause issues on the metrics backend (i.e., the Gateway) and affect performance. In general, enabling labels does not impact performance when the set of possible values is bounded.
{% endhint %}

Labels are used to provide dimensionality to a metric. For example, metrics related to a HTTP request have an `http_path` label that allows them to query timeseries for a specific path, or any other operation.

You can specify which labels to use in the configuration file:

```yaml
services:
  metrics:
    enabled: true
    labels:
      - local
      - http_method
      - http_code
    prometheus:
      enabled: true
```

Default values are `local`, `http_method` and `http_code`. For a full list of labels, see [Enum Label](https://vertx.io/docs/apidocs/io/vertx/micrometer/Label.html).

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
