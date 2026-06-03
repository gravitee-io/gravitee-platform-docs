
# Reporter Settings — OpenTelemetry section (native APIs)

The Reporter Settings page of a V4 native API includes an **OpenTelemetry** section with **Enabled** and **Verbose** toggles for configuring per-API tracing.

The page also includes an **Enable connection metrics reporting** toggle that controls whether connection events are indexed in Elasticsearch or OpenSearch. This setting is independent of event-metrics reporting and defaults to `true` for new native APIs. When enabled, the system reports connection metrics including client identifiers, broker identifiers, connection status, and connection duration. For details, see [Connection logs](../../analyze-and-monitor-apis/logging/native-api-connection-logs-concepts-and-data-model.md#native-api-connection-logs-concepts-and-data-model).

For complete configuration details and the full attribute reference, see:

* [OpenTelemetry — Per-API tracing configuration for V4 native APIs](../../analyze-and-monitor-apis/opentelemetry.md#per-api-tracing-configuration-for-v4-native-apis)
* [Enable OpenTelemetry tracing for a Kafka API](../../kafka-gateway/create-and-configure-kafka-apis/configure-kafka-apis/enable-opentelemetry-tracing-for-a-kafka-api.md)

