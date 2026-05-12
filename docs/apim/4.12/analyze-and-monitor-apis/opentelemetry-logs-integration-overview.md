# OpenTelemetry Logs Integration Overview

## Overview

OpenTelemetry Logs Integration injects active trace IDs and span IDs into runtime log records captured during request processing and exports them to Loki via OTLP. This enables full log-to-trace correlation in Grafana: each log line in Loki carries the trace ID so you can navigate directly from a log to its corresponding trace in Tempo. This applies to v4 HTTP/Proxy APIs and v4 Message APIs.

## Key Concepts

### Log-to-Trace Correlation

When OTel Logs is enabled, every runtime log record captured during request processing includes the active OpenTelemetry trace ID and span ID. These identifiers allow observability backends like Grafana to link log lines in Loki to their corresponding distributed traces in Tempo. The gateway exports log records asynchronously via OTLP/HTTP to avoid adding latency to the request path.

### Capture Points

Each Loki log entry corresponds to one of four capture points in the request lifecycle:

| Capture Point | Log Body Content |
|:--------------|:-----------------|
| entrypoint-request | Request body before any policies (original payload) |
| endpoint-request | Request body after request policies (transformed payload) |
| endpoint-response | Raw backend response body |
| entrypoint-response | Response body + response headers after response policies |

### OTel Logs Toggle

The OTel Logs toggle is a per-API setting available in the Console UI under Runtime Logs settings. It is only available when OpenTelemetry Tracing is already enabled on the API. When enabled, all four payload directions (entrypoint request/response, endpoint request/response) are captured regardless of Elasticsearch logging configuration. Header capture remains controlled by the Elasticsearch logging configuration. Capture is subject to the tracing sampling strategy configured in the API analytics settings.

<figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-01.png" alt="OpenTelemetry settings panel showing Enabled, Verbose, and OTel Logs toggle options"><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/apim-opentelemetry-logs-integration-step-02.png" alt="OpenTelemetry settings showing Enabled toggle active, Verbose toggle inactive, and OTel Logs toggle inactive"><figcaption></figcaption></figure>

## Prerequisites

Before you enable OpenTelemetry Logs Integration, complete the following steps:

* Install the `gravitee-reporter-otel` plugin on the gateway by copying the plugin `.zip` file into the gateway's `plugins/` directory. The gateway silently ignores `.jar` files — the plugin must be a `.zip`. Without this plugin, trace and span IDs are captured internally but nothing is exported to Loki.
* Enable OpenTelemetry globally on the gateway.
* Ensure a compatible log backend is reachable from the gateway (e.g., Loki via an OTel Collector or directly via OTLP/HTTP).
* Verify that the `service.name` used by both the tracer and the OTel logger match in Tempo and Loki for Grafana log-trace correlation to work. Both use `gio_apim_gateway` by default. If they differ, the "Logs for this span" button in Tempo will silently return no results.

