---
hidden: false
noIndex: false
description: Wire the OpenTelemetry pipeline that fills the Gamma Trace Explorer. Follow the steps to configure the Gateway exporter, the Collector, and the Management API readers.
---

# Configure OpenTelemetry tracing and logs

The Trace Explorer reads trace and log data from an OpenTelemetry pipeline that you run alongside Gravitee. Turning on tracing for an individual proxy doesn't populate it on its own. The Gateway has to export the data. An OpenTelemetry Collector has to receive it and write it to Elasticsearch. The Management API has to read from the same Elasticsearch indices. Every one of those settings is off by default, so a stock installation shows an empty Trace Explorer.

## How trace data reaches the Trace Explorer

Four components take part in the pipeline:

1. **The Gateway** emits spans over OTLP once OpenTelemetry is enabled on it. It emits captured request and response payloads as OpenTelemetry log records once the OpenTelemetry reporter is enabled.
2. **An OpenTelemetry Collector** receives both signals and writes them to Elasticsearch.
3. **Elasticsearch** stores traces and logs in separate OpenTelemetry data streams.
4. **The Management API** reads them back through two independent repository scopes, `otel-traces` and `otel-logs`.

The two scopes serve different parts of the Trace Explorer. The trace list is served by the traces reader alone. Opening a single trace fetches its spans from the traces reader, then fetches that trace's log records from the logs reader and attaches them to the matching spans. Configuring `otel-traces` gets traces on screen. Adding `otel-logs` adds span events and captured payloads inside each trace.

## Configure the Gateway to export trace data

Set the following on the Gateway.

<table>
    <thead>
        <tr>
            <th width="330">Setting</th>
            <th width="380">Description</th>
            <th>Default</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>services.opentelemetry.enabled</code></td>
            <td>Turns on OpenTelemetry on the Gateway. Nothing is exported while this is <code>false</code>.</td>
            <td><code>false</code></td>
        </tr>
        <tr>
            <td><code>services.opentelemetry.exporter.endpoint</code></td>
            <td>The OTLP endpoint the Gateway sends spans to.</td>
            <td><code>http://localhost:4317</code></td>
        </tr>
        <tr>
            <td><code>services.opentelemetry.exporter.protocol</code></td>
            <td>The transport used for spans.</td>
            <td><code>grpc</code></td>
        </tr>
        <tr>
            <td><code>services.opentelemetry.exporter.logsEndpoint</code></td>
            <td>The OTLP endpoint for log records. Set the full URL, including the signal path. The shipped default points at Loki, not at your Collector.</td>
            <td><code>http://localhost:3100/otlp/v1/logs</code></td>
        </tr>
        <tr>
            <td><code>reporters.otel.enabled</code></td>
            <td>Emits captured request and response payloads as OpenTelemetry log records.</td>
            <td><code>false</code></td>
        </tr>
    </tbody>
</table>

For Docker Compose, add the settings to the environment of the `gateway` service:

```yaml
gateway:
  environment:
    - gravitee_services_opentelemetry_enabled=true
    - gravitee_services_opentelemetry_exporter_endpoint=http://otel-collector:4317
    - gravitee_services_opentelemetry_exporter_protocol=grpc
    - gravitee_services_opentelemetry_exporter_logsEndpoint=http://otel-collector:4318/v1/logs
    - gravitee_reporters_otel_enabled=true
```

For the Helm chart, add them to your `values.yaml`:

```yaml
gateway:
  services:
    opentelemetry:
      enabled: true
      exporter:
        endpoint: http://otel-collector:4317
        protocol: grpc
        logsEndpoint: http://otel-collector:4318/v1/logs
  reporters:
    otel:
      enabled: true
```

