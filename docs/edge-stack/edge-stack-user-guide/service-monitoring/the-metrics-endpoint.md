---
noIndex: true
---

# The Metrics Endpoint

> For an overview of other options for gathering statistics on Ambassador Edge Stack, see the [Statistics and Monitoring](statistics-and-monitoring.md) overview.

Each Ambassador Edge Stack pod exposes statistics and metrics for that pod at `http://{POD}:8877/metrics`. The response is in the text-based Prometheus [exposition format](https://prometheus.io/docs/instrumenting/exposition_formats/).

## Understanding the statistics

The Prometheus exposition format includes special "HELP" lines that make the file self-documenting as to what specific statistics mean.

* `envoy_*`: See the [Envoy documentation](https://www.envoyproxy.io/docs/envoy/v1.23.0/operations/admin.html#get--stats-prometheus).
* `ambassador_*`:
  * `ambassador_edge_stack_*` (not present in Emissary-ingress):
    * `ambassador_edge_stack_go_*`: See \[`promethus.NewGoCollector()`]\[].
    * `ambassador_edge_stack_promhttp_*` See [`promhttp.Handler()`](https://godoc.org/github.com/prometheus/client_golang/prometheus/promhttp#Handler).
    * `ambassador_edge_stack_process_*`: See \[`promethus.NewProcessCollector()`]\[]..
  * `ambassador_*_time_seconds` (for `*` = one of `aconf`, `diagnostics`, `econf`, `fetcher`, `ir`, or `reconfiguration`): Gauges of how long the various core operations take in the diagd process.
  * `ambassador_diagnostics_(errors|notices)`: The number of diagnostics errors and notices that would be shown in the diagnostics UI or the Edge Policy Console.
  * `ambassador_diagnostics_info`: [Info](https://prometheus.github.io/client_python/) about the Ambassador Edge Stack install; all information is presented in labels; the value of the Gauge is always "1".
  * `ambassador_process_*`: See [`prometheus_client.ProcessCollector`](https://prometheus.github.io/client_python/collector/).

## Polling the `:8877/metrics` endpoint with Prometheus

To scrape metrics directly, follow the instructions for [monitoring-with-prometheus-and-grafana.md](monitoring-with-prometheus-and-grafana.md "mention").

### Using Grafana to visualize statistics gathered by Prometheus

#### Sample dashboard

We provide a [sample Grafana dashboard](https://grafana.com/grafana/dashboards/4698-ambassador-edge-stack/) that displays information collected by Prometheus from the `:8877/metrics` endpoint.

<figure><img src="../../.gitbook/assets/00 aes 16.png" alt=""><figcaption></figcaption></figure>

## Additional Edge Stack latency metrics

Edge Stack provides some additional metrics around latency. Unlike the metrics from the above endpoint on port 8877, these metrics are collected and provided from a different component of Edge Stack. These additional metrics and the endpoint for them are opt-in. To enable them, set the environment variable `ENABLE_PLUGIN_FILTER_METRICS` to `"true"` on your Edge Stack deployment. By default, they will be available on the `/metrics` path on port `8878`. The port can be configured using the `PLUGIN_FILTER_METRICS_PORT` environment variable.
