# Reporter Settings — OpenTelemetry section (native APIs)

The Reporter Settings page of a V4 native API includes an **OpenTelemetry** section with **Enabled** and **Verbose** toggles for configuring per-API tracing.

Additionally, the Reporter Settings page provides controls for connection metrics reporting. Connection logs are generated automatically when connection metrics reporting is enabled. To enable reporting for a native API:

1. Navigate to **APIs > [Your Native API] > Settings > Reporter**.
2. Toggle **Enable connection metrics reporting** to enable connection-level metrics.
3. Save the configuration.

Connection metrics are emitted on connection open, connection close, and error events. Logs are stored in Elasticsearch or OpenSearch and become available in the Management Console and Management API within the configured retention window.

**Reporter Settings Reference**:

| Field | Description | Default |
|:------|:------------|:--------|
| Enable connection metrics reporting | Controls whether connection metrics are sent to Elasticsearch or OpenSearch | `true` (when analytics configuration is absent) |
| Enable event-metrics reporting | Controls whether message-level metrics are sent to Elasticsearch or OpenSearch | Inherited from existing analytics configuration |

For complete OpenTelemetry configuration details and the full attribute reference, see:

* [OpenTelemetry — Per-API tracing configuration for V4 native APIs](../../analyze-and-monitor-apis/opentelemetry.md#per-api-tracing-configuration-for-v4-native-apis)
* [Enable OpenTelemetry tracing for a Kafka API](../../kafka-gateway/create-and-configure-kafka-apis/configure-kafka-apis/enable-opentelemetry-tracing-for-a-kafka-api.md)