Payload logging needs the OpenTelemetry reporter plugin on the Gateway. For the plugin prerequisite and the per-API capture behavior, see [OpenTelemetry Logs Integration Overview](https://documentation.gravitee.io/apim/analyze-and-monitor-apis/opentelemetry/opentelemetry-logs-integration-overview).

## Configure the Management API to read trace data

Point both repository scopes at the Elasticsearch cluster your Collector writes to.

<table>
    <thead>
        <tr>
            <th width="360">Setting</th>
            <th width="350">Description</th>
            <th>Default</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>repositories.otel-traces.type</code></td>
            <td>Backend for the trace reader. Set it to <code>elasticsearch</code>. While it stays <code>none</code>, trace searches return no results.</td>
            <td><code>none</code></td>
        </tr>
        <tr>
            <td><code>repositories.otel-traces.elasticsearch.endpoints</code></td>
            <td>The Elasticsearch endpoints holding the trace data stream.</td>
            <td>-</td>
        </tr>
        <tr>
            <td><code>repositories.otel-traces.elasticsearch.index</code></td>
            <td>The index or data stream template to read traces from.</td>
            <td>-</td>
        </tr>
        <tr>
            <td><code>repositories.otel-logs.type</code></td>
            <td>Backend for the log reader. Set it to <code>elasticsearch</code>. While it stays <code>none</code>, traces open without span events or payloads.</td>
            <td><code>none</code></td>
        </tr>
        <tr>
            <td><code>repositories.otel-logs.elasticsearch.endpoints</code></td>
            <td>The Elasticsearch endpoints holding the log data stream.</td>
            <td>-</td>
        </tr>
        <tr>
            <td><code>repositories.otel-logs.elasticsearch.index</code></td>
            <td>The index or data stream template to read log records from.</td>
            <td>-</td>
        </tr>
    </tbody>
</table>

Both index templates follow the OpenTelemetry data stream shape `<type>-<dataset>.otel-<namespace>`. The `<type>` half is fixed by the signal, so it's `traces` for one scope and `logs` for the other, and the `.otel-` separator is part of the OpenTelemetry naming convention. The dataset and namespace halves are yours to choose. The `{orgId}` and `{envId}` placeholders are substituted at query time, which gives each organization or environment its own data stream. Whatever you set here has to match what the Collector writes.

{% hint style="warning" %}
**Environment variables drop the hyphen**

The configuration keys are `repositories.otel-traces` and `repositories.otel-logs`. As environment variables, write them without the hyphen, as `gravitee_repositories_oteltraces_*` and `gravitee_repositories_otellogs_*`. Gravitee resolves the hyphen-free spelling back to the hyphenated key.
{% endhint %}

For Docker Compose, add the settings to the environment of the `management_api` service:

```yaml
management_api:
  environment:
    - gravitee_repositories_oteltraces_type=elasticsearch
    - gravitee_repositories_oteltraces_elasticsearch_endpoints_0=http://elasticsearch:9200
    - gravitee_repositories_oteltraces_elasticsearch_index=traces-gamma.otel-local
    - gravitee_repositories_otellogs_type=elasticsearch
    - gravitee_repositories_otellogs_elasticsearch_endpoints_0=http://elasticsearch:9200
    - gravitee_repositories_otellogs_elasticsearch_index=logs-gamma.otel-local
```

For the Helm chart, add them to your `values.yaml`:

```yaml
api:
  otelTraces:
    type: elasticsearch
    elasticsearch:
      endpoints:
        - http://elasticsearch:9200
      index: traces-apim.otel-{orgId}
  otelLogs:
    type: elasticsearch
    elasticsearch:
      endpoints:
        - http://elasticsearch:9200
      index: logs-apim.otel-{orgId}
```

## Add an OpenTelemetry Collector

The Collector isn't a Gravitee component. Run any OpenTelemetry Collector distribution that meets the following requirements:

* It accepts OTLP on the endpoints you configured on the Gateway. The example above uses gRPC on port `4317` for spans and HTTP on port `4318` for log records.
* It carries both a `traces` pipeline and a `logs` pipeline, so that both signals are written.
* It exports to the same Elasticsearch cluster the Management API reads, using index names that match the two reader templates.

For receiver, exporter, and pipeline syntax, see the [OpenTelemetry Collector documentation](https://opentelemetry.io/docs/collector/configuration/).

For Docker Compose, add the Collector as another service and mount its configuration file:

```yaml
otel-collector:
  image: <your-collector-image>
  command: ['--config=/etc/otelcol/config.yaml']
  volumes:
    - ./otel-collector-config.yaml:/etc/otelcol/config.yaml:ro
  networks: [gamma]
```

## Verification

To verify the pipeline is working as expected, follow these steps:

1. Enable tracing on one API proxy. For the steps, see [Configure logging and tracing](../api-management/build/configure-your-api-proxy/configure-logging-and-tracing.md).
2. Send a request through the Gateway to that proxy.
3. Open the Trace Explorer for the same proxy. For the steps, see [View API logs](../api-management/observe/view-api-logs.md).
4.  Confirm the request appears as a trace.

    <!-- TODO: Screenshot of the Gamma Trace Explorer listing a trace for a proxy after the pipeline is wired -->

    <figure><img src="../.gitbook/assets/PLACEHOLDER-gamma-trace-explorer-populated.png" alt=""><figcaption><p>The Trace Explorer listing a trace once the pipeline is wired</p></figcaption></figure>

{% hint style="info" %}
**The Trace Explorer is still empty**

Check each hop in turn. Confirm that OpenTelemetry is enabled on the Gateway and that its exporter endpoint resolves to the Collector. Confirm that the Collector is receiving the spans, which you can surface by adding a debug exporter to its pipelines. Confirm that documents landed in Elasticsearch under the index names you configured. Confirm that both repository scopes are set to `elasticsearch` and read those same index names. For the debug exporter, see the [OpenTelemetry Collector documentation](https://opentelemetry.io/docs/collector/configuration/).
{% endhint %}

## Next steps

* [View API logs](../api-management/observe/view-api-logs.md). Inspect request logs and traces for an API proxy.
* [Inspect your agent log](../agent-management/observe/inspect-your-agent-log.md). Trace agent invocations through the AI Gateway.
