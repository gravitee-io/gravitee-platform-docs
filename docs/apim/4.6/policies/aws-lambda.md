---
description: This page provides the technical details of the AWS Lambda policy
hidden: true
---

# AWS Lambda

## Overview

The AWS Lambda policy can be used to request a Lambda instead of or in addition to the backend.

By default, the Lambda is called in addition to the backend, meaning the consumer will not receive the response from the Lambda.

Functional and implementation information for the `aws-lambda` policy is organized into the following sections:

* [Examples](aws-lambda.md#examples)
* [Configuration](aws-lambda.md#configuration)
* [Errors](aws-lambda.md#errors)
* [Changelogs](aws-lambda.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can only be applied to v2 APIs. It cannot be applied to v4 message APIs or v4 proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="HTTP proxy API example" %}
Sample policy configuration:

```json
"configuration": {
    "variables": [
      {
        "name": "lambdaResponse",
        "value": "{#jsonPath(#lambdaResponse.content, '$')}"
      }
    ],
    "secretKey": "secretKey",
    "accessKey":"accessKey",
    "payload": "{ \"key\": \"value\" }",
    "scope": "REQUEST",
    "function": "lambda-example",
    "region": "us-east-1",
    "sendToConsumer": true,
    "endpoint": "http://aws-lambda-url/function"
}
```
{% endtab %}
{% endtabs %}

## Configuration

### Phases

The phases checked below are supported by the `aws-lambda` policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="203.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `aws-lambda` policy with the following options:

<table><thead><tr><th width="186">Property</th><th width="115" data-type="checkbox">Required</th><th width="199">Description</th><th width="105">Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>The scope on which apply the policy</td><td>string</td><td>REQUEST</td></tr><tr><td>region</td><td>true</td><td>The AWS region</td><td>string</td><td>us-east-1</td></tr><tr><td>accessKey</td><td>false</td><td>AWS Access Key</td><td>string</td><td>-</td></tr><tr><td>secretKey</td><td>false</td><td>AWS Secret Key</td><td>string</td><td>-</td></tr><tr><td>function</td><td>true</td><td>The name of the AWS Lambda function to call</td><td>string</td><td>-</td></tr><tr><td>payload</td><td>false</td><td>Payload of the request to AWS Lambda function</td><td>string</td><td>-</td></tr><tr><td>variables</td><td>false</td><td>The variables to set in the execution context when retrieving content of HTTP call (support EL)</td><td>List of variables</td><td>-</td></tr><tr><td>sendToConsumer</td><td>false</td><td>Check this option if you want to send the response of the lambda to the initial consumer without going to the final upstream (endpoints) selected by the gateway.</td><td>boolean</td><td>false</td></tr></tbody></table>

## Errors

| HTTP status code | Message                   |
| ---------------- | ------------------------- |
| `500`            | Request processing broken |

You can override the default response provided by the policy with the response templates feature. These templates must be defined at the API level with the APIM Console **Proxy > Response Templates** function.

The error keys sent by this policy are as follows:

<table><thead><tr><th width="356">Key</th><th>Default status</th><th>Parameters</th></tr></thead><tbody><tr><td>AWS_LAMBDA_INVALID_RESPONSE</td><td>500</td><td>-</td></tr><tr><td>AWS_LAMBDA_INVALID_STATUS_CODE</td><td>400</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-xml/blob/master/CHANGELOG.md" %}
