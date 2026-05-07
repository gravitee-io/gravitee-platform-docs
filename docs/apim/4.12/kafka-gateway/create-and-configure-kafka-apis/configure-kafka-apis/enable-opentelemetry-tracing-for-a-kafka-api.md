# Enable OpenTelemetry Tracing for a Kafka API

## Creating OpenTelemetry Tracing for a Kafka API

To enable tracing for a Kafka native API:

1. Ensure gateway-level tracing is enabled by setting `services.opentelemetry.enabled=true` in the gateway configuration.
2. Optionally configure `services.opentelemetry.kafka.tracedApiKeys` to filter traced protocol types. Recommended: `[PRODUCE, FETCH]` to reduce noise from housekeeping requests.
3. Navigate to the API's Reporter Settings in the management console.
4. Locate the OpenTelemetry section.
5. Enable the **Enabled** toggle to activate per-API tracing (`analytics.tracing.enabled=true`).
6. If deep debugging is required, enable the **Verbose** toggle to add per-phase, per-flow, and per-policy spans.

    {% hint style="warning" %}
    Verbose mode significantly increases trace volume on high-throughput APIs. Enable only for deep debugging.
    {% endhint %}
7. Save the configuration to begin generating spans for the API's Kafka operations.

## Managing Tracing Configuration

To adjust tracing behavior after initial enablement:

1. Return to the API's Reporter Settings.
2. Modify the **Enabled** or **Verbose** toggles as needed.
3. Save the configuration. Changes take effect immediately.

To disable tracing:

* Disable the **Enabled** toggle to stop all tracing for the API.
* Disable the **Verbose** toggle to reduce trace volume while leaving standard tracing active.

## End-User Configuration

### Per-API Tracing Settings

| Property | Description | Example |
|:---------|:------------|:--------|
| `analytics.tracing.enabled` | Per-API OpenTelemetry tracing toggle | `true` |
| `analytics.tracing.verbose` | Per-API verbose mode toggle | `false` |

## Restrictions

Per-API tracing toggles are disabled in the UI when:

* Analytics is disabled (`analytics.enabled=false`)
* The user lacks `api-definition-u` permission
* The API is not V4 or not NATIVE type

The **Verbose** toggle is disabled when tracing is not enabled (`tracingEnabled=false`).
