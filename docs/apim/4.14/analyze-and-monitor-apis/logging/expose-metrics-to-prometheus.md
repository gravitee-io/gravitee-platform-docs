---
description: Expose API Management 4.13 metrics to Prometheus. Follow the configuration steps needed to make the metrics available to scrape.
---

# Expose metrics to Prometheus

## Overview

The following sections detail the configurations necessary to expose metrics to Prometheus.

## Enable the metrics service

Prometheus support is activated and exposed using the component’s internal API. Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
```yaml
services:
  metrics:
    enabled: true
    prometheus:
      enabled: true
```
{% endcode %}
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Gateway service:

```bash
gravitee_services_metrics_enabled=true
gravitee_services_metrics_prometheus_enabled=true
```
{% endtab %}

{% tab title="Helm values.yaml" %}
Set the `gateway.services.metrics` block in your `values.yaml` file. The APIM Helm chart renders this block directly into the Gateway `gravitee.yml` at install time:

```yaml
gateway:
  services:
    metrics:
      enabled: true
      prometheus:
        enabled: true
        concurrencyLimit: 3
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
* By default, the internal component API is bound to `localhost` only and must not be invoked outside `localhost`. To widely expose the API, you may need to set the `services.core.http.host` property to the correct network interface.
* If you run the application in a Docker container, set the IP address to 0.0.0.0.
{% endhint %}

## Limit concurrent scrapes

The metrics endpoint serves up to three scrapes at a time and answers any further scrape with HTTP 429 until a slot is free again. A slot is freed when its scrape completes, fails, or loses its connection, and after 30 seconds at the latest, when the Gateway aborts the scrape and closes its connection. Set `services.metrics.prometheus.concurrencyLimit` to change the number of slots, and `services.metrics.prometheus.timeout` to change the wait in milliseconds.

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

## Kafka active connections

`kafka_active_connections` is a gauge reporting how many downstream connections are active per client identity: plan, application, the Kafka `client.id`, and the client library name and version the client advertises at the handshake ([KIP-511](https://cwiki.apache.org/confluence/display/KAFKA/KIP-511%3A+Collect+and+Expose+Client%27s+Name+and+Version+in+the+Brokers)).

It restores the per-client view that is otherwise lost once traffic reaches the broker aggregated behind a single upstream service account. Where the connection analytics answer *what happened*, this answers *what is connected right now*.

The metric is **opt-in** and requires the metrics service to be enabled.

{% tabs %}
{% tab title="gravitee.yaml" %}
{% code title="gravitee.yml" %}
```yaml
services:
  metrics:
    enabled: true
    prometheus:
      enabled: true
    kafka:
      activeConnections:
        enabled: true             # defaults to false
        maxClientIdCardinality: 10000
```
{% endcode %}
{% endtab %}

{% tab title=".env" %}
```bash
gravitee_services_metrics_enabled=true
gravitee_services_metrics_prometheus_enabled=true
gravitee_services_metrics_kafka_activeConnections_enabled=true
gravitee_services_metrics_kafka_activeConnections_maxClientIdCardinality=10000
```
{% endtab %}

{% tab title="Helm values.yaml" %}
```yaml
gateway:
  services:
    metrics:
      enabled: true
      prometheus:
        enabled: true
      kafka:
        activeConnections:
          enabled: true
          maxClientIdCardinality: 10000
