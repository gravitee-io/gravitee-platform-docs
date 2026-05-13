# Configure Gateway for OpenTelemetry Logs

## Gateway Configuration

### OpenTelemetry Service

Configure the following properties in `gravitee.yaml` to enable OpenTelemetry tracing and configure the logs export endpoint:

| Property | Description | Example |
|:---------|:------------|:--------|
| `services.opentelemetry.enabled` | Enable OpenTelemetry globally on the gateway | `true` |
| `services.opentelemetry.traces.enabled` | Enable OpenTelemetry tracing | `true` |
| `services.opentelemetry.exporter.logsEndpoint` | OTLP HTTP endpoint for log records. Must be the full URL including signal path (e.g., `/v1/logs`). Log records are always exported over HTTP/protobuf (not gRPC). | `http://localhost:3100/otlp/v1/logs` |
| `services.opentelemetry.exporter.compression` | Compression algorithm for log export | `none` |
| `services.opentelemetry.exporter.timeout` | Export timeout | `10s` |

**Environment variable equivalent:** `gravitee_services_opentelemetry_exporter_logsEndpoint=http://<loki>:3100/otlp/v1/logs`

{% hint style="warning" %}
When running the gateway inside Docker, use the container hostname (e.g., `http://loki:3100/otlp/v1/logs`), not `localhost` — `localhost` resolves to the gateway container itself.
{% endhint %}

{% hint style="info" %}
If OTel is disabled globally on the gateway, the feature has zero overhead.
{% endhint %}
