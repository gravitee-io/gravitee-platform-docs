---
description: >-
  This page details the types and organization of information recorded by
  Gravitee reporters
---

# Formats

## Supported formats

The same payload can be sent to any of the Gravitee reporters to write the record of events to a particular output. Payload data can be converted to JSON, CSV, or Elasticsearch format, depending on the reporter type:

<table><thead><tr><th width="192">Reporter</th><th data-type="checkbox">JSON</th><th data-type="checkbox">CSV</th><th data-type="checkbox">Elasticsearch</th></tr></thead><tbody><tr><td>Elasticsearch</td><td>false</td><td>false</td><td>true</td></tr><tr><td>File</td><td>true</td><td>true</td><td>true</td></tr><tr><td>TCP</td><td>true</td><td>true</td><td>true</td></tr><tr><td>Datadog</td><td>false</td><td>false</td><td>false</td></tr></tbody></table>

## Expected output

Each reporter writes particular payload data to files that share a common naming convention and structure, regardless of output format. JSON, CSV, and Elasticsearch formats each generate the following files, which pertain to different [Gravitee execution engines](../../../overview/gravitee-api-definitions-and-execution-engines/README.md):

{% tabs %}
{% tab title="Common" %}
The following file is common to both the legacy and reactive execution engines:

<table><thead><tr><th width="205.66666666666666">File name</th><th>Description</th></tr></thead><tbody><tr><td><code>monitor.json</code><br>(or <code>monitor.csv</code>)</td><td>Reports the state of a Gravitee node (Gateway, APIM)</td></tr></tbody></table>
{% endtab %}

{% tab title="Legacy" %}
The following files pertain to the legacy execution engine only:

<table><thead><tr><th width="277.66666666666663">File name</th><th>Description</th></tr></thead><tbody><tr><td><code>endpoint-status.json</code><br>(or <code>endpoint-status.csv</code>)</td><td>Pushed as the result of an API healthcheck </td></tr><tr><td><code>metrics.json</code><br>(or <code>metrics.csv</code>)</td><td>Common metrics related to a specific HTTP request</td></tr><tr><td><code>log.json</code><br>(or <code>log.csv</code>)</td><td>An in-depth report of an HTTP request, where the body can be appended to the data structure. This file content is configured from the UI (in the logs => configure logging section).</td></tr></tbody></table>
{% endtab %}

{% tab title="Reactive" %}
The following files pertain to the reactive execution engine only:

<table><thead><tr><th width="271.66666666666663">File name</th><th>Description</th></tr></thead><tbody><tr><td><code>metrics.json</code> <br>(or <code>metrics.csv</code>)</td><td>Common metrics related to a specific HTTP request</td></tr><tr><td><code>log.json</code> <br>(or <code>log.csv</code>)</td><td>An in-depth report of an HTTP request, where the body can be appended to the data structure. This file content is configured from the UI (in the logs => configure logging section).</td></tr><tr><td><code>message-metrics.json</code><br>(or <code>message-metrics.csv</code>)</td><td>Same as <code>metrics.json</code> but for an event-driven API</td></tr><tr><td><code>message-log.json</code> <br>(or <code>message-log.csv</code>)</td><td>Same as <code>log.json</code> but for an event-driven API</td></tr></tbody></table>
{% endtab %}
{% endtabs %}

## Metrics

The metrics recorded for a given payload are similar for all reporters and formats. Below are the metrics for a sample payload in JSON, CSV, and Elasticsearch formats:

{% tabs %}
{% tab title="JSON" %}
Sample contents of `metrics.json`:&#x20;

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
Sample contents of `metrics.csv`:

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
Sample contents of `metrics.json`:

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

Depending on which execution engine is used, equivalent fields observe slightly different naming conventions. The number of fields also differs slightly due to differences in execution engine.

### Field definitions

The following table maps field names between JSON and Elasticsearch formats and provides a description for each.&#x20;

Naming conventions are consistent within a certain format. Although there is significant overlap, the specific fields that are generated depend on which execution engine and format are used. The table below compares data recorded with the reactive engine.

