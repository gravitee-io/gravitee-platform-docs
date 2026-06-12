---
description: An overview about reporters.
metaLinks:
  alternates:
    - ./
hidden: true
noIndex: true
---

# Reporters

## Overview

Reporters are designed to record a variety of events occurring in the Gravitee API Management (APIM) Gateway and output them to a new source in their order of occurrence. Reporters take the **application** **data** from the Gravitee gateway, capturing metrics and logs about proxied requests, and offload them to a system of your choice. Reporters are a critical part of creating a production-grade monitoring system for your API traffic in Gravitee.

Elasticsearch is the default reporter for gateway runtime data and is required for visualizing runtime analytics in the Gravitee UI. You can also use reporters to feed other visualization tools, e.g. for those based on Elastic (Kibana), or for systems like Datadog.

{% hint style="info" %}
If you want to monitor the **server** logs from the gateway or the management API, you can use an agent for your observability platform (e.g. the [Datadog agent](https://docs.datadoghq.com/agent/?tab=Linux)) to tail the server logs. If you want to monitor the server metrics from your Gravitee infrastructure (e.g. CPU and memory usage), you can instrument the server directly or use the Prometheus endpoint for the Gravitee component.
{% endhint %}

You can configure various aspects of reporters, such as reporting monitoring data, request metrics, and health checks. All reporters are enabled by default. To stop a reporter, you need to add the property `enabled: false`. Use the tab that matches your deployment method.

{% tabs %}
{% tab title="gravitee.yaml" %}
```yaml
reporters:
  elasticsearch:
    endpoints:
      - http://localhost:9200
#    index: gravitee
#    bulk:
#       actions: 500           # Number of requests action before flush
#       flush_interval: 1      # Flush interval in seconds
#    security:
#       username:
#       password:
```
{% endtab %}

{% tab title=".env" %}
Add the following variables to the `.env` file loaded by your `docker-compose.yml`, or to the `environment:` block of the Gateway service:

```bash
gravitee_reporters_elasticsearch_endpoints_0=http://localhost:9200
# gravitee_reporters_elasticsearch_index=gravitee
# gravitee_reporters_elasticsearch_bulk_actions=500
# gravitee_reporters_elasticsearch_bulk_flush_interval=1
# gravitee_reporters_elasticsearch_security_username=
# gravitee_reporters_elasticsearch_security_password=
```
{% endtab %}

{% tab title="Helm values.yaml" %}
The Elasticsearch reporter is enabled by default in the APIM Helm chart. Connection details come from the shared `es:` block; reporter-specific toggles go under `gateway.reporters.elasticsearch`:

```yaml
gateway:
  reporters:
    elasticsearch:
      enabled: true

es:
  endpoints:
    - http://elasticsearch-master:9200
  index: gravitee
  security:
    enabled: false
    # username:
    # password:
```
{% endtab %}
{% endtabs %}

This page documents the available reporters and the metrics and logs captured by each reporter, in a generic format. The configuration for each reporter and the format of the metrics in those reporting systems are covered in their own pages.

{% hint style="warning" %}
Configuration details for the Elasticsearch reporter are available in the [Elasticsearch Repository](../../prepare-a-production-environment/repositories/elasticsearch.md#elasticsearch) documentation.
{% endhint %}

## Available Reporters

The following reporters are currently compatible with APIM:

<table><thead><tr><th width="151">Type</th><th data-type="checkbox">Bundled in Distribution</th><th data-type="checkbox">Default</th><th data-type="checkbox">Enterprise only</th></tr></thead><tbody><tr><td>Elasticsearch</td><td>true</td><td>true</td><td>false</td></tr><tr><td>File</td><td>true</td><td>false</td><td>false</td></tr><tr><td>TCP</td><td>true</td><td>false</td><td>true</td></tr><tr><td>Datadog</td><td>false</td><td>false</td><td>true</td></tr></tbody></table>

{% hint style="warning" %}
To learn more about Gravitee [Enterprise Edition](../../readme/enterprise-edition.md) and what's included in various enterprise packages, please:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

## Metrics Sent via Reporters

By default, reporters generate the following data, with the camelCase format shown generically. Each reporter type converts the naming convention from camelCase to the format required by that system. The metrics are different between Gravitee v2 and v4 APIs, and v4 metrics are further broken down by request-level metrics and message-level metrics. v4 APIs that use LLM-Proxy or MCP-Proxy endpoints report additional metrics specific to those API types.

### Custom Metrics from Policies

Some policies emit custom metrics that appear in the API analytics dashboard. These metrics are stored under `additional-metrics` and use typed prefixes (`keyword_`, `long_`, `double_`) to indicate the field type in the reporting system.

#### PII Filtering Policy Metrics

The PII Filtering Policy emits the following custom metrics when PII is detected:

| Metric Name           | Type | Purpose                                                                                           |
| --------------------- | ---- | ------------------------------------------------------------------------------------------------- |
| `long_pii_total`      | long | Total count of PII detections across all categories                                               |
| `long_pii_<category>` | long | Per-category PII detection count (e.g., `long_pii_person`, `long_pii_email`, `long_pii_location`) |

These metrics are incremented for each detected PII entity and are visible in the API analytics dashboard alongside standard request metrics.

{% tabs %}
{% tab title="v4 Metrics" %}
<table><thead><tr><th width="349">Metric Name</th><th>Purpose</th></tr></thead><tbody><tr><td>requestId</td><td>Unique identifier Universally Unique Identifier (UUID) identifying the request</td></tr><tr><td>transactionId</td><td>Used to track end-to-end transactions spanning across multiple HTTP requests. The Gateway configuration allows defining an expected correlation ID header passed by a client request. If this header is set, the content of this field will be set to the value of the header. If no correlation header has been passed, the content of this field will be the same as the content of the request ID. This value will be propagated to the upstream service using the correlation header defined in the configuration (the default header is <code>X-Gravitee-Transaction-Id</code>).</td></tr><tr><td>apiId</td><td>ID of the API</td></tr><tr><td>apiName</td><td>Name of the API at the time of the request</td></tr><tr><td>apiProductId</td><td>ID of the API Product the API belongs to. Empty if the API isn't part of an API Product.</td></tr><tr><td>apiType</td><td>Type of the API (message, proxy)</td></tr><tr><td>planId</td><td>ID of the plan</td></tr><tr><td>applicationId</td><td>The application ID; for a keyless plan, this value is "1"</td></tr><tr><td>subscriptionId</td><td>The subscription ID; for a keyless plan, this value will be the same as the value of the remote address field</td></tr><tr><td>organizationId</td><td>ID of the organization the API belongs to</td></tr><tr><td>environmentId</td><td>ID of the environment the API belongs to</td></tr><tr><td>clientIdentifier</td><td>Unique identifier for the client</td></tr><tr><td>tenant</td><td>ID of the tenant evaluated for the API (see <a href="../../configure-and-manage-the-platform/gravitee-gateway/tenants.md">tenants</a>)</td></tr><tr><td>zone</td><td>Text field set in gravitee.yml to indicate additional information about the gateway instance the API is running on</td></tr><tr><td>httpMethod</td><td>HTTP verb used in the client connection</td></tr><tr><td>localAddress</td><td>The address used as a destination when the incoming request was issued by the client</td></tr><tr><td>remoteAddress</td><td>The remote address used as a source when the incoming request was issued by the client</td></tr><tr><td>host</td><td>The content of the <code>Host</code> header, passed when the incoming request was issued by the client</td></tr><tr><td>uri</td><td>The URI used by the client to perform its request (this includes the context path of the request and query parameters)</td></tr><tr><td>pathInfo</td><td>The path used to perform the client request (starting from the context path of the API)</td></tr><tr><td>mappedPath</td><td>If a path mapping has been defined to group requests in your analytics, this is the value of your mapping.</td></tr><tr><td>userAgent</td><td>The content of the <code>User-Agent</code> header, passed by the client when the incoming request was issued</td></tr><tr><td>requestContentLength</td><td>The size of the body, in bytes, of the incoming request issued by the Gateway client</td></tr><tr><td>requestEnded</td><td>Boolean to indicate if the request has completed; request may be ongoing if the connection is over Websocket or SSE</td></tr><tr><td>entrypointId</td><td>ID of the entrypoint used in the API connection</td></tr><tr><td>endpoint</td><td>The URL used by the proxy to forward the request to the upstream service</td></tr><tr><td>endpointResponseTimeMs</td><td>The time (ms) it takes the upstream service to respond to the Gateway proxy</td></tr><tr><td>responseContentLength</td><td>The size of the body, in bytes, of the response received by the Gateway client</td></tr><tr><td>status</td><td>HTTP response status code returned to the client</td></tr><tr><td>gatewayResponseTimeMs</td><td>The time (ms) it takes the Gateway to respond to the client (this includes the roundtrip between the Gateway and the upstream service)</td></tr><tr><td>gatewayLatencyMs</td><td>The overhead added by the Gateway when forwarding the request upstream and the response back to the client</td></tr><tr><td>user</td><td>The authenticated user, if any type of security was used when processing the request</td></tr><tr><td>securityType</td><td>The security type, if security was used when processing the request (can be either API_KEY, OAUTH2 or JWT)</td></tr><tr><td>securityToken</td><td>The security token, if any type of security was used when processing the request</td></tr><tr><td>errorMessage</td><td>A more detailed explanation of the error associated with the error key (if any)</td></tr><tr><td>errorKey</td><td>If the policy chain was interrupted by an error, this key identifies the error type</td></tr></tbody></table>
{% endtab %}

{% tab title="v4 Message Metrics" %}
| Metric Name         | Purpose                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| requestId           | ID of the request                                                                                 |
| apiId               | ID of the API                                                                                     |
| apiName             | Name of the API at the time of the request                                                        |
| organizationId      | ID of the organization the API belongs to                                                         |
| environmentId       | ID of the environment the API belongs to                                                          |
| clientIdentifier    | Unique ID for the client                                                                          |
| correlationId       | Internal and unique ID to identify the Gravitee message                                           |
| parentCorrelationId | Parent correlation ID of the message, if any                                                      |
| operation           | AsyncAPI operation, either subscribe or publish                                                   |
| connectorType       | Type of connector from which the message originated, either endpoint or entrypoint                |
| connectorId         | ID of the connector from which the message originated (e.g. Mock, SSE, Webhook, Kafka)            |
| contentLength       | Size of the message                                                                               |
| count               | Number of messages processed without error                                                        |
| errorCount          | Number of messages for which an error was produced                                                |
| countIncrement      | Total number of messages processed across requests, based on the metrics for the previous message |
| errorCountIncrement | Total number of error processed across requests, based on the metrics for the previous message    |
| error               | Boolean for whether there was an error message                                                    |
| gatewayLatencyMs    | Latency added to the request execution when processing the message                                |
{% endtab %}

{% tab title="v2 Metrics" %}
<table><thead><tr><th width="349">Metric Name</th><th>Purpose</th></tr></thead><tbody><tr><td>timestamp</td><td>The timestamp of the transaction in milliseconds</td></tr><tr><td>proxyResponseTimeMs</td><td>The time (ms) it takes the Gateway to respond to the client (this includes the roundtrip between the Gateway and the upstream service)</td></tr><tr><td>proxyLatencyMs</td><td>The overhead added by the Gateway when forwarding the request upstream and the response back to the client</td></tr><tr><td>apiResponseTimeMs</td><td>The time (ms) it takes the upstream service to respond to the Gateway proxy</td></tr><tr><td>requestId</td><td>Unique identifier Universally Unique Identifier (UUID) identifying the request</td></tr><tr><td>api</td><td>ID of the API</td></tr><tr><td>apiName</td><td>Name of the API at the time of the request</td></tr><tr><td>application</td><td>The application ID; for a keyless plan, this value is "1"</td></tr><tr><td>transactionId</td><td>Used to track end-to-end transactions spanning across multiple HTTP requests. The Gateway configuration allows defining an expected correlation ID header passed by a client request. If this header is set, the content of this field will be set to the value of the header. If no correlation header has been passed, the content of this field will be the same as the content of the request ID. This value will be propagated to the upstream service using the correlation header defined in the configuration (the default header is <code>X-Gravitee-Transaction-Id</code>).</td></tr><tr><td>clientIdentifier</td><td>Unique identifier for the client</td></tr><tr><td>organizationId</td><td>ID of the organization the API belongs to</td></tr><tr><td>environmentId</td><td>ID of the environment the API belongs to</td></tr><tr><td>tenant</td><td>ID of the tenant evaluated for the API (see <a href="../../configure-and-manage-the-platform/gravitee-gateway/tenants.md">tenants</a>)</td></tr><tr><td>message</td><td>A detailed explanation of the error associated with the error key (if any)</td></tr><tr><td>plan</td><td>ID of the plan</td></tr><tr><td>localAddress</td><td>The address used as a destination when the incoming request was issued by the client</td></tr><tr><td>remoteAddress</td><td>The remote address used as a source when the incoming request was issued by the client</td></tr><tr><td>httpMethod</td><td>HTTP verb used in the client connection</td></tr><tr><td>host</td><td>The content of the <code>Host</code> header, passed when the incoming request was issued by the client</td></tr><tr><td>uri</td><td>The URI used by the client to perform its request (this includes the context path of the request and query parameters)</td></tr><tr><td>requestContentLength</td><td>The size of the body, in bytes, of the response received by the Gateway client</td></tr><tr><td>responseContentLength</td><td>The size of the body, in bytes, of the response received by the Gateway client</td></tr><tr><td>status</td><td>HTTP response status code integer</td></tr><tr><td>endpoint</td><td>The URL used by the proxy to forward the request to the upstream service</td></tr><tr><td>path</td><td>The path used to perform the client request (starting from the context path of the API)</td></tr><tr><td>mappedPath</td><td>If a path mapping has been defined to group requests in your analytics, this is the value of your mapping.</td></tr><tr><td>userAgent</td><td>The content of the <code>User-Agent</code> header, passed by the client when the incoming request was issued</td></tr><tr><td>user</td><td>The authenticated user, if any type of security was used when processing the request</td></tr><tr><td>securityType</td><td>The security type, if security was used when processing the request (can be either API_KEY, OAUTH2 or JWT)</td></tr><tr><td>securityToken</td><td>The security token, if any type of security was used when processing the request</td></tr><tr><td>errorKey</td><td>If the policy chain was interrupted by an error, this key identifies the error type</td></tr><tr><td>subscription</td><td>The subscription ID; for a keyless plan, this value will be the same as the value of the remote address field</td></tr><tr><td>zone</td><td>Text field set in gravitee.yml to indicate additional information about the gateway instance the API is running on</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

When a v4 API uses an LLM-Proxy endpoint, the following additional metrics are reported alongside the standard v4 metrics. These metrics are stored under `additional-metrics` and use typed prefixes (`keyword_`, `long_`, `double_`) to indicate the field type in the reporting system.

| Metric Name                      | Type    | Purpose                                                                                      |
| -------------------------------- | ------- | -------------------------------------------------------------------------------------------- |
| `keyword_llm-proxy_provider`     | keyword | The endpoint group name (provider) used for the request (for example, `openai`, `anthropic`) |
| `keyword_llm-proxy_model`        | keyword | The model name used for the request (for example, `gpt-4`, `claude-3`)                       |
| `long_llm-proxy_tokens-sent`     | long    | Number of input tokens sent to the LLM                                                       |
| `long_llm-proxy_tokens-received` | long    | Number of output tokens received from the LLM                                                |
| `double_llm-proxy_sent-cost`     | double  | Cost of input tokens, based on model pricing configuration                                   |
| `double_llm-proxy_received-cost` | double  | Cost of output tokens, based on model pricing configuration                                  |

{% hint style="info" %}
The Gateway also computes two derived metrics for analytics dashboards: **total token count** (`tokens-sent + tokens-received`) and **total token cost** (`sent-cost + received-cost`). These are calculated at query time and do not appear as separate reported fields.
{% endhint %}

When a v4 API uses an MCP-Proxy endpoint, the following additional metrics are reported alongside the standard v4 metrics. These metrics are stored under `additional-metrics` and use typed prefixes (`keyword_`, `long_`) to indicate the field type in the reporting system.

| Metric Name                          | Type    | Purpose                                                                                                       |
| ------------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------- |
| `long_mcp-proxy_response-error-code` | long    | Numeric MCP error code returned by the backend. Typically follows JSON-RPC 2.0 error codes (see table below). |
| `keyword_mcp-proxy_method`           | keyword | Static keyword indicating the MCP method invoked by the request                                               |
| `keyword_mcp-proxy_tools/call`       | keyword | The name of the tool called via the `tools/call` method                                                       |
| `keyword_mcp-proxy_resources/read`   | keyword | The URI of the resource read via the `resources/read` method                                                  |
| `keyword_mcp-proxy_prompts/get`      | keyword | The name of the prompt retrieved via the `prompts/get` method                                                 |

The `keyword_mcp-proxy_{method}` metrics are dynamic: each distinct MCP method produces its own keyword field reporting the specific name or URI used.

**MCP error codes**

The `long_mcp-proxy_response-error-code` field uses standard JSON-RPC 2.0 error codes:

| Error Code | Meaning            |
| ---------- | ------------------ |
| -32700     | Parse error        |
| -32600     | Invalid request    |
| -32601     | Method not found   |
| -32602     | Invalid params     |
| -32603     | Internal error     |
| -32002     | Resource not found |

## Log Data Sent via Reporters

In addition to metrics, the gateway can send additional log messages about API execution to the target reporting system. The content of the logs depends on how [logging is configured](../logging/) for the API, and whether the API is a v2 or v4 API. There are also separate log messages generated for v4 request and response phases as well as message-level logging (which uses sampling). The contents of the logs are as follows:

{% tabs %}
{% tab title="v4 Logs" %}
| Log Identifier     | Purpose                                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------------------------- |
| apiId              | ID of the API                                                                                                       |
| apiName            | Name of the API at the time of the request                                                                          |
| clientIdentifier   | Unique identifier for the client                                                                                    |
| endpointRequest    | Map of the request body, method, and URI sent by the client                                                         |
| endpointResponse   | Map of the request body and status returned by the client                                                           |
| entrypointRequest  | Map of the body, method, and URI sent by the gateway to the backend                                                 |
| entrypointResponse | Map of the body and status returned by the gateway from the backend                                                 |
| requestEnded       | Boolean to indicate if the request has completed; request may be ongoing if the connection is over Websocket or SSE |
| requestId          | Unique identifier Universally Unique Identifier (UUID) identifying the request                                      |
{% endtab %}

{% tab title="v4 Message Logs" %}
| Log Identifier    | Purpose                                                                                  |
| ----------------- | ---------------------------------------------------------------------------------------- |
| apiId             | ID of the API                                                                            |
| apiName           | Name of the API at the time of the request                                               |
| client Identifier | Unique identifier for the client                                                         |
| connectorId       | ID of the connector from which the message originated (e.g. Mock, SSE, Webhook, Kafka)   |
| connectorType     | Type of connector from which the message originated, either endpoint or entrypoint       |
| correlationId     | Internal and unique ID to identify the Gravitee message                                  |
| messageId         | Unique identifier for the message                                                        |
| messagePayload    | Contents of the message; you can disable message payload logging in the logging settings |
| operation         | AsyncAPI operation, either subscribe or publish                                          |
| requestId         | ID of the request                                                                        |
{% endtab %}

{% tab title="v2 Logs" %}
| Log Identifier | Purpose                                                             |
| -------------- | ------------------------------------------------------------------- |
| api            | ID of the API                                                       |
| apiName        | Name of the API at the time of the request                          |
| clientRequest  | Map of the request body, method, and URI sent by the client         |
| clientResponse | Map of the request body and status returned by the client           |
| proxyRequest   | Map of the body, method, and URI sent by the gateway to the backend |
| proxyResponse  | Map of the body and status returned by the gateway from the backend |
{% endtab %}
{% endtabs %}

## Formats

The same payload can be sent to any of the Gravitee reporters to write the record of events to a particular output. Payload data can be converted to JSON, CSV, or Elasticsearch format, depending on the reporter type:

<table><thead><tr><th width="192">Reporter</th><th data-type="checkbox">JSON</th><th data-type="checkbox">CSV</th><th data-type="checkbox">Elasticsearch</th></tr></thead><tbody><tr><td>Elasticsearch</td><td>false</td><td>false</td><td>true</td></tr><tr><td>File</td><td>true</td><td>true</td><td>true</td></tr><tr><td>TCP</td><td>true</td><td>true</td><td>true</td></tr><tr><td>Datadog</td><td>false</td><td>false</td><td>false</td></tr></tbody></table>

The metrics are generated in the various formats stated above depending on the reporter, and depending on the execution engine the API uses . An example of the formats is as below (Datadog has a unique format structure):

{% tabs %}
{% tab title="JSON" %}
When using e.g. the File Reporter with JSON format, here is a sample of the contents of `metrics.json`:

{% code title="Reactive engine" %}
```json
{
  "timestamp": 1692359213844,
  "requestId": "076aea69-6024-4590-aaea-6960247590a0",
  "transactionId": "076aea69-6024-4590-aaea-6960247590a0",
  "apiId": "5f67b38f-0700-4557-a7b3-8f0700855779",
  "apiName": "echo-api",
  "apiType": "proxy",
  "planId": "8463511c-fbed-4ca9-a351-1cfbed9ca99d",
  "applicationId": "91f077b0-1204-49e4-b077-b0120419e4f6",
  "subscriptionId": "318e47e5-349c-4fa4-8e47-e5349c3fa444",
  "clientIdentifier": "318e47e5-349c-4fa4-8e47-e5349c3fa444",
  "organizationId": "DEFAULT",
  "environmentId": "DEFAULT",
  "httpMethod": "GET",
  "localAddress": "127.0.0.1",
  "remoteAddress": "127.0.0.1",
  "host": "localhost:8082",
  "uri": "/test-v4",
  "pathInfo": "",
  "userAgent": "curl/7.88.1",
  "requestContentLength": -1,
  "requestEnded": true,
  "entrypointId": "http-proxy",
  "endpoint": "https://api.gravitee.io/echo",
  "endpointResponseTimeMs": 137,
  "status": 200,
  "responseContentLength": 274,
  "gatewayResponseTimeMs": 144,
  "gatewayLatencyMs": 7,
  "errorKey": null,
  "errorMessage": null
}
```
{% endcode %}

{% code title="Legacy engine" %}
```json
{
  "timestamp": 1692357381941,
  "proxyResponseTimeMs": 150,
  "proxyLatencyMs": 6,
  "apiResponseTimeMs": 144,
  "requestId": "13f5ae30-068b-4e2d-b5ae-30068bae2d2d",
  "api": "ff3c6c48-53e0-41d6-bc6c-4853e011d656",
  "apiName": "echo-api",
  "application": "91f077b0-1204-49e4-b077-b0120419e4f6",
  "transactionId": "13f5ae30-068b-4e2d-b5ae-30068bae2d2d",
  "plan": "e115ea63-7cef-4646-95ea-637cef7646ec",
  "organizationId": "DEFAULT",
  "environmentId": "DEFAULT",
  "localAddress": "127.0.0.1",
  "remoteAddress": "127.0.0.1",
  "httpMethod": "GET",
  "host": "localhost:8082",
  "uri": "/test",
  "requestContentLength": 0,
  "responseContentLength": 275,
  "status": 200,
  "endpoint": "https://api.gravitee.io/echo",
  "path": "",
  "userAgent": "curl/7.88.1",
  "securityType": "API_KEY",
  "securityToken": "21b560b2-59b8-4a4b-921a-32b3731fdec4",
  "subscription": "04975880-f147-43bc-9758-80f147e3bcbb",
  "customMetrics": {
    "zone": "europe-north1-a"
  }
}
```
{% endcode %}
{% endtab %}

{% tab title="CSV" %}
The File Reporter writes one CSV record per request to `metrics.csv`. Fields are separated by `;`, string values are wrapped in `"`, and each record ends with `\r\n`. Empty values appear as `""` for strings and as the empty position for numbers. Columns are written in a fixed order, which differs between the Reactive engine (v4 APIs) and the Legacy engine (v2 APIs).

The columns described below are the request metrics. Records also contain trailing columns for any populated `additionalMetrics` (numeric, double, keyword, boolean, integer, string, and JSON values, in that order) followed by any `customMetrics` set on the request. Each `additionalMetrics` and `customMetrics` value is appended in iteration order.

{% code title="Reactive engine — column reference" %}
<table>
    <thead>
        <tr>
            <th width="80">Position</th>
            <th width="220">Column</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>1</td><td><code>transactionId</code></td><td>End-to-end transaction ID. Falls back to <code>requestId</code> if no correlation header is set.</td></tr>
        <tr><td>2</td><td><code>requestId</code></td><td>Unique UUID identifying the request.</td></tr>
        <tr><td>3</td><td><code>timestamp</code></td><td>Request timestamp in milliseconds since epoch.</td></tr>
        <tr><td>4</td><td><code>remoteAddress</code></td><td>Source address of the incoming request.</td></tr>
        <tr><td>5</td><td><code>localAddress</code></td><td>Destination address the incoming request was issued to.</td></tr>
        <tr><td>6</td><td><code>apiId</code></td><td>ID of the API.</td></tr>
        <tr><td>7</td><td><code>apiName</code></td><td>Name of the API at the time of the request.</td></tr>
        <tr><td>8</td><td><code>organizationId</code></td><td>ID of the organization the API belongs to.</td></tr>
        <tr><td>9</td><td><code>environmentId</code></td><td>ID of the environment the API belongs to.</td></tr>
        <tr><td>10</td><td><code>applicationId</code></td><td>Application ID. <code>"1"</code> for keyless plans.</td></tr>
        <tr><td>11</td><td><code>planId</code></td><td>ID of the plan.</td></tr>
        <tr><td>12</td><td><code>subscriptionId</code></td><td>Subscription ID. Empty for keyless plans.</td></tr>
        <tr><td>13</td><td><code>user</code></td><td>Authenticated user, if security was used.</td></tr>
        <tr><td>14</td><td><code>tenant</code></td><td>Tenant evaluated for the API.</td></tr>
        <tr><td>15</td><td><code>uri</code></td><td>URI used by the client (includes context path and query string).</td></tr>
        <tr><td>16</td><td><code>pathInfo</code></td><td>Path portion after the API context path.</td></tr>
        <tr><td>17</td><td><code>mappedPath</code></td><td>Path mapping value, if a path mapping is configured.</td></tr>
        <tr><td>18</td><td><code>httpMethod</code></td><td>HTTP method of the client request.</td></tr>
        <tr><td>19</td><td><code>status</code></td><td>HTTP response status code returned to the client.</td></tr>
        <tr><td>20</td><td><code>entrypointId</code></td><td>ID of the entrypoint used by the API.</td></tr>
        <tr><td>21</td><td><code>endpoint</code></td><td>URL the proxy used to forward the request upstream.</td></tr>
        <tr><td>22</td><td><code>errorKey</code></td><td>Error key, if the policy chain was interrupted by an error.</td></tr>
        <tr><td>23</td><td><code>errorMessage</code></td><td>Detailed explanation of the error.</td></tr>
        <tr><td>24</td><td><code>userAgent</code></td><td><code>User-Agent</code> header from the client request.</td></tr>
        <tr><td>25</td><td><code>host</code></td><td><code>Host</code> header from the client request.</td></tr>
        <tr><td>26</td><td><code>requestContentLength</code></td><td>Size in bytes of the incoming request body. <code>-1</code> if unknown.</td></tr>
        <tr><td>27</td><td><code>responseContentLength</code></td><td>Size in bytes of the response body returned to the client.</td></tr>
        <tr><td>28</td><td><code>endpointResponseTimeMs</code></td><td>Time (ms) for the upstream service to respond to the gateway.</td></tr>
        <tr><td>29</td><td><code>gatewayResponseTimeMs</code></td><td>Time (ms) for the gateway to respond to the client (includes upstream roundtrip).</td></tr>
        <tr><td>30</td><td><code>gatewayLatencyMs</code></td><td>Overhead added by the gateway when forwarding the request and response.</td></tr>
        <tr><td>31</td><td><code>securityType</code></td><td>Security type used (<code>API_KEY</code>, <code>OAUTH2</code>, <code>JWT</code>).</td></tr>
        <tr><td>32</td><td><code>securityToken</code></td><td>Security token, if security was used.</td></tr>
    </tbody>
</table>
{% endcode %}

{% code title="Reactive engine — sample" %}
```csv
"076aea69-6024-4590-aaea-6960247590a0";"076aea69-6024-4590-aaea-6960247590a0";1692359213844;"127.0.0.1";"127.0.0.1";"5f67b38f-0700-4557-a7b3-8f0700855779";"echo-api";"DEFAULT";"DEFAULT";"91f077b0-1204-49e4-b077-b0120419e4f6";"8463511c-fbed-4ca9-a351-1cfbed9ca99d";"318e47e5-349c-4fa4-8e47-e5349c3fa444";"";"";"/test-v4";"";"";"GET";200;"http-proxy";"https://api.gravitee.io/echo";"";"";"curl/7.88.1";"localhost:8082";-1;274;137;144;7;"";""
```
{% endcode %}

{% code title="Legacy engine — column reference" %}
<table>
    <thead>
        <tr>
            <th width="80">Position</th>
            <th width="220">Column</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>1</td><td><code>transactionId</code></td><td>End-to-end transaction ID. Falls back to <code>requestId</code> if no correlation header is set.</td></tr>
        <tr><td>2</td><td><code>requestId</code></td><td>Unique UUID identifying the request.</td></tr>
        <tr><td>3</td><td><code>timestamp</code></td><td>Request timestamp in milliseconds since epoch.</td></tr>
        <tr><td>4</td><td><code>remoteAddress</code></td><td>Source address of the incoming request.</td></tr>
        <tr><td>5</td><td><code>localAddress</code></td><td>Destination address the incoming request was issued to.</td></tr>
        <tr><td>6</td><td><code>api</code></td><td>ID of the API.</td></tr>
        <tr><td>7</td><td><code>apiName</code></td><td>Name of the API at the time of the request.</td></tr>
        <tr><td>8</td><td><code>organizationId</code></td><td>ID of the organization the API belongs to.</td></tr>
        <tr><td>9</td><td><code>environmentId</code></td><td>ID of the environment the API belongs to.</td></tr>
        <tr><td>10</td><td><code>application</code></td><td>Application ID. <code>"1"</code> for keyless plans.</td></tr>
        <tr><td>11</td><td><code>plan</code></td><td>ID of the plan.</td></tr>
        <tr><td>12</td><td><code>subscription</code></td><td>Subscription ID. Empty for keyless plans.</td></tr>
        <tr><td>13</td><td><code>user</code></td><td>Authenticated user, if security was used.</td></tr>
        <tr><td>14</td><td><code>tenant</code></td><td>Tenant evaluated for the API.</td></tr>
        <tr><td>15</td><td><code>uri</code></td><td>URI used by the client (includes context path and query string).</td></tr>
        <tr><td>16</td><td><code>path</code></td><td>Path portion after the API context path.</td></tr>
        <tr><td>17</td><td><code>mappedPath</code></td><td>Path mapping value, if a path mapping is configured.</td></tr>
        <tr><td>18</td><td><code>httpMethod</code></td><td>HTTP method of the client request.</td></tr>
        <tr><td>19</td><td><code>status</code></td><td>HTTP response status code returned to the client.</td></tr>
        <tr><td>20</td><td><code>endpoint</code></td><td>URL the proxy used to forward the request upstream.</td></tr>
        <tr><td>21</td><td><code>errorKey</code></td><td>Error key, if the policy chain was interrupted by an error.</td></tr>
        <tr><td>22</td><td><code>message</code></td><td>Detailed explanation of the error.</td></tr>
        <tr><td>23</td><td><code>userAgent</code></td><td><code>User-Agent</code> header from the client request.</td></tr>
        <tr><td>24</td><td><code>host</code></td><td><code>Host</code> header from the client request.</td></tr>
        <tr><td>25</td><td><code>requestContentLength</code></td><td>Size in bytes of the incoming request body.</td></tr>
        <tr><td>26</td><td><code>responseContentLength</code></td><td>Size in bytes of the response body returned to the client.</td></tr>
        <tr><td>27</td><td><code>apiResponseTimeMs</code></td><td>Time (ms) for the upstream service to respond to the gateway.</td></tr>
        <tr><td>28</td><td><code>proxyResponseTimeMs</code></td><td>Time (ms) for the gateway to respond to the client (includes upstream roundtrip).</td></tr>
        <tr><td>29</td><td><code>proxyLatencyMs</code></td><td>Overhead added by the gateway when forwarding the request and response.</td></tr>
        <tr><td>30</td><td><code>securityType</code></td><td>Security type used (<code>API_KEY</code>, <code>OAUTH2</code>, <code>JWT</code>).</td></tr>
        <tr><td>31</td><td><code>securityToken</code></td><td>Security token, if security was used.</td></tr>
    </tbody>
</table>
{% endcode %}

{% code title="Legacy engine — sample" %}
```csv
"13f5ae30-068b-4e2d-b5ae-30068bae2d2d";"13f5ae30-068b-4e2d-b5ae-30068bae2d2d";1692357381941;"127.0.0.1";"127.0.0.1";"ff3c6c48-53e0-41d6-bc6c-4853e011d656";"echo-api";"DEFAULT";"DEFAULT";"91f077b0-1204-49e4-b077-b0120419e4f6";"e115ea63-7cef-4646-95ea-637cef7646ec";"04975880-f147-43bc-9758-80f147e3bcbb";"";"";"/test";"";"";"GET";200;"https://api.gravitee.io/echo";"";"";"curl/7.88.1";"localhost:8082";0;275;144;150;6;"API_KEY";"ff3c6c48-53e0-41d6-bc6c-4853e011d656"
```
{% endcode %}
{% endtab %}

{% tab title="Elasticsearch" %}
When using e.g. the File Reporter with Elasticsearch format, here is a sample of the contents of `metrics.json`:

{% code title="Reactive engine" %}
```json
{
  "type": "v4-metrics",
  "date": "2023.08.18",
  "_id": "076aea69-6024-4590-aaea-6960247590a0",
  "gateway": "gateway-id",
  "@timestamp": "2023-08-18T11:46:53.844Z",
  "request-id": "076aea69-6024-4590-aaea-6960247590a0",
  "client-identifier": "318e47e5-349c-4fa4-8e47-e5349c3fa444",
  "transaction-id": "076aea69-6024-4590-aaea-6960247590a0",
  "api-id": "5f67b38f-0700-4557-a7b3-8f0700855779",
  "plan-id": "8463511c-fbed-4ca9-a351-1cfbed9ca99d",
  "application-id": "91f077b0-1204-49e4-b077-b0120419e4f6",
  "subscription-id": "318e47e5-349c-4fa4-8e47-e5349c3fa444",
  "http-method": 3,
  "local-address": "127.0.0.1",
  "remote-address": "127.0.0.1",
  "host": "localhost:8082",
  "uri": "/test-v4",
  "path-info": "",
  "user-agent": "",
  "request-ended": "true",
  "endpoint": "https://api.gravitee.io/echo",
  "endpoint-response-time-ms": 137,
  "status": 200,
  "response-content-length": 274,
  "gateway-response-time-ms": 144,
  "gateway-latency-ms": 7
}
```
{% endcode %}

{% code title="Legacy engine" %}
```json
{
  "gateway": "gateway-id",
  "@timestamp": "2023-08-18T11:16:21.941Z",
  "type": "request",
  "date": "2023.08.18",
  "_id": "13f5ae30-068b-4e2d-b5ae-30068bae2d2d",
  "transaction": "13f5ae30-068b-4e2d-b5ae-30068bae2d2d",
  "method": 3,
  "uri": "/test",
  "status": 200,
  "response-time": 150,
  "api-response-time": 144,
  "proxy-latency": 6,
  "request-content-length": 0,
  "response-content-length": 275,
  "plan": "e115ea63-7cef-4646-95ea-637cef7646ec",
  "api": "ff3c6c48-53e0-41d6-bc6c-4853e011d656",
  "application": "91f077b0-1204-49e4-b077-b0120419e4f6",
  "local-address": "127.0.0.1",
  "remote-address": "127.0.0.1",
  "endpoint": "https://api.gravitee.io/echo",
  "path": "",
  "host": "localhost:8082",
  "user-agent": "",
  "security-type": "API_KEY",
  "security-token": "21b560b2-59b8-4a4b-921a-32b3731fdec4",
  "subscription": "04975880-f147-43bc-9758-80f147e3bcbb",
  "custom": {
    "zone": "europe-north1-a"
  }
}
```
{% endcode %}
{% endtab %}
{% endtabs %}

## Configuring Reporters & Selecting Fields

The reporters are configured in the `gravitee.yml`configuration file for the **gateway**. Each reporter has its own unique configuration. Consult the documentation for each reporter for details on how to configure it. Elasticsearch is used by default.

{% hint style="info" %}
If you wish to use a reporter not included in the default distribution, you must first add the reporter as a plugin. Refer to the [Plugins](../../plugins/) guide to learn more.
{% endhint %}

Each reporter has a section for configuring field exclusions and, depending on reporter type, field inclusion. Each log and metric section above has a naming convention for how it appears in field inclusion and exclusion lists, which is as follows:

| Name               | Purpose                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| request            | Metrics for v2 APIs                                                                            |
| node               | Monitoring metrics for the gateway                                                             |
| health-check       | Health check logs for all API types                                                            |
| log                | Logs for v2 APIs                                                                               |
| v4-log             | Logs for v4 APIs                                                                               |
| v4-metrics         | Metrics for v4 API at the request level for requests proxied through the gateway               |
| v4-message-metrics | Metrics at the message level, driven off of sampling and the logging configuration for the API |
| v4-message-log     | Logging at the message level captured for v4 message APIs                                      |

You can exclude, include, or rename various metrics based on the reporter type. See the docs for each reporter for details. For example, with the file reporter you can configure the following:

```yaml
  file:
    enabled: true
    fileName: ${gravitee.home}/metrics/%s-yyyy_mm_dd
    output: json # Can be csv, json, elasticsearch or message_pack
    request:
      exclude:
        - responseTime
      include: # Only if exclude is used (supports json path)
        - api
      rename: # (supports json path)
        application: app
        request.ip: address
```
