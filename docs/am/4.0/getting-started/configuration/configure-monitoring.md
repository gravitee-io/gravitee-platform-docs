# Configure Monitoring

## Overview

Gravitee offers multiple ways to monitor and check the status and availability of your Gravitee Access Management (AM) installations.

* [Internal APIs](configure-am-gateway/internal-api.md) to monitor your AM components health.
* External tools like [Prometheus](configure-monitoring.md#prometheus) to monitor, visualize and alert.
* [Audit logs](../../guides/audit-trail.md) to analyze your business activity.

## Prometheus

Prometheus is an open-source systems monitoring and alerting toolkit. Prometheus collects and stores its metrics as time series data, i.e. metrics information is stored with the timestamp at which it was recorded, alongside optional key-value pairs called labels.

{% hint style="info" %}
For more elaborate overviews of Prometheus and how to install it please visit the [official website](https://prometheus.io/).
{% endhint %}

### Enable the metrics service

You can enable the metrics service in the `gravitee.yml` configuration file. Prometheus support is activated and exposed using the internal API of the [Gateway](configure-am-gateway/internal-api.md) and [Management](configure-am-api/internal-api.md) components.

```yaml
services:
  metrics:
    enabled: true
    prometheus:
      enabled: true
```

By default, the internal API is bound to `localhost` only, so it must not be invoked outside `localhost`. If you need to expose the API more widely, you may need to set the `services.core.http.host` property to the correct network interface. If you are running the application in a Docker container, set the IP to the IP address of the container. Each change requires a restart.

### Configure labels

Labels are used to provide dimensionality to a metric. For instance, metrics related to a HTTP request have a `http_path` label, which allows them to query time series for a specific path, or any other operation on time series.

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
    prometheus:
      enabled: true
```

The list of available labels can be found here: [Label](https://vertx.io/docs/apidocs/io/vertx/micrometer/Label.html)

{% hint style="warning" %}
Enabling labels may result in a high cardinality in values, which can cause issues on the metrics backend (i.e. the gateway) and affect performance. So it must be used with care. In general, it is fine to enable labels when the set of possible values are bounded.
{% endhint %}

Default values are `local`, `http_method` and `http_code`.

{% hint style="info" %}
Starting from the version 3.10.0, Gravitee AM uses Vert.x 4 and the metrics labels have been renamed. We have introduced a new field in prometheus configuration that you can configure to use old Vert.x 3 label names. Set it to 3.10, to use old labels.
{% endhint %}

```yaml
services:
  metrics:
    prometheus:
      naming:
        version: 3.10
```

### Prometheus configuration

The following example uses the metrics provided by the [AM Gateway internal API](configure-am-gateway/internal-api.md) and the [AM Management internal API.](configure-am-api/internal-api.md)

{% hint style="info" %}
Find the complete available metrics list in the [next section.](configure-monitoring.md#available-metrics)
{% endhint %}

The default port is :

* 18092 for the AM Gateway
* 18093 for the AM Management API

Scrape Management API metrics

```yaml
scrape_configs:
  - job_name: 'gio-am-mngt'
    basic_auth:
      username: admin
      password: adminadmin
    metrics_path: /_node/metrics/prometheus
    static_configs:
      - targets: ['localhost:18093']
```

Scrape Gateway metrics

```yaml
scrape_configs:
  - job_name: 'gio-am-gw'
    basic_auth:
      username: admin
      password: adminadmin
    metrics_path: /_node/metrics/prometheus
    static_configs:
      - targets: ['localhost:18092']
```

### Available metrics

This section lists and describes available metrics specific to Access Management.

There are three types of metrics:

* **Counter**: reports a count over a specified property of an application
* **Gauge**: only reports data when observed
* **Timer**: measure latencies or frequency of events in the system

#### Access Management

This section describes metrics that are provided by the Management API and the Gateway.

| Metrics                 | Type    | Description                                                                                    |
| ----------------------- | ------- | ---------------------------------------------------------------------------------------------- |
| gio\_events\_sync       | Gauge   | Number of events to process by the synchronization servide.                                    |
| gio\_apps               | Gauge   | Number of applications managed by the Gateway                                                  |
| gio\_app\_evt\_total    | Counter | Number of events (Create, Update, Delete) regarding applications received by the Gateway       |
| gio\_domains            | Gauge   | Number of domains managed by the Gateway                                                       |
| gio\_domain\_evt\_total | Counter | Number of events (Create, Update, Delete) regarding domains received by the Gateway            |
| gio\_idps               | Gauge   | Number of identity providers managed by the Gateway                                            |
| gio\_idp\_evt\_total    | Counter | Number of events (Create, Update, Delete) regarding identity providers received by the Gateway |
| gio\_auth\_evt\_total   | Counter | Global number of events (Create, Update, Delete) received by the Gateway                       |

| Metrics                                      | Type    | Description                                                              |
| -------------------------------------------- | ------- | ------------------------------------------------------------------------ |
| http\_server\_active\_connections            | Gauge   | Number of opened connections to the HTTP Server.                         |
| http\_server\_request\_bytes\_max            | Gauge   | Size of requests in bytes                                                |
| http\_server\_request\_bytes\_sum            | Counter | Total sum of observations for http\_server\_request\_bytes\_max          |
| http\_server\_request\_bytes\_count          | Counter | Number of observations for http\_server\_request\_bytes\_max             |
| http\_server\_requests\_total                | Counter | Number of processed requests                                             |
| http\_server\_active\_requests               | Gauge   | Number of requests being processed                                       |
| http\_server\_response\_bytes\_max           | Gauge   | Size of responses in bytes                                               |
| http\_server\_response\_bytes\_sum           | Counter | Total sum of observations for http\_server\_response\_bytes\_max         |
| http\_server\_response\_bytes\_count         | Counter | Number of observations for http\_server\_response\_bytes\_max            |
| http\_server\_response\_time\_seconds\_max   | Gauge   | Response processing time                                                 |
| http\_server\_response\_time\_seconds\_sum   | Counter | Total sum of observations for http\_server\_response\_time\_seconds\_max |
| http\_server\_response\_time\_seconds\_count | Counter | Number of observations for http\_server\_response\_time\_seconds\_max    |

|   | In addition of these metrics, JVM metrics about GC, Heap and Threads are available and prefixed by `jvm_`. |
| - | ---------------------------------------------------------------------------------------------------------- |

#### Backend

AM can rely on MongoDB or a RDBMS (Postgres, MySQL, MariaDB or SQLServer) to persist data. AM will provide metrics about connection pool for this system.

**MongoDB**

| Metrics                                 | Type  | Description                                     |
| --------------------------------------- | ----- | ----------------------------------------------- |
| mongodb\_driver\_pool\_checkedout       | Gauge | Number of connections that are currently in use |
| mongodb\_driver\_pool\_size             | Gauge | Current size of the Connections Pool            |
| mongodb\_driver\_pool\_waitingqueuesize | Gauge | Size of the wait queue for a connection         |

**RDBMS**

| Metrics                         | Type  | Description                                     |
| ------------------------------- | ----- | ----------------------------------------------- |
| r2dbc\_pool\_acquiredSize       | Gauge | Number of connections that are currently in use |
| r2dbc\_pool\_allocatedSize      | Gauge | Current size of the Connections Pool            |
| r2dbc\_pool\_pendingAcquireSize | Gauge | Size of the wait queue for a connection         |
| r2dbc\_pool\_idleSize           | Gauge | Number of connections that are currently idle   |
| r2dbc\_pool\_maxAllocatedSize   | Gauge | Maximum number of allocated connections         |
