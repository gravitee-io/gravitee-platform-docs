= Metrics Reporter policy

ifdef::env-github[]
image:https://img.shields.io/static/v1?label=Available%20at&message=Gravitee.io&color=1EC9D2["Gravitee.io", link="https://download.gravitee.io/#graviteeio-apim/plugins/policies/gravitee-policy-metrics-reporter/"]
image:https://img.shields.io/badge/License-Apache%202.0-blue.svg["License", link="https://github.com/gravitee-io/gravitee-policy-metrics-reporter/blob/master/LICENSE.txt"]
image:https://img.shields.io/badge/semantic--release-conventional%20commits-e10079?logo=semantic-release["Releases", link="https://github.com/gravitee-io/gravitee-policy-metrics-reporter/releases"]
image:https://circleci.com/gh/gravitee-io/gravitee-policy-metrics-reporter.svg?style=svg["CircleCI", link="https://circleci.com/gh/gravitee-io/gravitee-policy-metrics-reporter"]
image:https://f.hubspotusercontent40.net/hubfs/7600448/gravitee-github-button.jpg["Join the community forum", link="https://community.gravitee.io?utm_source=readme", height=20]
endif::[]


== Phase

[cols="^2,^2,^2,^2",options="header"]
|===
|onRequest|onResponse|onRequestContent|onResponseContent

|
|
|
|X

|===

== Description

This policy allows you to push the request metrics to a custom endpoint.

Running this policy ensure that the complete response is already send to the initial consumer.

You can configure the payload to send to the custom endpoint by using the https://freemarker.apache.org[Freemarker^]
template engine.

Example:

```
{
    "id": "${request.id}",
    "transaction": "${request.transactionId}",
    "status": "${response.statusCode}"
}
```


== Compatibility with APIM

|===
|Plugin version | APIM version

|2.x and upper                  | 3.18.x to latest
|1.2.x and upper                | 3.15.x to 3.17.x
|1.1.x and upper                | 3.10.x to 3.14.x
|1.0.x and upper                | 3.9.x
|===

== Properties

[cols="^2,^2",options="header"]
|===
|key|description

| request.requestId
| The request ID

| request.transactionId
| The Transaction ID

| request.headers
| The request's HTTP headers

| request.params
| The request's query parameters

| request.method
| The HTTP method used by the consumer

| request.uri
| The request's URI

| request.path
| The request's path

| request.scheme
| The request's scheme

| request.localAddress
| The IP address of the API Gateway

| request.remoteAddress
| The IP address of the consumer

| request.contentLength
| The size of the request payload

| response.statusCode
| The response's HTTP status code

| response.statusReason
| The response's HTTP status reason

| response.headers
| The response's HTTP headers

| response.contentLength
| The size of the response payload

| request.metrics.api
| The ID of the API

| request.metrics.application
| The ID of the consuming application

| request.metrics.plan
| The ID of the plan

| request.metrics.subscription
| The ID of the subscription

| request.metrics.tenant
| The tenant value (from the gateway)

| request.metrics.host
| The value of the `Host` header

| request.metrics.proxyResponseTimeMs
| The global response time to process and respond to the consumer

| request.metrics.proxyLatencyMs
| The latency of the gateway to apply policies

| request.metrics.apiResponseTimeMs
| The response time spend to call the backend upstream

| request.metrics.user
| The end-user who's doing the call (in case of OAuth2 / JWT / Basic Auth)

| request.metrics.userAgent
| The value of the `user-agent` header

| request.metrics.errorKey
| The key of the error if the policy chain is failing

| request.metrics.zone
| The zone of the gateway

| request.metrics.customMetrics
| A dictionary of custom metrics (if policy custom-metrics is used)

| context.attributes['my-attribute']
| Get the value of the `my-attribute` attribute

|===

== Example

```
"metrics-reporter": {
	"method":"POST",
	"url":"https://my_custom_endpoint/report",
	"body":"{\n\t\"requestId\": \"${request.requestId}\",\n\t\"transactionId\": \"${request.transactionId}\",\n\t\"headers\": \"${request.headers}\",\n\t\"params\": \"${request.params}\",\n\t\"method\": \"${request.method}\",\n\t\"uri\": \"${request.uri}\",\n\t\"path\": \"${request.path}\",\n\t\"scheme\": \"${request.scheme}\",\n\t\"localAddress\": \"${request.localAddress}\",\n\t\"remoteAddress\": \"${request.remoteAddress}\",\n\t\"contentLength\": ${request.contentLength},\n\t\"statusCode\": ${response.statusCode},\n\t\"statusReason\": \"${response.statusReason}\",\n\t\"headers\": \"${response.headers}\",\n\t\"contentLength\": ${response.contentLength},\n\t\"api\": \"${request.metrics.api}\",\n\t\"application\": \"${request.metrics.application}\",\n\t\"plan\": \"${request.metrics.plan}\",\n\t\"subscription\": \"${request.metrics.subscription}\",\n\t\"tenant\": \"${request.metrics.tenant}\",\n\t\"host\": \"${request.metrics.host}\",\n\t\"proxyResponseTimeMs\": ${request.metrics.proxyResponseTimeMs},\n\t\"proxyLatencyMs\": ${request.metrics.proxyLatencyMs},\n\t\"apiResponseTimeMs\": ${request.metrics.apiResponseTimeMs},\n\t\"user\": \"${request.metrics.user}\",\n\t\"userAgent\": \"${request.metrics.userAgent}\",\n\t\"errorKey\": \"${request.metrics.errorKey}\",\n\t\"zone\": \"${request.metrics.zone}\"\n}"}
}
```
