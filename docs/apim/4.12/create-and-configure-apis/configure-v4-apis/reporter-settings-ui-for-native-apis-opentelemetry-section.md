# Reporter Settings UI for Native APIs (OpenTelemetry Section)

## Related Changes

The Reporter Settings UI for native APIs now includes an OpenTelemetry section with **Enabled** and **Verbose** slide toggles.

The **Enabled** toggle help text explains that per-request spans are generated only for Kafka operations listed in the gateway-level `services.opentelemetry.kafka.tracedApiKeys` configuration.

The **Verbose** toggle help text warns that enabling verbose mode increases trace volume significantly and should be used only for deep debugging. A warning icon is displayed inline with the verbose toggle help text.

Both toggles are disabled when analytics is disabled, the user lacks `api-definition-u` permission, or the API is not V4 or not NATIVE type. The **Verbose** toggle is additionally disabled when tracing is not enabled.

