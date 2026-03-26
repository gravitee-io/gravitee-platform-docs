---
description: Tutorial on Logging.
---

# Logging

## Introduction

This section explains how to expose metrics to Prometheus.

## Enable the metrics service

You enable the metrics service in the `gravitee.yml` configuration file. Prometheus support is activated and exposed using the component’s internal API.

```yaml
services:
  metrics:
    enabled: true
    prometheus:
      enabled: true
```

{% hint style="info" %}
By default, the internal component API is bound to `localhost` only, so it must not be invoked outside `localhost`. If you need to expose the API more widely, you may need to set the `services.core.http.host` property to the correct network interface. If you are running the application in a Docker container, set the IP to the IP address of the container. Each change requires a restart.
{% endhint %}

## Configure labels

Labels are used to provide dimensionality to a metric. For instance, metrics related to a HTTP request have a `http_path` label, which allows them to query timeseries for a specific path, or any other operation on timeseries.

You can specify which labels you want in the configuration file:

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
Enabling labels may result in a high cardinality in values, which can cause issues on the metrics backend (i.e. the gateway) and affect performance.\
So it must be used with care.\
In general, it is fine to enable labels when the set of possible values is bounded.
{% endhint %}

Default values are `local`, `http_method` and `http_code`.

Vert.x 4 is used by default. We have introduced a new field in Prometheus configuration that you can configure to use old Vert.x 3 label names. To use old labels, set it to `3.10` .

```yaml
services:
  metrics:
    prometheus:
      naming:
        version: 3.10
```

## Prometheus configuration

The following example requests Prometheus scrape the formatted metrics available in the Gateway internal API.

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

### Prometheus UI

By default when running Prometheus, the UI is exposed at `http://localhost:9090/graph`
