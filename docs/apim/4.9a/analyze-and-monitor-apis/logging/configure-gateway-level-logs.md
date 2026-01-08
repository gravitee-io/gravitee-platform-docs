# Configure Gateway-level Logs

## Overview

This section describes the Gateway logging capabilities that are applied to all v4 APIs by default. To enable logging, you must configure the Gateway and define the message sampling strategy.

{% hint style="info" %}
These settings can be overridden by the logging configurations applied to individual APIs.
{% endhint %}

## Configure the Gateway

To configure the Gateway logging capabilities, complete the following steps.

1.  Log in to your APIM Console, and then click **Settings**.

    <figure><img src="../../.gitbook/assets/logging_gc.png" alt=""><figcaption></figcaption></figure>
2.  In the **Settings** menu, click **API Logging**.

    <figure><img src="../../.gitbook/assets/logging_gc1.png" alt=""><figcaption></figcaption></figure>
3.  Set the API logging capabilities and configuration values:

    * **Max Duration** of API full logging
    * **Enable audit on API Logging consultation**
    * **Generate API Logging audit events**
    * **Display end user on API Logging**
    * The default values and limits for each message sampling strategy

    <div data-gb-custom-block data-tag="hint" data-style="info" class="hint hint-info"><p>For more information on Gateway API logging configuration settings, see <a data-mention href="configure-gateway-level-logs.md#configuration-setting-details">#configuration-setting-details</a>.</p></div>

API logging capabilities and configuration settings are grouped into the following categories:

* [#duration](configure-gateway-level-logs.md#duration "mention")
* [#audit](configure-gateway-level-logs.md#audit "mention")
* [#user](configure-gateway-level-logs.md#user "mention")
* [#message-sampling-defaults-and-limits](configure-gateway-level-logs.md#message-sampling-defaults-and-limits "mention")

### Duration

Limit logging duration to avoid excessive CPU/memory consumption and the prolonged capture of headers and body payload.

The default maximum duration is 90000 ms. This value logs minimal call information. A value of 0 is interpreted as no maximum duration.

<figure><img src="../../.gitbook/assets/image (360) (1).png" alt=""><figcaption></figcaption></figure>

### Audit

Enable the following options to track who accessed specific data from the audit view:

* **Enable audit on API Logging consultation:** Records who accessed API logs.
* **Generate API Logging audit events (API\_LOGGING\_ENABLED, API\_LOGGING\_DISABLED, API\_LOGGING\_UPDATED):** Records changes to the API logging configuration.

<figure><img src="../../.gitbook/assets/image (361) (1).png" alt=""><figcaption></figcaption></figure>

### User

Enable **Display end user on API Logging (in case of OAuth2/JWT plan)** to include information about the end user in the logs. This is applicable to OAuth2 or JWT plans.

<figure><img src="../../.gitbook/assets/image (362) (1).png" alt=""><figcaption></figcaption></figure>

### Message sampling defaults and limits

{% hint style="info" %}
Message sampling is used to avoid excessive resource consumption and is only applicable to v4 message APIs.
{% endhint %}

Set the defaults and limits of the following strategies to control how messages are sampled.

*   **Probabilistic:** Messages are sampled based on a specified probability value between 0.01 and 0.5.

    * **Default probability: 0.01** - 1% of messages are sampled.
    * **Default limit: 0.5** - API publishers sampled number of messages cannot exceed 50% of the total.<br>

    <figure><img src="../../.gitbook/assets/logging-probabalistic.png" alt=""><figcaption></figcaption></figure>
*   **Count:** When the counted number of messages reaches the specified value, that message is sampled, and the count resets. For example, a value of five means that every fifth message is sampled.

    * **Default value: 100** - The 100th message is sampled for every 100 messages counted.
    * **Default limit: 10** - No less than 10 messages should be sampled.<br>

    <figure><img src="../../.gitbook/assets/logging-count.png" alt=""><figcaption></figcaption></figure>
*   **Temporal:** Messages are sampled at a specified time duration value that conforms to ISO-8601 format.&#x20;

    * **Default value: PT1S** - One message is sampled every seconds.
    * **Default limit: PT1S** - No less than one message per second can be logged.<br>

    <figure><img src="../../.gitbook/assets/logging-temporal.png" alt=""><figcaption></figcaption></figure>
*   **Windowed count:** The input value specifies the number of consecutive messages that are sampled during a sliding time window, which conforms to an ISO-8601 duration. Once the message count is reached, no new messages are logged until the window closes and a new window begins.

    * **Default value: 1/PT10S** - One message is sampled every ten seconds
    * **Default limit: 1/PT1S** - One message cannot be sampled more than once per second.<br>

    <figure><img src="../../.gitbook/assets/logging-windowed.png" alt=""><figcaption></figcaption></figure>



## Message sampling system-level defaults

Platform administrators can change the [message sampling defaults and limits](configure-gateway-level-logs.md#message-sampling-defaults-and-limits) to hard thresholds and manageable default values to support high throughput cases.

{% hint style="info" %}
Message sampling **default** and **limit** values are made read-only if your `gravitee.yaml` or Helm Chart configures these settings to have values other than their defaults.
{% endhint %}

{% tabs %}
{% tab title="gravitee.yml" %}
Update the REST API `gravitee.yml` to cement these settings:

```yaml
# Logging settings
logging:
  messageSampling:
    probabilistic:
      default: 0.01
      limit: 0.5
    count:
      default: 100
      limit: 10
    temporal:
      default: PT1S
      limit: PT1S
    windowed_count:
      default: 1/PT10S
      limit: 1/PT1S
```
{% endtab %}

{% tab title="Helm Charts" %}
Update `values.yaml` to cement these settings:

```yaml
api:
  configuration:
    logging:
      probabilistic:
        default: 0.01
        limit: 0.5
      count:
        default: 100
        limit: 10
      temporal:
        default: PT1S
        limit: PT1S
      windowed_count:
        default: 1/PT10S
```
{% endtab %}
{% endtabs %}

* **Probabilistic:** Must be a `double` < 1 representing a percentage.
* **Count:** Must be an `integer`.
* **Temporal:** Must be a `string` in ISO 8601 format.
* **Windowed count:** Must be a `string`  formatted as `COUNT/DURATION`, where `COUNT` is a positive integer and `DURATION` is string in ISO 8601 format.

## Configure the maximum logged payload size

When message content or webhook request body logging is enabled, administrators can limit the size of the record that is logged at the Gateway level.

{% tabs %}
{% tab title="gravitee.yml" %}
Update the Gateway API `gravitee.yml` file to set the maximum log size:

```yaml
reporters:
  logging:
    max_size: 4MB
```
{% endtab %}

{% tab title="Helm Charts" %}
Update `values.yaml` to set the maximum log size:

```yaml
gateway:
  reporters:
    logging:
      max_size: 4MB
```
{% endtab %}
{% endtabs %}

You can use the following convention to set the max size: `{positive integer}[unit]`.&#x20;

* `G` or `GB` for gigabytes
* `M` or `MB` for megabytes
* `K` or `KB` for kilobytes
* `B` for bytes
* No unit = `MB`&#x20;

For example: `4MB` equivalent of  `4M` or  `4096KB`.
