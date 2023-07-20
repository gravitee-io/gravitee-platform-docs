---
description: This page provides the technical details of the Request Content Limit policy
---

# Request Content Limit

## Overview

Functional and implementation information for the Request Content Limit policy is organized into the following sections:

* [Configuration](template-policy-rework-structure-26.md#configuration)
* [Compatibility](template-policy-rework-structure-26.md#compatibility-matrix)
* [Errors](template-policy-rework-structure-26.md#errors)
* [Changelogs](template-policy-rework-structure-26.md#changelogs)

{% hint style="warning" %}
This example will work for [v2 APIs and v4 proxy APIs.](../../overview/gravitee-api-definitions-and-execution-engines.md)

Currently, this policy can **not** be applied at the message level.
{% endhint %}

You can use the `request-content-limit` policy to specify a maximum request content length allowed. This limit is compared to the content length header of the request.

## Configuration

Policies can be added to flows that are assigned to an API or to a plan. Gravitee supports configuring policies [through the Policy Studio](../../guides/policy-design/) in the Management Console or interacting directly with the Management API.

When using the Management API, policies are added as flows either directly to an API or to a plan. To learn more about the structure of the Management API, check out the [reference documentation here.](../management-api-reference/)

{% code title="Sample Configuration" %}
```json
"request-content-limit": {
  "limit": 1000
}
```
{% endcode %}

### Reference

<table><thead><tr><th>Property</th><th data-type="checkbox">Required</th><th>Description</th><th>Type</th></tr></thead><tbody><tr><td>limit</td><td>true</td><td>Maximum length of request content allowed</td><td>int</td></tr></tbody></table>

### Phases

Policies can be applied to the request or the response of a Gateway API transaction. The request and response are broken up into [phases](broken-reference) that depend on the [Gateway API version](../../overview/gravitee-api-definitions-and-execution-engines.md). Each policy is compatible with a subset of the available phases.

The phases checked below are supported by the Request Content Limit policy:

<table data-full-width="false"><thead><tr><th width="209">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="188.41136671177264">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>true</td><td>onRequest</td><td>true</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>false</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>false</td></tr></tbody></table>

## Compatibility

The [changelog for each version of APIM](../../releases-and-changelog/changelog/) provides a list of policies included in the default distribution.&#x20;

## Errors

#### Default errors

| Code  | Message                                                                           |
| ----- | --------------------------------------------------------------------------------- |
| `400` | The limit from the configuration is not correct.                                  |
| `413` | Incoming HTTP request payload exceed the size limit.                              |
| `411` | The HTTP request is not chunked and does not specify the `Content-Length` header. |

#### Default response override

You can use the response template feature to override the default responses provided by the policy. These templates must be defined at the API level (see the API Console **Response Templates** option in the API **Proxy** menu).

Some possible responses are:

| Error | description                                                                                         |
| ----- | --------------------------------------------------------------------------------------------------- |
| 400   | Content-length is not a valid integer.                                                              |
| 411   | The request did not specify the length of its content, which is required by the requested resource. |
| 413   | The request is larger than the server is willing or able to process.                                |

#### Error keys

The error keys sent by this policy are as follows:

| Key                                       | Parameters     |
| ----------------------------------------- | -------------- |
| REQUEST\_CONTENT\_LIMIT\_TOO\_LARGE       | length - limit |
| REQUEST\_CONTENT\_LIMIT\_LENGTH\_REQUIRED | limit          |

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-request-content-limit/blob/master/CHANGELOG.md" %}
