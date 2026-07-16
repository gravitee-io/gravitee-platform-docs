# Enable OpenTelemetry tracing for a Kafka API

This page explains how to enable OpenTelemetry tracing for a single Kafka native API once gateway-level tracing is in place. For the broader OpenTelemetry feature overview and the full attribute reference, see [OpenTelemetry](../../../analyze-and-monitor-apis/opentelemetry.md).

## Enable tracing for a Kafka API

To enable tracing for a Kafka native API:

1. Ensure gateway-level tracing is enabled by setting `services.opentelemetry.enabled=true` in the gateway configuration.
2. **Strongly recommended for production**: configure `services.opentelemetry.kafka.tracedApiKeys: [PRODUCE, FETCH]` to keep full visibility on the data path while dropping high-frequency housekeeping operations such as `METADATA`, `HEARTBEAT`, `FIND_COORDINATOR`, and `API_VERSIONS`. Leaving the list empty traces every Kafka protocol operation, which can produce a high volume of spans on busy APIs.
3. Navigate to the API's Reporter Settings in the management console.
4. Locate the OpenTelemetry section.
5. Enable the **Enabled** toggle to activate per-API tracing (`analytics.tracing.enabled=true`).
6. If deep debugging is required, enable the **Verbose** toggle to add per-phase, per-flow, and per-policy spans.

    {% hint style="warning" %}
    Verbose mode significantly increases trace volume on high-throughput APIs. Enable only for deep debugging.
    {% endhint %}
7. Save the configuration to begin generating spans for the API's Kafka operations.

## Manage tracing configuration

To adjust tracing behavior after initial enablement:

1. Return to the API's Reporter Settings.
2. Modify the **Enabled** or **Verbose** toggles as needed.
3. Save the configuration. Changes take effect on the next API deployment.

To disable tracing:

* Disable the **Enabled** toggle to stop all tracing for the API.
* Disable the **Verbose** toggle to reduce trace volume while leaving standard tracing active.

## Per-API tracing settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `analytics.tracing.enabled` | Per-API OpenTelemetry tracing toggle | `true` |
| `analytics.tracing.verbose` | Per-API verbose mode toggle | `false` |
| `analytics.otelLogs.enabled` | Emit request and response payloads as OpenTelemetry log records correlated to the active trace. Only effective when `analytics.enabled` and `analytics.tracing.enabled` are both `true`. | `false` |

## Limitations

The per-API tracing toggles in the UI are disabled when:

* Analytics is disabled (`analytics.enabled=false`)
* The user lacks the `api-definition-u` permission
* The API is not a V4 NATIVE API

The **Verbose** toggle is additionally disabled when `analytics.tracing.enabled=false`.
