# Configure Gateway for OpenTelemetry Logs

## Gateway Configuration

### OpenTelemetry Service

To enable OpenTelemetry tracing and configure the logs export endpoint, configure the following properties in your `gravitee.yaml`:

| Property | Description | Example |
|:---------|:------------|:--------|
| `services.opentelemetry.enabled` | Enable OpenTelemetry globally on the Gateway | `true` |
| `services.opentelemetry.traces.enabled` | Enable OpenTelemetry tracing | `true` |
| `services.opentelemetry.exporter.logsEndpoint` | OTLP HTTP endpoint for log records. This must be the full URL including signal path, for exmaple, `/v1/logs`. Log records are always exported over HTTP/Protobuf and not gRPC. | `http://localhost:3100/otlp/v1/logs` |
| `services.opentelemetry.exporter.compression` | Compression algorithm for log export | `none` |
| `services.opentelemetry.exporter.timeout` | Export timeout | `10s` |

**Environment variable equivalent:** `gravitee_services_opentelemetry_exporter_logsEndpoint=http://<loki>:3100/otlp/v1/logs`

{% hint style="warning" %}
When you run the Gateway inside Docker, use the container hostname, for example, `http://loki:3100/otlp/v1/logs`, not `localhost` because `localhost` resolves to the Gateway container itself.
{% endhint %}

{% hint style="info" %}
If OTel is disabled globally on the Gateway, the feature has zero overhead.
{% endhint %}
