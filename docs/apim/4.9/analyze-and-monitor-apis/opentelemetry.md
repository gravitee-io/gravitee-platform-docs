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

With OpenTelemetry, tracers are created for specific services. By default, A global tracer is created for a Gateway-level service and follows the same lifecycle as the Gateway. Optionally, you can create a tracer when an API is deployed. An API-level tracer follows the same lifecycle as the API and stops when you undeploy an API.

You can enable verbose tracing for v4 APIs. The Verbose option uses technical tracing to generate additional request execution details. These additional details increase the number of spans per trace and generates a pre-processor-transaction trace.

To enable OpenTelemetry, complete the following steps:

1. [#enable-opentelemetry-for-your-gateway](opentelemetry.md#enable-opentelemetry-for-your-gateway "mention")
2. [#enable-opentelemetry-for-an-api](opentelemetry.md#enable-opentelemetry-for-an-api "mention")

## Enable OpenTelemetry for your Gateway

{% hint style="warning" %}
* If you currently use the Jaeger plugin, you must update your configuration to target your OpenTelemetry endpoint.
* `services.tracing.otel` is deprecated.
{% endhint %}

* To enable OpenTelemetry for your Gateway, follow the steps for your installation type:

{% tabs %}
{% tab title="gravitee.yml" %}
-   To enable OpenTelemetry, add the following configuration to your `gravitee.yml` file:<br>

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
- Replace `<OPENTELEMETRY_ENDPOINT>` with the endpoint that you use for your OpenTelemetry collector. The default endpoint is `http://localhost:4317`.
{% endtab %}

{% tab title="values.yaml" %}
*   To enable OpenTelemetry, add the following configuration to your `values.yaml` file:<br>

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
*   To enable enable OpenTelemetry, add the following environment variable to your `.env` file:<br>

    ```bash
    GRAVITEE_SERVICES_OPENTELEMETRY_ENABLED=true
    ```
{% endtab %}
{% endtabs %}

For more information about OpenTelemetry configurations, go to [Gravitee's Gravitee Node OpenTelemetry GitHub README](https://github.com/gravitee-io/gravitee-node/tree/master/gravitee-node-opentelemetry).

### Verification

*   To verify that you are sending traces to your OpenTelemetry collector, use the following command:<br>

    ```
    curl -i http://localhost:8082/my-api/endpoint
    ```

    \
    The trace for the Gateway appears in your OpenTelemetry collector.

## Enable OpenTelemetry for an API

{% hint style="warning" %}
To enable OpenTelemetry for an API, you must have OpenTelemetry enabled on your Gateway. For more information about enabling OpenTelemetry for your Gateway, see [#enable-opentelemetry-for-your-gateway](opentelemetry.md#enable-opentelemetry-for-your-gateway "mention").
{% endhint %}

1.  From the **Dashboard**, click **APIs**.<br>

    <figure><img src="../.gitbook/assets/image (59).png" alt=""><figcaption></figcaption></figure>
2.  From the **APIs** screen, select the API that you to enable OpenTelemetry for.<br>

    <figure><img src="../.gitbook/assets/image (60).png" alt=""><figcaption></figcaption></figure>
3.  From your **API** menu, click **Deployment**.<br>

    <figure><img src="../.gitbook/assets/image (55) (1) (1).png" alt=""><figcaption></figcaption></figure>
4.  From the **Deployment** screen, click **Reporter Settings**.<br>

    <figure><img src="../.gitbook/assets/image (58) (1).png" alt=""><figcaption></figcaption></figure>
5.  Navigate to the **OpenTelemetry** section, and then turn on the **Enabled** toggle.<br>

    <figure><img src="../.gitbook/assets/image (65).png" alt=""><figcaption></figcaption></figure>
6.  (Optional) Turn on the **Verbose** toggle.<br>

    <div data-gb-custom-block data-tag="hint" data-style="warning" class="hint hint-warning"><p>If you enable verbose, the number of spans for each trace increases, which might impact performance.</p></div>

    <figure><img src="../.gitbook/assets/image (66).png" alt=""><figcaption></figcaption></figure>
7.  In the **You have unsaved changes** pop-up window, click **Save**.<br>

    <figure><img src="../.gitbook/assets/image (67).png" alt=""><figcaption></figcaption></figure>

### Verification

*   To verify that you are sending traces to your OpenTelemetry collector, call the API using the following command:<br>

    ```
    curl -i "http://<GATEWAY_HOST>:<GATEWAY_PORT>/<CONTEXT_PATH>/"
    ```

    * Replace `<GATEWAY_HOST>` with your Gateway host. For example, `localhost` .
    * Replace `<GATEWAY_PORT>` with the port for your Gateway. For example, `8084` .
    * Replace `<CONTEXT_PATH>` with the context path for your API. For example, `test` .

The trace for the API appears in your OpenTelemetry collector.

## OpenTelemetry API trace details

You can use OpenTelemetry traces to view the following API transaction details:

* Plan type used. For example, Keyless and API Key.
* `api_Id` .
* Webhook `subscription_Id` .
* Webhook URL.
* Number of messages. This number is based on the defined sampling value.
* Type of server used. For example, Mock and Kafka.
* Policies being executed,
* `message_Id` . For example, the ID of each message in a Kafka topic.
* If you call an API with invalid auth, you can see a trace with a warning and logs with details about the errors.
* For a POST or GET request, you see the following information: `request_body_size`, `request_content_length`, `context-path`, `host.name` and `http_status_code`
