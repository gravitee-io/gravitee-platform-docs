# Reporters

## Overview

Reporters are designed to record a variety of events occurring in the Gravitee API Management (APIM) Gateway and output them to a new source in their order of occurrence. Reporters take the **application** **data** from the Gravitee gateway, capturing metrics and logs about proxied requests, and offload them to a system of your choice. Reporters are a critical part of creating a production-grade monitoring system for your API traffic in Gravitee.

ElasticSearch is the default reporter for gateway runtime data and is required for visualizing runtime analytics in the Gravitee UI. You can also use reporters to feed other visualization tools, e.g. for those based on Elastic (Kibana), or for systems like Grafana and Datadog.

{% hint style="info" %}
If you want to monitor the **server** logs from the gateway or the management API, you can use an agent for your observability platform (e.g. the [Datadog agent](https://docs.datadoghq.com/agent/?tab=Linux)) to tail the server logs. If you want to monitor the server metrics from your Gravitee infrastructure (e.g. CPU and memory usage), you can instrument the server directly or use the Prometheus endpoint for the Gravitee component.
{% endhint %}

You can configure various aspects of reporters, such as reporting monitoring data, request metrics, and health checks. All reporters are enabled by default. To stop a reporter, you need to add the property `enabled: false`:

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

This page documents the available reporters and the metrics and logs captured by each reporter, in a generic format. The configuration for each reporter and the format of the metrics in those reporting systems are covered in their own pages.

{% hint style="warning" %}
Configuration details for the Elasticsearch reporter are available in the [Elasticsearch Repository](../../configure-apim/repositories/#elasticsearch) documentation.
{% endhint %}

## Available Reporters

The following reporters are currently compatible with APIM:

<table><thead><tr><th width="151">Type</th><th data-type="checkbox">Bundled in Distribution</th><th data-type="checkbox">Default</th><th data-type="checkbox">Enterprise only</th></tr></thead><tbody><tr><td>Elasticsearch</td><td>true</td><td>true</td><td>false</td></tr><tr><td>File</td><td>true</td><td>false</td><td>false</td></tr><tr><td>TCP</td><td>true</td><td>false</td><td>true</td></tr><tr><td>Datadog</td><td>false</td><td>false</td><td>true</td></tr></tbody></table>

{% hint style="warning" %}
To learn more about Gravitee [Enterprise Edition](../../overview/enterprise-edition.md) and what's included in various enterprise packages, please:

* [Book a demo](https://app.gitbook.com/o/8qli0UVuPJ39JJdq9ebZ/s/rYZ7tzkLjFVST6ex6Jid/)
* [Check out the pricing page](https://www.gravitee.io/pricing)
{% endhint %}

## Metrics Sent via Reporters

By default, reporters generate the following data, with the camelCase format shown generically. Each reporter type converts the naming convention from camelCase to the format required by that system. The metrics are different between Gravitee v2 and v4 APIs, and v4 metrics are further broken down by request-level metrics and message-level metrics.

{% tabs %}
{% tab title="v4 Metrics" %}
<table><thead><tr><th width="349">Metric Name</th><th>Purpose</th></tr></thead><tbody><tr><td>requestId</td><td>Unique identifier Universally Unique Identifier (UUID) identifying the request</td></tr><tr><td>transactionId</td><td>Used to track end-to-end transactions spanning across multiple HTTP requests. The Gateway configuration allows defining an expected correlation ID header passed by a client request. If this header is set, the content of this field will be set to the value of the header. If no correlation header has been passed, the content of this field will be the same as the content of the request ID. This value will be propagated to the upstream service using the correlation header defined in the configuration (the default header is <code>X-Gravitee-Transaction-Id</code>).</td></tr><tr><td>apiId</td><td>ID of the API</td></tr><tr><td>apiName</td><td>Name of the API at the time of the request</td></tr><tr><td>apiType</td><td>Type of the API (message, proxy)</td></tr><tr><td>planId</td><td>ID of the plan</td></tr><tr><td>applicationId</td><td>The application ID; for a keyless plan, this value is "1"</td></tr><tr><td>subscriptionId</td><td>The subscription ID; for a keyless plan, this value will be the same as the value of the remote address field</td></tr><tr><td>clientIdentifier</td><td>Unique identifier for the client</td></tr><tr><td>tenant</td><td>ID of the tenant evaluated for the API (see <a href="../tenants.md">tenants</a>)</td></tr><tr><td>zone</td><td>Text field set in gravitee.yml to indicate additional information about the gateway instance the API is running on</td></tr><tr><td>httpMethod</td><td>HTTP verb used in the client connection</td></tr><tr><td>localAddress</td><td>The address used as a destination when the incoming request was issued by the client</td></tr><tr><td>remoteAddress</td><td>The remote address used as a source when the incoming request was issued by the client</td></tr><tr><td>host</td><td>The content of the <code>Host</code> header, passed when the incoming request was issued by the client</td></tr><tr><td>uri</td><td>The URI used by the client to perform its request (this includes the context path of the request and query parameters)</td></tr><tr><td>pathInfo</td><td>The path used to perform the client request (starting from the context path of the API)</td></tr><tr><td>mappedPath</td><td>If a path mapping has been defined to group requests in your analytics, this is the value of your mapping.</td></tr><tr><td>userAgent</td><td>The content of the <code>User-Agent</code> header, passed by the client when the incoming request was issued</td></tr><tr><td>requestContentLength</td><td>The size of the body, in bytes, of the incoming request issued by the Gateway client</td></tr><tr><td>requestEnded</td><td>Boolean to indicate if the request has completed; request may be ongoing if the connection is over Websocket or SSE</td></tr><tr><td>entrypointId</td><td>ID of the entrypoint used in the API connection</td></tr><tr><td>endpoint</td><td>The URL used by the proxy to forward the request to the upstream service</td></tr><tr><td>endpointResponseTimeMs</td><td>The time (ms) it takes the upstream service to respond to the Gateway proxy</td></tr><tr><td>responseContentLength</td><td>The size of the body, in bytes, of the response received by the Gateway client</td></tr><tr><td>gatewayResponseTimeMs</td><td>The time (ms) it takes the Gateway to respond to the client (this includes the roundtrip between the Gateway and the upstream service)</td></tr><tr><td>gatewayLatencyMs</td><td>The overhead added by the Gateway when forwarding the request upstream and the response back to the client</td></tr><tr><td>user</td><td>The authenticated user, if any type of security was used when processing the request</td></tr><tr><td>securityType</td><td>The security type, if security was used when processing the request (can be either API_KEY, OAUTH2 or JWT)</td></tr><tr><td>securityToken</td><td>The security token, if any type of security was used when processing the request</td></tr><tr><td>errorMessage</td><td>A more detailed explanation of the error associated with the error key (if any)</td></tr><tr><td>errorKey</td><td>If the policy chain was interrupted by an error, this key identifies the error type</td></tr></tbody></table>
{% endtab %}

{% tab title="v4 Message Metrics" %}
| Metric Name         | Purpose                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| requestId           | ID of the request                                                                                 |
| apiId               | ID of the API                                                                                     |
| apiName             | Name of the API at the time of the request                                                        |
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
<table><thead><tr><th width="349">Metric Name</th><th>Purpose</th></tr></thead><tbody><tr><td>timestamp</td><td>The timestamp of the transaction in milliseconds</td></tr><tr><td>proxyResponseTimeMs</td><td>The time (ms) it takes the Gateway to respond to the client (this includes the roundtrip between the Gateway and the upstream service)</td></tr><tr><td>proxyLatencyMs</td><td>The overhead added by the Gateway when forwarding the request upstream and the response back to the client</td></tr><tr><td>apiResponseTimeMs</td><td>The time (ms) it takes the upstream service to respond to the Gateway proxy</td></tr><tr><td>requestId</td><td>Unique identifier Universally Unique Identifier (UUID) identifying the request</td></tr><tr><td>api</td><td>ID of the API</td></tr><tr><td>apiName</td><td>Name of the API at the time of the request</td></tr><tr><td>application</td><td>The application ID; for a keyless plan, this value is "1"</td></tr><tr><td>transactionId</td><td>Used to track end-to-end transactions spanning across multiple HTTP requests. The Gateway configuration allows defining an expected correlation ID header passed by a client request. If this header is set, the content of this field will be set to the value of the header. If no correlation header has been passed, the content of this field will be the same as the content of the request ID. This value will be propagated to the upstream service using the correlation header defined in the configuration (the default header is <code>X-Gravitee-Transaction-Id</code>).</td></tr><tr><td>clientIdentifier</td><td>Unique identifier for the client</td></tr><tr><td>tenant</td><td>ID of the tenant evaluated for the API (see <a href="../tenants.md">tenants</a>)</td></tr><tr><td>message</td><td>A detailed explanation of the error associated with the error key (if any)</td></tr><tr><td>plan</td><td>ID of the plan</td></tr><tr><td>localAddress</td><td>The address used as a destination when the incoming request was issued by the client</td></tr><tr><td>remoteAddress</td><td>The remote address used as a source when the incoming request was issued by the client</td></tr><tr><td>httpMethod</td><td>HTTP verb used in the client connection</td></tr><tr><td>host</td><td>The content of the <code>Host</code> header, passed when the incoming request was issued by the client</td></tr><tr><td>uri</td><td>The URI used by the client to perform its request (this includes the context path of the request and query parameters)</td></tr><tr><td>requestContentLength</td><td>The size of the body, in bytes, of the response received by the Gateway client</td></tr><tr><td>responseContentLength</td><td>The size of the body, in bytes, of the response received by the Gateway client</td></tr><tr><td>status</td><td>HTTP response status code integer</td></tr><tr><td>endpoint</td><td>The URL used by the proxy to forward the request to the upstream service</td></tr><tr><td>path</td><td>The path used to perform the client request (starting from the context path of the API)</td></tr><tr><td>mappedPath</td><td>If a path mapping has been defined to group requests in your analytics, this is the value of your mapping.</td></tr><tr><td>userAgent</td><td>The content of the <code>User-Agent</code> header, passed by the client when the incoming request was issued</td></tr><tr><td>user</td><td>The authenticated user, if any type of security was used when processing the request</td></tr><tr><td>securityType</td><td>The security type, if security was used when processing the request (can be either API_KEY, OAUTH2 or JWT)</td></tr><tr><td>securityToken</td><td>The security token, if any type of security was used when processing the request</td></tr><tr><td>errorKey</td><td>If the policy chain was interrupted by an error, this key identifies the error type</td></tr><tr><td>subscription</td><td>The subscription ID; for a keyless plan, this value will be the same as the value of the remote address field</td></tr><tr><td>zone</td><td>Text field set in gravitee.yml to indicate additional information about the gateway instance the API is running on</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Log Data Sent via Reporters

In addition to metrics, the gateway can send additional log messages about API execution to the target reporting system. The content of the logs depends on how [logging is configured](../logging.md) for the API, and whether the API is a v2 or v4 API. There are also separate log messages generated for v4 request and response phases as well as message-level logging (which uses sampling). The contents of the logs are as follows:

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
  "apiType": "proxy",
  "planId": "8463511c-fbed-4ca9-a351-1cfbed9ca99d",
  "applicationId": "91f077b0-1204-49e4-b077-b0120419e4f6",
  "subscriptionId": "318e47e5-349c-4fa4-8e47-e5349c3fa444",
  "clientIdentifier": "318e47e5-349c-4fa4-8e47-e5349c3fa444",
  "httpMethod": "GET",
  "localAddress": "127.0.0.1",
  "remoteAddress": "127.0.0.1",
  "host": "localhost:8082",
  "uri": "/test-v4",
  "pathInfo": "",
  "userAgent": "curl/7.88.1",
  "requestContentLength": -1,
  "requestEnded": true,
  "endpoint": "https://api.gravitee.io/echo",
  "endpointResponseTimeMs": 137,
  "status": 200,
  "responseContentLength": 274,
  "gatewayResponseTimeMs": 144,
  "gatewayLatencyMs": 7
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
  "application": "91f077b0-1204-49e4-b077-b0120419e4f6",
  "transactionId": "13f5ae30-068b-4e2d-b5ae-30068bae2d2d",
  "plan": "e115ea63-7cef-4646-95ea-637cef7646ec",
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
When using e.g. the File Reporter with CSV format, here is a sample of the contents of `metrics.csv`:

{% code title="Reactive engine" %}
```csv
"076aea69-6024-4590-aaea-6960247590a0";
"076aea69-6024-4590-aaea-6960247590a0";
1692359213844;
"127.0.0.1";
"127.0.0.1";
"5f67b38f-0700-4557-a7b3-8f0700855779";
"91f077b0-1204-49e4-b077-b0120419e4f6";
"8463511c-fbed-4ca9-a351-1cfbed9ca99d";
"318e47e5-349c-4fa4-8e47-e5349c3fa444";
"";
"";
"/test-v4";
"";
"";
"GET";
200;
"https://api.gravitee.io/echo";
"";
"";
"curl/7.88.1";
"localhost:8082";
-1;
274;
137;
144;
7;
"";
""

```
{% endcode %}

{% code title="Legacy engine" %}
```csv
"13f5ae30-068b-4e2d-b5ae-30068bae2d2d";
"13f5ae30-068b-4e2d-b5ae-30068bae2d2d";
1692357381941;
"127.0.0.1";
"127.0.0.1";
"ff3c6c48-53e0-41d6-bc6c-4853e011d656";
"91f077b0-1204-49e4-b077-b0120419e4f6";
"e115ea63-7cef-4646-95ea-637cef7646ec";
"04975880-f147-43bc-9758-80f147e3bcbb";
"";
"";
"/test";
"";
"";
"GET";
200;
"https://api.gravitee.io/echo";
"";
"";
"curl/7.88.1";
"localhost:8082";
0;
275;
144;
150;
6;
"API_KEY";
"ff3c6c48-53e0-41d6-bc6c-4853e011d656";
"europe-north1-a"
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
If you wish to use a reporter not included in the default distribution, you must first add the reporter as a plugin. Refer to the [Plugins](../../getting-started/plugins/) guide to learn more.
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
