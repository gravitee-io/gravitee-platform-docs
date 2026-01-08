# Expose Metrics to Prometheus

## Overview

The following sections detail the configurations necessary to expose metrics to Prometheus.

## Enable the metrics service

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

## Configure labels

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

## Prometheus configuration

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
