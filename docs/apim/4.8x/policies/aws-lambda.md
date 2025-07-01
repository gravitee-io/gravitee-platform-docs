---
hidden: true
---

# AWS Lambda

## Overview

The AWS Lambda policy can be used to request a Lambda instead of or in addition to the backend.

By default, the lambda is called in addition to the backend, meaning the consumer will not receive the response from Lambda.

A lambda can be defined through IAM roles instead of providing a client secret. If the client ID and secret are left blank, the policy will use the machine identification.

## Examples

{% hint style="warning" %}
This policy can be applied to v2 APIs, v4 HTTP proxy APIs, and v4 message APIs. It cannot be applied to v4 TCP proxy APIs.
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

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="203.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>true</td><td>onResponse</td><td>true</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

### Options

You can configure the `aws-lambda` policy with the following options:

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>The scope on which to apply the policy (only relevant for v2 APIs).</td><td>string</td><td>REQUEST</td></tr><tr><td>region</td><td>true</td><td>The AWS region.</td><td>string</td><td>us-east-1</td></tr><tr><td>accessKey</td><td>false</td><td>The AWS Access Key.</td><td>string</td><td>-</td></tr><tr><td>secretKey</td><td>false</td><td>The AWS Secret Key.</td><td>string</td><td>-</td></tr><tr><td>function</td><td>true</td><td>The name of the AWS Lambda function to call.</td><td>string</td><td>-</td></tr><tr><td>payload</td><td>false</td><td>The payload of the request to the AWS Lambda function.</td><td>string</td><td>-</td></tr><tr><td>variables</td><td>false</td><td>The variables to set in the execution context when retrieving the content of the HTTP call (supports EL).</td><td>List of variables</td><td>-</td></tr><tr><td>sendToConsumer</td><td>false</td><td>Check this option if you want to send the response of the lambda to the initial consumer without going to the final upstream (endpoints) selected by the Gateway.</td><td>boolean</td><td>false</td></tr><tr><td>invocationType</td><td>true</td><td><p><strong>RequestResponse (default) –</strong> Invoke the function synchronously. Keep the connection open until the function returns a response or times out. The API response includes the function response and additional data.</p><p><strong>Event –</strong> Invoke the function asynchronously. Send events that fail multiple times to the function’s dead-letter queue (if one is configured). The API response only includes a status code. <strong>DryRun –</strong> Validate parameter values and verify that the user or role has permission to invoke the function.</p></td><td>string</td><td>RequestResponse</td></tr><tr><td>qualifier</td><td>false</td><td>Specify a version or alias to invoke a published version of the function.</td><td>string</td><td>-</td></tr><tr><td>logType</td><td>true</td><td>Set to Tail to include the execution log in the response. Applies to synchronously invoked functions only.</td><td>string</td><td>None</td></tr><tr><td>roleArn</td><td>false</td><td>The arn of the role to be assumed. This is used when authentication is relying on the AWS Security Token Service (STS) to assume a Role and create temporary, short-lived sessions to use for authentication.</td><td>string</td><td>-</td></tr><tr><td>roleSessionName</td><td>false</td><td>An identifier for the assumed role session. Only used when authentication is based on AWS Security Token Service (STS).</td><td>string</td><td>gravitee</td></tr></tbody></table>

## Compatibility Matrix

The following is the compatibility matrix for APIM and the `aws-lambda` policy:

<table data-full-width="false"><thead><tr><th>Plugin Version</th><th>Supported APIM versions</th><th>JDK version</th></tr></thead><tbody><tr><td>2.x</td><td>4.7.x and later</td><td>21</td></tr><tr><td>1.x</td><td>3.x to 4.6.x</td><td>17</td></tr></tbody></table>

## Errors

| HTTP status code | Message                   |
| ---------------- | ------------------------- |
| `500`            | Request processing broken |

You can override the default response provided by the policy with the response templates feature. These templates must be defined at the API level with the APIM Console **APIs >** **Entrypoints > Response Templates** function.

The error keys sent by this policy are as follows:

<table><thead><tr><th width="356">Key</th><th>Default status</th><th>Parameters</th></tr></thead><tbody><tr><td>AWS_LAMBDA_INVALID_RESPONSE</td><td>500</td><td>-</td></tr><tr><td>AWS_LAMBDA_INVALID_STATUS_CODE</td><td>400</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-aws-lambda/blob/master/CHANGELOG.md" %}