<table><thead><tr><th width="210">JSON</th><th>Elasticsearch</th><th>Description</th></tr></thead><tbody><tr><td><code>timestamp</code></td><td><code>@timestamp</code></td><td>The timestamp of the transaction in milliseconds. Elasticsearch formats the <code>@timestamp</code> field as an ISO 8601 string.</td></tr><tr><td></td><td><code>date</code></td><td>This field is only added if the Elasticsearch format is used with the TCP or file reporter. It enables building the index name in your ingest pipeline (e.g., when using Logstash).</td></tr><tr><td></td><td><code>type</code></td><td>This field is only added if the Elasticsearch format is used with the TCP or file reporter. It enables building the index name in your ingest pipeline (e.g., when using Logstash).</td></tr><tr><td><code>requestID</code></td><td><code>request-id</code></td><td>Universally Unique Identifier (UUID) identifying the request. </td></tr><tr><td></td><td><code>_id</code></td><td>If you are using Elasticsearch format, the content of the  <code>_id</code> and <code>request-id</code> fields will be identical.</td></tr><tr><td><code>transactionID</code></td><td><code>transaction-id</code></td><td>This ID can be used to track end-to-end transactions spanning across multiple HTTP requests. The Gateway configuration allows defining an expected correlation ID header passed by a client request. If this header is set, the content of this field will be set to the value of the header. If no correlation header has been passed, the content of this field will be the same as the content of the request ID. This value will be propagated to the upstream service using the correlation header defined in the configuration (the default header is <code>X-Gravitee-Transaction-Id</code>).</td></tr><tr><td><code>apiID</code></td><td><code>api-id</code></td><td>The API ID.</td></tr><tr><td><code>apiType</code></td><td><code>type</code></td><td>The API type (can be either "proxy" or "message").</td></tr><tr><td><code>planID</code></td><td><code>plan-id</code></td><td>The plan ID.</td></tr><tr><td><code>applicationID</code></td><td><code>application-id</code></td><td>The application ID. For a keyless plan, this value is "1".</td></tr><tr><td><code>subscriptionID</code></td><td><code>subscription-id</code></td><td>The subscription ID. For a keyless plan, this value will be the same as the value of the remote address field.</td></tr><tr><td><code>user</code></td><td><code>user</code></td><td>The authenticated user, if any type of security was used when processing the request.</td></tr><tr><td><code>securityType</code></td><td><code>security-type</code></td><td>The security type, if security was used when processing the request (can be either API_KEY, OAUTH2 or JWT).</td></tr><tr><td><code>securityToken</code></td><td><code>security-token</code></td><td>The security token, if any type of security was used when processing the request.</td></tr><tr><td><code>clientIdentifier</code></td><td><code>client-identifier</code></td><td>This field identifies the client of the request. It is either the subscription ID (if any) or, for a keyless plan, a hash of the remote address. The <code>Client-Identifier</code> can be provided by the client using the header <code>X-Gravitee-Client-Identifier</code>; in this case, the value used by Gravitee will be the original inferred value suffixed with the overridden value.</td></tr><tr><td><code>httpMethod</code></td><td><code>http-method</code></td><td>The HTTP method used to perform the client request.</td></tr><tr><td><code>localAddress</code></td><td><code>local-address</code></td><td>The address used as a destination when the incoming request was issued by the client.</td></tr><tr><td><code>remoteAddress</code></td><td><code>remote-address</code></td><td>The remote address used as a source when the incoming request was issued by the client.</td></tr><tr><td><code>host</code></td><td><code>host</code></td><td>The content of the <code>Host</code> header, passed when the incoming request was issued by the client.</td></tr><tr><td><code>uri</code></td><td><code>uri</code></td><td>The URI used by the client to perform its request (this includes the context path of the request and query parameters).</td></tr><tr><td><code>path-info</code></td><td><code>path-info</code></td><td>The path used to perform the client request (starting from the context path of the API).</td></tr><tr><td><code>mappedPath</code></td><td><code>mapped-path</code></td><td>If a path mapping has been defined to group requests in your analytics, this is the value of your mapping.</td></tr><tr><td><code>userAgent</code></td><td><code>user-agent</code></td><td>The content of the <code>User-Agent</code> header, passed by the client when the incoming request was issued.</td></tr><tr><td><code>requestContentLength</code></td><td></td><td>The size of the body, in bytes, of the incoming request issued by the Gateway client.</td></tr><tr><td><code>requestEnded</code></td><td><code>request-ended</code></td><td>Flag to indicate if the request completed.</td></tr><tr><td><code>endpoint</code></td><td><code>endpoint</code></td><td>The URL used by the proxy to forward the request to the upstream service.</td></tr><tr><td><code>endpointResponseTimeMs</code></td><td><code>endpoint-response-time-ms</code></td><td>The time (ms) it takes the upstream service to respond to the Gateway proxy.</td></tr><tr><td><code>status</code></td><td><code>status</code></td><td>The HTTP status code of the transaction.</td></tr><tr><td><code>responseContentLength</code></td><td><code>response-content-length</code></td><td>The size of the body, in bytes, of the response received by the Gateway client.</td></tr><tr><td><code>gatewayResponseTimeMs</code></td><td><code>gateway-response-time-ms</code></td><td>The time (ms) it takes the Gateway to respond to the client (this includes the roundtrip between the Gateway and the upstream service).</td></tr><tr><td><code>gatewayLatencyMs</code></td><td><code>gateway-latency-ms</code></td><td>The overhead added by the Gateway when forwarding the request upstream and the response back to the client.</td></tr><tr><td></td><td><code>gateway</code></td><td>A UUID identifying the Gateway instance handling the request.</td></tr><tr><td><code>errorKey</code></td><td><code>error-key</code></td><td>If the policy chain was interrupted by an error, this key identifies the error type.</td></tr><tr><td><code>errorMessage</code></td><td><code>error-message</code></td><td>A more detailed explanation of the error associated with the error key (if any).</td></tr><tr><td><code>custom</code></td><td><code>custom</code></td><td>Custom metrics defined via the <code>assign-metrics</code> policy will be added to this dictionary.</td></tr></tbody></table>

