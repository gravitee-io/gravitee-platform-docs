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

You can enable verbose tracing for v4 APIs. Verbose mode adds detailed execution events to each policy span, capturing headers and context attributes before and after policy execution.

To enable OpenTelemetry, complete the following steps:

1. [#enable-opentelemetry-for-your-gateway](opentelemetry.md#enable-opentelemetry-for-your-gateway "mention")
2. [#enable-opentelemetry-for-an-api](opentelemetry.md#enable-opentelemetry-for-an-api "mention")

## Naming Conventions&#x20;

Gravitee follows OpenTelemetry naming conventions:

* Standard attributes are prefixed with `gravitee.`.
* Custom attributes remain unchanged without a prefix or alteration. For example, attributes added via the Assign Attributes policy.&#x20;
* Headers are prefixed with `http.request.` or `http.response.` based on the execution phase.
* Gravitee-specific headers contain `X-Gravitee` in their names.&#x20;

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

### Verification

*   To verify that you are sending traces to your OpenTelemetry collector, use the following command:<br>

    ```bash
    curl -i http://localhost:8082/my-api/endpoint
    ```

    \
    The trace for the Gateway appears in your OpenTelemetry collector.

## Enable OpenTelemetry for an API

{% hint style="warning" %}
To enable OpenTelemetry for an API, you must have OpenTelemetry enabled on your Gateway. For more information, see [#enable-opentelemetry-for-your-gateway](opentelemetry.md#enable-opentelemetry-for-your-gateway "mention").
{% endhint %}

## Tracing modes&#x20;

Gravitee APIM offers two levels of tracing to capture API request execution data.

### (Always active) Standard tracing&#x20;

Standard tracing is enabled by default. It captures request and response flow, policy execution timing, backend invocation spans, error tracking, and conditional policy trigger recording.

### (Optional) Verbose mode&#x20;

Verbose mode adds detailed execution events to each policy span. It captures the complete state before and after policy execution through span events that include headers and context attributes.

#### **What verbose mode captures**

Verbose mode records the following execution data:

* Detailed header captures (request & response).
* Context attribute snapshots.
* Pre and post policy execution events.
* Complete state visibility before and after each policy.

#### **When to enable verbose mode:**&#x20;

Enable verbose mode for the following scenarios:

* To debug policy transformations.
* To troubleshoot header manipulation.
* To view context attributes before and after policy execution.&#x20;
* For deep request/response analysis.
* When compliance requires detailed audit trails.

#### **Performance considerations:**&#x20;

Verbose mode affects resource usage in the following ways:

* Increases trace size significantly (10-50x) by including additional span event data.
* Uses a higher network bandwidth to reach the OpenTelemetry collector.
* Requires additional storage in the observability backend.
* Results in minimal performance impact (< 1ms per policy).

### Verification

*   To verify that you are sending traces to your OpenTelemetry collector, call the API using the following command:

    ```bash
    curl -i "http://<GATEWAY_HOST>:<GATEWAY_PORT>/<CONTEXT_PATH>/"
    ```

    * Replace `<GATEWAY_HOST>` with your Gateway host. For example, `localhost`.
    * Replace `<GATEWAY_PORT>` with the port for your Gateway. For example, `8084`.
    * Replace `<CONTEXT_PATH>` with the context path for your API. For example, `test`.

    The trace for the API appears in your OpenTelemetry collector.

## OpenTelemetry API trace details

You can use OpenTelemetry traces to view the following API transaction details:

* Plan type used. For example, Keyless and API Key.
* `api_Id`.
* Webhook `subscription_Id`.
* Webhook URL.
* Number of messages. This number is based on the defined sampling value.
* Type of server used. For example, Mock or Kafka.
* Policies that are executed.
* `message_Id` . For example, the ID of each message in a Kafka topic.
* If you call an API with invalid authentication, you can see a trace with a warning and logs with details about the errors.
* For a POST or GET request, you see the following information: `request_body_size`, `request_content_length`, `context-path`, `host.name` and `http_status_code`.
