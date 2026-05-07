---
description: An overview about opentelemetry.
---

# OpenTelemetry

{% hint style="warning" %}
OpenTelemetry replaces OpenTracing. For more information about OpenTracing, see [OpenTracing](https://app.gitbook.com/s/i9IyjWJmsUdoilz8Mqms/using-the-product/using-the-gravitee-api-management-components/general-configuration/opentracing "mention").
{% endhint %}

## Overview

With Gravitee's OpenTelemetry feature, you can trace every request handled by the API Management (APIM) Gateway in self-hosted installations and hybrid deployments. A request refers to the input object as defined by OpenTelemetry, which can be an HTTP request or other objects like a message or Kafka record.

The OpenTelemetry framework supports standardized observability, which means that you can export your Gravitee traces to any telemetry tool. For example, Jaeger.

With OpenTelemetry, tracers are created for specific services. By default, a global tracer is created for a Gateway-level service and follows the same lifecycle as the Gateway. For v2 APIs, this global tracer is used when you enable OpenTelemetry in the Gateway configuration. Optionally, you can create a tracer when a v4 API is deployed. An API-level tracer follows the same lifecycle as the API and stops when you undeploy an API.

You can enable verbose tracing for v4 APIs. Verbose mode adds detailed execution events to each policy span, which captures headers and context attributes before and after policy execution. When you enable verbose tracing, policy descriptions configured in policy step definitions are included in tracing spans as the `gravitee.policy.description` attribute. This inclusion improves observability by annotating trace data with the purpose or intent of each policy step.

For Kafka native APIs, OpenTelemetry tracing provides distributed tracing for Kafka protocol operations, capturing connection lifecycle, authentication, and per-request spans with protocol-specific attributes (topics, batch counts, consumer groups, error codes). Tracing is opt-in at both gateway and API levels, with an optional verbose mode that adds per-phase, per-flow, and per-policy spans for deep debugging.

To enable OpenTelemetry, complete the following steps:

1. [#enable-opentelemetry-for-your-gateway](opentelemetry.md#enable-opentelemetry-for-your-gateway "mention")
2. [#enable-opentelemetry-for-an-api](opentelemetry.md#enable-opentelemetry-for-an-api "mention")

## Naming Conventions

Gravitee follows OpenTelemetry naming conventions:

* Standard attributes are prefixed with `gravitee.`.
* Custom attributes remain unchanged without a prefix or alteration. For example, attributes added with the Assign Attributes policy.
* Headers are prefixed with `http.request.` or `http.response.` based on the execution phase.
* Gravitee-specific headers contain `X-Gravitee` in their names.

## Enable OpenTelemetry for your Gateway

{% hint style="warning" %}
* If you currently use the Jaeger plugin, you must update your configuration to target your OpenTelemetry endpoint.
* `services.tracing.otel` is deprecated.
{% endhint %}

To enable OpenTelemetry for your Gateway, follow the steps for your installation type:

{% tabs %}
{% tab title="gravitee.yml" %}
*   To enable OpenTelemetry, add the following configuration to your `gravitee.yml` file:

    ```yaml
    services:
      opentelemetry:
        enabled: true
        # Will add technical information spans
        verbose: false # set to true to enable verbose
        # Allow to add any extra attributes on all spans
        extraAttributes:
          - deployment.environment.name: production

        # Kafka tracing filter
        kafka:
          # Restricts per-request spans to specific Kafka protocol types; empty list traces all types
          tracedApiKeys:
            - PRODUCE
            - FETCH

        exporter:
          endpoint: <OPENTELEMETRY_ENDPOINT>
          protocol: http/protobuf          # 'grpc' by default
          compression: gzip                # 'none' by default
          # Key-value pairs used as headers of exporter requests
         # headers:
            - X-Custom-Header: value
          # collector max time to process a batch of telemetry data
         # timeout: 10000 # default

          # proxy config (can reuse Gateway's)
         # proxy:
         #   enable: true               # disabled by default
         #   host: myproxy.acme.com
         #   port: 1234

          # if endpoint URL uses scheme https:// the following is used
         # ssl:
         #   trustAll: true                 # false by default
         #   verifyHostname: false          # true by default
            # for mTLS
         #   keystore:
         #     type: pem                    # supports 'pkcs12' and 'jks'
         #     certs:
         #       - /path/to/certificate.pem
         #     keys:
         #       - /path/to/private_key.pem
            # CA certs
         #   truststore:
         #     type: pkcs12                 # supports 'pem' and 'jks'
         #     path: /path/to/certs.p12
         #     password: password

    ```
* Replace `<OPENTELEMETRY_ENDPOINT>` with the endpoint that you use for your OpenTelemetry collector. The default endpoint is `http://localhost:4317`.
{% endtab %}

{% tab title="values.yaml" %}
*   To enable OpenTelemetry, add the following configuration to your `values.yaml` file:

    ```yaml
    gateway:
      services:
        opentelemetry:
          enabled: true
          # Will add technical information spans
          verbose: true
          # Allow to add any extra attributes on all spans
          extraAttributes:
            - deployment.environment.name: production

          # Kafka tracing filter
          kafka:
            # Restricts per-request spans to specific Kafka protocol types; empty list traces all types
            tracedApiKeys:
              - PRODUCE
              - FETCH

          exporter:
            endpoint: <OPENTELEMETRY_ENDPOINT>
            protocol: http/protobuf          # 'grpc' by default
            compression: gzip                # 'none' by default (default)
            # Key-value pairs used as headers of exporter requests
            headers:
              - X-Custom-Header: value
            # collector max time to process a batch of telemetry data
            timeout: 10000 # default

            # proxy config (can reuse Gateway's)
            proxy:
              enable: true               # disabled by default
              host: myproxy.acme.com
              port: 1234

            # if endpoint URL uses scheme https:// the following is used
            ssl:
              trustAll: true                 # false by default
              verifyHostname: false          # true by default
              # for mTLS
              keystore:
                type: pem                    # supports 'pkcs12' and 'jks'
                certs:
                  - /path/to/certificate.pem
                keys:
                  - /path/to/private_key.pem
              # CA certs
              truststore:
                type: pkcs12                 # supports 'pem' and 'jks'
                path: /path/to/certs.p12
                password: password
    ```
* Replace `<OPENTELEMETRY_ENDPOINT>` with the endpoint that you use for the your OpenTelemetry collector. The default endpoint is `http://localhost:4317`.
{% endtab %}

{% tab title="Environment variables" %}
*   To enable enable OpenTelemetry, add the following environment variable to your `.env` file:

    ```bash
    GRAVITEE_SERVICES_OPENTELEMETRY_ENABLED=true
    ```
{% endtab %}
{% endtabs %}

For more information about OpenTelemetry configurations, go to the [Gravitee Node OpenTelemetry GitHub README](https://github.com/gravitee-io/gravitee-node/tree/master/gravitee-node-opentelemetry).

### Kafka Tracing Filter

The `services.opentelemetry.kafka.tracedApiKeys` property restricts per-request spans to specific Kafka protocol types (e.g., `PRODUCE`, `FETCH`). If the list is empty or omitted, all Kafka protocol types are traced. Filtering to `[PRODUCE, FETCH]` reduces noise from housekeeping requests like `METADATA`, `HEARTBEAT`, and `FIND_COORDINATOR`.

### Verification

*   To verify that you are sending traces to your OpenTelemetry collector, use the following command:

    ```bash
    curl -i http://localhost:8082/my-api/endpoint
    ```

    The trace for the Gateway appears in your OpenTelemetry collector.

## Enable OpenTelemetry for an API

{% hint style="warning" %}
To enable OpenTelemetry for an API, you must have OpenTelemetry enabled on your Gateway. For more information, see [#enable-opentelemetry-for-your-gateway](opentelemetry.md#enable-opentelemetry-for-your-gateway "mention").
{% endhint %}

### Per-API Tracing Configuration for V4 Native APIs

V4 NATIVE APIs support per-API OpenTelemetry tracing configuration through the following properties:

| Property | Description | Example |
|:---------|:------------|:--------|
| `analytics.tracing.enabled` | Per-API OpenTelemetry tracing toggle | `true` |
| `analytics.tracing.verbose` | Per-API verbose mode toggle | `false` |

Tracing requires enablement at both the gateway level (`services.opentelemetry.enabled=true`) and the per-API level (`analytics.tracing.enabled=true`). If either is disabled, no spans are created for that API. This two-tier model allows platform administrators to control tracing infrastructure globally while API owners decide which APIs to instrument.

Per-API tracing settings are configured in the Reporter Settings UI for native APIs. The OpenTelemetry section includes **Enabled** and **Verbose** slide toggles. The **Enabled** toggle help text explains that per-request spans are generated only for Kafka operations listed in the gateway-level `services.opentelemetry.kafka.tracedApiKeys` configuration. The **Verbose** toggle help text warns that enabling verbose mode increases trace volume significantly and should be used only for deep debugging. A warning icon is displayed inline with the verbose toggle help text.

Both toggles are disabled when analytics is disabled (`analytics.enabled=false`), the user lacks `api-definition-u` permission, or the API is not V4 or not NATIVE type. The **Verbose** toggle is additionally disabled when tracing is not enabled (`analytics.tracing.enabled=false`).

## Tracing modes

Gravitee APIM offers two levels of tracing to capture API request execution data.

### (Always active) Standard tracing

Standard tracing is enabled by default. It captures request and response flow, policy execution timing, backend invocation spans, error tracking, and conditional policy trigger recording.

For Kafka native APIs, standard mode creates a root connection span (SpanKind.SERVER), authentication span, broker connect span (SpanKind.CLIENT), and per-request grouping spans (e.g., PRODUCE with SpanKind.PRODUCER).

### (Optional) Verbose mode

Verbose mode adds detailed execution events to each policy span. It captures the complete state before and after policy execution through span events that include headers and context attributes. When you enable verbose tracing, policy descriptions configured in policy step definitions are included in tracing spans as the `gravitee.policy.description` attribute.

For Kafka native APIs, verbose mode requires both gateway-level `services.opentelemetry.verbose=true` and per-API `analytics.tracing.verbose=true`. Verbose mode adds per-phase, per-flow, and per-policy spans beneath each per-request span.

#### What verbose mode captures

Verbose mode records the following execution data:

* Detailed header captures (request & response).
* Context attribute snapshots.
* Pre and post policy execution events.
* Complete state visibility before and after each policy.
* Policy descriptions from policy step definitions.
* For Kafka native APIs: per-phase spans (e.g., Interact request, Publish), flow spans (e.g., plan, api), and policy spans.

#### When to enable verbose mode

Enable verbose mode for the following scenarios:

* To debug policy transformations.
* To troubleshoot header manipulation.
* To view context attributes before and after policy execution.
* For deep request/response analysis.
* When compliance requires detailed audit trails.
* To annotate trace data with the purpose or intent of each policy step.

#### Performance considerations

Verbose mode affects resource usage in the following ways:

* Increases trace size significantly (10-50x) by including additional span event data.
* Uses a higher network bandwidth to reach the OpenTelemetry collector.
* Requires additional storage in the observability backend.
* Results in minimal performance impact (< 1ms per policy).

{% hint style="warning" %}
Enable verbose mode only for deep debugging — it significantly increases trace volume on high-throughput Kafka APIs.
{% endhint %}

### Verification

*   To verify that you are sending traces to your OpenTelemetry collector, call the API using the following command:

    ```bash
    curl -i "http://<GATEWAY_HOST>:<GATEWAY_PORT>/<CONTEXT_PATH>/"
    ```

    * Replace `<GATEWAY_HOST>` with your Gateway host. For example, `localhost`.
    * Replace `<GATEWAY_PORT>` with the port for your Gateway. For example, `8084`.
    * Replace `<CONTEXT_PATH>` with the context path for your API. For example, `test`.

    The trace for the API appears in your OpenTelemetry collector.

## Policy description tracing

Policy description tracing enables API administrators to include human-readable policy descriptions in distributed tracing spans when verbose tracing is enabled. This feature annotates trace data with the purpose or intent of each policy step. This feature makes it easier to diagnose API execution flows and troubleshoot issues across request and message processing pipelines.

### Tracing span attributes

When you enable verbose tracing, the gateway adds a `gravitee.policy.description` attribute to each policy execution span. The attribute value is populated from the description field configured in the policy step definition. If the description is blank or if you disable verbose tracing, the attribute is omitted. Existing span attributes, for example, `gravitee.policy`, `gravitee.phase`, `messaging.message.id`, `messaging.operation.type`, have not changed.

### Shared Policy Groups

Shared Policy Groups allow reusable policy chains to be referenced across multiple flows. Policy descriptions from steps within a Shared Policy Group are included in tracing spans when you enable verbose mode. Nested Shared Policy Groups, which is a Shared Policy Group referencing another Shared Policy Group, are not supported and are skipped with a warning logged to the Gateway.

### Creating policy descriptions

To create policy description tracing, configure a description for each policy step in your API flow definition. When the gateway executes the policy, it stores the description in an internal execution context attribute. The tracing hook reads this attribute and adds the `gravitee.policy.description` span attribute if  you enable verbose tracing. For Shared Policy Groups, descriptions from individual steps within the group are captured and traced in the same way. If a policy step has no description or the description is blank, the attribute is not included in the span.

### Viewing tracing data

After you enable verbose tracing and configuring policy descriptions, tracing spans include the `gravitee.policy.description` attribute with existing attribute like `gravitee.policy`, `gravitee.phase`. For message policies, spans also include `messaging.message.id` and `messaging.operation.type` that are set to `PROCESS`. The description attribute is cleared between policy executions. If a subsequent policy has no description, the attribute is set to `null` in the execution context.

The attribute is visible on the span corresponding to the policy execution in any connected OpenTelemetry-compatible observability backend, for example:

* Jaeger
* Grafana Tempo

### Restrictions

Policy description tracing has the following restrictions:

* Policy descriptions are included in tracing spans only when verbose tracing is explicitly enabled using the internal execution context attribute.
* Nested Shared Policy Groups are not supported. Steps with policy ID matching the Shared Policy Group identifier are skipped and a warning is logged with the following message: "Nested Shared Policy Group is not supported. The Shared Policy Group {name}will be ignored".
* Blank or whitespace-only descriptions are treated as absent and not added to spans.
* The description attribute is cleared between policy executions; if a policy has no description, the attribute is set to `null`.
* Disabled steps are excluded from tracing.

### Supported API types

This feature applies to the following API types:

* v4 HTTP/Proxy APIs
* v2 APIs
* v4 Message APIs
* Shared Policy Groups across all API types

APIs without policy descriptions continue to work without changes. APIs with policy descriptions automatically include them in tracing spans when verbose tracing is enabled. No breaking changes are introduced. Existing tracing behavior remains intact when verbose mode is disabled.

## OpenTelemetry API trace details

You can use OpenTelemetry traces to view the following API transaction details:

* Plan type used. For example, Keyless and API Key.
* `api_Id`.
* Webhook `subscription_Id`.
* Webhook URL.
* Number of messages. This number is based on the defined sampling value.
* Type of server used. For example, Mock or Kafka.
* Policies that are executed.
* Policy descriptions when you enable verbose tracing.
* `message_Id`. For example, the ID of each message in a Kafka topic.
* If you call an API with invalid authentication, you can see a trace with a warning and logs with details about the errors.
* For a POST or GET request, you see the following information: `request_body_size`, `request_content_length`, `context-path`, `host.name` and `http_status_code`.

## Kafka Native API Tracing

OpenTelemetry tracing for Kafka native APIs provides distributed tracing for Kafka protocol operations, capturing connection lifecycle, authentication, and per-request spans with protocol-specific attributes (topics, batch counts, consumer groups, error codes).

### Dual-Level Enablement

Tracing requires enablement at both the gateway level (`services.opentelemetry.enabled=true`) and the per-API level (`analytics.tracing.enabled=true`). If either is disabled, no spans are created for that API. This two-tier model allows platform administrators to control tracing infrastructure globally while API owners decide which APIs to instrument.

### Span Attributes

Spans include OpenTelemetry semantic conventions for messaging systems and Gravitee-specific attributes:

| Attribute | Description |
|:----------|:------------|
| `messaging.system` | Always `"kafka"` |
| `messaging.destination.name` | Topic name(s), comma-separated; falls back to `"id:<uuid>"` for Kafka protocol v12+ |
| `messaging.consumer.group.name` | Consumer group ID (JOIN_GROUP, HEARTBEAT, OFFSET_COMMIT, LEAVE_GROUP, SYNC_GROUP) |
| `messaging.batch.message_count` | Number of records in PRODUCE/FETCH request/response |
| `messaging.operation.type` | `"send"` (PRODUCE), `"receive"` (FETCH, JOIN_GROUP, SYNC_GROUP), `"settle"` (OFFSET_COMMIT) |
| `messaging.operation.name` | `"send"`, `"poll"`, `"commit"`, `"join"`, `"sync"`, `"heartbeat"`, `"leave"` |
| `messaging.client.id` | Kafka client ID from request header |
| `error.type` | Kafka error code name (e.g., `"INVALID_REQUEST"`) or exception class name |
| `gravitee.api.id` | API identifier |
| `gravitee.auth.method` | `"SASL"` or `"PLAINTEXT"` |
| `gravitee.auth.sasl.mechanism` | SASL mechanism (e.g., `"PLAIN"`) |
| `gravitee.auth.principal` | Authenticated principal name |
| `gravitee.auth.plan` | Resolved plan name |
| `gravitee.auth.security.type` | Security type (e.g., `"api-key"`, `"key-less"`) |
| `gravitee.error.origin` | Error classification: `"policy"`, `"security"`, `"broker"`, `"internal"` |
| `gravitee.error.recommendation` | Human-readable error guidance |
| `network.peer.address` | Client IP address |
| `network.peer.port` | Client port |
| `server.address` | Broker domain pattern |
| `server.port` | Gateway listener port |

### Error Attribution

Errors are classified by origin (`policy`, `security`, `broker`, `internal`) and recorded in the `gravitee.error.origin` span attribute. Policy failures, authentication failures, broker errors, and internal errors are distinguished to guide troubleshooting.