### CSV format

Files formatted as CSV do not include a key. Use the following table to map the offset of metrics data recorded with the reactive engine to the corresponding field:

<table><thead><tr><th width="110">Offset</th><th width="253">Field</th><th>Sample value</th></tr></thead><tbody><tr><td>0</td><td><code>transactionID</code></td><td>076aea69-6024-4590-aaea-6960247590a0</td></tr><tr><td>1</td><td><code>requestID</code></td><td>076aea69-6024-4590-aaea-6960247590a0</td></tr><tr><td>2</td><td><code>timestamp</code></td><td>1692359213844</td></tr><tr><td>3</td><td><code>remoteAddress</code></td><td>127.0.0.1</td></tr><tr><td>4</td><td><code>localAddress</code></td><td>127.0.0.1</td></tr><tr><td>5</td><td><code>apiID</code></td><td>5f67b38f-0700-4557-a7b3-8f0700855779</td></tr><tr><td>6</td><td><code>applicationID</code></td><td>91f077b0-1204-49e4-b077-b0120419e4f6</td></tr><tr><td>7</td><td><code>planID</code></td><td>8463511c-fbed-4ca9-a351-1cfbed9ca99d</td></tr><tr><td>8</td><td><code>subscriptionID</code></td><td>318e47e5-349c-4fa4-8e47-e5349c3fa444</td></tr><tr><td>9</td><td><code>user</code></td><td>5f2dd42f-610b-4719-ae39-8ccf7243047e</td></tr><tr><td>10</td><td><code>tenant</code></td><td></td></tr><tr><td>11</td><td><code>uri</code></td><td>/test-v4</td></tr><tr><td>12</td><td><code>path</code></td><td>/</td></tr><tr><td>13</td><td><code>mappedPath</code></td><td>/:anyPath</td></tr><tr><td>14</td><td><code>httpMethod</code></td><td>GET</td></tr><tr><td>15</td><td><code>status</code></td><td>200</td></tr><tr><td>16</td><td><code>endpoint</code></td><td>https://api.gravitee.io/echo</td></tr><tr><td>17</td><td><code>errorKey</code></td><td>GATEWAY_OAUTH2_ACCESS_DENIED</td></tr><tr><td>18</td><td><code>errorMessage</code></td><td></td></tr><tr><td>19</td><td><code>userAgent</code></td><td>curl/7.88.1</td></tr><tr><td>20</td><td><code>host</code></td><td>api.example.com</td></tr><tr><td>21</td><td><code>requestContent</code></td><td>-1</td></tr><tr><td>22</td><td><code>responseContent</code></td><td>274</td></tr><tr><td>23</td><td><code>endpointResponseTimeMs</code></td><td>137</td></tr><tr><td>24</td><td><code>gatewayResponseTimeMs</code></td><td>144</td></tr><tr><td>25</td><td><code>gatewayLatencyMs</code></td><td>7</td></tr><tr><td>26</td><td><code>securityType</code></td><td>OAUTH2</td></tr><tr><td>27</td><td><code>securityToken</code></td><td>6d8772c9-3336-4ede-8ffd-4852cfb85f95</td></tr><tr><td>28</td><td><code>customMetrics[0]</code></td><td></td></tr></tbody></table>
