---
description: An overview about metrics reporter.
metaLinks:
  alternates:
    - >-
      https://app.gitbook.com/s/bGmDEarvnV52XdcOiV8o/create-and-configure-apis/apply-policies/policy-reference/metrics-reporter
---

# Metrics Reporter

## Overview

The `metrics-reporter` policy allows you to push the request metrics to a custom endpoint. Running this policy ensures that the complete response has already been sent to the initial consumer.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs. It cannot be applied to v4 proxy APIs or v4 message APIs.
{% endhint %}

{% tabs %}
{% tab title="v2 API example" %}
```json
"metrics-reporter": {
	"method":"POST",
	"url":"https://my_custom_endpoint/report",
	"body":"{\n\t\"requestId\": \"${request.requestId}\",\n\t\"transactionId\": \"${request.transactionId}\",\n\t\"headers\": \"${request.headers}\",\n\t\"params\": \"${request.params}\",\n\t\"method\": \"${request.method}\",\n\t\"uri\": \"${request.uri}\",\n\t\"path\": \"${request.path}\",\n\t\"scheme\": \"${request.scheme}\",\n\t\"localAddress\": \"${request.localAddress}\",\n\t\"remoteAddress\": \"${request.remoteAddress}\",\n\t\"contentLength\": ${request.contentLength},\n\t\"statusCode\": ${response.statusCode},\n\t\"statusReason\": \"${response.statusReason}\",\n\t\"headers\": \"${response.headers}\",\n\t\"contentLength\": ${response.contentLength},\n\t\"api\": \"${request.metrics.api}\",\n\t\"application\": \"${request.metrics.application}\",\n\t\"plan\": \"${request.metrics.plan}\",\n\t\"subscription\": \"${request.metrics.subscription}\",\n\t\"tenant\": \"${request.metrics.tenant}\",\n\t\"host\": \"${request.metrics.host}\",\n\t\"proxyResponseTimeMs\": ${request.metrics.proxyResponseTimeMs},\n\t\"proxyLatencyMs\": ${request.metrics.proxyLatencyMs},\n\t\"apiResponseTimeMs\": ${request.metrics.apiResponseTimeMs},\n\t\"user\": \"${request.metrics.user}\",\n\t\"userAgent\": \"${request.metrics.userAgent}\",\n\t\"errorKey\": \"${request.metrics.errorKey}\",\n\t\"zone\": \"${request.metrics.zone}\"\n}"}
}
```
{% endtab %}
{% endtabs %}

## Configuration

The payload sent to a custom endpoint can be configured using the [Freemarker](https://freemarker.apache.org/) template engine. For example:

```ftl
{
    "id": "${request.id}",
    "transaction": "${request.transactionId}",
    "status": "${response.statusCode}"
}
```

### Phases

The phases checked below are supported by the `metrics-reporter` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `metrics-reporter` policy with the following options:

<table><thead><tr><th width="396">Property key</th><th>Description</th></tr></thead><tbody><tr><td><code>request.requestId</code></td><td>The request ID</td></tr><tr><td><code>request.transactionId</code></td><td>The transaction ID</td></tr><tr><td><code>request.headers</code></td><td>The request’s HTTP headers</td></tr><tr><td><code>request.params</code></td><td>The request’s query parameters</td></tr><tr><td><code>request.method</code></td><td>The HTTP method used by the consumer</td></tr><tr><td><code>request.uri</code></td><td>The request’s URI</td></tr><tr><td><code>request.path</code></td><td>The request’s path</td></tr><tr><td><code>request.scheme</code></td><td>The request’s scheme</td></tr><tr><td><code>request.localAddress</code></td><td>The IP address of the API Gateway</td></tr><tr><td><code>request.remoteAddress</code></td><td>The IP address of the consumer</td></tr><tr><td><code>request.contentLength</code></td><td>The size of the request payload</td></tr><tr><td><code>response.statusCode</code></td><td>The response’s HTTP status code</td></tr><tr><td><code>response.statusReason</code></td><td>The response’s HTTP status reason</td></tr><tr><td><code>response.headers</code></td><td>The response’s HTTP headers</td></tr><tr><td><code>response.contentLength</code></td><td>The size of the response payload</td></tr><tr><td><code>request.metrics.api</code></td><td>The ID of the API</td></tr><tr><td><code>request.metrics.application</code></td><td>The ID of the consuming application</td></tr><tr><td><code>request.metrics.plan</code></td><td>The ID of the plan</td></tr><tr><td><code>request.metrics.subscription</code></td><td>The ID of the subscription</td></tr><tr><td><code>request.metrics.tenant</code></td><td>The tenant value (from the Gateway)</td></tr><tr><td><code>request.metrics.host</code></td><td>The value of the <code>Host</code> header</td></tr><tr><td><code>request.metrics.proxyResponseTimeMs</code></td><td>The global response time to process and respond to the consumer</td></tr><tr><td><code>request.metrics.proxyLatencyMs</code></td><td>The latency of the Gateway to apply policies</td></tr><tr><td><code>request.metrics.apiResponseTimeMs</code></td><td>The response time spent to call the backend upstream</td></tr><tr><td><code>request.metrics.user</code></td><td>The end user who’s making the call (in case of OAuth2 / JWT / Basic Auth)</td></tr><tr><td><code>request.metrics.userAgent</code></td><td>The value of the <code>user-agent</code> header</td></tr><tr><td><code>request.metrics.errorKey</code></td><td>The key of the error if the policy chain is failing</td></tr><tr><td><code>request.metrics.zone</code></td><td>The zone of the Gateway</td></tr><tr><td><code>request.metrics.customMetrics</code></td><td>A dictionary of custom metrics (if policy custom-metrics is used)</td></tr><tr><td><code>context.attributes['my-attribute']</code></td><td>Get the value of the <code>my-attribute</code> attribute</td></tr></tbody></table>

## Compatibility matrix

The following is the compatibility matrix for APIM and the `metrics-reporter` policy:

| Plugin version | Supported APIM versions |
| -------------- | ----------------------- |
| 1.0.x+         | 3.9.x                   |
| 1.1.x+         | 3.10.x to 3.14.x        |
| 1.2.x+         | 3.15.x to 3.17.x        |
| 2.x+           | 3.18.x+                 |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-metrics-reporter/blob/master/CHANGELOG.md" %}
