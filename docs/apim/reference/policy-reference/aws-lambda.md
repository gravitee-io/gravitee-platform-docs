---
description: This page provides the technical details of the AWS Lambda policy
---

# AWS Lambda

## Overview

Functional and implementation information for the AWS Lambda policy is organized into the following sections:

* [Configuration](aws-lambda.md#configuration)
* [Compatibility](aws-lambda.md#compatibility)
* [Errors](aws-lambda.md#errors)
* [Changelogs](aws-lambda.md#changelogs)

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

The AWS Lambda policy can be used to request a Lambda instead of or in addition to the backend.

By default, the Lambda is called in addition to the backend, meaning the consumer will not receive the response from the Lambda.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
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
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td>scope</td><td>true</td><td>The scope on which apply the policy</td><td>string</td><td>REQUEST</td></tr><tr><td>region</td><td>true</td><td>The AWS region</td><td>string</td><td>us-east-1</td></tr><tr><td>accessKey</td><td>false</td><td>AWS Access Key</td><td>string</td><td>-</td></tr><tr><td>secretKey</td><td>false</td><td>AWS Secret Key</td><td>string</td><td>-</td></tr><tr><td>function</td><td>true</td><td>The name of the AWS Lambda function to call</td><td>string</td><td>-</td></tr><tr><td>payload</td><td>false</td><td>Payload of the request to AWS Lambda function</td><td>string</td><td>-</td></tr><tr><td>variables</td><td>false</td><td>The variables to set in the execution context when retrieving content of HTTP call (support EL)</td><td>List of variables</td><td>-</td></tr><tr><td>sendToConsumer</td><td>false</td><td>Check this option if you want to send the response of the lambda to the initial consumer without going to the final upstream (endpoints) selected by the gateway.</td><td>boolean</td><td>false</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into phases that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the AWS Lambda policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>true</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>true</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Errors

#### Default error <a href="#user-content-default-error" id="user-content-default-error"></a>

| Code  | Message                   |
| ----- | ------------------------- |
| `500` | Request processing broken |

#### Override errors <a href="#user-content-override-errors" id="user-content-override-errors"></a>

You can override the default response provided by the policy with the response templates feature. These templates must be defined at the API level with the APIM Console **Proxy > Response Templates** function.

The error keys sent by this policy are as follows:

| Key                                | Default status | Parameters |
| ---------------------------------- | -------------- | ---------- |
| AWS\_LAMBDA\_INVALID\_RESPONSE     | 500            | -          |
| AWS\_LAMBDA\_INVALID\_STATUS\_CODE | 400            | -          |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-json-xml/blob/master/CHANGELOG.md" %}
