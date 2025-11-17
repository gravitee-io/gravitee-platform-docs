---
description: This page provides the technical details of the Message Filtering policy
---

# Message Filtering

{% hint style="warning" %}
**This feature requires** [**Gravitee's Enterprise Edition**](../../overview/gravitee-apim-enterprise-edition/README.md)**.**
{% endhint %}

## Overview

The `message-filtering` policy enables the API publisher to create and enforce a filter that controls which messages are streamed to the subscriber/consumer, given a defined set of criteria.&#x20;

Functional and implementation information for the `message-filtering` policy is organized into the following sections:

* [Examples](message-filtering.md#examples)
* [Configuration](message-filtering.md#configuration)
* [Changelogs](message-filtering.md#changelogs)

## Examples

{% hint style="warning" %}
This policy can be applied to v4 message APIs. It cannot be applied to v2 APIs or v4 proxy APIs.
{% endhint %}

{% tabs %}
{% tab title="Message API example" %}
If this is my message:

```json
{
    "productId": "1234",
    "value": "any value"
}
```

I will be able to filter any messages according to subscriptions metadata `productId` by configuring the policy as follows:

```json
 {
    "name": "Products filter",
    "description": "Filter messages based on subscription product id",
    "enabled": true,
    "policy": "message-filtering",
    "configuration": {
        "filter": "#jsonPath(#message.content, '$.productId') == '#subscription.metadata.productId'"
    }
}
```
{% endtab %}
{% endtabs %}

## Configuration

Sample policy configuration:

{% code title="Sample Configuration" %}
```json
{
  "name": "Message filtering",
  "description": "Apply filter to messages",
  "enabled": true,
  "policy": "message-filtering",
  "configuration": {
    "filter": "{#jsonPath(#message.content, '$.feature') == #subscription.metadata.feature}"
  }
}
```
{% endcode %}

### Phases

The phases checked below are supported by the `message-filtering` policy:

<table data-full-width="false"><thead><tr><th width="202">v2 Phases</th><th width="139" data-type="checkbox">Compatible?</th><th width="198">v4 Phases</th><th data-type="checkbox">Compatible?</th></tr></thead><tbody><tr><td>onRequest</td><td>false</td><td>onRequest</td><td>false</td></tr><tr><td>onResponse</td><td>false</td><td>onResponse</td><td>false</td></tr><tr><td>onRequestContent</td><td>false</td><td>onMessageRequest</td><td>true</td></tr><tr><td>onResponseContent</td><td>false</td><td>onMessageResponse</td><td>true</td></tr></tbody></table>

### Options

You can configure the `message-filtering` policy with the following options:

<table><thead><tr><th width="116">Property</th><th width="105" data-type="checkbox">Required</th><th width="152">Description</th><th width="100">Type</th><th>Default</th></tr></thead><tbody><tr><td>filter</td><td>true</td><td>The filter's rule</td><td>string</td><td>-</td></tr></tbody></table>

## Changelogs

{% @github-files/github-code-block url="https://github.com/gravitee-io/gravitee-policy-message-filtering/blob/master/CHANGELOG.md" %}