```
{% endtab %}
{% endtabs %}

A scrape then returns one series per client identity:

```
kafka_active_connections{application="gio-apim-gateway",organization_id="DEFAULT",environment_id="DEFAULT",api_id="orders-stream",plan_id="p1",application_id="a1",client_id="orders-consumer-1",client_software_name="librdkafka",client_software_version="2.6.1"} 42
```

`application` is the Gravitee component reporting the metric, as on every other Gateway metric. The subscribing application is `application_id`.

A client that does not advertise its library — KafkaJS, or any client on an `ApiVersions` request older than v3 — is reported as `client_software_name="unknown"`, and likewise for the version. That is a value, not an absence: those connections are counted like any other.

### Cardinality

A series is **removed from the registry when its last connection closes**. The number of live series therefore follows how many connections are open at once, not how many client ids have ever been seen — which is what makes `client_id` usable as a label at all, since it is free-form text the client chooses and often carries a pod name or a UUID. A client that reconnects under a new id leaves nothing behind.

`maxClientIdCardinality` (default `10000`) caps how many distinct `client.id` values are labelled at the same time, per API. Beyond it, further client ids are reported as `client_id="other"`. The connection is still counted, so the gauge keeps summing to the true number of active connections and only loses granularity. Slots are released as connections close, so a Gateway returns to full granularity on its own — the cap is a backstop, not a budget that runs out.

The cap applies to `client_id` alone. `client_software_name` and `client_software_version` are bounded in charset and length but not in how many distinct values they may take: they come off the same unauthenticated handshake frame, so a client that puts a build hash or an instance id in its version string produces one series per value, with no bucket to collapse onto. Removal on last close still keeps the total proportional to the connections open at once rather than to every value ever seen.

A `client.id` longer than 256 characters is cut to 256, the last three being `...`. That keeps it correlatable with the client's own configuration and distinguishable from `client_id="other"`, which means the cap was reached instead.

{% hint style="info" %}
The resulting ceiling is `maxClientIdCardinality + 1`, multiplied by the plan, application and client library combinations an API sees.
{% endhint %}

### Virtual clusters

{% hint style="warning" %}
On a virtual-cluster topology the bootstrap connection is not counted: the Gateway serves it from the endpoint itself and never reaches the point where a connection is reported. Every client keeps one open for its whole life, so the gauge undercounts by one per client there.

The connection analytics documents have the same blind spot, so the two agree with each other — but neither reports the true total on those topologies.
{% endhint %}

## Elasticsearch reporter dropped documents

From APIM 4.14, `reporter_elasticsearch_dropped_documents` counts the analytics documents that the [Elasticsearch reporter](../reporters/elasticsearch-reporter.md#documents-dropped-by-the-reporter) drops instead of writing them to Elasticsearch, on every cluster flavor and index mode. Prometheus exposes it as `reporter_elasticsearch_dropped_documents_total`.

The metric requires the metrics service to be enabled. Each series appears with the first document dropped for its `reason` and `type`, so a Gateway that never dropped a document exposes no series. An absent series means that no document was dropped.

| Label | Values |
| ----- | ------ |
| `reason` | `setup`: the document was reported before the reporter setup succeeded, or after it failed.<br>`overflow`: the bulk requests waiting to be sent exceeded `reporters.elasticsearch.bulk.max_memory_size`.<br>`error`: the bulk request still failed after the last retry.<br>`rejected`: Elasticsearch rejected the document, for example because of a mapping error. |
| `type` | The report type, for example `request`, `log`, `v4-metrics`, `v4-log`, `v4-message-metrics`, `v4-message-log`, or `topic-event-metrics`. |

For example, when the reporter drops the documents reported before its setup succeeds, a scrape returns the following series:

```
reporter_elasticsearch_dropped_documents_total{application="gio-apim-gateway",instance="dev",reason="setup",type="v4-log",} 21.0
reporter_elasticsearch_dropped_documents_total{application="gio-apim-gateway",instance="dev",reason="setup",type="v4-metrics",} 21.0
```

In dashboards and alerts, add `or vector(0)` to the query, so that it returns `0` instead of no data while no document was dropped:

```
sum(rate(reporter_elasticsearch_dropped_documents_total[5m])) or vector(0)
```

The metric is exposed on the `/_node/metrics/prometheus` endpoint of the internal API, port `18082` by default, which requires the credentials set in `services.core.http.authentication`. For more information, see [Gateway internal API](../../configure-and-manage-the-platform/gravitee-gateway/gateway-internal-api.md) and [Prometheus configuration](#prometheus-configuration).

Documents lost when a Gateway stops abruptly aren't counted.

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

## Visualize metrics in Grafana

For a complete, runnable example that deploys Prometheus and Grafana with Docker Compose and imports a sample APIM dashboard, see [Monitor APIM with Prometheus and Grafana using Docker Compose](../../how-to-guides/use-case-tutorials/monitor-apim-with-prometheus-and-grafana.md).
