# Expose Metrics to Prometheus

## Overview

This guide explains how to expose the Gravitee Gateway's internal API metrics to Prometheus, and then verify that the metrics have been collected correctly.

## Prerequisites

* Administrative access to your Gateway instance to edit the `gravitee.yml` file.
* A Prometheus server with write access to your `prometheus.yml` file.
* A Kafka API. For more information about creating a Kafka API, see [create-kafka-apis.md](create-and-configure-kafka-apis/create-kafka-apis.md "mention").

## Expose metrics to Prometheus

To expose the metrics for your Kafka Gateway, complete the following steps:&#x20;

1. [#enable-prometheus](expose-metrics-to-prometheus.md#enable-prometheus "mention")
2. [#produce-or-consume-a-kafka-message](expose-metrics-to-prometheus.md#produce-or-consume-a-kafka-message "mention")
3. [#scrape-the-internal-api-for-metrics](expose-metrics-to-prometheus.md#scrape-the-internal-api-for-metrics "mention")

### Enable Prometheus&#x20;

Prometheus support is activated and exposed using the internal API.&#x20;

* To enable Prometheus, add the following configuration to your `gravitee.yml` file:

```yaml
services:
  metrics:
    enabled: true
    prometheus:
      enabled: true
```

{% hint style="info" %}
* By default, the internal component API is bound to `localhost`, so the internal API can only be invoked in `localhost`. To widely expose the API, set the `services.core.http.host` property to the correct network interface.&#x20;
* If you run the application in a Docker container, set the IP address to `0.0.0.0`.
{% endhint %}

### Produce or consume a Kafka message

For Prometheus to contain metrics to collect, you must either produce a Kafka message or consume a Kafka message. For more information about producing and consuming Kafka messages, see [#produce-or-consume-a-kafka-message](expose-metrics-to-prometheus.md#produce-or-consume-a-kafka-message "mention").

### Scrape the internal API for metrics

* To scrape the formatted Kafka Gateway metrics that are available in the Gateway internal API, use the following request:

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
By default,  the UI is exposed at `http://localhost:9090/graph`.
{% endhint %}

### Verification

When you access the `/_node/metrics/prometheus` endpoint, it displays the following metrics:

{% code lineNumbers="true" %}
```bash
# HELP net_server_active_connections Number of opened connections to the server
# TYPE net_server_active_connections gauge
net_server_active_connections{application="gio-apim-gateway",instance="dev",local="0.0.0.0:9092",} 1.0
# HELP net_client_active_connections Number of connections to the remote host currently opened
# TYPE net_client_active_connections gauge
net_client_active_connections{application="gio-apim-gateway",instance="dev",local="?",} 2.0

# HELP kafka_downstream_produce_topic_records_total Number of records produced
# TYPE kafka_downstream_produce_topic_records_total counter
kafka_downstream_produce_topic_records_total{application="gio-apim-gateway",instance="dev",} 2.0
# HELP kafka_downstream_produce_topic_record_bytes Size of produced records in bytes
# TYPE kafka_downstream_produce_topic_record_bytes summary
kafka_downstream_produce_topic_record_bytes_count{application="gio-apim-gateway",instance="dev",} 1.0
kafka_downstream_produce_topic_record_bytes_sum{application="gio-apim-gateway",instance="dev",} 82.0
# HELP kafka_downstream_produce_topic_record_bytes_max Size of produced records in bytes
# TYPE kafka_downstream_produce_topic_record_bytes_max gauge
kafka_downstream_produce_topic_record_bytes_max{application="gio-apim-gateway",instance="dev",} 82.0
# HELP kafka_upstream_produce_topic_record_bytes_max Size of produced records in bytes
# TYPE kafka_upstream_produce_topic_record_bytes_max gauge
kafka_upstream_produce_topic_record_bytes_max{application="gio-apim-gateway",instance="dev",} 82.0
# HELP kafka_upstream_produce_topic_record_bytes Size of produced records in bytes
# TYPE kafka_upstream_produce_topic_record_bytes summary
kafka_upstream_produce_topic_record_bytes_count{application="gio-apim-gateway",instance="dev",} 1.0
kafka_upstream_produce_topic_record_bytes_sum{application="gio-apim-gateway",instance="dev",} 82.0
# HELP kafka_upstream_produce_topic_records_total Number of records produced
# TYPE kafka_upstream_produce_topic_records_total counter
kafka_upstream_produce_topic_records_total{application="gio-apim-gateway",instance="dev",} 2.0
```
{% endcode %}

## Full list of metrics for your Kafka Gateway

Here is a full list of metrics for your Kafka Gateway that are viewable with Prometheus:&#x20;

| Metric                                            | What it measures                                                      |
| ------------------------------------------------- | --------------------------------------------------------------------- |
| net\_server\_active\_connections                  | Count of active Kafka connections opened by clients to the Gateway    |
| net\_client\_active\_connections                  | Count of active connections from the Gateway to the Kafka brokers     |
| kafka\_downstream\_produce\_topic\_records\_total | Total number of produced records received by the Gateway from clients |
| kafka\_downstream\_produce\_topic\_record\_bytes  | Total bytes of produced records received by the Gateway from clients  |
| kafka\_upstream\_produce\_topic\_records\_total   | Total number of produced records the Gateway sends to brokers         |
| kafka\_upstream\_produce\_topic\_record\_bytes    | Total bytes of produced records the Gateway sends to brokers          |
| kafka\_downstream\_fetch\_topic\_records\_total   | Total number of fetched records the Gateway sends to clients          |
| kafka\_downstream\_fetch\_topic\_record\_bytes    | Total bytes of fetched records the Gateway sends to clients           |
| kafka\_upstream\_fetch\_topic\_records\_total     | Total number of fetched records the Gateway receives from brokers     |
| kafka\_upstream\_fetch\_topic\_record\_bytes      | Total bytes of fetched records the Gateway receives from brokers      |
