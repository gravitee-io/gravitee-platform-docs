# OpenTelemetry

{% hint style="warning" %}
OpenTelemetry replaces OpenTracing. For more information about OpenTracing, see [OpenTracing](https://app.gitbook.com/s/i9IyjWJmsUdoilz8Mqms/using-the-product/using-the-gravitee-api-management-components/general-configuration/opentracing "mention").
{% endhint %}

## Overview

Gravitee's OpenTelemetry solution allows you to trace every request handled by the API Management (APIM) Gateway. A request refers to the input object as defined by OpenTelemetry, which can be an HTTP request or other objects like a message or Kafka record. The OpenTelemetry framework supports standardized observability, meaning that you can export your Gravitee traces to any telemetry tool. For example, Jaegar.

With OpenTelemetry, tracers are created for specific services. A global tracer is created for a Gateway-level service and follows the same lifecycle as the Gateway. At a more granular level, a tracer can be created when a API is deployed. An API-level tracer follows the same lifecycle as the API and will be stopped/removed when the API is undeployed.

Verbose tracing is supported for v4 APIs and can be enabled for individual APIs. The **Verbose** option uses technical tracing to generate additional request execution details. These additional details increase the number of spans per trace and generates a pre-processor-transaction trace.

To use OpenTelemetry, you must enable OpenTelemetry on your Gateway, and optionally for APIs that you have deployed. When OpenTelemetry is enabled at the API level, OpenTelemetry data is generated.

## Enabling OpenTelemetry for your Gateway

{% hint style="warning" %}
If you currently use the Jaeger plugin, you must update your configuration to target your OpenTelemetry endpoint.

`services.tracing.otel` is deprecated. You must use the following configurations.
{% endhint %}

### Simple configuration

* To enable OpenTelemetry on your Gateway, add the following code to your `gravitee.yaml` file:

```yaml
services:
  opentelemetry:  
    enabled: true
    exporter:
      endpoint: <OPENTELEMETRY_ENDPOINT>
```

* If unset default endpoint is `http://locahost:4317`, replace \<OPENTELMETRY\_ENDPOINT> with the endpoint that you use for OpenTelemetry.
* If your endpoint URL uses `http://` or `grpc://` , you can use this configuration for a basic default configuration.

### Advanced configuration

With the following configuration, you can complete the following actions with OpenTelemetry:

* Configure TLS and mTLS
* Add extra attributes to all spans
* Add headers to exporter requests
* Set proxy configuration

```yaml
services:
  opentelemetry:
    enabled: true
    # Will add technical information spans
    verbose: true
    # Allow to add any extra attributes on all spans
    extraAttributes:
      - deployment.environment.name: production
    
    exporter:
      endpoint: https://localhost:5555
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

For more information about all the settings that you can configure for OpenTelemetry, go to this [GitHub README](https://github.com/gravitee-io/gravitee-node/tree/master/gravitee-node-opentelemetry).

### Helm Charts

1. To enable OpenTelemetry with Helm Charts, add the following configuration to your `values.yml`file:

```yaml
gateway:
  services:
    opentelemetry:
      enabled: true
      exporter:
        endpoint: <OPENTELEMETRY_ENDPOINT>
```

* If unset default endpoint is `http://locahost:4317`, replace \<OPENTELMETRY\_ENDPOINT> with the endpoint that you use for OpenTelemetry.
* If your endpoint URL uses `http://` or `grpc://` , you can use this configuration for a basic default configuration.

2.  (Optional) For a more advanced configuration, add the following configuration to your `values.yaml`:

    With the following configuration, you can complete the following actions with OpenTelemetry:

    * Configure TLS and mTLS
    * Add extra attributes to all spans
    * Add headers to exporter requests
    * Set proxy configuration

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
        endpoint: https://localhost:5555
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

For more information about all the settings that you can configure for OpenTelemetry, go to this [GitHub README](https://github.com/gravitee-io/gravitee-node/tree/master/gravitee-node-opentelemetry).

## Enabling OpenTelemetry for an API

{% hint style="warning" %}
To enable OpenTelemetry for an API, you must have OpenTelemetry enabled on your Gateway.
{% endhint %}

1. Log in to your APIM Console.
2. Select **APIs** from the left nav.
3. Select a deployed API.
4. From the inner left nav, select **API Traffic**.
5. On the **API Traffic** screen, click the **Settings** header.
6. Scroll down to the **OpenTelemetry** section and toggle **Enabled** to ON.
7. (Optional) Toggle **Verbose** to ON to enable technical tracing.

<figure><img src="../../4.7/.gitbook/assets/1 otel 1.png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
Enabling **Verbose** increases the number of spans per trace, which can negatively impact performance.
{% endhint %}

## OpenTelemetry API trace details

OpenTelemetry traces can be used to view the following API transaction details:

* Plan type used (e.g., Keyless, API Key)
* `api_Id`
* Webhook `subscription_Id`
* Webhook URL
* Number of messages (based on the defined sampling value)
* Type of server used (e.g., Mock, Kafka)
* Policies being executed
* `message_Id` (e.g., the ID of each message in a Kafka topic)
* If i call an api with invalid auth, i can see a trace with a warning and logs with details about the errors
* For a POST/GET request: `request_body_size`, `request_content_length`, `context-path`, `host.name` and `http_status_code`
